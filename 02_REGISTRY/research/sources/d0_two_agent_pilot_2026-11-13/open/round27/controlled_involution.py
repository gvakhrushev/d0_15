#!/usr/bin/env python3
"""Compile Hadamard-controlled V_delta for known basis labels a,b.
Logical primitive grammar X,CX,CCX,Z,CZ; no native H1 admission implied.
Bits are little-endian; clean scratch is part of the declared input contract.
"""
from collections import Counter
from dataclasses import dataclass

@dataclass(frozen=True)
class Gate:
 op:str
 wires:tuple

def layout(n):
 assert n>=2
 # Clean controls: h,delta may be arbitrary/entangled; membership/work/q born 0.
 return {'n':n,'data':list(range(n)),'hadamard':n,'delta':n+1,
         'membership':n+2,'work':list(range(n+3,n+3+max(0,n-3))),
         'phase_work':n+3+max(0,n-3),'qubits':n+4+max(0,n-3)}

def compile_pair(n,a,b):
 assert n>=2 and 0<=a<2**n and 0<=b<2**n and a!=b
 L=layout(n);h=L['hadamard'];delta=L['delta'];m=L['membership'];q=L['phase_work'];work=L['work']
 diff=[j for j in range(n) if ((a^b)>>j)&1];pivot=diff[0];others=diff[1:]
 controls=[j for j in range(n) if j!=pivot]
 # T sends the two selected strings to the SAME n−1 control pattern.
 desired={j:((a>>j)&1)^(((a>>pivot)&1) if j in others else 0) for j in controls}
 flip=[j for j in controls if desired[j]==0]
 gate=lambda op,*w:Gate(op,tuple(w));gates=[]
 def member_toggle():
  for j in others:gates.append(gate('CX',pivot,j))
  for j in flip:gates.append(gate('X',j))
  if len(controls)==1:gates.append(gate('CX',controls[0],m))
  elif len(controls)==2:gates.append(gate('CCX',controls[0],controls[1],m))
  else:
   gates.append(gate('CCX',controls[0],controls[1],work[0]))
   for k in range(2,len(controls)-1):gates.append(gate('CCX',work[k-2],controls[k],work[k-1]))
   gates.append(gate('CCX',work[len(controls)-3],controls[-1],m))
   for k in range(len(controls)-2,1,-1):gates.append(gate('CCX',work[k-2],controls[k],work[k-1]))
   gates.append(gate('CCX',controls[0],controls[1],work[0]))
  for j in reversed(flip):gates.append(gate('X',j))
  for j in reversed(others):gates.append(gate('CX',pivot,j))
 member_toggle()
 # Conditional sign −1 exactly for h=delta=1 and x outside {a,b}.
 gates += [gate('CCX',h,delta,q),gate('Z',q),gate('CZ',q,m),gate('CCX',h,delta,q)]
 # Controlled transposition; membership is invariant under this operation.
 for j in diff:gates.append(gate('CCX',h,m,j))
 member_toggle()
 allowed={'X':1,'CX':2,'CCX':3,'Z':1,'CZ':2}
 for g in gates:
  assert g.op in allowed and len(g.wires)==allowed[g.op] and len(set(g.wires))==len(g.wires) and all(0<=w<L['qubits'] for w in g.wires)
 count=Counter(g.op for g in gates)
 if n>=3:
  expected={'X':4*len(flip),'CX':4*len(others),'CCX':4*n-8+len(diff),'Z':1,'CZ':1}
  assert all(count[k]==v for k,v in expected.items()),(n,a,b,count,expected)
 return {'n':n,'a':a,'b':b,'diff_bits':diff,'pivot':pivot,'normalization_flips':flip,
         'layout':L,'gates':gates,'counts':dict(sorted(count.items())),'clean_scratch':[m,*work,q]}

def interpret(gates,state):
 """Signed permutation for a single full computational basis column."""
 phase=1
 for g in gates:
  op,w=g.op,g.wires
  if op=='X':state^=1<<w[0]
  elif op=='CX':state^=((state>>w[0])&1)<<w[1]
  elif op=='CCX':state^=(((state>>w[0])&(state>>w[1]))&1)<<w[2]
  elif op=='Z':phase*=(-1)**((state>>w[0])&1)
  elif op=='CZ':phase*=(-1)**(((state>>w[0])&(state>>w[1]))&1)
  else:raise ValueError(op)
 return state,phase

def expected(n,a,b,x,h,delta):
 member=x==a or x==b
 return ((x^(a^b)) if h and member else x),(-1 if h and delta and not member else 1)

def serial(c):
 return {**{k:v for k,v in c.items() if k!='gates'},'gates':[{'op':g.op,'wires':g.wires} for g in c['gates']]}

def choi_label(address,input_,output):
 assert 0<=address<4096 and 0<=input_<32 and 0<=output<32
 return (address<<10)|(input_<<5)|output

def car_label(site,grade):
 assert 0<=site<256 and 0<=grade<16
 return (site<<4)|grade

def inverse_gates(circuit):
 """Exact inverse on ALL input columns: each logical primitive is involutive."""
 return tuple(reversed(circuit['gates']))
