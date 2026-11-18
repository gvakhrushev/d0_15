"""Check the restricted fixed-core SAM stationary reduction."""
from pathlib import Path
import hashlib
import json
import numpy as np
import sympy as S

HERE=Path(__file__).resolve().parent
checks=[]
def need(ok,name,kind='exact'):
    if not bool(ok): raise AssertionError(name)
    checks.append({'name':name,'kind':kind})
def eq(x,y,name): need(S.simplify(x-y)==0,name)
u,d,m,v,w0,w1=S.symbols('u d m v w0 w1',positive=True)
b0,b1=u*m+d,u*m-d
nu=w0*b0*b0+w1*b1*b1
L=w0*b0+w1*b1
M=S.Matrix([[nu,u*S.sqrt(v)*L],[u*S.sqrt(v)*L,u*u*(w0+w1)*v]])
eq(M.det(),4*w0*w1*u*u*d*d*v,'actual SAM block determinant')
eq(S.trace(M),nu+u*u*(w0+w1)*v,'actual SAM block trace')
eq((w0+w1)*nu-4*w0*w1*d*d,L*L,'variance derivative positive square')
tv=nu+u*u*(w0+w1)*v
dv=4*w0*w1*u*u*d*d*v
# Implicit differentiation lambda^2-T lambda+D=0 at lambda=nu,v=0.
eq(S.diff(tv,v)-S.diff(dv,v)/nu,u*u*L*L/nu,'optimized variance derivative')
eq(w0*(u*u*(m*m+v)+2*u*d*m+d*d)+
   w1*(u*u*(m*m+v)-2*u*d*m+d*d),tv,'full cold trace retains second moment')

pn=(np.sqrt(5)-1)/2
un,dn=(np.sqrt(pn)+pn)/2,(np.sqrt(pn)-pn)/2
sn=pn**3
coeffs=[(0.0004056225182407943,0.000004198575632191515),
        (0.0004361385286587986,0.000004198575632191515)]
# These printed coefficients are used ONLY in numerical diagnostics.
# Their exact origin and positivity are checked in check_stationary_backward.py.
rng=np.random.default_rng(33420261113)
diagnostics=[]
for i,(h0,h1) in enumerate(coeffs):
    al,be=pn*h0,pn*pn*h1
    for idx,spread in enumerate([0.,0.01,0.08]):
        cs=0.75+spread*np.array([-1.,-.4,.3,1.])
        psi=rng.normal(size=4)+1j*rng.normal(size=4)
        psi/=np.linalg.norm(psi)
        mean=float(np.vdot(psi,cs*psi).real)
        variance=float(np.vdot(psi,cs*cs*psi).real-mean*mean)
        variance=max(variance,0.)
        q=(1-sn*mean)/2
        w0n,w1n=al/(1-q),be/q
        f0,f1=(un*cs+dn)*psi,(un*cs-dn)*psi
        mat=w0n*np.outer(f0,f0.conj())+w1n*np.outer(f1,f1.conj())
        vals,vecs=np.linalg.eigh(mat)
        chi=vecs[:,-1]
        n=w0n*(un*mean+dn)**2+w1n*(un*mean-dn)**2
        tr=n+un*un*(w0n+w1n)*variance
        det=4*w0n*w1n*un*un*dn*dn*variance
        lam=(tr+np.sqrt(tr*tr-4*det))/2
        prefix=f'word {i}, spread {spread}'
        need(abs(lam-vals[-1])<1e-17,prefix+': full complex SAM spectrum','numerical')
        need(np.linalg.norm(mat@chi-lam*chi)<1e-17,prefix+': stationary backward row','numerical')
        need(-1e-17<lam-n<un*un*(w0n+w1n)*variance+1e-17,
             prefix+': quadratic-spread value bound','numerical')
        zn=.6
        price_gain=4*np.log((1-zn+zn*lam)/(1-zn+zn*n))
        bound=4*zn/(1-zn)*un*un*(w0n+w1n)*variance
        need(-1e-14<=price_gain<=bound+1e-14,prefix+': marked price improvement bound','numerical')
        if spread:
            # Wrong whole-bank norm substitution would replace these squared
            # cold norms by the full effects. They disagree on this fixed core.
            need(abs(np.vdot(f0,f0).real-(1-q))>0.01,
                 prefix+': cold SAM map is not full branch isometry','numerical')
        diagnostics.append({'word':i,'spread':spread,'variance':variance,
                            'price_improvement':price_gain,'bound':bound})

out={'status':'PASS','exact_checks':sum(x['kind']=='exact' for x in checks),
     'numerical_diagnostics':sum(x['kind']=='numerical' for x in checks),
     'checks':checks,'diagnostics':diagnostics,
     'proof_sha256':hashlib.sha256((HERE/'SAM_BACKWARD_RU.md').read_bytes()).hexdigest(),
     'baseline':'dc411daf01f697ec85dd22f28bfe124171796645',
     'scope':{'fixed_core_mathematical_SAM_stationarity':True,
              'full_native_fibre_admission':False,'old_history_replaced_by_identity':False,
              'Cost_Info_binding':False,'GR_closed':False}}
(HERE/'SAM_CHECK.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','exact_checks','numerical_diagnostics']},ensure_ascii=False))
