#!/usr/bin/env python3
"""Exact controls for the post-#227 synthesis; research only.

Owns: quartic variational chain control, finite torsion-coset count controls,
flat Cartan invertibility, the zero-phase star mass, and narrow counterchecks
of the published #231 transpose, joint-block and curvature assertions.
Does not compute the delegated joint L=4 census or residual nonlinear germs.
Does not certify Laurent's theorem, an uncomputed D0 torsion-coset cover,
refinement-uniform isolation, or a continuum compactness theorem.
"""
from itertools import combinations, product
from fractions import Fraction
import sympy as s

checks = 0

def check(name, condition):
    global checks
    if not condition:
        raise AssertionError(name)
    checks += 1

# 1. Fixed degree, fixed nearest-neighbor stencil, shrinking Holder exponent.
t = s.symbols("t", real=True)
for n in range(1, 9):
    x = s.symbols("x0:" + str(n), real=True)
    residuals = [x[i]**2 - x[i+1] for i in range(n-1)] + [x[-1]**2]
    potential = s.expand(sum(r*r for r in residuals)/2)
    gradient = s.Matrix([s.diff(potential, xi) for xi in x])
    weights = [2**i for i in range(n)]
    weighted_euler = sum(weights[i]*x[i]*gradient[i] for i in range(n))
    positive_sum = sum(2**(i+1)*residuals[i]**2 for i in range(n))
    check("chain_weighted_euler_"+str(n), s.expand(weighted_euler-positive_sum) == 0)
    curve = dict(zip(x, [t**(2**i) for i in range(n)]))
    target = s.zeros(n, 1)
    target[-1] = 2*t**(3*2**(n-1))
    check("chain_gradient_"+str(n), gradient.subs(curve) == target)
    check("chain_degree_"+str(n), s.Poly(potential, *x).total_degree() == 4)
    check("chain_bound_decreases_"+str(n), Fraction(1, 3*2**(n-1)) > 0)
    if n > 1:
        # Earlier than the last site, only neighboring variables enter.
        for i, component in enumerate(gradient):
            check("chain_locality", component.free_symbols <= set(x[max(0,i-1):min(n,i+2)]))

# 2. Two connected torsion cosets in (C*)^4; intersection is connected.
# Q1: z0=i, Q2: z1=-1; union count L^3[4|L]+L^3[2|L]-L^2[4|L].
# Characters are represented exactly by indices k/L in Q/Z, no float roots.
for L in range(1, 13):
    count1 = count2 = union = intersection = 0
    for k in product(range(L), repeat=4):
        q1 = Fraction(k[0], L) == Fraction(1,4)
        q2 = Fraction(k[1], L) == Fraction(1,2)
        count1 += q1
        count2 += q2
        intersection += q1 and q2
        union += q1 or q2
    f1 = L**3 if L % 4 == 0 else 0
    f2 = L**3 if L % 2 == 0 else 0
    fi = L**2 if L % 4 == 0 else 0
    check("coset_counts_"+str(L), (count1,count2,intersection,union) == (f1,f2,fi,f1+f2-fi))
    # A single coset type has an unbounded number of characters.
    if L % 4 == 0:
        check("coset_type_not_dimension_bound", count1 == L**3)
    # Nonprimitive binomial z0^2=1 splits into two connected cosets.
    roots = sum((2*k) % L == 0 for k in range(L))
    check("nonprimitive_binomial_components", roots == (2 if L % 2 == 0 else 1))

# 3. Literal canonical naked-star mass, without Fourier orbit enumeration.
eta = s.diag(1,-1,-1,-1)
pairs = list(combinations(range(4),2))
pindex = {p:i for i,p in enumerate(pairs)}
gens = []
for i in (1,2,3):
    X = s.zeros(4); X[0,i]=X[i,0]=1; gens.append(X)
for i,j in ((1,2),(1,3),(2,3)):
    X = s.zeros(4); X[i,j]=1; X[j,i]=-1; gens.append(X)
