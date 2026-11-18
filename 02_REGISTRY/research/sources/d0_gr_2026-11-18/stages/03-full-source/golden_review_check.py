import itertools
from sympy import QQ, sqrt
AA=sqrt((sqrt(5)-1)/2)
K=QQ.algebraic_field(AA)
a=K.from_sympy(AA)
p=a*a
Z,O=K.zero,K.one
q=p*p
u=O-q
bits=list(itertools.product(range(2), repeat=6))
def zeros():
    return {b:Z for b in bits}
def j(col):
    out=zeros()
    for key in bits:
        d,c,S,A,B,f=key
        if f==0: out[key]=col[2*c+d]*[a,p][S]*[a,p][A]*[a,p][B]
    return out
def js(col):
    out=[Z]*4
    for (d,c,S,A,B,f),v in col.items():
        if f==0: out[c*2+d]+=v*[a,p][S]*[a,p][A]*[a,p][B]
    return out
def step(key):
    d,c,S,A,B,f=key
    sign=1
    if c==0:
        if A: f^=1
        else:
            # Other known arm is Z X: signed permutation (input 0 maps to -1)
            sign=1 if d else -1
            d^=1
    elif A:
        sign=-1 if d else 1
        d^=1
    else:
        if S==0 and B==1: f^=1
        S^=1
    return (d,c,S,A,B,f),sign
M={key:step(key) for key in bits}
assert len({key for key,sign in M.values()})==64
Mi={out:(inp,sign) for inp,(out,sign) in M.items()}
def apply(v, R):
    tgt=zeros()
    for key,(dest,sign) in R.items(): tgt[dest]=sign*v[key]
    return tgt
def proj(v):
    return j(js(v))
def sub(v,w): return {i:v[i]-w[i] for i in bits}
def scale(s,v):return {i:s*v[i] for i in bits}
def prob(v):return sum((e*e for e in v.values()),Z)
for i in range(4):
    col=[O if i==k else Z for k in range(4)]
    V=apply(j(col),M)
    goal=([Z,-O,Z,Z],[O,Z,Z,Z],[Z,Z,a,p],[Z,Z,-p,a])[i]
    target=j(goal)
    assert js(V)==[p*entry for entry in goal]
    first_fail=sub(V,proj(V))
    assert prob(first_fail)==u
    back=apply(first_fail,Mi)
    for b,returned in enumerate((proj(back),sub(back,proj(back)))):
        out=apply(returned,M)
        final=proj(out)
        assert prob(final)==q*u*u
        assert final==scale([p*u,-p*u][b],target)
        fail=sub(out,final)
        assert fail==scale([u,q][b],first_fail)
print("All 64 signed columns form a permutation; four input columns for coherent ctl(ZX,G) satisfy the stated compression and every retry path over Q(a).")
print("q, lambda, mean calls:",float(K.to_sympy(q)),float(K.to_sympy(2*q*u)),float(K.to_sympy(O+O/q)))
