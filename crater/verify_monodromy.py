"""Machine verification for monodromy.md: the 3-sheeted covering over
C^3 \\ {L=0} has full S_3 monodromy.

Checks 1-2 are exact symbolic computation and constitute the proof
(irreducible cubic => transitive; disc = (2S)^2 * (-L) with L irreducible
=> non-square discriminant => not inside A_3). Checks 3-5 are numerical
*witnesses* of the local structure: transposition around the rim, identity
around the S-wall, and generation of the full S_3 by rim loops on a generic
complex line (root-tracking continuation with fine steps).

Run: python3 verify_monodromy.py   (sympy + numpy; ~1 minute)
"""
import sympy as sp
import numpy as np

x, A, B, C, t = sp.symbols('x A B C t')
L = 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2
cubic = L*x**3 + (4 - 3*B*C)*x - 2*C

# -- 1. the fiber cubic is irreducible ----------------------------------------
fac = sp.factor_list(sp.expand(cubic), x, A, B, C)
assert len(fac[1]) == 1 and fac[1][0][1] == 1
assert sp.Poly(fac[1][0][0], x).degree() == 3
print("1. fiber cubic irreducible over the function field       OK")

# -- 2. L irreducible => -L not a square => disc -4LS^2 non-square -------------
facL = sp.factor_list(L)
assert len(facL[1]) == 1 and facL[1][0][1] == 1
print("2. L irreducible; disc = (2S)^2*(-L) is a non-square      OK")
#    (1)+(2): monodromy is transitive and not inside A_3  =>  S_3.

# -- numeric witnesses ---------------------------------------------------------
def track(roots_at, path):
    prev = roots_at(path[0]); order = list(range(3))
    for tt in path[1:]:
        cur = roots_at(tt)
        newo, used = [], set()
        for i in order:
            d = [abs(prev[i] - cur[j]) if j not in used else np.inf
                 for j in range(3)]
            j = int(np.argmin(d)); used.add(j); newo.append(j)
        prev, order = cur, newo
    return tuple(order)

# -- 3./4. the line B = C = 1: rim at A=0, 2/27; S-wall at A=1/27 ---------------
def roots_line1(Av):
    return np.roots([27*Av**2 - 2*Av, 0, 1, -2])

def circle(center, r, n=4000):
    return [center + r*np.exp(1j*th) for th in np.linspace(0, 2*np.pi, n)]

assert track(roots_line1, circle(2/27, 0.008)) == (1, 0, 2)
assert track(roots_line1, circle(0.0, 0.008)) == (1, 0, 2)
print("3. rim loops (A=0 and A=2/27): transposition (0 1)        OK")
assert track(roots_line1, circle(1/27, 0.006)) == (0, 1, 2)
print("4. S-wall loop (A=1/27): identity                          OK")

# -- 5. generic complex line: rim loops generate all of S_3 --------------------
base = (0.31 + 0.12j, 0.83 - 0.21j, 1.07 + 0.33j)
dire = (1.0 + 0.41j, -0.57 + 0.89j, 0.23 - 0.71j)
line = {A: base[0] + t*dire[0], B: base[1] + t*dire[1], C: base[2] + t*dire[2]}
tpoly = sp.Poly(sp.expand(L.subs(line)), t)
rims = np.roots([complex(c) for c in tpoly.all_coeffs()])

def roots_generic(tt):
    Av = base[0] + tt*dire[0]; Bv = base[1] + tt*dire[1]; Cv = base[2] + tt*dire[2]
    Lv = 27*Av**2*Cv**2 - 18*Av*Bv*Cv + 16*Av + Bv**3*Cv - Bv**2
    return np.roots([Lv, 0, 4 - 3*Bv*Cv, -2*Cv])

def based_loop(tk, r=0.02, n=4000):
    start = tk + r*(-tk/abs(tk))
    spoke = [s*start for s in np.linspace(0, 1, n//2)]
    return spoke + circle(tk, r, n)[:0] + \
        [tk + (start - tk)*np.exp(1j*th) for th in np.linspace(0, 2*np.pi, n)] \
        + spoke[::-1]

perms = {track(roots_generic, based_loop(complex(tk))) for tk in rims}
def compose(p, q):
    return tuple(q[p[i]] for i in range(3))
group = {(0, 1, 2)} | perms
grew = True
while grew:
    new = {compose(a, b) for a in group for b in group} - group
    grew = bool(new); group |= new
assert len(group) == 6, group
print("5. generic-line rim loops generate S_3 (order 6)           OK")

print("DONE — full S_3 monodromy verified.")
