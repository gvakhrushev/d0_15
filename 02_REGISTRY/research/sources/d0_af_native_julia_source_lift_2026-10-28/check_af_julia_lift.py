#!/usr/bin/env python3
"""Exact-source transplantation of the owned Hermitian zero-Walsh Julia corner.

Uses the original four-level Fibonacci inclusion, not a supplied blank. This is
an AF-operator construction; no native primitive compiler or physical GR closure
is asserted. Full original fine-record instruments are NOT identified.
"""
from __future__ import annotations
import hashlib, importlib.util, json, math, platform
from pathlib import Path
import numpy as np
import scipy
import scipy.linalg as la
import scipy.sparse as ss
import sympy as sp

p=(math.sqrt(5)-1)/2
kappa=2*p*p
zeta=2**-20
COUNT=0
MAXERR={}

def require(ok, text):
    global COUNT
    COUNT+=1
    if not bool(ok): raise ArithmeticError(text)

def near(a,b,text,tol=3e-11):
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    MAXERR[text]=max(MAXERR.get(text,0.),err)
    require(err<tol,text+': '+str(err))
    return err

def adj(a): return a.conj().T

class Inclusion:
    def __init__(self,old,depth,D=1):
        self.old=tuple(old); self.depth=depth; self.D=D
        paths=[[(a,j) for j in range(d)] for a,d in enumerate(old)]
        for _ in range(depth): paths=[paths[0]+paths[1],paths[0]]
        self.paths=paths;self.new=tuple(map(len,paths)); self.positions={}
        for b in range(2):
            for a,d in enumerate(old):
                starts=[j for j,x in enumerate(paths[b]) if x==(a,0)]
                self.positions[b,a]=[list(range(j,j+d)) for j in starts]
                for j in starts:
                    require(paths[b][j:j+d]==[(a,t) for t in range(d)],'real recursive copy ordering')
    def expanded(self,inds):
        return [r*self.D+t for r in inds for t in range(self.D)]
    def embed(self,blocks):
        out=[np.zeros((d*self.D,d*self.D),complex) for d in self.new]
        for b in range(2):
            for a in range(2):
                for inds in self.positions[b,a]:
                    ix=self.expanded(inds);out[b][np.ix_(ix,ix)]=blocks[a]
        return out
    def expectation(self,blocks):
        out=[np.zeros((d*self.D,d*self.D),complex) for d in self.old]
        for a in range(2):
            for b in range(2):
                for inds in self.positions[b,a]:
                    ix=self.expanded(inds)
                    out[a]+=p**(self.depth+b-a)*blocks[b][np.ix_(ix,ix)]
        return out
    def canonical_input(self):
        D=self.D
        oldoff=np.cumsum([0]+[d*d*D for d in self.old])
        newoff=np.cumsum([0]+[d*d*D for d in self.new])
        rows=[];cols=[];vals=[]
        for b,db in enumerate(self.new):
            for a,da in enumerate(self.old):
                for inds in self.positions[b,a]:
                    for r in range(da):
                        for s in range(da):
                            for t in range(D):
                                rows.append(newoff[b]+(inds[r]*db+inds[s])*D+t)
                                cols.append(oldoff[a]+(r*da+s)*D+t)
                                vals.append(p**((self.depth+b-a)/2))
        out=ss.coo_matrix((vals,(rows,cols)),shape=(newoff[-1],oldoff[-1])).tocsr()
        near((out.conj().T@out).toarray(),np.eye(oldoff[-1]),'actual canonical isometry')
        return out
    def apply_full_left(self,blocks,embedding):
        # Each old RIGHT column is acted on separately but retained in the output.
        arr=embedding.toarray() if ss.issparse(embedding) else np.asarray(embedding)
        pieces=[];off=0;D=self.D
        for db,B in zip(self.new,blocks):
            n=db*db*D
            data=arr[off:off+n].reshape(db,db,D,-1)
            transformed=np.einsum('iakb,kjbr->ijar',B.reshape(db,D,db,D),data,optimize=True)
            # Keep the actual row,right,DATA,input order of the canonical carrier.
            pieces.append(transformed.reshape(n,-1))
            off+=n
        return np.concatenate(pieces,axis=0)


