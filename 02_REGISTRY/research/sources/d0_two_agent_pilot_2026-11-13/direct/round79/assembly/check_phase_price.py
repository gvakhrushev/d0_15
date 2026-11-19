"""Same two actual readouts, opposite full Book03 price secants after a paid sign."""
from fractions import Fraction as F
from math import sqrt
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[4]/"d0_native_execution_domain_2026-10-24"))
import native_execution as ne


def word(k, target, blocks=1, with_overlaps=False):
    g=ne.Gate
    port,x,y=2,3,4
    def sign(j):
        route=(g("CX",(port,j)),g("CX",(j,port)),g("CX",(port,j)))
        return (*route,g("SourceI",(port,0,1)),g("SourceI",(port,0,1)),*route)
    equal=(g("CX",(x,y)),)*2
    rotations=(g("G",(x,)),g("G",(y,)))
    assert 0 <= k <= blocks
    stages=rotations*k+equal*(blocks-k)+sign(y)+sign(target)
    ex=ne.Execution(5,(),(),stages,profile=ne.G_CX_SOURCE_I,
                    source_port=port,source_spin=(0,1),report_bits=(x,y))
    ne.execution_from_json(ne.canonical_json(ex),max_qubits=5,max_expanded_stages=len(stages))
    p=(sqrt(5)-1)/2
    v=np.array([sqrt(p),p])
    birth=np.eye(4)
    for _ in (port,x,y):
        birth=np.kron(birth,v[:,None])
    out=birth.copy()
    overlaps=[]
    for op in stages:
        previous=out
        out=np.array(ne.gate_matrix(ex,op,max_qubits=5,max_expanded_stages=len(stages)),dtype=float)@out
        if with_overlaps:
            overlaps.append(abs(previous[:,0]@out[:,0]))
    cq=[]
    for a in range(4):
        blocks=out.reshape(4,2,4,4)[:,:,a,:]
        weight=blocks.transpose(2,0,1).reshape(4,-1)
        cq.append(weight@weight.T)
    result=(birth.T@out,cq,len(stages))
    return (*result,overlaps) if with_overlaps else result


def main():
    p=(sqrt(5)-1)/2
    cp=((1.,sqrt(p)), (p**3,sqrt(p)*(1-4*p*p)))
    records={}
    for side,target in enumerate((4,3)):
        for k in (0,1):
            cold,cq,n=word(k,target)
            assert n==18 and np.allclose(cold,cp[side][k]**2*np.eye(4),atol=1e-13)
            assert np.allclose(sum(cq),np.eye(4))
            if not side:
                records[k]=cq
            else:
                assert np.allclose(records[k],cq,atol=1e-13)
    # Bound the complete heat on two different initial gates of dimension D_f each.
    # D_clk >= 4^13 D_f, ||U-V||_1 <= 2D_f per gate.
    p0,p1=F(61803398874,10**11),F(61803398876,10**11)
    assert p0*p0+p0 < 1 < p1*p1+p1
    heat=F(24,359*4**13)
    rz=F(4,2**20)
    positive=rz*(1-p1*p1)-heat
    negative=rz*(p0**2*(4*p0**2-1)**4-p1**12)-heat
    assert positive>F(23,10**7) and negative>F(9,10**8)
    print("full price plus secant >",float(positive))
    print("full price minus secant <",-float(negative))
    print("all four old probabilities agree at each endpoint, complete spectral secants have opposite signs")


if __name__=="__main__":
    main()
