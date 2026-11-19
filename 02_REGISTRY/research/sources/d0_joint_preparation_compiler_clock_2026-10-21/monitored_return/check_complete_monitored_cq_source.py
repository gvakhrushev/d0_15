#!/usr/bin/env python3
"""Actual native monitored return: full CQ source, no-floor tails, interval sign.

Consumes the 4D monodromy already derived in the original sixteen-stage
clock/work owner. Does not admit a new gate, select Book Info, or claim GR.
Only Python standard library and numpy are required. Never edits repo inputs.
"""
from __future__ import annotations
import json
import math
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path
import numpy as np

CHECKS=[]
def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    CHECKS.append(name)

PHI=(1+math.sqrt(5))/2
ELL=math.log(PHI)
C_NATIVE=math.sqrt(5)-2
RHO=.75
A=RHO**-.5
THETA=RHO**.125
RR=THETA**2
UU=1+math.log(RHO)
VV=-math.log(RR)

def entropy_tail(N):
    return A*A/ELL*RR**N*((math.log(RHO)+VV*N)/(1-RR)
                                +VV*RR/(1-RR)**2)

def source_tail(N):
    T1=(N+1)/(1-RR)+RR/(1-RR)**2
    T2=N*(N+1)/(1-RR)+2*(N+1)*RR/(1-RR)**2+2*RR*RR/(1-RR)**3
    return 2*A**3/(ELL*THETA)*RR**N*(UU*(T1+N)+VV*(T2+N*N))

def matrices(c):
    k=math.sqrt(1-c*c)
    M=np.array([[c,0,-k,0],[0,c,0,-k],[0,-k,0,-c],[-k,0,-c,0.]])
    dM=np.array([[1,0,c/k,0],[0,1,0,c/k],[0,c/k,0,-1],[c/k,0,-1,0.]])
    return M,dM

Q=np.diag([0.,1.,1.,1.]);P=np.eye(4)-Q
J=np.array([[0.,-1,0,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]])

def price_and_source(M,dM,N,C=None,dC=None,w=0.,dw=0.):
    V=Q@M;dV=Q@dM
    state=np.array([1.,0,0,0]);dstate=np.zeros(4)
    power=np.eye(4);dpower=np.zeros((4,4))
    H=dH=prob=mean=0.;probs=[]
    for n in range(1,N+1):
        amp=(M@state)[0];damp=(dM@state+M@dstate)[0]
        pn=float(amp*amp);dpn=float(2*amp*damp)
        if pn>0:
            H-=pn*math.log(pn)/ELL
            dH-=dpn*(math.log(pn)+1)/ELL
        probs.append(pn);prob+=pn;mean+=n*pn
        dstate,state=dV@state+V@dstate,V@state
        dpower,power=dV@power+V@dpower,V@power
    survival=float(state@state);dsurvival=float(2*state@dstate)
    if survival>0:
        H-=survival*math.log(survival)/ELL
        dH-=dsurvival*(math.log(survival)+1)/ELL
    R=power@power.T;dR=dpower@power.T+power@dpower.T
    cost=dcost=0.
    if C is not None:
        if dC is None:dC=np.zeros((4,4))
        cost=float(np.trace(C@(np.eye(4)-R)))+w*survival
        dcost=float(np.trace(dC@(np.eye(4)-R)-C@dR))+dw*survival+w*dsurvival
    return dict(H=H,dH=dH,prob=prob,mean=mean,survival=survival,
                dsurvival=dsurvival,probs=probs,S=cost-H,dS=dcost-dH,
                cost=cost,dcost=dcost)

