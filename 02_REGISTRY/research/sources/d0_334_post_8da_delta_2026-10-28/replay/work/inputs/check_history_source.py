#!/usr/bin/env python3
"""Same original CAR/Julia/Walsh/Golden source on a retained multi-tick tape.

No new physical decoder or state is introduced. Algebraic original operators
are consumed from the pinned owners. Smooth operator comparisons below do
NOT grant continuous native gate admission. The full large many-tick unitary
is not materialized; its actual fine-history isometry is replayed at m=2.
"""
from __future__ import annotations
import hashlib, json, math, platform
from pathlib import Path
import numpy as np
import scipy.linalg as la
import sympy as s
import mpmath as mp

P=(math.sqrt(5)-1)/2
KAPPA=2*P*P
ZETA=2**-20
I=np.eye(16,dtype=complex)
COUNT=0

def require(ok, name):
    global COUNT
    COUNT += 1
    if not bool(ok): raise ArithmeticError(name)

def near(a,b,name,atol=3e-12):
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    require(err<atol,name+': '+str(err))
    return err

ORDER=(0,2,3,1)
CREATORS=[]
for mode in range(4):
    c=np.zeros((16,16),complex)
    for bits in range(16):
        if not ((bits>>mode)&1):
            c[bits|(1<<mode),bits]=(-1)**sum((bits>>j)&1 for j in ORDER[:ORDER.index(mode)])
    CREATORS.append(c)
GEN=CREATORS[0]@CREATORS[1].conj().T+CREATORS[1]@CREATORS[0].conj().T

def rows(r,nu,dr=0.,dnu=0.,full=False):
    """Literal first Julia operands, duplicated adjacent words, Walsh ordering."""
    U=I+2*r/(1-r*r)*GEN+2*r*r/(1-r*r)*GEN@GEN
    dU=2*(1+r*r)/(1-r*r)**2*dr*GEN+4*r/(1-r*r)**2*dr*GEN@GEN
    words=[];dwords=[];a=np.zeros((16,16),complex);da=a.copy()
    def julia_root(T,dT):
        vals,V=la.eigh((I-T+(I-T).conj().T)/2)
        require(vals.min()>0,'strict original Julia root chart')
        S=(V*np.sqrt(vals))@V.conj().T
        dS=la.solve_sylvester(S,S,-dT)
        near(S@S,I-T,'complete Julia square root')
        near(S@dS+dS@S,-dT,'complete Julia derivative')
        return S,dS
    phases=(1j,1j,-1,-1j)
    for j,c in enumerate(CREATORS):
        b=nu*c;db=dnu*c
        x=phases[j]*(b@U if j==1 else b)
        dx=phases[j]*(db@U+b@dU if j==1 else db)
        a+=x+x.conj().T-b-b.conj().T
        da+=dx+dx.conj().T-db-db.conj().T
        if full:
            left,dl=julia_root(x@x.conj().T,dx@x.conj().T+x@dx.conj().T)
            right,drr=julia_root(x.conj().T@x,dx.conj().T@x+x.conj().T@dx)
            l0,dl0=julia_root(b@b.conj().T,db@b.conj().T+b@db.conj().T)
            r0,dr0=julia_root(b.conj().T@b,db.conj().T@b+b.conj().T@db)
            for w,dw in [((x,left),(dx,dl)),((x.conj().T,right),(dx.conj().T,drr)),
                         ((-b,-l0),(-db,-dl0)),((-b.conj().T,-r0),(-db.conj().T,-dr0))]:
                words.extend((w,w));dwords.extend((dw,dw))
    a/=16;da/=16
    A=a.conj().T@a;dA=da.conj().T@a+a.conj().T@da
    C=I-KAPPA*A;dC=-KAPPA*dA
    out={'a':a,'da':da,'A':A,'dA':dA,'C':C,'dC':dC}
    if full:
        W=la.hadamard(32)/32
        n=np.einsum('ij,jkab->ikab',W,np.asarray(words)).reshape(64,16,16)
        dn=np.einsum('ij,jkab->ikab',W,np.asarray(dwords)).reshape(64,16,16)
        near(n[0],a,'same original zero Walsh row')
        near(dn[0],da,'same original row derivative')
        near(sum(v@v.conj().T for v in n),I,'original row completeness')
        near(sum(v.conj().T@v for v in n),I,'original column completeness')
        raw=np.zeros((128,16,16),complex);draw=raw.copy()
        for j in range(64):
            X=n[j].conj().T@a;dX=dn[j].conj().T@a+n[j].conj().T@da
            raw[2*j]=(I if j==0 else 0)-2*P*P*X
            raw[2*j+1]=-2*P*math.sqrt(P)*X
            draw[2*j]=-2*P*P*dX
            draw[2*j+1]=-2*P*math.sqrt(P)*dX
        near(raw[0],C,'original K0 corner')
        near(draw[0],dC,'original K0 corner derivative')
        near(np.einsum('kji,kjl->il',raw.conj(),raw),I,'all128 CPTP')
        near(np.einsum('kji,kjl->il',draw.conj(),raw)+np.einsum('kji,kjl->il',raw.conj(),draw),
             np.zeros((16,16)),'all128 derivative completeness')
        # Full2048 reflection is I-2LL*. Verify its all-column algebra via L*L.
        N=np.concatenate(list(n),axis=1)
        L=np.concatenate([P*N.conj().T,math.sqrt(P)*N.conj().T],axis=0)
        near(L.conj().T@L,I,'original2048 full reflection column algebra')
        require(L.shape==(2048,16),'original full2048, no substitute dilation')
        out.update({'kraus':raw,'dkraus':draw,'fine_rows':128})
    return out

