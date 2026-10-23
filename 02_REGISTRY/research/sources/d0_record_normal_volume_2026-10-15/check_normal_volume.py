#!/usr/bin/env python3
"""Exact algebra for the record normal-volume bridge.
The general tube/variation theorems are proved in the adjacent owner memo.
These finite checks do NOT prove native admission, action selection or GR.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from itertools import combinations, product
from pathlib import Path
import sympy as s

OWNER = '02_REGISTRY/research/sources/d0_flat_record_2026-10-15/check_flat_record.py'
OWNER_BLOB = '06f465874f07fae82111ee9453f4b5ca0b963267'
checks: list[str] = []


def eq(a, b, label):
    difference = a-b
    if isinstance(difference, s.MatrixBase):
        good = all(s.simplify(v) == 0 for v in difference)
    else:
        good = s.simplify(difference) == 0
    if not good:
        raise ArithmeticError(label)
    checks.append(label)


def require(good, label):
    if not good:
        raise ArithmeticError(label)
    checks.append(label)


def load_frame(root):
    path = root / OWNER
    raw = path.read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(blob == OWNER_BLOB, 'actual flat-record owner blob')
    spec = importlib.util.spec_from_file_location('pinned_flat_record', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.frame(4)[1]


def invariants(shapes):
    """Gauss curvature in an orthonormal tangent/normal frame, dimension four."""
    n = 4
    ric = s.zeros(n)
    H2 = s.S.Zero
    B2 = s.S.Zero
    for B in shapes:
        require(B.shape == (n, n) and B == B.T, 'symmetric four-dimensional shape')
        ric += s.trace(B)*B-B*B
        H2 += s.trace(B)**2
        B2 += s.trace(B*B)
    R = s.expand(s.trace(ric))
    Rm2 = s.S.Zero
    for i,j,k,l in product(range(n), repeat=4):
        value = sum((B[i,k]*B[j,l]-B[i,l]*B[j,k] for B in shapes), s.S.Zero)
        Rm2 += value**2
    Ric2 = s.trace(ric*ric)
    GB = s.expand(Rm2-4*Ric2+R**2)
    eq(R, H2-B2, 'contracted Gauss equation')
    return {'R': R, 'Ric': ric, 'B2': s.expand(B2), 'H2': s.expand(H2),
            'Rm2': s.expand(Rm2), 'Ric2': s.expand(Ric2), 'GB': GB}


def determinant_average(shapes, c2, c4, t):
    """Exact expectation from determinant evaluations and isotropic 2/4 moments.

    E xi_A xi_B=c2 delta_AB, E xi_A xi_B xi_C xi_D=
    c4(delta_AB delta_CD+delta_AC delta_BD+delta_AD delta_BC).
    Odd moments vanish; det is degree four, hence there is no higher remainder.
    """
    second = sum(((s.trace(B)**2-s.trace(B*B))/2 for B in shapes), s.S.Zero)
    dets = [s.expand(B.det()) for B in shapes]
    mixed = s.S.Zero
    for i,j in combinations(range(len(shapes)),2):
        mixed += ((shapes[i]+shapes[j]).det()+(shapes[i]-shapes[j]).det()
                  -2*dets[i]-2*dets[j])/2
    fourth = 3*sum(dets, s.S.Zero)+mixed
    return s.expand(1+c2*t**2*second+c4*t**4*fourth)


def run(root):
    checks.clear()
    ks = load_frame(root)
    t = s.symbols('t', real=True)
    c2, c4 = s.symbols('c2 c4', positive=True)
    p = (s.sqrt(5)-1)/2
    golden = s.simplify(p**3)
    B1 = s.diag(1,2,3,4)
    B2 = s.Matrix([[2,1,0,1],[1,-1,2,0],[0,2,3,1],[1,0,1,2]])
    B3 = s.Matrix([[0,1,1,0],[1,2,0,1],[1,0,-1,2],[0,1,2,1]])
    complete = []
    for i in range(4):
        B=s.zeros(4); B[i,i]=1; complete.append(B)
    for i,j in combinations(range(4),2):
        B=s.zeros(4); B[i,j]=B[j,i]=1; complete.append(B)
    fixtures = {'sphere':[s.eye(4)], 'rank_one':[s.diag(2,0,0,0)],
                'noncommuting_two':[B1,B2], 'noncommuting_three':[B1,B2,B3],
                'ten_normal_shapes':complete}
    data={}
    for name,shapes in fixtures.items():
        inv=invariants(shapes)
        direct=determinant_average(shapes,c2,c4,t)
        target=1+c2*t**2*inv['R']/2+c4*t**4*inv['GB']/8
        eq(direct,target,'exact all-orders determinant identity: '+name)
        # The graph (x, x^T B_A x/2) realizes these shapes as an actual local germ.
        norm_budget=sum((s.trace(B*B) for B in shapes),s.S.Zero)
        require(norm_budget/2500 < 1,'positive-Jacobian tube at |t xi|<=1/50: '+name)
        data[name]={'scalar':str(inv['R']),'gauss_bonnet':str(inv['GB'])}
    require(B1*B2 != B2*B1,'noncommuting shape fixture is genuine')
    # Independent exact integration for codimension one, uniform unit interval.
    x=s.symbols('x',real=True)
    d=(s.eye(4)-t*x*B1).det()
    eq(s.integrate(d,(x,-1,1))/2,
       determinant_average([B1],s.Rational(1,3),s.Rational(1,15),t),
       'independent exact interval normalizer')
    # Normal-frame covariance, contrasted with a covariance-isotropic but fourth-anisotropic rule.
    a,b=s.Rational(3,5),s.Rational(4,5)
    rotated=[a*B1+b*B2,-b*B1+a*B2]
    eq(determinant_average(rotated,c2,c4,t),determinant_average([B1,B2],c2,c4,t),
       'all 2/4 isotropic moments preserve normal-frame invariance')
    def axes_rule(shapes):
        return s.expand(sum(((s.eye(4)-t*B).det()+(s.eye(4)+t*B).det()
                             for B in shapes),s.S.Zero)/(2*len(shapes)))
    difference=s.expand(axes_rule(rotated)-axes_rule([B1,B2]))
    eq(difference.coeff(t,2),0,'second moments alone match')
    require(difference.coeff(t,4)!=0,'fourth-anisotropy is genuinely visible')
    # Same exact theory for arbitrary unused normal dimensions; no zero directions removed.
    inv=invariants([B1,B2])
    for k in (2,32,572):
        u=s.Rational(1,k+2); v=s.Rational(1,(k+2)*(k+4))
        eq(determinant_average([B1,B2],u,v,t),1+u*t*t*inv['R']/2+v*t**4*inv['GB']/8,
           'full normal-ball moments including zero directions: '+str(k))
    # Existing full golden record, expressed in orthonormal tangent coordinates.
    flat=[-2/s.sqrt(12*golden)*(k*k.T) for k in ks]
    f=invariants(flat)
    eq(f['R'],0,'actual golden record is intrinsically flat')
    eq(f['GB'],0,'actual golden record has zero Euler density')
    eq(f['H2'],16/golden,'actual full flat-record bending is nonzero')
    eq(f['B2'],16/golden,'actual flat-record second form norm')
    require(s.simplify(f['B2']/2500)<1,'actual golden flat tube has a positive Jacobian at radius 1/50')
    eq(determinant_average(flat,c2,c4,t),1,'flat record normalizer exactly one at every allowed scale')
    # Averaging log is not log of average: the missing cumulant is mean-curvature squared.
    quenched2=c2*f['B2']/2
    annealed2=-c2*f['R']/2
    eq(quenched2-annealed2,c2*f['H2']/2,'normalizer cumulant supplies intrinsic cancellation')
    eq(quenched2,8*c2/golden,'flat positive mean-log cost survives')
    jplus,jminus=1-t,1+t
    eq((jplus+jminus)/2,1,'two retained branches normalizer')
    mean_log=-s.log(1-t*t)/2
    eq(s.diff(mean_log,t,2).subs(t,0),1,'finite-branch mean-log mismatch')
    # Exact two-resolution contrast, without subtracting a fitted geometry term.
    R,E4,V=s.symbols('R E4 V',real=True)
    lam=s.symbols('lambda',positive=True)
    Z=lambda scale: V+c2*scale**2*R/2+c4*scale**4*E4/8
    contrast=s.cancel((Z(lam*t)-Z(t))/(c2*(lam*lam-1)*t*t/2))
    eq(contrast,R+c4*(lam*lam+1)*t*t*E4/(4*c2),'exact two-scale scalar action')
    eq(s.diff(contrast,R),1,'Einstein-Hilbert coefficient is exactly one')
    # Sphere integral checks the full metric variation, not only a pointwise scalar.
    radius=s.symbols('radius',positive=True)
    omega4=8*s.pi**2/3
    vol=omega4*radius**4; EH=12*omega4*radius**2; GBint=24*omega4
    spherecontrast=contrast.subs({V:vol,R:EH,E4:GBint})
    eq(s.diff(spherecontrast,radius),64*s.pi**2*radius,'finite-scale nonlinear sphere source')
    eq(s.diff(GBint,radius),0,'four-dimensional topological remainder has zero source')
    require(s.diff(radius**5*120/radius**4,radius)!=0,'five-dimensional Euler remainder is not discarded')
    require(s.diff(radius*GBint,radius)!=0,'moving coefficient cannot be declared topological')
    # Log of the local normalizer introduces R^2 at next order, unlike the raw contrast.
    local=1+c2*t*t*R/2+c4*t**4*E4/8
    log4=s.expand(s.series(-s.log(local),t,0,6).removeO()).coeff(t,4)
    eq(log4,c2**2*R**2/8-c4*E4/8,'local log keeps curvature-square correction')
    return {'scope':'conditional geometric normalizer/source theorem, not native price selection or full GR',
            'exact_checks':len(checks),'checked_labels':checks,
            'source_owner_git_blob':OWNER_BLOB,'fixture_invariants':data,
            'tube_normalizer':'1+c2*t^2*R/2+c4*t^4*GB/8 exactly in tangent dimension four',
            'two_scale_contrast':'int R dV + c4*(lambda^2+1)*t^2/(4*c2)*int GB dV',
            'full_metric_first_variation':'-int Einstein^{mu nu} delta q_mu nu dV; closed 4D or compact-support variations',
            'normal_moment_law':'fixed radial profile, c2>0; field-dependent moments retained separately',
            'flat_record_normalizer':'1 exactly in the permitted tube; full 24-state projector owner retained',
            'anisotropic_axis_rule_difference':str(difference),
            'native_measure_admitted':False,'native_action_binding':False,
            'Lorentz_spacetime_derived':False,'lattice_raw_source_limit_proved':False,
            'new_Lean_proof':False,'GR_closed':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    root=args.repo_root or Path(__file__).resolve().parents[4]
    text=json.dumps(run(root),ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.output: args.output.write_text(text,encoding='utf8')
    print(text,end='')

if __name__=='__main__': main()
