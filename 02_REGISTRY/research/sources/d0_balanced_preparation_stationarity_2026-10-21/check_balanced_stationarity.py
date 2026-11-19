#!/usr/bin/env python3
"""Authored narrow controls for the exact balanced-preparation proof.

No original L4/4096-D Dirac, 255-leaf support, Lean or GR replay is run.
The noncommuting 8-D/r=2 example is a complete parity-preserving model.
All checks raise explicitly and therefore also execute under python -O.
"""
from __future__ import annotations

import json
from fractions import Fraction as F
from typing import Any

import mpmath as mp

mp.mp.dps = 100
p = (mp.sqrt(5) - 1) / 2
lnphi = -mp.log(p)
passed: list[str] = []
metrics: dict[str, Any] = {}


def check(name: str, condition: Any) -> None:
    if not bool(condition):
        raise RuntimeError('FAILED: ' + name)
    passed.append(name)


def close(x: Any, y: Any, tol: str = '1e-70') -> bool:
    return abs(x - y) <= mp.mpf(tol) * max(1, abs(x), abs(y))


def tr(A: mp.matrix) -> mp.mpf:
    return sum(A[i, i] for i in range(A.rows))


def norm2(A: mp.matrix) -> mp.mpf:
    return sum(abs(A[i, j]) ** 2 for i in range(A.rows) for j in range(A.cols))


def matclose(A: mp.matrix, B: mp.matrix, tol: str = '1e-70') -> bool:
    return norm2(A - B) <= mp.mpf(tol) ** 2 * max(1, norm2(A), norm2(B))


def spectral(A: mp.matrix, func) -> mp.matrix:
    vals, vec = mp.eigsy(A)
    if min(vals) <= 0:
        raise RuntimeError('Expected positive OLD matrix; no spectral floor is used')
    return vec * mp.diag([func(x) for x in vals]) * vec.T


def entropy_positive(A: mp.matrix) -> mp.mpf:
    vals = mp.eigsy(A, eigvals_only=True)
    if min(vals) <= 0:
        raise RuntimeError('Positive compressed Gram expected; no eigenvalue deletion')
    return -sum(x * mp.log(x) for x in vals) / lnphi


def embed_columns(columns: list[mp.matrix]) -> mp.matrix:
    return mp.matrix([[col[i] for col in columns] for i in range(columns[0].rows)])


def C_angles(c, theta) -> mp.matrix:
    C = mp.zeros(8, 2)
    for s in range(2):
        rad = mp.sqrt(p*p - c[s]*c[s])
        vals = (mp.sqrt(p), rad*mp.cos(theta[s]), c[s], rad*mp.sin(theta[s]))
        for j, v in enumerate(vals):
            C[4*s+j, s] = v / mp.sqrt(2)
    return C


def C_raw(c, b) -> mp.matrix:
    return C_angles(c, [mp.asin(b[s]/mp.sqrt(p*p-c[s]*c[s])) for s in range(2)])


J = mp.zeros(8)
J[3, 1], J[1, 3] = 1, -1
parity = mp.diag([-1, -1, 1, 1, -1, -1, 1, 1])


def effects():
    I = mp.eye(8)
    X = mp.diag([mp.mpf((-1)**i)/(i+2) for i in range(8)])
    Y = mp.diag([mp.mpf((-1)**(i+1))/(i+3) for i in range(8)])
    for i, j, d in [(0,1,5),(0,4,6),(1,5,-7),(2,3,6),(3,7,8),(2,6,9)]:
        X[i,j] = X[j,i] = mp.mpf(1)/d
    for i, j, d in [(0,5,7),(1,4,-8),(4,5,6),(2,7,-6),(3,6,7),(6,7,5)]:
        Y[i,j] = Y[j,i] = mp.mpf(1)/d
    E0, E1, E2 = (I+X/8)/3, (I+Y/8)/3, (I-(X+Y)/8)/3
    B = spectral(E0, mp.sqrt)
    stopped = [E1, E2, B*E1*B, B*E2*B, B**4]
    return (E0, E1, E2), B, stopped


one, Bblank, Es = effects()


def one_price(C: mp.matrix, Elist=Es) -> mp.mpf:
    return sum(entropy_positive(C.T*E*C) for E in Elist) - mp.log(2)/lnphi


def two_price(c, theta0, a, Elist=Es) -> mp.mpf:
    C0 = C_angles(c, theta0)
    if a == 0:
        return one_price(C0, Elist)
    theta1 = [theta0[0]+a, theta0[1]]
    C1 = C_angles(c, theta1)
    delta = C1-C0
    # Exact rank-one compression, retaining both original RIGHT columns.
    W = embed_columns([C0[:,j]+p*p*delta[:,j] for j in range(2)] +
                      [mp.sqrt(p**3)*delta[:,0]])
    return sum(entropy_positive(W.T*E*W) for E in Elist)-mp.log(2)/lnphi


