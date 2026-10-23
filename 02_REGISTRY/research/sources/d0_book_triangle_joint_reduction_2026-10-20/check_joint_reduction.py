#!/usr/bin/env python3
"""Bounded exact controls for the common Book multiplier theorem.

The polynomial stationary example is an algebraic control, NOT a native
action or a GR solution. Native application uses owned star homogeneity.
"""
import json
import sympy as s

r, x, y, u = s.symbols('r x y u', real=True)
p, ell = s.symbols('p ell', positive=True)
P = (x-y)**2+u*u*(x*x+y*y)
A = r*r/2
W = p**3*s.exp(-3*ell*r)
S = A+W*P
geom = [x, y, u]
root = {r: 0, x: 1, y: 1, u: 0}
assert s.expand(x*s.diff(P, x)+y*s.diff(P, y)-2*P) == 0
assert s.simplify(s.diff(S, r)-s.diff(A, r)-P*s.diff(W, r)) == 0
for z in geom:
    assert s.simplify(s.diff(S, z)-W*s.diff(P, z)) == 0
    assert s.simplify(s.diff(S, r, z)-s.diff(W, r)*s.diff(P, z)) == 0
for z in [r]+geom:
    assert s.diff(S, z).subs(root) == 0
H = s.hessian(S, [r]+geom).subs(root)
HP = s.hessian(P, geom).subs(root)
assert H[0, 0] == 1
assert H[0, 1:] == s.zeros(1, 3)
assert H[1:, 0] == s.zeros(3, 1)
assert H[1:, 1:] == p**3*HP
assert HP.rank() == 2
assert H[1:, 1:]-H[1:, 0]*H[0, 1:]/H[0, 0] == p**3*HP

# Exact SAME-action triangular coordinate substitution.
xx, yy = s.symbols('X Y', real=True)
new = s.simplify(S.subs({x: xx/s.sqrt(W), y: yy/s.sqrt(W)}))
assert s.simplify(new-A-P.subs({x: xx, y: yy})) == 0
map_jac = s.Matrix([s.sqrt(W)*x, s.sqrt(W)*y, r]).jacobian([x, y, r])
assert s.simplify(map_jac.det()-W) == 0

# Native original triangle count, forced multiplier and moving source.
assert 6*9*11*13 == 7722
native_Z3 = 7722*W
assert s.simplify(native_Z3/7722-W) == 0
assert s.simplify(s.diff(W, r)+3*ell*W) == 0
assert s.simplify(s.diff(W, r, 2)-9*ell**2*W) == 0

# Actual four-dimensional densitized scalar homogeneity, no assigned action.
a, b, c, d, scale = s.symbols('a b c d scale', positive=True)
ks = s.symbols('k0:4', real=True)
q = ks[0]**2/a**2-ks[1]**2/b**2-ks[2]**2/c**2-ks[3]**2/d**2
volume = a*b*c*d
matter = volume*q
scaled = {z: scale*z for z in (a, b, c, d)}
assert s.simplify(matter.subs(scaled, simultaneous=True)-scale**2*matter) == 0
assert s.simplify(q.subs(scaled, simultaneous=True)-q/scale**2) == 0
assert s.simplify(volume.subs(scaled, simultaneous=True)-scale**4*volume) == 0

# Hostile controls: every retained assumption matters.
# Fixing the coframe removes the radial Euler; a geometry-stationary point
# can have P != 0 and a genuine P DW internal source.
fixed_P = 1+u*u
assert s.diff(fixed_P, u).subs(u, 0) == 0
assert fixed_P.subs(u, 0) == 1
assert s.diff(A+W*fixed_P, r).subs({r: 0, u: 0}) == -3*ell*p**3
# Site-dependent weights do not preserve original-coordinate link roots.
w1, w2 = s.symbols('w1 w2', positive=True)
local = w1*x*x*u-w2*y*y*u
bare = x*x*u-y*y*u
assert all(s.diff(bare, z).subs({x: 1, y: 1, u: 0}) == 0 for z in geom)
assert s.diff(local, u).subs({x: 1, y: 1, u: 0}) == w1-w2
# Same-action local dressing does NOT commute with eliminating history
# while holding the ORIGINAL coframe fixed.
local_S = r*r/2+u*(s.exp(r)*x*x-y*y)
local_H = s.hessian(local_S, [r, x, y, u]).subs(root)
local_R = local_H[0, 1:]
local_correction = -local_R.T*local_R/local_H[0, 0]
assert local_correction[2, 2] == -1
local_new = s.simplify(local_S.subs(x, s.exp(-r/2)*xx))
assert s.simplify(local_new-r*r/2-u*(xx*xx-y*y)) == 0
assert all(s.diff(local_new, r, z) == 0 for z in (xx, y, u))
# Positive field-dependent W alone is insufficient at a singular radial map.
e = s.symbols('e', positive=True)
assert s.diff((1/e**2)*e**2, e) == 0
assert s.simplify(1+s.diff(s.log(1/e**2), e)*e/2) == 0
# Higher effective original-coordinate vertices need not be identical.
abstract_P = s.symbols('P', real=True)
regular = r*r/2+(1+r)*abstract_P
eliminated = s.expand(regular.subs(r, -abstract_P))
assert eliminated == abstract_P-abstract_P**2/2

print(json.dumps({
    'status': 'PASS',
    'input_ref': '960da9344e1893888d85d41fc57bdca9bade259e',
    'native_triangle_count': 7722,
    'native_common_factor': 'Tr(K^3)/7722; canonical p^3',
    'source_and_joint_Hessian': 'PASS exact independent product-chart control',
    'history_Schur_cross_block_at_root': '0',
    'all_order_coordinate_identity': 'S=A(r)+P(sqrt(W(r))*e,U)',
    'densitized_4D_massless_scalar_degree': 2,
    'hostile_fixed_boundary_control': 'P!=0, P*DW survives',
    'hostile_local_weight_control': 'original link source=w1-w2',
    'hostile_singular_radial_map': 'W=1/e^2 gives spurious constant action',
    'higher_original_coordinate_correction': '-P^2/2 in explicit internal elimination',
    'native_full_action_factorization_proved': False,
    'physical_internal_root_constructed': False,
    'GR_closed': False, 'raw216_closed': False
}, indent=2))
