"""Certify the entropy of the actual six freshly addressed registers in original full128.
Python 3.9+, NumPy, mpmath. No other project files required.
"""
import json
from fractions import Fraction
import numpy as np
import mpmath as mp

mp.mp.dps=75
mp.iv.dps=65
iv=mp.iv
def need(x,l):
    if not x: raise ArithmeticError(l)
def hd(x,y): return bin(x^y).count("1")
def demand(X,low,up,label):
    need(X>=iv.mpf(str(low)) and X<=iv.mpf(str(up)),label)
def midpoint(X): return float(X.mid)
def fixed(x):
    # The interval proof uses the actual finite decimal, not the eigensolver object.
    return iv.mpf(mp.nstr(x,59))
def matrix(entries):
    return iv.matrix(entries)
def cert_small(A,tol):
    # Symmetric bound on both spectral and Frobenius norms by d*max|A_ij|.
    return all(abs(x)*A.rows < iv.mpf(tol) for x in A)

# Exact original 32 Walsh columns in units 1/5, represented as Gaussian integers.
eye=np.eye(16,dtype=complex)
order=(0,2,3,1)
rows=[]
for mode,phase in enumerate((1j,1j,-1,-1j)):
    c=np.zeros_like(eye)
    for old in range(16):
        if not ((old>>mode)&1):
            c[old | (1<<mode),old]=(-1)**sum((old>>j)&1 for j in order[:order.index(mode)])
    proj=np.einsum("ij,kj->ik",c,c.conj(),optimize=False)
    for pair in ((3*phase*c,5*eye-proj),(3*phase.conjugate()*c.T,4*eye+proj),
                 (-3*c,-5*eye+proj),(-3*c.T,-4*eye-proj)):
        rows.extend((pair,pair))
walsh=np.array([[(-1)**hd(n&j,0) for j in range(32)] for n in range(32)])
num=np.einsum("nj,jbkl->nbkl",walsh,np.asarray(rows),optimize=False).reshape(64,16,16)
trace_num=np.sum(num.real**2+num.imag**2,axis=(1,2)).astype(int)
need(max(trace_num)<2**39,"integer Walsh norm products are exact")
addr=[j for j,alpha in enumerate(trace_num) if alpha]
need(len(addr)==21,"actual positive address support")
jet={9:-Fraction(27,10),**dict.fromkeys((13,29,45,61),Fraction(3,40)),
     **dict.fromkeys((16,20,24,28,48,52,56,60),Fraction(3,10))}
need(sum(jet.values())==0 and set(jet)<=set(addr),"jet and support")
dist=sum(w*hd(j,9) for j,w in jet.items())
need(dist==9,"exact Hamming transport from the unique negative row")
def qdata(ctx):
    p=(ctx.sqrt(5)-1)/2
    k=ctx.mpf(9)/640
    fac=p**2*k/4
    w=[]; dw=[]
    for j in addr:
        w.append((1-2*p**2*k)**2+4*p**3*k**2 if j==0 else fac*int(trace_num[j])/25600)
        d=jet.get(j,Fraction(0)); dw.append(fac*d.numerator/d.denominator)
    return p,w,dw
p,w,dw=qdata(iv)
need(iv.mpf(1) in sum(w) and iv.mpf(0) in sum(dw),"interval normalization")
ell=-iv.log(p)
# Classical after reading all 0/10 registers. Bits are independently flipped on a given address.
entropy_der=iv.mpf(0); derivative_total=iv.mpf(0); prob_total=iv.mpf(0)
signed_y=[]
for y in range(64):
    kernel=[p**(6+hd(j,y)) for j in addr]
    mix=sum(a*b for a,b in zip(w,kernel))
    jet_y=sum(a*b for a,b in zip(dw,kernel))
    entropy_der-=jet_y*iv.log(mix)
    signed_y.append(jet_y)
    prob_total+=mix; derivative_total+=jet_y
need(iv.mpf(1) in prob_total and iv.mpf(0) in derivative_total,"all 64 output words")
classical=entropy_der/ell
transport_bound=9*p**3*(9*p**2/2560)
# Coherent pointer marginal: nonzero spectrum coincides with S=sqrt(Q) Gram sqrt(Q).
def gram(ctx,pp,weights):
    overlap=2*pp*ctx.sqrt(pp)
    return ctx.matrix([[ctx.sqrt(weights[a]*weights[b])*overlap**hd(j,k)
                        for b,k in enumerate(addr)] for a,j in enumerate(addr)])
