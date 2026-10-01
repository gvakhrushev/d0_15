#!/usr/bin/env python3
"""Literal curved-branch Gram response at the same fixed metric on five meshes.

Optional numerical control for A4D_WARPED_DESIGNATED_NORMAL_RESCUE.md.
The analytic theorem does not infer existence or a continuum rate from this
finite grid sequence. No branch-dependent metric source is assigned.
"""
import sys
import json
import numpy as np
from scipy.linalg import solve,logm
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from a4d_designated_curved_hessian_probe import *
SYM=[(a,b) for a in range(4) for b in range(a,4)]

def metric_readout(model,k):
    out=np.zeros((model.n,10))
    for x in range(model.n):
        solder=model.solder[x]
        q=solder.T@ETA@solder
        for face,(a,b) in enumerate(PAIRS):
            u,v=[j for j in range(4) if j not in (a,b)]
            loc=[(x,a),((x+(a==1))%model.n,b),((x+(b==1))%model.n,a),(x,b)]
            fac=[k[xx,r] if j<2 else linv(k[xx,r]) for j,(xx,r) in enumerate(loc)]
            plaquette=matprod(fac)
            for j,(r,s) in enumerate(SYM):
                dq=np.zeros((4,4));dq[r,s]=dq[s,r]=1
                ds=solder@np.linalg.solve(q,dq)/2
                da=orient(a,b)*(wedge(ds[:,u],solder[:,v])+wedge(solder[:,u],ds[:,v]))@G2@STAR
                weight=np.zeros((4,4))
                for value,(aa,bb) in zip(da,PAIRS):
                    weight[aa,bb]+=value*SIG[bb]/2;weight[bb,aa]-=value*SIG[aa]/2
                out[x,j]+=np.sum(weight*plaquette)
    return out

def run(n,amp):
    k=Model(n,0).identity()
    for amplitude in np.linspace(0,amp,5)[1:]:
        model=Model(n,float(amplitude))
        for _ in range(12):
            _,g,H=model.assemble(k)
            if max(abs(g))<5e-14:break
            delta=solve(H.real,-g,assume_a='sym')
            k=model.update(k,delta)
        else:raise RuntimeError('Newton failure')
    _,g,H=model.assemble(k)
    eq=metric_readout(model,k)
    # Direct Gram Euler convention: r=G_standard/2, with raised output
    # and the factor two on off-diagonal slots. The exact new owner checks
    # all ten normal-Hessian columns independently.
    target=4*np.pi*np.pi*amp*np.array([-1,0,0,0,0,0,0,.5,0,.5])
    normed=n*n*eq[0]
    data={'L':n,'epsilon':amp,'residual':float(max(abs(g))),
          'normalized_response':normed.tolist(),'target':target.tolist(),
          'difference':float(max(abs(normed-target)))}
    print(json.dumps(data),flush=True)
    return data
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--periods',type=int,nargs='+',default=[8,12,16,24,32])
    parser.add_argument('--amplitude',type=float,default=0.02)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report={
        'metric':'diag(1,-1,-f(x1)^2,-f(x1)^2), f=1+epsilon*(1-cos(2*pi*x1))',
        'fixed_epsilon':args.amplitude,
        'readout':'literal Gram partial at the metric-normal point x1=0',
        'target_convention':'G_standard/2, owner r=-K_Schur[J]',
        'runs':[run(n,args.amplitude) for n in args.periods],
        'status':'NUMERICAL_CONTROLS; exact existence for sufficiently large L is proved separately',
        'nonclaims':['no validated finite-L Newton roots',
                     'no exact prescribed joint metric source',
                     'no unrestricted transverse branch theorem']}
    if args.output:
        args.output.write_text(json.dumps(report,indent=2)+'\n')
