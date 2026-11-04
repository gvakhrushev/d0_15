#!/usr/bin/env python3
"""Exact EW3--6 source application; native readback/full heat are separate owners."""
import json
from itertools import product
from fractions import Fraction as Fraction
import sympy as s

checks = []

def need(condition, name):
    if not bool(condition):
        raise RuntimeError("FAILED: " + name)
    checks.append(name)

def zero(expression, name):
    need(s.expand(expression) == 0, name)

def simpzero(expression, name):
    need(s.simplify(expression) == 0, name)

# Three independent CALLS; all four outcomes INSIDE each call remain arbitrary.
def law(a, P, beta):
    return {(0,0): 1-a-beta+P, (0,1): beta-P, (1,0): a-P, (1,1): P}

a0, ap, am, P0, Pp, Pm, b0, bp, bm = s.symbols('a0 ap am P0 Pp Pm beta0 betap betam')
laws = (law(a0,P0,b0), law(ap,Pp,bp), law(am,Pm,bm))
for j,L in enumerate(laws):
    zero(sum(L.values())-1, 'four-outcome normalization '+str(j))
chi_sum = beta_sum = s.Integer(0)
count = 0
for outcome in product(tuple(laws[0]), repeat=3):
    mass = s.prod(L[v] for L,v in zip(laws,outcome))
    (A0,R0),(Ap,Rp),(Am,Rm) = outcome
    chi_sum += mass*A0*(Ap*Rp-Am*Rm)
    beta_sum += mass*R0
    count += 1
need(count == 64, 'all 64 fine outcomes of three joint calls retained')
zero(chi_sum-a0*(Pp-Pm), 'conditional calibration chi without within-call independence')
zero(beta_sum-b0, 'raw baseline REPORT remains its actual marginal')
alpha, r0, Delta, eta = s.symbols('alpha r0 Delta eta', positive=True)
zero((a0*(Pp-Pm)).subs({a0:alpha,Pp:alpha*(s.Symbol('rm')+Delta),Pm:alpha*s.Symbol('rm')})-alpha**2*Delta,
     'common READY law gives chi equals alpha squared Delta_r')

# Exact source factorization BEFORE imposing any guard.
c,beta,chi,lam,pg,ag,zeta,rank = s.symbols('c beta chi lambda p a_G zeta rank', positive=True)
K = 4*lam*r0*chi
d0 = c-K
k = ag-(ag-pg)*beta
cread = k*c-(ag-pg)*(1-beta)*K
for coordinate in (c,beta,chi,lam,r0):
    residual = s.diff(cread,coordinate)-k*s.diff(c,coordinate)
    expected = -(ag-pg)*(d0*s.diff(beta,coordinate)+(1-beta)*s.diff(K,coordinate))
    zero(residual-expected, 'exact full corner residual '+str(coordinate))
Dread = 1-zeta+zeta*cread**2
Dold = 1-zeta+zeta*c**2
GJ = k*(cread/c)*Dold/Dread
nb = 2*rank*zeta*cread*(ag-pg)*d0/Dread
nc = 2*rank*zeta*cread*(ag-pg)*4*lam*r0*(1-beta)/Dread
for coordinate in (c,beta,chi):
    Jread_source = -2*rank*zeta*cread*s.diff(cread,coordinate)/Dread
    Jold_source = -2*rank*zeta*c*s.diff(c,coordinate)/Dold
    expected = GJ*Jold_source+nb*s.diff(beta,coordinate)+nc*s.diff(chi,coordinate)
    simpzero(Jread_source-expected, 'exact feedback normal factorization '+str(coordinate))
    simpzero(Jread_source-nb*s.diff(beta,coordinate)-nc*s.diff(chi,coordinate)-GJ*Jold_source,
             'reactions cancel ONLY displayed feedback normals '+str(coordinate))
# Hostile control: equal global means do not preserve the local product term.
u,v,bstar,chistar = s.symbols('u v beta_star chi_star', positive=True)
cstar = 1-8*lam
def read_at(bb,cc):
    return pg*cstar+(ag-pg)*(1-bb)*(cstar-4*lam*r0*cc)
aligned = (read_at(bstar+u,chistar+v)+read_at(bstar-u,chistar-v))/2
opposed = (read_at(bstar+u,chistar-v)+read_at(bstar-u,chistar+v))/2
zero(((bstar+u)+(bstar-u))/2-bstar, 'two-site beta mean retained')
zero(((chistar+v)+(chistar-v))/2-chistar, 'two-site chi mean retained')
zero(aligned-opposed-8*(ag-pg)*lam*r0*u*v,
     'same global calibration means can change averaged read corner')

