#!/usr/bin/env python3
"""Exact controls for the actual positive point-state refinement boundary.

Infinite state classification and weak-limit proofs are in the companion memo.
Finite fixtures are controls, not substitutes for those all-size arguments.
Default replay checks an immutable ledger and the compiled owner/source pins.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import comb, prod
from pathlib import Path
import hashlib
import json
import sympy as sp

INPUT_HEAD = "60ebc9b6832ee2c12d08b5b3fdb3d3725e6feba5"
INPUTS = [
    "03_FORMALIZATION/D0/Geometry/ArchiveLaplacianRG.lean",
    "03_FORMALIZATION/D0/Geometry/ArchivePhaseDistance.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseProductCarrier.lean",
    "03_FORMALIZATION/D0/Geometry/Archive1DCochainRefinement.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveRefinementHodgeWeights.lean",
    "03_FORMALIZATION/D0/Geometry/A4DGoldenAFCommutativeTargetBoundary.lean",
    "03_FORMALIZATION/D0/Probability/FiniteArchiveMeasure.lean",
    "02_REGISTRY/research/A4D_NATIVE_VERIFICATION_REFINEMENT_BOUNDARY.md",
    "02_REGISTRY/research/A4D_NATIVE_COCHAIN_REFINEMENT.md",
    "02_REGISTRY/research/A4D_NATIVE_LOGDET_SOURCE_BOUNDARY.md",
]


def cap(L, j):
    return j if j < L else 0


def actual_composite(L, M, j):
    assert 2 <= L <= M and 0 <= j < M
    for size in range(M - 1, L - 1, -1):
        j %= size
    return j


def project(L, M, x):
    return tuple(actual_composite(L, M, j) for j in x)


def push(weights, p):
    result = defaultdict(F)
    for x, mass in weights.items():
        result[p(x)] += mass
    return dict(result)


def tv(mu, nu):
    return sum((abs(mu.get(x, 0) - nu.get(x, 0)) for x in mu.keys() | nu.keys()), F(0)) / 2


def uniform(L, dim=1):
    return {x: F(1, L**dim) for x in product(range(L), repeat=dim)}


def tv_formula(L, M, dim):
    return sum((comb(dim, k) * (L - 1)**(dim - k)
                * abs(F((M - L + 1)**k, M**dim) - F(1, L**dim))
                for k in range(dim + 1)), F(0)) / 2


def geometric_weights(L, ratio):
    return [1 - ratio + ratio**L] + [(1 - ratio) * ratio**j for j in range(1, L)]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument("--output", type=Path)
    ap.add_argument("--expect", type=Path)
    args = ap.parse_args(); repo = args.repo.resolve(); checks = []
    sha = lambda p: hashlib.sha256((repo/p).read_bytes()).hexdigest()
    def check(name, condition):
        assert bool(condition), name
        checks.append(name); print("PASS_" + name, flush=True)

    receipt_path = "02_REGISTRY/research/certificates/a4d_native_measure_refinement_results.json"
    receipt = json.loads((repo/receipt_path).read_text())
    assert receipt["status"] == "PASS" and receipt["compiler_exit_code"] == 0 and not receipt["sorryAx"]
    assert receipt["printed_axiom_dependencies"] == 25
    assert set(receipt["axioms"]) <= {"propext", "Classical.choice", "Quot.sound"}
    output = (repo/receipt["output"]).read_text()
    assert not any(s in output for s in ["sorryAx", "error:", "warning:"])
    for p, digest in {**receipt["transitive_d0_source_sha256"], **receipt["toolchain_input_sha256"],
                      receipt["capsule"]: receipt["capsule_sha256"], receipt["output"]: receipt["output_sha256"]}.items():
        assert sha(p) == digest, "LEAN_INPUT_CHANGED: " + p
    check("COMPILED_ACTUAL_HISTORY_STATE_AND_MASS_BINDINGS", True)

    pairs = [(2,3),(3,4),(3,7),(4,8),(4,12),(8,16),(12,24),(16,64)]
    for L, M in pairs:
        check(f"ACTUAL_COMPOSITE_AND_ALL_POINT_HISTORIES_{L}_{M}",
              all(actual_composite(L,M,j) == cap(L,j) for j in range(M))
              and all(cap(L,cap(M,j)) == cap(L,j) for j in range(2*M)))
    check("LONG_JUMP_SINGLE_MODULO_IS_NOT_NATIVE", actual_composite(4,8,5) == 0 and 5%4 == 1)
    check("FULL_ROLE_COMPOSITE_IS_COORDINATEWISE", all(
          project(4,8,x) == tuple(cap(4,j) for j in x) for x in product(range(8),repeat=4)))
    def collapse(t): return 2*t if t<F(1,2) else F(0)
    def circle_distance(a,b): return min(abs(a-b),1-abs(a-b))
    for L in [4,8,12,16]:
        check("ACTUAL_DOUBLED_PHYSICAL_READOUT_"+str(L),all(
              F(actual_composite(L,2*L,j),L)==collapse(F(j,2*L)) for j in range(2*L)))
    points=[F(j,32) for j in range(32)]
    check("COLLAPSE_IS_CONTINUOUS_TORUS_LIPSCHITZ_CONTROL",all(
          circle_distance(collapse(a),collapse(b))<=2*circle_distance(a,b) for a in points for b in points))
    check("EVERY_RATIONAL_CONTROL_IS_ABSORBED",all(
          collapse(collapse(collapse(collapse(collapse(collapse(t))))))==0 for t in points))
    n=sp.symbols("n",nonnegative=True,integer=True)
    check("ALL_SIZE_SMOOTH_PEAK_RECURRENCE_POLYNOMIAL",sp.expand(4*(n+1)**3-(2*n+1)**2*(n+2))==3*n+2)
    for N in [1,3,6,12,24,48]:
        b=F(comb(2*N,N),4**N)
        check("EXACT_SMOOTH_PEAK_MEAN_BOUND_"+str(N),b*b<=F(1,N+1)
              and F(comb(2*(N+1),N+1),4**(N+1))==b*F(2*N+1,2*N+2))
    rho_min,rho_max=F(54,67),F(242,201);N=6;b=F(comb(2*N,N),4**N)
    check("FIXED_SMOOTH_VOLUME_WITNESS_QUANTITATIVE_LOWER_BOUND",
          (N+1)**2>=32*rho_max/rho_min and rho_min/16-rho_max*b**4>=rho_min/32)
    # Every finite prefix is determined by its top point. Infinite classification
    # is separately compiled, not inferred from these finite counts.
    for M in [3,4,8,12]:
        prefixes = [tuple(actual_composite(L,M,j) for L in range(2,M+1)) for j in range(M)]
        check("FINITE_PREFIXES_MATCH_BIRTH_CODES_"+str(M), len(set(prefixes)) == M and all(
              h == tuple(cap(L,j) for L in range(2,M+1)) for j,h in enumerate(prefixes)))

    state_controls = {}
    for L in [2,3,4,8,16]:
        M=L+1; weights=[F(j+1, M*(M+1)//2) for j in range(M)]
        B=sp.Matrix(M,L,lambda j,i:int(j%L == i))
        W=sp.diag(*map(sp.Rational,weights)); G=B.T*W*B
        coarse=push({(j,):weights[j] for j in range(M)},lambda x:(x[0]%L,))
        check("POSITIVE_STATE_DUAL_AND_SCALAR_MASS_"+str(L),
              sum(coarse.values()) == 1 and all(v>0 for v in coarse.values())
              and G == sp.diag(*(sp.Rational(coarse[(i,)]) for i in range(L))))
        f=sp.Matrix([i*i-2*i+3 for i in range(L)])
        check("ALL_BASIS_WEIGHTS_AND_QUADRATIC_PULLBACK_"+str(L),
              ((B*f).T*W*(B*f))[0] == (f.T*G*f)[0]
              and all((B.T*sp.Matrix(weights))[i] == G[i,i] for i in range(L)))
        state_controls[str(L)]={"zero_weight":str(coarse[(0,)]),"positive_total":str(sum(coarse.values()))}
    bad=sp.Matrix([[1,-2],[-2,5]])
    check("POSITIVE_QUADRATIC_MATRIX_NEED_NOT_GIVE_POSITIVE_POINT_STATE",
          bad[0,0]>0 and bad.det()==1 and bad*sp.ones(2,1)==sp.Matrix([-1,3]))

    geometric = {}
    ratio=F(2,3)
    for L in [2,4,8,12,16,32]:
        M=2*L; coarse=geometric_weights(L,ratio); fine=geometric_weights(M,ratio)
        pushed=push({(j,):fine[j] for j in range(M)},lambda x:(actual_composite(L,M,x[0]),))
        mean=sum((coarse[j]*F(j,L) for j in range(L)),F(0))
        check("INFINITE_SUPPORT_COMPATIBLE_POSITIVE_PROFILE_"+str(L),
              sum(coarse)==sum(fine)==1 and min(coarse)>0
              and all(pushed[(j,)] == coarse[j] for j in range(L)))
        check("DIRECT_PLACEMENT_ATOMIC_CONCENTRATION_BOUND_"+str(L),
              mean <= ratio/((1-ratio)*L) and coarse[0]>=1-ratio)
        geometric[str(L)]={"origin_mass":str(coarse[0]),"coordinate_mean":str(mean),"bound":str(F(2,L))}

    atoms={(1,1,2,3):F(1,4),(0,7,0,2):F(1,3),(5,0,1,11):F(1,6),(0,0,0,0):F(1,4)}
    assert sum(atoms.values())==1
    def mixture(L): return push(atoms,lambda a:tuple(cap(L,j) for j in a))
    for L,M in [(2,4),(4,8),(8,12),(12,16)]:
        mu,nu=mixture(L),mixture(M)
        check(f"CORRELATED_BIRTH_MIXTURE_FULL_ROLE_COMPATIBILITY_{L}_{M}",
              push(nu,lambda x:project(L,M,x))==mu and sum(mu.values())==1)
    mu=mixture(16)
    joint=sum(v for x,v in mu.items() if x[0]==1 and x[1]==1)
    marg0=sum(v for x,v in mu.items() if x[0]==1);marg1=sum(v for x,v in mu.items() if x[1]==1)
    check("NO_COORDINATE_INDEPENDENCE_ASSUMED", joint==F(1,4) and joint != marg0*marg1)
    def full_correlated(L):
        a,b=geometric_weights(L,F(1,2)),geometric_weights(L,F(2,3))
        return {x:(prod(a[j] for j in x)+prod(b[j] for j in x))/2
                for x in product(range(L),repeat=4)}
    mu,nu=full_correlated(4),full_correlated(8)
    check("STRICTLY_POSITIVE_CORRELATED_FIBERS_ARE_NONEMPTY", min(mu.values())>0 and min(nu.values())>0
          and sum(mu.values())==sum(nu.values())==1 and push(nu,lambda x:project(4,8,x))==mu)

    defects={}
    for L,M in [(2,3),(3,4),(4,5),(4,8),(8,16),(12,24),(16,32),(64,128)]:
        one=push(uniform(M),lambda x:project(L,M,x)); expected=F((L-1)*(M-L),L*M)
        check(f"EXACT_ONE_COORDINATE_TOTAL_VARIATION_{L}_{M}", tv(uniform(L),one)==expected)
        four=tv_formula(L,M,4)
        if M<=8:
            full=push(uniform(M,4),lambda x:project(L,M,x))
            check(f"FULL_ROLE_TV_FORMULA_ENUMERATION_{L}_{M}",tv(uniform(L,4),full)==four)
        if M==2*L and L>=16:
            check("SHARP_COMPOSED_FOUR_ROLE_DEFECT_"+str(L),four==F(15,16)*F(L-1,L)**4)
        defects[f"{L}_{M}"]={"one":str(expected),"four":str(four)}
    for L in [4,8,16,32,64]:
        one_step=F(L-1,L*(L+1));total=sum((F(k-1,k*(k+1)) for k in range(L,2*L)),F(0))
        check("ADJACENT_SMALLNESS_DOES_NOT_CONTROL_COMPOSITION_"+str(L),
              tv_formula(L,L+1,4)<=4*one_step and one_step<F(1,L)
              and total>=F(L-1,2*L) and F(L-1,2*L)>=F(3,8))
    # Finite prefixes can be perfectly compatible and have a uniform top;
    # changing the top changes the purported earlier physical state.
    mu4_top8=push(uniform(8),lambda x:project(4,8,x))
    mu4_top16=push(uniform(16),lambda x:project(4,16,x))
    check("FINITE_HORIZON_UNIFORM_TOP_IS_NOT_ONE_INFINITE_STATE", mu4_top8!=mu4_top16
          and mu4_top8[(0,)]==F(5,8) and mu4_top16[(0,)]==F(13,16))

    z=sp.symbols("z");trig={}
    for L in [4,8,12,16,20,24]:
        modulus=sp.Poly(sp.cyclotomic_poly(L,z),z,domain=sp.QQ)
        reduce=lambda expr:sp.Poly(sp.expand(expr),z,domain=sp.QQ).rem(modulus).as_expr()
        cosines=[(z**j+z**((-j)%L))/2 for j in range(L)]
        csum=reduce(sum(cosines));c2=reduce(sum(c*c for c in cosines))
        volume=reduce(sum((1+c/10)**2 for c in cosines))/L
        fsum=reduce(sum(1-c for c in cosines))
        check("EXACT_CYCLOTOMIC_SMOOTH_AND_CURVED_VOLUME_SUMS_"+str(L),
              csum==0 and c2==sp.Rational(L,2) and volume==sp.Rational(201,200) and fsum==L)
        trig[str(L)]={"volume":str(volume),"smooth_sum":str(fsum)}
    L,M=4,8;one_minus_cos=[0,1,2,1]
    def smooth(x):return prod(one_minus_cos[j] for j in x)
    target=sum(F(smooth(x),L**4) for x in product(range(L),repeat=4))
    projected=sum(F(smooth(project(L,M,x)),M**4) for x in product(range(M),repeat=4))
    check("FIXED_SMOOTH_FULL_ROLE_COMPOSED_GAP",target==1 and projected==F(1,16)
          and target-projected==F(15,16))

    # Exact Q(sqrt(2)) arithmetic for every point of the curved 8^4 grid.
    cs=[(F(1),F(0)),(F(0),F(1,2)),(F(0),F(0)),(F(0),-F(1,2)),
        (-F(1),F(0)),(F(0),-F(1,2)),(F(0),F(0)),(F(0),F(1,2))]
    q2=[]
    for a,b in cs:
        a,b=1+a/10,b/10
        q2.append((a*a+2*b*b,2*a*b))
    total=[F(0),F(0)];observed=[F(0),F(0)];norm=F(200,201*M**4)
    for x in product(range(M),repeat=4):
        v=one_minus_cos[actual_composite(L,M,x[1])]
        for k in range(2):
            total[k]+=norm*q2[x[0]][k]
            observed[k]+=norm*q2[x[0]][k]*v
    check("ACTUAL_CURVED_VOLUME_FULL_ROLE_COMPOSED_GAP",total==[1,0] and observed==[F(1,2),0])

    eta=sp.diag(1,-1,-1,-1);q0=sp.Rational(11,10);metric=q0*eta;inverse=metric.inv()
    jet=sp.zeros(4);jet[0,0]=-2*sp.pi**2/5
    def dGamma(a,b,d,c):
        return sp.simplify(sum(eta[a,m]*(eta[m,d]*jet[c,b]+eta[m,b]*jet[c,d]-eta[b,d]*jet[c,m])
                               for m in range(4))/(2*q0))
    Ricci=sp.Matrix(4,4,lambda b,d:sp.simplify(sum(dGamma(a,b,d,a)-dGamma(a,b,a,d) for a in range(4))))
    Rstd=sp.simplify(sum(inverse[b,d]*Ricci[b,d] for b in range(4) for d in range(4)))
    check("ALL_CURVED_SECOND_JET_RICCI_AND_OWNER_SIGN",metric.det()==-q0**4
          and Ricci==Ricci.T and Rstd==120*sp.pi**2/121)
    dc,df=F(1,16),F(1,64);base=F(201,200)
    corrected_coarse=1-dc/(base+dc*dc/2)
    corrected_fine=(base/2+df*df/8)/(base+df*df/2)
    check("SMALL_NONSEPARABLE_METRIC_CORRECTION_DOES_NOT_REMOVE_GAP",
          corrected_coarse-corrected_fine>F(2,5) and F(9,10)-dc>0)

    # Protected controls: different refinement, macroscopic reconstruction,
    # and the actual separate finite archive measure.
    floor_push=push(uniform(8,4),lambda x:tuple(j//2 for j in x))
    check("DIFFERENT_DYADIC_RULE_HAS_COMPATIBLE_DIFFUSE_RECOVERY",floor_push==uniform(4,4)
          and all(max(abs(F(j,8)-F(j//2,4)) for j in x)<=F(1,8)
                  for x in product(range(8),repeat=4)))
    check("DYADIC_RULE_IS_NOT_ACTUAL_NATIVE_COMPOSITE",project(4,8,(5,5,5,5))!=(2,2,2,2))
    kernel={x:F(1,4**4) for x in product(range(4),repeat=4)}
    check("MACROSCOPIC_KERNEL_CAN_IMPORT_ANY_DIFFUSE_TARGET",sum(kernel.values())==1
          and kernel==uniform(4,4) and kernel[(2,0,0,0)]>0)
    points=[]
    for r in range(4):
        for sign in [-1,1]:
            x=[F(0)]*4;x[r]=F(sign,5);points.append(tuple(x))
    check("LITERAL_EIGHT_ATOM_MEASURE_REMAINS_DISTINCT",len(set(points))==8
          and all(sum(x[r]*x[s]/8 for x in points)==(F(1,100) if r==s else 0)
                  for r in range(4) for s in range(4)))

    payload={"status":"PASS","input_head":INPUT_HEAD,"inputs_sha256":{p:sha(p) for p in INPUTS},
        "lean_receipt_sha256":sha(receipt_path),"checks":checks,"state_controls":state_controls,
        "geometric_positive_controls":geometric,"total_variation_controls":defects,"exact_trig_controls":trig,
        "compatible_state_class":"all nonnegative summable mixtures on N^Role with total mass one",
        "history_class":"countable actual coordinatewise Role histories; not the flattened archive",
        "weak_limit_class":"PURELY_ATOMIC_FOR_ARBITRARY_POINT_AND_SHRINKING_POSITIVE_KERNEL_READOUTS",
        "approximate_extension":"TOTAL_COMPOSED_TV_ERROR_TENDS_TO_ZERO; SUMMABLE_STEP_ERROR_SUFFICES",
        "direct_smooth_compatibility":"ONLY_DELTA0_LIMIT_UNDER_ALL_FIXED_SMOOTH_DOUBLING_TESTS",
        "smooth_positive_density_gap_bound":"m / 32 with (N+1)^2 >= 32 M/m",
        "adjacent_smallness":"INSUFFICIENT; UNIFORM_DIFFUSE_STATES_HAVE_O(1/L)_STEP_DEFECT",
        "uniform_smooth_composed_gap":"15 / 16","curved_volume_weak_gap":"1 / 2",
        "curved_metric_R_owner":"-120 pi^2 / 121","curved_metric_total_volume":"201 / 200",
        "small_metric_correction_gap_control":str(corrected_coarse-corrected_fine),
        "scope":"Complete positive point-state class on the actual coordinatewise refinement diagram. No claim that action-contrast estimates imply TV, no native physical measure selection, no field-state or full-core no-go.",
        "protected_exceptions":["Only adjacent errors tend to zero","Finite compatible prefixes with changing top state",
            "Different nested-grid projections","Macroscopic nonlocal probability kernels",
            "Field-state configurations and signed or nonpositive point functionals",
            "Distinct flattened archive and its already constructed golden record measure"]}
    out=json.dumps(payload,sort_keys=True,indent=2)+"\n"
    if args.output:args.output.write_text(out)
    else:
        expected=args.expect or Path(__file__).with_name("a4d_native_measure_refinement_certificate.json")
        assert expected.read_text()==out,"PINNED_LEDGER_MISMATCH"
        print("PASS_IMMUTABLE_PINNED_LEDGER")
    print("PASS_NATIVE_MEASURE_REFINEMENT",len(checks))


if __name__=="__main__":main()