def product(cs):
    K=I.copy()
    for C in cs: K=C@K
    return K

def jet(cs,dcs):
    K=I.copy();dK=np.zeros_like(K)
    for C,dC in zip(cs,dcs):dK=dC@K+C@dK;K=C@K
    return K,dK

def price_from_F(F,z=ZETA):
    ev=la.eigvalsh((F+F.conj().T)/2)
    return -float(np.log1p(-z*ev).sum())

def action_source(items,z=ZETA):
    cs=[x['C'] for x in items];dcs=[x['dC'] for x in items]
    K,dK=jet(cs,dcs);F=I-K.conj().T@K;R=la.inv(I-z*F)
    g=-2*z*np.trace(R@K.conj().T@dK).real
    pref=[I.copy()]
    for C in cs:pref.append(C@pref[-1])
    post=I.copy();weights=[None]*len(cs)
    for j in reversed(range(len(cs))):
        V=pref[j]@R@K.conj().T@post
        weights[j]=(V+V.conj().T)/2
        post=post@cs[j]
    g2=2*z*KAPPA*sum(np.trace(W@x['dA']).real for W,x in zip(weights,items))
    near(g,g2,'noncommuting all-history adjoint source',2e-13)
    q=KAPPA*sum(la.norm(x['A'],2) for x in items)
    total_da=sum(la.norm(x['dA'],'nuc') for x in items)
    leading=2*z*KAPPA*sum(np.trace(x['dA']).real for x in items)
    budget=4*z*KAPPA*q/(1-z)*total_da
    require(abs(g-leading)<=budget+1e-15,'cumulative-memory C1 bound')
    weights_error=max(la.norm(W-I,2) for W in weights)
    require(weights_error<=2*q/(1-z)+1e-12,'all matrix adjoint weights close-to-identity bound')
    return {'K':K,'dK':dK,'F':F,'R':R,'source':g,'leading_source':leading,
            'cumulative_leakage':q,'source_error_bound':budget,'weights_error':weights_error,
            'price':price_from_F(F,z)}