# Directed decimal interval arithmetic. Elementary ln/sqrt results are
# bracketed by one adjacent Decimal on each side, in addition to directed
# elementary arithmetic. With 256 significant digits the final enclosure
# includes recurrence and logarithm roundoff, not only the analytic tail.
PREC=256
class I:
    def __init__(self,x,y=None):
        if isinstance(x,I):self.lo,self.hi=x.lo,x.hi;return
        self.lo=Decimal(x);self.hi=Decimal(x if y is None else y)
    @staticmethod
    def directed(fn,rounding):
        with localcontext() as ctx:
            ctx.prec=PREC;ctx.rounding=rounding
            return fn()
    def __add__(self,o):
        o=I(o);return I(self.directed(lambda:self.lo+o.lo,ROUND_FLOOR),
                       self.directed(lambda:self.hi+o.hi,ROUND_CEILING))
    __radd__=__add__
    def __neg__(self):return I(self.hi.copy_negate(),self.lo.copy_negate())
    def __sub__(self,o):return self+-I(o)
    def __rsub__(self,o):return I(o)+-self
    def __mul__(self,o):
        o=I(o)
        low=[self.directed(lambda a=a,b=b:a*b,ROUND_FLOOR)
             for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        high=[self.directed(lambda a=a,b=b:a*b,ROUND_CEILING)
              for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        return I(min(low),max(high))
    __rmul__=__mul__
    def recip(self):
        if self.lo<=0<=self.hi:raise ZeroDivisionError('interval contains zero')
        return I(self.directed(lambda:Decimal(1)/self.hi,ROUND_FLOOR),
                 self.directed(lambda:Decimal(1)/self.lo,ROUND_CEILING))
    def __truediv__(self,o):return self*I(o).recip()
    def __rtruediv__(self,o):return I(o)*self.recip()
    def __pow__(self,n):
        if n<0:return (self.recip())**(-n)
        result=I(1);base=self
        while n:
            if n%2:result=result*base
            base=base*base;n//=2
        return result
    def square(self):
        if self.lo<=0<=self.hi:
            high=max(self.directed(lambda:self.lo*self.lo,ROUND_CEILING),
                     self.directed(lambda:self.hi*self.hi,ROUND_CEILING))
            return I(0,high)
        return self*self
    def sqrt(self):
        if self.lo<0:raise ValueError('negative sqrt interval')
        with localcontext() as ctx:
            ctx.prec=PREC
            lo=self.lo.sqrt();hi=self.hi.sqrt()
            return I(0 if self.lo==0 else lo.next_minus(),hi.next_plus())
    def ln(self):
        if self.lo<=0:raise ValueError('nonpositive log interval')
        with localcontext() as ctx:
            ctx.prec=PREC
            return I(self.lo.ln().next_minus(),self.hi.ln().next_plus())
    def as_strings(self):return [str(self.lo),str(self.hi)]

def imatvec(M,v):
    return [sum((M[i][j]*v[j] for j in range(4)),I(0)) for i in range(4)]

def interval_native(N=512):
    rt5=I(5).sqrt();c=rt5-2;k=(1-c.square()).sqrt()
    phi=(1+rt5)/2;ell=phi.ln()
    z=I(0);one=I(1)
    M=[[c,z,-k,z],[z,c,z,-k],[z,-k,z,-c],[-k,z,-c,z]]
    dM=[[one,z,c/k,z],[z,one,z,c/k],[z,c/k,z,-one],[c/k,z,-one,z]]
    state=[one,z,z,z];dstate=[z,z,z,z];H=I(0);dH=I(0)
    structural_zeros=[]
    for n in range(1,N+1):
        mv=imatvec(M,state);dmv=imatvec(dM,state)
        mdv=imatvec(M,dstate);a=mv[0];da=dmv[0]+mdv[0]
        pp=a.square();dpp=2*a*da
        if pp.hi==0:
            structural_zeros.append(n)
        else:
            if pp.lo<=0:raise ArithmeticError('increase interval precision')
            lp=pp.ln();H=H-pp*lp/ell;dH=dH-dpp*(lp+1)/ell
        state=[z]+mv[1:]
        dstate=[z]+[dmv[i]+mdv[i] for i in range(1,4)]
    sn=sum((x.square() for x in state),I(0))
    dsn=2*sum((state[i]*dstate[i] for i in range(4)),I(0))
    if sn.hi!=0:
        lsn=sn.ln();H=H-sn*lsn/ell;dH=dH-dsn*(lsn+1)/ell
    rho=I(3)/4;theta=rho.sqrt().sqrt().sqrt();rr=theta.square()
    aa=1/rho.sqrt();uu=1+rho.ln();vv=-rr.ln()
    T1=(N+1)/(1-rr)+rr/(1-rr)**2
    T2=N*(N+1)/(1-rr)+2*(N+1)*rr/(1-rr)**2+2*rr.square()/(1-rr)**3
    BN=2*aa**3/(ell*theta)*rr**N*(uu*(T1+N)+vv*(T2+N*N))
    EN=aa.square()/ell*rr**N*((rho.ln()+vv*N)/(1-rr)+vv*rr/(1-rr)**2)
    # Exact ||dM/dc||=1/sqrt(1-c²) on this orthogonal reflection family.
    source_error=BN/k
    total_source=dH+I(source_error.hi.copy_negate(),source_error.hi)
    total_entropy=H+I(0,EN.hi)
    return dict(N=N,precision=PREC,H_N=H.as_strings(),dH_N=dH.as_strings(),
                analytic_source_error=source_error.as_strings(),
                analytic_entropy_error=EN.as_strings(),
                H_infinity=total_entropy.as_strings(),
                dH_infinity=total_source.as_strings(),
                exact_zero_histories=structural_zeros,
                positive_source=total_source.lo>Decimal('10.61'))

def main():
    one_third=I(1)/3
    check('directed_division_contains_exact_third',one_third.lo*3<=1<=one_third.hi*3)
    fifth_root=I(5).sqrt()
    check('outward_square_root_contains_exact_five',fifth_root.square().lo<=5<=fifth_root.square().hi)
    check('interval_negation_is_exact_and_reverses_endpoints',
          (-one_third).lo==one_third.hi.copy_negate() and (-one_third).hi==one_third.lo.copy_negate())
    M,dM=matrices(C_NATIVE);L=np.linalg.norm(dM,2)
    check('literal_native_monodromy_unitary',np.linalg.norm(M.T@M-np.eye(4),2)<1e-14)
    check('known_four_block_contraction',np.linalg.norm(np.linalg.matrix_power(Q@M,4),2)**2<.75)
    check('exact_tangent_norm',abs(L-1/math.sqrt(1-C_NATIVE**2))<1e-14)
    check('elementary_N36_cutoff',abs(A*THETA**36-81/256)<1e-14 and 81/256<1/3)
    long=price_and_source(M,dM,800)
    check('complete_return_mass',abs(long['prob']-1)<2e-14)
    check('complete_mean_four',abs(long['mean']-4)<2e-13)
    check('same_word_second_history_dark',long['probs'][1]==0)
    check('same_word_first_history',abs(long['probs'][0]-C_NATIVE**2)<1e-14)
    for N in (36,64,128,256):
        short=price_and_source(M,dM,N)
        check('complete_finite_normalization_'+str(N),abs(short['prob']+short['survival']-1)<2e-14)
        check('entropy_value_tail_'+str(N),0<=long['H']-short['H']+1e-13<=entropy_tail(N)+2e-13)
        check('entropy_source_tail_'+str(N),abs(long['dH']-short['dH'])<=source_tail(N)*L+2e-12)
    # Noncommuting perturbation: exact orthogonal plane rotation, fixed P.
    for angle in (0.,.001,-.001):
        rot=np.eye(4);rot[:2,:2]=[[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]]
        mm=rot@M;dm=J@mm
        ll=price_and_source(mm,dm,800)
        for N in (36,128,256):
            ss=price_and_source(mm,dm,N)
            check('noncommuting_CQ_source_tail_'+str(angle)+'_'+str(N),
                  abs(ll['dH']-ss['dH'])<=source_tail(N)*np.linalg.norm(dm,2)+2e-12)
    da2=(J@M@Q@M+M@Q@J@M)[0,0]
    check('actual_dark_history_rank_birth',abs(da2+(1-C_NATIVE**2))<1e-14)
    # Literal paid status-code/clock source. This exposes a surviving entropy force.
    g=16.
    C=(g+2)*np.eye(4)-M.T@P@M
    dC=-dM.T@P@M-M.T@P@dM
    full=price_and_source(M,dM,800,C,dC)
    check('whole_status_clock_cost',abs(full['cost']-(4*g+7))<3e-12)
    check('constant_mean_is_not_constant_complete_price',abs(full['dcost'])<1e-12 and full['dS']<-10)
    check('complete_price_source_equals_negative_entropy',abs(full['dS']+full['dH'])<1e-12)
    # Spectator dynamics alone cannot erase a spin-dependent actual price.
    prep_angle=math.pi/8
    C_eff=(2+math.cos(2*prep_angle))*np.eye(4)
    dC_eff=-2*math.sin(2*prep_angle)*np.eye(4)
    prep_price=price_and_source(M,np.zeros((4,4)),800,C_eff,dC_eff)
    check('spin_dependent_price_retains_input_preparation_source',
          abs(prep_price['dH'])<1e-14 and
          abs(prep_price['dS']+8*math.sin(2*prep_angle))<1e-12)
    # A real terminal cap charge and its derivative are included, not normalized away.
    N=64;w=7.;dw=.2;short=price_and_source(M,dM,N,C,dC,w,dw)
    cost_bound=4*(np.linalg.norm(dC,2)+(8*N/3)*np.linalg.norm(C,2)*L)*RHO**(N//4)
    abort_bound=A*A*RR**N*abs(dw)+2*N*A**3/THETA*RR**N*w*L
    check('whole_paid_CQ_source_with_abort_bound',
          abs(short['dS']-full['dS'])<=cost_bound+source_tail(N)*L+abort_bound)
    # Interval calculation includes the complete abort entropy and analytic tail.
    rigor=interval_native(512)
    check('interval_certified_native_entropy_force_positive',rigor['positive_source'])
    bounds=rigor['dH_infinity']
    check('narrow_rigorous_native_source_enclosure',
          Decimal(bounds[0])>Decimal('10.615563318') and Decimal(bounds[1])<Decimal('10.615563320'))
    result=dict(status='PASS',checks=CHECKS,count=len(CHECKS),
        H_native_800=long['H'],dH_dc_native_800=long['dH'],
        supplied_cycle_gate_charge=g,full_status_clock_cost=full['cost'],
        full_CQ_source_dc=full['dS'],interval=rigor,
        scope='same declared monitored 16-stage native return; full pointer/CQ cut',
        physical_monitors_and_field_map_admitted=False,Book_Info_selected=False,GR_closed=False)
    (Path(__file__).resolve().parent/'COMPLETE_MONITORED_CQ_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
