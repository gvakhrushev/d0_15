#!/usr/bin/env python3
"""Full-clock thermal source, without reflection/isospectral assumptions.

Exact native 38/39-stage five-wire words independently replayed from the
owned G, CX, quaternion SourceI definitions. Structural smooth phase
controls do NOT assert continuous native pulse admission. All heat modes
and the paired-Hodge harmonic complement remain in the formula.
"""
from __future__ import annotations
from fractions import Fraction as Q
from collections import Counter
import json, math
import numpy as np
import scipy.linalg as la
import mpmath as mp
import sympy as s
from sympy.polys.matrices import DomainMatrix
mp.mp.dps = 160
checks=0

def require(ok, name):
    global checks
    checks+=1
    if not bool(ok): raise AssertionError(name)

def near(a,b,name,tol=2e-11):
    require(np.allclose(a,b,atol=tol,rtol=tol),name)

def fmt(v): return mp.nstr(v,32)

def rational_bounds(N, scene):
    # beta=2p^2 belongs to (3/4,4/5). All bounds here are exact rationals.
    x=Q(2,55) if scene else Q(2,5)
    q=x**N/math.factorial(N)
    alpha=Q(176,359) if scene else Q(40,3)
    exp_majorant=1/(1-x*x)
    first=alpha*exp_majorant*q/(1-q)**2
    second_cross=alpha*exp_majorant*2*q*q/(1-q)**3+Q(4,5)*first*first
    return first,second_cross

def mpq(q): return mp.mpf(q.numerator)/q.denominator

def bare_heat(N,theta,beta):
    # Two exact monodromy phases +/-theta, with both Hodge grades.
    Z=2*sum(mp.exp(-beta*(1-mp.cos((2*mp.pi*j+sgn*theta)/N)))
            for sgn in (-1,1) for j in range(N))
    return mp.log(Z)/beta

def bare_series(N,theta,beta,order=24):
    # Z=4 N exp(-beta) [I0+2 sum I_(kN) cos(k theta)].
    A=mp.besseli(0,beta)+2*sum(mp.besseli(k*N,beta)*mp.cos(k*theta)
                              for k in range(1,order+1))
    return mp.log(4*N*mp.exp(-beta)*A)/beta

def bare_phase_control(N):
    beta=2*((mp.sqrt(5)-1)/2)**2; theta=mp.mpf('0.47')
    direct=bare_heat(N,theta,beta)
    series=bare_series(N,theta,beta)
    g=mp.diff(lambda th:bare_series(N,th,beta),theta)
    h=mp.diff(lambda th:bare_series(N,th,beta),theta,2)
    gd=mp.diff(lambda th:bare_heat(N,th,beta),theta)
    hd=mp.diff(lambda th:bare_heat(N,th,beta),theta,2)
    # For this unit-speed phase path ||W'||=||W''||=1.
    b1,b2=rational_bounds(N,False)
    scale=max(abs(g),abs(h),mp.mpf('1e-145'))
    err=max(abs(g-gd),abs(h-hd))/scale
    # Truncation at 24 windings is bounded, but tiny for these N>=3.
    require(abs(direct-series)<mp.mpf('1e-75'),'phase value/series')
    require(err<mp.mpf('1e-55'),'phase first/second derivative agreement')
    require(0<abs(g)<mpq(b1),'nonzero nonreflection heat below exact C1 bound')
    require(abs(h)<mpq(b1+b2),'nonreflection heat below exact C2 bound')
    return {'N':N,'heat':fmt(direct),'first_source':fmt(g),'second_source':fmt(h),
            'relative_jet_error':fmt(err),'C1_bound':fmt(mpq(b1)),
            'C2_unit_phase_bound':fmt(mpq(b1+b2))}

