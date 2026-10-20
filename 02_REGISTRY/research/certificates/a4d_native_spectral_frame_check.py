#!/usr/bin/env python3
"""Immutable exact controls for the native flux spectral-frame obstruction.

The arbitrary-function theorem is compiled in the companion Lean capsule;
finite fixtures do not replace its quantifiers. No action or physical gate
is defined by this checker.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as sp

INPUT_HEAD = '080cb15ceb6b273f1f4bb5ccaae50251307d257b'
INPUTS = [
 '03_FORMALIZATION/D0/Geometry/A4DDiscreteEnergyKernel.lean',
 '03_FORMALIZATION/D0/Geometry/A4DConstitutiveKernelClassification.lean',
 '03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean',
 '03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean',
 '02_REGISTRY/research/certificates/a4d_native_reference_weight.lean',
 '02_REGISTRY/research/certificates/a4d_native_reference_weight_results.json',
]

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
    ap.add_argument('--output',type=Path)
    ap.add_argument('--expect',type=Path)
    args=ap.parse_args();repo=args.repo.resolve();checks=[]
    def check(name,truth):
        assert bool(truth),name
        checks.append(name);print('PASS_'+name,flush=True)
    def sha(p):return hashlib.sha256((repo/p).read_bytes()).hexdigest()
    for stem,count in [('spectral_frame',14),('reference_weight',17)]:
        rec=json.loads((repo/('02_REGISTRY/research/certificates/a4d_native_'+stem+'_results.json')).read_text())
        assert rec['compiler_exit_code']==0 and rec['status']=='PASS'
        assert not rec['sorryAx'] and rec['printed_axiom_dependencies']==count
        assert set(rec['axioms']) <= {'propext','Classical.choice','Quot.sound'}
        for p,d in {**rec['transitive_d0_source_sha256'],**rec['toolchain_input_sha256'],
                    rec['capsule']:rec['capsule_sha256'],rec['output']:rec['output_sha256']}.items():
            assert sha(p)==d,'COMPILED_INPUT_CHANGED: '+p
    check('COMPILED_ACTUAL_OPERATOR_AND_EXTERIOR_BINDINGS',True)
    a,b,alpha,delta,s=sp.symbols('a b alpha delta s',real=True)
    eta=sp.diag(1,-1,-1,-1)
    B=sp.eye(4);B[0,0]=B[1,1]=a;B[0,1]=B[1,0]=b
    reduce=lambda z:sp.rem(sp.expand(z),b*b-a*a+1,b)
    check('GENERAL_CONNECTED_BOOST_LORENTZ',all(reduce(z)==0 for z in B*eta*B.T-eta))
    check('GENERAL_CONNECTED_BOOST_PROPER',sp.expand(B.det())==a*a-b*b)
    fixed=B.subs({a:sp.Rational(5,4),b:sp.Rational(3,4)})
    check('FIXED_RATIONAL_BOOST_PROPER_TIME_ORIENTED',fixed.det()==1 and fixed[0,0]>0)
    sectors=[tuple((m>>r)&1 for r in range(4)) for m in range(16)]
    annih=[]
    for r in range(4):
        A=sp.zeros(16)
        for m,S in enumerate(sectors):
            if S[r]:A[m-(1<<r),m]=(-1)**sum(S[:r])
        annih.append(A)
    ends=[[annih[r].T*annih[t] for t in range(4)] for r in range(4)]
    vacuum=sp.zeros(16,1);vacuum[0]=1
    check('ALL_16_LITERAL_CAR_ENDS_KILL_SCALAR',all(C*vacuum==sp.zeros(16,1) for row in ends for C in row))
    def H(E):return sp.trace(E)*sp.eye(16)-sum((E[r,t]*(ends[r][t]+ends[t][r]) for r in range(4) for t in range(4)),sp.zeros(16))
    p=lambda z:1+z+alpha*z*z
    thetas={'minus':sp.diag(1,-2,-sp.Rational(1,2),-sp.Rational(1,2)),
            'plus':sp.diag(2,-1,-sp.Rational(3,2),-sp.Rational(3,2))}
    rays={};defects={};action_defects={};verticals={}
    evars=sp.symbols('e0:16',real=True);E=sp.Matrix(4,4,evars);theta=eta+E
    G=theta*eta*theta.T
    packed=[(i,j) for i in range(4) for j in range(i,4)]
    J=sp.Matrix([G[i,j] for i,j in packed]).jacobian(evars)
    Tvars=sp.symbols('T0:10',real=True);T=sp.zeros(4)
    for v,(i,j) in zip(Tvars,packed):T[i,j]=T[j,i]=v
    packed_gradient=J.T*sp.Matrix([T[i,j]*(1 if i==j else 2) for i,j in packed])
    check('ALL_TEN_PACKED_METRIC_WEIGHTS',sp.expand(packed_gradient-sp.Matrix(list(2*T*theta*eta)))==sp.zeros(16,1))
    X=sp.zeros(4);X[0,1]=X[1,0]=1
    for name,theta0 in thetas.items():
        sign=-1 if name=='minus' else 1
        check('NONDEGENERATE_ORIENTED_'+name,theta0.det()<0 and theta0[0,0]>0 and sp.trace(theta0-eta)==0)
        theta1=theta0*B
        check('ENTIRE_RAW_GRAM_ORBIT_'+name,all(reduce(z)==0 for z in theta1*eta*theta1.T-theta0*eta*theta0.T))
        ray=sp.trace(theta1-eta)
        check('EXACT_SCALAR_RAY_'+name,sp.expand(ray-sign*(a-1))==0)
        rays[name]={'theta_det':str(theta0.det()),'scalar_argument':str(ray),'base_argument':'0'}
        h=H(theta1-eta)
        check('FULL_CONSTANT_FOCK_OPERATOR_SCALAR_'+name,h*vacuum==ray*vacuum and h.T==h)
        q=sp.eye(16)+h+alpha*h*h
        check('LITERAL_QUADRATIC_KERNEL_AND_ACTION_'+name,sp.expand(q*vacuum-p(ray)*vacuum)==sp.zeros(16,1)
              and sp.expand((vacuum.T*q*vacuum)[0]/2-p(ray)/2)==0)
        defect=sp.expand((p(ray)-p(0)).subs({a:sp.Rational(5,4),b:sp.Rational(3,4)}))
        defects[name]=defect;action_defects[name]=defect/2
        check('FIXED_DEFECT_'+name,defect==sign*sp.Rational(1,4)+alpha/16)
        th=theta0*fixed;ep=th-eta;site=dict(zip(evars,list(ep)))
        jp=J.subs(site);vertical=sp.Matrix(list(th*X));covector=(1+2*alpha*sp.trace(ep))*sp.Matrix(list(sp.eye(4)))
        check('ALL_TEN_GRAM_ROWS_AND_VERTICAL_KERNEL_'+name,jp.rank()==10 and jp*vertical==sp.zeros(10,1))
        v=sp.expand((covector.T*vertical)[0]);verticals[name]=v
        check('LITERAL_VERTICAL_RESPONSE_'+name,v==sign*sp.Rational(3,4)*(1+sign*alpha/2))
        alphas=[0,sp.Rational(1,4),1,2] if name=='plus' else [0,sp.Rational(1,4),1,-2]
        check('NO_METRIC_COVECTOR_FIT_'+name,all(jp.T.row_join(covector.subs(alpha,c)).rank()==11 for c in alphas))
    check('SHARP_ALL_COEFFICIENT_OPERATOR_GAP',sp.expand(defects['plus']-defects['minus'])==sp.Rational(1,2)
          and max(abs(v.subs(alpha,0)) for v in defects.values())==sp.Rational(1,4))
    check('SHARP_NORMALIZED_OWNED_ACTION_GAP',sp.expand(action_defects['plus']-action_defects['minus'])==sp.Rational(1,4)
          and max(abs(v.subs(alpha,0)) for v in action_defects.values())==sp.Rational(1,8))
    check('COEFFICIENT_INDEPENDENT_VERTICAL_DEFECT',sp.expand(verticals['plus']-verticals['minus'])==sp.Rational(3,2))
    for L in (4,8,12):
        # The generic compiled scalar eigenvector supplies the all-stage identity.
        energies={k:L**4*v for k,v in action_defects.items()}
        check('NORMALIZED_CONSTANT_FIELD_ALL_SITES_'+str(L),all(sp.expand(energies[k]/L**4-action_defects[k])==0 for k in energies))
    # The rays cover all reals: choose a=1-s on s<=0 or a=1+s on s>=0.
    check('NEGATIVE_RAY_INVERSE',sp.simplify((1-a).subs(a,1-s)-s)==0)
    check('POSITIVE_RAY_INVERSE',sp.simplify((a-1).subs(a,1+s)-s)==0)
    Ed=sp.diag(0,-delta,0,0)
    near=sp.factor(p(sp.trace((eta+Ed)*B-eta))-p(sp.trace(Ed)))
    check('ARBITRARILY_NEAR_FLAT_DEFECT',sp.expand(near-(a-1)*delta*(-1+alpha*delta*(a+1)))==0)
    check('OWNED_POSITIVE_POLYNOMIAL_SQUARE',sp.simplify(p(s)-(alpha*(s+1/(2*alpha))**2+1-1/(4*alpha)))==0)
    check('FIELD_ONLY_ROOT_NOT_JOINT_GATE',p(-1).subs(alpha,0)==0 and sp.diff(p(s),s).subs({s:-1,alpha:0})!=0)
    # Passing a few probes is not the quantified scalar-descent theorem.
    cubic=1+s-16*s**3
    check('TWO_PROBES_INSUFFICIENT_FOR_GENERAL_NONLINEAR_FUNCTION',cubic.subs(s,sp.Rational(1,4))==1
          and cubic.subs(s,-sp.Rational(1,4))==1 and sp.diff(cubic,s).subs(s,0)==1
          and cubic.subs(s,sp.Rational(1,8))!=1)
    ext=sp.zeros(16)
    for i,S in enumerate(sectors):
        rows=[r for r in range(4) if S[r]]
        for j,Tset in enumerate(sectors):
            cols=[r for r in range(4) if Tset[r]]
            if len(rows)==len(cols):ext[i,j]=fixed.extract(rows,cols).det() if rows else 1
    check('ACTUAL_EXTERIOR_SCALAR_FIXED',ext*vacuum==vacuum and ext.T*vacuum==vacuum)
    oneform=sp.zeros(16,1);oneform[1]=1
    check('CONSTANT_SPECTRAL_READOUT_NOT_FULL_COUNTING_ACTION_COVARIANCE',(ext*oneform).dot(ext*oneform)-oneform.dot(oneform)==sp.Rational(9,8))
    hscale=sp.symbols('hscale',positive=True)
    collapsing=1+hscale*sp.sin(s/hscale)
    check('FIXED_FIRST_JET_DOES_NOT_PREVENT_SPECTRAL_COLLAPSE',collapsing.subs(s,0)==1 and sp.diff(collapsing,s).subs(s,0)==1
          and sp.simplify((collapsing-1).subs(s,sp.pi*hscale/2))==hscale)
    # A fixed smooth curved conformal background: rho=1+cos(2*pi*x_C)/10.
    # The scalar block is m=2+sum_r theta_rr A_r rho; H is self-adjoint.
    # Thus the owned normalized energy is (1+mean(m)+alpha*mean(m*m))/2.
    kappa=sp.Rational(1,10);d=sp.Rational(1,4);qcos=sp.symbols('qcos',real=True)
    mean_square=1+kappa*kappa/2
    mean_average_product=1+kappa*kappa*(1+qcos)/4
    mr_minus=2-sp.Rational(3,2)*mean_square-sp.Rational(1,2)*mean_average_product
    mr_plus=2-sp.Rational(1,2)*mean_square-sp.Rational(3,2)*mean_average_product
    bm=sp.expand(-2*d*mr_minus+d*d*mean_square)
    bp=sp.expand(2*d*mr_plus+d*d*mean_square)
    check('CURVED_ALL_SIZE_QUADRATIC_COEFFICIENTS',bm==(215+2*qcos)/3200 and bp==(191-6*qcos)/3200)
    check('CURVED_UNIFORM_POSITIVE_COEFFICIENT_BOUNDS',bm.subs(qcos,-1)==sp.Rational(213,3200)
          and bp.subs(qcos,1)==sp.Rational(37,640) and sp.diff(bm,qcos)>0 and sp.diff(bp,qcos)<0)
    for L in (4,8,12,16):
        rho=[1+kappa*sp.cos(2*sp.pi*j/L) for j in range(L)]
        avg=[(rho[j]+rho[(j-1)%L])/2 for j in range(L)]
        mean=lambda seq:sp.simplify(sum(seq)/L)
        check('CURVED_EXACT_SAMPLING_MOMENTS_'+str(L),mean(rho)==1 and mean([z*z for z in rho])==mean_square
              and sp.simplify(mean([rho[j]*avg[j] for j in range(L)])-mean_average_product.subs(qcos,sp.cos(2*sp.pi/L)))==0)
        for name in ('minus','plus'):
            sign=-1 if name=='minus' else 1
            m=[2-sp.Rational(3,2)*rho[j]-sp.Rational(1,2)*avg[j] if name=='minus'
               else 2-sp.Rational(1,2)*rho[j]-sp.Rational(3,2)*avg[j] for j in range(L)]
            mp=[m[j]+sign*d*rho[j] for j in range(L)]
            de=sp.expand(mean([mp[j]-m[j] for j in range(L)])/2+
                         alpha*mean([mp[j]**2-m[j]**2 for j in range(L)])/2)
            bc=bm if name=='minus' else bp
            difference=sp.Poly(sp.expand(de-sign*d/2-alpha*bc.subs(qcos,sp.cos(2*sp.pi/L))/2),alpha)
            # Exact algebraic-number reduction handles nested L=16 radicals;
            # no floating-point tolerance or numerical equality fallback.
            check('CURVED_LITERAL_ACTION_DEFECT_'+name+'_'+str(L),all(
                sp.polys.numberfields.to_number_field(coef).as_expr()==0
                for coef in difference.all_coeffs()))
    # Independent full Levi-Civita computation, used only to certify curvature.
    x=sp.symbols('x',real=True);rho=sp.Function('rho')(x)
    der=lambda expr,j:sp.diff(expr,x) if j==2 else 0
    curvatures={}
    for name,th in thetas.items():
        g0=th*eta*th.T;g=rho*rho*g0;inv=g.inv()
        gamma=[[[sp.simplify(sum(inv[k,l]*(der(g[l,j],i)+der(g[l,i],j)-der(g[i,j],l))/2 for l in range(4))) for j in range(4)] for i in range(4)] for k in range(4)]
        ricci=sp.Matrix(4,4,lambda i,j:sp.simplify(sum(der(gamma[k][i][j],k)-der(gamma[k][i][k],j)
            +sum(gamma[k][k][l]*gamma[l][i][j]-gamma[k][j][l]*gamma[l][i][k] for l in range(4)) for k in range(4))))
        scalar=sp.simplify(sum(inv[i,j]*ricci[i,j] for i in range(4) for j in range(4)))
        check('CURVED_ALL_64_CHRISTOFFEL_AND_16_RICCI_'+name,sp.simplify(scalar+6*sp.diff(rho,x,2)/(g0[2,2]*rho**3))==0)
        value=sp.simplify(scalar.subs({rho:sp.Rational(11,10),sp.diff(rho,x):0,sp.diff(rho,x,2):-2*sp.pi**2/5}))
        check('GENUINELY_CURVED_BACKGROUND_'+name,value!=0 and g0.det()<0)
        curvatures[name]=str(value)
    payload={'status':'PASS','scope':'Necessary scalar frame descent for spectral functions of the literal flux operator; owned kernelPoly/squaredFluxEnergy candidate binding only, no new native action or physical gate.',
        'input_head':INPUT_HEAD,'inputs_sha256':{p:sha(p) for p in INPUTS},'checks':checks,
        'rays':rays,'operator_defects':{k:str(v) for k,v in defects.items()},'normalized_action_defects':{k:str(sp.expand(v)) for k,v in action_defects.items()},
        'sharp_operator_gap':'1/4','sharp_normalized_action_gap':'1/8','curved_operator_quadratic_coefficients':{'minus':str(bm),'plus':str(bp)},'curved_scalar_curvatures_at_zero':curvatures,'vertical_defects':{k:str(v) for k,v in verticals.items()},
        'protected_exception':'The admitted class must include the two full frame orbits and the scalar sector with its actual exterior lift. Constant scalar functions pass only this necessary test; different readouts, pairings or restricted sectors require separate owners.'}
    out=json.dumps(payload,sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(out)
    else:
        ledger=args.expect or Path(__file__).with_name('a4d_native_spectral_frame_certificate.json')
        assert ledger.read_text()==out,'PINNED_LEDGER_MISMATCH'
        print('PASS_IMMUTABLE_PINNED_LEDGER')
    print('PASS_NATIVE_SPECTRAL_FRAME',len(checks))

if __name__=='__main__':main()
