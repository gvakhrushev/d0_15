#!/usr/bin/env python3
"""Fixed-Golden native source stencils with an actual retained record.

All expanded calls are positive G/CX/SourceI. Large repeats are specified,
NOT iterated or claimed run on hardware. The 42-variable test is a local
Palatini jet, not a lattice GR root or a runtime quantum field decoder.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse, hashlib, json, math
import mpmath as mp
import numpy as np
import scipy.linalg as la
import sympy as sp

mp.mp.dps=85
mp.iv.dps=90
CHECKS=0
PIN='4b30fcb4dc743e7a04415c9701aae19a847e8dab'
PP=(mp.sqrt(5)-1)/2
THETA=mp.atan2(PP,mp.sqrt(PP))
PPI=(mp.iv.sqrt(5)-1)/2
THETAI=mp.iv.atan2(PPI,mp.iv.sqrt(PPI))
ZETA=mp.mpf(2)**-20
ZETAI=mp.iv.mpf(1)/2**20

def check(v, msg):
    global CHECKS
    CHECKS+=1
    if not bool(v): raise AssertionError(msg)

def iv(x):
    if hasattr(x,'_mpi_'): return x
    if isinstance(x,sp.Rational): return mp.iv.mpf(int(x.p))/int(x.q)
    if isinstance(x,Fraction): return mp.iv.mpf(x.numerator)/x.denominator
    return mp.iv.mpf(x)

def low(x):
    with mp.workdps(110): return mp.mpf(x._mpi_[0])
def high(x):
    with mp.workdps(110): return mp.mpf(x._mpi_[1])
def mid(x): return (low(x)+high(x))/2
def mag(x): return max(abs(low(x)),abs(high(x)))
def text(x,n=28): return mp.nstr(x,n)
def outward_decimal(endpoint, upward, places=80):
    sign,man,exp,_=endpoint
    num=(-man if sign else man)*10**places
    if exp>=0: num*=2**exp;den=1
    else: den=2**(-exp)
    n=(-((-num)//den)) if upward else (num//den)
    st=str(abs(n)).rjust(places+1,'0')
    return ('-' if n<0 else '')+st[:-places]+'.'+st[-places:]
def interval_text(x):
    return [outward_decimal(x._mpi_[0],False),outward_decimal(x._mpi_[1],True)]
def upper_iv(x): return mp.iv.mpf(x.b)
def lower_iv(x): return mp.iv.mpf(x.a)

def near(a,b,msg,tol=1e-11):
    e=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    check(e<tol,msg+': '+str(e));return e

# Physical wire names match the parent's actual 16-wire input.
WIRES=(0,6,10,11,12,13,14)
DIM=1<<len(WIRES)

def gate_matrix(op, wires):
    k=len(wires)
    if op=='CX': loc=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],int)
    elif op=='SourceI':
        Li=np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]],int)
        loc=la.block_diag(np.eye(4,dtype=int),Li)
    elif op=='GJ': loc=np.array([[0,-1],[1,0]],int)
    else: raise ValueError(op)
    positions=[WIRES.index(w) for w in wires]
    result=np.zeros((DIM,DIM),dtype=np.int64)
    for col in range(DIM):
        bits=[(col>>(len(WIRES)-1-j))&1 for j in range(len(WIRES))]
        c=sum(bits[w]<<(k-1-j) for j,w in enumerate(positions))
        for r in range(1<<k):
            if not loc[r,c]: continue
            bb=bits[:]
            for j,w in enumerate(positions):bb[w]=(r>>(k-1-j))&1
            row=sum(bb[j]<<(len(WIRES)-1-j) for j in range(len(WIRES)))
            result[row,col]=int(loc[r,c])
    return result

SI=('SourceI',(0,13,14)); COPY=('CX',(11,10)); G=('G',(11,))
SWAP=[('CX',(0,11)),('CX',(11,0)),('CX',(0,11))]
ZWORD=SWAP+[SI,SI]+SWAP
SEED=[('CX',(6,12))]+[SI]*4
BASE=SEED+[COPY]+ZWORD+[G,COPY]

def primitive_replay():
    cache={g:gate_matrix(*g) for g in set(BASE) if g[0]!='G'}
    Jq=gate_matrix('GJ',(11,))
    I=np.eye(DIM,dtype=np.int64)
    # Exact integer coefficient matrices of c=cos(m theta),s=sin(m theta).
    pre=I.copy();post=I.copy();seen=False
    for g in BASE:
        if g[0]=='G':seen=True;continue
        if not seen:pre=cache[g]@pre
        else:post=cache[g]@post
    A=post@pre;B=post@Jq@pre
    check(np.array_equal(A,A.T) and np.array_equal(B,B.T),'family endpoint Hermitian coefficientwise')
    check(np.array_equal(A@A,I) and np.array_equal(B@B,I),'both endpoint coefficients involutive')
    check(not np.any(A@B+B@A),'endpoint coefficients anticommute')
    check(np.trace(A)==np.trace(B)==0,'equal positive/negative full multiplicities')
    # Source input: data6,Spin13/14 arbitrary; port/query/record/seed blank.
    inputs=[]
    for idx in range(DIM):
        bits={w:(idx>>(len(WIRES)-1-j))&1 for j,w in enumerate(WIRES)}
        if all(bits[w]==0 for w in (0,10,11,12)):inputs.append(idx)
    embed=I[:,inputs];P=embed@embed.T
    M=np.diag([int(((i>>(len(WIRES)-1-WIRES.index(10)))&1)==0 and
                   ((i>>(len(WIRES)-1-WIRES.index(12)))&1)==0) for i in range(DIM)])
    Click=np.diag([((i>>(len(WIRES)-1-WIRES.index(10)))&1) for i in range(DIM)])
    Q=embed.T@A@embed
    check(Q.shape==(8,8) and np.trace(Q)==4 and np.array_equal(Q@Q,Q),'same seed returning projector')
    check(not np.any(embed.T@B@embed),'no sine return corner')
    check(not np.any((M-P)@A@embed) and not np.any((M-P)@B@embed),'exact saturated recorded effect on all inputs')
    check(np.array_equal(embed.T@A.T@Click@A@embed,np.zeros((8,8),int)),'no-click amplitude zero')
    check(np.array_equal(embed.T@B.T@Click@B@embed,np.eye(8,dtype=int)),'actual retained click law on all inputs')
    check(not np.any(embed.T@(A.T@Click@B+B.T@Click@A)@embed),'no report cross term')
    Zmat=I.copy()
    for g in ZWORD:Zmat=cache[g]@Zmat
    check(np.array_equal(Zmat@Zmat,I),'literal Z-word square')
    check(np.array_equal(Zmat@Jq@Zmat,-Jq),'exact positive-call inverse synthesis')
    check(len(BASE)==16 and dict(Counter(g[0] for g in BASE))=={'CX':9,'SourceI':6,'G':1},'parent16 actual inventory')
    # All columns at native m=1, full endpoint cotangent matrices.
    c=float(mp.sqrt(PP));s=float(PP);U=c*A+s*B
    K=embed.T@U@embed;E=embed.T@U.T@M@U@embed
    z=float(ZETA);D=(1-z)*np.eye(8)+z*K.T@K
    inv=la.inv(D)
    AJ=-2*z*U@embed@inv@K.T@embed.T
    AE=-2*z*U@embed@inv@embed.T@U.T@M
    coterr=near(AJ,AE,'all-endpoint return/record cotangent',1e-18)
    near(E,K.T@K,'native exact-gap value',1e-15)
    # Every occurrence, including temporary routes, inherits the full identity.
    floats=[]
    for g in BASE:floats.append(c*I+s*Jq if g[0]=='G' else cache[g].astype(float))
    prefixes=[np.eye(DIM)]
    for g in floats:prefixes.append(g@prefixes[-1])
    suffix=[None]*(len(floats)+1);suffix[-1]=np.eye(DIM)
    for j in range(len(floats)-1,-1,-1):suffix[j]=suffix[j+1]@floats[j]
    rng=np.random.default_rng(291026)
    worst=0.;rows=[]
    for j,g in enumerate(floats):
        # a generic independent local occurrence perturbation on the full active carrier
        X=rng.normal(size=(DIM,DIM));X=X-X.T;X/=la.norm(X,2)
        du=suffix[j+1]@X@g@prefixes[j]
        dk=embed.T@du@embed
        de=embed.T@(du.T@M@U+U.T@M@du)@embed
        gj=-2*z*np.trace(inv@K.T@dk)
        ge=-z*np.trace(inv@de)
        worst=max(worst,near(gj,ge,'independent occurrence source identity',1e-18))
        # reflection makes every Fourier thermal-character first derivative zero
        for k in (1,2,3,4):
            hv=k*np.trace(np.linalg.matrix_power(U,k-1)@du).real
            check(abs(hv)<1e-12,'whole heat-character derivative on each occurrence')
        rows.append(float(gj))
    # The actual G occurrence changes the report: the unrestricted source is NOT zero.
    j=BASE.index(G);du=suffix[j+1]@Jq@floats[j]@prefixes[j]
    dk=embed.T@du@embed
    g_active=-2*z*np.trace(inv@K.T@dk)
    fullG=2*g_active # actual oldRIGHT multiplicity2
    check(fullG>0,'nonzero true stage15 row retained')
    # Independent final work rotation at the saturated point: derivative zero,
    # second order is not falsely asserted zero.
    X=Jq.astype(float)
    du=X@U
    dk=embed.T@du@embed
    gx=-2*z*np.trace(inv@K.T@dk)
    check(abs(gx)<1e-18,'former independent return normal vanishes at saturation')
    return {'active_columns_replayed':DIM,'source_columns_active':8,'full_source_rank':16,
            'full_work_dimension':65536,'oldRIGHT_factor':2,'inactive_blank_factor':256,
            'family_integer_identities_exact':True,'native16_inventory':dict(Counter(g[0] for g in BASE)),
            'full_cotangent_error':coterr,'all16_occurrence_max_error':worst,
            'actual_stage15_G_source':float(fullG),'independent_final_return_source':float(2*gx),
            'huge_clock_diagonalized':False}, (A,B,embed,Q)

# Third-order interval Taylor arithmetic: coefficient k = f^(k)/k!.
class Jet:
    def __init__(self,v):
        self.a=[iv(t) for t in v] if isinstance(v,(list,tuple)) else [iv(v),iv(0),iv(0),iv(0)]
    def __add__(self,o):
        o=asjet(o);return Jet([a+b for a,b in zip(self.a,o.a)])
    __radd__=__add__
    def __neg__(self):return Jet([-v for v in self.a])
    def __sub__(self,o):return self+-asjet(o)
    def __rsub__(self,o):return asjet(o)+-self
    def __mul__(self,o):
        o=asjet(o);return Jet([sum((self.a[j]*o.a[k-j] for j in range(k+1)),iv(0)) for k in range(4)])
    __rmul__=__mul__
    def inv(self):
        b=[1/self.a[0]]
        for k in range(1,4):b.append(-sum((self.a[j]*b[k-j] for j in range(1,k+1)),iv(0))/self.a[0])
        return Jet(b)
    def __truediv__(self,o):return self*asjet(o).inv()
    def __rtruediv__(self,o):return asjet(o)*self.inv()
    def __pow__(self,n):
        if not isinstance(n,int):raise ValueError('integer powers only')
        if n<0:return self.inv()**(-n)
        r=Jet(1)
        for _ in range(n):r=r*self
        return r
    def sqrt(self):
        b=[mp.iv.sqrt(self.a[0])]
        for k in range(1,4):
            b.append((self.a[k]-sum((b[j]*b[k-j] for j in range(1,k)),iv(0)))/(2*b[0]))
        return Jet(b)
    def log(self):
        # derivative f'/f; integrate its Taylor coefficients.
        der=Jet([self.a[1],2*self.a[2],3*self.a[3],0])*self.inv()
        return Jet([mp.iv.log(self.a[0]),der.a[0],der.a[1]/2,der.a[2]/3])

def asjet(x):return x if isinstance(x,Jet) else Jet(x)


def ratfun_jet(expr,t,base,width=0):
    num,den=sp.fraction(sp.cancel(expr))
    X=Jet([iv([str(base-width),str(base+width)]),1,0,0])
    def hor(poly):
        value=Jet(0)
        for c in sp.Poly(poly,t).all_coeffs():value=value*X+iv(c)
        return value
    return hor(num)/hor(den)

PAIRS=[(a,b) for a in range(4) for b in range(a+1,4)]
ETA=sp.diag(1,-1,-1,-1)
V0=sp.Matrix([1,sp.Rational(1,10),-sp.Rational(1,5),sp.Rational(1,20)])
V1=sp.Matrix([sp.Rational(1,5),sp.Rational(2,5),sp.Rational(1,10),-sp.Rational(3,10)])
BASE_Y=[sp.Rational(j-20,1000) for j in range(42)]
BASE_Y[40]=sp.Rational(19,100);BASE_Y[41]=-sp.Rational(13,100)

def operands(y):
    e=sp.eye(4)+sp.Matrix(4,4,y[:16]);ei=e.inv();g=e.T*ETA*e;gi=g.inv()
    ws=[]
    for mu in range(4):
        om=sp.zeros(4)
        for j,(a,b) in enumerate(PAIRS):om[a,b]=y[16+6*mu+j];om[b,a]=-y[16+6*mu+j]
        ws.append(om*ETA)
    R=sp.Integer(0)
    for mu in range(4):
        for nu in range(4):
            F=(ws[mu]*ws[nu]-ws[nu]*ws[mu])*ETA
            R+=(ei[mu,:]*F*ei[nu,:].T)[0]
    f=sp.cancel(e.det()*R/2)
    q=sp.cancel(y[40]**2*(V0.T*gi*V0)[0]+y[41]**2*(V1.T*gi*V1)[0])
    return f,q

def price_jets(f,q):
    p=Jet(PPI);tau=p*p
    x=tau*f;y=tau*q
    ee=p*p*(1+x);ell=4*ee*(1-ee);b=p-p*p*y;BB=4*b*b*(1-b*b)
    AA=ell+(1-ell)*BB
    report=(AA+BB)*ZETAI-AA*BB*(ZETAI**2)
    alpha=4*p*p;gamma=p*p
    oldc=(1-alpha*gamma*report*(1-gamma*report)).sqrt()
    click=(1-oldc)/2
    J=-8*(1-click*ZETAI).log() # the fixed -8log(1-zeta) baseline is carried separately
    return report,click,J


def convergent_above(alpha,minq):
    a=alpha;p0,p1=0,1;q0,q1=1,0
    for _ in range(1000):
        k=int(mp.floor(a));p0,p1=p1,k*p1+p0;q0,q1=q1,k*q1+q0
        if q1>=minq:
            check(math.gcd(p1,q1)==1,'coprime rotation convergent')
            return p1,q1
        a=1/(a-k)
    raise ArithmeticError('continued fraction did not terminate at requested resolution')

def compile_probability(target,Pnum,Qden):
    # m=2t+1. The exact Golden angular variable is theta/pi, never a fitted angle.
    x=mid(target);phi=mp.asin(mp.sqrt(x))
    beta=(phi-THETA)/(2*mp.pi);beta=beta-mp.floor(beta)
    k=int(mp.nint(beta*Qden))%Qden
    tt=(k*pow(Pnum,-1,Qden))%Qden
    m=2*tt+1
    sine=mp.iv.sin(m*THETAI);cosine=mp.iv.cos(m*THETAI)
    xi=sine**2
    check(low(sine)>0 and low(cosine)>0,'both actual branch amplitudes have the required sign')
    amplitude_error=mp.iv.sqrt((cosine-mp.iv.sqrt(1-target))**2+(sine-mp.iv.sqrt(target))**2)
    check(0<low(xi)<high(xi)<mp.mpf('.5'),'real compiled probability collar')
    # Actual interval check; the continued-fraction theorem is not used as an unverified numerical certificate.
    err=mag(xi-target)
    angular_bound=3*mp.pi/Qden
    analytic_prob=(2*mp.sqrt(high(target))+angular_bound)*angular_bound
    check(err<=analytic_prob,'actual word value inside constructive bound')
    check(m%2==1 and 1<=m<2*Qden,'positive odd original Golden count')
    return {'m':m,'actual_probability':interval_text(xi),'target_probability':interval_text(target),
            'probability_error_bound':text(err,35),'constructive_probability_bound':text(analytic_prob,35),
            'full_operator_approximation_interval':interval_text(amplitude_error)},xi


def full_stencil(outdir):
    t=sp.symbols('s',real=True)
    h=mp.mpf(1)/1000
    Pnum,Qden=convergent_above(THETA/mp.pi,10**14)
    # Verify the actual rational approximation with independent interval bounds.
    ai=THETAI/mp.iv.pi
    check(mag(ai-iv(Fraction(Pnum,Qden)))<mp.mpf(1)/(Qden*Qden),'verified rational angle approximant')
    f0,q0=operands(BASE_Y)
    rp,xp,jp=price_jets(Jet(iv(f0)),Jet(iv(q0)))
    P0=rp.a[0];X0=xp.a[0]
    alpha=4*PPI**2;gamma=PPI**2
    c0=mp.iv.sqrt(1-alpha*gamma*P0*(1-gamma*P0))
    dxdp=alpha*gamma*(1-2*gamma*P0)/(4*c0)
    Gamma=8*ZETAI*dxdp/(1-ZETAI*X0)
    check(low(Gamma)>0,'actual nonzero full recorded field gain')
    centre,Xcentre=compile_probability(X0,Pnum,Qden)
    words={'centre':centre};rows=[];maxerr=mp.mpf(0);sumerr=mp.mpf(0);sum_bound=mp.mpf(0)
    nonzero=0;sum_bound_iv=iv(0);sum_error_iv=iv(0);step_iv=iv(Fraction(1,1000))
    for j in range(42):
        y=BASE_Y[:];y[j]=y[j]+t
        f,q=operands(y)
        fj0=ratfun_jet(f,t,mp.mpf(0));qj0=ratfun_jet(q,t,mp.mpf(0))
        R0,_,J0=price_jets(fj0,qj0)
        Rgrad=R0.a[1]
        check(mag(J0.a[1]-Gamma*Rgrad)<mp.mpf('1e-70'),'exact interval field chain derivative')
        if mag(Rgrad)>mp.mpf('1e-30'):nonzero+=1
        ref=[];actual=[];errorvals=[]
        for label,s in [('minus',-h),('plus',h)]:
            rf,xf,jf=price_jets(ratfun_jet(f,t,s),ratfun_jet(q,t,s))
            item,act=compile_probability(xf.a[0],Pnum,Qden)
            words[f'{j:02d}_{label}']=item
            ref.append(jf.a[0]);actual.append(-8*mp.iv.log(1-ZETAI*act));errorvals.append(upper_iv(abs(act-xf.a[0])))
        qnative=(actual[1]-actual[0])/(2*step_iv*Gamma)
        discrepancy=mag(qnative-Rgrad)
        # Rigorous third derivative bound on the entire REAL field interval, not a fit at the midpoint.
        _,_,Jseg=price_jets(ratfun_jet(f,t,mp.mpf(0),h),ratfun_jet(q,t,mp.mpf(0),h))
        smooth_iv=upper_iv(abs(Jseg.a[3]))*step_iv**2/lower_iv(Gamma)
        compilation_iv=8*ZETAI*(errorvals[0]+errorvals[1])/(2*step_iv*lower_iv(Gamma)*(1-ZETAI))
        total_bound_iv=smooth_iv+compilation_iv
        smooth_bound=high(smooth_iv);compilation_bound=high(compilation_iv);bound=high(total_bound_iv)
        sum_bound_iv+=total_bound_iv;sum_error_iv+=upper_iv(abs(qnative-Rgrad))
        check(discrepancy<=bound,'certified true native42 source error')
        maxerr=max(maxerr,discrepancy);sumerr+=discrepancy;sum_bound+=bound
        rows.append({'coordinate':j,'sector':'coframe' if j<16 else ('connection' if j<40 else 'matter'),
                     'original_report_derivative':interval_text(Rgrad),'native_source':interval_text(qnative),
                     'absolute_error_bound_observed':text(discrepancy,30),
                     'proved_error_bound':text(bound,30),'smooth_bound':text(smooth_bound,30),
                     'compiler_bound':text(compilation_bound,30)})
    mmax=max(w['m'] for w in words.values());mmin=min(w['m'] for w in words.values())
    Tmax=(mmax-mmin)//2
    count={'G':mmax,'CX':9+12*Tmax,'SourceI':6+4*Tmax}
    N=sum(count.values())
    for w in words.values():
        ng=(mmax-w['m'])//2;nz=Tmax-ng
        check(ng>=0 and nz>=0,'nonnegative matched padding')
        check(w['m']+2*ng==mmax,'matched Golden inventory')
        check(9+12*(ng+nz)==count['CX'] and 6+4*(ng+nz)==count['SourceI'],'matched exact work inventory')
        check(w['m']+15+18*ng+16*nz==N,'matched true raw duration')
        w['padding_I_G']=ng;w['padding_I_Z']=nz
    programme={'format':'d0-positive-word-with-exact-repetitions-v1','input_commit':PIN,
       'semantics':'Finite fully unrolled word; repetitions are compact notation, no free runtime loop assumed.',
       'macros':{'seed':[{'op':a,'wires':list(b)} for a,b in SEED],
                 'Z_query':[{'op':a,'wires':list(b)} for a,b in ZWORD],
                 'I_G':['G11','Z_query','G11','Z_query'],
                 'I_Z':['Z_query','Z_query']},
       'word_template':['seed','CX(11,10)','Z_query','G11 repeated m','CX(11,10)',
                        'I_G repeated padding_I_G','I_Z repeated padding_I_Z'],
       'same_inventory':count,'expanded_calls_per_word':N,'words':words}
    (outdir/'programmes.json').write_text(json.dumps(programme,indent=2,sort_keys=True),encoding='utf-8')
    check(nonzero>20,'off-shell test has many nonzero independent field rows')
    check(sumerr<mp.mpf('1e-9'),'native covector accuracy in dual max norm')
    return {'test_kind':'42 independent pointwise Palatini coordinates, not original finite-mesh solve',
       'field_step':str(Fraction(1,1000)),'actual_original_report':interval_text(P0),
       'actual_good_record_gain':interval_text(Gamma),'all_42_coordinates':rows,
       'max_coordinate_error':text(maxerr,30),'dual_max_norm_error':text(sumerr,30),
       'dual_max_norm_proved_bound':text(high(sum_bound_iv),30),'dual_bound_outward_interval':interval_text(sum_bound_iv),
       'actual_error_sum_outward_interval':interval_text(sum_error_iv),'nonzero_test_rows':nonzero,
       'programmes':len(words),'continued_fraction_p':Pnum,'continued_fraction_q':Qden,
       'native_G_power_range':[mmin,mmax],'same_inventory':count,'expanded_calls_per_word':N,
       'whole_Hodge_mode_count_per_word':425*N*65536,
       'full_heat_contrast':'exactly zero: equal N,full carrier,reflection signature',
       'large_repeated_words_iterated':False,'runtime_field_reader_implemented':False}


def hostile_controls():
    # Retaining the report does not force saturation: the unsaturated echo keeps a nonzero normal.
    c=.61;s=math.sqrt(1-c*c);R=np.array([[c,-s],[s,c]])
    Z=np.diag([1.,-1.]);CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],float)
    U=np.kron(R,np.eye(2))@np.kron(Z,np.eye(2))@CNOT@np.kron(R.T,np.eye(2))
    i=np.eye(4)[:,[0]];P=i@i.T;M=np.diag([1,0,1,0])
    F=(M-P)@U@i;gap=float((F.T@F)[0,0])
    check(gap>1e-3,'unsaturated recorded echo is not silently identified')
    # A fixed projective report is not a full physical variational-domain theorem.
    return {'unsaturated_echo_gap':gap,'full_task_selection_proved':False,
            'all_fine_history_equivalence_claimed':False}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    native,_=primitive_replay()
    out={'input_commit':PIN,'native_family':native,'stencil':full_stencil(args.out),
         'negative_controls':hostile_controls(),'checks':CHECKS,
         'status':'PASS_NATIVE_RECORD_SATURATED_42_SOURCE_STENCILS',
         'GR_closed':False,'physical_variation_domain_derived':False,'same_runtime_field_compiler_proved':False,
         'new_all42_stationary_root':False,'Lean_or_CI_run':False,
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (args.out/'result.json').write_text(json.dumps(out,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps({'checks':CHECKS,'status':out['status'],'max_error':out['stencil']['max_coordinate_error'],
                      'norm_bound':out['stencil']['dual_max_norm_proved_bound'],
                      'calls':out['stencil']['expanded_calls_per_word'],'GR_closed':False},indent=2))
if __name__=='__main__':main()