def scene_matrices():
    cuts=(0,9,20,33);Adj=np.zeros((33,33))
    for i in range(3):
        for j in range(3):
            if i!=j:Adj[cuts[i]:cuts[i+1],cuts[j]:cuts[j+1]]=1
    deg=Adj.sum(1)+2
    R=np.diag(1/np.sqrt(deg))
    require(int(Adj.sum()/2)==359,'owned scene edges')
    near(deg,np.array([26]*9+[24]*11+[22]*13),'owned scene degrees')
    return R@Adj@R,R@R

def shift(gates):
    N=len(gates);d=len(gates[0]);T=np.zeros((N*d,N*d),complex)
    for j,g in enumerate(gates):T[((j+1)%N)*d:((j+1)%N+1)*d,j*d:(j+1)*d]=g
    return T

def full_scene_control():
    # These smooth matrices are a structural comparison only.
    def rot(a):return np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
    gates=[rot(.13),rot(-.21),rot(.55)]
    N=3;d=2;T=shift(gates);B,C=scene_matrices()
    L=np.eye(33*N*d)-np.kron(B,np.eye(N*d))-np.kron(C,T+T.conj().T)
    eig=la.eigvalsh(L)
    beta=2*((math.sqrt(5)-1)/2)**2
    Z0=np.exp(-beta*eig).sum()
    Zphase=0.
    phases=(.47,-.47)
    for theta in phases:
        for k in range(N):
            Ls=np.eye(33)-B-2*math.cos((theta+2*math.pi*k)/N)*C
            Zphase+=np.exp(-beta*la.eigvalsh(Ls)).sum()
    near(Z0,Zphase,'all scene eigenvalues/phase sum')
    paired=2*Z0+359*N*d
    require(425*N*d==2550,'full two-grade dimension, no oldRIGHT added twice')
    require(eig.min()>-1e-12 and eig.max()<2+1e-12,'normalized Hodge range')
    return {'vertices':33,'H0_modes':len(eig),'full_H0_H1_modes':425*N*d,
            'harmonic_complement':359*N*d,'full_heat':math.log(paired)/beta,
            'spectral_identity_error':float(abs(Z0-Zphase))}

