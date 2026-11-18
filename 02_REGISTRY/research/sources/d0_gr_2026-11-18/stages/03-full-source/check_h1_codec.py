"""Exact right derivative at q=p^2 of optimal complete-record binary Huffman length."""
import heapq
import json
from math import comb,sqrt
from pathlib import Path

# c+d*p with p^2=1-p.
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
def mul(x,y):
    a,b=x;c,d=y
    return (a*c+b*d,a*d+b*c-b*d)
def power(x,n):
    out=(1,0)
    for i in range(n): out=mul(out,x)
    return out
def sg(v): return (v>0)-(v<0)
def sign(x):
    c,d=x; a=2*c-d
    if sg(a)*sg(d)>=0:return sg(a) or sg(d)
    delta=a*a-5*d*d
    return sg(a)*sg(delta)
def value(x):
    from decimal import Decimal,getcontext
    getcontext().prec=80
    return float(Decimal(x[0])+Decimal(x[1])*(Decimal(5).sqrt()-1)/2)
class Node:
    __slots__=('w','v')
    def __init__(self,w,v):self.w=w;self.v=v
    def __lt__(self,o):
        cmp=sign(sub(self.w,o.w))
        return cmp<0 if cmp else sign(sub(self.v,o.v))<0

p=(0,1); s=power(p,6); dim=(1,0)
def slope(m,left_at_half=False):
    heap=[]
    for k in range(m+1):
        nu=mul(power(s,k),power(sub(dim,s),m-k))
        if left_at_half:
            # Sort mass + t*direction with t=1/2-q down to zero. Multiplying
            # both zeroth-order masses by two preserves their Huffman order.
            n0=Node(nu,nu)
            n1=Node(nu,sub((0,0),nu))
        else:
            n0=Node(mul(p,nu),sub((0,0),nu))
            n1=Node(mul(power(p,2),nu),nu)
        heap.extend([n0,n1]*comb(m,k))
    heapq.heapify(heap)
    deriv=(0,0)
    while len(heap)>1:
        a=heapq.heappop(heap);b=heapq.heappop(heap)
        n=Node(add(a.w,b.w),add(a.v,b.v))
        deriv=add(deriv,n.v)
        heapq.heappush(heap,n)
    assert heap[0].w==((2,0) if left_at_half else (1,0)) and heap[0].v==(0,0)
    return sub((0,0),deriv) if left_at_half else deriv

rows=[]
for m in range(1,13):
    v=slope(m); w=slope(m,True); d=sub(mul((2*m,0),s),v)
    rows.append({'m':m,'max_optimal_joint_secant_q_ge_p2_exact':v,'min_optimal_joint_secant_q_le_half_exact':w,'min_optimal_joint_secant':value(w),'max_optimal_joint_secant':value(v),'minimum_margin_exact':d,'minimum_margin':value(d),'positive':sign(d)>0})
first=next(z for z in rows if z['positive'])
print(json.dumps({'status':'PASS','p_basis':'a+b*p; p=(sqrt(5)-1)/2','first_m_in_exact_exhaustion':first['m'],'rows':rows},indent=2))
