#!/usr/bin/env python3
"""Check the joint-projector theorem, actual wrappers and independent prices."""
from pathlib import Path
from collections import Counter
from itertools import zip_longest
import hashlib,json
import numpy as np
import full_choi_bank as b
P=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plan=json.loads((P/'FULL_CHOI_BANK_PLAN.json').read_text())
for path,digest in plan['source_sha256'].items():assert h(Path(path))==digest,path
lay=b.layout();b.validate(lay);assert len(b.data(lay)+b.private(lay))==46
extended=dict(lay,qubits=2747);b.validate(extended,range(2739,2747))
for bad in (lay['SAM'][0],b.data(lay)[0],b.private(lay)[0],lay['port'],lay['aux_arbitrary'],lay['oldRIGHT_witness']):
    try:b.validate(extended,[bad])
    except AssertionError:pass
    else:raise AssertionError('accepted external wire collision')
def price(t,port):
    op=t['op']
    if op=='seq':
        out=Counter()
        for child in t['children']:out.update(price(child,port))
        return out
    if op=='repeat':return Counter({k:int(t['count'])*v for k,v in price(t['child'],port).items()})
    return Counter({('G_port' if t['wires'][0]==port else 'G_other') if op=='G' else op:1})
def total(blocks,port):
    out=Counter()
    for t in blocks:out.update(price(t,port))
    return out
def inv(v):return Counter({'G_port':v['G_port']+v['G_other'],'G_other':0,'CX':v['CX']+6*v['G_other'],'SourceI':3*v['SourceI']+4*(v['G_port']+v['G_other'])})
# Recompute the adapter's eight actual levels from leaf inventories instead
# of calling A21/B39's budget recurrence. The Omega provider inventories are
# pinned previously verified child inputs, not a free oracle.
x=b.c.inputs();fixed=b.c.adapter.fixed(b.c.adapter_layout(lay),int(x['phase']['phase_k']),int(x['phase']['correction_l']),x['h_k'])
H=price(fixed['H'],lay['port']);good=total(fixed['good'],lay['port']);start=total(fixed['start'],lay['port']);correction=price(fixed['correction'],lay['port'])
sourceplan=json.loads((b.D/'round21/CHOI_LOADER_PLAN.json').read_text())
for bank in ('y+','y-','f','0','x+','x-','q'):
    cv=Counter({k:int(v) for k,v in sourceplan['banks'][bank]['Omega_forward'].items()});u=H+cv+H
    for _ in range(8):u=u+good+inv(u)+start+u
    u.update(correction);inventory=b.inventory(bank);assert +u==+inventory['U_half_forward']
    r=Counter({'G_other':(1<<46)*b.reflection_k(),'CX':1<<46})
    raw=total(b.raw_zero_blocks(b.data(lay),lay),lay['port']);private=total(b.raw_zero_blocks(b.private(lay),lay),lay['port'])
    full=raw+r+inv(u)+r+u;prepared=private+full
    for name,value in [('bank_forward',full),('bank_literal_inverse',inv(full)),('RAW_prepared_forward',prepared),('RAW_prepared_literal_inverse',inv(prepared))]:
        assert +value==+inventory[name]
        assert all(value[k]==int(plan['native_inventories'][bank][name][k]) for k in ('G_port','G_other','CX','SourceI'))
assert +raw==+Counter({'G_port':22,'CX':132,'SourceI':88}) and +private==+Counter({'G_port':24,'CX':144,'SourceI':96})

# Small fully emitted native wrapper: independently materialize one forward
# DAG and repeatedly invert THAT paid DAG. This catches inverse-of-inverse
# cancellation and reverse-order mistakes at the U and preparation boundary.
toy={'SAM':[],'address':[],'choi_input':[],'choi_output':[0],'branch':1,'phase_rebit':2,'comparator_scratch':[],
     'port':4,'spin':[5,6],'aux_arbitrary':3,'oldRIGHT_witness':7,'qubits':8}
U=b.nb.seq(b.nb.gate('G',0),b.nb.gate('CX',1,0),b.nb.gate('SourceI',4,5,6),b.nb.gate('G',3))
saved=(b.validate,b.reflection_k,b.c.half_blocks)
def toy_U(bank,lay=None,levels=8,inverse_depth=0):yield b.inverse(U,inverse_depth,toy)
def flat(trees):
    for tree in trees:yield from b.nb.expand(tree,1000000)
