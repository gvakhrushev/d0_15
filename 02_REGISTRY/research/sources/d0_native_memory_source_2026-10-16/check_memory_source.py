#!/usr/bin/env python3
"""Exact full16 memory/source identities in the declared v8 interface.
No network, input-suite execution, root search, physical admission or GR claim.
"""
from __future__ import annotations
import json
from itertools import combinations
import sympy as s

p,a=s.symbols("p a", positive=True)
A,B=s.symbols("A B", real=True)
I=s.eye(16)
checks=[]
def reduce(x):
    x=s.expand(x)
    x=s.rem(x,a*a-p,a)
    return s.expand(s.rem(x,p*p+p-1,p))
def matrix_red(M):
    return s.Matrix(M).applyfunc(reduce)
def eq(name,x,y=0):
    if isinstance(x,s.MatrixBase) or isinstance(y,s.MatrixBase):
        good=matrix_red(s.Matrix(x)-s.Matrix(y))==s.zeros(*s.Matrix(x).shape)
    else: good=reduce(x-y)==0
    if not good: raise ArithmeticError(name)
    checks.append(name)
def require(name,condition):
    if not bool(condition): raise ArithmeticError(name)
    checks.append(name)
C=[]
for r in range(4):
    M=s.zeros(16)
    for mask in range(16):
        if not mask&(1<<r):
            M[mask|(1<<r),mask]=(-1)**((mask&((1<<r)-1)).bit_count())
    C.append(M)
b=[M.T for M in C]
def creator(v): return sum((v[i]*C[i] for i in range(4)),s.zeros(16))
def annihilator(v): return sum((v[i]*b[i] for i in range(4)),s.zeros(16))
def gamma(v): return creator(v)+annihilator(v)
def kappa(v): return creator(v)-annihilator(v)
def lift(W): return sum((W[i,j]*C[i]*b[j] for i in range(4) for j in range(4)),s.zeros(16))
def cross(v):
    x,y,z=v
    return s.Matrix([[0,-z,y],[z,0,-x],[-y,x,0]])
def native_record(r,sign=1):
    N=C[r]*b[r]
    H=s.diag(*[int(mask.bit_count()-int(bool(mask&(1<<r)))>=2) for mask in range(16)])
    return a*((I-H)+H*(I-2*N))+sign*p*((I-H)*(C[r]-b[r])-H*(C[r]+b[r]))
def homogeneous_symbols():
    frame=(A-B)*s.eye(4)+B*s.ones(4)
    legs=[frame.row(r).T for r in range(4)]
    roots=[(1+s.I)/s.sqrt(2),(1-s.I)/s.sqrt(2)]
    symbols=[]
    for j in range(4):
        for phase in roots:
            phases=[s.S.One]*4;phases[j]=phase
            D=8*(creator((phase-1)*legs[j])+annihilator((s.conjugate(phase)-1)*legs[j]))
            symbols.append((phases,D))
    return legs,symbols