def lift(inc,a_blocks,da_blocks=None):
    require(inc.depth==4,'owned four-level construction only')
    if da_blocks is None:da_blocks=[np.zeros_like(a) for a in a_blocks]
    out=[np.zeros((d*inc.D,d*inc.D),complex) for d in inc.new]
    dout=[np.zeros_like(x) for x in out]
    for a,(A,dA) in enumerate(zip(a_blocks,da_blocks)):
        near(A,adj(A),'Hermitian original row')
        near(dA,adj(dA),'Hermitian row variation')
        require(la.norm(A,2)<=1+1e-12,'original row contraction collar')
        I=np.eye(len(A));H=la.sqrtm(2*I-A@A).astype(complex)
        B=I-A@A; S=A@H
        dB=-(A@dA+dA@A)
        dH=la.solve_sylvester(H,H,dB)
        dS=dA@H+A@dH
        near(B@B+S@S,I,'actual rotation block identity')
        near(B@S,S@B,'rotation blocks commute')
        near(S@la.inv(H),A,'original signed row reconstructs without lost spectral sign')
        for b in range(2):
            copies=inc.positions[b,a]
            for q in range(0,len(copies)-1,2):
                x,y=inc.expanded(copies[q]),inc.expanded(copies[q+1])
                for target,bb,ss0 in ((out[b],B,S),(dout[b],dB,dS)):
                    target[np.ix_(x,x)]=bb;target[np.ix_(y,y)]=bb
                    target[np.ix_(x,y)]=-ss0;target[np.ix_(y,x)]=ss0
            if len(copies)%2:
                inds=inc.expanded(copies[-1]);out[b][np.ix_(inds,inds)]=I
    for U,dU in zip(out,dout):
        near(adj(U)@U,np.eye(len(U)),'full AF lift unitary')
        near(adj(U)@dU+adj(dU)@U,np.zeros_like(U),'full AF lift first jet')
    expected=[np.eye(len(a))-kappa*a@a for a in a_blocks]
    dexpected=[-kappa*(a@da+da@a) for a,da in zip(a_blocks,da_blocks)]
    for a,c,dc,ex,dex in zip(a_blocks,inc.expectation(out),inc.expectation(dout),expected,dexpected):
        near(c,ex,'four-level exact-source identity')
        near(dc,dex,'four-level full first-jet identity')
    max_a=max(la.norm(a,2) for a in a_blocks)
    max_da=max(la.norm(a,2) for a in da_blocks)
    max_dU=max(la.norm(du,2) for du in dout)
    require(max_dU<=(3+math.sqrt(2))*max_da+1e-12,'dimension-free derivative bound')
    return out,dout


def corner(blocks):
    # Representation on old GNS rows/right columns, with optional DATA already in blocks.
    return la.block_diag(*[np.kron(x,np.eye(len(x))) for x in blocks])


def price_source(K,dK,z=zeta):
    D=(1-z)*np.eye(len(K))+z*adj(K)@K
    F=np.eye(len(K))-adj(K)@K
    val=-np.log1p(-z*la.eigvalsh((F+adj(F))/2)).sum()
    src=-2*z*np.trace(la.solve(D,adj(K)@dK)).real
    return float(val),float(src)


def algebraic_identities():
    P=(sp.sqrt(5)-1)/2
    F=sp.Matrix([[1,1],[1,0]])**4
    require(F==sp.Matrix([[5,3],[3,2]]),'actual Fibonacci four-step multiplicities')
    for a in range(2):
        single=sum(P**(4+b-a)*(int(F[b,a])%2) for b in range(2))
        paired=sum(P**(4+b-a)*(int(F[b,a])-int(F[b,a])%2) for b in range(2))
        require(sp.simplify(single-P**3)==0,'exact unmatched mass p cubed')
        require(sp.simplify(paired-2*P**2)==0,'exact pair mass original Julia kappa')
        x=sp.symbols('x',real=True)
        require(sp.simplify(single+paired*(1-x*x)-(1-2*P**2*x*x))==0,'owned corner recovered, not fitted')
    return {'multiplicities':[[5,3],[3,2]],'unmatched_weight':'p^3',
            'paired_weight':'2*p^2','new_pure_flags':0,
            'identity':'E_4(V(a))=I-2*p^2*a^2 for the same Hermitian original a'}


def load_parent():
    parent=Path(__file__).resolve().parents[1]/'d0_original_retained_history_source_2026-10-28'/'check_history_source.py'
    if not parent.exists():raise FileNotFoundError('Supply the pinned sibling original-history checker: '+str(parent))
    digest=hashlib.sha256(parent.read_bytes()).hexdigest()
    require(digest=='a05b9295a116543c037eb668651195449bb5d7b9b061c70eb73c4a045238253a','pinned original constructor hash')
    spec=importlib.util.spec_from_file_location('owned_history',parent)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod,digest