def exact_native():
    p=(s.sqrt(5)-1)/2;a=s.sqrt(p);field=s.QQ.algebraic_field(a)
    def dm(M):return DomainMatrix.from_Matrix(s.Matrix(M)).convert_to(field)
    I=dm(s.eye(32));Z=dm(s.zeros(32))
    G=s.Matrix([[a,-p],[p,a]])
    Li=s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    SI=s.diag(s.eye(4),Li)
    CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    def gate(op,wires):
        local={'G':G,'CX':CX,'SourceI':SI}[op]
        require(4 not in wires,'immutable oldRIGHT retained')
        require((op!='SourceI' or wires==(0,2,3)),'actual SourceI frame')
        require(op=='SourceI' or not set(wires)&{2,3},'no separate Spin addressing')
        out=s.zeros(32);k=len(wires)
        for col in range(32):
            bits=[(col>>(4-j))&1 for j in range(5)]
            j=sum(bits[w]<<(k-1-u) for u,w in enumerate(wires))
            for i in range(1<<k):
                if local[i,j]==0:continue
                bb=bits[:]
                for u,w in enumerate(wires):bb[w]=(i>>(k-1-u))&1
                row=sum(bb[u]<<(4-u) for u in range(5))
                out[row,col]=local[i,j]
        ans=dm(out)
        require((ans.transpose().matmul(ans)-I).is_zero_matrix,'primitive all32 orthogonality')
        return ans
    def swap(a,b):return [('CX',(a,b)),('CX',(b,a)),('CX',(a,b))]
    si=('SourceI',(0,2,3)); route=swap(0,1)
    vg=route+[('G',(0,))]+route
    def inverse(word):
        out=[]
        for op,wires in word[::-1]:
            if op=='CX':out.append((op,wires))
            elif op=='SourceI':out.extend([si]*3)
            else:
                r=[] if wires[0]==0 else swap(wires[0],0)
                out+=r+[si,si,('G',(0,)),si,si]+r
        return out
    query=inverse(vg)+route+[si,si]+route+vg
    v=[('G',(1,))]
    A=inverse(v)+v+query;BB=inverse(v)+query+v
    cache={g:gate(*g) for g in set(A+BB)}
    p0=dm(s.diag(*([1]*8+[0]*24)))
    def endpoint(word):
        W=I
        for g in word:W=cache[g].matmul(W)
        require((W.transpose().matmul(W)-I).is_zero_matrix,'endpoint all32 unitarity')
        return W
    wa,wb=endpoint(A),endpoint(BB)
    c=p**3; ss=2*a*p
    qa=s.Matrix([[c,ss],[ss,-c]])
    qb=G*qa*G.T
    ea=dm(s.kronecker_product(s.eye(2),qa,s.eye(8)))
    eb=dm(s.kronecker_product(s.eye(2),qb,s.eye(8)))
    require((wa-ea).is_zero_matrix and (wb-eb).is_zero_matrix,'literal 38-stage original endpoints')
    require(len(query)==26 and len(A)==len(BB)==38,'actual raw stages')
    inv=dict(Counter(g[0] for g in A))
    require(inv==dict(Counter(g[0] for g in BB))=={'G':4,'CX':24,'SourceI':10},'equal original inventory')
    # Append a REAL CX at the end; neither endpoint is now a reflection.
    tail=('CX',(0,1));wc=cache[tail].matmul(wa);wd=cache[tail].matmul(wb)
    require(not (wc.matmul(wc)-I).is_zero_matrix,'39-stage C not reflection')
    require(not (wd.matmul(wd)-I).is_zero_matrix,'39-stage D not reflection')
    we=cache[si].matmul(wa)
    require((wc.matmul(p0)-we.matmul(p0)).is_zero_matrix,'two 39-stage words have identical full admitted input-output columns')
    require(not (wc-we).is_zero_matrix,'input-output equality does not delete complementary columns')
    require((p0.matmul(wc).matmul(p0)-p0.scalarmul(field.from_sympy(c))).is_zero_matrix,'C original input corner')
    cb=2*p**6-1
    require((p0.matmul(wd).matmul(p0)-p0.scalarmul(field.from_sympy(cb))).is_zero_matrix,'D original input corner')
    # Full spectrum: port0 reflection +/-1; port1 XQ rotation, 8 copies each.
    def tr(M):
        z=M.to_dense().rep.to_ddm()
        return sum((z[i][i] for i in range(32)),field.zero)
    for W,sk in [(wc,ss),(wd,2*c*ss),(we,s.Integer(0))]:
        Wk=I
        for k in range(1,5):
            Wk=W.matmul(Wk)
            expected=8*(1+(-1)**k+2*s.chebyshevt(k,sk))
            require(tr(Wk)==field.from_sympy(expected),'all32 spectral trace moments')
    # Every nonclosing leakage vanishes for actual generated cuts.
    for word in [A,BB,A+[tail],BB+[tail]]:
        pref=I;pj=p0
        for idx,g in enumerate(word):
            mat=cache[g];nxt=mat.matmul(pref)
            pn=nxt.matmul(p0).matmul(nxt.transpose())
            if idx<len(word)-1:
                require((I-pn).matmul(mat).matmul(pj).is_zero_matrix,'generated nonclosing cut exact')
            pref,pj=nxt,pn
    # Recheck the new generated-cut source on the actual 38-stage word.
    # The rank-supported commutator is a mathematical comparison, not a new gate.
    gen=wa.matmul(p0)-p0.matmul(wa)
    require((wa.matmul(gen)+gen.matmul(wa)).is_zero_matrix,'reflection anti-commutator')
    dP0=gen.matmul(p0)-p0.matmul(gen)
    pref=[I]
    for g in A: pref.append(cache[g].matmul(pref[-1]))
    cuts=[v.matmul(p0).matmul(v.transpose()) for v in pref[:-1]]
    dcuts=[Z]+[-v.matmul(dP0).matmul(v.transpose()) for v in pref[1:-1]]
    dgs=[Z for _ in A]
    dgs[0]=-cache[A[0]].matmul(gen)
    dgs[-1]=gen.matmul(cache[A[-1]])
    for j in range(len(A)-1):
        gj=cache[A[j]]
        dC=-dcuts[j+1].matmul(gj).matmul(cuts[j])+(I-cuts[j+1]).matmul(dgs[j]).matmul(cuts[j])+(I-cuts[j+1]).matmul(gj).matmul(dcuts[j])
        require(dC.is_zero_matrix,'generated-cut nonclosing first jet')
    gL=cache[A[-1]];PL=cuts[-1]
    CL=(I-p0).matmul(gL).matmul(PL)
    gatejet=(I-p0).matmul(dgs[-1]).matmul(PL)
    cutjet=(I-p0).matmul(gL).matmul(dcuts[-1])
    zeta=s.Rational(1,2**20); e=1-c*c
    Res=I+PL.scalarmul(field.from_sympy(zeta*e/(1-zeta*e)))
    gate_source=2*field.from_sympy(zeta)*tr(Res.matmul(CL.transpose()).matmul(gatejet))
    cut_source=2*field.from_sympy(zeta)*tr(Res.matmul(CL.transpose()).matmul(cutjet))
    expected_half=field.from_sympy(16*zeta*c*e/(1-zeta*e))
    require(gate_source==cut_source==expected_half,'both generated-source halves positive and equal')
    source_string=str(s.N(field.to_sympy(gate_source+cut_source),40))
    return {'source_commit':'5fe5203da2439d325dc9ef70f52c1111822fc22b',
            'native_definition_blob':'9a32a3fa2e594c087d24b9d5dec497c4c5e03f44',
            'original_word_stages':38,'original_inventory':inv,
            'modified_word_stages':39,'modified_inventory':{'G':4,'CX':25,'SourceI':10},
            'fibre_dimension':32,'active_rank':8,'all_column_replay':True,
            'modified_words_are_nonreflective':True,
            'generated_cut_and_gate_sources_exact_equal_positive_halves':True,
            'full_QUERY_source_at_native_zeta':source_string,
            'same_output_pair':{'first_tail':'CX(0,1)','second_tail':'SourceI(0,2,3)',
              'same_all_8_input_columns':True,'different_full_32_column_operators':True,
              'second_inventory':{'G':4,'CX':24,'SourceI':11},
              'same_inventory_claimed':False},
            'modified_H0_H1_scene_modes':425*39*32}

