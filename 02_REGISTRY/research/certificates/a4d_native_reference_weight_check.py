#!/usr/bin/env python3
"""Exact controls for the existing shape-sensitive referenceCellWeight family.

No new action or physical gate is installed. General proofs and scope are in
A4D_NATIVE_REFERENCE_WEIGHT_BOUNDARY.md. Default replay is immutable.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as sp

INPUT_HEAD = "75527846bf3603a1c51acf445f8354e3254341be"
INPUTS = [
 "03_FORMALIZATION/D0/Geometry/A4DLocatedMatterCellEnergy.lean",
 "03_FORMALIZATION/D0/Geometry/A4DDiscreteEnergyKernel.lean",
 "03_FORMALIZATION/D0/Geometry/ArchiveCARDegreePreserving.lean",
 "03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean",
 "03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean",
 "03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean",
 "03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean",
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument("--output", type=Path)
    ap.add_argument("--expect", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    checks = []
    def check(name, value):
        assert bool(value), name
        checks.append(name)
        print("PASS_"+name, flush=True)
    def entries(M):
        return [[str(x) for x in row] for row in M.tolist()]
    receipt_path = repo/"02_REGISTRY/research/certificates/a4d_native_reference_weight_results.json"
    receipt = json.loads(receipt_path.read_text())
    assert receipt["status"] == "PASS" and receipt["compiler_exit_code"] == 0
    assert not receipt["sorryAx"] and receipt["printed_axiom_dependencies"] == 17
    for path,digest in {**receipt["transitive_d0_source_sha256"], **receipt["toolchain_input_sha256"],
                        receipt["capsule"]: receipt["capsule_sha256"], receipt["output"]: receipt["output_sha256"]}.items():
        assert hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest, "LEAN_INPUT_CHANGED: "+path
    check("COMPILED_LITERAL_OPERATOR_AND_FRAME_BINDINGS", True)

    # Fock labels in literal A,B,C,D order, bit r records occupation of role r.
    sectors = [tuple((m >> r)&1 for r in range(4)) for m in range(16)]
    annih = []
    for r in range(4):
        A = sp.zeros(16)
        for ket,S in enumerate(sectors):
            if S[r]: A[ket-(1<<r),ket] = (-1)**sum(S[:r])
        annih.append(A)
    ends = [[annih[s].T*annih[r] for r in range(4)] for s in range(4)]
    vacuum = sp.zeros(16,1);vacuum[0]=1
    check("ALL_16_CAR_ENDS_ANNIHILATE_ACTUAL_VACUUM", all(ends[s][r]*vacuum == sp.zeros(16,1) for s in range(4) for r in range(4)))
    evars = sp.symbols('e0:16', real=True);e=sp.Matrix(4,4,evars)
    c,t,delta=sp.symbols('c t delta', real=True)
    q=[]
    for S in sectors:
        q.append(sum(e[r,a]**2 for r in range(4) for a in range(4) if not any(S) or S[r]))
    H = sp.trace(e)*sp.eye(16)-sum((e[s,r]*(ends[s][r]+ends[r][s]) for s in range(4) for r in range(4)),sp.zeros(16))
    W = sp.eye(16)+H+c*sp.diag(*q)
    F=lambda E: 1+sp.trace(E)+c*sum(z*z for z in E)
    check("FULL_16_COMPONENT_LITERAL_CONSTANT_WEIGHT", W.T==W and sp.expand(W*vacuum-F(e)*vacuum)==sp.zeros(16,1))
    check("ALL_SIXTEEN_SCALAR_READOUT_DERIVATIVES", sp.Matrix(4,4,[sp.diff(F(e),z) for z in evars])==sp.eye(4)+2*c*e)
    half=-sp.eye(4)/2
    check("NONZERO_FIELD_KERNEL_DEPENDS_ON_COEFFICIENT", F(half)==c-1)
    check("FULL_SCALAR_CRITICAL_COMPLETION", sp.expand(F(half+t*e).subs(c,1)-t*t*sum(z*z for z in e))==0)
    check("CRITICAL_NONDEGENERATE_RAW_GRAM", (sp.diag(1,-1,-1,-1)+half).det()==-sp.Rational(27,16))
    check("KERNEL_NOT_ALREADY_PRESENT_AT_FLAT", W.subs(dict(zip(evars,[0]*16)))==sp.eye(16))

    eta=sp.diag(1,-1,-1,-1)
    boost=sp.eye(4);boost[0,0]=boost[1,1]=sp.Rational(5,4);boost[0,1]=boost[1,0]=sp.Rational(3,4)
    check("BOOST_PROPER_TIME_ORIENTED", boost*eta*boost.T==eta and boost.det()==1 and boost[0,0]>0)
    e0=sp.zeros(4);e1=sp.diag(0,-1,0,0)
    defects=[]; frame_data={}
    for name,E in [('flat',e0),('second',e1),('critical',half)]:
        theta=eta+E;ep=theta*boost-eta
        check("RAW_GRAM_AND_ORIENTATION_PRESERVED_"+name, (eta+ep)*eta*(eta+ep).T==theta*eta*theta.T
              and theta.det()!=0 and (eta+ep).det()==theta.det())
        defect=sp.expand(F(ep)-F(E));defects.append(defect)
        frame_data[name]={"before":str(sp.expand(F(E))),"after":str(sp.expand(F(ep))),"defect":str(defect),"raw_determinant":str(theta.det())}
    check("FIRST_FRAME_DEFECT_FORCES_C_ZERO", defects[0]==5*c/4)
    check("SECOND_FRAME_DEFECT_REJECTS_C_ZERO", defects[1]==33*c/8-sp.Rational(1,4) and defects[1].subs(c,0)!=0)
    check("COEFFICIENT_INDEPENDENT_DEFECT_COMBINATION", sp.expand(defects[1]-sp.Rational(33,10)*defects[0])==-sp.Rational(1,4))
    check("SHARP_UNIFORM_FRAME_GAP_5_OVER_86", defects[0].subs(c,sp.Rational(2,43))==sp.Rational(5,86)
          and defects[1].subs(c,sp.Rational(2,43))==-sp.Rational(5,86))
    check("FIELD_KERNEL_NOT_LORENTZ_INVARIANT", frame_data['critical']['before']=='c - 1'
          and sp.simplify(F((eta+half)*boost-eta).subs(c,1))==sp.Rational(25,16))
    # Exterior minors are the literal owned representation; scalar state is fixed.
    ext=sp.zeros(16)
    for i,S in enumerate(sectors):
        rows=[r for r in range(4) if S[r]]
        for j,T in enumerate(sectors):
            cols=[r for r in range(4) if T[r]]
            if len(rows)==len(cols): ext[i,j]=boost.extract(rows,cols).det() if rows else 1
    check("ACTUAL_EXTERIOR_SCALAR_IS_FIXED", ext*vacuum==vacuum and ext.T*vacuum==vacuum)

    # Exact arbitrarily-small rational boost family, so the obstruction is local.
    z=sp.symbols('z', real=True)
    a=(1+z*z)/(1-z*z);b=2*z/(1-z*z)
    small=sp.eye(4);small[0,0]=small[1,1]=a;small[0,1]=small[1,0]=b
    E=sp.diag(0,-delta,0,0);Ep=(eta+E)*small-eta
    target=(a-1)*(-delta+2*c*(a*(delta*delta+2*delta+2)+delta*delta+delta))
    check("GENERAL_SMALL_BOOST_IS_LORENTZ", sp.simplify(small*eta*small.T-eta)==sp.zeros(4))
    check("GENERAL_NEAR_FLAT_DEFECT", sp.factor(F(Ep)-F(E)-target)==0)
    check("SMALL_BOOST_FLAT_FORCES_C_ZERO", sp.factor((F(Ep)-F(E)).subs(delta,0)-4*c*a*(a-1))==0)
    check("C_ZERO_FAILS_ARBITRARILY_NEAR_FLAT", sp.factor((F(Ep)-F(E)).subs(c,0)+delta*(a-1))==0)

    # Readout covectors cannot be fitted to ten metric slots if they see a vertical direction.
    X=sp.zeros(4);X[0,1]=X[1,0]=1
    rank_records={}
    for name,E,coeff in [('flat_c1',e0,1),('flat_c2',e0,2),('second_c0',e1,0)]:
        theta=(eta+E)*boost;ep=theta-eta
        dG=e*eta*theta.T+theta*eta*e.T
        slots=[(i,j) for i in range(4) for j in range(i,4)]
        jac=sp.Matrix([dG[i,j] for i,j in slots]).jacobian(evars)
        K=sp.eye(4)+2*coeff*ep
        kv=sp.Matrix(list(K));v=theta*X
        ward=sum(K[i,j]*v[i,j] for i in range(4) for j in range(4))
        check("ALL_TEN_GRAM_ROWS_AND_VERTICAL_RESPONSE_"+name, jac.rank()==10 and jac*sp.Matrix(list(v))==sp.zeros(10,1) and ward!=0)
        check("NO_METRIC_COVECTOR_FIT_"+name, jac.T.row_join(kv).rank()==11)
        rank_records[name]={"Gram_rank":10,"augmented_rank":11,"vertical_response":str(ward)}

    # Full exact Laurent symbol of the existing links/averages/CAR at the constant coframe.
    phases=sp.symbols('z0:4', nonzero=True)
    cs=[(x+1/x)/2 for x in phases]
    Hp=sum((half[r,r]*cs[r]*sp.eye(16) for r in range(4)),sp.zeros(16))
    for s in range(4):
        for r in range(4):
            Hp-=half[s,r]*(phases[s]*(1+1/phases[r])/2*ends[s][r]
                           +(1+phases[r])/phases[s]/2*ends[r][s])
    qhalf=[v.subs(dict(zip(evars,half))) for v in q]
    Wp=sp.eye(16)+Hp+c*sp.diag(*qhalf)
    eigen=[]
    for m,S in enumerate(sectors):
        k=sum(S)
        low=c-1 if k==0 else k-1+c*k/4
        roles=list(range(4)) if k==0 else [r for r in range(4) if not S[r]]
        ev=low+sum((1-cs[r])/2 for r in roles)
        assert sp.factor(Wp[m,m]-ev)==0
        assert all(Wp[m,n]==0 for n in range(16) if n!=m)
        eigen.append({"sector_ABCD":list(S),"degree":k,"minimum_on_unit_torus":str(low),"symbol":str(sp.expand(ev))})
    check("ALL_16_LAURENT_BLOCKS_WITH_LITERAL_SHIFT_PLACEMENT", True)
    check("C1_ONLY_POSSIBLE_KERNEL_SECTOR_IS_SCALAR", all(sp.Rational(sum(S))-1+sp.Rational(sum(S),4)>0 for S in sectors[1:]))
    check("C2_UNIFORM_LOWER_BOUND_IS_ONE_HALF", min([1]+[sp.Rational(sum(S))-1+sp.Rational(sum(S),2) for S in sectors[1:]])==sp.Rational(1,2))

    # Independent real-space matrix reconstruction at L=2, all 16 sectors.
    L=2;U=sp.Matrix([[0,1],[1,0]]);shifts=[]
    for r in range(4): shifts.append(sp.kronecker_product(*[U if i==r else sp.eye(L) for i in range(4)]))
    spectrum={1:[],2:[]};vacuum_kernel=None
    for m,S in enumerate(sectors):
        k=sum(S)
        Hx=sum((-sp.Rational(1,4)*(shifts[r]+shifts[r].T) for r in range(4)),sp.zeros(16))
        for r in range(4):
            if S[r]: Hx+=sp.eye(16)/2+(shifts[r]+shifts[r].T)/4
        for coeff in [1,2]:
            mat=sp.eye(16)+Hx+coeff*qhalf[m]*sp.eye(16)
            eigs=mat.eigenvals()
            spectrum[coeff].extend([v for v,n in eigs.items() for _ in range(n)])
            if coeff==1 and m==0: vacuum_kernel=mat.nullspace()
    check("FULL_REAL_SPACE_C1_KERNEL_EXACTLY_CONSTANT_SCALAR", spectrum[1].count(0)==1 and min(spectrum[1])==0
          and len(vacuum_kernel)==1 and vacuum_kernel[0]==sp.ones(16,1))
    check("FULL_REAL_SPACE_C2_POSITIVE_WITH_SHARP_GAP", min(spectrum[2])==sp.Rational(1,2) and len(spectrum[2])==256)
    gaps={}
    for L in [2,3,4,8,12]:
        gap=sp.simplify(min(sp.Rational(1,4),sp.sin(sp.pi/L)**2))
        gaps[str(L)]=str(gap)
        check(f"SCALAR_FIRST_NONZERO_FOURIER_MODE_{L}", sp.simplify((1-sp.cos(2*sp.pi/L))/2-sp.sin(sp.pi/L)**2)==0)
    check("C1_RANGE_GAP_VANISHES", sp.limit(sp.sin(sp.pi/z)**2,z,sp.oo)==0 and sp.limit(z*z*sp.sin(sp.pi/z)**2,z,sp.oo)==sp.pi**2)
    check("SINGULAR_WEIGHT_ROOT_IS_NOT_A_POSITIVE_WEIGHT", F(half).subs(c,1)==0 and F(half).subs(c,sp.Rational(1,2))<0)

    payload={"status":"PASS","input_head":INPUT_HEAD,
      "input_sha256":{p:hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in INPUTS},
      "lean_capsule_receipt_sha256":hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
      "checks":checks,"frame_controls":frame_data,"metric_covector_controls":rank_records,
      "uniform_frame_defect_lower_bound":"5/86","sharp_coefficient":"2/43",
      "constant_coframe":entries(half),"all_sector_symbols":eigen,"c1_range_gaps":gaps,
      "c2_uniform_lower_bound":"1/2",
      "scope":"Existing reference weight operator, scalar readout/frame descent and kernel/range classification at a fixed nondegenerate flat Gram. No new action, coupled source/Ward, continuum recovery, positive GR or full-core no-go."}
    if args.output: args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    expected=args.expect or (Path(__file__).with_name('a4d_native_reference_weight_certificate.json') if not args.output else None)
    if expected:
        assert json.loads(expected.read_text())==payload,'PINNED_LEDGER_MISMATCH'
        print('PASS_IMMUTABLE_PINNED_LEDGER',flush=True)
    print('PASS_NATIVE_REFERENCE_WEIGHT_BOUNDARY',len(checks),flush=True)

if __name__=='__main__': main()
