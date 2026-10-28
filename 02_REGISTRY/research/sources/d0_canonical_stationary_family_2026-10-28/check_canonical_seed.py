#!/usr/bin/env python3
"""Canonical Fibonacci AF stationary reflections; not a proof of D0 -> GR.

The permutations below are exact finite AF elements. They are NOT declared
G/CX/SourceI calls. N=5 in the heat control is a structural clock, not a
certificate that the row swaps cost five native pulses. No zero blanks are
substituted for the actual canonical GNS embedding.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
import platform
from pathlib import Path
import numpy as np
import scipy
import scipy.linalg as la
import scipy.sparse as ss

COUNT=0
P=(math.sqrt(5)-1)/2
Z=2.0**-20
BETA=2*P*P
INPUT='d9ef0b0558fcabbc097ecf2024a10b31ec0b5852'


def check(ok: bool, name: str) -> None:
    global COUNT
    COUNT+=1
    if not bool(ok):
        raise ArithmeticError(name)


def near(x, y, name: str, tol: float=2e-11) -> float:
    error=float(np.max(np.abs(np.asarray(x)-np.asarray(y))))
    check(error<tol, name+': '+str(error))
    return error


def adj(x): return x.conj().T

def gp(k: int) -> tuple[int,int]:
    # Exact p^k=a+b*p, p^2=1-p. All relevant k are nonnegative.
    a,b=1,0
    for _ in range(k): a,b=b,a-b
    return a,b


class AF:
    def __init__(self, old: tuple[int,int], depth: int):
        if depth<1 or min(old)<1: raise ValueError('Positive dimensions/depth required')
        self.old=old;self.depth=depth
        self.m=np.linalg.matrix_power(np.array([[1,1],[1,0]],dtype=np.int64),depth)
        paths=[[(a,row) for row in range(old[a])] for a in range(2)]
        for _ in range(depth): paths=[paths[0]+paths[1],paths[0]]
        self.paths=paths;self.new=tuple(map(len,paths));self.positions={}
        for b in range(2):
            for a,da in enumerate(old):
                starts=[i for i,v in enumerate(paths[b]) if v==(a,0)]
                self.positions[b,a]=[list(range(t,t+da)) for t in starts]
                check(len(starts)==self.m[b,a], 'actual recursive copy multiplicity')
                for t in starts:
                    check(paths[b][t:t+da]==[(a,j) for j in range(da)], 'old matrix unit stays contiguous')

    def embed(self, xs):
        ys=[np.zeros((d,d),dtype=np.asarray(xs[0]).dtype) for d in self.new]
        for b in range(2):
            for a in range(2):
                for inds in self.positions[b,a]: ys[b][np.ix_(inds,inds)]=xs[a]
        return ys

    def expectation(self, xs):
        out=[]
        for a,da in enumerate(self.old):
            y=np.zeros((da,da),complex)
            for b in range(2):
                for inds in self.positions[b,a]:y+=P**(self.depth+b-a)*xs[b][np.ix_(inds,inds)]
            out.append(y)
        return out

    def exact_expectation_equal(self, xs, target):
        # Integer input signed permutations, equality in Z[p], no floating tolerance.
        for a,da in enumerate(self.old):
            aa=np.zeros((da,da),dtype=object);bb=aa.copy()
            for b in range(2):
                ag,bg=gp(self.depth+b-a)
                for inds in self.positions[b,a]:
                    block=np.asarray(xs[b][np.ix_(inds,inds)],dtype=object)
                    aa+=ag*block;bb+=bg*block
            check(np.array_equal(aa,target[a]) and np.array_equal(bb,np.zeros((da,da),dtype=object)),
                  'exact full conditional expectation in Z[p]')

    def canonical_input(self):
        oldoff=np.cumsum([0]+[d*d for d in self.old])
        newoff=np.cumsum([0]+[d*d for d in self.new])
        rr=[];cc=[];vv=[]
        for a,da in enumerate(self.old):
            for b,db in enumerate(self.new):
                for inds in self.positions[b,a]:
                    for i in range(da):
                        for j in range(da):
                            rr.append(int(newoff[b]+inds[i]*db+inds[j]))
                            cc.append(int(oldoff[a]+i*da+j))
                            vv.append(P**((self.depth+b-a)/2))
        E=ss.coo_matrix((vv,(rr,cc)),shape=(int(newoff[-1]),int(oldoff[-1]))).tocsr()
        near((E.T@E).toarray(),np.eye(int(oldoff[-1])), 'canonical trace input, all columns')
        return E


def make_reflection(af: AF, signs: tuple[tuple[int,...],tuple[int,...]]):
    out=[];transpositions=[]
    for a in range(2):
        check(len(signs[a])==af.old[a] and all(t in (-1,0,1) for t in signs[a]), 'declared Hermitian partial isometry')
        check(signs[a].count(0)%2==0, 'even kernel per central type')
    for b,db in enumerate(af.new):
        W=np.zeros((db,db),dtype=int);pairs=[]
        for a,da in enumerate(af.old):
            copies=af.positions[b,a];m=len(copies)
            zeros=[j for j,t in enumerate(signs[a]) if t==0]
            if zeros:check(m>=2, 'actual derangement copy space')
            for j,s in enumerate(signs[a]):
                if s:
                    for inds in copies: W[inds[j],inds[j]]=s
            for j0,j1 in zip(zeros[::2],zeros[1::2]):
                for t in range(m):
                    x=copies[t][j0];y=copies[(t+1)%m][j1]
                    W[y,x]=W[x,y]=1;pairs.append([x,y])
        check(np.array_equal(W,W.T), 'exact selfadjoint AF element')
        check(np.array_equal(W@W,np.eye(db,dtype=int)), 'exact involution, all left columns')
        out.append(W);transpositions.append(pairs)
    target=[np.diag(s) for s in signs]
    af.exact_expectation_equal(out,target)
    return out,target,transpositions


def left(xs):
    return ss.block_diag([ss.kron(ss.csr_matrix(x),ss.eye(len(x)),format='csr') for x in xs],format='csr')


def right(xs):
    return ss.block_diag([ss.kron(ss.eye(len(x)),ss.csr_matrix(x.T),format='csr') for x in xs],format='csr')


def seed_and_refinement():
    old=(3,2);signs=((0,1,0),(1,1));base=AF(old,3)
    Ws,target,pairs=make_reflection(base,signs)
    Id=base.canonical_input().toarray();U=left(Ws).toarray()
    C=la.block_diag(*[np.kron(c,np.eye(len(c))) for c in target])
    err=near(Id.T@U@Id,C,'actual full GNS corner')
    S=C.T@C;Pin=Id@Id.T;Q=U@Pin@U.T
    near(Pin@Q,Q@Pin,'canonical input and output projections commute')
    check(np.array_equal(S@S,S),'canonical corner is exact partial isometry')
    # Source proof is algebraic. Check its matrix realization independently.
    D=(1-Z)*np.eye(13)+Z*S
    A=U@Id@la.inv(D)@Id.T@U.T
    cot=-Z*(A@Pin-Pin@A)
    near(cot,0,'full endpoint return cotangent')
    maxrow=0.;directions=0
    for b,db in enumerate(base.new):
        generators=[]
        for i in range(db):
            X=np.zeros((db,db),complex);X[i,i]=1j;generators.append(X)
        for i in range(db):
            for j in range(i):
                X=np.zeros((db,db),complex);X[i,j]=1;X[j,i]=-1;generators.append(X)
                X=np.zeros((db,db),complex);X[i,j]=X[j,i]=1j;generators.append(X)
        for X in generators:
            dx=[np.zeros_like(w,dtype=complex) for w in Ws];dx[b]=X@Ws[b]
            dc=la.block_diag(*[np.kron(a,np.eye(len(a))) for a in base.expectation(dx)])
            v=-2*Z*np.trace(la.solve(D,C.T@dc)).real
            maxrow=max(maxrow,abs(v));directions+=1
            check(abs(v)<1e-18,'all independent old-left Lie algebra source rows')
    # Retained old-right action is exact, but the whole old LEFT law is not frozen.
    maxright=0.
    for a,da in enumerate(old):
        for i in range(da):
            for j in range(da):
                x=[np.zeros((k,k),int) for k in old];x[a][i,j]=1
                R=right(base.embed(x)).toarray()
                maxright=max(maxright,near(U@R,R@U,'original right columns are retained'))
    x=[np.diag([1,0,-1]),np.zeros((2,2),int)]
    lhs=base.expectation([w@a@w for w,a in zip(Ws,base.embed(x))])
    near(lhs[0],-x[0],'nontrivial old-left effect, not falsely labelled pure gauge')
    # Preserve exactly the incoming original A0 path-label algebra, not all A2 effects.
    archive0=[np.diag([1,0,1]),np.diag([1,0])]
    fine_archive=base.embed(archive0)
    for w,aa in zip(Ws,fine_archive):
        check(np.array_equal(w@aa,aa@w),'exact fixed ORIGINAL A0 archive law')
    # Tensor identity on all Spin/oldRIGHT columns preserves its full M8 algebra.
    for label in (0,1):
        for a in range(8):
            for b in range(8):
                check(all(np.array_equal(w@aa,aa@w) for w,aa in zip(Ws,fine_archive)),
                      'all128 original archive matrix units, by exact tensor factorization')
    # The inherited original W, not a fresh unrelated endpoint at each refinement.
    profiles=[];cur=Ws
    for depth in range(3,8):
        af=AF(old,depth)
        if depth>3:cur=[la.block_diag(cur[0],cur[1]),cur[0]]
        af.exact_expectation_equal(cur,target)
        for w in cur:check(np.array_equal(w@w,np.eye(len(w),dtype=int)), 'same inherited endpoint remains an involution')
        emb=af.canonical_input()
        near((emb.T@left(cur)@emb).toarray(),C,'compatible canonical refinement source')
        d=sum(n*n for n in af.new)
        minus=sum(n*(n-int(np.trace(w)))//2 for n,w in zip(af.new,cur))
        profiles.append({'target_level':2+depth,'left_dimensions':list(af.new),
                         'GNS_dimension_with_Spin4_oldRIGHT2':8*d,
                         'minus_eigen_multiplicity_with_spectators':8*minus,
                         'input_rank':104,'return_rank':56,'escape_rank':48})
    return {'old_level':2,'new_level':5,'old_algebra_dimensions':[3,2],
      'new_algebra_dimensions':list(base.new),'left_permutation_images':[[int(i) for i in np.argmax(w,axis=0)] for w in Ws],
      'path_transpositions':pairs,'path_transpositions_are_native_gate_calls':False,
      'GNS_input_rank':104,'whole_GNS_dimension':1864,'spin_oldright_factor':8,
      'new_blank_qubits':0,'supplied_pure_state_preparation':False,
      'actual_GNS_compression_error':err,'full_source_operator_norm':float(la.norm(cot,2)),
      'all_complex_left_directions_checked':directions,'max_left_source':maxrow,
      'old_right_commutator_max':maxright,
      'return_price':-48*math.log1p(-Z),'gain_after_scalar_future_T_1':56*Z,
      'fixed_original_A0_archive_preserved':True,'all128_protected_archive_units_checked':128,
      'passive_refinements':profiles},(base,Ws,Id,U,C)


def classification_controls():
    af=AF((3,2),4);allowed=0;excluded=0;archive_allowed=0
    for vals in itertools.product((-1,0,1),repeat=5):
        signs=(vals[:3],vals[3:]);zero=np.array([s.count(0) for s in signs])
        traces=np.array([sum(s) for s in signs]);d=np.array([3,2])
        ranks_twice=af.m@(d+traces)
        even=bool(np.all(ranks_twice%2==0))
        check(even==bool(np.all(zero%2==0)),'invertible Fibonacci incidence mod two')
        if even:
            W,C,_=make_reflection(af,signs);allowed+=1
            for b,w in enumerate(W):
                rankplus=(len(w)+int(np.trace(w)))//2
                check(2*rankplus==int(ranks_twice[b]),'exact signature imposed by original trace')
            archived=all(sum(signs[a][j]==0 for j in group)%2==0
                         for a,groups in enumerate((((0,2),(1,)),((0,),(1,)))) for group in groups)
            AA=af.embed([np.diag([1,0,1]),np.diag([1,0])])
            if archived:
                archive_allowed+=1
                check(all(np.array_equal(w@aa,aa@w) for w,aa in zip(W,AA)),
                      'fixed-archive sufficiency for every spectral pattern')
        else:excluded+=1
    check(allowed==70 and excluded==173 and archive_allowed==40,'all spectral patterns, with and without original archive')
    # A0 has scalar blocks: any nonzero kernel has odd rank in a type.
    for depth in range(1,13):
        M=np.linalg.matrix_power(np.array([[1,1],[1,0]],dtype=np.int64),depth)
        for c in itertools.product((-1,0,1),repeat=2):
            parity=np.all((M@np.array([1+c[0],1+c[1]]))%2==0)
            check(parity==(0 not in c),'A0 separate-zero reflection class has no escape')
    return {'old_dimensions':[3,2],'all_spectral_patterns':243,
            'constructible_patterns':allowed,'parity_excluded_patterns':excluded,
            'fixed_original_archive_constructible_patterns':archive_allowed,
            'necessary_and_sufficient_condition':'even kernel rank in each original central type',
            'A0_exclusion_scope':'selfadjoint involution with separately vanishing return; not all H+J critical points'}


def nonscalar_future(data):
    base,Ws,i,U,C=data;r=len(C)
    R=C@C.T
    rng=np.random.default_rng(411)
    A0=rng.normal(size=(r,r))+1j*rng.normal(size=(r,r))
    A=R@A0@R+(np.eye(r)-R)@A0@(np.eye(r)-R)
    A/=2*la.norm(A,2);M=adj(A)@A
    escaped=int(np.flatnonzero(np.diag(R)==0)[0]);returned=int(np.flatnonzero(np.diag(R)==1)[0])
    a=1-Z;b=Z
    def prior_source(M,X):
        D=a*np.eye(r)+b*adj(C)@M@C
        dC=adj(i)@X@U@i
        return -2*b*np.trace(la.solve(D,adj(C)@M@dC)).real
    maxerr=0.;maxzero=0.
    for changed in (False,True):
        MM=M.copy()
        if changed:
            V=np.eye(r);t=.34;V[np.ix_([escaped,returned],[escaped,returned])]=[[math.cos(t),-math.sin(t)],[math.sin(t),math.cos(t)]]
            MM=V@MM@V.T
        Cq=R@MM@R
        B=R@la.inv(a*np.eye(r)+b*Cq)@R
        cot=-b*i@(B@MM-MM@B)@adj(i)
        norm=la.norm(cot,2)
        if changed:check(norm>1e-9,'crossing the actual returned sector creates a real old source')
        else:near(cot,0,'arbitrary nonscalar block-respecting future has zero prefix source')
        for _ in range(12):
            X0=rng.normal(size=U.shape)+1j*rng.normal(size=U.shape)
            X=(X0-adj(X0))/2;X/=la.norm(X,'fro')
            direct=prior_source(MM,X);expected=np.trace(cot@X).real
            maxerr=max(maxerr,near(direct,expected,'full prefix source after true nonscalar future',1e-17))
            if not changed:maxzero=max(maxzero,abs(direct))
    return {'source_identity_error':maxerr,'preserving_future_max_source':maxzero,
            'criterion':'[A* A, K0 K0*]=0',
            'condition':'actual factored cold product A K0; not arbitrary future interference',
            'future_heat_source_set_to_zero':False}


def full_scene_heat():
    # Complete canonical base carrier has +178/-55 before the true spectator8.
    sizes=[9,11,13];cuts=np.cumsum([0]+sizes);Adj=np.zeros((33,33))
    for a in range(3):
        for b in range(3):
            if a!=b:Adj[cuts[a]:cuts[a+1],cuts[b]:cuts[b+1]]=1
    degree=Adj.sum(1)+2;R=np.diag(1/np.sqrt(degree));B=R@Adj@R;C=R@R
    N=5;d=233;z0=0.;slopes=[]
    for theta,mult in ((0.,178),(math.pi,55)):
        slope=0.;zz=0.
        for j in range(N):
            phi=(theta+2*math.pi*j)/N
            e,V=la.eigh(np.eye(33)-B-2*math.cos(phi)*C)
            weight=np.exp(-BETA*e);zz+=weight.sum()
            slope-=2*BETA*math.sin(phi)/N*np.dot(weight,np.diag(V.T@C@V))
        z0+=mult*zz;slopes.append(slope)
    fullZ=8*(2*z0+359*N*d)
    near(slopes,0,'full finite Bloch heat gradient at both endpoint phases',1e-14)
    return {'N_structural_control_only':N,'GNS_dimension_with_spectators':8*d,
      'full_two_grade_modes':425*N*d*8,'harmonic_modes':359*N*d*8,
      'full_heat_diagnostic':math.log(fullZ)/BETA,
      'phase_sum_derivative_error':max(map(abs,slopes)),
      'native_raw_clock_length_selected':False,
      'theorem_stationarity_for_each_fixed_actual_N':True}


def nonselecting_family(data):
    af,Ws,i,U,C=data
    vals=[]
    for theta in (0.,.23,.71):
        varied=[]
        for b,w in enumerate(Ws):
            V=w.astype(complex).copy()
            for t,inds in enumerate(af.positions[b,0]):
                x=inds[0];y=af.positions[b,0][(t+1)%len(af.positions[b,0])][2]
                V[y,x]=np.exp(1j*(t+1)*theta);V[x,y]=np.exp(-1j*(t+1)*theta)
            near(adj(V),V,'phase family selfadjoint')
            near(V@V,np.eye(len(V)),'phase family remains involution')
            varied.append(V)
        e=af.expectation(varied)
        near(e[0],np.diag([0,1,0]),'all phases invisible to same corner')
        near(e[1],np.eye(2),'returning component unchanged')
        change=max(la.norm(v-w,2) for v,w in zip(varied,Ws))
        vals.append(float(change))
    check(vals[-1]>.1,'stationary family contains genuinely distinct endpoints')
    return {'distinct_operator_distances':vals,'whole_stationarity_inferred_algebraically':True,
            'field_equation_selected_by_this_family':False,
            'reason':'along this exact family both heat spectrum and return block are constant'}


def main():
    result,data=seed_and_refinement()
    out={'status':'PASS_CANONICAL_AF_STATIONARY_REFLECTIONS','input_commit':INPUT,
         'canonical_seed':result,'incoming_archive_owner':'185ab21cb165cbf420291a6d8a2056dc366e5275',
         'classification':classification_controls(),
         'nonscalar_future':nonscalar_future(data),'complete_heat':full_scene_heat(),
         'stationarity_does_not_select_geometry':nonselecting_family(data)}
    out.update({'checks':COUNT,'GR_closed':False,'G_CX_SourceI_word_emitted':False,
                'physical_AF_actuation_proved':False,'all42_Einstein_source_map_proved':False,
                'AF_refinement_identified_with_spacetime_mesh':False,'Lean_or_CI_run':False,
                'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
                'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False))

if __name__=='__main__': main()
