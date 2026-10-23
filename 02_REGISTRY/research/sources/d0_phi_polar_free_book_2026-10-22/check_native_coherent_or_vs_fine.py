#!/usr/bin/env python3
"""OR-only coherent work versus independently measured Golden subflags.
Native N1 p, zeta, x/y ratios and original strict h0 42-root intervals.
Mathematical two-factor dilation, NOT mandatory physical M1/G0 readout.
"""
from decimal import Decimal
from mpmath import iv
iv.dps=85
p=(iv.sqrt(5)-1)/2; z=iv.mpf(2)**-20; lp=iv.log(1/p)
checks=[]
def check(label,pred):
    if not bool(pred): raise AssertionError(label)
    checks.append(label)
def box(x,e='1e-12'):
    q=Decimal(x);d=Decimal(e)
    return iv.mpf([str(q-d),str(q+d)])
def calc(x,y):
    E=p*p*(1+x);L=4*E*(1-E)
    b=p-p*p*y;B=4*b*b*(1-b*b);A=L+(1-L)*B
    By=-8*p*p*b*(1-2*b*b);Ay=(1-L)*By
    Lx=4*p*p*(1-2*E);Ax=Lx*(1-B)
    u=z*A;v=z*B;r=u+v-u*v
    ux=z*Ax;uy=z*Ay;vy=z*By
    rx=ux*(1-v);ry=uy*(1-v)+vy*(1-u)
    hp=lambda t:iv.log((1-t)/t)/lp
    h=lambda t:-(t*iv.log(t)+(1-t)*iv.log(1-t))/lp
    MI=h(u)+h(v)-h(r)
    MIx=hp(u)*ux-hp(r)*rx
    MIy=hp(u)*uy+hp(v)*vy-hp(r)*ry
    coarse=1+r-h(r)
    fine=2+u+v-h(u)-h(v)
    coarsex=(1-hp(r))*rx
    coarsey=(1-hp(r))*ry
    finex=(1-hp(u))*ux
    finey=(1-hp(u))*uy+(1-hp(v))*vy
    return dict(u=u,v=v,r=r,MI=MI,MIx=MIx,MIy=MIy,
                coarse=coarse,fine=fine,
                coarsex=coarsex,coarsey=coarsey,
                finex=finex,finey=finey,
                lam_c=coarsey/coarsex,lam_f=finey/finex,
                delta=finey/finex-coarsey/coarsex,
                extra_cost=1+u*v)
states=[('0','0'),
        ('0.001370578581747874','-0.000016169093857131'),
        ('-0.000127665084908232','0.000005454102084650')]
for i,(x,y) in enumerate(states):
    d=calc(box(x),box(y))
    check(str(i)+' original positive rates',
          d['u'].a>0 and d['v'].a>0 and d['r'].a>0)
    check(str(i)+' original coarse OR larger than each separate event',
          d['r'].a>d['u'].b and d['r'].a>d['v'].b)
    check(str(i)+' exactly positive conditional hidden flag Info',d['MI'].a>0)
    check(str(i)+' true two-terminal extra output charge >1',d['extra_cost'].a>1)
    check(str(i)+' offshell geometric hidden Info jet positive',d['MIx'].a>0)
    check(str(i)+' offshell matter hidden Info jet negative',d['MIy'].b<0)
    check(str(i)+' true fine source ratio strictly below OR ratio',d['delta'].b<0)
    check(str(i)+' ratio shift lies strictly between -.10 and -.08',
          d['delta'].a>iv.mpf('-.10') and d['delta'].b<iv.mpf('-.08'))
    check(str(i)+' hidden fine information source nonzero',
          d['MIx'].a>0 and d['MIy'].b<0)
    if i==0:
        check('null: original lambda -23.416 reproduced',
              d['lam_c'].a>iv.mpf(-23.42) and d['lam_c'].b<iv.mpf(-23.41))
        check('null: fine report different lambda approx -23.506',
              d['lam_f'].a>iv.mpf(-23.52) and d['lam_f'].b<iv.mpf(-23.49))
    else:
        check(str(i)+' original full42 h0 click stays in strict domain',
              d['r'].a>iv.mpf('1.8e-6') and d['r'].b<iv.mpf('1.9e-6'))
    print('cell',i,'OR',d['lam_c'],'FINE',d['lam_f'],
          'strict difference',d['delta'])
    print('conditional hidden Info',d['MI'],
          'dI/dx',d['MIx'],'dI/dy',d['MIy'])
print('PASS',len(checks),'original φ two factor OR/coherent vs fine-source controls')
print('Physical common native 42 writer/Book P,heat,Info and GR remain OPEN.')
