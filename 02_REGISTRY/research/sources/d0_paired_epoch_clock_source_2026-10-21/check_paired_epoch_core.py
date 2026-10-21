#!/usr/bin/env python3
"""Exact D0 paired-epoch clock/source transport. No physical cut selection.
Consumes the full H+J+R/complement definition; does not replay full128 Dirac.
"""
from pathlib import Path
import json
import sympy as s

checks=[]
def ok(name,condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)

for ell in (1,2,3):
    n=2*ell+1
    S=s.zeros(n)
    for j in range(n):
        S[(j+ell)%n,j]=1
    E=s.zeros(n,2);E[0,0]=1;E[ell,1]=1
    T=E.T*S*E
    ok(f'unitary_completion_{ell}',S.T*S==s.eye(n))
    ok(f'forward_no_wrap_on_active_inputs_{ell}',S[ell,0]==S[2*ell,ell]==1)
    ok(f'one_epoch_clock_blind_{ell}',S[0,0]==0)
    ok(f'paired_epoch_nilpotent_corner_{ell}',T==s.Matrix([[0,0],[1,0]]))
    ok(f'paired_epoch_return_rank_one_{ell}',T.T*T==s.diag(1,0))
    for a in range(n):
        for b in range(a+1,n):
            K=s.zeros(n);K[b,a]=1;K[a,b]=-1
            dT=E.T*(S*K-K*S)*E
            dR=dT.T*T+T.T*dT
            ok(f'clock_cut_first_source_zero_{ell}_{a}_{b}',dR[0,0]==dR[1,1]==0)
    psi=E*s.Matrix([1,1])/s.sqrt(2)
    ok(f'coherent_rank_one_not_excluded_{ell}',(psi.T*S*psi)[0]==s.Rational(1,2))

# Arbitrary DATA block; the original complement includes all orthogonal work.
a,b,c,d,z=s.symbols('a b c d z',real=True)
A=s.Matrix([[a,b],[c,d]])
zero=s.zeros(2)
Al=zero.row_join(zero).col_join(A.row_join(zero))
Fd=s.eye(2)-A.T*A
Fl=s.eye(4)-Al.T*Al
ok('full_operator_complement',Fl==s.diag(Fd,s.eye(2)))
ok('full_logdet_factor',s.factor((s.eye(4)-z*Fl).det()-(1-z)**2*(s.eye(2)-z*Fd).det())==0)
ok('normalized_trace_gain_is_halved',s.trace(Fl)/4==s.Rational(1,2)+s.trace(Fd)/4)

# Same conditional stack, spectator clock heat operator and original RIGHT.
beta,Z,C0,C1,R,J=s.symbols('beta Z C0 C1 R J',positive=True)
r,dim=s.symbols('r dim',positive=True,integer=True)
Sd=s.log(C0*Z)/beta+J+R
Sl=s.log(2*C1*Z)/beta+J-r*dim*s.log(1-z)+R
offset=s.log(2*C1/C0)/beta-r*dim*s.log(1-z)
ok('whole_HJR_exact_offset',s.simplify(s.expand_log(Sl-Sd-offset,force=True))==0)
for y in (Z,J,R):
    ok('data_source_equal_'+str(y),s.diff(Sl-Sd,y)==0)
ok('moving_beta_source_retained',s.diff(offset,beta)==-s.log(2*C1/C0)/beta**2)
ok('moving_z_source_retained',s.diff(offset,z)==r*dim/(1-z))
Delta=s.diag(2,5,7)
C=s.Matrix([[1,0],[0,1],[0,0]])/s.sqrt(2)
Cl=C.col_join(s.zeros(3,2))
Dl=s.diag(Delta,Delta)
ok('fixed_RIGHT_Gram',Cl.T*Cl==C.T*C)
ok('all_clock_preparation_equations_lift',Dl*Cl==Cl*s.diag(2,5))

# Nonuniform moving positive clock coordinates use the TRUE weighted adjoint.
x=s.symbols('x',positive=True)
S=s.zeros(5)
for j in range(5):S[(j+2)%5,j]=1
E=s.zeros(5,2);E[0,0]=1;E[2,1]=1
CW=s.diag(1,x,x*x,2*x,3*x*x);W=CW*CW
Sw=CW.inv()*S*CW;Ew=CW.inv()*E
Tw=s.simplify(Ew.T*W*Sw*Ew)
ok('moving_positive_clock_metric_exact',Tw==s.Matrix([[0,0],[1,0]]))
ok('moving_clock_weight_source_zero',Tw.diff(x)==s.zeros(2))

# Actual native CAR rotation rank and Golden recombination, not a 2-plane cut.
p=(s.sqrt(5)-1)/2
g=s.Matrix([[s.sqrt(p),-p],[p,s.sqrt(p)]])
X=s.Matrix([[0,1],[1,0]])
ok('native_forward_recombiner',s.simplify(X*g*X-g.T)==s.zeros(2))
K=s.zeros(16)
for j in (6,10,12,14):K[j+1,j]=1;K[j,j+1]=-1
Pi=-K*K
ok('native_CAR_rank_eight',Pi.rank()==8 and Pi*Pi==Pi and K.T==-K)
ok('native_k1_feedback_bound',s.simplify(128*s.Rational(1,2**20)*16*p**6*8*s.Rational(11,12)**4-s.Rational(14641,1327104)*p**6)==0)

result={'status':'AUTHOR_EXACT_CORE_PASS','checks':checks,'count':len(checks),
 'input_ref':'c49ebdb12244943d1ec45ef6d148a0432481141e',
 'native_complement_blob':'db279db445bcc013827773bdede3488a9461fcea',
 'scope':'conditional finite clock/cut and spectator-stack source transport',
 'complete_physical_price_selected':False,'actual_clock_gate_compilation_proved':False,
 'unrestricted_work_cut_stationarity_proved':False,'GR_closed':False}
Path(__file__).with_name('CORE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