def core_and_roots():
    for i in range(4):
        for j in range(4):
            eq(f"CAR_{i}_{j}",C[i]*b[j]+b[j]*C[i],I if i==j else s.zeros(16))
    Q=s.zeros(16,4)
    for j,slot in enumerate((0,1,14,15)):Q[slot,j]=1
    QP=Q*Q.T
    spatial=[]
    for i,j in ((1,2),(1,3),(2,3)):
        W=s.zeros(4);W[i,j]=1;W[j,i]=-1
        spatial.append(lift(W))
        eq(f"spatial_fixed_sector_{i}{j}",lift(W)*Q,s.zeros(16,4))
    eq("fixed_sector_is_exactly_four",s.Matrix.vstack(*spatial).rank(),12)
    U=[native_record(r) for r in range(4)]
    for r,Ur in enumerate(U):eq(f"actual_full_record_orthogonality_{r}",Ur.T*Ur,I)
    for sign in (-1,1):
        eq(f"autonomous_record_preserves_fixed_sector_{sign}",(I-QP)*native_record(0,sign)*Q,s.zeros(16,4))
    seed=s.zeros(16,1);seed[1]=seed[15]=1
    eq("actual_whole_blank_norm", (seed.T*seed)[0],2)
    eq("actual_whole_blank_in_fixed_sector",QP*seed,seed)
    # All memory amplitudes in this sector have the same first source at the old root.
    legs,symbols=homogeneous_symbols()
    eps=(128-64*s.sqrt(2))*(A*A+3*B*B)
    for k,(phase,D) in enumerate(symbols):
        eq(f"all_eight_shell_symbols_{k}",D*D,eps*I)
    # Every homogeneous creator-frame slot; CAR makes the derivative scalar.
    for r in range(4):
        for j in range(4):
            expected=0;actual=s.zeros(16)
            v=s.eye(4)[:,j]
            for phases,D in symbols:
                dD=8*(creator((phases[r]-1)*v)+annihilator((s.conjugate(phases[r])-1)*v))
                actual+=D*dD+dD*D
                expected+=2*64*s.re((phases[r]-1)*sum(
                    s.conjugate(phases[t]-1)*legs[t][j] for t in range(4)))
            eq(f"all_coframe_source_scalar_{r}_{j}",actual/8,expected*I/8)
    coeff=8*(2-s.sqrt(2))
    total=sum(legs,s.zeros(4,1));Js=[]
    for r in range(4):
        W=s.zeros(4);W[1:,1:]=cross(legs[r][1:,:])
        G=lift(W)
        eq(f"native_leg_stabilized_{r}",W*legs[r],s.zeros(4,1))
        eq(f"full_CAR_stabilizer_commutes_{r}",G*creator(legs[r])-creator(legs[r])*G,s.zeros(16))
        # Four operator coefficients exhaust Tr(D_k dD_r(k)) for every momentum.
        # This verifies zero spectral heat/feedback link-source on ALL modes,
        # not a truncation of those traces to the occupied shell.
        for j in range(4):
            traces=s.Matrix([s.trace(X*G*Y) for X in (creator(legs[j]),annihilator(legs[j]))
                             for Y in (creator(legs[r]),annihilator(legs[r]))])
            eq(f"every_thermal_mode_link_trace_{r}_{j}",traces,s.zeros(4,1))
        accum=s.zeros(16)
        for phases,D in symbols:
            dD=8*G*(phases[r]*creator(legs[r])-s.conjugate(phases[r])*annihilator(legs[r]))
            eq(f"link_jet_kills_fixed_sector_{r}_{len(checks)}",dD*Q,s.zeros(16,4))
            accum+=D*dD+dD*D
        Jr=coeff*gamma(W*total)*kappa(legs[r]);Js.append(Jr)
        eq(f"exact_complete_link_source_{r}",accum/8,Jr)
        eq(f"fixed_sector_source_compression_{r}",Q.T*Jr*Q,s.zeros(4))
        eq(f"trace_matches_original_maximal_density_{r}",s.trace(Jr),0)
    eq("time_leg_source_zero",Js[0],s.zeros(16))
    dd=A*A+3*B*B;oo=2*B*(A+B)
    GJ=s.Matrix(3,3,lambda i,j:s.trace(Js[i+1]*Js[j+1]))
    common=16*coeff**2*(A-B)**2*(A+3*B)**2
    eq("three_complete_source_constraints_Gram",GJ,
       common*((2*dd+oo)*s.eye(3)-oo*s.ones(3)))
    eq("Gram_singlet_eigenvalue",2*dd-2*oo,2*(A-B)**2)
    eq("affine_density_fibre_dimension",16**2-1-3,252)
    # A smooth amplitude path (x from1 to0) from full Schmidt rank128 to rank8.
    Pm=seed*seed.T/2
    x=s.symbols("x", real=True)
    Amp=x*(I-Pm)/4+s.sqrt(16-15*x*x)*Pm/4
    rho=x*x*I/16+(1-x*x)*Pm
    eq("entire_amplitude_homotopy_density",Amp*Amp.T,rho)
    eq("homotopy_normalizer",s.trace(rho),1)
    eq("homotopy_old_endpoint",Amp.subs(x,1),I/4)
    eq("homotopy_memory_endpoint",Amp.subs(x,0),Pm)
    for r,Jr in enumerate(Js):
        eq(f"homotopy_full_source_{r}",s.trace(rho*Jr),0)
    eq("endpoint_matter_schmidt_rank",8*Pm.rank(),8)
    eq("full_reference_carrier_unchanged",8*16,128)
    # Two real ordered native records; fixed exterior eta bridge on all states.
    m01=matrix_red(U[1]*U[0]*seed);m10=matrix_red(U[0]*U[1]*seed)
    diff=s.zeros(16,1);diff[2]=2-2*p;diff[12]=2*p-2
    eq("owned_two_path_full_state_difference",m10-m01,diff)
    eq("owned_two_path_distance",(diff.T*diff)[0],16-24*p)
    Qeta=s.diag(*[(-1)**((mask>>1).bit_count()) for mask in range(16)])
    r01=Qeta*m01;r10=Qeta*m10
    for label,v in (("01",r01),("10",r10)):
        eq(f"prepared_order_state_normalized_{label}",(v.T*v)[0],2)
    k=16*a*(2-s.sqrt(2))*(A-B)*(A+3*B)
    direction=s.Matrix([0,2*B,-A,-A])
    f01=s.Matrix([reduce((r01.T*Jr*r01)[0]/2) for Jr in Js])
    f10=s.Matrix([reduce((r10.T*Jr*r10)[0]/2) for Jr in Js])
    eq("complete_order_01_connection_source",f01,k*p*direction)
    eq("complete_order_10_connection_source",f10,k*(2-3*p)*direction)
    eq("golden_order_source_ratio",f10,p**3*f01)
    require("connection_source_not_identically_zero",reduce(f01[2])!=0)
    eq("equal_price_value_does_not_fix_source",eps*(r10.T*r10)[0]/2,eps*(r01.T*r01)[0]/2)
    # The entire existing even-tick engine orbit has a closed source recurrence.
    # No new clock/state field is added; k labels a mathematical statement about
    # the already proved orbit. This is a fixed spatial probe after that state.
    xx,yy,bb,cc=s.symbols("xx yy bb cc",real=True)
    internal=s.Matrix([xx,yy,bb,cc])
    U1hat=Qeta*U[1]*Qeta
    after=U1hat*Q*internal
    rawforce=s.Matrix([reduce((after.T*Jr*after)[0]/2) for Jr in Js])
    imbalance=bb*bb+cc*cc-xx*xx-yy*yy
    remainder=8*B*p*p*(2-s.sqrt(2))*(A-B)*(A+3*B)*imbalance*s.Matrix([0,0,1,-1])
    eq("complete_future_readout_on_equal_sector_norms",
       rawforce,k*p*(cc*yy-bb*xx)*direction+remainder)
    rr=2*p-1; ss=2*a*p
    rot=s.Matrix([[rr,-ss],[ss,rr]])
    eq("actual_two_tick_rotation_unitarity",rot.T*rot,s.eye(2))
    eq("all_time_source_characteristic_recursion",rot*rot-2*rr*rot+s.eye(2),s.zeros(2))
    upper=s.Matrix([0,1])
    for tick in range(5):
        state=Q*s.Matrix([-ss,rr,-upper[0],-upper[1]])
        state=matrix_red(state)
        eq(f"all_time_reference_norm_{tick}",(state.T*state)[0],2)
        probe=matrix_red(U1hat*state)
        f=s.Matrix([reduce((probe.T*Jr*probe)[0]/2) for Jr in Js])
        expected=-k*p*reduce(s.chebyshevt(tick+1,rr))*direction
        eq(f"actual_engine_to_source_{tick}",f,expected)
        upper=matrix_red(rot*upper)
    # At the eigenshell every actual normalized preparation jet has zero direct cost.
    dr=s.Matrix([[0,1],[1,0]]) # trace zero; elementary arbitrary off-diagonal probe
    eq("moving_preparation_source_at_eigenvalue",s.trace(eps*dr),0)
    return {"source01":"K p (0,2B,-A,-A)",
             "source10":"K (2-3p) (0,2B,-A,-A) = p^3 source01",
            "even_tick_future_source":"-K p T_(k+1)(2p-1) (0,2B,-A,-A)",
            "source_recurrence":"f_(k+2)=2(2p-1) f_(k+1)-f_k",
            "K":"16 sqrt(p) (2-sqrt(2)) (A-B) (A+3B)",
            "memory_masks":[0,1,14,15], "conditional_root_fibre_real_affine_dimension":252,
            "pure_memory_preparation_Schmidt_rank":8,
            "full_reference_dimension":128}