def full_two_tick():
    one=rows(1/9,3/5,dr=1,full=True)
    two=rows(1/8,1/2,dr=-.7,dnu=.2,full=True)
    require(la.norm(one['A']@two['A']-two['A']@one['A'])>1e-10,
            'actual original successive A operators do not commute')
    H=np.einsum('bij,ajk->abik',two['kraus'],one['kraus']).reshape(128**2,16,16)
    dH=(np.einsum('bij,ajk->abik',two['dkraus'],one['kraus'])+
        np.einsum('bij,ajk->abik',two['kraus'],one['dkraus'])).reshape(H.shape)
    near(np.einsum('kji,kjl->il',H.conj(),H),I,'all16384 original fine histories CPTP')
    out=action_source([one,two])
    near(H[0],out['K'],'actual zero-record product')
    near(dH[0],out['dK'],'actual zero-record derivative')
    F=np.einsum('kji,kjl->il',H[1:].conj(),H[1:])
    dF=np.einsum('kji,kjl->il',dH[1:].conj(),H[1:])+np.einsum('kji,kjl->il',H[1:].conj(),dH[1:])
    e0=near(F,out['F'],'all nonblank records agree with complete defect')
    e1=near(dF,-out['dK'].conj().T@out['K']-out['K'].conj().T@out['dK'],
            'all nonblank record source agrees with endpoint product')
    from_tape=ZETA*np.trace(out['R']@dF).real
    near(from_tape,out['source'],'full tape source')
    def scalar(t):
        its=[rows(1/9+t,3/5),rows(1/8-.7*t,1/2+.2*t)]
        K=product([x['C'] for x in its]);return price_from_F(I-K.conj().T@K)
    eps=2e-4
    fd=(-scalar(2*eps)+8*scalar(eps)-8*scalar(-eps)+scalar(-2*eps))/(12*eps)
    near(fd,out['source'],'independent full scalar finite difference',3e-14)
    naive=sum(action_source([x])['source'] for x in [one,two])
    require(abs(naive-out['source'])>1e-10,'sum of one-tick sources is not full-history source')
    return {'ticks':2,'fine_histories':128**2,'DATA_dimension':16,
      'oldRIGHT_multiplicity_in_test':1,'all_input_columns':16,
      'complete_output_isometry_rows':16*128**2,'large_total_unitary_materialized':False,
      'noncommutation_norm':float(la.norm(one['A']@two['A']-two['A']@one['A'])),
      'defect_error':e0,'source_matrix_error':e1,'actual_full_source':out['source'],
      'finite_difference_error':float(abs(fd-out['source'])),
      'incorrect_sum_of_one_tick_sources':naive,'difference_from_incorrect_sum':out['source']-naive}

def exact_repeated_source():
    p=(s.sqrt(5)-1)/2;Kfield=s.QQ.algebraic_field(p);f=Kfield.from_sympy
    zero,one=Kfield.zero,Kfield.one
    # First jets in the OWNED two spectral invariants s,t, not a new fit.
    def const(x):return (f(s.sympify(x)),zero,zero)
    def add(a,b):return tuple(x+y for x,y in zip(a,b))
    def mul(a,b):return (a[0]*b[0],a[1]*b[0]+a[0]*b[1],a[2]*b[0]+a[0]*b[2])
    def neg(a):return tuple(-x for x in a)
    def smul(a,c):return mul(a,const(c))
    r,nu=s.symbols('r nu',real=True)
    polyP=5*r**4+r**3-8*r*r-r+5;polyQ=23*r**4+6*r**3-32*r*r-10*r+25
    S=nu**2*polyP/(64*(1-r*r)**2);T=nu**4*polyQ/(16384*(1-r*r)**2)
    b={r:s.Rational(1,9),nu:s.Rational(3,5)}
    sj=(f(S.subs(b)),one,zero);tj=(f(T.subs(b)),zero,one)
    def pmul(x,y):
        return (add(mul(x[0],y[0]),neg(mul(mul(x[1],y[1]),tj))),
                add(add(mul(x[0],y[1]),mul(x[1],y[0])),mul(mul(x[1],y[1]),sj)))
    C=(const(1),const(-2*p*p));ret=[]
    for n in (1,2,4):
        powc=(const(1),const(0))
        for _ in range(2*n):powc=pmul(powc,C)
        u=add(const(1-s.Rational(1,2**20)),smul(powc[0],s.Rational(1,2**20)))
        v=smul(powc[1],s.Rational(1,2**20))
        den=add(add(mul(u,u),mul(mul(u,v),sj)),mul(mul(v,v),tj))
        ds=-f(s.Integer(8))*den[1]/den[0];dt=-f(s.Integer(8))*den[2]/den[0]
        grads=[ds*f(s.diff(S,var).subs(b))+dt*f(s.diff(T,var).subs(b)) for var in (r,nu)]
        ret.append((n,den,grads))
    wedge=ret[0][2][0]*ret[1][2][1]-ret[0][2][1]*ret[1][2][0]
    require(wedge!=zero,'exact nonparallel original one/two-tick gradients')
    expr=Kfield.to_sympy(wedge)
    ratios=[ret[1][2][i]/ret[0][2][i] for i in (0,1)]
    require(ratios[0]!=ratios[1],'no common scalar source gain on original two-parameter chart')
    mp.mp.dps=80
    result=[]
    for n,den,gg in ret:
        result.append({'ticks':n,'source_r':str(s.N(Kfield.to_sympy(gg[0]),40)),
                       'source_nu':str(s.N(Kfield.to_sympy(gg[1]),40))})
    # Independent direct 16x16 product evaluation at actual fixture.
    item=rows(1/9,3/5,dr=1)
    for n,den,gg in ret:
        out=action_source([item]*n)
        near(out['source'],float(s.N(Kfield.to_sympy(gg[0]),30)),'exact scalar/direct16 source')
    return {'exact_field':'Q(sqrt(5))','native_fixture':{'r':'1/9','nu':'3/5','z':'2^-20'},
      'jets':result,'wedge_nonzero_exact':True,'wedge_diagnostic':str(s.N(expr,40)),
      'wedge_exact':str(expr),'two_to_one_r_ratio':str(s.N(Kfield.to_sympy(ratios[0]),40)),
      'two_to_one_nu_ratio':str(s.N(Kfield.to_sympy(ratios[1]),40)),
      'scope':'same original smooth operator comparison; not independently established physical field admission'}

