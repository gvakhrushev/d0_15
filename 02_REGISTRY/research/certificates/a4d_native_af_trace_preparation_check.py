#!/usr/bin/env python3
"""Exact full-carrier controls of the compatible AF trace/preparation boundary."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

STEM='02_REGISTRY/research/certificates/a4d_native_af_trace_preparation'
PROOF='02_REGISTRY/research/A4D_NATIVE_AF_TRACE_PREPARATION.md'
INPUT='abe5d0677fb68396e824c4894fce7d1254b979b2'
SCOPE={
    'all_nonnegative_compatible_normalized_traces_classified':True,
    'Perron_eigenprofile_assumed_in_new_completeness_theorem':False,
    'finite_horizon_interval_is_entire_positive_trace_range':True,
    'finite_trace_distance_bound_is_physical_action_error':False,
    'full_GNS_density_fiber_analytic_dimension_d_squared_minus_d':True,
    'full_GNS_density_equal_to_defining_representation_density':False,
    'faithfulness_on_represented_algebra_implies_full_density_faithful':False,
    'all_traceless_and_cross_block_directions_retained':True,
    'varying_prices_retain_same_protected_zero_vector':True,
    'varying_prices_are_unfixed_scalar_heat_shifts':False,
    'internal_coordinate_conjugation_selects_full_density':False,
    'visible_trace_compatibility_proves_full_density_refinement':False,
    'normalized_isometric_compression_allows_faithful_new_modes':False,
    'constructed_density_family_declared_native_preparation':False,
    'matrix_fiber_covariance_and_Gibbs_arguments_new_Lean_theorems':False,
    'native_F_or_source_or_Ward_or_GR_closed':False,
    'Gibbs_identification_required_of_every_native_route':False,
    'T0_T3_or_original_parent_terminals_closed':False,
    'every_state_in_fixed_trace_simple_cyclic_ground_class_has_descent':True,
    'finite_thermal_minimum_exists_on_that_full_faithful_fiber':False,
    'descent_with_feedback_and_matter_fixed_asserted_native':False,
}
ROOT=None
Q=None

def load_field(root):
    global Q
    path=root/'02_REGISTRY/research/certificates/a4d_native_golden_cost_refinement_check.py'
    spec=importlib.util.spec_from_file_location('golden_cost_exact_field',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    Q=module.Q

def sign(x):
    x=Q.co(x);a,b=2*x.a-x.b,x.b
    if b==0:return (a>0)-(a<0)
    if a==0:return (b>0)-(b<0)
    if a>0 and b>0:return 1
    if a<0 and b<0:return -1
    gap=a*a-5*b*b
    return ((gap>0)-(gap<0))*(1 if a>0 else -1)

def qabs(x):return x if sign(x)>=0 else -x

class K:
    """Q(p)[sqrt(p)] with exact coefficients, p^2+p=1."""
    def __init__(self,x=0,y=0):self.x,self.y=Q.co(x),Q.co(y)
    @staticmethod
    def co(x):return x if isinstance(x,K) else K(x)
    def __add__(self,o):
        o=self.co(o);return K(self.x+o.x,self.y+o.y)
    __radd__=__add__
    def __neg__(self):return K(-self.x,-self.y)
    def __sub__(self,o):return self+-self.co(o)
    def __rsub__(self,o):return self.co(o)+-self
    def __mul__(self,o):
        o=self.co(o);return K(self.x*o.x+Q(0,1)*self.y*o.y,self.x*o.y+self.y*o.x)
    __rmul__=__mul__
    def __eq__(self,o):
        o=self.co(o);return self.x==o.x and self.y==o.y
    def __repr__(self):return f'K({self.x},{self.y})'

def clean(a):return {ij:K.co(v) for ij,v in a.items() if v!=0}
def add(*matrices):
    z={}
    for mat in matrices:
        for ij,v in mat.items():z[ij]=z.get(ij,K())+v
    return clean(z)
def scale(c,a):return clean({ij:K.co(c)*v for ij,v in a.items()})
def eye(n):return {(i,i):K(1) for i in range(n)}
def transpose(a):return {(j,i):v for (i,j),v in a.items()}
def mul(a,b):
    rows=defaultdict(list)
    for (k,j),v in b.items():rows[k].append((j,v))
    z={}
    for (i,k),v in a.items():
        for j,w in rows[k]:z[i,j]=z.get((i,j),K())+v*w
    return clean(z)
def trace(a):return sum((v for (i,j),v in a.items() if i==j),K())
def partial(a,size,offset=0):
    return clean({(i,j):sum((a.get((offset+i*size+k,offset+j*size+k),K()) for k in range(size)),K())
                  for i in range(size) for j in range(size)})

def mathematics():
    checks=Counter()
    def ck(n,predicate):
        assert bool(predicate),n
        checks[n]+=1
    p=Q(0,1)
    ck('positive_golden_embedding',sign(p)>0 and sign(1-p)>0 and p+p*p==1)
    counts=[(1,1)]
    for n in range(30):
        a,b=counts[-1];counts.append((a+b,a))
    for n,(a,b) in enumerate(counts):
        x,y=p**(n+1),p**(n+2)
        ck('actual_all_level_trace_mass',a*x+b*y==1)
        ck('actual_recurrence_and_nonnegative_weights',x==y+p**(n+3) and sign(x)>0 and sign(y)>0)
        if n<30:ck('count_product_growth',counts[n+1][0]*counts[n+1][1]>=2*a*b)
    for k in range(8):
        a,b=counts[k]
        u,v,w=1,0,1
        for r in range(13):
            A,B=counts[k+r]
            ck('actual_matrix_power_counts',(a*u+b*v,a*v+b*w)==(A,B))
            ck('Cassini_determinant',u*w-v*v==(-1)**r)
            lo,hi=sorted([F(u,A),F(v,B)])
            ck('full_finite_interval_width',hi-lo==F(b,A*B))
            ck('canonical_inside_every_horizon',sign(p**(k+1)-lo)>=0 and sign(hi-p**(k+1))>=0)
            ck('finite_trace_distance_bound',F(a*b,A*B)<=F(1,2**r))
            for c in [F(0),F(1,3),F(1)]:
                s,t=c/A,(1-c)/B
                x,y=u*s+v*t,v*s+w*t
                ck('terminal_state_pullback_full_normalization',a*x+b*y==1 and lo<=x<=hi)
                dx,dy=Q(x)-p**(k+1),Q(y)-p**(k+2)
                distance=F(1,2)*(a*qabs(dx)+b*qabs(dy))
                ck('weighted_trace_distance_reduction',distance==a*qabs(dx))
                ck('actual_finite_horizon_distance',sign(F(a*b,A*B)-distance)>=0)
            u,v,w=u+v,u,v
    # A long positive finite prefix is not positivity on the whole tower.
    x,y=p+F(1,10**8),p*p-F(1,10**8)
    seq=[x,y]
    for n in range(60):seq.append(seq[-2]-seq[-1])
    ck('finite_prefix_not_infinite_selector',all(sign(z)>0 for z in seq[:8]) and any(sign(z)<0 for z in seq))
    for n in range(40):
        e=seq[n+1]-p*seq[n];en=seq[n+2]-p*seq[n+1]
        ck('defect_exact_backward_identity',e==-p*en)
    prepared={}
    for n in [2,3]:
        a,b=counts[n];d=a*a+b*b;t=p**(n+1);u=a*t;v=b*p*t
        ck('full_GNS_dimension',d==[13,34][n-2] and d!=a+b)
        da=[i*a+i for i in range(a)];db=[a*a+i*b+i for i in range(b)]
        O={};E={}
        for i in da:
            for j in da:O[i,j]=K(t);E[i,j]=K(v*F(1,a))
        for i in db:
            for j in db:O[i,j]=K(p*t);E[i,j]=K(u*F(1,b))
        for i in da:
            for j in db:
                O[i,j]=O[j,i]=K(0,t)
                E[i,j]=E[j,i]=K(0,-t)
        Pa=add({(i,i):K(1) for i in range(a*a)}, {(i,j):K(-F(1,a)) for i in da for j in da})
        Pb=add({(i,i):K(1) for i in range(a*a,d)}, {(i,j):K(-F(1,b)) for i in db for j in db})
        projectors=[O,E,Pa,Pb]
        ck('full_orthogonal_decomposition',add(*projectors)==eye(d))
        for i,A in enumerate(projectors):
            ck('all_projectors_selfadjoint_idempotent',transpose(A)==A and mul(A,A)==A)
            ck('full_multiplicities',trace(A)==[1,1,a*a-1,b*b-1][i])
            for j,B in enumerate(projectors):
                if i!=j:ck('mutual_orthogonality',mul(A,B)=={})
        ck('cyclic_state_faithful_only_on_represented_algebra',trace(O)==1 and partial(O,a)==scale(t,eye(a)) and partial(O,b,a*a)==scale(p*t,eye(b)))
        r0=u*v;ra=(u-r0*v)*F(1,a*a-1);rb=(v-r0*u)*F(1,b*b-1)
        ck('positive_complement_weights',all(sign(r)>0 and sign(1-r)>0 for r in [r0,ra,rb]))
        R=add(scale(r0,E),scale(ra,Pa),scale(rb,Pb))
        ck('entire_complement_and_protected_kernel',mul(R,O)=={} and trace(R)==1)
        ck('residual_same_forced_trace',partial(R,a)==scale(t,eye(a)) and partial(R,b,a*a)==scale(p*t,eye(b)))
        # Complete affine fiber: every represented matrix unit has a right
        # inverse under the partial trace. The complex-linear rank is d;
        # the star-preserving map has real Hermitian rank d as well.
        for size,offset in [(a,0),(b,a*a)]:
            for i in range(size):
                for j in range(size):
                    witness={(offset+i*size,offset+j*size):K(1)}
                    ck('partial_trace_surjective_units',partial(witness,size,offset)=={(i,j):K(1)})
        ck('full_extension_affine_dimension',d*d-d==(a**4-a*a)+(b**4-b*b)+2*a*a*b*b)
        for lam in [F(1,2),F(2,3),F(3,4)]:
            rho=add(scale(lam,O),scale(1-lam,R))
            eig=[Q(lam),(1-lam)*r0,(1-lam)*ra,(1-lam)*rb]
            mult=[1,1,a*a-1,b*b-1]
            ck('full_density_trace_and_marginals',trace(rho)==1 and partial(rho,a)==scale(t,eye(a)) and partial(rho,b,a*a)==scale(p*t,eye(b)))
            ck('faithful_state_and_fixed_largest_vector',all(sign(e)>0 for e in eig) and all(sign(lam-e)>0 for e in eig[1:]) and mul(rho,O)==scale(lam,O))
            ck('complete_nonzero_mode_count',sum(mult)==d)
            for e,P in zip(eig,projectors):ck('actual_full_spectral_projectors',mul(rho,P)==scale(e,P))
            ck('cross_block_correlations_not_removed',any(i<a*a<=j and z!=0 for (i,j),z in rho.items()))
            # Complex diagonal phase conjugation on each underlying matrix
            # block acts by i^(row-col) on its matrix units.
            phases=[(i-j)%4 for i in range(a) for j in range(a)]+[(i-j)%4 for i in range(b) for j in range(b)]
            ck('complex_phase_covariance',all((phases[i]-phases[j])%4==0 for (i,j),z in rho.items() if z!=0))
            # A rational rotation is not merely a basis permutation.
            V={(i,i):F(1) for i in range(a)}
            V.update({(0,0):F(3,5),(0,1):-F(4,5),(1,0):F(4,5),(1,1):F(3,5)})
            G={}
            for (i,k),z in V.items():
                for (j,l),w in V.items():G[i*a+j,k*a+l]=K(z*w)
            G.update({(i,i):K(1) for i in range(a*a,d)})
            ck('nontrivial_inner_rotation_covariance',mul(mul(G,rho),transpose(G))==rho)
            Z=F(1,lam)
            ck('ordinary_full_heat_partition',sum((m*e*F(1,lam) for m,e in zip(mult,eig)),Q())==Z)
            ck('ground_zero_reconstruction_no_scalar_modulus',eig[0]==lam and all(sign(e*F(1,lam)-1)<0 for e in eig[1:]))
            for step in [F(1,4),F(1,2)]:
                lam2=lam+step*(1-lam)
                moved=add(scale(1-step,rho),scale(step,O))
                ck('full_cyclic_descent_curve',moved==add(scale(lam2,O),scale(1-lam2,R)))
                ck('descent_retains_exact_observable_trace',partial(moved,a)==scale(t,eye(a)) and partial(moved,b,a*a)==scale(p*t,eye(b)))
                ck('descent_keeps_protected_ground_vector',mul(moved,O)==scale(lam2,O) and lam2>lam and lam2<1)
                ck('strictly_smaller_full_partition',F(1,lam2)<Z)
            prepared[n,lam]=(rho,O,d)
        # A state outside the invariant one-parameter family: correlate two
        # traceless matrix-unit directions across the two full blocks.
        eps=ra*rb*F(1,2)
        cross={(1,a*a+1):K(eps),(a*a+1,1):K(eps)}
        Rp=add(R,cross)
        ck('noncovariant_full_fiber_witness',partial(Rp,a)==scale(t,eye(a)) and partial(Rp,b,a*a)==scale(p*t,eye(b)) and trace(Rp)==1 and mul(Rp,O)=={})
        ck('noncovariant_witness_strict_positivity',sign(ra*rb-eps*eps)>0 and sign(1-ra-rb)>0)
        rhop=add(scale(F(1,2),O),scale(F(1,2),Rp))
        moved=add(scale(F(3,4),rhop),scale(F(1,4),O))
        ck('descent_is_not_only_covariant_family',partial(moved,a)==scale(t,eye(a)) and partial(moved,b,a*a)==scale(p*t,eye(b)) and mul(moved,O)==scale(F(5,8),O))
    a,b=counts[2];df=counts[3][0]**2+counts[3][1]**2;J={}
    for i in range(a):
        for j in range(a):
            J[i*(a+b)+j,i*a+j]=K(0,1)
            J[(a+b)**2+i*a+j,i*a+j]=K(p)
    for i in range(b):
        for j in range(b):J[(a+i)*(a+b)+a+j,a*a+i*b+j]=K(1)
    ck('literal_GNS_embedding_isometry',mul(transpose(J),J)==eye(a*a+b*b))
    ck('literal_cyclic_vector_refines',mul(mul(J,prepared[2,F(1,2)][1]),transpose(J))==prepared[3,F(1,2)][1])
    compressed=mul(mul(transpose(J),prepared[3,F(1,2)][0]),J)
    lost=1-trace(compressed)
    ck('normalized_compression_rejects_faithful_new_modes',lost.y==0 and sign(lost.x)>0)
    ck('all_new_complement_dimensions',df-(a*a+b*b)==21)
    import sympy as s
    beta,lam=s.symbols('beta lam',positive=True)
    ck('true_scalar_price_derivative',s.simplify(s.diff(-s.log(lam)/beta,lam)+1/(beta*lam))==0)
    step=s.symbols('step',real=True)
    ck('universal_cyclic_descent_derivative',s.simplify(s.diff(-s.log(lam+(1-lam)*step)/beta,step).subs(step,0)+(1-lam)/(beta*lam))==0)
    ck('fixed_zero_price_gap',s.expand_log(s.log(2)-s.log(s.Rational(4,3))-s.log(s.Rational(3,2)),force=True)==0)
    return dict(sorted(checks.items()))

MUTATIONS={
    'wrong_incidence':('counts.append((a+b,a))','counts.append((a+b,b))'),
    'wrong_finite_horizon_bound':('F(a*b,A*B)<=F(1,2**r)','F(a*b,A*B)<=F(1,3**r)'),
    'defining_dimension_substitution':('d=a*a+b*b;t=p**(n+1)','d=a+b;t=p**(n+1)'),
    'missing_cross_block_sign':('E[i,j]=E[j,i]=K(0,-t)','E[i,j]=E[j,i]=K(0,t)'),
    'wrong_residual_marginal':('(u-r0*v)*F(1,a*a-1)','(u-r0*u)*F(1,a*a-1)'),
    'missing_retained_density_weight':('scale(1-lam,R)','scale(1,R)'),
    'wrong_partition_normalization':('Z=F(1,lam)','Z=F(1,1-lam)'),
    'discarded_refinement_complement':('lost=1-trace(compressed)','lost=K(0)'),
    'wrong_descent_direction':('lam2=lam+step*(1-lam)','lam2=lam-step*(1-lam)'),
}

def validate(ledger):
    assert ledger['input_head']==INPUT and ledger['scope']==SCOPE
    for path,digest in ledger['inputs'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    receipt=json.loads((ROOT/(STEM+'_results.json')).read_text())
    assert receipt['returncode']==0 and receipt['new_declarations']==16
    assert receipt['axiom_union']==['Classical.choice','Quot.sound','propext']
    capsule=(ROOT/(STEM+'.lean')).read_text()
    names=re.findall(r'^#check (D0\.Research\.AFTracePreparation\.\w+)$',capsule,re.M)
    assert len(names)==len(set(names))==16 and names==receipt['declarations']
    output=(ROOT/(STEM+'_output.txt')).read_text()
    assert not any(x in output for x in ['error:','sorryAx','warning:'])
    assert receipt['capsule_sha256']==hashlib.sha256(capsule.encode()).hexdigest()
    assert receipt['output_sha256']==hashlib.sha256(output.encode()).hexdigest()
    for name in names:assert name in output and "'"+name+"' depends on axioms:" in output
    for path,digest in receipt['transitive_d0_source_sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest

def main():
    global ROOT
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path);ap.add_argument('--math-only',action='store_true');ap.add_argument('--write-certificate',action='store_true')
    args=ap.parse_args();ROOT=args.repo.resolve() if args.repo else Path(__file__).resolve().parents[3]
    load_field(ROOT)
    if args.math_only:print(json.dumps(mathematics()));return
    path=ROOT/(STEM+'_certificate.json')
    if args.write_certificate:
        assert not path.exists(),'refuse to overwrite existing expectations'
        receipt=json.loads((ROOT/(STEM+'_results.json')).read_text())
        pins=set(receipt['transitive_d0_source_sha256'])|{PROOF,STEM+'.lean',STEM+'_check.py',STEM+'_output.txt',STEM+'_results.json',
            '03_FORMALIZATION/lean-toolchain','03_FORMALIZATION/lake-manifest.json',
            '03_FORMALIZATION/D0/Algebra/FibonacciPerronTraceCanonicity.lean',
            '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
            '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md',
            '02_REGISTRY/research/A4D_NATIVE_MODULAR_PREPARATION_BOUNDARY.md'}
        for stem in ['a4d_native_golden_cost_refinement','a4d_native_modular_preparation_boundary']:
            pins.update(str(p.relative_to(ROOT)) for p in (ROOT/'02_REGISTRY/research/certificates').glob(stem+'*') if p.is_file())
        j=dict(input_head=INPUT,scope=SCOPE,inputs={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(pins)},checks=mathematics(),math_mutants=list(MUTATIONS))
        path.write_text(json.dumps(j,indent=2)+'\n')
    ledger=json.loads(path.read_text());validate(ledger)
    checks=mathematics();assert checks==ledger['checks'] and ledger['math_mutants']==list(MUTATIONS)
    text=Path(__file__).read_text();prefix,suffix=text.split('\nMUTATIONS=',1)
    for name,(old,new) in MUTATIONS.items():
        assert prefix.count(old)==1,(name,prefix.count(old))
        with tempfile.TemporaryDirectory(prefix='d0-af-trace-') as folder:
            temp=Path(folder)/'mutant.py';temp.write_text(prefix.replace(old,new)+'\nMUTATIONS='+suffix)
            r=subprocess.run([sys.executable,str(temp),'--repo',str(ROOT),'--math-only'],text=True,capture_output=True,timeout=120)
            assert r.returncode!=0 and 'AssertionError' in r.stderr,(name,r.returncode,r.stderr[-600:])
    rejected=0
    for key,value in SCOPE.items():
        bad=json.loads(json.dumps(ledger));bad['scope'][key]=not value
        try:validate(bad)
        except AssertionError:rejected+=1
        else:raise AssertionError(('false_scope_accepted',key))
    print(json.dumps(dict(verdict='PASS_FULL_AF_TRACE_PREPARATION_BOUNDARY',exact_controls=sum(checks.values()),groups=len(checks),executed_math_mutants_rejected=len(MUTATIONS),false_scope_ledgers_rejected=rejected,new_Lean_propositions=16,native_F_T0_T3_or_GR_closed=False),sort_keys=True))

if __name__=='__main__':main()
