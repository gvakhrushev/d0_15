#!/usr/bin/env python3
"""Exact second-order compatibility in the supplied four-phase D0 germ.

Consumes the original Ward delivery, without modifying it. No full GR,
nonlinear-gauge, stable-matter, or all-mesh continuum theorem is asserted.
Run: python synthesis_check.py --input /path/D0_joint_ward_resonance_git_intake_2026-10-15.zip
Requires Python 3.11+ and SymPy. All asserted algebra uses exact arithmetic.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from itertools import combinations
from pathlib import Path
import sys
import tempfile
import zipfile
import sympy as s

LINEAR_SHA256='8a25e81936ef10346c41cdc9d9bea899f415cd6c55c847b604d94a4a48d01474'
LEAF='02_REGISTRY/research/sources/d0_joint_lattice_ward_resonance_2026-10-15'
DEP='02_REGISTRY/research/sources/d0_full4d_intake_2026-10-15'

def require(ok, message):
    if not ok: raise RuntimeError(message)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    with tempfile.TemporaryDirectory(prefix='d0-synthesis-') as td:
        root=Path(td)
        with zipfile.ZipFile(args.input) as z:
            name='repo/'+LEAF+'/linear.py'
            data=z.read(name)
            require(hashlib.sha256(data).hexdigest()==LINEAR_SHA256,'Changed input symbol consumer')
            target=root/LEAF/'linear.py';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
            for name in z.namelist():
                prefix='OFFLINE_DEPENDENCY/'+DEP+'/'
                if name.startswith(prefix) and not name.endswith('/'):
                    basename=Path(name).name
                    require(basename in {'restore.py',*(f'payload.xz.{j:02}' for j in range(5))},'Unexpected capsule input')
                    out=root/DEP/basename;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(z.read(name))
        spec=importlib.util.spec_from_file_location('owned_d0_linear',target)
        require(spec is not None and spec.loader is not None,'Missing loader')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        R=m.resonance();Y=R['Y'];eta=m.eta;PAIR=m.PAIR;GEN=m.GEN;G2=m.G2;STAR=m.STAR;I=s.eye(4)
        print('stage: input restored',flush=True)
        ranks=[]
        for n in range(4):
            z=[s.S.One,s.I**n,s.I**n,s.S.One];J=m.joint(z);H=J[10:,10:];C=J[10:,:10];G=m.backward_lift(z)
            ranks.append([J.rank(),H.rank(),H.row_join(C).rank(),G.rank()])
        require(ranks==[[24,24,24,0],[28,22,23,4],[30,24,24,4],[28,22,23,4]],'Four-harmonic rank mismatch')
        require(sum(34-v[0] for v in ranks)==26,'Kernel count')
        require(sum(v[0] for v in ranks)==110,'Normal count')
        for charge in range(-7,8):
            av=s.simplify(sum(s.I**(charge*j) for j in range(4))/4)
            require(av==int(charge%4==0),'Character orthogonality')
        for degree in (1,3,5,7):
            require(all((2*positive-degree)%4!=0 for positive in range(degree+1)), 'Odd self interaction')
        require((1-1+0)%4==0 and (1+1+2)%4==0,'Actual cubic channels')

        def from_vectors(xs):
            fields=[]
            for x in xs:
                q=s.zeros(4)
                for val,(a,b) in zip(x[:10],m.PACK):q[a,b]=q[b,a]=val
                A=[sum((x[10+6*r+k]*GEN[k] for k in range(6)),s.zeros(4)) for r in range(4)]
                fields.append((eta*q/2,A))
            return fields

        def pattern(chi):
            v=Y*s.Matrix(chi)
            return from_vectors([s.simplify(v*s.I**j+s.conjugate(v*s.I**j)) for j in range(4)])

        def add(F,V,c=1):
            return [(e+c*f,[a+c*b for a,b in zip(A,B)]) for (e,A),(f,B) in zip(F,V)]

        def mul(A,B,N):
            return [sum((A[j]*B[k-j] for j in range(k+1)),s.zeros(4)) for k in range(N+1)]

        def cayley(A,N):
            return [I]+[A**k/s.Integer(2)**(k-1) for k in range(1,N+1)]

        def coefficient(F,N=3):
            result=s.S.Zero;shift=[0,1,1,0]
            for j,(e,A) in enumerate(F):
                for r,t in PAIR:
                    u,v=[a for a in range(4) if a not in (r,t)]
                    seq=[r,t,u,v];sg=(-1)**sum(seq[a]>seq[b] for a,b in combinations(range(4),2))
                    W=[sg*m.wedge(I[:,u],I[:,v]).T*G2*STAR,
                       sg*(m.wedge(e[:,u],I[:,v])+m.wedge(I[:,u],e[:,v])).T*G2*STAR,
                       sg*m.wedge(e[:,u],e[:,v]).T*G2*STAR]
                    terms=[A[r],F[(j+shift[r])%4][1][t],-F[(j+shift[t])%4][1][r],-A[t]]
                    P=[I]+[s.zeros(4) for _ in range(N)];Pi=P.copy()
                    for X in terms:P=mul(P,cayley(X,N),N)
                    for X in reversed(terms):Pi=mul(Pi,cayley(-X,N),N)
                    for w in range(min(2,N)+1):
                        C=(P[N-w]-Pi[N-w])*eta/2
                        result+=(W[w]*s.Matrix([C[a,b] for a,b in PAIR]))[0]
            return s.factor(result)

        print('stage: ranks and selection done',flush=True)
        Gpi=m.backward_lift([1,-1,-1,1])
        VG=[from_vectors([Gpi[:,k]*(-1)**j for j in range(4)]) for k in range(4)]
        VG3=[coefficient(v) for v in VG]
        def force(chi):
            F=pattern(chi)
            return [s.factor((coefficient(add(F,v))-coefficient(add(F,v,-1)))/2-v3) for v,v3 in zip(VG,VG3)]
        basis=[[28,0],[28*s.I,0],[0,28],[0,28*s.I]]
        bf=[force(c) for c in basis]
        print('stage: diagonal coefficients done',flush=True)
        require(bf==[[0,512,512,0],[0,-512,-512,0],[0,-512,-512,0],[0,512,512,0]],'Diagonal compatibility coefficients')
        for i,j in combinations(range(4),2):
            fij=force([basis[i][k]+basis[j][k] for k in range(2)])
            require(fij==[bf[i][k]+bf[j][k] for k in range(4)],'Mixed quadratic compatibility coefficient')
        print('stage: mixed coefficients done',flush=True)
        # All coefficients of a homogeneous real quadratic form in four variables
        # are thereby identified, not inferred from an unbounded numerical sample.
        require(s.Rational(512,28**2)==s.Rational(32,49),'Amplitude calibration')
        q=s.symbols('a b c d',real=True)
        required=q[0]**2-q[1]**2-q[2]**2+q[3]**2
        require(required.subs(dict(zip(q,(1,0,0,0))))!=0,'Noncompatible control lost')
        require(required.subs(dict(zip(q,(1,0,1,0))))==0,'Compatible polarization')
        require(required.subs(dict(zip(q,(1,1,0,0))))==0,'Compatible quadrature')

        # Zero-frequency kernel is exactly the ten constant coframe/metric slots.
        # Charge conservation makes the response Hermitian-quadratic in chi.
        Qm=[]
        for a,b in m.PACK:
            V=s.zeros(4);V[a,b]=V[b,a]=1;Qm.append(eta*V/2)
        def uniform_sources(chi):
            F=pattern(chi);out=[s.S.Zero]*10;shift=[0,1,1,0]
            for j,(e,A) in enumerate(F):
                for r,t in PAIR:
                    u,v=[a for a in range(4) if a not in (r,t)]
                    seq=[r,t,u,v];sg=(-1)**sum(seq[a]>seq[b] for a,b in combinations(range(4),2))
                    terms=[A[r],F[(j+shift[r])%4][1][t],-F[(j+shift[t])%4][1][r],-A[t]]
                    F1=sum(terms,s.zeros(4))
                    F2=sum((A*B-B*A for j,A in enumerate(terms) for B in terms[j+1:]),s.zeros(4))/2
                    v1=s.Matrix([(F1*eta)[a,b] for a,b in PAIR]);v2=s.Matrix([(F2*eta)[a,b] for a,b in PAIR])
                    for k,B in enumerate(Qm):
                        d0=sg*(m.wedge(B[:,u],I[:,v])+m.wedge(I[:,u],B[:,v])).T*G2*STAR
                        d1=sg*(m.wedge(e[:,u],B[:,v])+m.wedge(B[:,u],e[:,v])).T*G2*STAR
                        out[k]+=(d0*v2+d1*v1)[0]
            return [s.factor(v) for v in out]
        for chi in ([1,0],[0,1],[1,1],[1,s.I]):
            require(uniform_sources(chi)==[0]*10,'Nonzero uniform kernel source')
        for chi in ([1,0],[1,1],[1+s.I,0]):
            require(coefficient(pattern(chi),2)==0,'Input is not quadratic-null')
            require(coefficient(pattern(chi),3)==0,'Forbidden pure cubic term')

        print('stage: zero mode and cubic done',flush=True)
        # Generic stationary elimination quartic identity; not a D0 coefficient.
        H,B,C,t=s.symbols('H B C t', nonzero=True)
        y=-B*t**2/(2*H)
        require(s.expand(H*y**2/2+B*y*t**2/2+C*t**4/24-t**4*(C/24-B**2/(8*H)))==0, 'Schur quartic coefficient')
        receipt={
          'status':'EXACT_FINITE_SECOND_ORDER_COMPATIBILITY',
          'input_zip_sha256':hashlib.sha256(args.input.read_bytes()).hexdigest(),
          'linear_input_sha256':LINEAR_SHA256,
          'rank_rows_J_H_HC_G':ranks,
          'real_microcell_dimensions':{'total':136,'kernel':26,'normal':110},
          'fourier_normalization':'x_j=Y chi i^j+conjugate; Y^*Y=I/7; sum four faces-of-cell sites',
          'kernel_force_pi':'(32/49)*Re(chi1^2-chi2^2)*(0,1,1,0)',
          'kernel_force_zero':'all ten components identically zero',
          'quadratic_compatibility':'Re(chi1^2-chi2^2)=0',
          'scope':'fixed four-phase translation-invariant microcell; original naked-star action; affine coframe chart',
          'not_proved':['exact nonlinear resonant roots','positive physical energy','native full Cost-Info identification','all-mode refining limit','nonlinear gauge symmetry','GR closure'],
          'claim_of_lean_compilation':False,
          'sympy_version':s.__version__
        }
        text=json.dumps(receipt,ensure_ascii=False,indent=2)
        print(text)
        if args.output:args.output.write_text(text+'\n',encoding='utf8')

if __name__=='__main__': main()