pa,wa,_=qdata(mp.mp)
Sn=gram(mp.mp,pa,wa)
eig,U=mp.eigsy(Sn)
S=gram(iv,p,w)
L=iv.diag([fixed(x) for x in eig])
W=matrix([[fixed(U[i,j]) for j in range(U.cols)] for i in range(U.rows)])
J=iv.eye(len(addr))
orth=W.T*W-J
residual=S*W-W*L
need(cert_small(orth,"1e-51") and cert_small(residual,"1e-51"),"certified near-orthogonal eigendecomposition")
need(all(L[i,i] <= L[i+1,i+1] for i in range(len(addr)-1)), "verified ordered approximate spectrum")
need(L[0,0]>iv.mpf("1e-16") and L[len(addr)-1,len(addr)-1]<=1,"lower eigenvalue and upper eigenvalue")
# Polar correction: ||U-Q||<=orth, ||S-Q L Q*||<=residual+3orth<4e-51.
# Log is op-Lipschitz with constant 1/min(lambda) on this positive interval;
# min lambda >1e-16-4e-51>1e-17. Also ||log L||<40.
logL=iv.diag([iv.log(L[i,i]) for i in range(len(addr))])
need(all(abs(logL[i,i])<40 for i in range(len(addr))),"bounded log of candidate eigenvalues")
logS=W*logL*W.T
dS=matrix([[S[i,j]*(dw[i]/w[i]+dw[j]/w[j])/2 for j in range(len(addr))]
           for i in range(len(addr))])
need(sum(abs(x) for x in dS)<100,"trace norm of the Gram tangent <= sum of entry magnitudes")
JQ=-sum(dS[i,j]*logS[j,i] for i in range(len(addr)) for j in range(len(addr)))/ell
guard=iv.mpf(["-1e-29","1e-29"])  # 100*(4e-51/1e-17+3e-51*40)/ell <1e-29.
quantum=JQ+guard
kap=27*p**2/25600
res=kap*((41*iv.log(2)+16*iv.log(3)-4*iv.log(5))/ell-6*p**3)

tv_classical=sum(abs(x) for x in signed_y)/2
tv_full=sum(abs(x) for x in dw)/2
active=[i for i,d in enumerate(dw) if not (0 in d)]
signed_gram=matrix([[dw[i]*(2*p*iv.sqrt(p))**hd(addr[i],addr[j]) for j in active] for i in active])
# Similar to G^(1/2) diag(dw) G^(1/2), hence has precisely one negative eigenvalue.
# The determinant is negative below its magnitude and positive above that number.
def secular(t):
    return iv.det(signed_gram+t*iv.eye(len(active)))
lo,hi=Fraction(0),Fraction(1,100)
def as_iv(x): return iv.mpf(x.numerator)/x.denominator
need(secular(as_iv(hi))>0,"upper negative eigenvalue bound")
for _ in range(31):
    middle=(lo+hi)/2
    value=secular(as_iv(middle))
    if value>0: hi=middle
    elif value<0: lo=middle
    else: raise ArithmeticError("uncertified determinant sign")
tv_q=iv.mpf([as_iv(lo),as_iv(hi)])
demand(quantum,"0.0039730060182410770","0.0039730060182410771","coherent erasure derivative")
demand(classical,"0.0006113045526199756","0.0006113045526199757","read erasure derivative")
bit_coeffs=[sum(wi*((j>>i)&1) for j,wi in jet.items()) for i in range(6)]
need(bit_coeffs==list(map(Fraction,["-12/5","0","3/2","-6/5","51/20","27/20"])),"actual six bit jets")
u=9*p**2/2560
thresholds=dict(common_local_target=midpoint(res/(u*p**3*9/5)), common_local_control_target=midpoint(res/(u*9/5)),
                independent_local_targets=midpoint(res/(u*p**3*9)),independent_local_control_targets=midpoint(res/(u*9)))
demand(res,"0.03254695878794524","0.03254695878794530","target slope")
demand(res/tv_classical,"30.07943","30.07944","classical oscillation threshold")
demand(res/tv_q,"24.05792926","24.05792936","coherent oscillation threshold")
demand(res/tv_full,"8.97675","8.97676","old-label threshold")
print(json.dumps(dict(result="PASS",positive_addresses=addr, material_same_history=True, hamming_cost=str(dist),
   d_entropy_read_in_golden_units=midpoint(classical), hamming_bound=midpoint(transport_bound),
   d_entropy_coherent_in_golden_units=midpoint(quantum), remaining_work_requirement=midpoint(res),
   smallest_gram_eigenvalue=midpoint(L[0,0]), largest_gram_eigenvalue=midpoint(L[len(addr)-1,len(addr)-1]),
   classical_interval=str(classical), coherent_interval=str(quantum),
   local_work_necessary_oscillations=thresholds, fixed_energy_oscillation=dict(classical_trace_variation=midpoint(tv_classical),
       coherent_trace_variation=str(tv_q), full_label_trace_variation=midpoint(tv_full),
       min_classical_price_range=midpoint(res/tv_classical),
       min_coherent_price_range=str(res/tv_q), min_full_label_price_range=midpoint(res/tv_full)),
   proof="interval matrix residual and polar-log bound; original 13-row jet input from section 7gd",
   complete_physical_binding=False),indent=2))
