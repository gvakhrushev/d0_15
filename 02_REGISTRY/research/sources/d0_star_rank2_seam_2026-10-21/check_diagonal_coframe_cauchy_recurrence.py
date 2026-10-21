#!/usr/bin/env python3
"""Original six-face finite D0: exact two-real-CAR matter plus FOUR
unrestricted diagonal coframe Euler rows by a coherent one-step recurrence.
The remaining off-diagonal coframe and proper-link rows are genuinely NONZERO.
This is not a whole42 root, physical Book choice, all-metric gauge theorem,
or a two-end Dirichlet solution. Uses the original N=1 source ON f=q=0.
"""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import expm
from scipy.optimize import root
from scipy.special import erfi
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
INPUT={
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py":
"a57f0e3e845290923c2ac88d39ba5c08af4f6fd6",
"02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py":
"525b257ec671500bd02c4791f9579dbde2439f21"}
def checkpins():
    for path,expect in INPUT.items():
        content=(ROOT/path).read_bytes()
        got=hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest()
        if got!=expect:raise AssertionError(("immutable owner changed",path,got,expect))
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(ROOT/"02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21"))
from check_star_rank2_seam import star_density,matter_query,LORENTZ,KAPPA,ETA,I
from native_master import GoldenMaster

def clock(r):
    return np.sqrt(np.pi/2)*(erfi(r/np.sqrt(2))-erfi(1/np.sqrt(2)))
def radius(t):
    return brentq(lambda r:clock(r)-t,.5,1.6,xtol=1e-14)
def golden_curve(r):
    A=np.sqrt(r)*np.exp(-r*r/4)
    k1=(1-r**-2)/2
    k2=np.exp(-r*r/4)/np.sqrt(r)
    return A,k1,k2
def boost(i):
    X=np.zeros((4,4))
    X[0,i]=X[i,0]=1.
    return X
BOOST=[boost(j) for j in (1,2,3)]
def comm(x,y):
    return np.sinh(x)*np.sinh(y)*(1-(np.cosh(x)-1)*(np.cosh(y)-1)/2)

def symbolic_reduction():
    r=s.symbols("r",positive=True)
    A=s.sqrt(r)*s.exp(-r*r/4)
    k1=(1-r**-2)/2
    k2=s.exp(-r*r/4)/s.sqrt(r)
    ddt=lambda f:s.simplify(s.exp(-r*r/2)*s.diff(f,r))
    kd=ddt(k2)
    E1=s.simplify(2*r*k1*k2+k2*k2/A-A)
    E2=s.simplify(2*r*kd+A*k2*k2+A**3)
    assert E1==0 and E2==0
    X,R=s.symbols("X R",positive=True)
    E_X=2*R*k1*k2+k2*k2/X-X
    E_Y=2*R*kd+X*k2*k2+X**3
    J=s.det(s.Matrix([[s.diff(E_X,X),s.diff(E_X,R)],
                      [s.diff(E_Y,X),s.diff(E_Y,R)]]))
    expected=-2*(r**4-2*r*r-1)*s.exp(-3*r*r/4)/r**s.Rational(7,2)
    assert s.simplify(J.subs({X:A,R:r})-expected)==0
    flow=-(kd/A+A*k1*k2)/r
    assert s.simplify(flow-ddt(k1))==0
    h,s1,s2,c12,c22=s.symbols("h s1 s2 c12 c22",nonzero=True)
    # Unscaled exact coframe first jets in the pre-existing original action
    ex=2*R*c12+c22/X-h*h*X
    ey=2*R*s2+X*c22+h*h*X**3
    ez=R*s1+s2/X+X*c12
    f=R*R*s1+2*R*s2/X+2*X*R*c12+c22
    # Radial Ward: sum of FOUR diagonal coframe Euleri = 2*f
    # on q=0; no 'f=0' equation added by hand.
    assert s.simplify(X*ex+(1/X)*ey+2*R*ez-2*f)==0
    sz=s.symbols("z")
    eq_poly=h*h*c12*sz*sz+(h*h*s2+c12*c22)*sz-s2*c22
    assert s.simplify((ex*X*s2-ey*X*c12)+eq_poly.subs(sz,X*X))==0
    q=2*s.symbols("eps",positive=True)**2
    # Discrete matter current J_t=p_t/X², Q=p_t²/X²-eps²/Y².
    # Q=0 => p_t=eps*X/Y and J_t=eps/(X*Y).
    PT,EP,Y=s.symbols("p_t epsilon Y",positive=True)
    j=s.simplify((PT/X**2).subs(PT,EP*X/Y))
    assert j==EP/(X*Y)
    return {"two_geometric_algebraic_equations":"E_X=E_Y=0",
       "quadratic_X_squared":"h² C12 z² + (h² S2+C12 C22)z - S2 C22=0",
       "third_connection_recurrence":"k1_next = k1 + asinh(-(S2/X+X C12)/R)/h",
       "jacobian_at_seed":str(expected),
       "positive_chart":"0<r<sqrt(1+sqrt(2))",
       "continuum_flow":"k1_t = exp(-r²/2)/r³",
       "q_zero_and_matter_euler":"X*Y=constant, not a freely postulated ansatz",
       "radial_trace_identity":"X EX + Y EY + 2 R Eperp = 2 f on q=0"}

