#!/usr/bin/env python3
"""Owned native-phase interval recurrence, with exact power-of-two shifts.

For every signed integer x, x//2^bits == x>>bits. This preserves every
outward rounding endpoint of native_phase._rotation_intervals, while avoiding
general large-integer division by the same power of two in each product.
"""
from math import isqrt

def rotation_intervals(multiplier,bits):
    assert type(multiplier) is int and multiplier>0 and type(bits) is int and bits>=16
    scale=1<<bits
    def add(a,b):return a[0]+b[0],a[1]+b[1]
    def neg(a):return -a[1],-a[0]
    def mul(a,b):
        v=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
        return min(v)>>bits,-((-max(v))>>bits)
    def unit(a):
        low,high=max(-scale,a[0]),min(scale,a[1]);assert low<=high
        return low,high
    def cmul(a,b):
        return unit(add(mul(a[0],b[0]),neg(mul(a[1],b[1])))),unit(add(mul(a[1],b[0]),mul(a[0],b[1])))
    sqrt5=isqrt(5*scale*scale)
    p=((sqrt5-scale)//2,-((-(sqrt5+1-scale))//2))
    a=(isqrt(p[0]*scale),isqrt(p[1]*scale)+1)
    result=((scale,scale),(0,0));base=(a,p);exponent=multiplier
    while exponent:
        if exponent&1:result=cmul(result,base)
        exponent>>=1
        if exponent:base=cmul(base,base)
    return scale,result[0],result[1]