# Existing common-writer calculation, with all failure terms still present.
Kw = 4*lam*alpha**2*r0*Delta
dw = cstar-Kw
bw = alpha*r0+(1-alpha)*eta
Cw = pg*cstar+(ag-pg)*(1-bw)*dw
Ka = s.diff(Kw,alpha)
Na = dw*(r0-eta)+(1-bw)*Ka
zero(s.diff(Cw,alpha)+(ag-pg)*Na, 'actual common-READY row retains failure marginal')
eta_star = (dw*r0+(1-alpha*r0)*Ka)/(dw+(1-alpha)*Ka)
simpzero(Na-(dw+(1-alpha)*Ka)*(eta_star-eta), 'unique fixed-failure READY sign threshold')
simpzero(eta_star-r0-(1-r0)*Ka/(dw+(1-alpha)*Ka), 'threshold lies above independent flag value')
zero(s.diff(Cw,eta)+(ag-pg)*dw*(1-alpha), 'free failure row remains nonzero')
Cind = Cw.subs(eta,r0)
zero(s.diff(Cind,alpha)+8*(ag-pg)*lam*(1-r0)*alpha*r0*Delta,
     'pinned independent full flag common-READY sign')
zero(s.diff(Cind,Delta)+4*(ag-pg)*lam*(1-r0)*alpha**2*r0,
     'matched reference contrast contributes with the same sign')
z=Fraction(1,2**20); lu=Fraction(5,8)**7
c_lower=1-8*lu; K_upper=8*lu*z*z; Ka_upper=16*lu*z*z
need(c_lower>Fraction(7,10) and K_upper<Fraction(3,10)*z*z,
     'original rare-report rational bounds for cstar and K')
need(c_lower-K_upper>Fraction(2,3), 'positive d0 uniform rational collar')
need(c_lower>3*K_upper and Ka_upper/(c_lower-K_upper)<z*z,
     'feasible threshold and eta_star minus r0 less than z0 squared')
current=s.symbols('current_report_sum_minus_2r0')
old_common = cstar-2*lam*alpha**2*Delta*current
zero(s.diff(old_common,alpha)+s.diff(old_common,Delta)*(-2*Delta/alpha),
     'constant chi linked direction leaves old corner invariant off shell')
read_common = pg*old_common+(ag-pg)*(1-r0)*(old_common-Kw)
zero(s.diff(read_common,alpha)+s.diff(read_common,Delta)*(-2*Delta/alpha),
     'constant chi linked direction leaves read corner invariant off shell')
zero(s.diff(read_common,current) - (ag-(ag-pg)*r0)*s.diff(old_common,current),
     'linked calibration invariance does not erase the field gain')

# A small exact MATRIX proper-cut control: the future removes S from endpoint.
# It is not a native synthesis/cost receipt; the separate native owner supplies it.
rot=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
Z=s.diag(1,-1); S1=rot.T*Z*rot
need(S1*S1==s.eye(2), 'source-erasure control is an exact reflection')
need(S1[0,0]==-s.Rational(7,25), 'proper-cut baseline reflection amplitude')
zero((ag*S1[0,0])**2-s.Rational(49,625)*ag**2,
     'proper-cut feedback before readback differs between reflections')
need(s.Rational(49,625)!=1, 'proper-cut source-erasure control is nontrivial')
need(Z*Z==S1*S1, 'paid matched future cancels either comparator exactly')

print(json.dumps({
 'status':'PASS','input_commit':'89707e8ad4787ace2da9d70b723b799094cee4d9',
 'checks':len(checks),'check_labels':checks,'fine_flag_outcomes':count,
 'formulas':{'chi':'alpha^2 Delta_r','K':'4 lambda r0 chi',
 'feedback':'dJ_read=G_J dJ_old+n_beta d_beta+n_chi d_chi',
 'reactions':'(-n_beta,-n_chi) cancel displayed feedback normals only',
 'hostile_global_mean_gap':'8(a_G-p)lambda r0 u v'},
 'scope':['conditional on the SAME SAM/SITE; common-law averaging needs proof',
          'actual failure law retained; no within-call READY/REPORT independence',
          'fixed lambda,r0 for the two-coordinate reaction statement',
          'same positive scalar physical cut and rank for feedback factorization',
          'native readback and full changed clock are supplied by separate packages',
          'full heat covector, comparator/scene/input rows remain'],
 'not_claimed':['full_heat_factorization','new_physical_guard_selection','M1_forcing',
                'complete_Cost_Info_binding','independent_field_channel','GR_closure'],
 'GR_closed':False},indent=2,sort_keys=True))
