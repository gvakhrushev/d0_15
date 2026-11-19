#!/usr/bin/env python3
"""Literal all128 two-round normalization, polar completion and true Book source.

Native Fourier fixture, not the complete 256-site primary metric. All 16384
ordered histories are used; oldRIGHT is retained as the declared multiplicity
128 in the unnormalized feedback trace. No physical Info law is assigned.
Analytical identities are proved in PROOF.md; floating tests have tolerances.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm, solve_sylvester
import sympy as sp

P = (np.sqrt(5.0) - 1.0) / 2.0
ELL = np.log(1.0 / P)
Z = 2.0**-20
RIGHT = 128
ORDER = (0, 2, 3, 1)
I = np.eye(16, dtype=complex)
CHECKS: list[str] = []


def require(ok: bool, name: str) -> None:
    if not bool(ok):
        raise ArithmeticError(name)
    CHECKS.append(name)


def adj(a: np.ndarray) -> np.ndarray:
    return a.conj().T


def hs(a: np.ndarray) -> float:
    return float(np.linalg.norm(a))


def real_trace(a: np.ndarray) -> float:
    v = np.trace(a)
    if abs(v.imag) > 1e-8 * max(1.0, abs(v.real)):
        raise ArithmeticError('non-real trace')
    return float(v.real)


def positive_sqrt(a: np.ndarray) -> np.ndarray:
    v, u = np.linalg.eigh((a + adj(a)) / 2)
    if v.min() <= 1e-12:
        raise ArithmeticError('outside strict positive chart')
    return (u * np.sqrt(v)) @ adj(u)


def logdet(a: np.ndarray) -> float:
    v = np.linalg.eigvalsh((a + adj(a)) / 2)
    if v.min() <= 0:
        raise ArithmeticError('nonpositive determinant argument')
    return float(np.log(v).sum())


def creators() -> list[np.ndarray]:
    out = []
    for role in range(4):
        c = np.zeros((16, 16), complex)
        earlier = ORDER[:ORDER.index(role)]
        for bits in range(16):
            if not (bits >> role) & 1:
                c[bits | (1 << role), bits] = (-1)**sum((bits >> j) & 1 for j in earlier)
        out.append(c)
    return out


def native(theta: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Reimplementation of pinned native_round, with all defect first jets.

    The actual owner uses nu=3/5, role-1 boost and L4 character (i,i,-1,-i).
    Walsh pairs are first-row Julia blocks. Labels interleave port 0/1.
    """
    c = creators()
    boost = c[0] @ adj(c[1]) + c[1] @ adj(c[0])
    u = expm(theta * boost)
    du = u @ boost
    phases = (1j, 1j, -1.0, -1j)
    words, jets = [], []
    for r in range(4):
        fixed = 0.6 * c[r]
        x = fixed @ (u if r == 1 else I) * phases[r]
        dx = fixed @ du * phases[r] if r == 1 else np.zeros_like(I)
        left = positive_sqrt(I - x @ adj(x))
        right = positive_sqrt(I - adj(x) @ x)
        dl = solve_sylvester(left, left, -dx @ adj(x) - x @ adj(dx))
        dr = solve_sylvester(right, right, -adj(dx) @ x - adj(x) @ dx)
        l0 = positive_sqrt(I - fixed @ adj(fixed))
        r0 = positive_sqrt(I - adj(fixed) @ fixed)
        zero = np.zeros_like(I)
        for w, dw in zip(((x,left),(adj(x),right),(-fixed,-l0),(-adj(fixed),-r0)),
                         ((dx,dl),(adj(dx),dr),(zero,zero),(zero,zero))):
            words.extend((w,w)); jets.extend((dw,dw))
    row, drow = [], []
    for label in range(32):
        signs = [(-1)**(bin(label & j).count('1') & 1) for j in range(32)]
        for coeff in range(2):
            row.append(sum((signs[j]*words[j][coeff] for j in range(32)), np.zeros_like(I))/32)
            drow.append(sum((signs[j]*jets[j][coeff] for j in range(32)), np.zeros_like(I))/32)
    a, da = row[0], drow[0]
    k, dk = [], []
    for j, n in enumerate(row):
        shared = adj(n) @ a
        dshared = adj(drow[j]) @ a + adj(n) @ da
        k.extend(((I if j == 0 else np.zeros_like(I))-2*P**2*shared, -2*P*np.sqrt(P)*shared))
        dk.extend((-2*P**2*dshared, -2*P*np.sqrt(P)*dshared))
    return np.asarray(k), np.asarray(dk), a, da