def original_two_tick():
    parent,digest=load_parent()
    one=parent.rows(1/9,3/5,dr=1,full=True)
    two=parent.rows(1/8,1/2,dr=-.7,dnu=.2,full=True)
    require(la.norm(one['a']@two['a']-two['a']@one['a'])>1e-7,'genuine noncommuting original rows')
    old=(1,1);D=16
    inc1=Inclusion(old,4,D)
    W1,dW1=lift(inc1,[one['a'],one['a']],[one['da'],one['da']])
    inc2=Inclusion(inc1.new,4,D)
    a2=[np.kron(np.eye(d),two['a']) for d in inc1.new]
    da2=[np.kron(np.eye(d),two['da']) for d in inc1.new]
    W2,dW2=lift(inc2,a2,da2)
    W1i=inc2.embed(W1);dW1i=inc2.embed(dW1)
    W=[b@a for a,b in zip(W1i,W2)]
    dW=[db@a+b@da for a,da,b,db in zip(W1i,dW1i,W2,dW2)]
    K=two['C']@one['C'];dK=two['dC']@one['C']+two['C']@one['dC']
    inc=Inclusion(old,8,D)
    for q,dq in zip(inc.expectation(W),inc.expectation(dW)):
        near(q,K,'ordered noncommuting original history corner')
        near(dq,dK,'ordered noncommuting original history source')
    # Direct complete GNS input-output evaluation, not only conditional traces.
    emb=inc.canonical_input()
    Y=inc.apply_full_left(W,emb);dY=inc.apply_full_left(dW,emb)
    near(adj(Y)@Y,np.eye(32),'all 32 canonical input columns retained')
    near(adj(Y)@dY+adj(dY)@Y,np.zeros((32,32)),'all-column derivative isometry')
    C=emb.conj().T@Y;dC=emb.conj().T@dY
    expected=la.block_diag(K,K);dexpected=la.block_diag(dK,dK)
    near(C,expected,'direct GNS compression, no corner-product assumption')
    near(dC,dexpected,'direct GNS complete source')
    v,g=price_source(C,dC);v0,g0=price_source(K,dK)
    near(v,2*v0,'full ordinary trace multiplicity not trace normalization')
    near(g,2*g0,'same full return covector with true multiplicity')
    # Independently contract all original fine histories.
    H=np.einsum('bij,ajk->abik',two['kraus'],one['kraus']).reshape(128**2,16,16)
    dH=(np.einsum('bij,ajk->abik',two['dkraus'],one['kraus'])+
        np.einsum('bij,ajk->abik',two['kraus'],one['dkraus'])).reshape(H.shape)
    oldF=np.einsum('kji,kjl->il',H[1:].conj(),H[1:])
    olddF=np.einsum('kji,kjl->il',dH[1:].conj(),H[1:])+np.einsum('kji,kjl->il',H[1:].conj(),dH[1:])
    near(oldF,np.eye(16)-adj(K)@K,'all 16384 parent records original defect')
    near(olddF,-adj(dK)@K-adj(K)@dK,'all 16384 parent record source')
    other_price=-np.log1p(-zeta*la.eigvalsh(oldF)).sum()
    other_source=zeta*np.trace(la.solve(np.eye(16)-zeta*oldF,olddF)).real
    near(v,2*other_price,'complete original tape/AF price equality')
    near(g,2*other_source,'complete original tape/AF source equality')
    return {'old_AF_level':0,'new_AF_level':8,'old_DATA_dimension':16,
            'fine_left_dimensions':list(inc.new),'GNS_times_DATA_dimension':int(emb.shape[0]),
            'canonical_input_columns':32,'full_source':g,'per_old_copy_original_source':g0,
            'old_multiplicity':2,'original_fine_histories_checked':128**2,
            'native_constructor_sha256':digest,'parent_constructor_checks':parent.COUNT,
            'full_fine_instrument_equivalence_claimed':False}


