#!/usr/bin/env python3
"""New full-archive feedback optimum and source; conditional physical recovery.

Exact algebra, operator inequality diagnostics with complex isometries, and
high-precision source/old-row identities. No fitted physical action.
"""
import json
import math
import mpmath as mp
import numpy as np
import sympy as s

checks = []


def ck(ok, name):
    if not bool(ok):
        raise ArithmeticError(name)
    checks.append(name)


def mm(a, b):
    return np.einsum("ij,jk->ik", a, b, optimize=False)


p = (s.sqrt(5)-1)/2
field = s.QQ.algebraic_field(s.sqrt(p))
eq = lambda x: field.from_sympy(s.expand(x)) == field.zero
uj = s.simplify(p**4/(1+p**4))
qstar = s.simplify(p**4/(1+2*p**4))
ck(eq((1-uj)/uj-p**(-4)), "actual fine born odds have exponent4")
ck(bool(qstar < p**2), "new full-archive coarse optimum lies below the entire old collar")
ck(eq((p**8+p**12)+p**12-p**8*(1+2*p**4)), "complete actual support born mass")
ck(bool(uj != p**2), "J optimum differs from old Golden fine/CQ optimum")
ck(eq(uj-(1/(1+p**(-4)))), "A8 tail minimum coincides only for a=1/4")

mp.mp.dps = 100
pf = (mp.sqrt(5)-1)/2
aa = mp.sqrt(pf**8+pf**12)
bb = pf**6
f = lambda q: aa*mp.sqrt(1-q)+bb*mp.sqrt(q)
df = lambda q: -aa/(2*mp.sqrt(1-q))+bb/(2*mp.sqrt(q))
ell = lambda q: -df(q)/f(q)
ellmin = ell(pf**2)
ellmax = ell(mp.mpf('.5'))
for i in range(101):
    q = pf**2 + (mp.mpf('.5')-pf**2)*i/100
    ck(f(q)>0 and df(q)<0 and ellmin<=ell(q)<=ellmax, "full archived source orientation and positive collar")
    ck(mp.diff(ell,q)>0, "logarithmic susceptibility strictly increases")
    theta = mp.atan(pf**2)
    c = lambda th: (pf**4*mp.cos(th)+pf**6*mp.sin(th))*mp.sqrt(1-q)+pf**6*mp.sqrt(q)
    ck(abs(mp.diff(c,theta))<mp.mpf('1e-98') and mp.diff(c,theta,2)<0, "true coherent tail maximum, amplitude coordinate")
    for coeff in (mp.mpf(0),mp.mpf('.25'),mp.mpf(1)):
        u = pf**4/(1+pf**4)
        parsed_row = (1-q)*(1-coeff*mp.log((1-u)/u)/mp.log(1/pf))
        ck(abs(parsed_row-(1-q)*(1-4*coeff))<mp.mpf('1e-98'), "additional parsed/CQ row retained")

# All three archive outcomes, not square roots of their probabilities only.
# bank dimension4, retained input rank2, j is the true bank embedding.
rng = np.random.default_rng(131809)
j = np.eye(4,dtype=complex)[:,:2]
max_eigen_defect = -math.inf
min_return = math.inf
for i in range(120):
    q = float(pf**2+(mp.mpf('.5')-pf**2)*(i%11)/10)
    raw = rng.normal(size=(8,2))+1j*rng.normal(size=(8,2))
    Q0,_ = np.linalg.qr(raw)
    raw = rng.normal(size=(4,2))+1j*rng.normal(size=(4,2))
    Q1,_ = np.linalg.qr(raw)
    # Q0 has the two fine tail rows as separate four-dimensional bank blocks.
    K00,K01 = math.sqrt(1-q)*Q0[:4], math.sqrt(1-q)*Q0[4:]
    K1 = math.sqrt(q)*Q1
    C = float(pf**4)*mm(j.conj().T,K00)+float(pf**6)*mm(j.conj().T,K01+K1)
    gram = mm(C.conj().T,C)
    defect = np.linalg.eigvalsh(gram-float(f(q)**2)*np.eye(2)).max()
    max_eigen_defect=max(max_eigen_defect,float(defect))
    ck(defect<3e-14, "global C*C <= f_arch squared I for complex branch isometries")
    theta = float(mp.atan(pf**2))
    opt = float(pf**4)*math.sqrt(1-q)*math.cos(theta)+float(pf**6)*(math.sqrt(1-q)*math.sin(theta)+math.sqrt(q))
    ck(abs(opt-float(f(q)))<1e-15, "all-input canonical target attains operator upper bound")
    z=.21
    eig = np.linalg.eigvalsh(gram)
    actual=-sum(math.log(1-z+z*float(e)) for e in eig)
    optimal=-2*math.log(1-z+z*float(f(q)**2))
    min_return=min(min_return,actual-optimal)
    ck(actual>=optimal-2e-14, "same original feedback J is globally minimized at full polar target")

# The exponentially small return stays inside the original gain; no rescaling.
records=[]
for M in (1,2,5,20):
    q=mp.mpf('.44'); z=mp.mpf(2)**(-20); rank=4
    old=mp.mpf('.37'); g=mp.mpf('.23')
    def J(qq,kk):
        return -rank*mp.log(1-z+z*kk*f(qq)**(2*M))
    ss=f(q)**(2*M);den=1-z+z*old*ss
    w=rank*z*old*ss/den
    Lambda=M*ell(q)*g
    Gamma=2*w*Lambda
    ck(Gamma>0, "actual full archive gain positive even when very small")
    ck(abs(mp.diff(lambda qq:J(qq,old),q)*g/Gamma-1)<mp.mpf('1e-55'), "actual common field gain includes all archive attenuation")
    ratio=abs(mp.diff(lambda kk:J(q,kk),old))/Gamma
    ck(abs(ratio-1/(2*old*Lambda))<mp.mpf('1e-55'), "old scalar source normalized by genuine gain decays as1/M")
    records.append({"M":M,"Gamma":mp.nstr(Gamma,30),"old_scalar_row_over_gain":mp.nstr(ratio,30)})

print(json.dumps({
    "status":"PASS_CONDITIONAL_FULL_ARCHIVE_RECOVERY_SOURCE",
    "checks":len(checks),
    "effective_born_masses":["p^8+p^12","p^12"],
    "fine_tail_optimum":mp.nstr(pf**4/(1+pf**4),35),
    "coarse_polar_threshold":mp.nstr(pf**4/(1+2*pf**4),35),
    "ell_min":mp.nstr(ellmin,35),"ell_max":mp.nstr(ellmax,35),
    "f_at_lower":mp.nstr(f(pf**2),35),"f_at_half":mp.nstr(f(mp.mpf('.5')),35),
    "max_complex_operator_defect":max_eigen_defect,
    "smallest_random_J_gap":min_return,
    "actual_gain_diagnostics":records,
    "extra_parsed_CQ_tail_row":"(1-q)*(1-4*a); it vanishes only at a=1/4",
    "native_full_recovery_word_constructed":False,
    "all_required_reader_transports_proved":False,
    "physical_Cost_Info_binding":False,
    "GR_closed":False,
},indent=2))
