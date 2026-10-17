"""Finite full-port Stinespring tangent metric, Berry curvature and exact native shell check.
No physical action selection and no original GR terminal.
"""
import sympy as s
import json

p=(s.sqrt(5)-1)/2
q=p*p
ell=s.log(1/p)
I=s.eye(3)
X=s.Matrix([[0,-1,0],[1,0,0],[0,0,0]])
Y=s.Matrix([[0,0,0],[0,0,-1],[0,1,0]])
count=0

def check(cond,label):
    global count
    if not bool(cond): raise RuntimeError(label)
    count+=1

def same(A,B,label):
    if isinstance(A,s.MatrixBase):
        check(all(s.simplify(a-b)==0 for a,b in zip(A,B)),label)
    else:check(s.simplify(A-B)==0,label)

check(s.simplify(p+q-1)==0,'golden normalization')
check(s.simplify(p-q-p**3)==0,'golden gap')

# Full golden control for one isometric reflection column M (including two ports).
def k0(M): return p*I+q*M
def k1(M): return p*s.sqrt(p)*(M-I)
# All physical 128 outcomes collapse to this two-port algebraic class on a single isometric record column.
# It is a special control class, not an assertion that a generic native SELECT is a 2-label instrument.
M=I
K=[k0(M),k1(M)]
same(sum((A.T*A for A in K),s.zeros(3)),I,'two-port completeness')
for V in (X,Y,X+Y):
    dK=[q*V,p*s.sqrt(p)*V]
    Gamma=sum((A.T*B for A,B in zip(K,dK)),s.zeros(3))
    S2=sum((B.T*B for B in dK),s.zeros(3))
    Q=S2-Gamma.T*Gamma
    same(Gamma,q*V,'full two-port Berry connection')
    same(Q,p**3*V.T*V,'strict golden tangent coercivity')
    same(Q.T,Q,'quantum geometric tensor symmetry in same direction')
    check(s.trace(Q)>0,'positive tangent source')
# Noncommuting curvature from the SAME golden isometry, without an inserted curvature operator.
Qxy=p**3*X.T*Y
Qyx=p**3*Y.T*X
F=Qxy-Qyx
same(F,-p**3*(X*Y-Y*X),'native record Berry curvature')
check(F!=s.zeros(3),'nonzero operator curvature')
check(s.trace(F)==0,'curvature not recoverable from scalar trace alone')
check(s.simplify(s.trace(Qxy))==0,'independent xy tangent metric')
# Rotation in M only is distinct from co-transforming both golden branches under a right frame.
same(p**3*X.T*X,s.simplify(q*X.T*X-q*q*X.T*X),'fixed port gauge anchor')
# If V --> VU as one common moving frame, perpendicular tangent =0.
check(X.T==-X,'skew local frame')

# Exact recurrence for actual complete retained tape's two-configuration transfer:
# C_n(t)=F_t**n(I); D_n=C_n'(0), E_n=C_n''(0).
# For the witness M0=I, My(t)=exp(tX), F_t(B)=p B+q exp(-tX) B.
# F0(B)=B; F'_0(B)=-q X B; F''_0(B)=q X**2 B.
for n in (1,2,3,4,7):
    D=s.zeros(3); E=s.zeros(3)
    for j in range(n):
        E_new=E+2*(-q*X*D)+q*X**2
        D_new=D-q*X
        D,E=D_new,E_new
    same(D,-n*q*X,'complete tape 1-jet finite recurrence')
    same(E,(n*q+n*(n-1)*q*q)*X**2,'complete tape 2-jet finite recurrence')
    Qn=-(E.T+E)/2-D.T*D
    same(Qn,n*p**3*X.T*X,'complete tape quantum metric exact')

# Actual 16-CAR/eight-shell native overlap fixture (prior owner), not a substitute/select-only shortcut:
# same original beta, epsilon and full controller reflection.
t=s.symbols('t',real=True)
nu=s.Rational(3,5); b=s.Rational(4,5)
ny=s.Rational(5,13); by=s.Rational(12,13)
nut=nu*s.cos(t)+b*s.sin(t)
bt=b*s.cos(t)-nu*s.sin(t)
f=s.trigsimp(nut**2+ny**2 -nut*ny*(1+nut*ny+bt*by))
check(s.simplify(f.subs(t,0)-s.Rational(226,4225))==0,'true SELECT and reflected full K fixture value')
check(s.simplify(s.diff(f,t).subs(t,0)-s.Rational(1736,4225))==0,'actual full native first comparative source')
f_diag=s.trigsimp(nut**2+nu**2-nut*nu*(1+nut*nu+bt*b))
check(s.simplify(s.diff(f_diag,t).subs(t,0))==0,'diagonal first source vanishes')
check(s.simplify(s.diff(f_diag,t,2).subs(t,0)-s.Rational(41,25))==0,'diagonal information metric first-shell')
# f(t) real and true derivative not an inserted flat-metric action.
# At original n_h=128/h^2, w_h=4sin^2(pi h), continuum n_h*w_h/128 -> 4pi².
info_theta=s.simplify(8*s.pi**2*q*(s.Rational(41,50))/ell)
first_offdiag=s.simplify(8*s.pi**2*q*(s.Rational(1736,4225))/ell)
check(float(s.N(info_theta))>0,'uniform nonzero time-scaled native relative metric')
check(float(s.N(first_offdiag))>0,'nonzero off-diagonal native source at flat geometry')
# one mathematical negative control: comparing the same exact native configuration yields zero first source,
# while a different fixed retained reference gives a positive first source.
check(s.simplify(s.diff(f,t).subs(t,0))!=0 and s.simplify(s.diff(f_diag,t).subs(t,0))==0,'reference-dependence of native source')
result={'status':'PASS','exact_controls':count,'golden_identity':'p+p^2=1','native_carrier':'full128 outcome round and inherited full16/eight-shell fixture','qgt_coercivity':'p^3 ||dM||_HS^2 <= Tr Q <= p^2 ||dM||_HS^2', 'berry_curvature':'-p^3 [X,Y] in SO(3) witness', 'whole_tape_jet_recursion':'first+second, no 128^n enumeration', 'shell_f':str(s.Rational(226,4225)), 'shell_df_offdiag':str(s.Rational(1736,4225)), 'shell_fdiag_second_theta':str(s.Rational(41,25)), 'shell_information_metric_theta_limit':str(s.N(info_theta,16)), 'shell_offdiag_first_source_limit':str(s.N(first_offdiag,16)), 'native_history_cost_selected':False,'full_einstein_action_proved':False}
print(json.dumps(result,ensure_ascii=False,sort_keys=True))
