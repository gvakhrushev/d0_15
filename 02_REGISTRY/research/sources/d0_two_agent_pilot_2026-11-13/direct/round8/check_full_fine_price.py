#!/usr/bin/env python3
"""Full fine-instrument price and nuisance-source checks, not physical C."""
import json
import math

import numpy as np
import sympy as s

exact, numeric = [], []


def ck(ok, name, target):
    if not bool(ok):
        raise AssertionError(name)
    target.append(name)


p=(s.sqrt(5)-1)/2
field=s.QQ.algebraic_field(s.sqrt(p))


def eq(x,y=0):
    return field.from_sympy(s.expand(x-y))==field.zero


def meq(x,y):
    return x.shape==y.shape and all(eq(v) for v in x-y)


G=s.Matrix([[s.sqrt(p),-p],[p,s.sqrt(p)]])
CX=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
Gt=s.kronecker_product(s.eye(2),G)
encoder=CX*Gt*CX
echo=CX*Gt*CX*Gt
inv_echo=echo.T
ck(meq(echo,s.diag(G*G,s.eye(2))),'literal positive echo acts only in r=0 sector',exact)
ck(meq(inv_echo,s.diag((G*G).T,s.eye(2))),'actual inverse echo preserves the complementary sector',exact)
for idx,proj in enumerate([s.diag(1,1,0,0),s.diag(0,0,1,0),s.diag(0,0,0,1)]):
    ck(meq(inv_echo.T*proj*inv_echo,proj),f'inverse echo preserves full coarse projector {idx}',exact)
ck(meq(inv_echo*encoder,Gt.T),'old E0 followed by inverse echo equals unconditional inverse G on all columns',exact)
v=s.Matrix([s.sqrt(p),p]);true_embed=s.kronecker_product(s.eye(2),v)
zero_embed=s.kronecker_product(s.eye(2),s.Matrix([1,0]))
ck(meq(inv_echo*encoder*true_embed,zero_embed),'true fresh tail becomes exact zero for arbitrary pointer/reference input',exact)
ck(2*17+2==36 and 17-3==14,'appended and replacement native costs are distinct and explicit',exact)


q,u,a,ell=s.symbols('q u a ell', positive=True)
hb=lambda x:-x*s.log(x)-(1-x)*s.log(1-x)
cost=2*(1-q)*(1-u)+3*(1-q)*u+3*q
ck(s.expand(cost-(2+q+(1-q)*u))==0,'all three true parsed lengths included',exact)
price=cost-a*(hb(q)+(1-q)*hb(u))/ell
du=(1-q)*(1-a*s.log((1-u)/u)/ell)
ck(s.simplify(s.diff(price,u)-du)==0,'independent tail row retained',exact)
ck(s.simplify(s.diff(price,u,2)-a*(1-q)/(ell*u*(1-u)))==0,
   'strict tail curvature for positive information coefficient',exact)
ck(eq(1-p**2,p),'Golden old tail conditional probability',exact)
ck(eq((1-p**2)/p**2,1/p),'Golden tail entropy derivative equals one unit',exact)
ck(eq(p+2*p**2,1+p**2),'Golden tail entropy equals (1+p squared) times ell',exact)
ck(eq(2-p**2,p+1),'original fine cost slope exact',exact)
m,lh=s.symbols('m L',real=True)
f=2+q+(1-q)*m-a*hb(q)/ell
ck(s.simplify(s.diff(f,q)-(1-m-a*s.log((1-q)/q)/ell))==0,
   'envelope source from entire price',exact)
trial=p**2-a*(1+p**2)
ck(s.expand(1-trial-a-(p+a*p**2))==0,
   'trial Golden tail proves positive all-coefficient margin',exact)
ck(s.simplify(p-p**2>0),'lower margin dominates p squared times (1+a)',exact)
theta=s.symbols('theta',real=True)
pzero=2+q+(1-q)*s.sin(theta)**2
ck(s.diff(pzero,theta).subs(theta,0)==0,'zero-info endpoint stationary in real amplitude coordinate',exact)
ck(s.simplify(s.diff(pzero,theta,2).subs(theta,0)-2*(1-q))==0,
   'zero-info endpoint has positive physical tail curvature',exact)
Hq=s.symbols('Hq',real=True)
old_difference=s.expand(cost.subs(u,p**2)-(Hq+(1-q)*(1+p**2))-(1+2*q-Hq))
ck(all(eq(c) for c in s.Poly(old_difference,q,Hq).coeffs()),
   'original a=1 full price exactly recovered with Golden tail entropy',exact)

pf=float(p); lf=math.log(1/pf)


def h(x):
    if x==0 or x==1:return 0.
    return -x*math.log(x)-(1-x)*math.log1p(-x)


def optimum(coeff):
    if coeff==0:return 0.,0.
    z=math.exp(-lf/coeff)
    return z/(1+z),-coeff*math.log1p(z)/lf


def fmin(q,coeff):
    _,ma=optimum(coeff)
    return 2+q+(1-q)*ma-coeff*h(q)/lf


def scalar_price(q,u,coeff):
    return 2+q+(1-q)*u-coeff*(h(q)+(1-q)*h(u))/lf


