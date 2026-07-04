#!/usr/bin/env python3
"""Round-2 directed seam (committed per skeptic #7 requirement): edge carrier, Q8-contact split,
directed Hashimoto archive. Reports the moment triple; targets (1/3, 12288/5, 0). Report-only."""
import numpy as np
V9=list(range(0,9));V11=list(range(9,20));V13=list(range(20,33))
part={}
for v in V9: part[v]='9'
for v in V11: part[v]='11'
for v in V13: part[v]='13'
dir_edges=[(a,b) for a in range(33) for b in range(33) if a!=b and part[a]!=part[b]]
NE=len(dir_edges); di={e:k for k,e in enumerate(dir_edges)}
B=np.zeros((NE,NE))
for (u,v),k in di.items():
    for w in range(33):
        if part[v]!=part[w] and w!=u and w!=v: B[k,di[(v,w)]]=1
q9={q:1+i for i,q in enumerate(['1','i','j','k','-1','-i','-j','-k'])}
def star(src,zone):
    v=np.zeros(NE)
    for w in zone: v[di[(src,w)]]=1; v[di[(w,src)]]=1
    return v/np.linalg.norm(v)
Hmu=[star(q9[q],V11) for q in ['1','i','-1','-i']]
def dm(q): return star(q9[q],V13)
rB=(dm('i')+dm('-i')); rC=(dm('j')+dm('-j')); rD=(dm('k')+dm('-k'))
rB/=np.linalg.norm(rB); rC/=np.linalg.norm(rC); rD/=np.linalg.norm(rD)
e0=np.zeros(NE)
for w in V11+V13: e0[di[(0,w)]]=1; e0[di[(w,0)]]=1
e0/=np.linalg.norm(e0)
M=np.array([e0]+Hmu+[rB,rC,rD]).T
assert np.allclose(M.T@M,np.eye(8)), "Gram"
P=M@M.T; Q=np.eye(NE)-P
Bs=P@B@Q; Ns=Q@B@Q; Cs=Q@B@P
m1=np.trace(Bs@Cs)/3; m2=np.trace(Bs@Ns@Cs); m3=np.trace(Bs@Ns@Ns@Cs)
print(f"round-2: mu1={m1:.6f} mu2={m2:.6f} mu3={m3:.6f} ratio={m2/(3*m1):.4f} (targets 1/3, 12288/5, 0; ratio 2457.6)")