def canonical_seed_composition():
    inc0=Inclusion((3,2),3)
    W0=[np.eye(13),np.eye(8)]
    for b,pairs in enumerate(([(0,7),(5,10),(8,2)],[(0,7),(5,2)])):
        for i,j in pairs:W0[b][i,i]=W0[b][j,j]=0;W0[b][i,j]=W0[b][j,i]=1
    Q=[np.diag([0.,1.,0.]),np.eye(2)]
    for got,q in zip(inc0.expectation(W0),Q):near(got,q,'same canonical archive-stationary seed')
    a=[np.array([[.21,0,.06],[0,.31,0],[.06,0,-.27]]),np.diag([.19,.37])]
    da=[np.array([[.03,0,-.02],[0,.08,0],[-.02,0,.01]]),np.diag([.04,-.07])]
    inc1=Inclusion(inc0.new,4)
    V,dV=lift(inc1,inc0.embed(a),inc0.embed(da))
    W0i=inc1.embed(W0)
    U=[v@w for v,w in zip(V,W0i)]
    dU=[dv@w for dv,w in zip(dV,W0i)]
    whole=Inclusion((3,2),7)
    R=[np.eye(len(x))-kappa*x@x for x in a]
    dR=[-kappa*(x@dx+dx@x) for x,dx in zip(a,da)]
    C=whole.expectation(U);dC=whole.expectation(dU)
    for c,dc,r,dr,q in zip(C,dC,R,dR,Q):
        near(c,r@q,'seed/future actual total-corner formula')
        near(dc,dr@q,'seed/future actual source pullback')
        near(r@q,q@r,'true archive sector effect commutes with seed return')
    fullC=corner(C);fulldC=corner(dC);value,src=price_source(fullC,fulldC)
    # All actual canonical inputs: 13 columns, retained regular-right multiplicities.
    emb=whole.canonical_input();Y=whole.apply_full_left(U,emb)
    near(emb.conj().T@Y,fullC,'direct seed+future GNS compression')
    near(adj(Y)@Y,np.eye(13),'complete seed+future input isometry')
    # The former factorization was not automatic: reversing the same seed returns all.
    reversed_seed=[w@w for w in W0]
    returned=inc0.expectation(reversed_seed)
    for r,q in zip(returned,Q):near(r,np.eye(len(q)),'coherent reentry countercontrol')
    mismatch=max(la.norm(r-q,2) for r,q in zip(returned,Q))
    require(mismatch>.99,'cold product fails for arbitrary archive-preserving continuation')
    # Every old A5 Lie direction is stationary for this true factorized continuation.
    maxrow=0.;num=0
    for b,db in enumerate(inc0.new):
        for i in range(db):
            X=np.zeros((db,db),complex);X[i,i]=1j
            gens=[X]
            for j in range(i):
                X=np.zeros((db,db),complex);X[i,j]=1;X[j,i]=-1;gens.append(X)
                X=np.zeros((db,db),complex);X[i,j]=X[j,i]=1j;gens.append(X)
            for X in gens:
                oldd=[np.zeros_like(w,dtype=complex) for w in W0];oldd[b]=X@W0[b]
                oldc=inc0.expectation(oldd)
                newdc=corner([r@v for r,v in zip(R,oldc)])
                _,gs=price_source(fullC,newdc)
                maxrow=max(maxrow,abs(gs));num+=1
                require(abs(gs)<1e-17,'every independent old-left return source')
    # Archive is unchanged on the actual entire fine algebra.
    labels=[np.diag([1.,0.,1.]),np.diag([1.,0.])]
    fine=whole.embed(labels)
    for u,l in zip(U,fine):near(u@l,l@u,'exact original A0 archive-law structure')
    # New source is not automatically stationary. It must retain its own equation.
    require(abs(src)>1e-9,'future physical-field source not silently suppressed')
    def scalar(t):
        rr=[np.eye(len(x))-kappa*(x+t*dx)@(x+t*dx) for x,dx in zip(a,da)]
        cc=corner([r@q for r,q in zip(rr,Q)])
        return price_source(cc,np.zeros_like(cc))[0]
    h=1e-4
    fd=(-scalar(2*h)+8*scalar(h)-8*scalar(-h)+scalar(-2*h))/(12*h)
    near(fd,src,'independent full price finite difference',2e-14)
    return {'old_AF_level':2,'seed_level':5,'final_level':9,
            'full_GNS_dimension':int(emb.shape[0]),'input_rank':13,
            'Spin4_oldRIGHT2_are_untouched_spectator_multiplicity':8,
            'with_spectators_full_dimension':8*int(emb.shape[0]),
            'with_spectators_input_rank':104,
            'old_left_directions_checked':num,'max_old_return_source':maxrow,
            'future_return_source_per_spectator':src,
            'complete_return_price_per_spectator':value,
            'coherent_reentry_product_mismatch':mismatch,
            'future_heat_stationarity_claimed':False}


