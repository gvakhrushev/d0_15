"""Original L4/CAR16 source with FIXED equal first and last groups.

No eigensolver, clipped spectrum, sampled phase, or reduced active trace.
The proof assumes IEEE binary64 round-to-nearest elementary arithmetic,
no overflow (all operands are norm bounded), and gamma_128 for a
complex length-16 dot product, gamma_2048 for the length-256 inner product.
Gradual-underflow errors are absorbed by the explicit 2^-1000 local margin.
All propagated error budgets are Fractions. No BLAS routine is used for floating products.
"""
from fractions import Fraction as F
import itertools,json,math,sys,hashlib,re,subprocess
from pathlib import Path
import numpy as np
np.seterr(all="raise")
SOURCE_HEAD="726192353504a81a9ab2b751f9b6c7866271e75a"
OWNER_SHA="3858e097939054ec0957321bcd70e7b98f68c68b74fb800bc8ef22a660a56c74"
PRIMARY="02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
CLOCK="02_REGISTRY/research/sources/d0_clock_winding_source_2026-10-28/PROOF_RU.md"
REPO=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else Path.cwd()
def git(*args):
    return subprocess.check_output(["git","--work-tree="+str(REPO),*args],cwd=REPO)
primary_blob=git("rev-parse",SOURCE_HEAD+":"+PRIMARY).decode().strip()
primary_text=git("cat-file","blob",primary_blob).decode()
owner_section=primary_text[primary_text.index("## 7db. A changing original full128 history reverses the complete scale source"):]
owner_code=re.search(r"```python\n(.*?)```",owner_section,re.S).group(1)
if hashlib.sha256(owner_code.encode()).hexdigest()!=OWNER_SHA:
    raise RuntimeError("immutable original source owner mismatch")
clock_blob=git("rev-parse",SOURCE_HEAD+":"+CLOCK).decode().strip()
clock_bytes=git("cat-file","blob",clock_blob)
if hashlib.sha256(clock_bytes).hexdigest()!="ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418":
    raise RuntimeError("immutable whole-clock proof mismatch")
def mm(a,b):
    return np.einsum("ik,kj->ij",a,b,optimize=False)

def require(test,msg):
    if not test: raise RuntimeError(msg)