toy_reports=[]
try:
    b.validate=lambda lay,extra_external=():None;b.reflection_k=lambda:1;b.c.half_blocks=toy_U
    for init in (False,True):
        literal=b.nb.seq(*b.bank_blocks('f',toy,initialize_private=init));expected_price=price(literal,toy['port'])
        for depth in range(4):
            own=list(b.bank_blocks('f',toy,depth,initialize_private=init));count=0
            for left,right in zip_longest(flat(own),b.nb.expand(literal,1000000)):
                assert left==right,(init,depth,count);count+=1
            assert +total(own,toy['port'])==+expected_price
            toy_reports.append({'initialize_private':init,'inverse_depth':depth,'literal_primitive_leaves_equal':count})
            literal=b.nb.inverse_literal(literal,toy['port'],tuple(toy['spin']));expected_price=inv(expected_price)
finally:b.validate,b.reflection_k,b.c.half_blocks=saved

# General isometry argument is analytic in the accompanying proof. This
# diagnostic deliberately uses an arbitrary U extension that entangles the
# external factor away from the joint anchor. Merely DATA-only reflection
# would not justify the all-column conclusion for such an extension.
mm=lambda a,c:np.einsum('ij,jk->ik',a,c,optimize=False)
omega=np.asarray([2.,1.,3.,4.]);omega/=np.linalg.norm(omega);r=np.asarray([1.,0.,0.,0.]);co=omega[0]
u=(r+omega)/np.sqrt(2*(1+co));uj=np.zeros(8);uj[::2]=u;rj=np.eye(8)[:,0];v=rj-uj;v/=np.linalg.norm(v)
F=np.eye(8)-2*np.outer(v,v);rng=np.random.default_rng(220046);q,_=np.linalg.qr(rng.normal(size=(14,14)));W=np.eye(16);W[2:,2:]=q
Uideal=mm(np.kron(F,np.eye(2)),W);J=np.eye(16)[:,:2];V=np.kron(uj[:,None],np.eye(2));assert np.max(abs(mm(Uideal,J)-V))<1e-15
R=np.eye(16);R[0,0]=R[1,1]=-1
K=np.outer(omega,r)-np.outer(r,omega);O=np.eye(4)+K+mm(K,K)/(1+co)
p=(np.sqrt(5)-1)/2;G=np.asarray([[np.sqrt(p),-p],[p,np.sqrt(p)]]);rawdata=np.kron(G.T,G.T);rawfull=np.kron(np.kron(rawdata,np.eye(2)),np.eye(2))
E=np.zeros((16,8))
for d in range(4):
    for e in range(2):E[4*d+e,2*d+e]=1
expected=mm(E,np.kron(mm(O,rawdata),np.eye(2)))
actual=mm(mm(mm(mm(mm(Uideal,R),Uideal.T),R),rawfull),E);idealerr=float(np.max(abs(actual-expected)));assert idealerr<2e-15
epsilon=.001;perturb=np.eye(16);i,j=0,7;perturb[i,i]=perturb[j,j]=np.cos(epsilon);perturb[j,i]=np.sin(epsilon);perturb[i,j]=-np.sin(epsilon)
Uactual=mm(perturb,Uideal);epsR=.0002;Ractual=R.copy();angle=np.pi+epsR;Ractual[:2,:2]=[[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]]
eta=float(np.linalg.norm(mm(Uactual,J)-V,2));delta=float(np.linalg.norm(Ractual-R,2))
actual=mm(mm(mm(mm(mm(Uactual,Ractual),Uactual.T),Ractual),rawfull),E);actualerr=float(np.linalg.norm(actual-expected,2));assert actualerr<=4*eta+2*delta
b.errors()
out={'status':'PASS_FULL_RAW_CHOI_JOINT_REFLECTION_ASSEMBLY','plan_sha256':h(P/'FULL_CHOI_BANK_PLAN.json'),'checker_sha256':h(Path(__file__)),
     'all7_bank_resource_recurrences_independently_recomputed':True,'literal_wrapper_checks':toy_reports,
     'arbitrary_external_extension_diagnostic':{'original_DATA_columns':4,'external_columns':2,'private_clean_wires':1,'ideal_max_entry_error':idealerr,'perturbed_operator_error':actualerr,'bound_4eta_plus2delta':4*eta+2*delta},
     'diagnostic_is_not_full_dimension_numerical_execution':True,'analytic_full_dimension_isometry_projector_proof_in_document':True,
     'DATA22_RAW_inverse_included':True,'private24_RAW_initializer_compiled_and_priced':True,'new_reflection_clean_work':0,
     'external_SITE_namespace_disjointness_checked':True,'unitary_error_on_clean_private_lt':'2^-3227','all1260_Choi_error_lt':'2^-3216',
     'giant_R46_sequence_enumerated':False,'full_giant_word_executed':False,'physical_C_closed':False,'GR_closed':False}
(P/'FULL_CHOI_BANK_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({key:out[key] for key in ('status','new_reflection_clean_work','all1260_Choi_error_lt')}))
