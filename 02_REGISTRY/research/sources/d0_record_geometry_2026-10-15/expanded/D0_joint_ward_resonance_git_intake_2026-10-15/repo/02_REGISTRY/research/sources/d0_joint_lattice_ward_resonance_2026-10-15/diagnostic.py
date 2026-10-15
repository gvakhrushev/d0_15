#!/usr/bin/env python3
"""Independent numerical tests, explicitly NOT interval/theorem receipts."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import argparse,json,sys
import numpy as np
import sympy as s
import linear as L
HERE=Path(__file__).resolve().parent

def expansion_checks():
    data=L.resonance();P=np.array(data['P'].tolist(),complex);Y=np.array(data['Y'].tolist(),complex);N=np.eye(34)-P
    z=s.symbols('z0:4',nonzero=True);fn=s.lambdify(z,L.joint(z),'numpy');out=[]
    for name,k,power,target in [
        ('transverse_to_resonance',[0,1,0,0],1,np.diag([2,-2])/7),
        ('tangent_noncharacteristic',[0,1,-1,0],2,np.array([[-3,-1],[-1,5]])/7),
    ]:
        previous=None
        for h in [1e-2,5e-3,2.5e-3]:
            zz=np.array([1,1j,1j,1])*np.exp(1j*h*np.array(k));J=fn(*zz)
            RN=N@np.linalg.inv(N@J@N+P)@N
            eff=7*Y.conj().T@(J-J@RN@J)@Y
            err=float(np.linalg.norm(eff/h**power-target,2))
            invscaled=float(h**power*np.linalg.norm(np.linalg.inv(eff),2))
            print(name,h,err,invscaled,flush=True)
            if previous is not None and not err<previous*.7:raise AssertionError('wrong remainder scaling')
            previous=err
            out.append(dict(name=name,h=h,scaled_error=err,scaled_inverse=invscaled))
    return out

def autodiff_checks():
    sys.path.insert(0,str(L.UPSTREAM.parent))
    import full4d_diagnostic as original
    import jax
    jax.config.update('jax_enable_x64',True)
    import jax.numpy as j
    a=np.zeros(6144);E=np.tile(np.eye(4),(4,4,4,4,1,1));grid=np.indices((4,4,4,4))
    fun=jax.jit(lambda de:jax.jvp(lambda ee:original.grad(j.array(a),ee),(j.array(E),),(de,))[1])
    rng=np.random.default_rng(20261015);out=[]
    for modes in [(0,1,1,0),(1,2,3,2)]:
        phase=(1j)**sum(k*grid[r] for r,k in enumerate(modes));q=rng.normal(size=10)+1j*rng.normal(size=10)
        field=np.real(phase[...,None]*q);V=np.zeros_like(E)
        for i,(r,t) in enumerate(L.PACK):V[...,r,t]=V[...,t,r]=field[...,i]
        de=np.array(L.eta.tolist(),float)@V/2
        actual=np.array(fun(j.array(de))).reshape(4,4,4,4,24)
        C=np.array(L.mixed([s.I**k for k in modes]).tolist(),complex)
        expected=np.real(phase[...,None]*(C@q))
        err=float(np.max(abs(actual-expected)))
        if err>1e-11:raise AssertionError('literal full-action mixed derivative disagrees')
        out.append({'modes':modes,'complete_rows':6144,'max_error':err})
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--autodiff',action='store_true');args=ap.parse_args()
    out={'status':'FLOATING_POINT_DIAGNOSTICS_NOT_PROOF','expansion':expansion_checks()}
    if args.autodiff:out['independent_full_action_autodiff']=autodiff_checks()
    (HERE/'diagnostic_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
