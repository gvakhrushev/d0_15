#!/usr/bin/env python3
"""Exact finite representation consumer, no lattice or root replay."""
import argparse
import ast
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s


def scalar_link_basis():
    """Four invariant families; each family has four literal4x4 edge jets."""
    boosts={}
    for i in range(1,4):
        O=s.zeros(4);O[0,i]=O[i,0]=1;boosts[i]=O
    families=[[s.zeros(4) for _ in range(4)] for _ in range(4)]
    families[0][0]=sum(boosts.values(),s.zeros(4))
    for i in range(1,4):
        families[1][i]=boosts[i]
        families[2][i]=sum((boosts[j] for j in range(1,4) if j!=i),s.zeros(4))
        for j in range(1,4):
            if j!=i:
                families[3][i][i,j]+=1
                families[3][i][j,i]-=1
    return tuple(tuple(family) for family in families)


def quotient(root):
    root=Path(root).resolve()
    path='02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
    node=next(n for n in ast.parse((root/path).read_text()).body
              if isinstance(n,ast.FunctionDef) and n.name=='creator')
    pin=hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()
    assert pin=='801b33d7ef3e41f6425be16153c82b1402215f6be757ea275ff06a69010f58e4'
    ns={'s':s,'SUBS':[tuple(i for i in range(4) if mask&(1<<i)) for mask in range(16)]}
    exec(compile(ast.Module(body=[node],type_ignores=[]),path,'exec'),ns)
    C=[ns['creator'](s.eye(4)[:,i]) for i in range(4)]
    gamma=lambda O:sum((O[i,j]*C[i]*C[j].T for i in range(4) for j in range(4)),s.zeros(16))
    generators=[]
    for i in range(1,4):
        O=s.zeros(4);O[0,i]=O[i,0]=1;generators.append(O)
    for i,j in [(1,2),(1,3),(2,3)]:
        O=s.zeros(4);O[i,j]=1;O[j,i]=-1;generators.append(O)
    labels=['B01','B02','B03','R12','R13','R23']
    u=s.Matrix(s.symbols('u0:4'))
    Cu=ns['creator'](u)
    for j,O in enumerate(generators):
        g=gamma(O)
        assert g.T==(g if j<3 else -g)
        assert g*Cu-Cu*g==ns['creator'](O*u)
    def coefficients(O):
        return s.Matrix([O[0,1],O[0,2],O[0,3],O[1,2],O[1,3],O[2,3]])
    reps=[];signs=[]
    for perm in itertools.permutations([1,2,3]):
        pi=[0]+list(perm)
        P=s.zeros(4)
        for j in range(4):P[pi[j],j]=1
        T=s.zeros(24)
        for leg in range(4):
            for j,O in enumerate(generators):
                coeff=coefficients(P*O*P.T)
                T[6*pi[leg]:6*pi[leg]+6,6*leg+j]=coeff
        assert T.T*T==s.eye(24)
        assert s.trace(T)==(24 if pi==[0,1,2,3] else 0)
        reps.append(T);signs.append(s.det(P))
    P0=sum(reps,s.zeros(24))/6
    Psign=sum((sign*T for sign,T in zip(signs,reps)),s.zeros(24))/6
    Pstd=s.eye(24)-P0-Psign
    assert [P.rank() for P in [P0,Psign,Pstd]]==[4,4,16]
    assert all(P*P==P for P in [P0,Psign,Pstd])
    # Literal invariant four-dimensional link normal basis.
    L=s.zeros(24,4)
    for j,family in enumerate(scalar_link_basis()):
        for leg,O in enumerate(family):
            L[6*leg:6*leg+6,j]=coefficients(O)
    assert L.rank()==4 and P0*L==L
    assert all(T*L==L for T in reps)
    assert L.T*L==s.diag(3,3,6,6)
    # A q with exactly two equal spatial components retains only this S2.
    swap=reps[1]  # permutation (1,3,2), i.e. exchange spatial roles2,3.
    assert swap*swap==s.eye(24) and s.trace(swap)==0
    assert (s.eye(24)+swap).rank()==12 and (s.eye(24)-swap).rank()==12
    # Whitening at n=e0: deltaL=-boost; true Lorentz gauge has
    # delta v=(rotation+boost)v, deltaA=omega_x-omega_y. Thus boost
    # parts cancel in u,M and in the whitened preparation exactly.
    bx,by,rx,ry=s.symbols('bx by rx ry')
    boost=generators[0];rotation=generators[3]
    ax=-bx*boost;ay=-by*boost
    ox=bx*boost+rx*rotation;oy=by*boost+ry*rotation
    assert ax+ox==rx*rotation
    assert ax+ox-oy-ay==(rx-ry)*rotation
    return {
      'status':'PASS','creator_AST_sha256':pin,
      'root':'actual homogeneous full-price root; invertible F=(a-b)I+b11^T,a>b>0,n=e0,A=I;rho=P_Omega tensorI16/128; complete occupied cluster isolated for Riesz prep reduction',
      'Gamma_types':dict(zip(labels,['symmetric']*3+['skew']*3)),
      'raw_joint_gauge':'delta v_r=omega v_r,delta n=omega n,delta A_r(q)=(1-exp(iq_r))omega,deltaPsi=Gamma(omega)Psi',
      'whitened_joint_gauge':'omega=R+B,deltaL=-B:delta u=R u,deltaM_r=(1-exp(iq_r))R,delta w=Gamma(R)w',
      'pure_link_gauge_at_fixed_fullcoframe':'none, since omega U=0 and U invertible imply omega=0',
      'joint_kernel':'contains six complex Lorentz directions per paired nonzero Fourier q before gauge fixing; additional kernels not excluded; no forced pure-link Hessian kernel',
      'coframe_gauge_quotient':'Xi=deltaV V^-1,omegaV=(Xi-eta Xi^T eta)/2;Nnormal_r=Nr-(1-exp(iq_r))omegaV;remaining metric10+observer3+normalLinks24',
      'axial_gauge_alternative':'ifd_j=1-exp(iq_j)!=0, setlinkj0 byomega=Nj/d_j;remaininglinks18 but coframe,observer,prep allshift;not fixedcoframe reduction',
      'puretime_q_stabilizer':'spatialS3; combined internal and role permutations preserve actual root and spectral price',
      'link_representation':'4 trivial +4 sign +8 standard; exact characters(24,0,0)',
      'H_link_block_sizes':'4x4 trivial,4x4 sign,8x8 standard multiplicity tensorI2 after orthonormalization',
      'scalar_source_consumer':'for S3-invariant coframe perturbation atq=(q0,0,0,0), only4x4 trivial link block couples; no invertibility claim',
      'trivial_link_basis':[
        'Omega0=B01+B02+B03, spatial legs0',
        'Omegai=B0i,i1..3;Omega0=0',
        'Omegai=sum(j!=i)B0j,i1..3;Omega0=0',
        'Omegai=sum(j!=i)Rij,i1..3;Omega0=0'],
      'trivial_basis_Gram':'diag(3,3,6,6) in sum_r sum_generators coefficient^2; divide columns bysqrt(3),sqrt(3),sqrt(6),sqrt(6) toorthonormalize',
      'two_equal_spatial_q':'S2 little group gives even12 and odd12; invariant scalar perturbations couple only even block',
      'generic_q':'no nontrivial spatial permutation stabilizer, so no automatic24-to-smaller block',
      'preparation_scope':'fixedRIGHT uniform128 Riesz cluster response, all16CAR retained; unrestricted sphere/common-energy Euler continuation is stronger and not inferred',
      'full_joint_curved_root_claimed':False,'block_nonsingularity_claimed':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--output',type=Path)
    args=p.parse_args();result=quotient(args.root)
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')