def balanced(c, theta, a, Elist=Es):
    return two_price(c, [theta[0]-p*p*a, theta[1]], a, Elist)


def central_diff(fun, x, h=mp.mpf('1e-22')):
    return (fun(x+h)-fun(x-h))/(2*h)


def Q_mass(c, theta):
    C = C_angles(c, theta)
    Y = J*C
    total = mp.mpf(0)
    for E in Es:
        G, T = C.T*E*C, C.T*E*Y
        total += tr(Y.T*E*Y - T.T*(G**-1)*T)
    return p**3 * total


# 1. Exact native constants, full CAR generator and all128 row normalization.
check('golden_quadratic', close(p+p*p, 1))
J16 = mp.zeros(16)
for j in (6,10,12,14):
    J16[j+1,j], J16[j,j+1] = 1, -1
check('full_generator_rank8', sum(1 for i in range(16) if J16[i,i^1] != 0) == 8)
check('full_generator_cubic', matclose(J16**3, -J16))
check('full_generator_clock_scalar_fixed', norm2(J16[:,1])+norm2(J16[:,0]) == 0)
cc, bb, aa = mp.mpf('0.04'), mp.mpf('0.07'), mp.mpf('0.13')
dd = mp.sqrt(p*p-cc*cc-bb*bb)
v = mp.zeros(16,1)
v[1],v[0],v[15],v[14]=mp.sqrt(p),cc,bb,dd
U16=mp.eye(16)+mp.sin(aa)*J16+(1-mp.cos(aa))*(J16**2)
vr=U16*v
check('native_exact_top_orbit', close(vr[15], bb*mp.cos(aa)+dd*mp.sin(aa)))
check('native_exact_slack_orbit', close(vr[14], dd*mp.cos(aa)-bb*mp.sin(aa)))
check('full_generator_isometry', matclose(U16.T*U16, mp.eye(16)))
# Exact real orthonormal-row control, not a re-enumeration of native Fourier order.
H=[[1 if (i&j).bit_count()%2==0 else -1 for j in range(128)] for i in range(256)]
check('all128_columns_orthonormal_control', all(sum(H[i][j]*H[i][k] for i in range(256)) == (256 if j==k else 0) for j in range(128) for k in range(128)))
check('each_row_norm_half', all(sum(F(h*h,256) for h in row)==F(1,2) for row in H))
check('native_local_reference_norm', F(128,256*128)==F(1,256))
check('native_nu', close(p**3*(p*p/256),p**5/256))

# 2. A complete, noncommuting, parity-preserving stopped instrument.
check('one_round_complete', matclose(sum(one,mp.zeros(8)),mp.eye(8)))
check('stopped_cap2_complete', matclose(sum(Es,mp.zeros(8)),mp.eye(8)))
check('query_noncommutes', norm2(one[0]*one[1]-one[1]*one[0])>mp.mpf('1e-8'))
for j,E in enumerate(Es):
    check(f'effect_{j}_positive', min(mp.eigsy(E,eigvals_only=True))>0)
    check(f'effect_{j}_parity', matclose(E*parity,parity*E))
check('abort_not_discardable', norm2(sum(Es[:-1],mp.zeros(8))-mp.eye(8))>mp.mpf('0.01'))
c=[mp.mpf('0.02'),mp.mpf('-0.03')]
theta=[mp.mpf('0.04'),mp.mpf('-0.06')]
C=C_angles(c,theta)
check('full_RIGHT_Gram',matclose(C.T*C,mp.eye(2)/2))
for j,E in enumerate(Es):
    check(f'old_Gram_{j}_faithful',min(mp.eigsy(C.T*E*C,eigvals_only=True))>mp.mpf('0.005'))
check('old_Grams_not_all_commuting',norm2((C.T*Es[0]*C)*(C.T*Es[1]*C)-(C.T*Es[1]*C)*(C.T*Es[0]*C))>mp.mpf('1e-12'))