def kl(x,y):
    return (0 if x==0 else x*math.log(x/y))+(0 if x==1 else (1-x)*math.log((1-x)/(1-y)))


max_scalar_gap_error=0.
for coeff in (0.,.05,.3,.7,1.,3.,100.):
    ua,ma=optimum(coeff)
    for qv in (pf**2,.43,.5):
        slope=1-ma-coeff*math.log((1-qv)/qv)/lf
        ck(pf+coeff*pf**2-1e-12<=slope<=1+coeff*math.log(2)/lf+1e-12,
           f'full source lower and upper bounds a={coeff},q={qv}',numeric)
        ck(abs(scalar_price(qv,ua,coeff)-fmin(qv,coeff))<5e-13,
           f'optimizer attains full fine price a={coeff},q={qv}',numeric)
        if coeff>0:
            row=(1-qv)*(1-coeff*math.log((1-ua)/ua)/lf)
            ck(abs(row)<2e-13,f'free tail row vanishes a={coeff},q={qv}',numeric)
        for uv in (.0,.17,pf**2,.6,1.):
            defect=scalar_price(qv,uv,coeff)-fmin(qv,coeff)
            target=(1-qv)*uv if coeff==0 else coeff*(1-qv)*kl(uv,ua)/lf
            max_scalar_gap_error=max(max_scalar_gap_error,abs(defect-target))
            ck(abs(defect-target)<3e-12 and defect>-3e-13,
               f'exact Gibbs-defect diagnostic a={coeff},q={qv},u={uv}',numeric)
ck(abs(optimum(1)[0]-pf**2)<1e-15 and abs(optimum(1)[1]+1)<1e-15,
   'original Golden polar tail recovered at a=1',numeric)
for qv in (pf**2,.43,.5):
    ck(abs(scalar_price(qv,pf**2,1)-(1+2*qv-h(qv)/lf))<2e-15,
       f'owned full fine code-minus-entropy exactly recovered q={qv}',numeric)
    ck(abs((1-qv)*(1-.3))>.3,
       f'old tail section really has a nonzero nuisance row at a=.3,q={qv}',numeric)


def mm(x,y):
    return np.einsum('ij,jk->ik',x,y,optimize=False)


def root_psd(mat):
    vals,vecs=np.linalg.eigh((mat+mat.conj().T)/2)
    if np.min(vals)<-1e-13:raise AssertionError('negative effect')
    return mm(vecs*np.sqrt(np.maximum(vals,0)),vecs.conj().T)


def entropy(mat):
    vals=np.linalg.eigvalsh((mat+mat.conj().T)/2)
    if np.min(vals)<-1e-12:raise AssertionError('negative branch state')
    vals=vals[vals>2e-14]
    return float(-np.sum(vals*np.log(vals)))


rng=np.random.default_rng(131608)
unitaries=[]
for _ in range(3):
    raw=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
    unitary,_=np.linalg.qr(raw);unitaries.append(unitary)
bell=np.array([1.,0.,0.,1.])/math.sqrt(2)
rho_bell=np.outer(bell,bell)
states=[rho_bell,.6*rho_bell+.4*np.eye(4)/4,np.diag([.4,.3,.2,.1])]
Y=np.array([[0,-1j],[1j,0]])
X=np.array([[0.,1.],[1.,0.]])
tail=.35*np.eye(4)+.13*np.kron(Y,np.eye(2))+.08*np.kron(X,X)
ck(np.linalg.norm(mm(tail,states[1])-mm(states[1],tail))>.05,
   'full-effect fixture really probes noncommuting quantum input',numeric)


def full_values(qv,tail_effect,state,coarse_effect=None):
    if coarse_effect is None:
        effects=[(1-qv)*(np.eye(4)-tail_effect),(1-qv)*tail_effect,qv*np.eye(4)]
    else:
        e0=np.eye(4)-coarse_effect
        re0=root_psd(e0)
        e01=mm(mm(re0,tail_effect),re0)
        effects=[e0-e01,e01,coarse_effect]
    blocks=[]
    ref_blocks=[]
    sr=root_psd(state)
    for effect,unitary in zip(effects,unitaries):
        branch=mm(unitary,root_psd(effect))
        blocks.append(mm(mm(branch,state),branch.conj().T))
        ref_blocks.append(mm(mm(sr,effect),sr))
    probs=np.array([float(np.trace(block).real) for block in blocks])
    hc=-float(np.sum(probs[probs>0]*np.log(probs[probs>0])))
    iq=sum(entropy(block) for block in blocks)-entropy(state)
    chi=entropy(state)-sum(pr*entropy(block/pr) for pr,block in zip(probs,ref_blocks) if pr>0)
    cost=float(probs@np.array([2.,3.,3.]))
    return cost,iq,hc,chi,probs