def effects(k: np.ndarray) -> np.ndarray:
    return np.einsum('hji,hjk->hik', k.conj(), k, optimize=True)


def gram(v: np.ndarray, dv: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray | None]:
    v = v.reshape(-1,16)
    n = adj(v) @ v
    if dv is None:
        return n, None
    dv = dv.reshape(-1,16)
    return n, adj(dv) @ v + adj(v) @ dv


def transfer(k: np.ndarray, dk: np.ndarray, x: np.ndarray, dx: np.ndarray,
             weights: np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    n, dn = np.zeros_like(I), np.zeros_like(I)
    for j in range(128):
        n += weights[j] * adj(k[j]) @ x @ k[j]
        dn += weights[j] * (adj(dk[j])@x@k[j] + adj(k[j])@dx@k[j] + adj(k[j])@x@dk[j])
    return n, dn


def normalized_complement(n: np.ndarray, dn: np.ndarray,
                          a: np.ndarray, da: np.ndarray) -> dict:
    sqrt_n = positive_sqrt(n)
    r = np.linalg.inv(sqrt_n)
    dsqrt = solve_sylvester(sqrt_n, sqrt_n, dn)
    dr = -r @ dsqrt @ r
    corner = a @ r
    dcorner = da @ r + a @ dr
    f = I - adj(corner)@corner
    df = -adj(dcorner)@corner-adj(corner)@dcorner
    g = adj(a)@a
    dg = adj(da)@a+adj(a)@da
    q = (1-Z)*n+Z*g
    dq = (1-Z)*dn+Z*dg
    j_split = RIGHT*(logdet(n)-logdet(q))
    dj_split = RIGHT*(real_trace(np.linalg.solve(n,dn))-real_trace(np.linalg.solve(q,dq)))
    j_direct = -RIGHT*float(np.log1p(-Z*np.linalg.eigvalsh((f+adj(f))/2)).sum())
    dj_direct = RIGHT*Z*real_trace(np.linalg.solve(I-Z*f,df))
    return dict(j=j_direct,dj=dj_direct,j_split=j_split,dj_split=dj_split,
                corner=corner,dcorner=dcorner,normalizer=r)


def hjr(theta: float, rho: np.ndarray) -> tuple[dict,np.ndarray]:
    k, dk, a, da = native(theta)
    h=.25; alpha=P**2*h**2/128; m=4; beta=m*alpha
    delta=(16/h)**2*a@a
    ddelta=(16/h)**2*(da@a+a@da)
    b=k[0]; db=dk[0]
    bm=np.linalg.matrix_power(b,m)
    bm1=np.linalg.matrix_power(b,m-1)
    zz=real_trace(bm)
    dbm=sum((np.linalg.matrix_power(b,j)@db@np.linalg.matrix_power(b,m-1-j) for j in range(m)),np.zeros_like(I))
    f=(1-Z)*I+Z*bm
    heat=np.log(RIGHT*128**2*zz)/beta
    loop=-RIGHT*float(np.log1p(-Z*np.linalg.eigvalsh(I-bm)).sum())
    rayleigh=real_trace(rho@delta)
    dh=-real_trace(bm1@ddelta)/zz
    dj=RIGHT*beta*Z*real_trace(np.linalg.solve(f,bm1@ddelta))
    dr=real_trace(rho@ddelta)
    w=rho-bm1/zz+RIGHT*beta*Z*np.linalg.solve(f,bm1)
    return dict(value=float(heat+loop+rayleigh),heat=float(heat),loop=loop,rayleigh=rayleigh,
                source=dh+dj+dr,heat_source=dh,loop_source=dj,matter_source=dr,
                operator_source=real_trace(w@ddelta),
                blank_trace=zz,blank_trace_source=real_trace(dbm),beta=float(beta)), delta


def exact_checks() -> dict:
    aa,z=sp.symbols('aa z',positive=True)
    n=sp.Matrix([[sp.Rational(3,5),sp.Rational(1,10)],[sp.Rational(1,10),sp.Rational(4,5)]])
    a=sp.Matrix([[sp.Rational(1,3),sp.Rational(1,7)],[0,sp.Rational(1,4)]])
    g=a.T*a
    q=(1-z)*n+z*g
    require(n*g != g*n, 'exact noncommuting determinant control')
    require(sp.cancel(((1-z)*aa**2*n+z*aa**2*g).det()/(aa**2*n).det()-q.det()/n.det())==0,
            'common scalar cancels from complete polar determinant')
    require(sp.diff(sp.cancel(((1-z)*aa**2*n+z*aa**2*g).det()/(aa**2*n).det()),aa)==0,
            'common scalar full derivative cancels exactly')
    ell,t=sp.symbols('ell t',positive=True)
    amp=sp.Rational(3,2)-t/(2*ell); prob=2-t/ell
    extra_tilt=1-t/(2*ell); extra_preserve=1
    require(sp.simplify((-1+extra_tilt)+sp.Rational(1,2)-(-1+amp))==0,
            'original Kraus extra tilt yields absolute amplitude ratio')
    require(extra_tilt.subs(t,ell)==sp.Rational(1,2) and amp.subs(t,ell)==1 and prob.subs(t,ell)==1,
            'uniform target does not equate unmarked extra factor with absolute weights')
    return {'noncommuting_polar_scalar_cancellation':'EXACT',
            'extra_on_unmarked_Kraus_to_target_q_t':'1-t/(2 ln phi)',
            'extra_on_already_marked_Kraus_preserving_q_t':extra_preserve}


def primary_application() -> dict:
    """Consume the proved primary local source; recompute its exact F/R counts.

    No full Dirac spectrum or geometric root is recomputed here.
    The integer routing is the original_counts definition at the pinned owner.
    """
    counts=[0]*256
    def radical_sign(a,b):
        if a==0: return (b>0)-(b<0)
        if b==0 or (a>0)==(b>0): return (a>0)-(a<0)
        d=a*a-5*b*b
        return ((d>0)-(d<0))*(1 if a>0 else -1)
    def visit(rem,depth,left,width):
        if rem==0:
            index=0
            for axis in range(4):
                ca=2*left[axis][0]+width[axis][0]
                cb=2*left[axis][1]+width[axis][1]
                aa,bb=4*(2*ca-cb),4*cb
                digit=0
                for cut in range(1,4):
                    if radical_sign(aa-4*cut,bb)>=0: digit=cut
                    else: break
                index=index*4+digit
            counts[index]+=1
            return
        axis=depth%4
        wf=width.copy(); wa,wb=width[axis]
        wf[axis]=(wb,wa-wb)
        visit(rem-1,depth+1,left.copy(),wf)
        if rem>=2:
            lr,wr=left.copy(),width.copy(); la,lb=left[axis]
            lr[axis]=(la+wb,lb+wa-wb)
            wr[axis]=(wa-wb,2*wb-wa)
            visit(rem-2,depth+1,lr,wr)
    visit(20,0,[(0,0)]*4,[(1,0)]*4)
    require(sum(counts)==10946 and min(counts)==29 and max(counts)==78,
            'primary uses the actual unequal cost20 F/R counts')
    def index(x): return ((x[0]*4+x[1])*4+x[2])*4+x[3]
    w=(1,1,2,2); up=(2,1,2,2)
    r1=Fraction(256*counts[index(w)],10946)
    r2=Fraction(256*counts[index(up)],10946)
    lower=Fraction(7,2048)*Fraction(3,5)**7*min(r1,r2)
    upper=Fraction(7,2048)*Fraction(5,8)**7*max(r1,r2)
    require(0<lower<upper,'primary preparation coefficient has a strict rational sign certificate')
    # This is the inherited local all128 formula, not a different Fourier seed.
    coefficient=-7*P**7*np.sqrt(float(r1*r2))/2048
    require(-float(upper)<coefficient<-float(lower),
            'same-primary HJR residual survives physical normalization with its exact sign')
    return {'scope':'substitution into inherited PRIMARY_CAR_PREPARATION_SOURCE, equations 5-8',
            'w':list(w),'next_u':list(up),'count_w':counts[index(w)],'count_next_u':counts[index(up)],
            'rho_w':str(r1),'rho_next_u':str(r2),
            'preparation_source':'-[7 p^7 sqrt(rho_w rho_next_u)/2048] t + O(t^3)',
            'linear_coefficient_approx':float(coefficient),
            'positive_magnitude_lower_rational':str(lower),'positive_magnitude_upper_rational':str(upper),
            'full_record_norm_preparation_source':'0 exactly by completeness',
            'polar_common_scalar_feedback_source':'0 exactly; not a compensating physical source',
            'primary_HJR_root':False,
            'not_claimed':'full paid actuator work; natively selected Book Info; full primary replay'}

def main() -> dict:
    exact=exact_checks()
    primary=primary_application()
    theta=.08; t=.7
    k,dk,a,da=native(theta)
    cost=np.tile([1.,2.],64)
    e=effects(k)
    normal,dnormal=gram(k,dk)
    require(hs(normal-I)<3e-12 and hs(dnormal)<3e-12,'full128 isometry and complete field first jet')
    require(hs(e[1::2].sum(axis=0)-4*P**3*a@a)<3e-13,'actual port effect all64 labels')
    step=1e-6
    kp=native(theta+step)[0]; km=native(theta-step)[0]
    require(hs((kp-km)/(2*step)-dk)<2e-8,'all128 analytic defect/source jets match differences')
    # H[first,second] is the complete second @ first chronological word.
    hist=np.einsum('bik,akj->abij',k,k,optimize=True).reshape(-1,16,16)
    dhist=(np.einsum('bik,akj->abij',dk,k,optimize=True)+np.einsum('bik,akj->abij',k,dk,optimize=True)).reshape(-1,16,16)
    cc=(cost[:,None]+cost[None,:]).reshape(-1)
    n0,dn0=gram(hist,dhist)
    require(hist.shape==(16384,16,16) and hs(n0-I)<5e-12 and hs(dn0)<5e-12,'all16384 histories normalized with zero complete norm source')
    factors=np.exp(-.5*t*cc)[:,None,None]
    marked=factors*hist; dmarked=factors*dhist
    nt,dnt=gram(marked,dmarked)
    nt_t,dnt_t=gram(marked,-.5*cc[:,None,None]*marked)
    w1=np.exp(-t*cost)
    n1,dn1=transfer(k,dk,I,np.zeros_like(I),w1)
    n2,dn2=transfer(k,dk,n1,dn1,w1)
    require(hs(n2-nt)<4e-12 and hs(dn2-dnt)<4e-12,'marked norm and field source agree with full history enumeration')
    formula=np.exp(-t)*(I+(np.exp(-t)-1)*e[1::2].sum(axis=0))
    require(hs(n1-formula)<3e-13,'exact one-round operator normalizer')
    # Mean total code price, both Schrödinger history sum and Heisenberg sum.
    c2=np.einsum('h,hij->ij',cc,effects(hist),optimize=True)
    c1=np.einsum('h,hij->ij',cost,e,optimize=True)
    c2_transfer=c1+transfer(k,dk,c1,np.zeros_like(I),np.ones(128))[0]
    c2_moment=-gram(hist,-.5*cc[:,None,None]*hist)[1]
    require(hs(c2-c2_transfer)<5e-12 and hs(c2-c2_moment)<5e-12,'same complete paid cost from transfer history and norm derivative')
    vals,vecs=np.linalg.eigh(nt)
    spread=float(vals[-1]-vals[0])
    require(spread>1e-6,'marked normalizer is genuinely nonscalar on original native fixture')
    qmid=vals[-1]/(vals[-1]+vals[0])
    require(abs(qmid-.5)>1e-6,'conditioning fails affine mixture on original input states')
    # The REAL output filter keeps every original history also on failure.
    # A single sqrt(I-N) is only a Gram compression, not the retained tape.
    fail_factor=np.sqrt(1-np.exp(-t*cc))[:,None,None]
    failed=fail_factor*hist; dfailed=fail_factor*dhist
    nf,dnf=gram(failed,dfailed)
    require(failed.shape==(16384,16,16) and hs(nt+nf-I)<3e-12 and hs(dnt+dnf)<3e-12,
            'physical post-filter retains all16384 failures and their full first source')
    b=k[0]; db=dk[0]
    blank=b@b; dblank=db@b+b@db
    at=np.exp(-t)*blank; dat=np.exp(-t)*dblank
    polar=normalized_complement(nt,dnt,at,dat)
    require(abs(polar['j']-polar['j_split'])<2e-11 and abs(polar['dj']-polar['dj_split'])<2e-12,
            'complete noncommuting polar determinant and first source')
    ni=polar['normalizer']
    require(hs(ni@nt@ni-I)<3e-12,'full polar record isometry')
    # Correct scalar gauge cancellation on the actual noncommuting fixture.
    scale=.77; dscale=.21
    polar_g=normalized_complement(scale**2*nt,scale**2*dnt+2*scale*dscale*nt,
                                 scale*at,scale*dat+dscale*at)
    require(abs(polar_g['j']-polar['j'])<2e-12 and abs(polar_g['dj']-polar['dj'])<2e-12,
            'changing unnormalized common gauge cannot change true normalized feedback source')
    # Root-free Grassmannian evaluation. No large output-space projector is built.
    ninv=np.linalg.inv(nt)
    angle=at@ninv@adj(at)
    dangle=dat@ninv@adj(at)+at@ninv@adj(dat)-at@ninv@dnt@ninv@adj(at)
    denom=(1-Z)*I+Z*angle
    projection_j=-RIGHT*float(np.log1p(-Z*np.linalg.eigvalsh(I-angle)).sum())
    projection_dj=-RIGHT*Z*real_trace(np.linalg.solve(denom,dangle))
    require(abs(projection_j-polar['j'])<2e-12 and abs(projection_dj-polar['dj'])<2e-12,
            'root-free range-projection source matches normalized Book determinant')
    # Any invertible right change, not only a scalar, is a representation gauge
    # for this normalized feedback trace with fixed active embedding.
    change=np.diag(np.linspace(.8,1.3,16)).astype(complex)
    change[0,3]=.12j; change[3,0]=.04
    dchange=np.zeros_like(I); dchange[0,3]=.07; dchange[4,2]=.11j
    gl_n=adj(change)@nt@change
    gl_dn=adj(dchange)@nt@change+adj(change)@dnt@change+adj(change)@nt@dchange
    gl_a=at@change; gl_da=dat@change+at@dchange
    gl=normalized_complement(gl_n,gl_dn,gl_a,gl_da)
    require(abs(gl['j']-polar['j'])<2e-12 and abs(gl['dj']-polar['dj'])<2e-12,
            'all moving invertible input-coordinate gauges preserve true feedback source')
    # The horizon-dependent Doob/polar factorization includes both step normalizers.
    n1s=positive_sqrt(n1); n1i=np.linalg.inv(n1s)
    kfirst=np.asarray([np.sqrt(w1[j])*n1s@k[j]@ni for j in range(128)])
    ksecond=np.asarray([np.sqrt(w1[j])*k[j]@n1i for j in range(128)])
    require(hs(effects(kfirst).sum(axis=0)-I)<3e-12 and hs(effects(ksecond).sum(axis=0)-I)<3e-12,
            'finite two-round polar dynamics normalized at each stage')
    doob=np.einsum('bik,akj->abij',ksecond,kfirst,optimize=True).reshape(-1,16,16)
    expected=marked@ni
    require(hs(doob-expected)<3e-12,'normalized stage words telescope on every retained history')
    # Marked conditional law equals the new isometry only with changed input.
    rho=np.diag(np.arange(1,17,dtype=float)); rho=rho/np.trace(rho)
    ns=positive_sqrt(nt); zrho=real_trace(rho@nt)
    rho_t=ns@rho@ns/zrho
    require(hs(rho_t-rho)>1e-6,'matching conditional law changes the prepared input')
    q_mark=np.einsum('hij,ji->h',effects(marked),rho,optimize=True).real/zrho
    q_doob=np.einsum('hij,ji->h',effects(doob),rho_t,optimize=True).real
    require(np.max(np.abs(q_mark-q_doob))<2e-13,'all conditional probabilities agree with exact changed-input dictionary')
    # Purification Gram is altered, not a free oldRIGHT-preserving preparation.
    pur=np.sqrt(rho)
    prior=adj(pur)@pur
    changed_right=adj(pur)@nt@pur/zrho
    right_error=hs(changed_right-prior)
    require(right_error>1e-6,'normalized marked preparation generally changes oldRIGHT Gram')
    require(hs(adj(pur)@(nt+nf)@pur-prior)<2e-12,
            'keeping every failure restores the original RIGHT marginal exactly')
    # Reporting the extra flag adds its real complete entropy and paid branches.
    q0=np.einsum('hij,ji->h',effects(hist),rho,optimize=True).real
    qs=np.exp(-t*cc)*q0; qf=(1-np.exp(-t*cc))*q0
    def entropy(prob):
        pos=prob[prob>0]
        return float(-np.sum(pos*np.log(pos))/ELL)
    flagprob=np.exp(-t*cc)
    flagentropy=-(flagprob*np.log(flagprob)+(1-flagprob)*np.log1p(-flagprob))/ELL
    flag_gain=float(q0@flagentropy)
    require(abs(entropy(np.r_[qs,qf])-entropy(q0)-flag_gain)<3e-12,
            'reported filter information includes every history and its flag entropy')
    cost_success=float(cc@qs/zrho)
    cost_failure=float(cc@qf/(1-zrho))
    require(abs(zrho*cost_success+(1-zrho)*cost_failure-real_trace(rho@c2))<2e-12,
            'paid query cost is not the successful conditional mean')
    # Retained physical failure vs deterministic polar normalization are different.
    ff=I-adj(at)@at; dff=-adj(dat)@at-adj(at)@dat
    filter_j=-RIGHT*float(np.log1p(-Z*np.linalg.eigvalsh(ff)).sum())
    filter_dj=RIGHT*Z*real_trace(np.linalg.solve(I-Z*ff,dff))
    frozen=normalized_complement(nt,np.zeros_like(I),at,dat)
    require(abs(filter_j-polar['j'])>1e-7,'physical filter and polar normalization have different complete feedback')
    require(abs(frozen['dj']-polar['dj'])>1e-9,'freezing operator-normalizer source is rejected')
    f0=I-adj(blank)@blank
    wrong=scale*f0
    correct=I-scale**2*adj(blank)@blank
    require(hs(wrong-correct)>.01,'multiplying complementary F is not scaling an active amplitude')
    # Check polar field derivative by a separate finite-difference calculation.
    def polar_value(th: float) -> float:
        kk,dd,_,_=native(th)
        n,nn=transfer(kk,dd,I,np.zeros_like(I),w1)
        n,nn=transfer(kk,dd,n,nn,w1)
        aa=np.exp(-t)*kk[0]@kk[0]
        return normalized_complement(n,np.zeros_like(I),aa,np.zeros_like(I))['j']
    hfd=2e-5
    fd=(polar_value(theta+hfd)-polar_value(theta-hfd))/(2*hfd)
    require(abs(fd-polar['dj'])<3e-9,'actual polar field first source agrees with direct finite difference')
    full,delta=hjr(theta,rho)
    require(abs(full['source']-full['operator_source'])<3e-10,'full HJR source equals original spectral plus matter operator source')
    hfd=1e-4
    fdh=(hjr(theta+hfd,rho)[0]['value']-hjr(theta-hfd,rho)[0]['value'])/(2*hfd)
    require(abs(fdh-full['source'])<2e-5,'full HJR source independently differentiated as a scalar value')
    require(abs(full['source'])>1e-5,'normalized complete-record log norm is not the full HJR action')
    # A normalized LEFT variation preserves oldRIGHT while allowing a genuine source.
    gen=np.zeros_like(I); gen[0,3]=1; gen[3,0]=-1
    drho=gen@rho-rho@gen
    prep_source=real_trace(delta@drho)
    # Do not assume this chosen fixture direction is nonzero.
    # Commutator choice is exact and gives a nonzero source whenever [Delta,rho]!=0.
    gen2=delta@rho-rho@delta
    drho2=gen2@rho-rho@gen2
    prep_descent=-real_trace(delta@drho2)
    require(prep_descent< -1e-10,'explicit oldRIGHT-preserving preparation descent for unchanged HJR fixture')
    return {
      'status':'PASS', 'checks':len(CHECKS),'names':CHECKS,
      'scope':{'native':'original L4 Fourier-character full128; one proper-link boost',
               'theta':theta,'marker_t':t,'histories':16384,'data_dimension':16,
               'oldRIGHT_feedback_multiplicity':RIGHT,
               'not_replayed':'256-site primary spectrum, all42 geometry, Lean and independent review',
               'marker':'analytical; physical filter includes new failure; polar word not claimed natively compiled',
               'book_gain_selected':False,'GR_closed':False},
      'exact':exact, 'primary_application':primary,
      'values':{'complete_norm_error':hs(n0-I),'complete_norm_source_error':hs(dn0),
                'marked_normalizer_min':float(vals[0]),'marked_normalizer_max':float(vals[-1]),
                'marked_normalizer_spread':spread,'marked_normalizer_field_source_norm':hs(dnt),
                'noncommuting_N_G_norm':hs(nt@adj(at)@at-adj(at)@at@nt),
                'postselected_half_mixture_weight':float(qmid),
                'conditional_preparation_RIGHT_change':right_error,
                'mean_two_round_reporting_cost':real_trace(rho@c2),
                'filter_success_probability':zrho,'filter_failure_probability':1-zrho,
                'query_cost_given_success':cost_success,'query_cost_given_failure':cost_failure,
                'extra_reported_flag_entropy_phi':flag_gain,
                'unmarked_heat_partition':full['blank_trace'],
                'unmarked_heat_partition_source':full['blank_trace_source'],
                'polar_feedback_value':polar['j'],'polar_feedback_source':polar['dj'],
                'range_projection_feedback_source':projection_dj,
                'frozen_normalizer_feedback_source':frozen['dj'],
                'filter_feedback_value':filter_j,'filter_feedback_source':filter_dj,
                'polar_source_finite_difference':fd,'full_HJR_source':full['source'],
                'HJR_heat_source':full['heat_source'],'HJR_feedback_source':full['loop_source'],
                'HJR_matter_field_source':full['matter_source'],
                'HJR_source_finite_difference':fdh,'oldRIGHT_preserving_HJR_descent':prep_descent}}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=main()
    text=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.write_text(text,encoding='utf-8')
    print(text,end='')
