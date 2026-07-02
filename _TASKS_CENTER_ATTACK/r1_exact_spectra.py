import sympy as sp

V9 = list(range(0,9)); V11 = list(range(9,20)); V13 = list(range(20,33))
part = {}
for v in V9: part[v]='9'
for v in V11: part[v]='11'
for v in V13: part[v]='13'
edges = [(a,b) for a in range(33) for b in range(a+1,33) if part[a]!=part[b]]
E = len(edges)
eidx = {e:i for i,e in enumerate(edges)}
def edge(a,b): return eidx[(a,b)] if (a,b) in eidx else eidx[(b,a)]
q9idx = {q: 1+i for i,q in enumerate(['1','i','j','k','-1','-i','-j','-k'])}

def spectra(c_zone, d_zone):
    nc, nd = len(c_zone), len(d_zone)
    def cmode(q):
        v = [sp.S(0)]*E
        for w in c_zone: v[edge(q9idx[q],w)] = 1/sp.sqrt(nc)
        return sp.Matrix(v)
    def dmode(q):
        v = [sp.S(0)]*E
        for w in d_zone: v[edge(q9idx[q],w)] = 1/sp.sqrt(nd)
        return sp.Matrix(v)
    e0v = [sp.S(0)]*E
    for w in V11: e0v[edge(0,w)] = 1/sp.sqrt(24)
    for w in V13: e0v[edge(0,w)] = 1/sp.sqrt(24)
    e0 = sp.Matrix(e0v)
    Hmu = [cmode('1'), cmode('i'), cmode('-1'), cmode('-i')]
    Ht = [(dmode(a)+dmode('-'+a))/sp.sqrt(2) for a in ['i','j','k']]
    modes = [e0]+Hmu+Ht
    br = Hmu+Ht
    # K = Q_bulk L_E P_br ; KtK on branch basis: compute via L_E action on branch modes
    # L_E = B B^T - 2I ; (L_E v)[e] = sum over edges f sharing a vertex with e of v[f] (incl. 2v[e]) - 2 v[e]
    # do it exactly via B
    B = sp.zeros(E,33)
    for i,(a,b) in enumerate(edges): B[i,a]=1; B[i,b]=1
    Mbr = sp.Matrix.hstack(*br)          # E x 7
    Mterm = sp.Matrix.hstack(*modes)     # E x 8
    LEbr = B*(B.T*Mbr) - 2*Mbr           # E x 7 = L_E P_br basis vectors
    # Q_bulk applied: subtract projections onto the 8 terminal modes
    coeffs = Mterm.T*LEbr                # 8 x 7
    QLEbr = LEbr - Mterm*coeffs
    KtK = (QLEbr.T)*QLEbr                # 7 x 7 exact
    KtK = sp.simplify(KtK)
    x = sp.symbols('x')
    cp = sp.factor(KtK.charpoly(x).as_expr())
    return cp

cp1 = spectra(V11, V13)
cp2 = spectra(V13, V11)
print("ORIGINAL (c->11,d->13) charpoly:"); sp.pprint(cp1)
print("SWAPPED  (c->13,d->11) charpoly:"); sp.pprint(cp2)