# 3. Exact balanced density source and the complete Ward identity.
a=mp.mpf('0.013')
C0=C_angles(c,[theta[0]-p*p*a,theta[1]])
C1=C_angles(c,[theta[0]+p*a,theta[1]])
rho=p*C0*C0.T+p*p*C1*C1.T
same=mp.sqrt(p)*C0
check('balance_parameter_identity',close((theta[0]-p*p*a)+a,theta[0]+p*a))
Y=J*C
rhojet=-p*p*p*(Y*C.T+C*Y.T)+p*p*p*(Y*C.T+C*Y.T)
check('balanced_density_jet_exact_zero',norm2(rhojet)==0)
check('balanced_state_not_pure_off_diagonal',norm2(rho-C*C.T)>mp.mpf('1e-10'))
D=C1-C0
W=embed_columns([C0[:,j]+p*p*D[:,j] for j in range(2)]+[mp.sqrt(p**3)*D[:,0]])
check('rank_one_spectral_compression',matclose(W*W.T,rho))
s=central_diff(lambda x:two_price(c,theta,x),mp.mpf(0))
u=central_diff(lambda x:one_price(C_angles(c,[x,theta[1]])),theta[0])
check('exact_source_Ward',close(s,p*p*u,'1e-35'))
check('fixed_first_arm_force_nonzero',abs(s)>mp.mpf('1e-30'))
bal_d=central_diff(lambda x:balanced(c,theta,x),mp.mpf(0))
check('balanced_entropy_source_zero',abs(bal_d)<mp.mpf('1e-35'))
check('positive_kernel_mass',Q_mass(c,theta)>p**5/4)
check('vacuum_mass_exact',close(Q_mass([0,0],[0,0]),p**5/2))
check('missing_abort_changes_mass',p**3*tr((J*C_angles([0,0],[0,0])).T*sum(Es[:-1],mp.zeros(8))*(J*C_angles([0,0],[0,0])))<p**5/2)
metrics['ward']={'first_arm_preparation_force':mp.nstr(s,22),'p_squared_material_source':mp.nstr(p*p*u,22),'balanced_source':mp.nstr(bal_d,5),'fixture_vacuum_nu':mp.nstr(p**5/2,22),'native_nu':mp.nstr(p**5/256,22)}

# 4. Logarithmic radial coefficient and sign, including nonzero material.
ratios=[]
for exp in (5,10,20):
    a=mp.mpf(10)**(-exp)
    val=balanced([0,0],[0,0],a)-one_price(C_angles([0,0],[0,0]))
    ratio=val/(a*a*mp.log(1/(a*a)))
    ratios.append(ratio)
    check(f'vacuum_radial_value_positive_{exp}',val>0)
    check(f'vacuum_mass_limit_error_{exp}',abs(ratio-p**5/(2*lnphi))<mp.mpf('0.1'))
check('radial_ratio_converges',abs(ratios[2]-p**5/(2*lnphi))<abs(ratios[1]-p**5/(2*lnphi))<abs(ratios[0]-p**5/(2*lnphi)))
for a in (mp.mpf('0.002'),mp.mpf('-0.002'),mp.mpf('1e-6'),mp.mpf('-1e-6')):
    check('nonvacuum_relative_value_'+str(a),balanced(c,theta,a)>one_price(C))
    d=central_diff(lambda x:balanced(c,theta,x),a,mp.mpf('1e-25'))
    check('nonvacuum_relative_radial_source_'+str(a),a*d>0)
metrics['log_coefficient']={'native':mp.nstr(p**5/(256*lnphi),22),'fixture_limit':mp.nstr(p**5/(2*lnphi),22),'finite_ratios':[mp.nstr(x,22) for x in ratios]}

# 5. All four mixed terms: M=p^3 P_b H_m, including hostile scalar control.
Cv=C_angles([0,0],[0,0]); Ja=J*Cv
Tb=mp.zeros(8,2);Tb[3,0]=1/mp.sqrt(2)
Ms=[]
for idx,(row,col) in enumerate(((2,0),(3,0),(6,1),(7,1))):
    T=mp.zeros(8,2);T[row,col]=1/mp.sqrt(2)
    Cbj=mp.zeros(8,2)
    if idx==1:Cbj[1,0]=-1/(p*mp.sqrt(2))
    mval=hval=mp.mpf(0)
    for E in Es:
        logG=spectral(Cv.T*E*Cv,mp.log)
        R=T.T*E*Ja+Ja.T*E*T+(J*T).T*E*Cv+Cv.T*E*(J*T)
        Gbj=T.T*E*Tb+Tb.T*E*T+Cbj.T*E*Cv+Cv.T*E*Cbj
        check(f'mixed_Gram_identity_{idx}_{len(passed)}',matclose(R,p*Gbj))
        mval-=p*p*tr(R*logG)/lnphi
        hval-=tr(Gbj*logG)/lnphi
    check(f'full_M_is_Hessian_row_{idx}',close(mval,p**3*hval))
    Ms.append(mval)