def solve_slab(lo,hi,n):
    # User-given Cauchy k1(lo), prescribed smooth original k2(t).
    # Boundary t_hi is OUTPUT, not an independently fixed Dirichlet datum.
    ts=np.linspace(clock(lo),clock(hi),n+1)
    h=float(ts[1]-ts[0])
    amp=np.sqrt(1/(2*KAPPA))
    k1=golden_curve(lo)[1]
    cells=[];stats=[]
    for j in range(n):
        t=ts[j]
        r=radius(t)
        rnext=radius(ts[j+1])
        A,_,k2=golden_curve(r)
        _,_,k2next=golden_curve(rnext)
        s2=np.sinh(h*(k2next-k2))
        c12=comm(h*k1,h*k2)
        c22=comm(h*k2,h*k2)
        def Euler(p):
            xx,rr=p
            return np.array([(2*rr*c12+c22/xx)/h**2-xx,
                             (2*rr*s2+xx*c22)/h**2+xx**3])
        root2=root(Euler,[A,r],tol=1e-11)
        xx,rr=root2.x
        err=float(max(abs(Euler([xx,rr]))))
        if xx<=0 or rr<=0 or err>2e-10:
            raise AssertionError(("algebraic coframe equations",lo,hi,n,j,err,root2.message))
        Y=1/xx
        s1=-(s2/xx+xx*c12)/rr
        k1_next=k1+np.arcsinh(s1)/h
        U=np.array([I]+[expm(h*ww*BOOST[i]) for i,ww in enumerate((k1,k2,k2))],dtype=complex)
        co=np.diag([xx,Y,rr,rr]).astype(complex)
        # TRUE finite scalar increments, not a substituted continuum stress.
        grads=np.array([[amp*xx*xx,0,0,0],[0,amp,0,0]],dtype=complex)
        cells.append(dict(e=co,u=U,v=grads))
        stats.append(dict(r=r, X=xx,R=rr,k1=k1,
                          x_from_seed=xx-A,R_from_seed=rr-r,
                          k1_from_seed=k1-golden_curve(r)[1]))
        k1=k1_next
    U_final=np.array([I]+[expm(h*ww*BOOST[i]) for i,ww in
                            enumerate((k1,golden_curve(hi)[2],golden_curve(hi)[2]))],dtype=complex)
    cells.append(dict(e=np.diag([1,1,hi,hi]).astype(complex),
                      u=U_final,v=np.zeros((2,4),dtype=complex)))
    # Original CAR scalar time history exists by chronological summation;
    # psi2=amp*x is the other independent spatial history.
    first_history=np.cumsum([0.]+[h*c['v'][0,0].real for c in cells[:-1]])
    assert len(first_history)==n+1
    max_f=max_q=max_diag=max_off=0.
    dx=1e-20
    for j in range(n):
        cur,nxt=cells[j:j+2]
        f=float(abs(star_density(cur,nxt,h)))
        q=float(abs(matter_query(cur)))
        if f>max_f:max_f=f
        if q>max_q:max_q=q
        # Differentiate all four original diagonal coframe components with
        # BOTH true real scalar gradients held FIXED, not moved with coframe.
        diag=[]
        for a in range(4):
            old=cur['e'][a,a]
            cur['e'][a,a]=old+1j*dx
            grad=(star_density(cur,nxt,h)+KAPPA*matter_query(cur)).imag/dx
            cur['e'][a,a]=old
            diag.append(grad)
        max_diag=max(max_diag,float(max(abs(v) for v in diag)))
        if j==n//2:
            for a in range(4):
                for b in range(4):
                    if a==b:continue
                    old=cur['e'][a,b]
                    cur['e'][a,b]=old+1j*dx
                    grad=(star_density(cur,nxt,h)+KAPPA*matter_query(cur)).imag/dx
                    cur['e'][a,b]=old
                    max_off=max(max_off,float(abs(grad)))
    assert max_f<3e-10 and max_q<2e-14 and max_diag<3e-9
    Xdiff=max(abs(x["x_from_seed"]) for x in stats)
    Rdiff=max(abs(x["R_from_seed"]) for x in stats)
    Kdiff=max(abs(x["k1_from_seed"]) for x in stats)
    assert max_off>1e-6,"remaining off-diagonal Euler source must not be hidden"
    assert max(Xdiff,Rdiff,Kdiff)<2.0*h
    return dict(r_interval=[lo,hi],steps=n,h=h,
       full_original_6face_f_max=max_f,actual_two_CAR_Q_max=max_q,
       all_four_true_diagonal_coframe_Euler_max=max_diag,
       unsolved_offdiagonal_coframe_Euler_midpoint=max_off,
       X_seed_distance=Xdiff,R_seed_distance=Rdiff,k1_seed_distance=Kdiff,
       two_original_material_current_rows="ZERO at all free interior stencils",
       exact_timeline="Cauchy k1 initial data; final k1 is derived, not prescribed",
       actual_sigma="same old Golden N1 with canonical x->-x retyping",
       PF="any fixed original positive counts on exact f=q=0 sheet")

def main():
    checkpins()
    master=GoldenMaster(55)
    assert master.a<0<master.b and abs(float(master.kappa)-KAPPA)<2e-12
    exact=symbolic_reduction()
    samples=[solve_slab(lo,hi,n) for lo,hi in
       ((1,1.2),(.85,1.15),(.9,1.4)) for n in (16,32,64,128)]
    print(json.dumps({"status":"PASS_EXACT_DIAGONAL_FOUR_PLUS_TWO_CAUCHY_BRANCH",
      "math":exact,"samples":samples,
      "scope":{"full42_exact_stationary":False,
         "solved_four_diagonal_coframe":True,"solved_two_scalar_Euler":True,
         "star_and_CAR_Q_zero_every_based_cell":True,
         "offdiagonal_coframe_Euler_not_zero":True,
         "full_proper_link_Euler_not_zero":True,
         "two_ended_fixed_collar_solved":False,
         "nonlinear_Book03_compulsory_selection":False,
         "GR_closed":False}},indent=2))

if __name__=="__main__":main()
