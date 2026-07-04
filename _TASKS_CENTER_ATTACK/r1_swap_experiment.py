import numpy as np

V9 = list(range(0,9)); V11 = list(range(9,20)); V13 = list(range(20,33))
part = {}
for v in V9: part[v]='9'
for v in V11: part[v]='11'
for v in V13: part[v]='13'
edges = []
for a in range(33):
    for b in range(a+1,33):
        if part[a]!=part[b]: edges.append((a,b))
E = len(edges)
eidx = {e:i for i,e in enumerate(edges)}
def edge(a,b): return eidx[(a,b)] if (a,b) in eidx else eidx[(b,a)]
q8 = ['1','i','j','k','-1','-i','-j','-k']
q9idx = {q: 1+i for i,q in enumerate(q8)}

def build(c_zone, d_zone):
    """c-modes (4-cycle carrier) into c_zone; d-modes (role modes) into d_zone."""
    def cmode(q):
        v = np.zeros(E); src=q9idx[q]
        for w in c_zone: v[edge(src,w)] = 1/np.sqrt(len(c_zone))
        return v
    def dmode(q):
        v = np.zeros(E); src=q9idx[q]
        for w in d_zone: v[edge(src,w)] = 1/np.sqrt(len(d_zone))
        return v
    e0 = np.zeros(E)
    for w in V11: e0[edge(0,w)] = 1/np.sqrt(24)
    for w in V13: e0[edge(0,w)] = 1/np.sqrt(24)
    Hmu = [cmode('1'), cmode('i'), cmode('-1'), cmode('-i')]
    rB = (dmode('i')+dmode('-i'))/np.sqrt(2)
    rC = (dmode('j')+dmode('-j'))/np.sqrt(2)
    rD = (dmode('k')+dmode('-k'))/np.sqrt(2)
    Htau = [rB,rC,rD]
    term = [e0]+Hmu+Htau
    G = np.array([[a@b for b in term] for a in term])
    def proj(cols):
        M = np.array(cols).T; return M @ M.T
    P_br = proj(Hmu)+proj(Htau)
    P_term = proj([e0])+P_br
    Q_bulk = np.eye(E)-P_term
    B = np.zeros((E,33))
    for i,(a,b) in enumerate(edges): B[i,a]=1; B[i,b]=1
    L_E = B@B.T - 2*np.eye(E)
    K = Q_bulk @ L_E @ P_br
    brcols = np.array(Hmu+Htau).T
    KtK_br = brcols.T @ (K.T@K) @ brcols
    ev = np.linalg.eigvalsh(KtK_br)
    return G, ev

for name, cz, dz in [("ORIGINAL c->11, d->13", V11, V13),
                     ("SWAPPED  c->13, d->11", V13, V11)]:
    G, ev = build(cz, dz)
    gram_ok = np.allclose(G, np.eye(8))
    rank_ok = np.all(ev > 1e-9)
    print(f"{name}: Gram=I8: {gram_ok} | rank K = 7 (min eig {ev.min():.4f}, max {ev.max():.4f}): {rank_ok}")
    print("   KtK_br eigenvalues:", np.round(ev, 4))