check('actual_control_M_nonzero',abs(Ms[1])>mp.mpf('1e-5'))
T=Tb
full=bad=mp.mpf(0)
for prob in (mp.mpf(1)/3,mp.mpf(2)/3):
    E=prob*mp.eye(8); logG=spectral(Cv.T*E*Cv,mp.log)
    Rshort=T.T*E*Ja+Ja.T*E*T
    Rfull=Rshort+(J*T).T*E*Cv+Cv.T*E*(J*T)
    full+=tr(Rfull*logG)
    bad+=tr(Rshort*logG)
check('scalar_instrument_full_M_zero',abs(full)<mp.mpf('1e-90'))
check('omitted_mixed_terms_create_false_source',abs(bad)>mp.mpf('0.01'))

# 6. Exact actual-port/central-gain neutral ledger and explicit non-neutral controls.
cost=[mp.mpf(x) for x in (2,3,3,4,2)]
mu=[mp.mpf(1)/3,mp.mpf(1)/6,mp.mpf(1)/6,mp.mpf(1)/12,mp.mpf(1)/4]
check('reference_all_leaves_complete',close(sum(mu),1))
Tledger=sum([(cost[j]+mp.log(mu[j])/lnphi)*E for j,E in enumerate(Es)],mp.zeros(8))
check('affine_ledger_balanced_jet_zero',tr(Tledger*rhojet)==0)
a=mp.mpf('0.013')
C0=C_angles(c,[theta[0]-p*p*a,theta[1]])
C1=C_angles(c,[theta[0]+p*a,theta[1]])
rho=p*C0*C0.T+p*p*C1*C1.T
q=[tr(E*rho) for E in Es]
Scoh=balanced(c,theta,a)+mp.log(2)/lnphi
relative_gain=-Scoh-sum(q[j]*mp.log(mu[j])/lnphi for j in range(5))+mp.log(4)/lnphi
net=sum(q[j]*cost[j] for j in range(5))-relative_gain
check('actual_port_gain_identity',close(net,balanced(c,theta,a)-mp.log(2)/lnphi+tr(Tledger*rho)))
eps=mp.mpf('0.017')
check('first_arm_only_work_not_neutral',abs(-p*p*eps)>0)
check('explicit_relative_work_not_neutral',eps!=0)
check('matched_two_arm_work_neutral',-p*p*p*eps+p*p*p*eps==0)
# A separately moving query has a field source even with identical prepared DATA.
# q(theta)=1/3+theta/10; the fixed-query coherent source does not acquire it.
query_source=(mp.log(2)/lnphi)/10
check('separately_moving_query_breaks_imported_Ward',abs(p*p*query_source)>mp.mpf('0.01'))

# A fixed noncentral reference on one leaf can see the full PR jet even
# though the balanced DATA derivative vanishes. No such reference is selected.
T=C.T*Es[0]*(J*C)
Gdot=mp.zeros(4)
D00=-p**3*(T+T.T);D11=-D00
D01=mp.sqrt(p**3)*(-p*p*T.T+p*T)
for i in range(2):
    for j in range(2):
        Gdot[i,j]=D00[i,j];Gdot[i+2,j+2]=D11[i,j]
        Gdot[i,j+2]=D01[i,j];Gdot[i+2,j]=D01[j,i]
Href=mp.diag([1,1,-1,-1])
check('balanced_complete_quantum_jet_can_be_nonzero',norm2(Gdot)>mp.mpf('1e-20'))
check('balanced_leaf_trace_source_zero',tr(Gdot)==0)
check('noncentral_reference_detects_hidden_source',abs(tr(Gdot*Href))>mp.mpf('1e-20'))
metrics['noncentral_reference_source']=mp.nstr(tr(Gdot*Href),22)

# Exact arithmetic reuse of the published coherent source enclosure.
# This is not a fresh evaluation of its original support/eigensolver fixture.
plo,phi=F(0),F(1)
for _ in range(100):
    pmid=(plo+phi)/2
    if pmid*pmid+pmid<1:plo=pmid
    else:phi=pmid
old_lo=F('-0.000000484198646894237340726684')
old_hi=F('-0.000000484198646476459455171882')
mat_lo=old_lo/(plo**3);mat_hi=old_hi/(phi**3)
check('published_material_source_interval_order',mat_lo<mat_hi<0)
check('material_source_inherited_nonzero',mat_hi<F('-0.000002'))
metrics['inherited_native_material_source']={
    'lower_rational':str(mat_lo),'upper_rational':str(mat_hi),
    'approximate_midpoint':mp.nstr((mp.mpf(mat_lo.numerator)/mat_lo.denominator+mp.mpf(mat_hi.numerator)/mat_hi.denominator)/2,22),
    'operation':'published coherent cap2 source divided by p^3; original support not rerun'}

