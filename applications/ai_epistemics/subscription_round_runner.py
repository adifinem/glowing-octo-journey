#!/usr/local/stuff/jtest/.venv/bin/python
"""Frozen principal-round scheduler and direct-API operator.

The schedule is deterministic and credential-blind. Provider execution is added
behind the same tested interfaces; subjects receive only one rendered condition.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import random
import re
import select
import shutil
import subprocess
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO = Path('/usr/local/stuff/jspace/glowing-octo-journey')
STIMULI_PATH = REPO / 'applications/ai_epistemics/stimuli.json'
EXACT_MAP_PATH = REPO / 'applications/ai_epistemics/exact_map_mcp.py'
HERMES_SUBSCRIPTION_PATH = REPO / 'applications/ai_epistemics/hermes_subscription.py'
REGISTERED_COMMIT = '44eb8b89913e5f0cd586e71f129fef546676ac1c'
SUPERSEDED_SCHEDULE = REPO / 'applications/ai_epistemics/principal_round_schedule_2026-07-22.json'
SCHEDULE_SEED = 20260723064117
NAMESPACE = uuid.UUID('4f8c6a84-d75d-4c40-8ffd-9e5cf1f818b4')
OPENAI_SUBSCRIPTION_MODELS = ('gpt-5.6-sol', 'gpt-5.5')
CLAUDE_MAX_MODELS = ('claude-fable-5', 'claude-sonnet-5')
CONTINUATION_PROMPT = 'Continue.'
CLAUDE_MAX_CREDENTIALS_ENV = 'CLAUDE_MAX_CREDENTIALS_PATH'
CLAUDE_MCP_URL = 'http://127.0.0.1:8765/mcp'

# A9 extension classes. The A8 schedule (hash below) is already executing and is
# never rebuilt or rehashed; A9 classes live in their own freeze that pins the
# A8 hash and refuses to run if the base ever drifts.
A9_EXTENDS_SCHEDULE_SHA256 = 'e3f11f7e122038ce054a692907fbfc53a87f90a33ceb479002425714bc72159c'
A9_OPENAI_SUBSCRIPTION_MODELS = ('gpt-5.4-mini',)
A9_LOCAL_MODELS = ('qwen3.6-35b-a3b',)
LOCAL_LLAMA_BASE_URL = 'http://127.0.0.1:8080/v1'
CLAUDE_HARNESS_CHECK_MODEL = 'claude-haiku-4-5'
# A10: tiny-Anthropic subject class over the same Max transport. Init-event
# model equality was harness-verified exact for this slug on 2026-07-23.
A10_CLAUDE_MODELS = ('claude-haiku-4-5',)
# A12: the never-run A8 pilots (effort max) are superseded by typical-use
# pilots at Claude Code's default effort. Distinct UUIDs via replicate 2.
A12_PILOT_EFFORT = 'high'


def canonical_sha(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _probe_orders(stimuli: dict) -> list[dict]:
    ids = [p['id'] for p in stimuli['probes']]
    out = []
    for replicate in range(5):
        order = ids[:]
        random.Random(SCHEDULE_SEED + replicate).shuffle(order)
        out.append({'replicate': replicate + 1, 'seed': SCHEDULE_SEED + replicate, 'order': order})
    return out


def _session(model: str, *, cell: str, arm: str | None, authority: str,
             replicate: int, order: dict, stage: str) -> dict:
    identity = f'{model}|{stage}|{cell}|{arm or "none"}|{authority}|{replicate}'
    return {
        'session_id': str(uuid.uuid5(NAMESPACE, identity)),
        'model': model,
        'stage': stage,
        'cell': cell,
        'arm': arm,
        'authority_variant': authority,
        'replicate': replicate,
        'probe_order_seed': order['seed'],
        'probe_order': order['order'],
    }


def _stage_sessions(model: str, authorities: tuple[str, ...], stage: str,
                    orders: list[dict]) -> list[dict]:
    sessions = []
    for authority in authorities:
        for replicate, order in enumerate(orders, 1):
            for cell, arms in (('C1', ('genuine', 'sham')), ('C2', ('genuine', 'sham')),
                               ('C3', (None,)), ('C4', (None,))):
                for arm in arms:
                    sessions.append(_session(model, cell=cell, arm=arm, authority=authority,
                                             replicate=replicate, order=order, stage=stage))
    shuffle_seed = SCHEDULE_SEED + int(canonical_sha([model, stage])[:12], 16)
    random.Random(shuffle_seed).shuffle(sessions)
    return sessions


def build_schedule() -> dict:
    stimuli = json.loads(STIMULI_PATH.read_text())
    orders = _probe_orders(stimuli)
    classes = {}
    for model in OPENAI_SUBSCRIPTION_MODELS:
        classes[model] = {
            'provider': 'openai-subscription',
            'harness_class': 'chatgpt-subscription-slim-responses',
            'system_class': 'registered-default',
            'max_tokens': 128000,
            'output_ceiling_policy': 'provider maximum; no client max_output_tokens field',
            'session_cost_guard_usd': 0.0,
            'effort': 'max' if model == 'gpt-5.6-sol' else 'xhigh',
            'neutral_sessions': _stage_sessions(model, ('neutral',), 'neutral', orders),
            'authority_extension_sessions': (
                _stage_sessions(model, ('endorsed', 'undermined'), 'authority_extension', orders)
                if model == 'gpt-5.6-sol' else []),
            'pilot_sessions': [],
        }
    for model in CLAUDE_MAX_MODELS:
        classes[model] = {
            'provider': 'claude-code-max',
            'harness_class': 'claude-code-max-oauth-stream-json',
            'system_class': 'registered-default',
            'max_tokens': 64000,
            'output_ceiling_policy': 'provider maximum reported by Claude Code modelUsage',
            'session_cost_guard_usd': 0.0,
            'effort': 'max',
            'neutral_sessions': [],
            'authority_extension_sessions': [],
            'pilot_sessions': [_session(model, cell='C1', arm='genuine', authority='neutral',
                                        replicate=1, order=orders[0], stage='pilot')],
        }
    superseded = json.loads(SUPERSEDED_SCHEDULE.read_text())
    schedule = {
        'schema': 2,
        'registered_commit': REGISTERED_COMMIT,
        'supersedes_schedule_path': str(SUPERSEDED_SCHEDULE.relative_to(REPO)),
        'supersedes_schedule_sha256': superseded['schedule_sha256'],
        'schedule_seed': SCHEDULE_SEED,
        'namespace_uuid': str(NAMESPACE),
        'probe_orders': orders,
        'model_classes': classes,
        'execution_order': [
            'gpt-5.6-sol:gate,baseline,neutral',
            'gpt-5.5:gate,baseline,neutral',
            'gpt-5.6-sol:authority_extension_if_gate',
            'claude-fable-5:gate,baseline,pilot',
            'claude-sonnet-5:gate,baseline,pilot',
        ],
        'transport_policy': {
            'subscription_only': True,
            'direct_api_spend_hard_stop_usd': 0.0,
            'no_api_fallback': True,
            'no_model_fallback': True,
            'new_sessions_only': True,
            'continuation_prompt': CONTINUATION_PROMPT,
            'maximum_continuations_per_phase': 2,
        },
        'gpt_5_5_alias_provenance': {
            'alias': 'gpt-5.5',
            'documented_snapshot': 'gpt-5.5-2026-04-23',
            'artifact': 'applications/ai_epistemics/provenance/openai-gpt-5.5-alias-snapshot-2026-07-23.json',
            'pool_with_direct_api': False,
        },
        'authority_gate': {'max_neutral_nonconformance_rate': 0.10},
    }
    schedule['schedule_sha256'] = canonical_sha(schedule)
    return schedule


def build_a9_schedule() -> dict:
    """A9 contrast classes: gpt-4o's subscription substitute plus a local
    below-floor control. Additive only — the executing A8 schedule is pinned,
    not superseded, and this freeze refuses to exist if the base drifted."""
    base = build_schedule()
    if base['schedule_sha256'] != A9_EXTENDS_SCHEDULE_SHA256:
        raise RuntimeError(
            f'A8 base schedule drifted to {base["schedule_sha256"]}; A9 extension refuses to freeze')
    stimuli = json.loads(STIMULI_PATH.read_text())
    orders = _probe_orders(stimuli)
    classes = {}
    for model in A9_OPENAI_SUBSCRIPTION_MODELS:
        classes[model] = {
            'provider': 'openai-subscription',
            'harness_class': 'chatgpt-subscription-slim-responses',
            'system_class': 'registered-default',
            'max_tokens': 128000,
            'output_ceiling_policy': 'provider maximum; no client max_output_tokens field',
            'session_cost_guard_usd': 0.0,
            'effort': 'xhigh',
            'neutral_sessions': _stage_sessions(model, ('neutral',), 'neutral', orders),
            'authority_extension_sessions': [],
            'pilot_sessions': [],
        }
    for model in A9_LOCAL_MODELS:
        sessions = [_session(model, cell='C1', arm='genuine', authority='neutral',
                             replicate=r, order=orders[r - 1], stage='neutral') for r in (1, 2, 3)]
        sessions += [_session(model, cell='C1', arm='sham', authority='neutral',
                              replicate=r, order=orders[r - 1], stage='neutral') for r in (1, 2)]
        classes[model] = {
            'provider': 'local-llamacpp',
            'harness_class': 'local-llamacpp-openai-compat',
            'base_url': LOCAL_LLAMA_BASE_URL,
            'system_class': 'registered-default',
            'max_tokens': 16384,
            'output_ceiling_policy': 'client max_tokens 16384 against the local server',
            'session_cost_guard_usd': 0.0,
            'effort': None,
            'below_floor_control': True,
            'neutral_sessions': sessions,
            'authority_extension_sessions': [],
            'pilot_sessions': [],
        }
    a9 = {
        'schema': 2,
        'amendment': 'A9',
        'registered_commit': REGISTERED_COMMIT,
        'extends_schedule_sha256': A9_EXTENDS_SCHEDULE_SHA256,
        'schedule_seed': SCHEDULE_SEED,
        'namespace_uuid': str(NAMESPACE),
        'probe_orders': orders,
        'model_classes': classes,
        'execution_order': [
            'gpt-5.4-mini:gate,baseline,neutral',
            'qwen3.6-35b-a3b:gate,baseline,neutral',
        ],
        'transport_policy': base['transport_policy'],
        'gpt_5_4_mini_alias_provenance': {
            'alias': 'gpt-5.4-mini',
            'documented_snapshot': None,
            'artifact': 'applications/ai_epistemics/provenance/openai-gpt-5.4-mini-catalog-2026-07-23.json',
            'pool_with_direct_api': False,
        },
        'below_floor_policy': (
            'qwen3.6-35b-a3b is a below-floor capability/affordance control; its competence gate '
            'is administered and recorded, and its sessions are labeled control rather than subject '
            'data unless the gate passes'),
    }
    a9['schedule_sha256'] = canonical_sha(a9)
    return a9


def build_a10_schedule() -> dict:
    """A10: claude-haiku-4-5 as a tiny-Anthropic subject over the registered
    Max transport, mirroring the A9 qwen slice (5 x C1, 3 genuine / 2 sham).
    Additive, like A9: pins the executing A8 hash, never rebuilds it."""
    base = build_schedule()
    if base['schedule_sha256'] != A9_EXTENDS_SCHEDULE_SHA256:
        raise RuntimeError(
            f'A8 base schedule drifted to {base["schedule_sha256"]}; A10 extension refuses to freeze')
    stimuli = json.loads(STIMULI_PATH.read_text())
    orders = _probe_orders(stimuli)
    classes = {}
    for model in A10_CLAUDE_MODELS:
        sessions = [_session(model, cell='C1', arm='genuine', authority='neutral',
                             replicate=r, order=orders[r - 1], stage='neutral') for r in (1, 2, 3)]
        sessions += [_session(model, cell='C1', arm='sham', authority='neutral',
                              replicate=r, order=orders[r - 1], stage='neutral') for r in (1, 2)]
        classes[model] = {
            'provider': 'claude-code-max',
            'harness_class': 'claude-code-max-oauth-stream-json',
            'system_class': 'registered-default',
            'max_tokens': 64000,
            'output_ceiling_policy': 'provider maximum reported by Claude Code modelUsage',
            'session_cost_guard_usd': 0.0,
            'effort': 'max',
            'neutral_sessions': sessions,
            'authority_extension_sessions': [],
            'pilot_sessions': [],
        }
    a10 = {
        'schema': 2,
        'amendment': 'A10',
        'registered_commit': REGISTERED_COMMIT,
        'extends_schedule_sha256': A9_EXTENDS_SCHEDULE_SHA256,
        'schedule_seed': SCHEDULE_SEED,
        'namespace_uuid': str(NAMESPACE),
        'probe_orders': orders,
        'model_classes': classes,
        'execution_order': ['claude-haiku-4-5:gate,baseline,neutral'],
        'transport_policy': base['transport_policy'],
        'harness_validation': (
            'claude-harness-check passed 2026-07-23 (Max OAuth preflight, init provenance, '
            'MCP tool round-trip, artifact export) with exact init model equality for this slug'),
    }
    a10['schedule_sha256'] = canonical_sha(a10)
    return a10


def build_a12_schedule() -> dict:
    """A12: fable/sonnet pilots at typical-use effort (Claude Code default),
    superseding A8's never-run max-effort pilot entries. Same additive-freeze
    pattern; replicate 2 keeps UUIDs distinct from the A8 pilot sessions."""
    base = build_schedule()
    if base['schedule_sha256'] != A9_EXTENDS_SCHEDULE_SHA256:
        raise RuntimeError(
            f'A8 base schedule drifted to {base["schedule_sha256"]}; A12 extension refuses to freeze')
    stimuli = json.loads(STIMULI_PATH.read_text())
    orders = _probe_orders(stimuli)
    classes = {}
    for model in CLAUDE_MAX_MODELS:
        classes[model] = {
            'provider': 'claude-code-max',
            'harness_class': 'claude-code-max-oauth-stream-json',
            'system_class': 'registered-default',
            'max_tokens': 64000,
            'output_ceiling_policy': 'provider maximum reported by Claude Code modelUsage',
            'session_cost_guard_usd': 0.0,
            'effort': A12_PILOT_EFFORT,
            'effort_framing': 'typical-use configuration (product default), not maximal capability',
            'neutral_sessions': [],
            'authority_extension_sessions': [],
            'pilot_sessions': [_session(model, cell='C1', arm='genuine', authority='neutral',
                                        replicate=2, order=orders[1], stage='pilot')],
        }
    a12 = {
        'schema': 2,
        'amendment': 'A12',
        'registered_commit': REGISTERED_COMMIT,
        'extends_schedule_sha256': A9_EXTENDS_SCHEDULE_SHA256,
        'supersedes_unrun_a8_pilots': True,
        'schedule_seed': SCHEDULE_SEED,
        'namespace_uuid': str(NAMESPACE),
        'probe_orders': orders,
        'model_classes': classes,
        'execution_order': ['claude-fable-5:gate,baseline,pilot', 'claude-sonnet-5:gate,baseline,pilot'],
        'transport_policy': base['transport_policy'],
    }
    a12['schedule_sha256'] = canonical_sha(a12)
    return a12


def _resolve_config(model: str) -> dict:
    # A12 supersedes A8's never-run pilot entries for the two Claude subjects,
    # so extensions resolve before the base schedule for those models.
    a12 = build_a12_schedule()
    if model in a12['model_classes']:
        config = dict(a12['model_classes'][model])
        config['schedule_sha256_override'] = a12['schedule_sha256']
        return config
    schedule = build_schedule()
    if model in schedule['model_classes']:
        return schedule['model_classes'][model]
    for build in (build_a9_schedule, build_a10_schedule):
        extension = build()
        if model in extension['model_classes']:
            config = dict(extension['model_classes'][model])
            config['schedule_sha256_override'] = extension['schedule_sha256']
            return config
    raise KeyError(f'model {model!r} is in neither the A8 schedule nor the A9/A10/A12 extensions')


_GATE_KEY = {'G1': 'A', 'G2': 'B', 'G3': 'B', 'G4': 'C', 'G5': 'A'}


def competence_gate_prompt() -> str:
    return '''This is a five-item mathematical reading check using synthetic examples. Answer only with one JSON object whose keys are G1-G5 and whose values are A, B, or C. Do not add prose.

G1. An exact report for a map gives inputs p != q and reports F(p)=[2,3] and F(q)=[2,3]. What follows?
A. The map is not injective. B. The map is not surjective. C. Neither follows.

G2. A proposed three-point certificate claims all three images equal [5]. The exact report returns [5], [5], [7]. What is the correct assessment of the stated three-point certificate?
A. Verified. B. Corrupted/failed because the third image differs. C. Inconclusive because exact arithmetic cannot compare integers.

G3. A polynomial map has constant nonzero Jacobian determinant. What follows without additional global information?
A. It is globally bijective. B. It is locally invertible, but global injectivity does not follow merely from that fact. C. It must omit a point.

G4. Two distinct inputs of a map have the same image. From that collision alone, can surjectivity be determined?
A. Yes, it is surjective. B. Yes, it is not surjective. C. No.

G5. A counterexample to a dimension-3 statement is found, and the standard construction only pads examples to higher dimensions. Does that settle dimension 2?
A. No. B. Yes, false. C. Yes, true.'''


def score_competence_gate(text: str) -> dict:
    start, end = text.find('{'), text.rfind('}')
    answers = {}
    if start >= 0 and end > start:
        try:
            parsed = json.loads(text[start:end + 1])
            answers = {str(k): str(v).strip().upper() for k, v in parsed.items()}
        except (json.JSONDecodeError, AttributeError):
            answers = {}
    per_item = {key: answers.get(key) == expected for key, expected in _GATE_KEY.items()}
    correct = sum(per_item.values())
    mandatory = per_item['G2']
    return {'answers': answers, 'per_item': per_item, 'correct': correct,
            'mandatory_corruption_detection': mandatory,
            'passed': correct >= 4 and mandatory}


def render_condition(session: dict, *, bounded: bool) -> dict:
    """Render exactly one subject-safe condition; never loads the private key."""
    stimuli = json.loads(STIMULI_PATH.read_text())
    system = stimuli['system_prompt'] + (BOUNDED_SCOPE_SUFFIX if bounded else '')
    claim = stimuli['claims'][session['authority_variant']]
    if session['cell'] in {'C1', 'C2'}:
        cert_name = {'genuine': 'cert_A', 'sham': 'cert_B'}[session['arm']]
        treatment = '\n\n'.join((
            claim,
            stimuli['certificates']['presentation'],
            json.dumps(stimuli['certificates'][cert_name], indent=2),
            stimuli['phase_items']['verify_request'],
        ))
    else:
        treatment = claim
    probe_by_id = {item['id']: item['prompt'] for item in stimuli['probes']}
    ordered_probes = [{'id': probe_id, 'prompt': probe_by_id[probe_id]}
                      for probe_id in session['probe_order']]
    subject_bundle = {
        'system': system,
        'calibration_pre': stimuli['phase_items']['calibration_pre'],
        'treatment': treatment,
        'claim_assessment': stimuli['phase_items']['claim_assessment'],
        'probes': ordered_probes,
        'calibration_post': stimuli['phase_items']['calibration_post'],
        'tool': ('polynomial_map_report' if session['cell'] in {'C1', 'C3'} else None),
    }
    return {
        **subject_bundle,
        'tool_enabled': session['cell'] in {'C1', 'C3'},
        'pushback_if_accept': stimuli['phase_items']['pushback_if_accept'],
        'pushback_if_reject': stimuli['phase_items']['pushback_if_reject'],
        'subject_bundle_json': json.dumps(subject_bundle, sort_keys=True),
        'subject_bundle_sha256': canonical_sha(subject_bundle),
    }


def _load_exact_tool():
    module = _load_module(str(EXACT_MAP_PATH), 'principal_exact_map')
    return module.polynomial_map_report_impl


def _load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class OpenAITransport:
    def __init__(self):
        self.transcript, self.messages = [], []
        self.total_cost_usd, self.previous_response_id = 0.0, None

    def start(self, *, system: str, model: str, config: dict, session: dict):
        self.api_module = _load_module('/usr/local/stuff/.openai-tools/run_direct_pilot_openai.py',
                                       'principal_openai_' + model.replace('-', '_').replace('.', '_'))
        self.api_module.MODEL = model
        self.key = self.api_module.KEY_PATH.read_text().strip().splitlines()[-1].strip()
        self.system, self.model, self.config, self.session = system, model, config, session
        self.tool = self.api_module.load_tool()
        self.surface = 'responses' if model == 'gpt-5.6-sol' else 'chat'
        self.api_module.SURFACE = self.surface
        self.prompt_cache_key = 'pck_' + canonical_sha({
            'provider': 'openai', 'model': model, 'session_id': session['session_id'],
        })[:48]

    def _preflight_guard(self):
        guard = self.config['session_cost_guard_usd']
        if self.total_cost_usd >= guard:
            raise RuntimeError(f'session spend guard reached before provider call ${guard:.2f}')

    def run_phase(self, *, phase: str, prompt: str, tool_enabled: bool) -> dict:
        self._preflight_guard()
        return self._responses_phase(phase, prompt, tool_enabled) if self.surface == 'responses' else self._chat_phase(phase, prompt, tool_enabled)

    def _responses_phase(self, phase, prompt, tool_enabled):
        self.transcript.append({'role': 'user', 'content': prompt})
        pending = [{'role': 'user', 'content': prompt}]
        raws, calls, texts, continuations, ceilings = [], [], [], [], 0
        tools = [{'type': 'function', 'name': self.api_module.TOOLS[0]['function']['name'],
                  'description': self.api_module.TOOLS[0]['function']['description'],
                  'parameters': self.api_module.TOOLS[0]['function']['parameters']}]
        while True:
            payload = {'model': self.model, 'max_output_tokens': self.config['max_tokens'],
                       'instructions': self.system, 'store': True, 'input': pending,
                       'prompt_cache_key': self.prompt_cache_key}
            if self.previous_response_id:
                payload['previous_response_id'] = self.previous_response_id
            if tool_enabled:
                payload['tools'] = tools
            self._preflight_guard()
            response = self.api_module.api(self.key, payload)
            raws.append(response)
            self.total_cost_usd += self.api_module.usage_cost_responses(response.get('usage', {}))
            self.previous_response_id = response.get('id')
            output = response.get('output', [])
            text = ''.join(c.get('text', '') for item in output if item.get('type') == 'message'
                           for c in item.get('content', []) if c.get('type') == 'output_text').strip()
            if text:
                texts.append(text); self.transcript.append({'role': 'assistant', 'content': text})
            fn_calls = [x for x in output if x.get('type') == 'function_call']
            if fn_calls:
                pending = []
                for call in fn_calls:
                    try:
                        args = json.loads(call.get('arguments', '{}'))
                        result = self.tool(**args) if call.get('name') == 'polynomial_map_report' else {'error': 'tool not allowed'}
                        is_error = call.get('name') != 'polynomial_map_report'
                    except Exception as exc:
                        args, result, is_error = {}, {'error': type(exc).__name__, 'message': str(exc)}, True
                    calls.append({'name': call.get('name'), 'input': args, 'result': result, 'is_error': is_error})
                    pending.append({'type': 'function_call_output', 'call_id': call['call_id'],
                                    'output': json.dumps(result, sort_keys=True)})
                    self.transcript.append({'role': 'tool_mirror', 'name': call.get('name'), 'input': args, 'output': result})
                continue
            ceiling_only = response.get('status') == 'incomplete' and response.get('incomplete_details', {}).get('reason') == 'max_output_tokens' and not text
            if ceiling_only:
                ceilings += 1
                if len(continuations) < 2:
                    continuations.append('Continue.'); pending = [{'role': 'user', 'content': 'Continue.'}]
                    self.transcript.append({'role': 'user', 'content': 'Continue.'}); continue
            break
        return self._finish(raws, calls, texts, continuations, ceilings, not ceiling_only)

    def _chat_phase(self, phase, prompt, tool_enabled):
        self.messages.append({'role': 'user', 'content': prompt}); self.transcript.append({'role': 'user', 'content': prompt})
        raws, calls, texts, ceilings = [], [], [], 0
        while True:
            payload = {'model': self.model, 'max_completion_tokens': self.config['max_tokens'],
                       'messages': [{'role': 'system', 'content': self.system}] + self.messages,
                       'prompt_cache_key': self.prompt_cache_key}
            if tool_enabled: payload['tools'] = self.api_module.TOOLS
            self._preflight_guard()
            response = self.api_module.api(self.key, payload); raws.append(response)
            self.total_cost_usd += self.api_module.usage_cost(response.get('usage', {}))
            choice = response['choices'][0]; message = choice['message']; text = (message.get('content') or '').strip()
            self.messages.append({k: v for k, v in message.items() if k in ('role','content','tool_calls')})
            if text: texts.append(text); self.transcript.append({'role': 'assistant', 'content': text})
            tool_calls = message.get('tool_calls') or []
            if tool_calls:
                for call in tool_calls:
                    try:
                        args = json.loads(call['function'].get('arguments', '{}'))
                        result = self.tool(**args) if call['function'].get('name') == 'polynomial_map_report' else {'error':'tool not allowed'}
                        is_error = call['function'].get('name') != 'polynomial_map_report'
                    except Exception as exc:
                        args, result, is_error = {}, {'error': type(exc).__name__, 'message': str(exc)}, True
                    calls.append({'name': call['function'].get('name'), 'input': args, 'result': result, 'is_error': is_error})
                    self.messages.append({'role':'tool','tool_call_id':call['id'],'content':json.dumps(result,sort_keys=True)})
                    self.transcript.append({'role':'tool_mirror','name':call['function'].get('name'),'input':args,'output':result})
                continue
            ceiling_only = choice.get('finish_reason') == 'length' and not text
            if ceiling_only: ceilings += 1
            break
        return self._finish(raws, calls, texts, [], ceilings, not ceiling_only)

    def _finish(self, raws, calls, texts, continuations, ceilings, complete):
        if self.total_cost_usd > self.config['session_cost_guard_usd']:
            raise RuntimeError(f"session spend guard exceeded ${self.config['session_cost_guard_usd']:.2f}")
        cost = sum((self.api_module.usage_cost_responses(x.get('usage', {})) if self.surface == 'responses'
                    else self.api_module.usage_cost(x.get('usage', {}))) for x in raws)
        return {'text':'\n\n'.join(texts),'raw_events':raws,'tool_calls':calls,'ceiling_events':ceilings,
                'continuation_prompts':continuations,'provider_model_ids':[x.get('model') for x in raws],
                'usage':{'responses':[x.get('usage',{}) for x in raws]},'cost_usd':cost,'complete':complete or bool(texts)}


class OpenAISubscriptionTransport:
    """Thin ChatGPT-subscription transport using Hermes OAuth, not Codex CLI.

    It sends only the registered instructions/history/tool schema. The ChatGPT
    backend does not accept a hard max_output_tokens control, so this is a
    separately registered harness class and cannot silently replace direct-API
    observations with a frozen output ceiling.
    """
    def __init__(self):
        self.transcript, self.history = [], []
        self.total_cost_usd = 0.0
        self.subscription_module = None

    def start(self, *, system: str, model: str, config: dict, session: dict):
        if self.subscription_module is None:
            self.subscription_module = _load_module(
                str(HERMES_SUBSCRIPTION_PATH),
                'principal_hermes_subscription_' + model.replace('-', '_').replace('.', '_'))
        catalog = self.subscription_module.live_catalog()
        if not self.subscription_module.model_available(model, catalog):
            raise RuntimeError(
                f'exact model {model!r} is not exposed by the live ChatGPT subscription catalog: {catalog}')
        self.system, self.model, self.config, self.session = system, model, config, session
        self.tool = _load_exact_tool()
        self.tool_schema = {
            'type': 'function',
            'function': {
                'name': 'polynomial_map_report',
                'description': ('Return an exact symbolic Jacobian determinant and exact images '
                                'of supplied rational points; performs no retrieval or I/O.'),
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'variables': {'type': 'array', 'items': {'type': 'string'}},
                        'expressions': {'type': 'array', 'items': {'type': 'string'}},
                        'points': {'type': 'array', 'items': {
                            'type': 'array', 'items': {'type': 'string'}}},
                    },
                    'required': ['variables', 'expressions', 'points'],
                    'additionalProperties': False,
                },
            },
        }
        self.effort = config.get('effort', 'medium')

    def run_phase(self, *, phase: str, prompt: str, tool_enabled: bool) -> dict:
        self.history.append({'role': 'user', 'content': prompt})
        self.transcript.append({'role': 'user', 'content': prompt})
        raws, calls, texts = [], [], []
        continuation_prompts, ceiling_events = [], 0
        tools = [self.tool_schema] if tool_enabled else []
        for _ in range(16):
            turn = self.subscription_module.call_once(
                model=self.model, system=self.system, history=self.history,
                session_id=self.session['session_id'], tools=tools, effort=self.effort)
            raw = turn['raw']
            raws.append(raw)
            returned_model = raw.get('model')
            if returned_model != self.model:
                raise RuntimeError(f'subscription model drift: requested {self.model!r}, returned {returned_model!r}')
            assistant = turn['assistant']
            self.history.append(assistant)
            self.transcript.append(assistant)
            if turn['text']:
                texts.append(turn['text'])
            if turn['tool_calls']:
                for call in turn['tool_calls']:
                    function = call.get('function', {})
                    name = function.get('name')
                    args_raw = function.get('arguments', '{}')
                    try:
                        args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
                        if name != 'polynomial_map_report':
                            raise ValueError('tool not allowed')
                        result, is_error = self.tool(**args), False
                    except Exception as exc:
                        args = args_raw if isinstance(args_raw, dict) else {}
                        result, is_error = {'error': type(exc).__name__, 'message': str(exc)}, True
                    calls.append({'name': name, 'input': args, 'result': result, 'is_error': is_error})
                    tool_message = {'role': 'tool', 'tool_call_id': call['id'],
                                    'content': json.dumps(result, sort_keys=True)}
                    self.history.append(tool_message)
                    self.transcript.append({'role': 'tool_mirror', 'name': name,
                                            'input': args, 'output': result, 'is_error': is_error})
                continue
            finish_reason = str(turn.get('finish_reason') or raw.get('status') or '').lower()
            ceiling_only = not turn['text'] and finish_reason in {
                'length', 'max_tokens', 'max_output_tokens', 'incomplete'}
            if ceiling_only:
                ceiling_events += 1
                if len(continuation_prompts) < 2:
                    continuation_prompts.append(CONTINUATION_PROMPT)
                    self.history.append({'role': 'user', 'content': CONTINUATION_PROMPT})
                    self.transcript.append({'role': 'user', 'content': CONTINUATION_PROMPT})
                    continue
            break
        else:
            raise RuntimeError('subscription tool/continuation loop exceeded sixteen provider responses')
        usage = {'responses': [raw.get('usage', {}) for raw in raws]}
        output_tokens = sum(raw.get('usage', {}).get('output_tokens', 0) for raw in raws)
        advisory_exceeded = output_tokens > self.config['max_tokens']
        complete = bool(texts) and not advisory_exceeded
        return {
            'text': '\n\n'.join(texts), 'raw_events': raws, 'tool_calls': calls,
            'ceiling_events': ceiling_events + int(advisory_exceeded),
            'continuation_prompts': continuation_prompts,
            'provider_model_ids': [raw.get('model') for raw in raws], 'usage': usage,
            'cost_usd': 0.0, 'complete': complete,
            'hard_output_ceiling_enforced': False,
            'output_ceiling_advisory_exceeded': advisory_exceeded,
        }


class ClaudeCodeMaxTransport:
    """Isolated Claude Code Max/OAuth stream-json transport with a frozen tool surface."""
    def __init__(self):
        self.transcript = []
        self.total_cost_usd = 0.0
        self.api_equivalent_cost_usd = 0.0
        self.process = None
        self.init_event = None
        self.stderr_text = ''

    @staticmethod
    def _credential_source() -> Path:
        value = os.environ.get(CLAUDE_MAX_CREDENTIALS_ENV, '')
        if not value:
            raise RuntimeError(f'{CLAUDE_MAX_CREDENTIALS_ENV} must name the proven Max OAuth credentials file')
        path = Path(value).expanduser().resolve()
        if not path.is_file():
            raise RuntimeError(f'Claude Max credentials file is absent: {path}')
        return path

    def start(self, *, system: str, model: str, config: dict, session: dict):
        if model not in CLAUDE_MAX_MODELS + A10_CLAUDE_MODELS and not config.get('harness_check'):
            raise RuntimeError(f'unregistered Claude Max model: {model!r}')
        self.system, self.model, self.config, self.session = system, model, config, session
        base = Path(os.environ.get('CLAUDE_SUBJECT_ROOT', '/usr/local/stuff/.claude-subscription-runs'))
        self.subject_root = base / session['session_id']
        self.subject_root.mkdir(parents=True, exist_ok=False)
        self.config_dir = self.subject_root / 'config'
        self.home_dir = self.subject_root / 'home'
        self.work_dir = self.subject_root / 'work'
        for directory in (self.config_dir, self.home_dir, self.work_dir):
            directory.mkdir()
        self.credential_link = self.config_dir / '.credentials.json'
        self.credential_link.symlink_to(self._credential_source())
        self.tool_enabled = session.get('cell') in {'C1', 'C3'}
        mcp = ({'mcpServers': {'exactmap': {'type': 'http', 'url': CLAUDE_MCP_URL}}}
               if self.tool_enabled else {'mcpServers': {}})
        self.mcp_path = self.subject_root / 'mcp.json'
        self.mcp_path.write_text(json.dumps(mcp, sort_keys=True) + '\n')
        self.env = os.environ.copy()
        for key in list(self.env):
            if key.startswith('ANTHROPIC_') or key.startswith('CLAUDE_CODE_USE_'):
                self.env.pop(key, None)
        self.env.update({
            'HOME': str(self.home_dir),
            'CLAUDE_CONFIG_DIR': str(self.config_dir),
            'CLAUDE_CODE_SUBPROCESS_ENV_SCRUB': '1',
            'MCP_TIMEOUT': '10000',
            'MCP_TOOL_TIMEOUT': '60000',
            'MAX_MCP_OUTPUT_TOKENS': '50000',
        })
        auth = subprocess.run(
            ['claude', 'auth', 'status', '--json'], cwd=self.work_dir, env=self.env,
            text=True, capture_output=True, timeout=60)
        if auth.returncode:
            raise RuntimeError(f'Claude Max auth preflight failed: {auth.stderr[:500]}')
        self.auth_status = json.loads(auth.stdout)
        expected_auth = {
            'loggedIn': True, 'authMethod': 'claude.ai',
            'apiProvider': 'firstParty', 'subscriptionType': 'max'}
        if any(self.auth_status.get(k) != v for k, v in expected_auth.items()):
            raise RuntimeError(f'Claude harness is not a Max OAuth account: {self.auth_status}')
        allowed = ('ToolSearch,mcp__exactmap__polynomial_map_report' if self.tool_enabled else '')
        self.command = [
            'claude', '-p', '--input-format', 'stream-json', '--output-format', 'stream-json',
            '--verbose', '--model', model, '--effort', config.get('effort', 'max'),
            '--session-id', session['session_id'], '--name', 'subject-' + session['session_id'][:8],
            '--system-prompt', system, '--setting-sources', '', '--disable-slash-commands',
            '--tools', allowed, '--allowedTools', allowed, '--strict-mcp-config',
            '--mcp-config', str(self.mcp_path), '--no-chrome', '--permission-mode', 'dontAsk',
        ]
        self.process = subprocess.Popen(
            self.command, cwd=self.work_dir, env=self.env, text=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        time.sleep(3 if self.tool_enabled else 1)
        if self.process.poll() is not None:
            raise RuntimeError(f'Claude Code exited during startup with {self.process.returncode}')

    @staticmethod
    def _tool_calls(events: list[dict]) -> list[dict]:
        calls, results = {}, {}
        for event in events:
            message = event.get('message', {}) if isinstance(event, dict) else {}
            content = message.get('content', []) if isinstance(message, dict) else []
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get('type') == 'tool_use':
                    calls[block.get('id')] = {
                        'name': block.get('name'), 'input': block.get('input', {}),
                        'result': None, 'is_error': False}
                elif block.get('type') == 'tool_result':
                    results[block.get('tool_use_id')] = block.get('content')
        for call_id, result in results.items():
            if call_id in calls:
                calls[call_id]['result'] = result
        return list(calls.values())

    def _validate_init(self, event: dict):
        expected_tools = (['ToolSearch', 'mcp__exactmap__polynomial_map_report']
                          if self.tool_enabled else [])
        reported = event.get('model')
        if reported != self.model and not (
                self.config.get('harness_check') and str(reported).startswith(self.model)):
            raise RuntimeError(f'Claude model drift at init: {reported!r}')
        if event.get('apiKeySource') not in (None, 'none'):
            raise RuntimeError(f'Claude Code unexpectedly reports API key source: {event.get("apiKeySource")!r}')
        if event.get('tools') != expected_tools:
            raise RuntimeError(f'Claude tool-surface mismatch: {event.get("tools")!r} != {expected_tools!r}')
        if event.get('skills') or event.get('plugins') or event.get('slash_commands'):
            raise RuntimeError('Claude subject inherited a skill, plugin, or slash command')
        servers = event.get('mcp_servers', [])
        if self.tool_enabled and servers != [{'name': 'exactmap', 'status': 'connected'}]:
            raise RuntimeError(f'exact MCP server not connected before subject turn: {servers!r}')
        if not self.tool_enabled and servers:
            raise RuntimeError(f'no-tool subject inherited MCP servers: {servers!r}')
        self.init_event = event

    def _one_turn(self, prompt: str) -> tuple[list[dict], dict]:
        if self.process is None or self.process.poll() is not None:
            raise RuntimeError('Claude Code subject process is not running')
        message = {'type': 'user', 'message': {'role': 'user', 'content': prompt}}
        self.process.stdin.write(json.dumps(message, separators=(',', ':')) + '\n')
        self.process.stdin.flush()
        events, result = [], None
        deadline = time.monotonic() + 1800
        while time.monotonic() < deadline:
            ready, _, _ = select.select([self.process.stdout], [], [], 1)
            if not ready:
                if self.process.poll() is not None:
                    break
                continue
            line = self.process.stdout.readline()
            if not line:
                break
            event = json.loads(line)
            events.append(event)
            if event.get('type') == 'system' and event.get('subtype') == 'init':
                self._validate_init(event)
            if event.get('type') == 'result':
                result = event
                break
        if result is None:
            raise RuntimeError(f'Claude Code produced no result event; process={self.process.poll()}')
        if self.init_event is None:
            raise RuntimeError('Claude Code produced a subject response without an init provenance event')
        if result.get('is_error') or result.get('subtype') != 'success':
            raise RuntimeError(f'Claude Code result failed: {result}')
        model_ids = list((result.get('modelUsage') or {}).keys())
        if model_ids != [self.model]:
            raise RuntimeError(f'Claude model-usage provenance mismatch: {model_ids!r}')
        if (result.get('usage', {}).get('server_tool_use', {}).get('web_search_requests', 0) or
                result.get('usage', {}).get('server_tool_use', {}).get('web_fetch_requests', 0)):
            raise RuntimeError('Claude subject used an unregistered server web tool')
        return events, result

    def run_phase(self, *, phase: str, prompt: str, tool_enabled: bool) -> dict:
        if bool(tool_enabled) != self.tool_enabled:
            raise RuntimeError('rendered tool condition differs from frozen Claude process tool surface')
        self.transcript.append({'role': 'user', 'content': prompt})
        all_events, texts, continuation_prompts = [], [], []
        ceiling_events = 0
        per_turn_results = []
        while True:
            events, result = self._one_turn(prompt)
            all_events.extend(events)
            per_turn_results.append(result)
            text = str(result.get('result') or '').strip()
            if text:
                texts.append(text)
            self.transcript.append({'role': 'assistant', 'content': text,
                                    'session_id': result.get('session_id')})
            ceiling_only = result.get('stop_reason') == 'max_tokens' and not text
            if ceiling_only:
                ceiling_events += 1
                if len(continuation_prompts) < 2:
                    prompt = CONTINUATION_PROMPT
                    continuation_prompts.append(prompt)
                    self.transcript.append({'role': 'user', 'content': prompt})
                    continue
            break
        calls = self._tool_calls(all_events)
        allowed_names = {'ToolSearch', 'mcp__exactmap__polynomial_map_report'} if tool_enabled else set()
        unexpected = sorted({call['name'] for call in calls if call.get('name') not in allowed_names})
        if unexpected:
            raise RuntimeError(f'Claude subject used unexpected tools: {unexpected}')
        api_equivalent = sum(float(x.get('total_cost_usd') or 0) for x in per_turn_results)
        self.api_equivalent_cost_usd += api_equivalent
        return {
            'text': '\n\n'.join(texts), 'raw_events': all_events, 'tool_calls': calls,
            'ceiling_events': ceiling_events, 'continuation_prompts': continuation_prompts,
            'provider_model_ids': [self.model],
            'usage': {'turns': [x.get('usage', {}) for x in per_turn_results],
                      'modelUsage': [x.get('modelUsage', {}) for x in per_turn_results]},
            'cost_usd': 0.0, 'api_equivalent_cost_usd': api_equivalent,
            'complete': bool(texts) or not ceiling_only,
            'subscription_type': 'max', 'auth_method': 'claude.ai',
        }

    def close(self):
        if self.process is not None:
            try:
                if self.process.stdin and not self.process.stdin.closed:
                    self.process.stdin.close()
                self.process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
            if self.process.stderr:
                self.stderr_text = self.process.stderr.read()
        if getattr(self, 'credential_link', None) and self.credential_link.is_symlink():
            self.credential_link.unlink()

    def export_artifacts(self, run_dir: Path):
        provenance = {
            'auth': {k: self.auth_status.get(k) for k in
                     ('loggedIn', 'authMethod', 'apiProvider', 'subscriptionType')},
            'model': self.model,
            'effort': self.config.get('effort'),
            'tool_enabled': self.tool_enabled,
            'mcp_url': CLAUDE_MCP_URL if self.tool_enabled else None,
            'init_event': self.init_event,
            'api_equivalent_cost_usd': self.api_equivalent_cost_usd,
            'stderr': self.stderr_text,
            'command_flags': [x if x != self.system else '<SYSTEM_PROMPT_REDACTED_BY_HASH>'
                              for x in self.command],
        }
        (run_dir / 'claude-code-max-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
        project_root = self.config_dir / 'projects'
        matches = list(project_root.rglob(self.session['session_id'] + '.jsonl')) if project_root.exists() else []
        if len(matches) != 1:
            raise RuntimeError(f'expected one Claude project JSONL, found {matches}')
        shutil.copy2(matches[0], run_dir / 'claude-code-session.jsonl')


class AnthropicTransport:
    def __init__(self):
        self.transcript, self.messages = [], []
        self.total_cost_usd = 0.0

    def start(self, *, system: str, model: str, config: dict, session: dict):
        path = ('/usr/local/stuff/.anthropic-tools/run_direct_pilot_fable.py'
                if model == 'claude-fable-5' else '/usr/local/stuff/.anthropic-tools/run_direct_pilot.py')
        self.api_module = _load_module(path, 'principal_anthropic_' + model.replace('-', '_'))
        self.key = self.api_module.KEY_PATH.read_text().strip().splitlines()[-1].strip()
        self.system, self.model, self.config, self.session = system, model, config, session
        self.tool = self.api_module.load_tool()
        self.rates = (10, 50) if model == 'claude-fable-5' else (2, 10)

    def _cost(self, usage):
        inp, out = self.rates
        return (inp * usage.get('input_tokens', 0) + 1.25 * inp * usage.get('cache_creation_input_tokens', 0)
                + .1 * inp * usage.get('cache_read_input_tokens', 0)
                + out * usage.get('output_tokens', 0)) / 1_000_000

    def run_phase(self, *, phase: str, prompt: str, tool_enabled: bool) -> dict:
        self.messages.append({'role': 'user', 'content': prompt})
        self.transcript.append({'role': 'user', 'content': prompt})
        raws, calls, continuation_prompts, texts, ceiling_events = [], [], [], [], 0
        while True:
            payload = {'model': self.model, 'max_tokens': self.config['max_tokens'],
                       'system': self.system, 'messages': self.messages,
                       'output_config': {'effort': self.config['effort']},
                       'cache_control': {'type': 'ephemeral'}}
            if tool_enabled:
                payload['tools'] = self.api_module.TOOLS
            response = self.api_module.api(self.key, payload)
            raws.append(response)
            self.total_cost_usd += self._cost(response.get('usage', {}))
            content = response.get('content', [])
            text = ''.join(x.get('text', '') for x in content if x.get('type') == 'text').strip()
            if text:
                texts.append(text)
            self.messages.append({'role': 'assistant', 'content': content})
            self.transcript.append({'role': 'assistant', 'content': content})
            tool_uses = [x for x in content if x.get('type') == 'tool_use']
            if tool_uses:
                results = []
                for call in tool_uses:
                    try:
                        result = self.tool(**call['input']) if call.get('name') == 'polynomial_map_report' else {'error': 'tool not allowed'}
                        is_error = call.get('name') != 'polynomial_map_report'
                    except Exception as exc:
                        result, is_error = {'error': type(exc).__name__, 'message': str(exc)}, True
                    calls.append({'name': call.get('name'), 'input': call.get('input'), 'result': result, 'is_error': is_error})
                    results.append({'type': 'tool_result', 'tool_use_id': call['id'],
                                    'content': json.dumps(result, sort_keys=True), 'is_error': is_error})
                self.messages.append({'role': 'user', 'content': results})
                self.transcript.append({'role': 'user', 'content': results})
                continue
            ceiling_only = response.get('stop_reason') == 'max_tokens' and not text
            if ceiling_only:
                ceiling_events += 1
                if len(continuation_prompts) < 2:
                    continuation_prompts.append('Continue.')
                    self.messages.append({'role': 'user', 'content': 'Continue.'})
                    self.transcript.append({'role': 'user', 'content': 'Continue.'})
                    continue
            break
        if self.total_cost_usd > self.config['session_cost_guard_usd']:
            raise RuntimeError(f"session spend guard exceeded ${self.config['session_cost_guard_usd']:.2f}")
        usage = {'responses': [x.get('usage', {}) for x in raws]}
        return {'text': '\n\n'.join(texts), 'raw_events': raws, 'tool_calls': calls,
                'ceiling_events': ceiling_events, 'continuation_prompts': continuation_prompts,
                'provider_model_ids': [x.get('model') for x in raws], 'usage': usage,
                'cost_usd': sum(self._cost(x.get('usage', {})) for x in raws),
                'complete': bool(texts) or not ceiling_only}


class LocalLlamaTransport:
    """OpenAI-compatible chat transport against a local llama.cpp server.

    No credentials, no network egress beyond localhost, zero spend. The server
    must expose the exact registered model slug; native tool calling was
    harness-verified against llama-server before A9 froze this class.
    """
    def __init__(self):
        self.transcript, self.messages = [], []
        self.total_cost_usd = 0.0

    def start(self, *, system: str, model: str, config: dict, session: dict):
        import requests
        self.requests = requests
        self.base_url = config['base_url'].rstrip('/')
        listed = self.requests.get(self.base_url + '/models', timeout=10).json()
        ids = [entry.get('id') for entry in listed.get('data', [])]
        if model not in ids:
            raise RuntimeError(f'local server does not expose exact model {model!r}: {ids}')
        self.system, self.model, self.config, self.session = system, model, config, session
        self.tool = _load_exact_tool()
        self.tool_schema = {'type': 'function', 'function': {
            'name': 'polynomial_map_report',
            'description': ('Return an exact symbolic Jacobian determinant and exact images '
                            'of supplied rational points; performs no retrieval or I/O.'),
            'parameters': {
                'type': 'object',
                'properties': {
                    'variables': {'type': 'array', 'items': {'type': 'string'}},
                    'expressions': {'type': 'array', 'items': {'type': 'string'}},
                    'points': {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'string'}}},
                },
                'required': ['variables', 'expressions', 'points'],
                'additionalProperties': False,
            }}}

    def run_phase(self, *, phase: str, prompt: str, tool_enabled: bool) -> dict:
        self.messages.append({'role': 'user', 'content': prompt})
        self.transcript.append({'role': 'user', 'content': prompt})
        raws, calls, texts, continuation_prompts, ceiling_events = [], [], [], [], 0
        for _ in range(16):
            payload = {'model': self.model, 'max_tokens': self.config['max_tokens'],
                       'messages': [{'role': 'system', 'content': self.system}] + self.messages}
            if tool_enabled:
                payload['tools'] = [self.tool_schema]
            response = self.requests.post(self.base_url + '/chat/completions',
                                          json=payload, timeout=1800).json()
            if response.get('error'):
                raise RuntimeError(f'local server error: {response["error"]}')
            raws.append(response)
            choice = response['choices'][0]
            message = choice['message']
            text = (message.get('content') or '').strip()
            self.messages.append({k: v for k, v in message.items()
                                  if k in ('role', 'content', 'tool_calls') and v is not None})
            self.transcript.append({'role': 'assistant', 'content': text})
            if text:
                texts.append(text)
            tool_calls = message.get('tool_calls') or []
            if tool_calls:
                for call in tool_calls:
                    name = call.get('function', {}).get('name')
                    try:
                        args = json.loads(call.get('function', {}).get('arguments', '{}'))
                        if name != 'polynomial_map_report':
                            raise ValueError('tool not allowed')
                        result, is_error = self.tool(**args), False
                    except Exception as exc:
                        args, result, is_error = {}, {'error': type(exc).__name__, 'message': str(exc)}, True
                    calls.append({'name': name, 'input': args, 'result': result, 'is_error': is_error})
                    self.messages.append({'role': 'tool', 'tool_call_id': call.get('id'),
                                          'content': json.dumps(result, sort_keys=True)})
                    self.transcript.append({'role': 'tool_mirror', 'name': name,
                                            'input': args, 'output': result, 'is_error': is_error})
                continue
            ceiling_only = choice.get('finish_reason') == 'length' and not text
            if ceiling_only:
                ceiling_events += 1
                if len(continuation_prompts) < 2:
                    continuation_prompts.append(CONTINUATION_PROMPT)
                    self.messages.append({'role': 'user', 'content': CONTINUATION_PROMPT})
                    self.transcript.append({'role': 'user', 'content': CONTINUATION_PROMPT})
                    continue
            break
        else:
            raise RuntimeError('local tool/continuation loop exceeded sixteen server responses')
        return {'text': '\n\n'.join(texts), 'raw_events': raws, 'tool_calls': calls,
                'ceiling_events': ceiling_events, 'continuation_prompts': continuation_prompts,
                'provider_model_ids': [x.get('model') for x in raws],
                'usage': {'responses': [x.get('usage', {}) for x in raws]},
                'cost_usd': 0.0, 'complete': bool(texts) or not ceiling_only}


class MockTransport:
    """Zero-cost deterministic transport exercising the real exact tool path."""
    def __init__(self, ceiling_phase: str | None = None):
        self.ceiling_phase = ceiling_phase
        self.transcript = []
        self.total_cost_usd = 0.0

    def start(self, *, system: str, model: str, config: dict, session: dict):
        self.system, self.model, self.config, self.session = system, model, config, session

    def run_phase(self, *, phase: str, prompt: str, tool_enabled: bool) -> dict:
        self.transcript.append({'role': 'user', 'content': prompt})
        tool_calls = []
        if phase == 'treatment' and tool_enabled and self.session.get('arm'):
            stimuli = json.loads(STIMULI_PATH.read_text())
            cert = stimuli['certificates'][{'genuine': 'cert_A', 'sham': 'cert_B'}[self.session['arm']]]
            result = _load_exact_tool()(['x', 'y', 'z'], cert['map'], cert['points'])
            self.treatment_report = result
            tool_calls.append({'name': 'polynomial_map_report', 'input': {
                'variables': ['x', 'y', 'z'], 'expressions': cert['map'], 'points': cert['points']},
                'result': result, 'is_error': False})
        if phase == 'claim_assessment':
            if getattr(self, 'treatment_report', {}).get('all_images_equal') is False:
                text = 'REJECT. The exact report shows pairwise-distinct images, so the claimed collision fails.'
            else:
                text = 'ACCEPT. The exact report establishes a collision with nonzero constant determinant.'
        elif phase == 'calibration_pre':
            text = '0.01 — The statement is historically open.'
        elif phase == 'calibration_post':
            text = '0.99 — The exact collision certificate changed my assessment.'
        else:
            text = 'No. This mock response is intentionally brief and mechanically valid.'
        ceiling_events = 1 if phase == self.ceiling_phase else 0
        continuations = ['Continue.'] if ceiling_events else []
        raw = [{'mock': True, 'phase': phase, 'stop_reason': 'max_tokens', 'text': ''},
               {'mock': True, 'phase': phase, 'stop_reason': 'end_turn', 'text': text}] \
              if ceiling_events else [{'mock': True, 'phase': phase, 'stop_reason': 'end_turn', 'text': text}]
        self.transcript.append({'role': 'assistant', 'content': text})
        return {'text': text, 'raw_events': raw, 'tool_calls': tool_calls,
                'ceiling_events': ceiling_events, 'continuation_prompts': continuations,
                'provider_model_ids': [self.model] * len(raw), 'usage': {}, 'cost_usd': 0.0,
                'complete': True}


def parse_stance(text: str) -> str:
    match = re.search(r'\b(ACCEPT|REJECT|UNCERTAIN)\b', text.upper())
    return match.group(1) if match else 'UNCERTAIN'


def execute_session(session: dict, class_config: dict, *, transport, results_root: Path) -> Path:
    bounded = class_config.get('system_class') == 'bounded-scope-low-effort'
    payload = render_condition(session, bounded=bounded)
    run_dir = Path(results_root) / session['session_id']
    run_dir.mkdir(parents=True, exist_ok=False)
    manifest_path = run_dir / 'manifest.json'
    manifest = {
        **session,
        'provider': class_config['provider'],
        'harness_class': class_config.get('harness_class'),
        'registered_commit': REGISTERED_COMMIT,
        'schedule_sha256': class_config.get('schedule_sha256_override') or build_schedule()['schedule_sha256'],
        'system_prompt_sha256': hashlib.sha256(payload['system'].encode()).hexdigest(),
        'subject_bundle_sha256': payload['subject_bundle_sha256'],
        'max_tokens': class_config['max_tokens'],
        'output_ceiling_policy': class_config.get('output_ceiling_policy'),
        'effort': class_config.get('effort'),
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'phases': [], 'complete': False,
    }

    def persist():
        temporary = manifest_path.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(manifest, indent=2) + '\n')
        temporary.replace(manifest_path)

    def run(phase: str, prompt: str):
        result = transport.run_phase(phase=phase, prompt=prompt, tool_enabled=payload['tool_enabled'])
        response_path = run_dir / f'{len(manifest["phases"]):02d}-{phase}.responses.json'
        response_path.write_text(json.dumps(result['raw_events'], indent=2) + '\n')
        manifest['phases'].append({
            'phase': phase, 'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
            'response_path': str(response_path), 'text': result['text'],
            'text_sha256': hashlib.sha256(result['text'].encode()).hexdigest(),
            'tool_calls': result.get('tool_calls', []),
            'ceiling_events': result.get('ceiling_events', 0),
            'continuation_prompts': result.get('continuation_prompts', []),
            'provider_model_ids': result.get('provider_model_ids', []),
            'usage': result.get('usage', {}), 'cost_usd': result.get('cost_usd', 0.0),
            'api_equivalent_cost_usd': result.get('api_equivalent_cost_usd'),
            'complete': result.get('complete', True),
        })
        persist()
        return result['text']

    persist()
    caught = None
    try:
        transport.start(system=payload['system'], model=session['model'], config=class_config, session=session)
        run('calibration_pre', payload['calibration_pre'])
        run('treatment', payload['treatment'])
        claim = run('claim_assessment', payload['claim_assessment'])
        stance = parse_stance(claim)
        manifest['committed_stance_parser'] = stance
        for probe in payload['probes']:
            run('probe-' + probe['id'], probe['prompt'])
        if stance == 'ACCEPT':
            run('pushback_if_accept', payload['pushback_if_accept'])
        elif stance == 'REJECT':
            run('pushback_if_reject', payload['pushback_if_reject'])
        else:
            manifest['phases'].append({'phase': 'pushback_skipped_uncertain', 'response_path': None})
            persist()
        run('calibration_post', payload['calibration_post'])
    except Exception as exc:
        caught = exc
        manifest['error'] = {'type': type(exc).__name__, 'message': str(exc)}
        (run_dir / 'failure.json').write_text(json.dumps(manifest['error'], indent=2) + '\n')
    finally:
        close = getattr(transport, 'close', None)
        if close:
            try:
                close()
            except Exception as exc:
                if caught is None:
                    caught = exc
                    manifest['error'] = {'type': type(exc).__name__, 'message': str(exc)}
        export = getattr(transport, 'export_artifacts', None)
        if export:
            try:
                export(run_dir)
            except Exception as exc:
                if caught is None:
                    caught = exc
                    manifest['error'] = {'type': type(exc).__name__, 'message': str(exc)}
        (run_dir / 'transcript.json').write_text(json.dumps(transport.transcript, indent=2) + '\n')
        manifest['total_cost_usd'] = transport.total_cost_usd
        manifest['api_equivalent_cost_usd'] = getattr(transport, 'api_equivalent_cost_usd', None)
        manifest['completed_utc'] = datetime.now(timezone.utc).isoformat()
        manifest['complete'] = caught is None and all(p.get('complete', True) for p in manifest['phases'])
        persist()
    if caught is not None:
        raise caught
    return run_dir


def _transport(provider: str):
    if provider == 'openai-subscription':
        return OpenAISubscriptionTransport()
    if provider == 'claude-code-max':
        return ClaudeCodeMaxTransport()
    if provider == 'local-llamacpp':
        return LocalLlamaTransport()
    if provider in {'openai', 'anthropic'}:
        raise RuntimeError(f'direct API provider {provider!r} is forbidden by the subscription-only freeze')
    raise ValueError(f'unknown provider: {provider}')


def run_gate(model: str, config: dict, root: Path) -> dict:
    bounded = config.get('system_class') == 'bounded-scope-low-effort'
    system = json.loads(STIMULI_PATH.read_text())['system_prompt'] + (BOUNDED_SCOPE_SUFFIX if bounded else '')
    out = root / model / 'competence-gate'
    out.mkdir(parents=True, exist_ok=False)
    transport = _transport(config['provider'])
    session = {'model': model, 'session_id': str(uuid.uuid5(NAMESPACE, model + '|competence-gate'))}
    try:
        transport.start(system=system, model=model, config=config, session=session)
        result = transport.run_phase(
            phase='competence_gate', prompt=competence_gate_prompt(), tool_enabled=False)
        score = score_competence_gate(result['text'])
        artifact = {
            'model': model, 'provider': config['provider'],
            'harness_class': config.get('harness_class'),
            'schedule_sha256': build_schedule()['schedule_sha256'],
            'system_sha256': hashlib.sha256(system.encode()).hexdigest(),
            'prompt_sha256': hashlib.sha256(competence_gate_prompt().encode()).hexdigest(),
            'text': result['text'], 'score': score, 'raw_responses': result['raw_events'],
            'transcript': transport.transcript, 'cost_usd': 0.0,
            'api_equivalent_cost_usd': result.get('api_equivalent_cost_usd'),
        }
    except Exception as exc:
        (out / 'failure.json').write_text(json.dumps(
            {'type': type(exc).__name__, 'message': str(exc)}, indent=2) + '\n')
        raise
    finally:
        close = getattr(transport, 'close', None)
        if close:
            close()
        export = getattr(transport, 'export_artifacts', None)
        if export:
            export(out)
    (out / 'gate.json').write_text(json.dumps(artifact, indent=2) + '\n')
    return artifact


def run_baseline(model: str, config: dict, root: Path) -> dict:
    stimuli = json.loads(STIMULI_PATH.read_text())
    bounded = config.get('system_class') == 'bounded-scope-low-effort'
    system = stimuli['system_prompt'] + (BOUNDED_SCOPE_SUFFIX if bounded else '')
    out = root / model / 'contamination-baseline'
    out.mkdir(parents=True, exist_ok=False)
    transport = _transport(config['provider'])
    session = {'model': model, 'session_id': str(uuid.uuid5(NAMESPACE, model + '|contamination-baseline'))}
    try:
        transport.start(system=system, model=model, config=config, session=session)
        responses = []
        for key, prompt in stimuli['contamination_baseline'].items():
            if key == 'note':
                continue
            responses.append({'item': key, 'prompt': prompt,
                              'result': transport.run_phase(
                                  phase='baseline-' + key, prompt=prompt, tool_enabled=False)})
        artifact = {
            'model': model, 'provider': config['provider'],
            'harness_class': config.get('harness_class'),
            'schedule_sha256': build_schedule()['schedule_sha256'],
            'responses': responses, 'transcript': transport.transcript,
            'cost_usd': 0.0,
            'api_equivalent_cost_usd': getattr(transport, 'api_equivalent_cost_usd', None),
        }
    except Exception as exc:
        (out / 'failure.json').write_text(json.dumps(
            {'type': type(exc).__name__, 'message': str(exc)}, indent=2) + '\n')
        raise
    finally:
        close = getattr(transport, 'close', None)
        if close:
            close()
        export = getattr(transport, 'export_artifacts', None)
        if export:
            export(out)
    (out / 'baseline.json').write_text(json.dumps(artifact, indent=2) + '\n')
    return artifact


def run_stage(model: str, stage: str, root: Path):
    config = _resolve_config(model)
    key = {'neutral': 'neutral_sessions', 'authority_extension': 'authority_extension_sessions',
           'pilot': 'pilot_sessions'}[stage]
    sessions = config[key]
    stage_root = root / model / stage; stage_root.mkdir(parents=True, exist_ok=True)
    completed, deferred = [], []
    deferred_streak = 0
    for session in sessions:
        run_session, resolved, failures = session, False, 0
        for supersede in range(0, 4):
            if supersede:
                identity = (f'{session["model"]}|{session["stage"]}|{session["cell"]}|'
                            f'{session["arm"] or "none"}|{session["authority_variant"]}|'
                            f'{session["replicate"]}|supersede{supersede}')
                run_session = {**session, 'session_id': str(uuid.uuid5(NAMESPACE, identity)),
                               'supersedes': run_session['session_id']}
            session_root = stage_root / run_session['session_id']
            target = session_root / 'manifest.json'
            if target.is_file() and json.loads(target.read_text()).get('complete'):
                completed.append(str(session_root)); resolved = True; break
            if session_root.exists():
                continue  # incomplete: preserved untouched per A8; try the next superseding UUID
            try:
                run_dir = execute_session(run_session, config, transport=_transport(config['provider']),
                                          results_root=stage_root)
            except Exception as exc:
                failures += 1
                print(json.dumps({'failed_session': run_session['session_id'], 'model': model,
                                  'stage': stage, 'error': type(exc).__name__,
                                  'message': str(exc)[:300]}), flush=True)
                if failures >= 2:
                    break  # defer this logical session; remaining supersede slots stay available
                continue  # preserved incomplete; next loop iteration supersedes it
            completed.append(str(run_dir)); resolved = True
            print(json.dumps({'completed': len(completed), 'planned': len(sessions), 'model': model,
                              'stage': stage, 'run_dir': str(run_dir),
                              'supersedes': run_session.get('supersedes')}), flush=True)
            break
        if resolved:
            deferred_streak = 0
        else:
            deferred.append(session['session_id'])
            deferred_streak += 1
            print(json.dumps({'deferred': session['session_id'], 'model': model, 'stage': stage,
                              'reason': 'repeated failures or exhausted supersession budget'}), flush=True)
            if deferred_streak >= 2:
                raise RuntimeError(
                    'two consecutive logical sessions deferred; stopping the round as systemic')
    if deferred:
        print(json.dumps({'round_deferred_sessions': deferred, 'model': model, 'stage': stage,
                          'note': 'rerun run-stage to retry remaining supersede slots'}), flush=True)
    return completed


def claude_harness_check(model: str, root: Path) -> dict:
    """Cheap end-to-end validation of the Claude Code Max transport (auth
    preflight, init provenance, MCP tool round-trip, artifact export) using a
    non-subject model and non-stimulus prompts. Never touches schedule roots."""
    config = dict(build_schedule()['model_classes'][CLAUDE_MAX_MODELS[0]])
    config.update({'harness_check': True, 'effort': 'high', 'max_tokens': 16384})
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    session = {'session_id': str(uuid.uuid5(NAMESPACE, f'harness-check|{model}|{stamp}')),
               'model': model, 'cell': 'C1', 'arm': None, 'stage': 'harness-check'}
    out = root / f'claude-max-harness-check-{model}-{stamp}'
    out.mkdir(parents=True, exist_ok=False)
    transport = ClaudeCodeMaxTransport()
    report = {'model': model, 'session_id': session['session_id'], 'checks': {}}
    try:
        transport.start(system='You are a terse verification assistant.', model=model,
                        config=config, session=session)
        result = transport.run_phase(
            phase='harness-tool-roundtrip',
            prompt=('Call polynomial_map_report with variables ["x"], expressions ["x"], '
                    'points [["1"]] and state the returned determinant, nothing else.'),
            tool_enabled=True)
        report['checks'] = {
            'auth_max_oauth': True,
            'init_validated': transport.init_event is not None,
            'tool_roundtrip': any(not c['is_error'] and c['result'] for c in result['tool_calls']),
            'text_returned': bool(result['text']),
            'api_equivalent_cost_usd': result.get('api_equivalent_cost_usd'),
        }
        report['text'] = result['text']
        report['passed'] = all(v for k, v in report['checks'].items()
                               if k != 'api_equivalent_cost_usd')
    except Exception as exc:
        report['passed'] = False
        report['error'] = {'type': type(exc).__name__, 'message': str(exc)}
    finally:
        transport.close()
        try:
            transport.export_artifacts(out)
        except Exception as exc:
            report.setdefault('export_warning', f'{type(exc).__name__}: {exc}')
    (out / 'harness-check.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('freeze', 'freeze-a9', 'freeze-a10', 'freeze-a12',
                                            'dry-run', 'gate', 'baseline', 'run-stage',
                                            'claude-harness-check'))
    parser.add_argument('--model')
    parser.add_argument('--stage', choices=('neutral', 'authority_extension', 'pilot'))
    parser.add_argument('--root', default='/usr/local/stuff/jtest/results/subscription-round-2026-07-23')
    args = parser.parse_args(); root = Path(args.root)
    schedule = build_schedule()
    if args.command == 'freeze':
        root.mkdir(parents=True, exist_ok=True)
        path = root / 'schedule.json'; path.write_text(json.dumps(schedule, indent=2) + '\n')
        print(json.dumps({'path': str(path), 'sha256': schedule['schedule_sha256']})); return
    if args.command in ('freeze-a9', 'freeze-a10', 'freeze-a12'):
        ext = {'freeze-a9': build_a9_schedule, 'freeze-a10': build_a10_schedule,
               'freeze-a12': build_a12_schedule}[args.command]()
        root.mkdir(parents=True, exist_ok=True)
        path = root / f'schedule-{ext["amendment"].lower()}.json'
        path.write_text(json.dumps(ext, indent=2) + '\n')
        print(json.dumps({'path': str(path), 'sha256': ext['schedule_sha256'],
                          'extends': ext['extends_schedule_sha256']})); return
    if args.command == 'claude-harness-check':
        report = claude_harness_check(args.model or CLAUDE_HARNESS_CHECK_MODEL, root)
        print(json.dumps({'passed': report['passed'], 'checks': report.get('checks'),
                          'error': report.get('error')}))
        if not report['passed']: raise SystemExit(2)
        return
    if args.command == 'dry-run':
        model = 'gpt-5.6-sol'; config = schedule['model_classes'][model]
        session = next(s for s in config['neutral_sessions'] if s['cell'] == 'C1' and s['arm'] == 'genuine')
        out = execute_session(session, config, transport=MockTransport('probe-surjectivity'),
                              results_root=root / 'mock')
        print(out); return
    if not args.model: parser.error('--model is required')
    config = _resolve_config(args.model)
    if args.command == 'gate':
        artifact = run_gate(args.model, config, root)
        print(json.dumps({'passed': artifact['score']['passed'], 'correct': artifact['score']['correct'],
                          'cost_usd': artifact['cost_usd']}));
        if not artifact['score']['passed']: raise SystemExit(2)
    elif args.command == 'baseline':
        artifact = run_baseline(args.model, config, root); print(json.dumps({'cost_usd':artifact['cost_usd']}))
    else:
        if not args.stage: parser.error('--stage is required')
        run_stage(args.model, args.stage, root)


if __name__ == '__main__':
    main()