def weak_history_controls():
    vals=[]
    for n in (8,16,32,64):
        h=1/n
        it=[rows(1/9+.025*math.sin(2*math.pi*j/n),h*(.5+.03*math.cos(2*math.pi*j/n)),
                 dnu=h*(.5+.03*math.cos(2*math.pi*j/n))) for j in range(n)]
        out=action_source(it)
        gain=2*ZETA*KAPPA*n*h*h
        err=abs(out['source']-out['leading_source'])/gain
        bound=out['source_error_bound']/gain
        vals.append({'ticks':n,'per_tick_nu_scale':h,'cumulative_leakage':out['cumulative_leakage'],
                     'normalized_source_error':err,'normalized_source_bound':bound})
    require(all(vals[j+1]['normalized_source_error']<.6*vals[j]['normalized_source_error']
                for j in range(3)),'controlled cumulative-weak-history convergence')
    # Critical age n~1/h^2: endpoint has nontrivial exponential memory.
    base=rows(1/9,3/5);B=base['A'];trB=float(np.trace(B).real)
    limiting_K=la.expm(-KAPPA*B);limit_price=price_from_F(I-limiting_K.conj().T@limiting_K)
    linear_price=2*ZETA*KAPPA*trB
    require(abs(limit_price-linear_price)>1e-9,'critical-age memory is not additive weak sum')
    critical=[]
    for n in (32,64,128,256):
        K=np.linalg.matrix_power(I-KAPPA*B/n,n)
        price=price_from_F(I-K.conj().T@K)
        critical.append({'ticks':n,'price_error_to_exact_exponential_limit':abs(price-limit_price)})
    require(critical[-1]['price_error_to_exact_exponential_limit']<critical[0]['price_error_to_exact_exponential_limit']/6,
            'critical-age exponential limit')
    return {'weak':vals,'critical':critical,'critical_limit_price':limit_price,
            'incorrect_additive_limit_price':linear_price,'critical_limit_gap':limit_price-linear_price,
            'physical_refinement_map_claimed':False}

def main():
    out={'input_commit':'46ebed17ddfa04faa8ab1a07a6a822b717f993ef',
         'original_constructor_blob':'d111c5bfeae3c384a4fe725f4a6d19277ea0005a',
         'full_tape':full_two_tick(),'repeated_original':exact_repeated_source(),
         'weak_and_critical':weak_history_controls(),
         'checks':COUNT,'status':'PASS_ORIGINAL_RETAINED_HISTORY_SOURCE',
         'GR_closed':False,'new_action_or_decoder':False,
         'original_42_field_source_transport_proved':False,
         'large_full_history_heat_replayed':False,'Lean_or_repository_CI_run':False,
         'scope':'exact complete-return formula and actual original CAR128 history controls; same geometric source map remains unproved',
         'environment':{'python':platform.python_version(),'numpy':np.__version__,'sympy':s.__version__},
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':main()
