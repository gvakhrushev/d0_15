"""An exact rank-two native mark and two physically capped Golden stopping registers.

Run python3 check_query_clocks.py; JSON is written to stdout. Needs SymPy, mpmath.
All target, clock and mass arithmetic is exact. Decimal displays of logarithms
use 115 decimal places internally. The error bounds use only 0 <= F <= I.
"""
from fractions import Fraction as Fr
import json
import mpmath as mp
import sympy as sp
from sympy.polys.matrices import DomainMatrix

mp.mp.dps = 115
N, L, rank = 6, 48, 2
z, eta = Fr(1,2**20), Fr(15,16)
scale = 4*rank*z/eta
p_symbol = (sp.sqrt(5)-1)/2
sqrt_p = sp.sqrt(p_symbol)
field = sp.QQ.algebraic_field(sqrt_p)
p_num = (mp.sqrt(5)-1)/2

# Exact Q(p) as a rational pair x+y*p, p^2=1-p.
def q(x): return (Fr(x),Fr(0))
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
def times(x,c): return (x[0]*c,x[1]*c)
def mul(x,y):
    return (x[0]*y[0]+x[1]*y[1], x[0]*y[1]+x[1]*y[0]-x[1]*y[1])
def divide(x,y):
    conjugate = (y[0]-y[1],-y[1])
    norm = mul(y,conjugate)
    assert norm[1] == 0 and norm[0] != 0
    return times(mul(x,conjugate),1/norm[0])
def power(x,n):
    out = q(1)
    for _ in range(n): out = mul(out,x)
    return out
def sign(v):
    # 2*(x+y*p) = (2*x-y)+y*sqrt(5), compare by exact squaring.
    k,y = 2*v[0]-v[1],v[1]
    if k*y >= 0:
        u=k or y
        return (u>0)-(u<0)
    t=k*k-5*y*y
    return (1 if k>0 else -1)*((t>0)-(t<0))
def as_q(value):
    # Reduce the exact quartic calculation to its even subfield Q(p).
    c = list(reversed(value.to_list())) + [0]*4
    assert c[1]==0 and c[3]==0
    def rational(t): return Fr(int(t.numerator),int(t.denominator)) if t else Fr(0)
    return (rational(c[0]),rational(c[2]))
def approx(x):
    def real(f): return mp.mpf(f.numerator)/f.denominator
    return real(x[0])+p_num*real(x[1])
def display(x): return mp.nstr(x,44)
def dm(x): return DomainMatrix.from_Matrix(x).convert_to(field).to_sparse()
def sum_q(values):
    out = q(0)
    for v in values: out=add(out,v)
    return out

p = (Fr(0),Fr(1))
a,b,m = [power(p,i) for i in (2,4,3)]
rho = add(a,b)
one = q(1)
cap_tail = power(a,L)
M = add(m,mul(sub(one,m),cap_tail))
M2 = mul(M,M)
# Coupling: all retained timely hits have exactly the same law up to a scalar.
timeout_probability = divide(cap_tail,M)
eps_q = sub(one,power(sub(one,timeout_probability),2))
simple_eps_q = divide(times(cap_tail,2),m)
assert sign(sub(simple_eps_q,eps_q)) >= 0
clock_error = times(eps_q,scale)
series_error = rank*z**(N+1)/((N+1)*(1-z))
assert sign(sub(clock_error,q(series_error))) > 0
threshold_weight = [mul(a,power(a,k)) for k in range(2*L-1)]
raw_atom = [mul(b,power(a,i)) for i in range(L)] + [cap_tail]
assert sum_q(raw_atom)==M

G = sp.Matrix([[sqrt_p,-p_symbol],[p_symbol,sqrt_p]])
cx = sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
J = dm(sp.eye(8)[:,[0,2]])
P = J*J.transpose()
I8 = dm(sp.eye(8))
G_environment = dm(sp.kronecker_product(G,sp.eye(4)))
G_bath = dm(sp.kronecker_product(sp.eye(4),G))
CX_environment = dm(sp.kronecker_product(cx,sp.eye(2)))
previous_marks = ["0.22748052996517557","0.22503768490011192","0.18120261840140084"]

def target(e,bx):
    U = (CX_environment*(G_environment**e))**2 * G_bath**(2*bx)
    assert U.transpose()*U == I8
    F = J.transpose()*U.transpose()*(I8-P)*U*J
    assert F[0,1].element != field.zero
    def trace(M): return as_q(M[0,0].element+M[1,1].element)
    traces = [trace(F**n) for n in range(1,N+1)]
    finite = sum_q(times(t,z**n/n) for n,t in enumerate(traces,1))
    mark = times(finite,1/scale)
    determinant = as_q((dm(sp.eye(2))-F*field.from_sympy(sp.Rational(z.numerator,z.denominator))).det())
    # Independent analytic spectrum from the Golden/CNOT circuit.
    def double_sine2(t):
        entry=(dm(G)**(2*t))[1,0].element
        return as_q(entry*entry)
    u=double_sine2(bx)
    v=sub(one,mul(sub(one,u),sub(one,double_sine2(e))))
    assert add(u,v)==traces[0] and mul(u,v)==as_q(F.det())
    for n,t in enumerate(traces,1): assert add(power(u,n),power(v,n))==t
    determinant_oracle=mul(sub(one,times(u,z)),sub(one,times(v,z)))
    assert determinant == determinant_oracle
    exact = -mp.log1p(approx(sub(determinant,one)))
    return mark, finite, exact