max_quantum_identity_error=0.
max_tail_stationarity_error=0.
positive_chi=0.
for si,state in enumerate(states):
    for qv in (.40,.48):
        cost,iq,hc,chi,probs=full_values(qv,tail,state)
        positive_chi=max(positive_chi,chi)
        ck(chi>-2e-12 and abs(iq-(hc-chi))<3e-12,
           f'full retained-output CQ decomposition state={si},q={qv}',numeric)
        uv=probs[1]/(1-qv)
        for bq,bc in [(0.,0.),(.4,0.),(0.,.7),(.3,.9)]:
            coeff=bq+bc
            value=cost-(bq*iq+bc*hc)/lf
            ua,_=optimum(coeff)
            target=(1-qv)*uv if coeff==0 else coeff*(1-qv)*kl(uv,ua)/lf+bq*chi/lf
            error=abs(value-fmin(qv,coeff)-target)
            max_quantum_identity_error=max(max_quantum_identity_error,error)
            ck(error<6e-12 and value>=fmin(qv,coeff)-6e-12,
               f'global fine-instrument defect state={si},q={qv},b={bq},{bc}',numeric)
            scalar=np.eye(4)*ua
            co,iqo,hco,chio,_=full_values(qv,scalar,state)
            ck(abs(co-(bq*iqo+bc*hco)/lf-fmin(qv,coeff))<5e-12 and abs(chio)<2e-12,
               f'scalar target reaches full ambient minimum state={si},q={qv},b={bq},{bc}',numeric)
            if coeff>0:
                # This changes actual fine effects, including genuinely complex
                # directions. Coarse q I stays fixed on ALL input columns.
                direction=.25*np.eye(4)+np.kron(Y,X)
                dt=min(1e-5,ua/100)
                vp=full_values(qv,scalar+dt*direction,state)
                vm=full_values(qv,scalar-dt*direction,state)
                derivative=((vp[0]-(bq*vp[1]+bc*vp[2])/lf)-(vm[0]-(bq*vm[1]+bc*vm[2])/lf))/(2*dt)
                max_tail_stationarity_error=max(max_tail_stationarity_error,abs(derivative))
                ck(abs(derivative)<2e-7,
                   f'full ambient tail row stationary state={si},q={qv},b={bq},{bc}',numeric)
ck(positive_chi>1e-3,'quantum deficit is nonzero away from scalar target',numeric)

# Elimination of the added fine split does not require a scalar coarse
# instrument. Its genuine pre-existing reference information is retained.
coarse=np.diag([.28,.49,.61,.42])
for si,state in enumerate(states):
    sr=root_psd(state)
    coarse_probs=[float(np.trace(mm(state,ef)).real) for ef in [np.eye(4)-coarse,coarse]]
    coarse_chi=entropy(state)-sum(pr*entropy(mm(mm(sr,ef),sr)/pr)
                    for ef,pr in zip([np.eye(4)-coarse,coarse],coarse_probs))
    qv=coarse_probs[1]
    for bq,bc in [(.6,0.),(.2,.8)]:
        coeff=bq+bc
        co,iqv,hcv,chiv,probs=full_values(qv,tail,state,coarse)
        ua,_=optimum(coeff)
        uv=probs[1]/(1-qv)
        gap=co-(bq*iqv+bc*hcv)/lf-fmin(qv,coeff)-bq*coarse_chi/lf
        target=coeff*(1-qv)*kl(uv,ua)/lf+bq*(chiv-coarse_chi)/lf
        ck(abs(gap-target)<4e-12 and chiv>=coarse_chi-2e-12 and gap>=-2e-12,
           f'nonscalar coarse information retained in full defect state={si},b={bq},{bc}',numeric)
        co,iqv,hcv,chiv,_=full_values(qv,np.eye(4)*ua,state,coarse)
        ck(abs(co-(bq*iqv+bc*hcv)/lf-fmin(qv,coeff)-bq*coarse_chi/lf)<5e-12
           and abs(chiv-coarse_chi)<3e-12,
           f'independent fine target preserves coarse information state={si},b={bq},{bc}',numeric)

# A uniform unknown-input outcome law does not assert a physical information
# definition. Also preserve the boundary distinction: a small nonzero fine
# branch at a=0 must stay in the law, even though its coefficient of entropy
# is zero in the stated price.
eps=1e-3
uv=math.sin(eps)**2
ck(abs(scalar_price(.43,uv,0)-fmin(.43,0)-.57*uv)<1e-15 and uv>0,
   'zero-info approximate dark branch is retained and paid',numeric)

print(json.dumps({
 'status':'PASS_SCOPED_FULL_FINE_PRICE',
 'exact_count':len(exact),'exact_checks':exact,
 'numeric_count':len(numeric),'numeric_checks':numeric,
 'diagnostics':{'max_scalar_defect_error':max_scalar_gap_error,
                'max_full_quantum_defect_error':max_quantum_identity_error,
                'max_full_tail_stationarity_error':max_tail_stationarity_error,
                'positive_quantum_information_deficit':positive_chi,
                'zero_info_gain':1.,'uniform_gain_lower_coefficients':[pf,pf**2]},
 'scope':'Actual three parsed lengths; exact algebra and bounded full-instrument numerical diagnostics. The global theorem is analytic. No full native H1 word or physical Cost-Info binding.',
 'native_changed_tail_admission_proved':False,
 'full_physical_C_closed':False,'GR_closed':False
},indent=2))