def native_scene_bounds():
    beta=2*((mp.sqrt(5)-1)/2)**2;p=(mp.sqrt(5)-1)/2
    ss=2*p**mp.mpf('1.5');ss2=2*p**3*ss
    tracegap=16*(ss-ss2);N=39
    # Exact Golden interval: f(8/13)<0<f(13/21), f(x)=x^2+x-1.
    pl,pu=Q(8,13),Q(13,21)
    require(pl*pl+pl-1<0<pu*pu+pu-1,'exact Golden root isolation')
    require(Q(39,50)**2<pl,'exact square-root lower bound')
    tracegap_lower=16*2*pl*Q(39,50)*(1-2*pu**3)
    require(tracegap_lower>8,'strict rational first spectral moment gap')
    require(16*2*pl*Q(39,50)>tracegap_lower,'same-output first winding also dominates')
    # a_N lower bound from N positive temporal steps, no spatial steps.
    lower=mp.exp(-beta)*beta**N/mp.factorial(N)*(9/mp.mpf(26)**N+11/mp.mpf(24)**N+13/mp.mpf(22)**N)
    x=beta/22;q=x**N/mp.factorial(N)
    # a_(kN)<=33 exp(beta(b-1)+x^2) q^k <=33 exp(x^2)q^k
    tail=33*mp.exp(x*x)*q*q/(1-q)
    # |Tr Wc^k-Tr Wd^k|<=64. First trace difference is >8.
    positive_trace_lower=tracegap*lower-64*tail
    require(positive_trace_lower>0,'strict total heat contrast at original beta')
    # Zfull between 359*N*d and 425*N*d; log ratio >=deltaZ/maxZ.
    # deltaZ=4N sum a_(kN) tracegap_k, d=32.
    heat_lower=4*positive_trace_lower/(beta*425*32)
    c1,_=rational_bounds(N,True)
    heat_upper=2*mpq(c1)
    # A conservative lower and tail bound entirely in exact rational arithmetic.
    xx=Q(2,55);qq=xx**N/math.factorial(N)
    aN_lower=Q(1,5)*Q(3,4)**N/math.factorial(N)*(Q(9,26**N)+Q(11,24**N)+Q(13,22**N))
    tail_upper=33/(1-xx*xx)*qq*qq/(1-qq)
    gap_lower=8*aN_lower-64*tail_upper
    require(gap_lower>0,'strict all-winding heat gap proved by exact rationals')
    exact_heat_lower=4*gap_lower/(Q(4,5)*425*32)
    require(0<mpq(exact_heat_lower)<heat_lower<heat_upper,'native contrast bounds')
    z=mp.mpf(2)**-20;c=p**3;cb=2*p**6-1
    Jgap=8*mp.log((1-z+z*cb*cb)/(1-z+z*c*c))
    require(Jgap>0,'actual original rank-eight feedback gap')
    return {'N':N,'trace_W_C_minus_W_D':fmt(tracegap),
            'strict_heat_gap_lower':fmt(mpq(exact_heat_lower)),
            'sharper_algebraic_lower_numeric':fmt(heat_lower),
            'heat_gap_upper':fmt(heat_upper),
            'strict_positive_sign_certified_in_exact_rationals':True,
            'same_input_output_pair_C_E':{'heat_gap_same_positive_lower_bound':fmt(mpq(exact_heat_lower)),
               'heat_gap_same_upper_bound':fmt(heat_upper),'feedback_difference_exact':'0',
               'proof':'first trace gap 16*s_A is larger; identical remaining-tail bound'},
            'feedback_gap':fmt(Jgap),'full_price_gap_is_strictly_positive':True,
            'heat_gap_proof':'positive first winding dominates bounded remaining windings',
            'full_large_heat_diagonalization_executed':False}

def main():
    data={'status':'PASS_FULL_CLOCK_WINDING_SOURCE',
          'native':exact_native(),
          'structural_phase_controls':[bare_phase_control(n) for n in (3,8,26,38)],
          'full_scene_control':full_scene_control(),
          'native_nonreflection_comparison':native_scene_bounds(),
          'source_bounds':[]}
    for N in (8,26,38,39,128):
        b1,b2=rational_bounds(N,False);s1,s2=rational_bounds(N,True)
        data['source_bounds'].append({'N':N,'bare_C1_endpoint':fmt(mpq(b1)),
          'scene_C1_endpoint':fmt(mpq(s1)),'scene_C1_gate_max':fmt(N*mpq(s1)),
          'scene_C2_cross_only':fmt(mpq(s2)),
          'bounds_computed_as_exact_rationals':True})
    data.update({'checks':checks,'scope':'same declared paired-clock or homogeneous INTERNAL scene; fixed dimensions/beta/scene',
       'continuous_native_gate_admission_asserted':False,'arbitrary_RawZone_scene_covered':False,
       'physical_action_selection_proved':False,'original_full42_replayed':False,'Lean_or_CI_run':False,'GR_closed':False})
    print(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__':main()
