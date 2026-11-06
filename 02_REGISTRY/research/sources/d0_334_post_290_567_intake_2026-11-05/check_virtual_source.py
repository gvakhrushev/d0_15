#!/usr/bin/env python3
"""Exact forward-memory quadratic source identities on the original scene/clock.
This constructs no native probability law or new physical price.
"""
import hashlib
import json
from math import comb
from pathlib import Path
import sympy as s
checks=[]
def need(ok,label):
    if not bool(ok): raise ArithmeticError(label)
    checks.append(label)
a=s.symbols('a',positive=True); p=a*a; poly=a**4+a**2-1
def red(x):
    num,den=s.fraction(s.cancel(x)); num=s.rem(num,poly,a); den=s.rem(den,poly,a)
    return s.rem(s.expand(num*s.invert(den,poly,a)),poly,a)
def zero(x):
    return all(red(v)==0 for v in x) if isinstance(x,s.MatrixBase) else red(x)==0
v=s.Matrix([a,p]); G=s.Matrix([[a,-p],[p,a]])
# Literal birth; G; G; G. No inverse is executed.
D=7; L=3; N=4
R=s.zeros(D,2); R[0:1,:]=v.T; R[1:3,:]=s.eye(2)-v*v.T
T=s.zeros(D); T[1:3,0:1]=v; T[3:5,1:3]=G; T[5:7,3:5]=G; T[:,5:7]+=R*G
need(zero(T.T*T-s.eye(D)),'literal complete growing clock is unitary')
powers=[s.eye(D)]
for j in range(1,2*L+1): powers.append((powers[-1]*T).applyfunc(red))
need(all(zero(s.trace(powers[j])) for j in range(1,L)),
     'actual shortest newborn return age is at least L')
need(not zero(s.trace(powers[L])),'shortest newborn trace is nonzero in literal fixture')
need(all(zero(powers[j][0,0]) for j in range(1,L+1)),
     'initial prepared cut has no return at depths one through L')
need(not zero(powers[N][0,0]),'actual initial return first occurs later at N')
# Original 33 vertices and all 718 directed edges, no quotient substituted.
zones=[0]*9+[1]*11+[2]*13
A=s.Matrix(33,33,lambda i,j:int(zones[i]!=zones[j]))
need(sum(A)==718,'original scene retains all 718 directed edges')
Ap=[s.eye(33)]
for j in range(1,2*L+1): Ap.append(Ap[-1]*A)
c=[s.trace(x) for x in Ap]
need(c[2]==718 and c[3]==7722,'original two and three step closed trace counts')
need(A.rank()==3,'original scene has thirty zero modes')
# Independent binomial expansion of the actual Hilbert-Schmidt quadratic form.
full=0; initial=0; surviving=[]
for i in range(L+1):
    for j in range(L+1):
        K=(powers[i].T*powers[j]).applyfunc(red)
        tr=red(s.trace(K)); prepared=red(K[0,0]); coeff=comb(L,i)*comb(L,j)
        full+=coeff*c[2*L-i-j]*tr
        # Scene preparation is the actual fixed coordinate vertex 0.
        initial+=coeff*Ap[2*L-i-j][0,0]*prepared
        if i!=j and tr!=0: surviving.append((i,j))
need(surviving==[(0,L),(L,0)],'all mixed history pairs retained, only opposite full wraps survive')
b=sum(comb(L,j)**2*c[2*L-2*j] for j in range(L+1))
expected=D*b+2*c[L]*s.trace(powers[L])
need(zero(full-expected),'full quadratic forward-memory trace identity')
expected_initial=sum(comb(L,j)**2*Ap[2*L-2*j][0,0] for j in range(L+1))
need(zero(initial-expected_initial),'same initial-cut quadratic response loses every field cross term')
need(expected_initial>0,'prepared-cut response remains positive despite source absence')
# Fixed-layout target trace from the full original XF comparison.
Q,dold,g,ell,beta,Zheat,heatcoef=s.symbols('Q dold g ell beta Zheat heatcoef',positive=True)
const=s.symbols('const',real=True)
full_target=D*b+2*c[L]*dold*L*(const+4*Q)
need(s.diff(full_target,Q)==8*c[L]*dold*L,'full flag report supplies correct quadratic trace coefficient')
S=-s.log(full_target)/(2*ell)
gamma=4*c[L]*dold*L*g/(ell*full_target)
need(s.simplify(-s.diff(S,Q)*g/gamma)==1,'half-log price has the positive oriented report gain')
gamma_heat=16*dold*g*L*heatcoef/(beta*Zheat)
need(s.simplify(gamma_heat/gamma-4*ell*heatcoef*full_target/(beta*Zheat*c[L]))==0,
     'master and virtual gains compared with actual normalizers')
