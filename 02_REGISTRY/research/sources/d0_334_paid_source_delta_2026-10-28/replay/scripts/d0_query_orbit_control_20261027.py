"""Exact scalar-corner QUERY orbit and a paid native reflection control.
This is an ambient comparison, not physical admission of a continuous gate.
"""
from pathlib import Path
from fractions import Fraction
import importlib.util,hashlib,sys,json
import sympy as S
from sympy.polys.matrices import DomainMatrix
owner=Path.cwd()/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
pin=hashlib.sha256(owner.read_bytes()).hexdigest()
assert pin=='222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c'
spec=importlib.util.spec_from_file_location('query_orbit_native',owner);n=importlib.util.module_from_spec(spec);sys.modules[spec.name]=n;spec.loader.exec_module(n)
Kfield=n.GOLDEN_FIELD
def eq(A,B): return DomainMatrix.from_Matrix(S.Matrix(A-B)).convert_to(Kfield).is_zero_matrix
c,u,t,z,R,a=S.symbols('c u t z R a',real=True,positive=True)
P=S.diag(1,0);Q=S.Matrix([[c,u],[u,-c]]);K=Q*P-P*Q;I=S.eye(2)
assert K.T==-K and K*K==-u**2*I
assert S.expand((K*Q-Q*K)[0,0]-(-2*u**2))==0
# The exponential has a real-plane rotation because K²=-u²I.
W=S.cos(u*t)*I+S.sin(u*t)/u*K
C=S.trigsimp((W*Q*W.T)[0,0])
assert S.trigsimp(C-(c*S.cos(2*u*t)-u*S.sin(2*u*t)))==0
assert S.simplify(S.diff(C,t).subs(t,0)+2*u**2)==0
# B=H+J, exact heat derivative vanishes on the declared reflection base.
DJ=S.diff(-R*S.log(a+z*C**2),t).subs(t,0)
assert S.simplify(DJ-4*R*z*c*u**2/(a+z*c**2))==0
assert S.simplify(DJ/u-4*R*z*c*u/(a+z*c**2))==0
# The native 7ch QUERY word, not a small-angle replacement.
port,q=0,1;spin=(2,3);old=(4,);SI=n.Gate('SourceI',(port,*spin))
sw=(n.Gate('CX',(port,q)),n.Gate('CX',(q,port)),n.Gate('CX',(port,q)))
def ex(word): return n.Execution(5,(port,q),old,tuple(word),n.G_CX_SOURCE_I,port,spin)
Vword=sw+(n.Gate('G',(port,)),)+sw
Vinv=n.inverse_word(ex(Vword),max_qubits=5,max_expanded_stages=1000)
Zword=sw+(SI,SI)+sw; word=Vinv+Zword+Vword
obj=ex(word);n.validate_execution(obj,max_qubits=5,max_expanded_stages=1000);inv=n.inventory(obj,max_qubits=5,max_expanded_stages=1000)
assert (inv.gate_count,inv.g_count,inv.cx_count,inv.source_i_count,inv.cut_rank)==(26,2,18,6,8)
Qn=S.Matrix(n.word_matrix(obj,max_qubits=5,max_expanded_stages=1000)); Ip=S.Matrix(n.input_isometry(obj,max_qubits=5,max_expanded_stages=1000)); Pn=Ip*Ip.T
Kn=Qn*Pn-Pn*Qn
cn=n.P**3;un=2*n.A*n.P
assert eq(Qn,Qn.T) and eq(Qn*Qn,S.eye(32))
assert eq(Ip.T*Qn*Ip,cn*S.eye(8))
assert eq(Ip.T*(Kn*Qn-Qn*Kn)*Ip,-2*un**2*S.eye(8))
assert Kfield.from_sympy(S.expand(cn**2+un**2-1))==Kfield.zero
# Rational finite-descent control, no floating evaluation of trigonometric signs.
f=Fraction;cr=f(3,5);ur=f(4,5);tr=f(1,100);theta=2*ur*tr
assert theta<=1 and theta<=ur/(2*cr)
# sin θ >= θ−θ³/6; 1−cos θ <= θ²/2.
delta_lower=ur*(theta-theta**3/6)-cr*theta**2/2
assert delta_lower>=f(7,6)*ur**2*tr>0
print(json.dumps({'status':'PASS','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'native_owner_sha256':pin,'native_query':'26 stages, all 32 columns, protected rank 8','scalar':'c=p^3, u=2 sqrt(p) p','full_orbit_corner_derivative':'-2(1-c^2) I','full_orbit_feedback_derivative':'4 R z c(1-c^2)/(a+z c^2)','unit_generator_feedback_derivative':'4 R z c sqrt(1-c^2)/(a+z c^2)','finite_descent_rational_lower':str(delta_lower),'scope':'ambient full-query comparator; finite abstract orbit sign; physical X_N, large 7cq and compiled tolerance task not checked'},indent=2))
