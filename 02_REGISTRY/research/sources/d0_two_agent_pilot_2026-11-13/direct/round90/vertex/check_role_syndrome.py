"""Native matched syndrome and the central-positive ambiguity on the A89 terminal."""
from itertools import product
import json
import sympy as sy
import numpy as np
from mpmath import iv

iv.dps=65
p=(iv.sqrt(5)-1)/2
a=iv.sqrt(p)
theta=iv.atan2(p,a)
tau=2320*theta-492*iv.pi


def need(condition,label):
    if not condition:
        raise ArithmeticError(label)


def interval(x,lo,hi):
    need(x.a>iv.mpf(lo) and x.b<iv.mpf(hi),(x,lo,hi))
    return [lo,hi]


def rot(t):
    return np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])


def suite():
    eye=np.eye(4)
    li=np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    lj=np.array([[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]])
    roles=[sg*e for sg in (1,-1) for e in (eye,li,lj,li@lj)]
    need(np.array_equal(li@li,-eye) and np.array_equal(li@lj,-lj@li),"physical Q8")
    cx=np.eye(4)[:,[0,1,3,2]]
    z=np.diag([1.,-1.])
    g=rot(float(theta.mid))
    need(np.max(abs(z@g@z-g.T))<1e-14,"true routed inverse")
    qA=float((2*p**3*(p*iv.sin(448*theta))**2).mid)
    expected=[]
    smallest=1.
    counts=0
    for k,sg,j,s,m,phase in product(range(2),(-1,1),range(2),range(2),range(2),range(2)):
        delta=sg*float(tau.mid) if j^s==k else 0.
        alpha=float(theta.mid)+(-1)**(s+m)*delta+phase*np.pi/2
        U=rot(alpha-float(theta.mid)); pre=U@g
        head=pre[:,0]; dark=np.array([-np.sin(alpha),np.cos(alpha)])
        state=np.kron(head,[1.,0.])
        # Inverse preparation, CX into real zero, then the original preparation.
        audited=np.kron(pre,np.eye(2))@cx@np.kron(pre.T,np.eye(2))@state
        need(np.max(abs(audited-state))<2e-14,"original complete ket/tape changed")
        # Fix the predecessor mass of each actual material branch (both positive).
        q=qA*(1+(5/16)*j); need(0<(q if m else 1-q)<1,"missing material branch")
        c,ss=np.cos(alpha),np.sin(alpha)
        r=(abs(ss/c))**2
        lower=(abs(ss)-abs(c)*r)**2/(1+r*r)
        for A,B in product(roles,repeat=2):
            D=(dark[0]*A+dark[1]*r*B)/np.sqrt(1+r*r)
            eigen=np.linalg.eigvalsh(D.T@D)[0]
            need(eigen+2e-14>=lower,"arbitrary spin/reference lower bound")
            smallest=min(smallest,eigen);counts+=1
        expected.append(lower)
    need(abs(min(expected)-smallest)<2e-14,"role bound not attained")
    # Golden monitor, fresh flag f, data target 0: full Kraus operators incl failures.
    av=float(a.mid);pv=float(p.mid); I=np.eye(2);X=np.eye(2)[::-1]
    birth=np.array([av,pv]); blocks=np.split(np.kron(g.T,I)@cx@np.kron(birth[:,None],I),2)
    need(np.max(abs(blocks[0]-(pv*I+pv**2*X)))<1e-14,"B149 first native branch")
    need(np.max(abs(blocks[1]-av*pv*(X-I)))<1e-14,"B149 real failure")
    need(np.max(abs(sum(K.T@K for K in blocks)-I))<1e-14,"trace preserving")
    layers=[np.diag([av,pv]),np.diag([pv,av])]
    masses={}
    for i,K in enumerate(blocks):
        for b,ext in enumerate(layers):
            leaf=ext@K[:,0]
            masses[str(i)+str(b)]=float(leaf@leaf)
            if (i,b)==(0,1):
                need(abs(leaf@leaf-pv**3)<1e-14,"joint successful mass")
                need(np.max(abs(leaf/np.linalg.norm(leaf)-birth))<1e-14,"native absolute conversion")
    need(abs(sum(masses.values())-1)<2e-14,"lost double-filter leaf")
    return counts


def exact():
    # Algebraic reduction p=a^2, a^4+a^2=1. All center identities avoid floats.
    x=sy.symbols("x"); P=x*x
    def same(expr):
        numerator=sy.cancel(expr).as_numer_denom()[0]
        need(sy.rem(numerator,x**4+x*x-1,x)==0,str(expr))
    same((P*P)**2+(x*P*P)**2-P**3)
    same((1+x)/2-(1-x)/2-x)
    same(P/x-x)
    same(P**2*(1-x)**2/(1+P**2) - (-P+x*P)**2/(1+P**2))
    same(2*P**2/(1+P)-2*P**3)


if __name__=="__main__":
    exact()
    rows=[]
    for sign in (-1,0,1):
        al=theta+sign*tau
        r=iv.tan(al)**2
        floor=(iv.sin(al)-r*iv.cos(al))**2/(1+r*r)
        bounds={-1:(".01492",".01494"),0:(".01263",".01265"),1:(".01046",".01048")}[sign]
        rows.append({"displacement":sign,"minimum_dark_probability":interval(floor,*bounds)})
    print(json.dumps({"tested_role_and_predecessor_combinations":suite(),
       "full_old_gram_zero_for_native_head":True, "all_wrong_law_lower_bounds":rows,
       "opposite_central_share_needed":interval((1-a)/2,".10692",".10693"),
       "strict_record_mark_dark_probability":interval(2*p**3,".47213",".47214"),
       "single_filter_accepted_mass":"p^2+p^4","two_filter_accepted_mass":"p^3",
       "first_filter":"p I + p^2 X","matching_success_effect_on_head":"diag(p,sqrt(p))",
       "positive_Q8_augmentation_fixed_by_spin":False,
       "full_economic_vertex_determined":False,"GR_closed":False},indent=2))
