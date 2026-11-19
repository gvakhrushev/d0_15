"""Check the two pre-reader intervals on the pinned native all-column operators."""
import argparse
from collections import Counter
from decimal import Decimal, localcontext
from functools import lru_cache
import hashlib
import json
from math import isqrt
from pathlib import Path
import subprocess
import sys
from types import ModuleType

REV = "15f5b786ed912a0e91d660e337bf60a7c15c7cfa"
OWNER = "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
SHA = "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
GRID = 10**68

def check(condition, message):
    if not condition:
        raise ValueError(message)

def native(repo):
    raw = ((Path(__file__).resolve().parents[1] / "frozen/native_execution.py").read_bytes()
           if repo is None else subprocess.check_output(["git","-C",str(repo),"show",REV+":"+OWNER]))
    check(hashlib.sha256(raw).hexdigest() == SHA,"native owner SHA-256")
    mod = ModuleType("pinned_coherence_native")
    sys.modules[mod.__name__] = mod
    exec(compile(raw, OWNER, "exec"),mod.__dict__)
    return mod

def compose(a,b):
    return tuple((1 if n>0 else -1)*a[abs(n)-1] for n in b)

def inverse(a):
    out = [0]*len(a)
    for i,n in enumerate(a):
        out[abs(n)-1] = (1 if n>0 else -1)*(i+1)
    return tuple(out)

def mul(a,b):
    xs = [x*y for x in a for y in b]
    return min(xs)//GRID, -((-max(xs))//GRID)

def scale(a,n):
    return min(n*a[0],n*a[1]), max(n*a[0],n*a[1])

def add(a,b):
    return a[0]+b[0],a[1]+b[1]

def div(a,b):
    check(b[0]>0,"denominator strictly positive")
    return (min(x*GRID//y for x in a for y in b),
            max(-((-x*GRID)//y) for x in a for y in b))

def display(a):
    with localcontext() as ctx:
        ctx.prec = 90
        return [str(Decimal(i)/Decimal(GRID)) for i in a]

def coefficients():
    sqrt5 = isqrt(5*GRID**2)
    p = (sqrt5-GRID)//2,(sqrt5+1-GRID+1)//2
    a = isqrt(p[0]*GRID),isqrt(p[1]*GRID)+1
    c,s = a,p
    for _ in range(9):
        c,s = add(mul(c,c),scale(mul(s,s),-1)), scale(mul(c,s),2)
    check(c[1]<0 and s[0]>0,"actual 512-angle sign")
    cot = div(c,s)
    p7=(GRID,GRID)
    for _ in range(7):
        p7=mul(p7,p)
    q0=scale(mul(mul(s,s),p7),4)
    gamma=mul(q0,cot)
    check(q0[0]*1000>129*GRID and q0[1]*100<13*GRID,"actual target coframe centre")
    check(gamma[0]*1000>-34*GRID and gamma[1]*1000<-33*GRID,"target coherence margin")
    pure = scale(cot,4)
    physical = mul(mul(a,p),pure)
    noisy = mul(mul(p,mul(p,p)),physical)
    check(noisy[0]*1000 > -119*GRID and noisy[1]*1000 < -118*GRID,"noisy fee slope")
    return {"kappa":display(mul(s,s)),"cot":display(cot),"target_Q0":display(q0),
            "target_gamma0":display(gamma),
            "X_difference_per_DQ":display(pure),"rotated_event_difference_per_DQ":display(physical),
            "parsed_length_difference_per_DQ":display(noisy)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path,default=None)
    ne = native(ap.parse_args().repo)
    s,e,r,t = 0,3,4,5
    def cx(i,j):
        return ne.Gate("CX",(i,j))
    c = cx(e,r)
    swap = (cx(s,e),cx(e,s),cx(s,e))
    z = swap+(ne.Gate("SourceI",(s,1,2)),)*2+swap
    neutral = (cx(r,t),)*len(z)
    def execution(word):
        return ne.Execution(6,(e,r,t),(),tuple(word),ne.G_CX_SOURCE_I,s,(1,2),())
    @lru_cache(maxsize=None)
    def op(g):
        M = ne.gate_matrix(execution((g,)),g)
        entries = M.todok()
        check(len(entries)==64,"one signed image per basis vector")
        out = [0]*64
        for (row,col),sign in entries.items():
            check(sign in (-1,1),"exact signed permutation")
            out[col] = int(sign)*(row+1)
        check(sorted(abs(x) for x in out)==list(range(1,65)),"bijective")
        return tuple(out)
    identity = tuple(range(1,65))
    def prefixes(word):
        ne.validate_execution(execution(word),max_qubits=6,max_expanded_stages=200)
        out = [identity]
        for g in word:
            out.append(compose(op(g),out[-1]))
        return out
    z_exp = tuple(((-1 if x & (1<<(5-e)) else 1)*(x+1)) for x in range(64))
    check(prefixes(z)[-1]==z_exp,"routed Z_e with live unknown source port and Spin")
    check(prefixes(neutral)[-1]==identity,"paid time-matched neutral word")
    results={}
    for name,A,B in (
        ("short",z+z+(c,),z+(c,)+z),
        ("synchronised",neutral+(c,)+z+z,z+(c,)+neutral+z),
    ):
        check(Counter(A)==Counter(B),"identical addressed gate inventory")
        pa,pb=prefixes(A),prefixes(B)
        check(pa[-1]==pb[-1]==op(c),"both full endpoints equal literal CX")
        gauges=[compose(y,inverse(x)) for x,y in zip(pa,pb)]
        check(gauges[0]==gauges[-1]==identity,"all-column boundary gauge")
        for j in range(len(A)):
            check(op(B[j])==compose(gauges[j+1],compose(op(A[j]),inverse(gauges[j]))),"every native stage intertwines")
        ia,ib=A.index(c),B.index(c)
        check(pa[ia]==identity and pb[ib]==z_exp,"opposite visibility at addressed CX input")
        if name=="synchronised":
            check(ia==ib and gauges[ia]==z_exp,"time-matched event gauge")
        results[name]={"stages":len(A),"one_based_reader_stages":[ia+1,ib+1],"gate_count":dict(Counter(g.op for g in A))}
    print(json.dumps({"status":"PASS","commit":REV,"native_sha256":SHA,"checked_columns":64,
        "intervals":results,"outward_bounds":coefficients(),
        "scope":"Block all-column conjugacy and literal comparator contrasts. Neither full Book price evaluation nor an EO coherent-jet certificate."},indent=2))

if __name__=="__main__":
    main()