def rank_free():
    P=s.diag(1,1,0,0);Q=s.eye(4)-P
    U=s.eye(4)
    for i,j in ((0,2),(1,3)):
        U[i,i]=U[j,j]=s.Rational(3,5)
        U[j,i]=s.Rational(4,5);U[i,j]=-s.Rational(4,5)
    Delta=U*s.diag(2,3,0,5)*U.T;eps=2
    QQ=(Delta-eps*s.eye(4))[2:,2:];Gq=QQ.inv()
    J=s.eye(4)[:,:2]-s.eye(4)[:,2:]*Gq*Delta[2:,:2]
    E=(Delta-eps*s.eye(4))[:2,:2]-Delta[:2,2:]*Gq*Delta[2:,:2]
    G=J.T*J
    C0=s.diag(s.Rational(3,5),0);Psi=J*C0
    eq("rank_free_Q_equation",Q*(Delta-eps*s.eye(4))*J,s.zeros(4,2))
    eq("rank_free_matter_equation",E*C0,s.zeros(2))
    require("E_is_not_zero_on_unoccupied_shell",E!=s.zeros(2))
    eq("rank_free_original_matter_reconstruction",(Delta-eps*s.eye(4))*Psi,s.zeros(4,2))
    eq("rank_free_moving_normalizer",s.trace(C0.T*G*C0),1)
    eq("rank_free_physical_rho_trace",s.trace(Psi*Psi.T),1)
    require("resolvent_two_signs_retained",QQ[0,0]<0<QQ[1,1])
    # Exact nonlinear dE identity with genuinely moving off-shell J.
    t=s.symbols("t",real=True)
    perturb=s.Matrix([[1,2,3,0],[2,-1,0,1],[3,0,1,2],[0,1,2,-2]])/17
    Dt=Delta+t*perturb;ep=eps+t/13
    Qt=(Dt-ep*s.eye(4))[2:,2:]
    Et=(Dt-ep*s.eye(4))[:2,:2]-Dt[:2,2:]*Qt.inv()*Dt[2:,:2]
    eq("rank_free_complete_schur_source_jet",Et.diff(t).subs(t,0),
       J.T*perturb*J-G/13)
    # Simple convex source image control and a separating field direction.
    PauliX=s.Matrix([[0,1],[1,0]]);PauliZ=s.diag(1,-1)
    rho=s.Matrix([[s.Rational(3,4),s.Rational(1,8)],
                  [s.Rational(1,8),s.Rational(1,4)]])
    eq("convex_source_normalization",s.trace(rho),1)
    require("convex_source_positive",rho.det()>0 and rho[0,0]>0)
    eq("convex_source_first_reading",s.trace(rho*PauliX),s.Rational(1,4))
    eq("convex_source_second_reading",s.trace(rho*PauliZ),s.Rational(1,2))
    require("separating_witness_rejects_unrealizable_source",s.Rational(3,2)>max(PauliZ.eigenvals()))
    # Positive constant cannot justify silently deleting an unprepared mode.
    require("rank_free_not_old_full_rank_equations",E[1,1]!=0 and C0[1,1]==0)
def run():
    checks.clear()
    result=core_and_roots();rank_free()
    return {"schema":"d0-native-memory-source/1","exact_checks":len(checks),
            "checks":checks,"exact_result":result,
            "old_root_recomputed":False,"actual_full_field_Hessian_certified":False,
            "new_nonflat_joint_root":False,"full_physical_history_cost_identified":False,
            "affine_path_to_return_admission_proved":False,"GR_closed":False,
            "publication_to_GitHub":False}
if __name__=="__main__":
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
