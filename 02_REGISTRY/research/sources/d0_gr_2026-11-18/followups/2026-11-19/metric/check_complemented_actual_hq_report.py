"""Exact scalar writer + actual Hq moment/report; bounded conditional scope."""
from itertools import product
from fractions import Fraction as F
import json, math
import sympy as S
import mpmath as mp

P=S.symbols('p', real=True)
p=(S.sqrt(5)-1)/2
N=4
coords=list(product(range(4),repeat=N))
unit=((1,0),(0,1),(-1,0),(0,-1))
ds=list(product((0,1),repeat=2))
fields={d:{x:unit[(x[1]+d[0]*x[0]+d[1]*x[2])%4] for x in coords} for d in ds}
table={}
for d,e in product(ds,repeat=2):
    total=F(0)
    for x in coords:
        for mu in range(4):
            nxt=list(x);nxt[mu]=(nxt[mu]+1)%4;nxt=tuple(nxt)
            da=[fields[d][nxt][i]-fields[d][x][i] for i in range(2)]
            db=[fields[e][nxt][i]-fields[e][x][i] for i in range(2)]
            # e=4I, h=1/4: g^mumu*(forward derivative)^2 = eta_mumu.
            # F=q/(2 A^2), SITE measure 1/256.
            total+=F((1 if mu==0 else -1)*sum(a*b for a,b in zip(da,db)),2*256)
    table[d,e]=total
    expected=(F(-(1+d[1]-d[0])) if d==e else F(0))
    if total!=expected: raise AssertionError((d,e,total,expected))

s,t,s1,t1,s2,t2=S.symbols('s t s1 t1 s2 t2',real=True)
weight=lambda d,x,y:(x if d[0] else 1-x)*(y if d[1] else 1-y)
F2=S.expand(sum(S.Rational(v.numerator,v.denominator)*weight(d,s1,t1)*weight(e,s2,t2) for (d,e),v in table.items()))
Fexpected=-((1-s1)*(1-s2)*((1-t1)*(1-t2)+2*t1*t2)+s1*s2*t1*t2)
assert S.expand(F2-Fexpected)==0
Fd=S.expand(F2.subs({s1:s,s2:s,t1:t,t2:t}))
assert S.expand(Fd-(-S.Rational(3,4)+S.Rational(3,2)*s-s*s)).subs(t,S.Rational(1,2))==0
assert Fd.subs({s:S.Rational(1,2),t:S.Rational(1,2)})==-S.Rational(1,4)
assert S.diff(Fd,s).subs({s:S.Rational(1,2),t:S.Rational(1,2)})==S.Rational(1,2)
assert S.diff(Fd,t).subs({s:S.Rational(1,2),t:S.Rational(1,2)})==-S.Rational(1,2)
assert S.simplify(2*(Fd.subs({s:p,t:S.Rational(1,2)})-Fd.subs({s:p**2,t:S.Rational(1,2)}))-p**3)==0
# Effective program basis spectrum after both actual complemented H outcomes.
prob=lambda b: p**2+p**3*b
spect=[]
for bits in product((0,1),repeat=4):
    spect.append(S.simplify(F2.subs(dict(zip((s1,t1,s2,t2),map(prob,bits))))))
