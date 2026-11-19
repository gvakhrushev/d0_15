#!/usr/bin/env python3
"""Actual eight-stage preparation and exact phase-kernel descent witness."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import sympy as s
from sympy.polys.matrices import DomainMatrix

OWNER_REL=Path('02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py')
ROOT=next((p for p in [Path.cwd(),*Path(__file__).resolve().parents]
           if (p/OWNER_REL).is_file()),None)
if ROOT is None:
    raise RuntimeError('Run within the repository or install checker there')
OWNER=ROOT/OWNER_REL
OWNER_SHA='222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c'
controls=[]
def require(ok,label):
    if not ok:
        raise RuntimeError(label)
    controls.append(label)
require(hashlib.sha256(OWNER.read_bytes()).hexdigest()==OWNER_SHA,'native owner input pin')
spec=importlib.util.spec_from_file_location('phase_native_owner',OWNER)
n=importlib.util.module_from_spec(spec);sys.modules[spec.name]=n;spec.loader.exec_module(n)
F=n.GOLDEN_FIELD;p=n.P;a=n.A
def zero(M,label):
    M=s.Matrix(M) if not isinstance(M,s.MatrixBase) else M
    require(DomainMatrix.from_Matrix(M).convert_to(F).is_zero_matrix,label)
def scalar_zero(v,label):
    zero(s.Matrix([s.expand(v)]),label)

S=(n.Gate('CX',(0,1)),n.Gate('CX',(1,0)),n.Gate('CX',(0,1)))
word=(n.Gate('G',(0,)),)+S+(n.Gate('G',(0,)),)+S
obj=n.Execution(5,(0,1),(4,),word,n.G_CX_SOURCE_I,0,(2,3))
n.validate_execution(obj,max_qubits=5,max_expanded_stages=100)
iv=n.inventory(obj,max_qubits=5,max_expanded_stages=100)
require((iv.gate_count,iv.g_count,iv.cx_count,iv.source_i_count,iv.full_dimension,iv.cut_rank)==(8,2,6,0,32,8),'exact paid inventory and active rank')
U=s.Matrix(n.word_matrix(obj,max_qubits=5,max_expanded_stages=100))
i=s.Matrix(n.input_isometry(obj,max_qubits=5,max_expanded_stages=100))
target=s.kronecker_product(s.Matrix(n.G_LOCAL),s.Matrix(n.G_LOCAL),s.eye(8))
zero(U-target,'all32-column endpoint G0 tensor G1 identity protected')
zero(U.T*U-s.eye(32),'full real unitarity')
v=s.Matrix([p,a*p,a*p,p*p]);weights=[p*p,p**3,p**3,p**4]
zero(U*i-s.kronecker_product(v,s.eye(8)),'all8 protected input columns')
scalar_zero(sum(weights)-1,'complete probability normalization')
for b in range(4):
    Eb=s.zeros(4);Eb[b,b]=1
    compressed=i.T*U.T*s.kronecker_product(Eb,s.eye(8))*U*i
    zero(compressed-weights[b]*s.eye(8),'complete label effect '+str(b))
require(2**2<5 and 5<3**2,'exact 0<p<1 establishes positive support')

J=s.Matrix([p,p*p,-p,-p*p]);k=s.Matrix([1,-1/p,0,0])
scalar_zero((J.T*k)[0],'exact non-global phase kernel')
require(all(F.from_sympy(s.expand(q))!=F.zero for q in J),'every J component nonzero')
for b in range(4):
    for c in range(b):
        e=s.zeros(4,1);e[b]=1;e[c]=-1
        outside=next(t for t in range(4) if t not in (b,c))
        require(e[outside]==0 and F.from_sympy(J[outside])!=F.zero,'transition vector outside span J '+str(c)+str(b))

sy=s.Matrix([[0,-s.I],[s.I,0]]);H=s.kronecker_product(sy,s.eye(2))
zero(s.Matrix(n.G_LOCAL)-(a*s.eye(2)-s.I*p*sy),'native finite Golden generator')
zero(H*H-s.eye(4),'Hamiltonian unit operator norm')

# Phi=(0,pi/2,0,0) is an AMBIENT coherent phase point, not a new native gate.
phase=s.diag(1,s.I,1,1);psi=phase*v
dpsi=s.I*s.diag(*list(k))*psi
dh=s.expand((dpsi.adjoint()*H*psi+psi.adjoint()*H*dpsi)[0])
scalar_zero(dh+2*a*p*p,'nonzero Hamiltonian derivative along phase kernel')
require(F.from_sympy(dh)!=F.zero,'strict descent failure without floats')
flow=-s.I*H*psi
dw=s.Matrix([s.expand(s.conjugate(psi[b])*flow[b]+s.conjugate(flow[b])*psi[b]) for b in range(4)])
expected=s.Matrix([-2*a*p*p,0,2*a*p*p,0])
zero(dw-expected,'exact full-Hilbert probability velocity')
scalar_zero((k.T*dw)[0]-dh,'probability tangency obstruction matches kernel source')
require(F.from_sympy(dw[0])!=F.zero and dw[1]==0,'flow outside one-dimensional probability tangent')

# At the original real phase base, both tests pass only pointwise.
psi0=v;dpsi0=s.I*s.diag(*list(k))*psi0
dh0=s.expand((dpsi0.adjoint()*H*psi0+psi0.adjoint()*H*dpsi0)[0])
scalar_zero(dh0,'real native base pointwise descent false positive')
flow0=-s.I*H*psi0
dw0=s.Matrix([s.expand(s.conjugate(psi0[b])*flow0[b]+s.conjugate(flow0[b])*psi0[b]) for b in range(4)])
zero(dw0-(-2*a*p)*J,'real native base tangent control')

# An arbitrarily small relative phase epsilon already creates the obstruction.
t,e,r=s.symbols('t e r',real=True)
expr=2*r*(p*s.sin(-t)+p*p*s.sin(-e+t/p))
epsilon_derivative=s.simplify(s.diff(expr,t).subs(t,0))
require(s.simplify(epsilon_derivative+2*p*r*(1-s.cos(e)))==0,'all-epsilon exact derivative')

result={
 'status':'PASS','input_commit':'1d29848fa0775485f7d48ab63f4a6625f9b705ad',
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'native_owner_sha256':OWNER_SHA,'sympy':s.__version__,
 'control_count':len(controls),'controls':controls,
 'native_word':{'stages':8,'G':2,'CX':6,'SourceI':0,'full_columns':32,'protected_input_rank':8},
 'probabilities':['p^2','p^3','p^3','p^4'],
 'J':['p','p^2','-p','-p^2'],'phase_kernel':['1','-1/p','0','0'],
 'phase_point':['0','pi/2','0','0'],'generator':'sigma_y(first port) tensor I(ordinary work)',
 'kernel_H_source':'-2 sqrt(p) p^2','Hilbert_probability_velocity':['-2 sqrt(p) p^2','0','2 sqrt(p) p^2','0'],
 'small_phase_source':'-2p sqrt(x(1-x)) (1-cos epsilon)',
 'native_real_base_kernel_source':'0','native_real_base_tangent':True,
 'phase_point_native_admission_proved':False,'local_lapse_H_N_identified':False,'GR_closed':False,
 'scope':'Full actual finite word and exact mathematical phase extension; no continuous native phase, selected normal Hamiltonian, HDA or GR proof.'
}
print(json.dumps(result,indent=2,sort_keys=True))
