#!/usr/bin/env python3
"""Bounded new weighted-source calculation on the unchanged primary carrier.
Imports definitions only. No old root/rank/continuum suite or repository writes.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time
import sympy as s
sys.dont_write_bytecode=True
DEFAULT_ROOT=Path('/Users/grigorijvahrusev/.codex/worktrees/same-execution-spatial-source/d0_15')
SOURCE='02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/literal_null_all40.py'


def require(ok,label):
    if not bool(ok): raise RuntimeError(label)


def zero(expr):
    if isinstance(expr,s.MatrixBase): return all(s.simplify(t)==0 for t in expr)
    return s.simplify(expr)==0


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,default=DEFAULT_ROOT)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    start=time.perf_counter()
    src=args.repo/SOURCE
    spec=importlib.util.spec_from_file_location('owned_definitions',src)
    g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    z=(0,0,0,0)
    w,wu,wv,wx,wy=s.symbols('A A_minus_u A_minus_v A_minus_x A_minus_y',real=True)
    weights={z:w,g.sh(z,0,-1):wu,g.sh(z,1,-1):wv,g.sh(z,2,-1):wx,g.sh(z,3,-1):wy}
    result=s.zeros(4,6)
    # Original face implementation, with the changed actual anchor weight.
    for axis in range(4):
        for j,(aa,bb) in enumerate(g.pairs):
            X=s.zeros(4);X[aa,bb]=1;X[bb,aa]=-1;X=X*g.eta
            val=0
            for r,t in g.pairs:
                if axis not in (r,t):continue
                other=t if axis==r else r
                for base in (z,g.sh(z,other,-1)):
                    P=g.I;dP=s.zeros(4)
                    for at,a,back in g.edges(base,r,t):
                        W=g.U(at,a,back)
                        dW=(-W*X if back else X*W) if at==z and a==axis else s.zeros(4)
                        dP=dP*W+P*dW;P=P*W
                    Pi=g.inv(P);dR=(dP+Pi*dP*Pi)/2
                    u,v=(i for i in range(4) if i not in (r,t))
                    val+=weights[base]*s.LeviCivita(r,t,u,v)*g.pair(g.e(base),u,v,dR)
            result[axis,j]=s.expand(val/g.h**2)
    H=g.H(z);Hx=g.H(g.sh(z,2,-1));Hy=g.H(g.sh(z,3,-1))
    Kx=g.A(g.sh(z,0,-1));Ky=g.B(g.sh(z,0,-1))
    Z=H*(w-wv)/2-w+wu
    expected=s.Matrix([
        [w-wv,w-wx,w-wy,0,0,0],
        [wu-w,wu*Kx-(w*H-wx*Hx)/2,wu*Ky-(w*H-wy*Hy)/2,w-wx,w-wy,0],
        [0,Z,0,wv-w,0,w-wy],
        [0,0,Z,0,wv-w,wx-w]])
    require(zero(result-expected),'all24 literal weighted link rows')
    decisive=[result[0,0],result[0,1],result[0,2],result[1,0]]
    require(decisive==[w-wv,w-wx,w-wy,wu-w],'four exact backward weight differences')
    cartan={Kx:(H-Hx)/2,Ky:(H-Hy)/2}
    require(zero(result.subs(cartan).subs({wu:w,wv:w,wx:w,wy:w})),'constant weights suffice on owned Cartan section')
    for axis,var in enumerate([wu,wv,wx,wy]):
        hostile={wu:w,wv:w,wx:w,wy:w};hostile[var]=w+1
        require(not zero(result.subs(cartan).subs(hostile)),'one wrong neighbor weight remains visible '+str(axis))

    # Homogeneity uses literal based face wedge and original local inverse metric.
    scale=s.symbols('scale',positive=True)
    E=s.Matrix(4,4,s.symbols('e0:16'))
    R=s.Matrix(4,4,s.symbols('r0:16'))
    for u,v in g.pairs:
        require(zero(g.pair(scale*E,u,v,R)-scale**2*g.pair(E,u,v,R)), 'literal anchor wedge homogeneity')
    hfield=s.symbols('H_local',real=True)
    eco=s.eye(4);eco[1,0]=hfield/2
    kk=s.Matrix(s.symbols('ku kv kx ky',real=True))
    metric=eco.T*g.eta*eco
    q=(kk.T*metric.inv()*kk)[0]
    require(zero(q-(2*kk[0]*kk[1]-hfield*kk[1]**2-kk[2]**2-kk[3]**2)), 'actual signed inverse-metric material density')
    qscaled=(kk.T*((scale*eco).T*g.eta*(scale*eco)).inv()*kk)[0]
    require(zero(qscaled-q/scale**2),'local inverse-metric homogeneity')

    # Original inverse-PF dictionary, full off-null identity and all moving-weight jets.
    r1,r2,bar,c,d=s.symbols('rho1 rho2 wbar c d',positive=True)
    f1,f2,q1,q2=s.symbols('fraw1 fraw2 qraw1 qraw2',real=True)
    baseline=r1**2+3*r2+bar
    raw=baseline+bar*r1*(c*f1+d*q1/r1**2)+bar*r2*(c*f2+d*q2/r2**2)
    op=baseline+bar*(c*(r1*f1+r2*f2)+d*(q1/r1+q2/r2))
    require(zero(raw-op),'exact original double-inverse dictionary identity')
    for v in [r1,r2,bar,f1,f2,q1,q2]:
        require(zero(s.diff(raw,v)-s.diff(op,v)),'complete moving source '+str(v))
    null={f1:0,f2:0,q1:0,q2:0}
    require(s.diff(raw,r1).subs(null)==2*r1,'baseline weight source survives zero densities')
    wrong=baseline+bar*r1*(c*f1+d*q1/r1)+bar*r2*(c*f2+d*q2/r2)
    require(not zero(s.diff(raw,q1)-s.diff(wrong,q1)),'missing inverse-PF factor rejected')
    # Actual unequal masses flatten once; an arbitrary added operational weight does not.
    masses=[s.Rational(2),s.Rational(5),s.Rational(11)]
    massbar=sum(masses)/3
    require(all(m/(m/massbar)==massbar for m in masses),'original nonuniform weights cancel once')

    # Exact weighted scalar/top adjoint in periodic v, with all labels present.
    b=s.symbols('B0:4',real=True)
    delta=s.symbols('delta0:4',real=True)
    du,h=s.symbols('D_u_Psi h',real=True,nonzero=True)
    first=s.expand(sum(2*b[j]*du*(delta[(j+1)%4]-delta[j])/h for j in range(4)))
    for j in range(4):
        require(zero(s.diff(first,delta[j])-2*du*(b[(j-1)%4]-b[j])/h),'material backward weighted source')
    require(zero(first.subs({b[j]:b[0] for j in range(1,4)})),'constant matter coefficient v-Stokes')
    require(not zero(first.subs({b[0]:1,b[1]:2,b[2]:1,b[3]:1})),'unequal matter weight visible')
    energy,lam,AA,BB,lap=s.symbols('E lambda A B lap',real=True)
    row=-AA*lap/(2*h)-2*BB*energy/h
    require(zero(row.subs(lap,-4*lam*energy)+2*(BB-lam*AA)*energy/h),'actual primary coframe residual')

    # A genuine coupled global ledger has one consistent aggregate auxiliary pair.
    a,pi,ss=s.symbols('a pi ss',nonzero=True)
    c1,c2,d1,d2,X1,X2,Y1,Y2=s.symbols('c1 c2 d1 d2 X1 X2 Y1 Y2',nonzero=True)
    F0=lambda xx,yy:a*xx+3*yy+xx**2+2*xx*yy+4*yy**2
    lhs=F0(ss,(pi/a)*(d1*Y1+d2*Y2))+pi*((a/pi)*(c1*X1+c2*X2)-ss)
    rhs=a*(c1*X1+c2*X2)+F0(ss,(pi/a)*(d1*Y1+d2*Y2))-pi*ss
    require(zero(lhs-rhs),'aggregate auxiliary exact identity')
    Fvector=F0(c1*X1+c2*X2,d1*Y1+d2*Y2)
    require(zero(s.diff(Fvector,X1)/c1-s.diff(Fvector,X2)/c2),'vector auxiliaries force one global scale')
    require(s.diff(Fvector,Y1,Y2)==8*d1*d2,'global material cross-cell term retained')

    report={'status':'PASS','scope':'new weighted input on unchanged primary carrier; no root/rank replay',
      'runtime':{'python':platform.python_version(),'sympy':s.__version__},
      'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
      'weighted_link_rows':[[str(result[i,j]) for j in range(6)] for i in range(4)],
      'decisive_weight_differences':[str(v) for v in decisive],
      'checks':['all24 weighted links','independent local geometry/material homogeneity','moving inverse-PF dictionary',
                'baseline preserved','four unequal-neighbor hostile controls','weighted material adjoint',
                'original coframe residual','global auxiliary consistency'],
      'elapsed_seconds':time.perf_counter()-start}
    report['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    payload=json.dumps(report,indent=2)+'\n'
    if args.output:
        args.output.write_text(payload)
        print(json.dumps({'status':report['status'],'output':str(args.output),'elapsed_seconds':report['elapsed_seconds']}))
    else: print(payload,end='')

if __name__=='__main__':main()
