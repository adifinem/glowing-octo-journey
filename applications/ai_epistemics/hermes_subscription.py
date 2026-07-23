#!/usr/bin/env python3
"""Minimal, auditable ChatGPT-subscription Responses harness via Hermes OAuth.

This module deliberately bypasses both the Codex CLI product harness and the
Hermes agent loop. It reuses Hermes only for credential refresh, required HTTP
headers, Responses message conversion, encrypted-reasoning replay, cache keys,
and robust SSE assembly. Callers provide the complete system instruction and
the complete function-tool allowlist.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

HERMES_SOURCE = Path('/home/j/.hermes/hermes-agent')
if str(HERMES_SOURCE) not in sys.path:
    # Append rather than prepend: the slim harness must not shadow unrelated
    # installed packages (notably the MCP SDK) in a host test process.
    sys.path.append(str(HERMES_SOURCE))


def _transport():
    from agent.transports import get_transport
    import agent.transports.codex  # noqa: F401

    return get_transport('codex_responses')


def build_request(
    *,
    model: str,
    system: str,
    history: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None,
    session_id: str,
    effort: str = 'high',
) -> dict[str, Any]:
    """Build one store-free Codex-backend request with an exact custom system.

    `max_output_tokens` is intentionally absent: chatgpt.com's subscription
    backend rejects it. That is a registered harness difference, not something
    this module hides or silently emulates.
    """
    if not isinstance(system, str) or not system.strip():
        raise ValueError('system must be a non-empty frozen instruction string')
    if effort not in {'low', 'medium', 'high', 'xhigh', 'max'}:
        raise ValueError(f'unsupported reasoning effort: {effort!r}')
    if not isinstance(history, list) or not history:
        raise ValueError('history must contain at least one message')

    request = _transport().build_kwargs(
        model=model,
        messages=[{'role': 'system', 'content': system}, *history],
        tools=tools or [],
        reasoning_config={'enabled': True, 'effort': effort},
        session_id=session_id,
        is_codex_backend=True,
        replay_encrypted_reasoning=True,
    )
    # Defensive experiment invariants. The generic transport currently already
    # enforces these for Codex, but fail closed if upstream behavior changes.
    if request.get('instructions') != system:
        raise RuntimeError('Hermes transport altered the frozen system instruction')
    request['store'] = False
    request.pop('max_output_tokens', None)
    cache_material = json.dumps(
        {'model': model, 'system': system, 'tools': tools or [], 'session_id': session_id},
        sort_keys=True, separators=(',', ':'),
    )
    request['prompt_cache_key'] = 'pck_' + hashlib.sha256(cache_material.encode()).hexdigest()[:48]
    if not tools:
        request.pop('tools', None)
        request.pop('tool_choice', None)
        request.pop('parallel_tool_calls', None)
    return request


def model_available(model: str, live_catalog: list[str]) -> bool:
    """Exact-slug availability only; do not equate rolling with dated models."""
    return model in set(live_catalog)


def live_catalog() -> list[str]:
    """Fetch only models returned live by ChatGPT; never synthetic fallbacks."""
    from hermes_cli.auth import resolve_codex_runtime_credentials
    from hermes_cli.codex_models import _fetch_models_from_api

    credentials = resolve_codex_runtime_credentials()
    return _fetch_models_from_api(credentials['api_key'])


def create_raw_client(model: str):
    """Return Hermes' raw OpenAI client configured for ChatGPT OAuth."""
    from agent.auxiliary_client import resolve_provider_client

    client, resolved_model = resolve_provider_client(
        'openai-codex', model=model, raw_codex=True,
    )
    if client is None:
        raise RuntimeError('Hermes could not resolve ChatGPT subscription credentials')
    if resolved_model != model:
        raise RuntimeError(
            f'model resolution drift: requested {model!r}, resolved {resolved_model!r}'
        )
    return client


def stream_response(client, request: dict[str, Any]):
    """Execute and robustly assemble raw Responses SSE events."""
    from agent.codex_runtime import _consume_codex_event_stream

    payload = dict(request)
    payload['stream'] = True
    event_stream = client.responses.create(**payload)
    try:
        response = _consume_codex_event_stream(
            event_stream, model=str(payload['model']),
        )
    finally:
        close = getattr(event_stream, 'close', None)
        if callable(close):
            close()
    if response is None:
        raise RuntimeError('subscription Responses stream returned no response')
    return response


def to_jsonable(value: Any) -> Any:
    """Lossless-enough recursive conversion for raw artifact persistence."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    model_dump = getattr(value, 'model_dump', None)
    if callable(model_dump):
        return to_jsonable(model_dump(mode='json'))
    if hasattr(value, '__dict__'):
        return {
            str(k): to_jsonable(v)
            for k, v in vars(value).items()
            if not str(k).startswith('_')
        }
    return str(value)


def extract_turn(response: Any) -> dict[str, Any]:
    """Normalize response text/tool calls and construct replayable history."""
    transport = _transport()
    normalized = transport.normalize_response(
        response, issuer_kind='codex_backend',
    )
    assistant: dict[str, Any] = {
        'role': 'assistant',
        'content': normalized.content or '',
    }
    if normalized.provider_data:
        assistant.update(normalized.provider_data)

    tool_calls = []
    for index, call in enumerate(normalized.tool_calls or []):
        provider_data = call.provider_data or {}
        call_id = provider_data.get('call_id') or call.id or f'call_{index}'
        response_item_id = provider_data.get('response_item_id')
        embedded_id = (
            f'{call_id}|{response_item_id}' if response_item_id else call_id
        )
        tool_calls.append({
            'id': embedded_id,
            'call_id': call_id,
            'response_item_id': response_item_id,
            'type': 'function',
            'function': {
                'name': call.name,
                'arguments': call.arguments,
            },
        })
    if tool_calls:
        assistant['tool_calls'] = tool_calls

    return {
        'text': normalized.content or '',
        'finish_reason': normalized.finish_reason,
        'assistant': assistant,
        'tool_calls': tool_calls,
        'raw': to_jsonable(response),
    }


def call_once(
    *, model: str, system: str, history: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None, session_id: str,
    effort: str = 'high', client=None,
) -> dict[str, Any]:
    """Convenience one-call entry point used by smoke tests and runners."""
    request = build_request(
        model=model, system=system, history=history, tools=tools,
        session_id=session_id, effort=effort,
    )
    live_client = client or create_raw_client(model)
    return extract_turn(stream_response(live_client, request))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--catalog', action='store_true')
    args = parser.parse_args()
    if args.catalog:
        print(json.dumps(live_catalog(), indent=2))
