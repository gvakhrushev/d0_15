"""Stage-resolved paid positive word for the two RAW returns; d=trace distance of a purified before/after pair."""
from collections import Counter
from pathlib import Path
import sys

import numpy as np

DIRECT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(DIRECT / "round79" / "memory"))
from check_cold_compensation import raw_bank, product, native
from math import sqrt

p=(sqrt(5)-1)/2
a=sqrt(p)
gate=native.Gate
spin=(0,1)
port=2
src=gate('SourceI',(port,*spin))


def swap(i,j):
    return (gate('CX',(i,j)),gate('CX',(j,i)),gate('CX',(i,j)))


def words(order):
    bank=gate('CX',order)
    enc=gate('CX',(4,5))
    forward=(bank,gate('CX',(2,4)),src,src,bank,enc,gate('G',(5,)),enc)
    context=native.Execution(6,(),(),forward,native.G_CX_SOURCE_I,port,spin)
    inverse=native.inverse_word(context,max_qubits=6,max_expanded_stages=100)
    route=swap(4,2)
    phase=route+(src,src)+route
    return context,(forward,phase,inverse)


def measure_word():
    from itertools import combinations
    controls=range(2,6)
    context=native.Execution(8,(),(),(),native.G_CX_SOURCE_I,port,spin)
    def inv_g(q):
        tiny=native.Execution(8,(),(),(gate('G',(q,)),),native.G_CX_SOURCE_I,port,spin)
        return native.inverse_word(tiny,max_qubits=8,max_expanded_stages=11)
    def conditional(pointer,inverse):
        result=[]
        core=inv_g(pointer) if inverse else (gate("G",(pointer,)),)
        for k in range(5):
            for subset in combinations(controls,k):
                cx=tuple(gate('CX',(q,pointer)) for q in subset)
                result.extend(cx+core+cx[::-1])
        return tuple(result)
    gates=sum((inv_g(q) for q in (*controls,6,7)),())
    gates+=conditional(6,False)+(gate('G',(7,)),)*16+conditional(7,True)
    gates+=tuple(gate("G",(q,)) for q in controls)
    native.inventory(native.Execution(8,(),(),gates,native.G_CX_SOURCE_I,port,spin),
                     max_qubits=8,max_expanded_stages=len(gates))
    return gates


def simulation(order, xp):
    # At the +i spin eigenvalue SourceI acts as multiplication by i on its active rows.
    # In the real representation, every entry A+iB below means A I_spin + B L_i.
    one=xp.mpf(1)
    pp=(xp.sqrt(5)-1)/2
    aa=xp.sqrt(pp)
    rr=xp.mpc
    def zero(): return rr(0)
    def tensor_v(state,n):
        for _ in range(n):
            state=[s*q for s in state for q in (aa,pp)]
        return state
    def apply(state,g):
        bits=2+(len(state)-1).bit_length()
        mask=lambda q: 1<<(bits-1-q)
        if g.op=='SourceI':
            active=mask(2)
            return [s*rr(0,1) if k&active else s for k,s in enumerate(state)]
        if g.op=='CX':
            c,t=map(mask,g.wires)
            return [state[k^t] if k&c else state[k] for k in range(len(state))]
        assert g.op=='G'
        t=mask(g.wires[0])
        return [(aa*s+(pp if k&t else -pp)*state[k^t]) for k,s in enumerate(state)]
    def walk(state,segments):
        weights=[]
        for g in segments:
            after=apply(state,g)
            z=sum((rr(s.real,-s.imag)*t for s,t in zip(state,after)),zero())
            state=after
            weights.append((z.real,z.imag))
        return state,weights
    context,segments=words(order)
    run=sum(segments,())
    ini=tensor_v([rr(1)],4)
    reflected,_=walk(ini,run)
    c=(pp**3)**(2+(order==(3,2)))
    u=c*c
    B=[(s-c*t)/xp.sqrt(1-u) for s,t in zip(reflected,ini)]
    P2,rows0=walk(ini,run)
    B2,rows1=walk(B,run)
    detector=measure_word()
    d0,rowsd0=walk(tensor_v(P2,2),detector)
    d1,rowsd1=walk(tensor_v(B2,2),detector)
    # (c+i s)^16 is the actually compiled common on-predicate rotation.
    z=rr(aa,pp)**16
    eta=z.imag**2
    for ending,yes in ((d0,u),(d1,1-u)):
        masses=[sum((abs(w)**2 for w in ending[b::4]),xp.mpf(0)) for b in range(4)]
        expected=(1-eta,eta*(1-yes),eta*yes,0)
        for x,y in zip(masses,expected):
            if hasattr(x,'a'):
                assert (x-y).a<=0<=(x-y).b
            else:
                assert abs(x-y)<1e-10
    return (u,eta,(rows0,rows1),(rowsd0,rowsd1),tuple(map(len,segments)))