def up(value):
    """Exact upward rounding of ERROR BOUNDS, not physical matrix entries."""
    qq=2**100
    return F((value.numerator*qq+value.denominator-1)//value.denominator,qq)

d=16;L=4;groups=9;m=644;z=F(1,2**20)
nu=F(sys.argv[1]) if len(sys.argv)>1 else F(3,5)
boundary_nu=F(3,5)
require(nu in (F(3,10),F(3,5)),'the two endpoints of one declared curve')
unit=F(1,2**53);gamma128=128*unit/(1-128*unit)
underflow=F(1,2**1000);gamma2=2*unit/(1-2*unit)
e_input=F(1,2**40);e_mul=F(1,2**39)
e_sub=F(1,2**44);e_update=F(1,2**33);e_trace=F(1,2**30)
gamma2048=2048*unit/(1-2048*unit)
gamma256=256*unit/(1-256*unit)
require(gamma2048*(4*2)*(4*19)+underflow<e_trace,'length256 complex vdot budget')
require(gamma256*256*16*2*19+underflow<F(1,2**20),'outer source summation budget')
require(groups==9 and 2*groups==18,'full derivative norm bound')
require(64*gamma128+underflow<e_mul,'contraction matrix multiply budget')
require(16*gamma128*(3*2+2*19)+F(1,2**43)+underflow<e_update,
        'derivative product/update budget')
require(16*unit*(2+F(1,10**6))+underflow<e_sub,'subtraction budget')
require(16*unit*3+underflow<e_sub,'final derivative scaling budget')
x=F(2,55)
require(F(176,359)/((1-x*x)*(1-x)**2)<1 and x<F(1,16),
        'complete clock majorant A1_N < 16^-N')
order=(0,2,3,1)
cre=[]
for r in range(4):
    cr=np.zeros((16,16),dtype=np.int64)
    for b in range(16):
        if not (b>>r)&1:
            cr[b|(1<<r),b]=(-1)**sum((b>>s)&1 for s in order[:order.index(r)])
    cre.append(cr)
eye=np.eye(16,dtype=np.int64)
for r,s in itertools.product(range(4),repeat=2):
    require(np.array_equal(cre[r]@cre[s].T+cre[s].T@cre[r],eye if r==s else 0*eye),
            'exact CAR anticommutator')
subsets=[[r for r in order if (b>>r)&1] for b in range(16)]
def det(a):
    if not a:return F(1)
    return sum(((-1)**j)*a[0][j]*det([row[:j]+row[j+1:] for row in a[1:]])
               for j in range(len(a)))

lam=[];axis=[F(1),F(0),F(0)]
for j in range(8):
    require(sum(v*v for v in axis)==1,'axis normalization')
    mat=[[F(int(a==b)) for b in range(4)] for a in range(4)]
    for a,b in itertools.product(range(3),repeat=2):
        mat[a+1][b+1]=2*axis[a]*axis[b]-int(a==b)
    require(det(mat)==1,'proper Lorentz spatial pi rotation')
    lm=np.empty((16,16),dtype=object)
    for a,aa in enumerate(subsets):
        for b,bb in enumerate(subsets):
            lm[a,b]=det([[mat[x][y] for y in bb] for x in aa]) if len(aa)==len(bb) else F(0)
    require(np.array_equal(lm@lm.T,eye),'exact exterior orthogonality')
    require(np.array_equal(lm@cre[0],cre[0]@lm),'original role0 own-leg condition')
    lam.append(lm)
    axis=[F(24,25)*axis[0]-F(7,25)*axis[1],
          F(7,25)*axis[0]+F(24,25)*axis[1],F(0)]
lam.append(lam[0].copy())
require(np.array_equal(lam[0],lam[-1]),"identical fixed prefix and suffix spatial connections")
left_right=[(cre[0]@lm,lm.T@cre[0].T) for lm in lam]

bits=80;two=2**bits;root=math.isqrt(5*two*two)
k_lo=F(3)-F(root+1,two);k_hi=F(3)-F(root,two)
k=float((k_lo+k_hi)/2);k_error=max(abs(F.from_float(k)-k_lo),abs(F.from_float(k)-k_hi))
require(k_error<F(1,2**50),'exact sqrt5 input enclosure')
require(2*F(1,2**45)+F(1,2**90)+16*gamma128*(1+F(1,2**45))**2+underflow<F(1,2**41),'A input budget')
require(32*gamma2+underflow<F(1,2**46),'C scalar/identity rounding budget')
require(0<F.from_float(k)<1 and F(1,2**41)+k_error+F(1,2**46)<e_input,'C input budget')

def exact_to_float(re,im):
    out=np.empty((16,16),complex);rows=[F(0)]*16;cols=[F(0)]*16
    for a,b in itertools.product(range(16),repeat=2):
        rr=F(re[a,b]);ii=F(im[a,b]);fr=float(rr);fi=float(ii)
        er=abs(F.from_float(fr)-rr)+abs(F.from_float(fi)-ii)
        rows[a]+=er;cols[b]+=er;out[a,b]=complex(fr,fi)
    err=max(rows+cols)
    require(err<=F(1,2**45),'exact matrix conversion enclosure')
    return out,err

def mul_power(a,ea,b,eb):
    er=up(ea+eb+ea*eb+e_mul)
    require(er<F(1,10**6),'all computed powers remain norm below2')
    return mm(a,b),er
def power(c,exponent):
    ans=np.eye(16,dtype=complex);ea=F(0);base=c;eb=e_input
    while exponent:
        if exponent&1:ans,ea=mul_power(ans,ea,base,eb)
        exponent//=2
        if exponent:base,eb=mul_power(base,eb,base,eb)
    return ans,ea

phases=((1,0),(0,1),(-1,0),(0,-1))
trace_values=[];max_a_error=F(0);expected_budget=None
active_groups=tuple(range(1,8))
require(2*len(active_groups)==14,"seven actual varying groups; boundary derivatives are zero")
for idx in itertools.product(range(L),repeat=4):
    ph=[phases[t] for t in idx]
    kk=np.eye(16,dtype=complex);dk=np.zeros((16,16),complex)
    ek=F(0);edk=F(0)
    for j in range(groups):
        require(2*j<=16,'preceding derivative norm bound')
        left,right=left_right[j]
        re=ph[0][0]*(left+right)-(cre[0]+cre[0].T)
        im=ph[0][1]*(left-right)
        for r in range(1,4):
            re=re+(ph[r][0]-1)*(cre[r]+cre[r].T)
            im=im+ph[r][1]*(cre[r]-cre[r].T)
        scale=boundary_nu if j in (0,8) else nu
        aa,a_error=exact_to_float(re*(scale/16),im*(scale/16))
        max_a_error=max(max_a_error,a_error)
        # Exact a is Hermitian; norm<=nu by the original four-role bound.
        require(np.array_equal(aa,aa.conj().T),'exact Hermitian pairing of rounded rational inputs')
        cc=np.eye(16)-k*mm(aa,aa)
        cm,ecm=power(cc,m);prev,eprev=power(cc,m-1)
        dc=2*m*(cm-prev) if j in active_groups else np.zeros((16,16),complex)
        edc=up(2*m*(ecm+eprev+e_sub)+e_sub) if j in active_groups else F(0)
        require(edc<F(1,10**4),'derivative power remains norm below3')
        new_edk=up(edc*(1+ek)+2*ek+ecm*(2*j+edk)+edk+e_update)
        new_ek=up(ecm+ek+ecm*ek+e_mul)
        dk=mm(dc,kk)+mm(cm,dk);kk=mm(cm,kk);edk=new_edk;ek=new_ek
    require(edk<F(1,1000),'derivative product remains norm below19')
    tr=float(np.einsum("ij,ij->",kk.conj(),dk,optimize=False).real)
    trace_values.append(tr)
    require(expected_budget is None or expected_budget==(ek,edk),'uniform exact budget')
    expected_budget=(ek,edk)

ek,edk=expected_budget
lead_float=-float(2*z)*sum(trace_values)
lead=F.from_float(lead_float)
# d_total=4096 and ||K'||<=14. vdot and outer sum errors are included.
e_lead=2*z*(4096*(edk+14*ek+ek*edk)+256*e_trace+F(1,2**20))
resolvent_tail=2*z*z*4096*14/(1-z)
lower=lead-e_lead-resolvent_tail;upper=lead+e_lead+resolvent_tail
# Actual full copied clock has at least8 stages per full128 round.
n=groups*m;N_min=8*n
require(N_min>=64 and 4*n*F(21,20)<2**15,'actual complete endpoint heat budget')
# A1_N < (1/16)^N, from the owned rational winding majorant.
heat_bound=F(1,2**240)
require(upper<F(-1,500000000) if nu==F(3,5) else lower>F(1,400000), 'certified sign of the full internal seven-group source')
require(upper+heat_bound<0 if nu==F(3,5) else lower-heat_bound>0, 'full Book sign with both boundary blocks fixed')
print('FULL FIXED-BOUNDARY SOURCE', str(nu), float(lower), float(upper), file=sys.stderr, flush=True)
out={'status':'PASS','GR_closed':False,
     'input_head':SOURCE_HEAD,'primary_blob':primary_blob,'source_owner_sha256':OWNER_SHA,
     'whole_clock_proof_blob':clock_blob,
     'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'input':{'L':L,'all_spatial_CAR_modes':4096,'nu':str(nu),'fixed_first_last_nu':str(boundary_nu),'last_rotation':'first_rotation','z':'2^-20',
              'rotation_cos':'24/25','rotation_sin':'7/25','groups':groups,
              'repetitions_per_group':m,'actual_full128_rounds':n,
              'minimum_copied_clock_stages':N_min},
     'method':'exact Gaussian-rational inputs; binary powers; IEEE gamma128 enclosure; analytic resolvent and whole-clock tails',
     'assumptions':['IEEE binary64 round-to-nearest matrix dot error <=gamma128; length256 vdot <=gamma2048',
                    'declared original matrix/clock realization; physical programme selection not asserted'],
     'leading_source':lead_float,'source_roundoff_bound':float(e_lead),
     'resolvent_tail_bound':float(resolvent_tail),
     'exact_input_max_operator_error_bound':float(max_a_error),
     'final_K_operator_error_bound':float(ek),'final_DK_operator_error_bound':float(edk),
     'full_feedback_source_enclosure':[float(lower),float(upper)],
     'whole_scene_heat_source_bound':'2^-240',
     'sign_certified':bool(upper+heat_bound<0 or lower-heat_bound>0),'actual_bulk_derivative_norm_bound':14,
     'exact_feedback_lower':str(lower),'exact_feedback_upper':str(upper),
     'exact_source_roundoff_bound':str(e_lead),'exact_resolvent_tail_bound':str(resolvent_tail),
     'sign_margin':('less than -1/500000000' if nu==F(3,5) else 'greater than 1/400000'),
     'scope':'ONE fixed-boundary internal scale equation on the original noncommuting history; all4096 modes and full128 realization. Not all40+matter stationarity, a finite G/CX compilation, physical admission, GR/refinement closure or a minimum.',
     'python':sys.version.split()[0],'numpy':np.__version__}
print(json.dumps(out,indent=2))