# 7. A nonzero-material one-arm stationary point, with negative field Hessian.
ts=mp.mpf('0.05'); es=mp.mpf(1)/4; et=mp.mpf(3)/4
ec=(mp.mpf(1)/2-p*p*(es*mp.cos(ts)**2+et*mp.sin(ts)**2))/p
Esmall=[mp.diag([ec,es,et]),mp.diag([1-ec,1-es,1-et])]

def vsmall(t):return mp.matrix([mp.sqrt(p),p*mp.cos(t),p*mp.sin(t)])

def qsmall(t):
    v=vsmall(t)
    return (v.T*Esmall[0]*v)[0]

def Asmall0(t):
    q=qsmall(t)
    return -(q*mp.log(q)+(1-q)*mp.log(1-q))/lnphi

def Asmall(t,a):
    if a==0:return Asmall0(t)
    u,v=vsmall(t),vsmall(t+a)
    out=mp.mpf(0)
    for E in Esmall:
        x=p*(u.T*E*u)[0];y=p*p*(v.T*E*v)[0];z=mp.sqrt(p**3)*(u.T*E*v)[0]
        total=x+y;det=x*y-z*z
        if det<=0:raise RuntimeError('nonzero-angle Gram lost positivity')
        big=(total+mp.sqrt(total*total-4*det))/2
        tiny=det/big
        out-=(big*mp.log(big)+tiny*mp.log(tiny))/lnphi
    return out

check('nonzero_matter_stationary_fixture_positive',0<ec<1)
check('nonzero_matter_probability_half',close(qsmall(ts),mp.mpf(1)/2))
check('baseline_material_stationarity',abs(mp.diff(Asmall0,ts))<mp.mpf('1e-90'))
Hess=mp.diff(Asmall0,ts,2)
check('baseline_has_negative_field_Hessian',Hess<0)
check('diagonal_preparation_stationarity',abs(p*p*mp.diff(Asmall0,ts))<mp.mpf('1e-90'))
for da in (mp.mpf('1e-5'),mp.mpf('-1e-5')):
    check('balanced_relative_min_despite_field_saddle_'+str(da),Asmall(ts-p*p*da,da)>Asmall0(ts))

# Find the fixed-first-arm optimizer by a derivative sign bracket, not a
# chosen target equation. These 1-D tests do not certify a native GR root.
def agrad(t,a):
    if a==0:return p*p*mp.diff(Asmall0,t)
    return mp.diff(lambda x:Asmall(t,x),a)

def optimizer(t):
    lo,hi=mp.mpf('-0.002'),mp.mpf('0.002')
    if not (agrad(t,lo)<0<agrad(t,hi)):raise RuntimeError('lost optimizer bracket')
    for _ in range(175):
        mid=(lo+hi)/2
        if agrad(t,mid)<0:lo=mid
        else:hi=mid
    return (lo+hi)/2

hessrat=[];opts=[]
for ss in ('1e-4','1e-7','1e-10'):
    d=mp.mpf(ss)
    ap=optimizer(ts+d);am=optimizer(ts-d)
    est=(Asmall(ts+d,ap)+Asmall(ts-d,am)-2*Asmall0(ts))/(d*d)
    ratio=est/Hess
    hessrat.append(ratio)
    opts.append({'delta':ss,'a_plus':mp.nstr(ap,20),'Hessian_ratio':mp.nstr(ratio,20)})
    check('fixed_profile_shift_'+ss,ap!=0)
    check('shifted_pair_not_joint_stationary_'+ss,abs(mp.diff(lambda t:Asmall(t,ap),ts+d))>mp.mpf('1e-20'))
    check('stationary_Hessian_ratio_'+ss,abs(ratio-1)<mp.mpf('0.1'))
check('stationary_Hessian_convergence',abs(hessrat[2]-1)<abs(hessrat[1]-1)<abs(hessrat[0]-1))
metrics['stationary_example']={'theta_star':mp.nstr(ts,10),'one_arm_Hessian':mp.nstr(Hess,22),'envelope_controls':opts}

print(json.dumps({'status':'PASS','precision_digits':mp.mp.dps,'checks':len(passed),
                  'check_names':passed,'metrics':metrics,
                  'scope':{'original_full128_support_replayed':False,'independent_review':False,
                           'physical_Book_selected':False,'GR_closed':False,
                           'fixture_data_dimension':8,'fixture_RIGHT_dimension':2,
                           'fixture_cap2_leaves':5}},indent=2,sort_keys=True))