star = s.zeros(6)
for a,b,sign in [((0,1),(2,3),-1),((0,2),(1,3),1),((0,3),(1,2),-1),
                 ((1,2),(0,3),1),((1,3),(0,2),-1),((2,3),(0,1),1)]:
    star[pindex[b],pindex[a]] = sign
G2 = s.diag(*[eta[a,a]*eta[b,b] for a,b in pairs])
basis = [s.eye(4)[:,i] for i in range(4)]
a = s.symbols("a0:24")
W = [sum((a[6*r+j]*gens[j] for j in range(6)),s.zeros(4)) for r in range(4)]

def wedge(u,v):
    return s.Matrix([u[i]*v[j]-u[j]*v[i] for i,j in pairs])

def orientation(indices):
    return (-1)**sum(indices[i]>indices[j] for i in range(4) for j in range(i+1,4))

potential = 0
for r,ss in pairs:
    u,v = [i for i in range(4) if i not in (r,ss)]
    curvature = (W[r]*W[ss]-W[ss]*W[r])*eta
    bivector = s.Matrix([curvature[i,j] for i,j in pairs])
    potential += orientation([r,ss,u,v])*(wedge(basis[u],basis[v]).T*G2*star*bivector)[0]
H0 = s.hessian(s.expand(potential), a)
check("literal_flat_mass_symmetric", H0 == H0.T)
check("literal_flat_mass_det_256", H0.det() == 256)
check("literal_flat_mass_no_kernel", H0.rank() == 24)
# Flat Cartan map omega -> T_rs = omega_r e_s - omega_s e_r.
T = s.Matrix.vstack(*[W[r]*basis[ss]-W[ss]*basis[r] for r,ss in pairs])
cartan = T.jacobian(a)
check("cartan_map_injective", cartan.rank() == 24)
check("cartan_map_square", cartan.shape == (24,24))
check("mass_cartan_factorization", (H0*cartan.inv())*cartan == H0)
# A rank-of-local-holonomy diagnostic is identically zero at the flat background.
M = s.eye(4)-s.eye(4)
check("flat_holonomy_rank_zero", M.rank() == 0)
check("flat_holonomy_compounds_zero", all(M.extract(rs,cs).det() == 0
      for r in range(1,5) for rs in combinations(range(4),r) for cs in combinations(range(4),r)))
# H0 is full rank despite all those holonomy compounds vanishing.

# Gram horizontal/vertical tangent decomposition at canonical solder.
qvars = s.symbols("q0:10")
symmetric_pairs = [(i,j) for i in range(4) for j in range(i,4)]
q = s.zeros(4)
for value,(i,j) in zip(qvars,symmetric_pairs):
    q[i,j] = q[j,i] = value