lo=S.simplify(F2.subs({s1:p**2,t1:p,s2:p**2,t2:p}))
hi=S.simplify(F2.subs({s1:p,t1:p**2,s2:p,t2:p**2}))
assert all(float(S.N(x-lo,20))>=-1e-15 and float(S.N(hi-x,20))>=-1e-15 for x in spect)
assert S.simplify(hi-lo-2*(18*p-11))==0
# Complete report probability of actual 2+8-sign owner, f=0.
mp.mp.dps=80
pp=(mp.sqrt(5)-1)/2
ell=mp.log(1/pp);A=pp*mp.sin(712*mp.asin(pp)); A2=A*A
z=mp.mpf(2)**-20;Lam=mp.mpf(1) # illustrative, physical norm bound not measured
L=4*pp**3
r=lambda y:1-(1-z*4*(pp+pp**2*y)**2*(1-(pp+pp**2*y)**2))*(1-z*(L+(1-L)*4*(pp+pp**2*y)**2*(1-(pp+pp**2*y)**2)))
rp=lambda y:mp.diff(r,y)
qstar=-A2/2; ystar=qstar/(64*Lam); rstar=r(ystar); rzero=r(mp.mpf(0))
assert rp(-mp.mpf(1)/64)>0 and rp(mp.mpf(1)/64)>0
C=rzero-rstar
assert C>0
# One actual recorded descriptor H is uniform at the P=|+> centre. For
# first T-sign, conditioning it produces two different pair moments; the
# exact multicopy report is multiaffine in eight independent sign means.
rH0=rstar-C/2;rH1=rstar+C/2
assert 0<rH0<rstar<rH1<1
# Reconstruct the ACTUAL 2+8-sign processor as a multiaffine polynomial
# of its independently supplied Hq sign means, not as eight reused signs.
v=S.symbols('v'); zz=S.Rational(1,2**20); ee=S.Rational(1,64)
B=lambda w:4*w*w*(1-w*w)
Lsym=4*p**3; u=p+p**2*ee*v; b=B(u)
rpoly=S.Poly(S.expand(zz*(b+Lsym+(1-Lsym)*b)-zz**2*b*(Lsym+(1-Lsym)*b)),v)
assert rpoly.degree()==8
coeff=[mp.mpf(str(S.N(rpoly.nth(k),80))) for k in range(9)]
tstar=qstar/Lam
multiaffine=lambda means:sum(coeff[k]*mp.fprod(means[:k]) for k in range(9))
assert abs(multiaffine([tstar]*8)-rstar)<mp.mpf('1e-75')
tH0=-3*A2/(4*Lam);tH1=-A2/(4*Lam)
assert abs(multiaffine([tH0]+[tstar]*7)-rH0)<mp.mpf('1e-75')
assert abs(multiaffine([tH1]+[tstar]*7)-rH1)<mp.mpf('1e-75')
# Conservative analytic bound for the actual report's y derivative on
# [-1/64,1/64], using p in (309/500,619/1000), u in (0.612,0.625).
assert 4*(2*F(619,1000)-1)<1
assert 8*F(381,1000)*F(612,1000)*(1-2*F(5,8)**2)>F(2,5)
h=lambda x:-x*mp.log(x)-(1-x)*mp.log(1-x)
I_exact=h(rstar)-(h(rH0)+h(rH1))/2
assert I_exact>0 and I_exact>=C*C/2
# Strict inequalities are witnessed for actual admissible end states.
Ffun=S.lambdify((s,t),Fd,'mpmath'); ss0=pp**2;ss1=pp
q0=2*A2*Ffun(ss0,mp.mpf('.5'));q1=2*A2*Ffun(ss1,mp.mpf('.5'))
assert mp.almosteq(q1-q0,A2*pp**3)
r0=r(q0/(64*Lam));r1=r(q1/(64*Lam))
assert r1>r0
# Relative FQ weights for all 32 descriptor/complement pairs are p^32;
# full physical code length 3 per pair gives p^96, and final fixed 0/10
# report adds p^(1+R): p^97[1-p^2 r]. This is an explicit model only.
res={'status':'PASS','site_count':len(coords),'descriptor_pair_cases':len(table),
 'mean_q_over_2A_squared_distinct_descriptors':'zero',
 'mean_q_over_2A_squared_equal_descriptors':{str(d):str(table[d,d]) for d in ds},
 'four_program_effect_spectrum_over_2A_squared':[str(x) for x in spect],
 'four_program_effect_gap_over_2A_squared':str(S.simplify(hi-lo)),
 'central_moment_over_2A_squared':str(Fd.subs({s:S.Rational(1,2),t:S.Rational(1,2)})),
 'central_partial_s':str(S.diff(Fd,s).subs({s:S.Rational(1,2),t:S.Rational(1,2)})),
 'central_partial_t':str(S.diff(Fd,t).subs({s:S.Rational(1,2),t:S.Rational(1,2)})),
 'actual_endpoints_q_difference':'A^2*p^3',
 'writer_complement_pairs_for_16_global_CAR_copies':32,
 'relative_descriptor_pair_weight':'p^32; all actual H/Q histories retained',
 'absolute_descriptor_code_weight_only':'p^96',
 'model_final_code_weight':'p^97*(1-p^2*r)',
 'physical_Lambda_not_measured_and_numerics_Lambda_1_only':True,
 'illustrative_A_squared':mp.nstr(A2,30),'illustrative_r0':mp.nstr(rzero,30),
 'illustrative_report_difference_endpoints':mp.nstr(r1-r0,30),
 'illustrative_central_h_r_covariance':mp.nstr(C/4,30),
 'illustrative_mutual_information_nats':mp.nstr(I_exact,30),
 'mutual_information_lower_bound':'(r(0)-r(qstar/(64 Lambda)))^2/2 nats',
 'full_Hq_gate_compilation_and_Geometric_bank':False,
 'complete_book03_cost_and_clock':False,'GR_closed':False}
print(json.dumps(res,indent=2,sort_keys=True))
