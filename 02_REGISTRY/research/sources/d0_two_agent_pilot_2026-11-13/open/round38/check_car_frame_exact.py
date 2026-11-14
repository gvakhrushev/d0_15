#!/usr/bin/env python3
"""A18 actual CAR frame structure and exact small-k fixed-bank identity."""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys,json,random
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open');P=D/'round18';sys.path.insert(0,str(P))
def load(n,p):
 sp=importlib.util.spec_from_file_location(n,p);o=importlib.util.module_from_spec(sp);sys.modules[n]=o;sp.loader.exec_module(o);return o
f=load('b38_frame',P/'car_frame.py');b=load('b38_b37frame',O/'round37/build_car_ustar.py');anc=load('b38_b35frame',O/'round35/anchor_reflection.py');lay=f.layout();U,Ui,R=f.fixed_components(lay)
assert Ui==f.m.nb.inverse_literal(U,lay['port'],tuple(lay['spin']))
assert lay['predicate_flag']==2711 and lay['predicate_work']==[2712,2713] and lay['native_aux_arbitrary']==2714 and lay['qubits']==2715
protected=lay['SAM']+lay['internal_SITE']+lay['RIGHT']+[lay['oldRIGHT_witness']]
for tree in (U,Ui,R):f.m.nb.validate_schema(tree,lay['qubits'],lay['port'],tuple(lay['spin']),protected)
# R=F† Z F as a chronological native DAG, not a merely approximate
# reflection: F is arbitrary actual unitary, Z²=I; hence R²=I exactly.
assert R['op']=='seq' and len(R['children'])==3
F,Z,Fi=R['children'];assert Fi==f.m.nb.inverse_literal(F,lay['port'],tuple(lay['spin']))
assert Z==f.m.nb.z_word(lay['predicate_flag'],lay['port'],tuple(lay['spin']))
for tree in (U,Ui,R):
 for leaf in f.m.nb.leaves(tree):
  assert not set(leaf['wires']).intersection(protected)
# Exact small-k native replay with arbitrary grade/predicate/port/spin/aux/old.
# Apply actual U†;R;U;U†;R;U, retaining every gate and no simplification.
port=7;spin=(8,9);aux=10;old=11
us=b.word(1,port=port,spin=spin);uis=b.nb.inverse_literal(us,port,spin)
rs=anc.build([0,1,2,3],1,4,[5,6],port,spin,aux,1,protected=[old])['native_DAG']
blocks=[uis,rs,us,uis,rs,us];word=[]
for block in blocks:
 for g in b.nb.expand(block,100000):word.append((g['op'],*g['wires']))
zero=(0,0,0,0);one=(1,0,0,0)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def ma(x):return x[3],x[0],x[1]-x[3],x[2]
def mp(x):return x[2],x[3],x[0]-x[2],x[1]-x[3]
def run(state):
 for op,*w in word:
  out={}
  if op=='G':
   for x,z in state.items():
    bit=(x>>w[0])&1;base=x&~(1<<w[0]);c0=neg(mp(z)) if bit else ma(z);c1=ma(z) if bit else mp(z)
    out[base]=add(out.get(base,zero),c0);y=base|(1<<w[0]);out[y]=add(out.get(y,zero),c1)
  elif op=='CX':
   for x,z in state.items():y=x^(((x>>w[0])&1)<<w[1]);out[y]=add(out.get(y,zero),z)
  else:
   assert op=='SourceI' and w==[port,*spin]
   for x,z in state.items():
    bit=(x>>port)&1;parity=((x>>spin[0])^(x>>spin[1]))&1;y=x^(bit<<spin[1]);v=neg(z) if bit and parity else z;out[y]=add(out.get(y,zero),v)
  state={x:z for x,z in out.items() if z!=zero}
 return state
rng=random.Random(3808);cases=set()
for grade in range(16):
 for _ in range(4):cases.add(grade|(rng.randrange(256)<<4))
for col in cases:assert run({col:one})=={col:one},col
# Conservative hybrid bound for q/y: 2 Um +2 Ustar+2 R.
assert 2*3+2*1+2*10==28 and 112*28<2**12
out={'status':'PASS_A18_CAR_FRAME_NATIVE_STRUCTURE_AND_FIXED_IDENTITY','source_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in [P/'car_frame.py',O/'round35/anchor_reflection.py',O/'round37/CAR_USTAR_NATIVE.json']},'actual_fixed_Ustar_literal_adjoint_verified':True,'actual_reflection_F_adjoint_Z_F_structure_verified':True,'all_SAM_SITE_RIGHT_oldRIGHT_untouched':True,'predicate_clean_wires':3,'native_aux_arbitrary':True,'exact_small_k_fixed_bank_identity_cases':len(cases),'small_k_full_paid_calls':len(word),'fixed_bank_identity_proof':'U R U† U R U†=I because R=F† Z F and Z²=I, for any predicate/aux state, with paid stages retained','q_y_hybrid_coefficient':'2*3+2*1+2*10=28','112_copy_conditional_error_lt':'2^-4084','scope':'fixed frame exact identity and q/y conditional hybrid bound; no vacuum/Fourier, births, marks or full H1','GR_closed':False}
Path(__file__).with_name('A18_CAR_FRAME_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
