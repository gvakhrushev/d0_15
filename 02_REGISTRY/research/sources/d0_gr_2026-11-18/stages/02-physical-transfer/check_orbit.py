"""Enumerate the original signed permutations, all key labels and both schedules."""
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import json
import sys
import sympy as sp

sys.path.insert(0,str(Path(__file__).resolve().parent / "primary"))
import native_execution as native

bus, spin1, spin2, data, old, flag = range(6)
def cx(src, dst):
    return native.Gate("CX",(src,dst))
def swap(i,j):
    return (cx(i,j),cx(j,i),cx(i,j))
def phase(q,n):
    wire = swap(bus,q)
    return wire+(native.Gate("SourceI",(bus,spin1,spin2)),)*n+wire
phase_bd = phase(flag,1)+phase(data,1)+(cx(flag,data),)+phase(data,3)+(cx(flag,data),)
plus, minus = phase_bd+(cx(flag,data),), (cx(flag,data),)+phase_bd
sign_word = {1:plus,-1:minus}
fixture = native.Execution(6,(flag,),(old,),plus,native.G_CX_SOURCE_I,bus,(spin1,spin2))
native.validate_execution(fixture,max_qubits=6,max_expanded_stages=100)
maps = {}
for g in set(plus):
    matrix = native.gate_matrix(fixture,g,max_qubits=6)
    table = {}
    for (r,c),v in matrix.todok().items():
        assert c not in table and v in (-1,1)
        table[c] = (r,int(v))
    assert table[0]==(0,1) and len(table)==64
    maps[g]=table

def apply(g, state):
    x,sgn=state
    y,coefficient=maps[g][x]
    return y,sgn*coefficient

def bit(w):
    return 1<<(5-w)
core = bit(bus)|bit(data)|bit(flag)
active = core|bit(spin2)
states = {(x,s) for x in range(64) if x&core and x&~active==0 for s in (-1,1)}
base=(bit(flag),1)
found={base}
while True:
    expanded=found|{apply(g,state) for g in maps for state in found}
    if expanded==found:
        break
    found=expanded
assert found==states and len(states)==28
for g in maps:
    assert {apply(g,state) for state in states}==states

def trajectory(word, initial):
    seq=[]
    st=initial
    for g in word:
        nxt=apply(g,st)
        seq.append((g.op,g.wires,st,nxt))
        st=nxt
    return seq,st

# At each absolute tick, compare full histories of the preceding window,
# including their actual intermediate states as well as all physical addresses.
def window_counts(same, lookback, guard):
    table=defaultdict(Counter)
    padding=(cx(flag,data),cx(flag,data))*(guard//2)
    for sign in [-1,1]:
        word=sign_word[sign]+padding+sign_word[sign if same else -sign]
        for state in states:
            seq,last=trajectory(word,state)
            x,t=state
            assert last==(x,-t if same and x&bit(flag) else t)
            for j in range(len(seq)):
                table[j][tuple(seq[max(0,j+1-lookback):j+1])]+=1
    return table

for window,guard in [(1,0),(3,4),(8,8)]:
    assert window_counts(True,window,guard)==window_counts(False,window,guard)

p=native.P
q=4*p**3
def measure(state):
    x,sgn=state
    if x==bit(flag):
        return 0 if sgn==1 else q
    return 2*p**3 if x&bit(flag) else p**2

joint_abs=0
conditional_entropy_inputs=[Counter(),Counter()]
counts={}
for same in [False,True]:
    hits=Counter()
    for sign in [-1,1]:
        word=sign_word[sign]+sign_word[sign if same else -sign]
        for state in states:
            seq,last=trajectory(word,state)
            # Occupation on the nonzero computational basis path, at SourceI only.
            hits[sum(op=="SourceI" and bool(st[0]&bit(bus)) for op,_,st,_ in seq)]+=1
            conditional_entropy_inputs[int(same)][sp.simplify(measure(last))]+=1
            if same:
                joint_abs+=abs(measure(state)-measure(last))
    counts[str(same)]=dict(sorted(hits.items()))
assert conditional_entropy_inputs[0]==conditional_entropy_inputs[1]
assert sp.simplify(joint_abs/56-q/14)==0
assert sp.simplify(q/28-(measure((bit(flag),-1))-measure(base))/28)==0
z=sp.symbols("z")
def polynomial(distribution):
    return sum(sp.Rational(count,56)*z**n for n,count in distribution.items())
tilt=sp.factor(polynomial(counts["True"])-polynomial(counts["False"]))
# This independent endpoint toll is positive on every edge and telescopes.
potential=lambda state: int(state==base)
boltzmann=0
for state in states:
    _,last=trajectory(plus+plus,state)
    boltzmann+=p**(potential(last)-potential(state))
assert sp.simplify(boltzmann-28-(1/p+p-2))==0
print(json.dumps({"status":"PASS","mask_orbit":len(states),"programmes":4,
    "tested_history_windows":[1,3,8],"guard_lengths":[0,4,8],
    "total_variation_given_ready":float(q/14),"single_event_contrast":float(q/28),
    "joint_entropy_equal":True,"source_active_path_histograms":counts,
    "source_active_moment_difference":str(tilt),
    "endpoint_toll_mass_excess":float((1/p+p-2)/28),"physical_C_closed":False},indent=2))
