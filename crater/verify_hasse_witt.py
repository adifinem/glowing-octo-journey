"""Exact certificate for the Hasse--Witt invariant of the generic trace form.

Convention: for a diagonal form <d1,...,dn>, the Hasse invariant is the
2-torsion Brauer class product over i<j of quaternion symbols (di,dj).
"""
import sympy as sp

A, B, C = sp.symbols("A B C")
R = 4 - 3*B*C
L = 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2
S = 27*A*C**2 - 9*B*C + 8
p = R/L
q = -2*C/L
Delta = -4*p**3 - 27*q**2

# Newton sums for the monic depressed cubic X^3+pX+q.
T = sp.Matrix([
    [3, 0, -2*p],
    [0, -2*p, -3*q],
    [-2*p, -3*q, 2*p**2],
])

# Gram--Schmidt over Q(A,B,C).
M = sp.Matrix([
    [1, 0, 2*p/3],
    [0, 1, -3*q/(2*p)],
    [0, 0, 1],
])
diagonal = sp.simplify(M.T*T*M)
d1 = sp.Integer(3)
d2 = -2*p
d3 = -Delta/(6*p)
assert all(sp.cancel(diagonal[i, j] - sp.diag(d1, d2, d3)[i, j]) == 0
           for i in range(3) for j in range(3))
assert sp.cancel(Delta + 4*S**2/L**3) == 0
assert sp.cancel(d3 - 2*S**2/(3*R*L**2)) == 0
assert sp.cancel(d1*d2*d3 - Delta) == 0
print("1. trace form diagonalized as <3,-2R/L,2S^2/(3RL^2)>  OK")

# Formal quaternion-symbol arithmetic in Br(K)[2]. A square class is a set of
# independent generators; repeated generators cancel. (a,a)=(a,-1).
def toggle(container, item):
    if item in container:
        container.remove(item)
    else:
        container.add(item)


def hilbert(left, right):
    result = set()
    for a in left:
        for b in right:
            pair = tuple(sorted((a, "-1"))) if a == b else tuple(sorted((a, b)))
            toggle(result, pair)
    return result


def brauer_sum(*classes):
    result = set()
    for cls in classes:
        for symbol in cls:
            toggle(result, symbol)
    return result

# Square classes of d1,d2,d3. Inverses have the same square class.
classes = [
    {"3"},
    {"-1", "2", "R", "L"},
    {"2", "3", "R"},
]
hasse = brauer_sum(
    hilbert(classes[0], classes[1]),
    hilbert(classes[0], classes[2]),
    hilbert(classes[1], classes[2]),
)
assert hasse == {
    ("-1", "3"), ("2", "3"), ("2", "L"), ("3", "R"), ("L", "R")
}
print("2. raw Hasse symbol product expanded in Br(K)[2]              OK")

# Two explicit norm witnesses supply the only extra relations needed:
#   R^3 = Norm_{K(sqrt(3L))/K}(S + 3C sqrt(3L)), so (3L,R)=0;
#   -2  = Norm_{Q(sqrt(3))/Q}(1 + sqrt(3)), so (3,-2)=0.
assert sp.expand(S**2 - 27*L*C**2 - R**3) == 0
assert 1**2 - 3*1**2 == -2
cusp_norm_relation = {("3", "R"), ("L", "R")}
constant_norm_relation = {("-1", "3"), ("2", "3")}
reduced_hasse = brauer_sum(hasse, cusp_norm_relation, constant_norm_relation)
assert reduced_hasse == {("2", "L")}
print("3. norm relations reduce Hasse--Witt invariant to (2,L)       OK")

# L is geometrically irreducible: as a quadratic in A its discriminant is
# 4R^3, not a square in Qbar(B,C). Consequently the
# tame residue of (2,L) at the prime divisor L=0 is the nonsquare constant 2,
# proving that the surviving Brauer class is nontrivial over Q(A,B,C).
assert sp.factor(sp.discriminant(L, A) - 4*R**3) == 0
print("4. disc_A(L)=4R^3 supports nonzero residue of (2,L) at L    OK")
print("DONE — Hasse--Witt(T)=(2,L) over Q(A,B,C); it splits over R/C.")