def owner_check(order):
    v,born=raw_bank(order)
    context,segments=words(order)
    gates=sum(segments,())
    ops={g:np.array(native.gate_matrix(context,g,max_qubits=6),float) for g in set(gates)}
    matrix=np.eye(64)
    for g in gates:
        matrix=product(ops[g],matrix)
    active=[2,4] if order==(2,3) else [2,3,4]
    diagonal=np.diag([(-1)**sum((j>>(5-q))&1 for q in active) for j in range(64)])
    np.testing.assert_allclose(matrix,diagonal,atol=1e-12)
    first=product(matrix,born)
    for state in (born,first):
        dark=product(v,state)[3::4]
        np.testing.assert_allclose(dark,0,atol=1e-12)


def certified():
    import argparse
    import mpmath as mp
    options=argparse.ArgumentParser(description=__doc__)
    options.add_argument('--rows',action='store_true',help='print Bell-RIGHT overlap coefficients and work of every addressed primitive')
    args=options.parse_args()
    mp.iv.dps=80
    iv=mp.iv
    zero=iv.mpf(0)
    def root(value):
        # True radicand is a squared distance; keep any rigorously possible nonnegative part.
        if value.b < 0:
            raise ArithmeticError(value)
        return iv.sqrt(iv.mpf([max(zero,value.a),value.b]))
    def work(rows,x):
        return sum((root(1-r**2-x*i**2) for r,i in rows),zero)
    def h(q):
        return -(q*iv.ln(q)+(1-q)*iv.ln(1-q))/iv.ln((1+iv.sqrt(5))/2)
    def disturbance(x):
        return x*root(1-x)+(1-x)*root(x)
    def measured(pi,eta):
        first=eta*pi
        return disturbance(first)+(1-first)*disturbance(eta*(1-pi)/(1-first))
    def mid(x): return float(x.mid)
    def contained(x,lo,hi):
        assert lo<x.a<=x.b<hi,(x,lo,hi)
    stats=[]
    for order in ((2,3),(3,2)):
        owner_check(order)
        u,eta,R,P,sizes=simulation(order,iv)
        context,segments=words(order)
        native_R=sum(segments,())
        native_P=measure_word()
        assert sizes==(8,8,22) and len(native_P)==400
        ro=[work(s,zero) for s in R]
        po=[work(s,zero) for s in P]
        read=(measured(u,eta)+measured(1-u,eta))/eta
        info=2*h(u)
        extras=2*h(eta)/eta
        return_raw=sum(ro)
        total=return_raw+sum(po)/eta
        print(order,'u %.12f eta %.12f'%(mid(u),mid(eta)))
        print('R by sector and forward/Z/inverse',[[round(mid(work(s[a:b],zero)),9)
              for a,b in ((0,8),(8,16),(16,38))] for s in R])
        print('detector 400-gate attempt by sector',*[round(mid(a),9) for a in po])
        print('total gates %0.10f, measured endpoint disturbance %0.10f'%(mid(total),mid(read)))
        print('full record info',mid(info+extras),'endpoints-only',mid(info))
        print('counts R',dict(Counter(q.op for q in native_R)),'detector',dict(Counter(q.op for q in native_P)))
        if args.rows:
            for name,stages,weights in [('R',native_R,R),('P',native_P,P)]:
                print('module,stage,gate,wires,r_P,i_P,r_B,i_B,d_P,d_B')
                for j,g in enumerate(stages):
                    p_row,b_row=(w[j] for w in weights)
                    print(name,j+1,g.op,g.wires,*[f'{mid(x):.12f}' for x in
                          (*p_row,*b_row,work([p_row],zero),work([b_row],zero))],sep=',')
        roots=2+(order==(3,2))
        delta=((iv.sqrt(5)-1)/2)**3
        fine_retry=((delta**4+(1-delta**2)**2)**roots-u**2)/(1-u)
        print('resolved-WORK retry',mid(fine_retry),'mean R',2**roots)
        stats.append((R,P,eta,return_raw,total,read,info+extras))
    delta=[stats[1][i]-stats[0][i] for i in range(3,7)]
    for name,x in zip(('R','R+P','read','info'),delta): print('secant',name,'%.10f'%mid(x))
    contained(delta[0],6.105739,6.105741)
    contained(delta[1],37.41272,37.41275)
    contained(delta[3],-.080474,-.080471)
    # Monotone square roots at the two ends of each cell bracket every polarization.
    def values(j):
        x=iv.mpf(j)/16
        out=[]
        for R,P,eta,*_ in stats:
            inner=sum(work(seq,x) for seq in R)
            out.append((inner,inner+sum(work(seq,x) for seq in P)/eta))
        return out
    previous=values(0)
    lower=[1e10,1e10]
    upper=[-1e10,-1e10]
    for j in range(1,17):
        current=values(j)
        for t in range(2):
            lo=current[1][t]-previous[0][t]
            hi=previous[1][t]-current[0][t]
            assert lo.a>0, (t,j,lo)
            lower[t]=min(lower[t],float(lo.a))
            upper[t]=max(upper[t],float(hi.b))
        previous=current
    print('all polarizations enclosed, R / R+P',list(zip(lower,upper)))


if __name__=='__main__':
    certified()