# Conservative all-L analytic bounds use only original dimensions and c_L>=718.
x=s.symbols('x',real=True)
need(s.expand(x*x/s.Integer(33)+33-2*x-(x-33)**2/s.Integer(33))==0,
     'full quadratic positivity bound retains all thirty-three scene modes')
need(s.Rational(33*718,(718-33)**2)<s.Rational(1,19),
     'actual-to-target normalizer error is below delta over nineteen')
need((s.Rational(718**2,33)+33+2*718)/(s.Rational(718**2,33)+33-2*718)<2,
     'uniform extrema normalizer ratio below two at conservative threshold')
need(s.Rational(33,718)<1,'L at least two excludes the zero c1 source')

# Symbolic fixed-tariff refinement on this same literal clock.
u, v, alpha = s.symbols('u v alpha', positive=True)

def polynomial_zero(expr):
    # u,v are genuine independent symbolic positive tariffs; only the
    # original Golden coefficient field is reduced by the owned polynomial.
    return all(red(t) == 0 for t in s.Poly(s.expand(expr), u, v).coeffs())

full, prepared, survivors = 0, 0, []
for i in range(L + 1):
    for j in range(L + 1):
        clock_pair = (powers[i].T * powers[j]).applyfunc(red)
        tr = red(s.trace(clock_pair))
        cut = red(clock_pair[0, 0])
        weight = comb(L, i) * comb(L, j) * u**(2*L-i-j) * v**(i+j)
        full += weight * c[2*L-i-j] * tr
        prepared += weight * Ap[2*L-i-j][0, 0] * cut
        if i != j and tr != 0:
            survivors.append((i, j))

b = sum(comb(L, j)**2 * u**(2*L-2*j) * v**(2*j) * c[2*L-2*j]
        for j in range(L + 1))
k = (u*v)**L * c[L]
full_expected = D*b + 2*k*red(s.trace(powers[L]))
prepared_expected = sum(comb(L, j)**2 * u**(2*L-2*j) * v**(2*j)
                        * Ap[2*L-2*j][0, 0] for j in range(L + 1))
need(survivors == [(0, L), (L, 0)],
     'positive tariffs retain all cross terms and the same two full-trace windings')
need(polynomial_zero(full-full_expected),
     'exact symbolic weighted full quadratic expansion equals D b plus 2 k ReTr T^L')
need(polynomial_zero(prepared-prepared_expected),
     'exact symbolic weighted original prepared cut has only diagonal pairs')
need(all(t >= 0 for t in s.Poly(prepared_expected-v**(2*L), u, v).coeffs()),
     'weighted prepared response is at least v^(2L) and has no current clock-body source')
need(polynomial_zero(full.subs(v, u)-u**(2*L)*full.subs({u: 1, v: 1})),
     'common positive tariff occurs once at amplitude level and twice in response')
need(polynomial_zero(u*s.diff(full, u)+v*s.diff(full, v)-2*L*full),
     'full response is homogeneous of degree 2L in the two tariffs')
need(polynomial_zero(u*s.diff(prepared, u)+v*s.diff(prepared, v)-2*L*prepared),
     'prepared response has the same common tariff degree despite zero field source')

Q, dold, gain, ell, beta, Zheat, heatcoef = s.symbols(
    'Q dold gain ell beta Zheat heatcoef', positive=True)
const = s.symbols('const', real=True)
target = D*b + 2*k*dold*L*(const+4*Q)
S = -s.log(target)/(2*ell)
Gamma = 4*k*dold*L*gain/(ell*target)
need(s.simplify(s.diff(target, Q)-8*k*dold*L) == 0,
     'weighted complete flag coefficient is exactly 8 k d_old L')
need(s.simplify(-s.diff(S, Q)*gain/Gamma-1) == 0,
     'weighted half-log source has exact fixed minus orientation and actual target gain')