def run_clocks(target_yes):
    # Infinite shell k has k+1 atoms w=a*a^k and their total is one.
    # Later shells have total/w = a*((k+2)/(1-a)+a/(1-a)^2) >= 1.
    # A greedy unsaturated shell leaves < w; a saturated shell leaves no
    # more than the remaining total. Therefore the infinite code is exact.
    # Every finite pair uses one of these first 2L-1 exact shell digits.
    remainder = target_yes
    digits = []
    for k,w in enumerate(threshold_weight):
        count = 0
        while count<k+1 and sign(sub(remainder,times(w,count+1)))>=0: count+=1
        remainder = sub(remainder,times(w,count))
        assert sign(remainder)>=0
        assert count==k+1 or sign(sub(w,remainder))>0
        digits.append(count)
    yes = q(0)
    split_cost = q(0)
    timed_out = q(0)
    for i,wi in enumerate(raw_atom):
        for j,wj in enumerate(raw_atom):
            h=mul(wi,wj)
            ready=(i<L and j<L)
            flag=ready and i<digits[i+j]
            if flag: yes=add(yes,h)
            if not ready: timed_out=add(timed_out,h)
            split_cost=add(split_cost,h if flag else mul(h,rho))
    trim = q(0)
    for k in range(2*L-1):
        lo=max(0,k-L+1)
        hi=min(k,L-1,digits[k]-1)
        trim=add(trim,times(mul(mul(b,b),power(a,k)),max(0,hi-lo+1)))
    assert trim==yes and divide(timed_out,M2)==eps_q
    Q=divide(yes,M2)
    assert split_cost==mul(M2,add(rho,mul(sub(one,rho),Q)))
    recovered=divide(sub(divide(split_cost,M2),rho),sub(one,rho))
    assert recovered==Q and sign(sub(target_yes,Q))>=0
    assert sign(sub(eps_q,sub(target_yes,Q)))>=0
    return split_cost,Q,times(sub(one,recovered),scale),digits

rows=[]
results=[]
for (e,bx),previous in zip([(1,1),(3,1),(1,3)],previous_marks):
    mark,finite,exact=target(e,bx)
    assert abs(approx(mark)-mp.mpf(previous))<mp.mpf("6e-17")
    paid,Q,reconstructed,digits=run_clocks(sub(one,mark))
    assert sign(sub(reconstructed,finite))>=0 and sign(sub(clock_error,sub(reconstructed,finite)))>=0
    assert 0 < exact-approx(finite) <= approx(q(series_error))
    results.append((finite,reconstructed,exact))
    rows.append(dict(word=[e,bx],mark=display(approx(mark)),target_yes=display(1-approx(mark)),
                     Q_L=display(approx(Q)),raw_Z=display(approx(paid)),digits=digits,
                     J6=display(approx(finite)),J_exact_logdet=display(exact),
                     J_from_raw_Z=display(approx(reconstructed)),
                     clock_error=display(approx(sub(reconstructed,finite))),
                     tail_J_exact_minus_J6=display(exact-approx(finite))))
contrasts=[]
for name,i in [("e: (3,1)-(1,1)",1),("b: (1,3)-(1,1)",2)]:
    f0,c0,j0=results[0]; fi,ci,ji=results[i]
    dc=approx(sub(ci,c0)); df=approx(sub(fi,f0)); dj=ji-j0
    previous=(mp.mpf(previous_marks[i])-mp.mpf(previous_marks[0]))*approx(q(scale))
    assert abs(df-previous)<mp.mpf("1e-21")
    assert abs(dc-df)<=approx(clock_error)
    assert abs(dc-dj)<=approx(add(clock_error,q(series_error)))
    contrasts.append(dict(variation=name,J6=display(df),J_exact_logdet=display(dj),
                          reconstructed=display(dc),previous_mark_contrast_rescaled=display(previous),
                          absolute_error_vs_logdet=display(abs(dc-dj))))
print(json.dumps(dict(status="PASS",rank=rank,depth=N,cap_each=L,z=str(z),eta=str(eta),
    underlying_clock="hit i<L has raw mass p^4*(p^2)^i; timeout i=L has mass (p^2)^L; either timeout means false",
    greedy_code="atom (i,j) selected iff neither timer times out and i < d_(i+j); infinite shell k has k+1 atoms p^2*(p^2)^k, and the later total is at least one such atom",
    full_clock_mass=display(approx(M)),joint_mass_before_final_split=display(approx(M2)),
    universal_bounds=dict(clock_event="0 <= s-Q_L <= 1-(1-(p^2)^L/M_L)^2 <= 2*(p^2)^L/p^3",
                          clock_event_bound=display(approx(eps_q)),
                          clock_J6=display(approx(clock_error)),positive_logdet_tail=display(approx(q(series_error))),
                          contrast_vs_exact=display(approx(add(clock_error,q(series_error)))),
                          contrast_rule="Jcalc-J in [-tail,clock]; differences bounded by clock+tail"),
    settings=rows, contrasts=contrasts,
    all_floors_certified_in="Q(sqrt(5))", source_price_bound=False),indent=2))