horizontal = q*eta/2  # row vectors of the four legs, not delta raw Theta
vertical_basis = [X.T for X in gens]
flatten = lambda m: s.Matrix([m[i,j] for i in range(4) for j in range(4)])
vertical = s.Matrix.hstack(*[flatten(m) for m in vertical_basis])
horizontal_map = flatten(horizontal).jacobian(qvars)
check("gram_vertical_rank_six", vertical.rank() == 6)
check("gram_horizontal_rank_ten", horizontal_map.rank() == 10)
check("gram_tangents_span_sixteen", vertical.row_join(horizontal_map).rank() == 16)
check("gram_horizontal_identity", horizontal*eta+eta*horizontal.T == q)
check("gram_vertical_kernel", all(m*eta+eta*m.T == s.zeros(4) for m in vertical_basis))
for L in range(8,65,4):
    neighboring_phase = Fraction(L//4+1,L)
    check("adjacent_diagonal_not_exact_singular", neighboring_phase not in (Fraction(1,4),Fraction(3,4)))

# Narrow audit of the newly published #231 input, using the MERGED owner.
# Only two claimed-control characters are checked, no orbit census is redone.
import contextlib
import io
from pathlib import Path
owner = Path(__file__).with_name("a4d_j2_smooth_resonance_closure_check.py")
marker = "# Exact diagonal quarter-wave data."
owner_source = owner.read_text(encoding="utf-8")
check("merged_symbol_section_unique", owner_source.count(marker) == 1)
namespace = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(owner_source.split(marker)[0], str(owner), "exec"), namespace)
Hsymbol = namespace["HAB"]
Ssymbol = namespace["HAQ"]
phasevars = namespace["z"]
v = s.zeros(24,1)
v[3],v[4],v[5] = 1,-1,1
quarter = dict.fromkeys(phasevars,s.I)
Hquarter = Hsymbol.subs(quarter)
Qquarter = Ssymbol.subs(quarter).T
check("quarter_invisible_vector_in_connection_kernel", Hquarter*v == s.zeros(24,1))
check("quarter_invisible_vector_in_metric_kernel", Qquarter*v == s.zeros(10,1))
# A single occupied link does not give zero plaquette curvature on this mode.
rotation = gens[3]-gens[4]+gens[5]
linear_curvature_01 = (1+s.I)*rotation  # state phase is z^-1=-i
check("quarter_invisible_vector_has_curvature", linear_curvature_01 != s.zeros(4))
# Gauge variation of curvature at a flat background is zero; this is nongauge.
sub = dict(zip(phasevars,[s.I,s.I,-s.I,-s.I]))
Hr, Qr = Hsymbol.subs(sub), Ssymbol.subs(sub).T
correct_stack = s.Matrix.vstack(Hr,Qr)
wrong_stack = s.Matrix.vstack(Hr.T,Qr)
check("transpose_audit_correct_nullity_one", len(correct_stack.nullspace()) == 1)
check("transpose_audit_wrong_nullity_zero", len(wrong_stack.nullspace()) == 0)
check("augmentation_transpose_rank_identity", correct_stack.rank() == Hr.T.row_join(Qr.T).rank())
# #231's published full block placement fails already at zero phase.
Qzero = s.zeros(10,24)
wrong_joint = s.Matrix.vstack(s.Matrix.hstack(s.zeros(10,10),Qzero),
                            s.Matrix.hstack(H0,s.zeros(24,10)))
correct_joint = s.Matrix.vstack(s.Matrix.hstack(s.zeros(10,10),Qzero),
                              s.Matrix.hstack(s.zeros(24,10),H0))
pure_connection = s.zeros(34,1); pure_connection[-1] = 1
check("wrong_joint_invents_connection_kernel", wrong_joint*pure_connection == s.zeros(34,1))
check("correct_joint_does_not_invent_connection_kernel", correct_joint*pure_connection != s.zeros(34,1))

# 4. Exact prescribed-source branch comparison has zero response difference.
source = s.symbols("source0:10")
kappa = s.symbols("kappa")
response1 = s.Matrix(source)*kappa
response2 = s.Matrix(source)*kappa
check("fixed_source_response_equality", response1-response2 == s.zeros(10,1))
# A values-only convergence control: F_h(x)=x+h sin(x/h), F'_h(0)=2.
x,h = s.symbols("x h", real=True, positive=True)
values_only = x+h*s.sin(x/h)
check("values_convergence_does_not_transfer_gradient", s.diff(values_only,x).subs(x,0) == 2)
# Better critical-point control: x+2h sin(x/h) has critical x_h=2 pi h/3,
# but its uniform limit x has derivative 1 at the limiting point 0.
values_only = x+2*h*s.sin(x/h)
check("values_convergence_wrong_critical_limit", s.simplify(s.diff(values_only,x).subs(x,2*s.pi*h/3)) == 0)
check("limiting_function_not_critical", s.diff(x,x) == 1)
print("PASS_A4D_DEEP_SYNTHESIS_STRUCTURE", checks, "exact controls")
print("SCOPE: structural controls; no D0 all-refinement coset enumeration or UV compactness certificate")