def constant_free_graph_tests():
    # Critical distinction: equality on the realization graph is NOT normal stationarity.
    inc=Inclusion((1,1),4)
    aa=[np.array([[.31]]),np.array([[.31]])]
    V,dV=lift(inc,aa,[np.ones((1,1)),np.ones((1,1))])
    C=la.block_diag(*inc.expectation(V));dC=la.block_diag(*inc.expectation(dV))
    _,source=price_source(C,dC)
    require(source>1e-7,'changing the declared native row has its real source')
    # A real independently varied pair rotation exists even holding a's semantic label fixed.
    delta=[np.zeros_like(v) for v in V]
    inds0=inc.expanded(inc.positions[0,0][0]);inds1=inc.expanded(inc.positions[0,0][1])
    G=np.zeros_like(V[0]);G[np.ix_(inds0,inds1)]=-np.eye(len(inds0));G[np.ix_(inds1,inds0)]=np.eye(len(inds0))
    delta[0]=G@V[0]
    _,normal=price_source(C,la.block_diag(*inc.expectation(delta)))
    require(abs(normal)>1e-8,'independent off-graph completion source is retained')
    return {'graph_source':source,'independent_completion_source':normal,
            'all_free_completion_controls_stationary':False}


def reduced_DATA_channel_controls():
    parent,_=load_parent()
    rows=[]
    r=1/9
    boost=(1+r)/(1-r)
    for scale in (1.,.5,.25,.125):
        nu=.6*scale
        rec=parent.rows(r,nu,full=True)
        a=rec['a'];a2=a@a;H=la.sqrtm(2*np.eye(16)-a2).astype(complex)
        B=np.eye(16)-a2;S=a@H
        old=rec['kraus']
        new=np.stack([math.sqrt(p**3)*np.eye(16),math.sqrt(kappa)*B,math.sqrt(kappa)*S])
        near(np.einsum('kji,kjl->il',new.conj(),new),np.eye(16),'new DATA channel trace preserving')
        near(np.einsum('kij,klj->il',new,new.conj()),np.eye(16),'new DATA channel unital')
        # The normalized Choi trace distance tests a genuine entangled input.
        vo=old.reshape(len(old),-1);vn=new.reshape(len(new),-1)
        choi_old=vo.T@vo.conj();choi_new=vn.T@vn.conj()
        distance=float(la.svdvals(choi_old-choi_new).sum()/16)
        xnorm=la.norm(a,2)
        deltaPsi=(3/8)*nu**2*(7+boost**2)
        theoretical=kappa*(2*deltaPsi*xnorm**2+(1+2*math.sqrt(2)/(math.sqrt(2)+1))*xnorm**4)
        require(distance<=theoretical+1e-12,'dimension-free proved diamond upper bound controls entangled input')
        unital_defect=float(la.norm(np.einsum('kij,klj->il',old,old.conj())-np.eye(16),2))
        require(unital_defect>1e-10,'finite DATA-channel equivalence is explicitly rejected')
        rows.append({'nu':nu,'normalized_Choi_trace_distance':distance,
                     'analytic_diamond_upper_bound':theoretical,
                     'distance_divided_by_nu_power4':distance/nu**4,
                     'original_unitality_defect':unital_defect})
    require(all(rows[j+1]['normalized_Choi_trace_distance']<.08*rows[j]['normalized_Choi_trace_distance'] for j in range(3)),
            'original DATA-channel discrepancy has controlled fourth-order decay')
    return {'controls':rows,'exact_finite_DATA_channel_equivalence':False,
            'bound':'kappa*(2*deltaPsi*||a||^2+(1+2sqrt(2)/(sqrt(2)+1))*||a||^4)',
            'deltaPsi_upper_bound':'(3/8)*nu^2*(7+||U_boost||^2)',
            'future_access_scope':'DATA and external reference; not the original fine-record algebra',
            'composition_error_bound':'sum of the per-tick diamond bounds, for DATA-only intervening channels'}


def main():
    out={'input_commit':'d37bd1ecf9550034586f32426fac84aecaf43be0',
         'four_level_identity':algebraic_identities(),
         'original_two_tick':original_two_tick(),
         'canonical_seed':canonical_seed_composition(),
         'domain_controls':constant_free_graph_tests(),
         'reduced_DATA_readout':reduced_DATA_channel_controls()}
    out.update({'status':'PASS_AF_ORIGINAL_JULIA_RETURN_SOURCE_TRANSPORT',
                'new_checks':COUNT,'max_errors':MAXERR,
                'new_pure_prepared_ancillas':0,
                'native_G_CX_SourceI_word_emitted':False,
                'full_history_record_laws_identified':False,
                'full_heat_source_identified':False,
                'all42_geometric_source_identified':False,
                'physical_variation_domain_proved':False,
                'GR_closed':False,'Lean_or_CI_run':False,
                'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},
                'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    print(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False))

if __name__=='__main__':main()
