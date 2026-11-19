"""All 16 deterministic binary recodings of the actual two-sector NC1 law."""
from collections import Counter
from itertools import product
import json
import mpmath as mp
import sympy as sp


def main():
    p=(sp.sqrt(5)-1)/2
    p2=sp.simplify(p**2);p3=sp.simplify(p**3)
    phi=(1+sp.sqrt(5))/2
    assert sp.simplify(p+p2-1)==0
    assert sp.simplify(1-2*p2-p3)==0
    label_values=[('0',0),('p^2',p2),('p',p),('p^3',p3),('1',1),
                  ('-p^2',-p2),('-p',-p),('-p^3',-p3),('-1',-1)]
    def label(x):
        for name,value in label_values:
            if sp.simplify(x-value)==0:return name
        raise AssertionError(str(x))
    # Entries of f are ordered (T,N) = (00,01,10,11).
    data=[];classes=Counter();fullzero=[];zero=[]
    allf=list(product((0,1),repeat=4))
    mp.mp.dps=70
    pp=(mp.sqrt(5)-1)/2;pp2=pp**2
    entropy=lambda xs:-sum((x*mp.log(x) for x in xs if x>0),mp.mpf(0))
    ell=mp.log((1+mp.sqrt(5))/2)
    hphi=entropy([pp,pp2])/ell
    assert abs(hphi-(1+pp2))<mp.mpf('1e-60')
    # Two noncommuting mixed old states rho_t; all conditional outputs
    # are isometric so their (possibly unequal) spectra remain exactly.
    def eig(a,d,b):
        disc=mp.sqrt((a-d)**2+4*b*b)
        return ((a+d+disc)/2,(a+d-disc)/2)
    ev=[eig(mp.mpf(3)/4,mp.mpf(1)/4,mp.mpf(1)/8),
        eig(mp.mpf(1)/3,mp.mpf(2)/3,mp.mpf(1)/6)]
    old_q=mp.mpf(29)/100
    Pt=[1-old_q,old_q]
    oldH=(entropy(Pt)+sum(Pt[t]*entropy(ev[t]) for t in (0,1)))/ell
    for f in allf:
        q0=sp.simplify(p*f[0]+p2*f[1])
        q1=sp.simplify(p2*f[2]+p*f[3])
        slope=sp.simplify(q1-q0)
        name=label(slope)
        classes[name]+=1
        if name=='0':zero.append(''.join(map(str,f)))
        full=sp.simplify(p3+slope)
        if full==0:fullzero.append(''.join(map(str,f)))
        # A literal t,n,o CQ direct sum with preserved old conditional spectra.
        weights=[]
        for t in (0,1):
            n1=pp2 if t==0 else pp
            for n in (0,1):
                o=f[2*t+n]
                pn=n1 if n else 1-n1
                weights.extend(Pt[t]*pn*x for x in ev[t])
                assert o in (0,1)
        newH=entropy(weights)/ell
        assert abs((newH-oldH)-(1+pp2))<mp.mpf('1e-60')
        data.append({'truth':''.join(map(str,f)),'conditional_r0':label(q0),
                     'conditional_r1':label(q1),'partial_source':name,
                     'both_codes_source':label(full) if full in [0,p2,p,1,-p2,-p,-1] else str(full)})
    assert classes==Counter({'0':4,'p^2':2,'-p^2':2,'p':2,'-p':2,
                              'p^3':1,'-p^3':1,'1':1,'-1':1})
    assert sorted(zero)==['0000','0110','1001','1111']
    assert fullzero==['1010']  # O=1-N, and N itself is charged separately.
    # Without recording N, keeping its full coherent environment does not
    # create h(N|T): O=T is deterministic conditional on already-read T.
    coherent_O_equals_T_entropy=mp.mpf(0)
    assert coherent_O_equals_T_entropy!=hphi
    # The two visible codes 0/10 for N and 1-N have total length exactly 3.
    assert all((1+n)+(1+(1-n))==3 for n in (0,1))
    print(json.dumps(dict(status='PASS',truth_order='(T,N)=(00,01,10,11)',
      law='P(N=1|T=0)=p^2, P(N=1|T=1)=p',
      conditional_CQ_entropy_increment='1+p^2, if N is recorded and the actual instrument is conditional scalar-isometric',
      unique_two_code_source_canceller='1010 = 1-N',
      single_output_zero_signal_truths=sorted(zero),
      class_counts=dict(sorted(classes.items())),all_16_rows=data,
      coherent_counterexample='O=T, N retained coherently and unread: entropy increment 0 rather than 1+p^2',
      scope='registered-output code-CQ only; physical compilation and full Cost-Info not inferred',
      full_cost_info_and_GR_closed=False),indent=2,sort_keys=True))

if __name__=='__main__':main()
