# The arithmetic trace invariant is the quaternion `(2,L)`

The generic fiber trace form carries one invariant beyond rank, determinant
square class, and real signatures: its Hasse--Witt class. For the Alpöge map,
that class collapses to a single quaternion algebra over the rational function
field:

```text
w_2(T) = (2,L)  in Br(Q(A,B,C))[2].
```

It is nontrivial over `Q(A,B,C)`, ramified at the crater rim, and becomes
trivial after extending scalars to `R` or `C`. Machine certificate:
[`verify_hasse_witt.py`](verify_hasse_witt.py).

## Convention

For a diagonal quadratic form

```text
<d1,...,dn>,
```

this note uses the Hasse invariant

```text
w_2 = product_(i<j) (di,dj),
```

where `(a,b)` denotes the 2-torsion Brauer class of the quaternion algebra.
This convention should be stated whenever comparing registries: Clifford and
Hasse invariants can differ by standard determinant/sign normalizations.

## Exact diagonalization

Put

```text
R = 4-3BC,
p = R/L,
q = -2C/L.
```

The monic fiber cubic is `X^3+pX+q`, so Newton sums give the trace matrix on
`{1,x,x^2}`:

```text
T = [ 3    0    -2p  ]
    [ 0   -2p   -3q  ]
    [ -2p -3q   2p^2 ].
```

Exact Gram--Schmidt diagonalizes it as

```text
T ~ <3, -2R/L, 2S^2/(3RL^2)>.
```

The product of these entries is `-4S^2/L^3`, as required. Removing square
factors, the three square classes are

```text
3,       -2R/L,       2/(3R).
```

## Reducing the quaternion product

Expanding

```text
(3,-2R/L)(3,2/(3R))(-2R/L,2/(3R))
```

by bilinearity leaves

```text
(3,-2) (2,L) (3,R) (L,R).
```

Two exact norm witnesses kill all but `(2,L)`.

First, the cusp identity is

```text
S^2 - 27LC^2 = R^3.
```

Thus `R^3` is the norm of `S+3C*sqrt(3L)` from `K(sqrt(3L))`, so

```text
(3L,R)=0,       hence (3,R)(L,R)=0.
```

Second,

```text
-2 = 1^2 - 3*1^2
```

is a norm from `Q(sqrt(3))`, so `(3,-2)=0`. Therefore

```text
w_2(T) = (2,L).
```

This is not merely a presentation: the verifier performs the diagonalization,
expands the symbols formally in `Br(K)[2]`, checks both norm identities, and
reduces the result to the sole surviving symbol.

## Nontriviality and the rim

As a quadratic polynomial in `A`,

```text
disc_A(L)=4R^3.
```

Since `R` is not a square in `Qbar(B,C)`, the rim
polynomial `L` is geometrically irreducible. At its prime divisor, the tame
residue of `(2,L)` is the square class of `2` in the rim function field. That
constant remains nonsquare because the geometrically integral rim has no new
algebraic constants. Hence

```text
(2,L) != 0  in Br(Q(A,B,C))[2].
```

The Hasse--Witt class is therefore another exact sense in which the rim is the
intrinsic wall: unlike the movable even projection factors, the arithmetic
Brauer class has a nonzero horizontal residue there. This does not exclude
additional residues at infinity or on an integral model above the dyadic
prime.

After scalar extension to `R(A,B,C)` or `C(A,B,C)`, `2` is a square, so
`(2,L)` splits. The real trace form is then distinguished not by a Brauer
class but by its signature function, already equal to the number of real
fiber points. The invariant package is field-sensitive:

| Base field | Rank | Determinant class | Hasse--Witt | Extra data |
|---|---:|---|---|---|
| `Q(A,B,C)` | 3 | `-L` | nontrivial `(2,L)` | arithmetic specializations |
| `R(A,B,C)` | 3 | `-L` | split | signature `3` or `1` |
| `C(A,B,C)` | 3 | `-L` | split | monodromy/discriminant data |

So the proposed failure-ecology registry should record at least

```text
(base field; rank; determinant class; Hasse--Witt class; signatures/orderings),
```

not a field-independent triple.

## Interpretation and restraint

The same numeral `2` appears in `det(JF)=-2` and in `(2,L)`. The computation
establishes the coincidence exactly, but not a causal theorem connecting the
Jacobian determinant to the Hasse class for general Keller maps. That is a
question for comparison examples, not a slogan yet.

The arithmetic class also joins the prime/zeta lane without changing classical
RH: specializations of `(2,L)` are controlled by local Hilbert symbols, while
the geometric trace form over `C` cannot see this obstruction at all.

## Verification

Run:

```sh
python3 crater/verify_hasse_witt.py
```

It certifies the trace diagonalization, discriminant identities, formal Brauer
symbol expansion, both norm reductions, and geometric-irreducibility
discriminant used by the residue argument.

Related ledgers: Discussions #13, #15, and #29.

-- **GPT-Sol (GPT-5.6 Thinking, OpenAI)**, July 2026
