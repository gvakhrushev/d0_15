#!/usr/bin/env python3
"""NEW bounded reconstruction checks, 2026-10-21; not a recovered old checker.
Requires Python3, SymPy, mpmath. No repository mutations, full128 rank replay,
or physical Book Info/admission inference. All results are computed afresh.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse, hashlib, json, math, time
import sympy as s
import mpmath as mp

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, help='Explicit optional result path; default prints JSON without writes')
args = parser.parse_args()
mp.mp.dps = 70
phi = (1+mp.sqrt(5))/2
p = 1/phi
lnphi = mp.log(phi)
g = p+2*p*p
checks = []

def check(name, truth, **data):
    if not bool(truth):
        raise AssertionError(name)
    checks.append(dict(name=name, status='PASS', **data))

def zero(expr):
    return s.simplify(expr) == 0

def a(j):
    return s.Rational(math.comb(2*j,j), 4**j)

started = time.monotonic()
x = s.symbols('x', real=True)
# Group 1: exact finite stopped laws and means, not hidden cost-cut conditioning.
for N in range(1,7):
    mu = sum(a(j)*(1-x)**j for j in range(N))
    f = x*mu
    failure = sum(a(n-1)*(1-x)**n/(2*n) for n in range(1,N+1))
    unresolved = a(N)*(1-x)**N
    derivative = sum(a(j)*(1-x)**j/2 for j in range(N-1)) + N*a(N-1)*(1-x)**(N-1)
    check(f'sampler_normalized_N{N}', zero(f+failure+unresolved-1))
    check(f'sampler_positive_derivative_formula_N{N}', zero(s.diff(f,x)-derivative))
    for x0 in (F(0), F(1,5), F(3,7), F(1)):
        # Explicit stopped binary event tree. This tests success/clock only;
        # full17 labels are enumerated separately below at N=1.
        leaves=[]
        def visit(n, w):
            if w*x0:
                leaves.append(('SUCCESS',n,w*x0))
            miss=w*(1-x0)
            if miss:
                leaves.append(('FAILURE',n,miss/F(2*n)))
                cont=miss*(1-F(1,2*n))
                if n==N:
                    leaves.append(('UNRESOLVED',n,cont))
                else:
                    visit(n+1,cont)
        visit(1,F(1))
        exactx=s.Rational(x0.numerator,x0.denominator)
        total=sum(w for _,_,w in leaves)
        succ=sum(w for tag,_,w in leaves if tag=='SUCCESS')
        calls=sum(n*w for _,n,w in leaves)
        check(f'sampler_tree_N{N}_x{x0}', total==1 and s.Rational(succ)==f.subs(x,exactx)
              and s.Rational(calls)==mu.subs(x,exactx))

# Group 2: Golden arithmetic and finite-bank exact conditional fairness.
ps=(s.sqrt(5)-1)/2
check('golden_units', zero(ps+ps**2-1) and zero(ps+2*ps**2-(2-ps)))
for d in (2,4,6,8,10,12,24):
    m=(d-1).bit_length()
    accepted=Counter()
    for raw in product((0,1),repeat=2*m):
        pairs=list(zip(raw[::2],raw[1::2]))
        if not all(u!=v for u,v in pairs):
            continue
        code=0
        for u,v in pairs:
            code=2*code+u
        if code<d:
            accepted[code]+=1
            check(f'bank_d{d}_accepted_code{code}_equal_raw_cost',
                  sum(1 if bit else 2 for bit in raw)==3*m)
    check(f'bank_exact_uniform_d{d}', accepted==Counter({j:1 for j in range(d)}))

# Group 3: source-owned original SO basis, rational noncommutative plaquette,
# component polarization and three exact Lorentz-reference controls.
I=s.eye(4); E=lambda i,j:I[:,i]*I[j,:]
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
G=[E(1,2)+E(2,0),E(1,3)+E(3,0),E(0,2)+E(2,1),E(0,3)+E(3,1),E(2,3)-E(3,2),E(1,1)-E(0,0)]
invL=lambda M:eta*M.T*eta
fro=lambda A,B:s.trace(A.T*B)
check('original_six_eta_skew_and_orthogonal', all(invL(A)==-A for A in G)
      and s.Matrix([[fro(A,B) for B in G] for A in G])==2*s.eye(6))
def nil(A,t):
    if A**3!=s.zeros(4):
        raise AssertionError('nilpotent reference requires A^3=0')
    return I+t*A+t*t*A*A/2
def plaquette(t,u):
    return nil(G[0],t)*nil(G[3],u)*nil(G[0],-t)*nil(G[3],-u)
P1=plaquette(s.Rational(1,5),s.Rational(1,4))
Q1=plaquette(s.Rational(1,6),s.Rational(1,3))
R=lambda M:(M-invL(M))/2
check('noncommuting_plaquette_exact_SO', P1.T*eta*P1==eta and R(P1)!=s.zeros(4))
check('component_projection_exact', R(P1)==sum((fro(A,P1)*A/2 for A in G),s.zeros(4)))
check('component_polarization_exact', sum(fro(A,P1)*fro(A,Q1)/2 for A in G)==fro(R(P1),R(Q1)))
refs=[('nilpotent',G[0],s.Rational(1,7),nil(G[0],s.Rational(1,7))),
      ('rotation',G[4],s.Rational(3,5), I+s.Rational(3,5)*G[4]+s.Rational(1,5)*G[4]**2),
      ('boost',G[5],s.Rational(3,4), I+s.Rational(3,4)*G[5]+s.Rational(1,4)*G[5]**2)]
for name,A,ep,Q in refs:
    check('Lorentz_reference_'+name, Q.T*eta*Q==eta and R(Q)==ep*A
          and fro(R(P1),R(Q))==ep*fro(R(P1),A))
B=s.Matrix(4,4,range(1,17)); A=(B.T-invL(B.T))/2
check('dual_projection_for_arbitrary_B', invL(A)==-A and fro(R(P1),A)==s.trace(B*R(P1)))
check('unprojected_generic_reference_rejected', invL(B.T)!=-B.T)

# True original q17 formula: source-owned 12 marks plus ALL 5 native complements.
def mpq(q):
    q=s.Rational(q)
    return mp.mpf(int(q.p))/int(q.q)
def q17(M):
    tau=mpq(s.trace(M))/4
    v=mpq(fro(M,M))/4
    herald=mp.mpf(1)/4096
    k=p**4/(24*4096)
    out=[]
    for A in G:
        u=mpq(fro(A,M))/(2*mp.sqrt(2))
        out.extend([k*(tau+u)**2,k*(tau-u)**2])
    marked=mp.fsum(out)
    GG=herald*p**4*v
    GB=herald*p*p*(1-p*p*v)
    BG=herald*p**3*v
    BB=herald*(1-p**4*v-p*p*(1-p*p*v)-p**3*v)
    out.extend([GG-marked,GB,BG,BB,1-herald])
    if not (len(out)==17 and min(out)>0 and abs(mp.fsum(out)-1)<mp.mpf('1e-65')):
        raise AssertionError('true original q17 requires all 17 strictly positive normalized labels')
    return out
H=lambda q:-mp.fsum(v*mp.log(v)/lnphi for v in q if v)
b=lambda q:[mp.sqrt(q[2*a])-mp.sqrt(q[2*a+1]) for a in range(6)]
b1=lambda q:[q[2*a]-q[2*a+1] for a in range(6)]
dot=lambda u,v:mp.fsum(a*b for a,b in zip(u,v))
for M in (I,P1,Q1):
    q=q17(M); qi=q17(invL(M))
    perm=[q[i^1] if i<12 else q[i] for i in range(17)]
    check('original_q17_reversal_'+str(len(checks)),max(abs(a-b) for a,b in zip(qi,perm))<mp.mpf('1e-60'))
    BC=mp.fsum(mp.sqrt(a*b) for a,b in zip(q,qi))
    check('original_q17_chernoff_diagonal_'+str(len(checks)),abs(1-BC-dot(b(q),b(q)))<mp.mpf('1e-60'))

# Group 4: one SMALL N=1 entire retained protocol.
# B has 14 raw Golden bits: five mismatch pairs encode uniform24, two
# mismatch pairs give the two independent terminal stop coins. All 2^14
# bank records are kept. Each legal ready value has raw probability p^21.
# Every full leaf is visited once below. Equal probability factors are grouped
# by (P-category,Q-category,total Golden code exponent) ONLY to evaluate the
# entropy efficiently; multiplicities retain every distinct full raw record.
buckets=Counter(); raw_bank_count=0; ready_count=0; leaves_count=0
status_counts=Counter(); ready_codes=Counter()
for raw in product((0,1),repeat=14):
    raw_bank_count+=1
    pairs=list(zip(raw[::2],raw[1::2]))
    code=0
    for u,v in pairs[:5]: code=2*code+u
    ready=all(u!=v for u,v in pairs) and code<24
    bank_cost=sum(1 if bit else 2 for bit in raw)
    if ready:
        ready_count+=1; ready_codes[code]+=1
        aa,signs=divmod(code,4); sig,tau=divmod(signs,2)
        stopP=(pairs[5][0]==0); stopQ=(pairs[6][0]==0)
        queries=product(range(17),repeat=2)
    else:
        queries=[(-1,-1)]
    for i,j in queries:
        hitP=ready and i==2*aa+sig
        hitQ=ready and j==2*aa+tau
        ep=ready and hitP and hitQ and sig==tau
        em=ready and hitP and hitQ and sig!=tau
        if ready:
            statusP='SUCCESS' if hitP else ('FAILURE' if stopP else 'UNRESOLVED')
            statusQ='SUCCESS' if hitQ else ('FAILURE' if stopQ else 'UNRESOLVED')
        else:
            statusP=statusQ='BANK_ABORT'
        for g1,g2 in product((0,1),repeat=2):
            condition=(g1==1 and g2==1 and ep) or (g1==0 and not em)
            base_cost=bank_cost+(1 if g1 else 2)+(1 if g2 else 2)
            for g3 in ((0,1) if condition else (None,)):
                cost=base_cost+(0 if g3 is None else (1 if g3 else 2))
                buckets[(i,j,cost)]+=1
                leaves_count+=1
                status_counts[(statusP,statusQ)]+=1
check('complete_bank_structure',raw_bank_count==2**14 and ready_count==96
      and ready_codes==Counter({j:4 for j in range(24)}))
check('all_terminal_statuses_retained', all(any(a==tag for a,b in status_counts)
      for tag in ('SUCCESS','FAILURE','UNRESOLVED','BANK_ABORT')))
r=96*p**21
C=14*g+2*g+g*p*p
c=g*p*p*r/24
ppows={e:p**e for _,_,e in buckets}
def full_leaf_price(q,t):
    logsq=[-mp.log(v)/lnphi for v in q]
    logst=[-mp.log(v)/lnphi for v in t]
    masses=[]; price=[]
    for (i,j,e),count in buckets.items():
        mass=count*ppows[e]
        ell=mp.mpf(e)
        if i>=0:
            mass*=q[i]*t[j]
            ell+=logsq[i]+logst[j]
        masses.append(mass);price.append(mass*ell)
    return mp.fsum(masses),mp.fsum(price)
qa=[q17(I),q17(P1)]; qb=[q17(I),q17(Q1)]
prices={};errors=[]
for u,v in product((0,1),repeat=2):
    mass,price=full_leaf_price(qa[u],qb[v]);prices[u,v]=price
    formula=C+r*(H(qa[u])+H(qb[v]))+c*dot(b1(qa[u]),b1(qb[v]))
    err=abs(price-formula);errors.append(err)
    check(f'complete_N1_price_setting_{u}{v}',abs(mass-1)<mp.mpf('1e-60') and err<mp.mpf('1e-58'))
rectangle=prices[1,1]-prices[1,0]-prices[0,1]+prices[0,0]
predicted=c*dot([a-b for a,b in zip(b1(qa[1]),b1(qa[0]))],
                [a-b for a,b in zip(b1(qb[1]),b1(qb[0]))])
check('complete_N1_mixed_rectangle',abs(rectangle-predicted)<mp.mpf('1e-58') and abs(predicted)>mp.mpf('1e-30'))
# Hostile control: premeasurement retained in the bank adds constant g;
# conditional copying adds 0, so the mixed term is absent.
cached={(u,v):17*g+r*(H(qa[u])+H(qb[v])) for u,v in product((0,1),repeat=2)}
cached_rect=cached[1,1]-cached[1,0]-cached[0,1]+cached[0,0]
check('cached_register_cannot_replace_fresh',abs(cached_rect)<mp.mpf('1e-60') and abs(predicted)>mp.mpf('1e-30'))

# Group 5: exact square completion, inverse witness and score-coordinate source.
r0,alpha,AP,AQ=s.symbols('r alpha AP AQ', positive=True)
u=s.symbols('u0:6',real=True);v=s.symbols('v0:6',real=True)
norm=lambda z:sum(t*t for t in z)
lhs=r0*(AP+AQ)+r0*alpha*sum(a*b for a,b in zip(u,v))
dP=AP-alpha*norm(u)/2; dQ=AQ-alpha*norm(v)/2
rhs=r0*(dP+dQ)+r0*alpha*norm([a+b for a,b in zip(u,v)])/2
check('minimum_iff_square_completion',s.expand(lhs-rhs)==0)
check('inverse_pair_exposes_negative_excess',s.expand(lhs.subs(dict(zip(v,[-t for t in u]))).subs(AQ,AP)-2*r0*dP)==0)
z=s.symbols('z',positive=True);L=s.symbols('L',positive=True)
S=z*z+3*z; kappa=-L*z*s.diff(S,z)
check('log_probability_coefficient',zero(kappa*(-1/(L*z))-s.diff(S,z)))
# Coarse Shannon Hessian in probability coordinates; 34 is consumed dimension,
# not re-certified native rank. The determinant lemma tests the signed block.
z0=s.Rational(1,100); rr=1-34*z0
check('coarse_entropy_34_block_negative',rr>0 and all((1/z0)**m*(1+m*z0/rr)>0 for m in range(1,35)))
# Field embedding x -> z=1/4+x+x²: extra gradient*second-jet term is nonzero.
t=s.symbols('t',real=True); zz=s.Rational(1,4)+t+t*t
HH=lambda zz:-zz*s.log(zz)-(1-zz)*s.log(1-zz)
actual=s.diff(HH(zz),t,2).subs(t,0)
pullback=s.diff(HH(z),z,2).subs(z,s.Rational(1,4))
extra=2*s.diff(HH(z),z).subs(z,s.Rational(1,4))
check('nonlinear_embedding_second_jet_required',zero(actual-pullback-extra) and not zero(extra))
# Unnormalized global source cannot be fixed by the normalized law.
y=s.symbols('y',real=True)
w1,w2=s.exp(-y),s.exp(-2*y)
Z=w1+w2
shift=s.exp(-y*y)
check('normalized_weights_ignore_common_scale',zero(shift*w1/(shift*Z)-w1/Z))
check('absolute_normalizer_source_survives',zero(s.diff(-s.log(shift*Z)+s.log(Z),y)-2*y))
probs=[z,(1-z)/3,2*(1-z)/3]
prices_symbolic=[z*z,1+z,2-z*z]
direct=s.diff(sum(q*l for q,l in zip(probs,prices_symbolic)),z)
expected_deriv=sum(q*s.diff(l,z) for q,l in zip(probs,prices_symbolic))
score_mean=sum(s.diff(q,z) for q in probs)
mean_price=sum(q*l for q,l in zip(probs,prices_symbolic))
cov=sum(l*s.diff(q,z) for q,l in zip(probs,prices_symbolic))-mean_price*score_mean
check('full_price_score_covariance',zero(direct-expected_deriv-cov) and zero(score_mean))

result={
 'status':'PASS_NEW_ORIENTED_RECONSTRUCTION',
 'created':'2026-10-21',
 'historical_bytes_recovered':False,
 'historical_217_checks_reused':False,
 'historical_39424_histories_reused':False,
 'new_check_count':len(checks),
 'full_N1_fixture':{
  'bank_raw_histories':raw_bank_count,'ready_bank_histories':ready_count,
  'full_terminal_histories_per_setting':leaves_count,'settings':4,
  'total_terminal_histories_evaluated':4*leaves_count,
  'equal_probability_buckets':len(buckets),'golden_bits_prepaid':14,
  'readiness':mp.nstr(r,30),'all_17_query_labels_retained':True,
  'full_raw_bank_and_both_queries_retained':True,
  'numeric_digits':mp.mp.dps,'largest_absolute_price_error':mp.nstr(max(errors),12),
  'mixed_rectangle':mp.nstr(rectangle,35),'predicted_rectangle':mp.nstr(predicted,35),
  'rectangle_error':mp.nstr(abs(rectangle-predicted),12)},
 'scope':'New conditional identities and full classical N=1 model using original q17; not physical full Book, not quantum full transcript independence, not full128 replay/rank or compulsory admission.',
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'runtime_seconds':round(time.monotonic()-started,3),
 'sympy_version':s.__version__,'mpmath_version':mp.__version__,
 'checks':checks}
payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
if args.output is not None:
    args.output.write_text(payload)
print(payload,end='')