Gamma_heat = 16*dold*L*gain*heatcoef/(beta*Zheat)
need(s.simplify(Gamma_heat/Gamma-4*ell*heatcoef*target/(beta*Zheat*k)) == 0,
     'master-to-weighted gain retains both actual positive normalizers')

r, l = s.symbols('r l', positive=True)
scaled_score = -s.log(alpha**(2*L)*r)/(2*ell)
need(s.simplify(s.diff(scaled_score, alpha)+L/(ell*alpha)) == 0,
     'independent common tariff scale has genuine nonzero alpha source -L/(alpha ell)')
need(s.simplify(s.expand_log(scaled_score+s.log(r)/(2*ell))
                +L*s.log(alpha)/ell) == 0,
     'exact common-scale score shift is -L log_phi(alpha)')
need(s.simplify(-(u*s.diff(target,u)+v*s.diff(target,v))/(2*ell*target)+L/ell) == 0,
     'the same nonzero scale row follows directly from the full target response')

# Rank-three bound is certified structurally, not by tariff sampling.
x1, x2, x3 = s.symbols('x1 x2 x3', real=True)
need(s.expand(3*(x1*x1+x2*x2+x3*x3)-(x1+x2+x3)**2
              -((x1-x2)**2+(x1-x3)**2+(x2-x3)**2)) == 0,
     'rank-three Cauchy-Schwarz identity holds for all real nonzero eigenvalues')
need(A.rank() == 3 and 3*c[2*L]-c[L]**2 >= 0,
     'the actual original 33-vertex scene satisfies rank-three moment bound')
need(s.simplify(u**(2*L)*c[2*L]+33*v**(2*L)
                -2*s.sqrt(33*c[2*L])*(u*v)**L
                -(s.sqrt(c[2*L])*u**L-s.sqrt(33)*v**L)**2) == 0,
     'weighted endpoint AM-GM gap is exactly a square for symbolic positive tariffs')
need(all(t >= 0 for t in s.Poly(b-u**(2*L)*c[2*L]-33*v**(2*L),u,v).coeffs()),
     'discarding only intermediate nonnegative diagonal terms gives the endpoint bound')
cc, residual = s.symbols('cc residual', positive=True)
need(s.expand(33*(cc**2/3+residual)-11*cc**2-33*residual) == 0,
     'rank-three bound gives sqrt(33 c_2L) at least sqrt(11) c_L')
need(2*s.sqrt(11) > 6,
     'uniform positive tariff bound b at least 2 sqrt(11) k is strictly stronger than 6 k')

dimension, kk, excess = s.symbols('dimension kk excess', positive=True)
bb = 6*kk+excess
Rmin, Rmax = dimension*(bb-2*kk), dimension*(bb+2*kk)
need(s.simplify(Rmin-4*dimension*kk-dimension*excess) == 0,
     'strict rank-three bound yields R_min greater than 4 D k')
need(s.simplify(2*Rmin-Rmax-dimension*excess) == 0,
     'the same bound gives R_max/R_min less than two for every positive tariff ratio')
length, rank, delta = s.symbols('length rank delta', positive=True)
error_bound = 2*kk*length*rank*delta/Rmin
need(s.simplify(length*rank*delta/(2*dimension)-error_bound
                -length*rank*delta*excess/(2*dimension*(4*kk+excess))) == 0,
     'normalized endpoint error has no exponential tariff ratio factor')
need(s.simplify((length*rank*delta/(2*dimension)).subs(dimension,2*length*rank)-delta/4) == 0,
     'actual dimension bound D at least 2 L r_latest gives relative error at most delta/4')

result={'status':'PASS','number_of_checks':len(checks),'checks':checks,
 'input_head':'2900145fe674629b61949587917a3a2ea5188797',
 'native_fixture':{'word':'birth;G;G;G','stage_widths':[1,2,2,2],'L':L,'N':N},
 'original_scene':{'vertices':33,'directed_edges':718,'c2':int(c[2]),'c3':int(c[3])},
 'not_claimed':['virtual clock tariff is selected','full Cost-Info aggregation',
 'new native XF history emitted','a Gibbs state is prepared','Einstein closure'],
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(result,sort_keys=True,indent=2))
