#!/usr/bin/env python3
"""Exact full16 golden/Julia tape channel; definitions only, no old run()."""
from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json
import sympy as s

ROOT=Path(__file__).resolve().parents[4]
CREATORS='02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS={
 CREATORS:'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
 '02_REGISTRY/research/sources/d0_complete_exit_source_2026-10-17/check_complete_exit_source.py':'cbd3a04b61a5e355131947df4fc3d6a6beae7ea526942868fbbf63b655ac492d',
 '02_REGISTRY/research/A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md':'cf77a70da503c0a58725e1470ed9b73a493ee01a82293058d49dfd6758ae735a'}

def run(repo=None):
    repo=ROOT if repo is None else Path(repo).resolve()
    checks=[]
    def require(ok,name):
        if not bool(ok): raise ArithmeticError('record_channel:'+name)
        checks.append(name)
    def eq(x,y,name):
        z=x-y
        entries=list(z) if isinstance(z,s.MatrixBase) else [z]
        require(all(s.expand(v)==0 for v in entries),name)
    for path,digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,'pin_'+Path(path).name)
    tree=ast.parse((repo/CREATORS).read_text())
    nodes=[n for n in tree.body if (isinstance(n,ast.FunctionDef) and n.name=='creator') or
      (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXTERIOR_ORDER' for t in n.targets))]
    require(len(nodes)==2,'only_owned_creator_and_order_definitions_loaded')
    scope={'s':s,'lru_cache':lru_cache}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),CREATORS,'exec'),scope)
    C=[scope['creator'](r) for r in range(4)]
    I,O=s.eye(16),s.zeros(16)
    nu,b=s.Rational(3,5),s.Rational(4,5)
    def lift(M): return sum((M[i,j]*C[i]*C[j].H for i in range(4) for j in range(4)),O.copy())
    def gen(i,j):
        M=s.zeros(4);M[i,j],M[j,i]=1,-1
        return lift(M)
    def rot(K): return I+s.Rational(4,5)*K+s.Rational(2,5)*K*K
    def rows(returns):
        words=[]
        for r in range(4):
            nr=C[r]*C[r].H
            l0=I+(b-1)*nr; r0=I+(b-1)*(I-nr)
            pr=nu*C[r]*returns[r]
            lr=l0;rr=returns[r].H*r0*returns[r]
            for top,upper in ((pr,lr),(pr.H,rr),(-nu*C[r],-l0),(-nu*C[r].H,-r0)):
                words.extend(((top,upper),(top,upper)))
        out={}
        for label in range(32):
            for coefficient in range(2):
                out[(label,coefficient)]=sum((s.Rational((-1)**bin(label&j).count('1'),32)*
                    words[j][coefficient] for j in range(32)),O.copy())
        return out
    k12,k23,k13=gen(1,2),gen(2,3),gen(1,3)
    returns=[rot(k12)*rot(k23),rot(k23),rot(k13),I]
    for r,U in enumerate(returns): eq(U.H*U,I,'actual_proper_SO3_return_'+str(r))
    N=rows(returns); A=N[(0,0)]; A2=A*A
    eq(A,A.H,'actual_A_hD16_selfadjoint')
    eq(sum((x*x.H for x in N.values()),O.copy()),I,'all64_row_completeness')
    require(all(x==O for (label,coefficient),x in N.items() if label%2),'duplicate_odd_rows_dark')
    require(sum(x!=O for x in N.values())>13,'full16_nontrivial_row_fixture')
    # Q(p) matrix pairs, p^2=1-p, preserve ordered products without radicals.
    def f(x): return (x,s.zeros(*x.shape))
    def add(X,Y): return (X[0]+Y[0],X[1]+Y[1])
    def neg(X): return (-X[0],-X[1])
    def mul(X,Y):
        bd=X[1]*Y[1]
        return (X[0]*Y[0]+bd,X[0]*Y[1]+X[1]*Y[0]-bd)
    def scale(c,X):
        a,b=c
        return (a*X[0]+b*X[1],a*X[1]+b*X[0]-b*X[1])
    def adj(X): return (X[0].H,X[1].H)
    def total(items):
        out=f(O)
        for x in items:out=add(out,x)
        return out
    def feq(X,Y,name):
        eq(X[0],Y[0],name+'_constant');eq(X[1],Y[1],name+'_p')
    def tr(X): return (s.trace(X[0]),s.trace(X[1]))
    def teq(X,Y,name):
        eq(X[0],Y[0],name+'_constant');eq(X[1],Y[1],name+'_p')
    def sandwich(K,X): return mul(mul(K,X),adj(K))
    B=add(f(I),scale((-2,2),f(A2)))
    L={key:scale((0,-2),f(x.H*A)) for key,x in N.items() if key!=(0,0)}
    def row_channel(X): return total(sandwich(f(x.H),X) for x in N.values())
    def blank(X): return sandwich(B,X)
    def blank1(X): return scale((-4,8),sandwich(f(A2),X))
    def exits(X): return add(total(sandwich(k,X) for k in L.values()),blank1(X))
    def channel(X): return add(blank(X),exits(X))
    def exact_channel(X):
        anti=add(mul(f(A2),X),mul(X,f(A2)))
        return add(add(X,scale((-2,2),anti)),scale((4,-4),row_channel(sandwich(f(A),X))))
    rho=f((I+(C[0]+C[0].H)/5)/16)
    feq(channel(rho),exact_channel(rho),'literal128_Kraus_exact_Euler_Lindblad_channel')
    teq(tr(channel(rho)),tr(rho),'channel_trace_preserved')
    all_effect=add(add(mul(adj(B),B),total(mul(adj(k),k) for k in L.values())),
                   scale((-4,8),f(A2*A2)))
    feq(all_effect,f(I),'literal128_effect_completeness_as_operator')
    expected_exit=add(scale((4,-4),row_channel(sandwich(f(A),rho))),
                      scale((-8,12),sandwich(f(A2),rho)))
    feq(exits(rho),expected_exit,'tilted_exit_includes_negative_Delta_rho_Delta_term')
    require(any(x!=O for x in add(exits(blank(rho)),neg(blank(exits(rho))))),
            'blank_and_exit_maps_really_noncommute')
    # Complete port1, including blank-label/port1, has effect4p^3 A^2.
    port1=add(scale((0,1),total(sandwich(k,rho) for k in L.values())),blank1(rho))
    port1_effect=scale((-4,8),f(A2))
    teq(tr(port1),tr(mul(rho,port1_effect)),'all_port1_effect_four_p3_A2')
    exit_effect=add(f(I),neg(mul(B,B)))
    teq(tr(exits(rho)),tr(mul(rho,exit_effect)),'all_exit_effect_I_minus_B2')
    # n=2 full counting polynomial; all later outputs remain, no first-exit cut.
    c0=tr(blank(blank(rho)))
    c1=tuple(x+y for x,y in zip(tr(blank(exits(rho))),tr(exits(blank(rho)))))
    c2=tr(exits(exits(rho)))
    one=(s.Integer(1),s.Integer(0))
    teq(tuple(c0[k]+c1[k]+c2[k] for k in range(2)),one,'count_generating_polynomial_at_one')
    count=tuple(c1[k]+2*c2[k] for k in range(2))
    recursive=tuple(x+y for x,y in zip(tr(mul(rho,exit_effect)),
                                      tr(mul(channel(rho),exit_effect))))
    teq(count,recursive,'count_derivative_matches_all_round_channel_recursion')
    second=tuple(c1[k]+4*c2[k] for k in range(2))
    require(second!=count,'second_count_moment_not_first_exit_or_mean')
    first_exit=tuple(x+y for x,y in zip(tr(exits(rho)),tr(exits(blank(rho)))))
    require(count!=first_exit,'total_count_distinct_from_first_exit_probability')
    code_cost=tuple(2*one[k]+tr(mul(rho,port1_effect))[k]+
                      tr(mul(channel(rho),port1_effect))[k] for k in range(2))
    def port0_map(X):return add(blank(X),scale((1,-1),total(sandwich(k,X) for k in L.values())))
    def port1_map(X):return add(scale((0,1),total(sandwich(k,X) for k in L.values())),blank1(X))
    direct_cost=tuple(tr(port0_map(rho))[k]+2*tr(port1_map(rho))[k]+
        tr(port0_map(channel(rho)))[k]+2*tr(port1_map(channel(rho)))[k] for k in range(2))
    teq(direct_cost,code_cost,'two_round_original_code_cost_full_port_marginal')
    sigma1=I/10+(C[1]+C[1].H)/7+C[0]*C[0].H/11
    normalizer1=s.trace(sigma1)
    rho1=f((sigma1-normalizer1*rho[0])/16)
    def count_map(X):return tuple(x+y for x,y in zip(tr(exits(X)),tr(exits(channel(X)))))
    raw_count1=count_map(f(sigma1))
    quotient_count1=tuple((raw_count1[k]-normalizer1*count[k])/16 for k in range(2))
    teq(count_map(rho1),quotient_count1,'moving_preparation_count_source_normalizer_retained')
    require(tuple(raw_count1[k]/16 for k in range(2))!=quotient_count1,
            'hostile_frozen_count_normalizer_rejected')
    # Past/future factorization, two noncommuting nonblank marks and BOTH ports.
    nonzero=[(key,x) for key,x in L.items() if x!=f(O)]
    pair=next(((x,y) for key,x in nonzero for key2,y in nonzero
               if key!=key2 and mul(x,y)!=mul(y,x)),None)
    require(pair is not None,'two_noncommuting_real_marks_exist')
    x,y=pair
    reduced=sandwich(y,sandwich(x,blank(rho)))
    port_weights=((1,-1),(0,1))  # q_port=(p^2,p), originalcode mu=(p,p^2).
    for first in (0,1):
        for last in (0,1):
            full=scale(port_weights[last],sandwich(y,scale(port_weights[first],sandwich(x,blank(rho)))))
            expected=scale(port_weights[last],scale(port_weights[first],reduced))
            feq(full,expected,'full_past_future_port_factor_'+str(first)+str(last))
    # log_phi p=-1: actual conditional cost, information and action coefficients.
    p=s.Symbol('p')
    reduce=lambda x:s.rem(s.Poly(s.expand(x),p),s.Poly(p*p+p-1,p)).as_expr()
    eq(reduce(p*p+2*p),1+p,'original_mu_port_expected_code_cost')
    eq(reduce(-p*p+p),2*p-1,'original_mu_port_KL_is_p3_not_zero')
    eq(reduce(2*p*p+p),2-p,'port_Shannon_action_coefficient')
    eq(reduce((p*p+2*p)-(-p*p+p)),2-p,'port_cost_minus_Info_equals_Shannon')
    require(reduce(-p*p+p)!=0,'hostile_reversed_reference_KL_zero_rejected')
    # One actual Fourier block, phase i at role0; all16 and any reference survive.
    NF=rows([s.I*I,I,I,I]);AF=NF[(0,0)];h=s.Rational(1,4)
    DF=16*AF/h;lam=2*nu*nu/(h*h)
    eq(DF*DF,lam*I,'literal_flat_Fourier_Delta_scalar_on_full16')
    af2=s.simplify(s.trace(AF*AF)/16)
    eq(AF*AF,af2*I,'flat_A_squared_scalar')
    bf=(1-2*af2,2*af2)
    def scalar_mul(X,Y):return (X[0]*Y[0]+X[1]*Y[1],X[0]*Y[1]+X[1]*Y[0]-X[1]*Y[1])
    b2=scalar_mul(bf,bf);r=(1-b2[0],-b2[1])
    eps=(s.Rational(1,64)*h*h,-s.Rational(1,64)*h*h)
    teq(r,tuple(lam*eps[k]-lam*lam*scalar_mul(eps,eps)[k]/4 for k in range(2)),
        'flat_exit_Bernoulli_rate_epsilon_lambda_minus_quadratic')
    pb1=(-4*af2*af2,8*af2*af2)
    label_effect=(4*af2*(1-af2),-4*af2*(1-af2))
    teq(r,tuple(pb1[k]+label_effect[k] for k in range(2)),
        'special_blank_label_port1_plus_label_exits_is_total_exit')
    teq((-4*af2,8*af2),tuple(lam*scalar_mul((0,1),eps)[k] for k in range(2)),
        'flat_all_port1_rate_p_epsilon_lambda')
    require(pb1!=(-4*af2,8*af2),'blank1_not_all_port1')
    # Exact entropy algebra is conditional-probability chain rule, not spectral entropy.
    e,l=s.symbols('epsilon lambda',positive=True)
    x=e*l
    eq(-x*(s.log(e)+s.log(l))-(1-x)*s.log(1-x),
       s.log(1/e)*x-(1-x)*s.log(1-x)-e*l*s.log(l),
       'entropy_log_epsilon_coefficient_is_expected_all_exit_count')
    return {'status':'PASS','exact_checks':len(checks),'checks':checks,'source_pins':PINS,
      'carrier':{'Fock':16,'Julia_words':32,'row_outputs':64,'golden_outcomes':128,
                 'dark_duplicate_outcomes':64,'reference_retained_by_tensor_identity':128},
      'channel':'Phi(rho)=rho-alpha{Delta,rho}+2alpha T(D rho D), T(X)=sum N_j^* X N_j',
      'tilted_exit':'epsilon T(D rho D)-epsilon^2 Delta rho Delta/4; epsilon=2alpha',
      'original_port_reference':['p','p^2'],'nonblank_conditional_port_probability':['p^2','p'],
      'port_coefficients':{'Cost':'1+p','Info':'p^3','Cost_minus_Info':'2-p'},
      'flat':{'lambda':str(lam),'h':str(h),'full128_record_count':'n rounds, not first exit'},
      'scope':{'old_runs_executed':False,'new_price_selected':False,'physical_admission_proved':False,
               'continuum_entropy_source_limit_proved_by_fixture':False,'prepared_probability_replaces_full_Z':False}}

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
