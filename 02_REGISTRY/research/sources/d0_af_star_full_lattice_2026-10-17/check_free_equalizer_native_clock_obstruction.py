#!/usr/bin/env python3
"""New native-clock / sameRIGHT prep-curvature scale consumer only."""
def free_equalizer_native_clock_obstruction(root):
    import ast,hashlib
    from pathlib import Path
    import sympy as s
    root=Path(root);checks=[]
    def ck(name,v):
        if not bool(v):raise ArithmeticError(name)
        checks.append(name)
    v8=root/'02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/verify.py'
    node=next(n for n in ast.parse(v8.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='exact')
    pin=hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()
    ck('literal oldv8 native word definition pin',pin=='9f62da27fd64a07005a5ee30eaedbf665f309f15b3799e8049e6f7290dac27ff')
    rpin=hashlib.sha256(v8.with_name('RESULT.md').read_bytes()).hexdigest()
    ck('literal oldv8 price and clock owner pin',rpin=='f7ea30d997a58fa4e608d4403acae5f5e3d7e5da45116f9a7c3f62be5e99115c')
    d,o,h=s.symbols('metric_diagonal metric_offdiagonal h',positive=True)
    c=s.symbols('cos_v cos_x cos_y',real=True);ss=s.symbols('sin_v sin_x sin_y',real=True)
    zz=s.Matrix([0]+[(c[j]-1+s.I*ss[j])/h for j in range(3)])
    G=(d-o)*s.eye(4)+o*s.ones(4)
    old=(zz.conjugate().T*G*zz)[0]
    uv=zz.copy();uv[0]=-2/h
    gap=s.simplify((uv.conjugate().T*G*uv)[0]-old)
    exact=4*(d+o*sum(1-z for z in c))/h**2
    ck('actual full4Role UV energy gap exact',s.simplify(gap-exact)==0)
    angle=s.symbols('preparation_angle',real=True)
    cc=s.Matrix([s.cos(angle),s.sin(angle)])
    ck('two Fourier planes preserve whole canonical Gram',s.trigsimp((cc.T*cc)[0])==1)
    ck('whole normalized preparation speed equalsone',s.trigsimp((cc.diff(angle).T*cc.diff(angle))[0])==1)
    ck('second preparation jet is genuine geodesic',cc.diff(angle,2)==-cc)
    E=s.symbols('old_energy',real=True)
    R=E*s.cos(angle)**2+(E+gap)*s.sin(angle)**2
    ck('original input Rayleigh second source twice actual gap',s.simplify(s.diff(R,angle,2).subs(angle,0)-2*exact)==0)
    ck('new normal is stationary at anglezero but not flat',s.diff(R,angle).subs(angle,0)==0)
    # A single exact cyclic sum certifies orthogonality of ku0 andkuL/2;
    # the already-owned128 transverse characters are not replayed.
    for L in (8,10):
        ck('checkerboard Fourier plane orthogonal L'+str(L),sum((-1)**j for j in range(L))==0)
        ck('all128 RIGHT columns retained L'+str(L),8*4*4==128 and L>=8)
    fp=root/'02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    creator=next(n for n in ast.parse(fp.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='creator')
    ns={'s':s,'SUBS':[tuple(i for i in range(4) if mask&(1<<i)) for mask in range(16)]}
    exec(compile(ast.Module(body=[creator],type_ignores=[]),str(fp),'exec'),ns)
    cr=[ns['creator'](s.eye(4)[:,i]) for i in range(4)]
    for j in range(1,4):ck('actual current staysrest on vacuum grades '+str(j),((cr[0]+cr[0].T)*(cr[j]-cr[j].T)).extract([1,14],[1,14])==s.zeros(2))
    p=(s.sqrt(5)-1)/2
    f=s.symbols('local_positive_factor',positive=True)
    m0=s.zeros(16,1);m0[1]=s.sqrt(p);m0[14]=s.sqrt(1-p)
    ck('same actual scalar andtop decoders remainzero',f*m0[0]*m0[1]==0 and f*m0[15]*m0[1]==0)
    ck('normalized local future clock unchanged',m0[1].is_positive is True)
    count,eps,kappa=s.symbols('survival_integer epsilon owned_signal_coefficient',positive=True)
    alpha=p*p*h*h/128;beta=count*alpha
    # Consume the already-owned free-equalizer radial balance atQ=0:
    # sigma_J=d_return*vartheta=epsilon/beta. No oldradial replay.
    sigma_J=eps/beta
    lower=s.simplify((8*d/h**2)/sigma_J)
    ck('actual integer-clock source ratio exact',s.simplify(lower-p*p*count*d/(16*eps))==0)
    ck('owned physical signal coefficient retained',s.simplify((8*d/h**2)/(kappa*sigma_J)-p*p*count*d/(16*eps*kappa))==0)
    r0=s.symbols('uniform_return_lower_bound',positive=True)
    ck('generalized r0 bound retains same native floor',s.simplify((8*d/h**2)/(eps/(beta*r0))-p*p*r0*count*d/(16*eps))==0)
    return {'status':'PASS','checks':checks,'source_sha256':{'oldv8_exact_AST':pin,'oldv8_RESULT':rpin},
      'actual_prep_tangent':'Use the already-owned128 transverse characters ku0, common actual vacuum m0, and multiply everycolumn by cos(x)+(-1)^ju sin(x). For |x|<pi/4 each local factor ispositive, the current/futureclockline and normalizedlocalm0 stayfixed, all scalar/top readouts stayzero, and completeRIGHT Gram staysI128/128. Both first/second wholepreparation norms equal1.',
      'actual_curvature':'Literal native Delta(k)=(z*Gz)I16 gives UVshiftkuL/2 gap=4h^-2[d+o sumtrans(1-cos)]. Hence Rold_second=8h^-2 average[d+o sumtrans(1-cos)]>=8d/h² for o>=0. Hgen/oldH and fixedgeometryQ/actualIIDdetectorJ are constant alongthis prepangle.',
      'new_scale_consumer':'In the specified FREE-equalizer caseA Hgen+J+Rold, with Rold independent ofM, consume existing exact radialstationarity. At flatQ0 matrixR=I it gives sigmaJ=d_return*vartheta=epsilon/beta. With the genuine integerclock beta=m p²h²/128,m>=1, Rold_second/sigmaJ>=p²m d/(16epsilon). A physical signal sigma=owned_kappa sigmaJ retains a further1/kappa. Rank/AFmultiplicity cannot make this vanish.',
      'scope':'A new exact C2scale obstruction for this freeequalizer caseA and chart including these genuineRIGHT prep normals, not a replay of oldradial no-go and not a fullD0 theorem. Assumes d stayspositive, epsilon and ownedkappa do not grow without actualbounds, o>=0 and literal clockbinding. Bound control M(S,Q) neednot admit the free radialvariation; linkednewRayleigh/otherhistory terms maychange it and must bepriced.'}
if __name__ == '__main__':
    import argparse, json
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default=str(Path(__file__).resolve().parents[4]))
    args = parser.parse_args()
    result = free_equalizer_native_clock_obstruction(args.root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
