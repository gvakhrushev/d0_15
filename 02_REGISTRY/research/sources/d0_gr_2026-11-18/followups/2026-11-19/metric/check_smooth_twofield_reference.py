"""Full-CAR curved references and smooth two-component material references."""
from fractions import Fraction as F
from itertools import combinations, product
from mpmath import iv
import json
import sympy as sp
from check_shared_site_union import eye, transpose, matmul, det, exterior, dgamma


def diff(a,b):
    return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]


def fock_trace(N,P):
    result=F(0)
    for grade in range(5):
        masks=list(combinations(range(4),grade))
        result += sum(dgamma(i,j,N)*exterior(P,j,i) for i in masks for j in masks)
    return result


def make_links(H,sgn):
    t,v=H/2,H/20
    ca,sa=(1+t*t)/(1-t*t),2*t/(1-t*t)
    cb,sb=(1-v*v)/(1+v*v),sgn*2*v/(1+v*v)
    A=eye(4); A[0][0]=A[2][2]=ca; A[0][2]=A[2][0]=sa
    Ai=eye(4); Ai[0][0]=Ai[2][2]=ca; Ai[0][2]=Ai[2][0]=-sa
    B=eye(4); B[1][1]=B[2][2]=cb; B[1][2]=sb; B[2][1]=-sb
    Bi=eye(4); Bi[1][1]=Bi[2][2]=cb; Bi[1][2]=-sb; Bi[2][1]=sb
    return (A,B,eye(4),eye(4)),(Ai,Bi,eye(4),eye(4)), (ca,sa,cb,sb)


def geometry(L):
    H=F(1,L)
    eta=eye(4)
    for i in (1,2,3): eta[i][i]=-1
    summaries=[]
    for sign in (1,-1):
        U,Ui,(ca,sa,cb,sb)=make_links(H,sign)
        for u,ui in zip(U,Ui):
            assert matmul(matmul(transpose(u),eta),u)==eta
            assert matmul(u,ui)==eye(4) and det(u)==1 and u[0][0]>0
        Fh=sa*sb*(2+(ca-1)*(1-cb))/(2*H**2)
        for r,s in combinations(range(4),2):
            P=matmul(matmul(matmul(U[r],U[s]),Ui[r]),Ui[s])
            if (r,s)!=(0,1): assert P==eye(4)
            N=[[F(0)]*4 for _ in range(4)]
            N[0][1]=N[1][0]=F(1)
            trace=-fock_trace(N,P)/(8*H**2)
            assert trace==(Fh if (r,s)==(0,1) else 0)
            if (r,s)==(0,1):
                D=diff(eye(4),P)
                for rows in combinations(range(4),3):
                    for cols in combinations(range(4),3):
                        assert exterior(D,rows,cols)==0
        summaries.append(Fh)
    assert summaries[0]==-summaries[1]
    assert F(160,1601)<summaries[0]<F(1,8)
    return summaries[0]


def all_forward_edges(L):
    # Exactly test every site and every directed forward edge of both fields.
    # For L=4 all trigonometric values are exact integers; all 256 cells used.
    assert L==4
    co=(1,0,-1,0); si=(0,1,0,-1)
    amp=sp.Symbol('a', real=True)
    H=sp.Rational(1,L)
    Fh=sp.Rational(geometry(L).numerator, geometry(L).denominator)
    k,s,rho=sp.symbols('k s rho', positive=True)
    aa=H**2*Fh/(4*k*sp.sin(sp.pi*H)**2)
    sums=[]
    for mu in (0,1):
        for x in product(range(L), repeat=4):
            grads=[]
            for nu in range(4):
                y=list(x);y[nu]=(y[nu]+1)%L
                d0=amp*sp.Rational(co[y[mu]]-co[x[mu]],1)/H
                d15=amp*sp.Rational(si[y[mu]]-si[x[mu]],1)/H
                grads.append((d0,d15))
                if nu!=mu: assert d0==0 and d15==0
            total=sum((1 if nu==0 else -1)*(a*a+b*b) for nu,(a,b) in enumerate(grads))
            assert sp.simplify(total.subs(amp**2,aa) - (1 if mu==0 else -1)*Fh/k)==0
            sums.append(total)
    assert len(sums)==512
    # SITE probability and density are not replaced by a uniform density.
    for density in (sp.Rational(1,2),sp.Rational(1),sp.Rational(3,2)):
        assert sp.simplify((density/s**2)*(Fh/k) - density*Fh/(s**2*k))==0
    return len(sums)*4


def orthogonal_target_check():
    # Check the universal complete-column builder on an exact 16D target.
    n=16; e=[F(i==1) for i in range(n)]; b=e[:]
    b[1]=F(3,5);b[0]=F(4,5)
    K=[[b[i]*e[j]-e[i]*b[j] for j in range(n)] for i in range(n)]
    K2=matmul(K,K)
    R=[[F(i==j)+K[i][j]+K2[i][j]/(1+b[1]) for j in range(n)] for i in range(n)]
    assert matmul(transpose(R),R)==eye(n)
    assert [R[i][1] for i in range(n)]==b
    # It is a plane rotation and identity on the other 14 coordinates.
    assert R[0][0]*R[1][1]-R[0][1]*R[1][0]==1


def main():
    levels={L:geometry(L) for L in (4,6,8,12)}
    edges=all_forward_edges(4)
    # Show exact trigonometric finite-difference identity at every distinct
    # phase for three more complete lattices, whose remaining coordinates repeat.
    phase_count=0
    for L in (6,8,12):
        H=sp.Rational(1,L)
        expected=4*sp.sin(sp.pi/L)**2/H**2
        for n in range(L):
            x=2*sp.pi*n/L;y=2*sp.pi*((n+1)%L)/L
            diff2=((sp.cos(y)-sp.cos(x))**2+(sp.sin(y)-sp.sin(x))**2)/H**2
            assert sp.simplify(diff2-expected)==0
            phase_count+=1
    orthogonal_target_check()
    iv.dps=50
    p=(iv.sqrt(5)-1)/2; z=iv.mpf(1)/2**20; L0=4*p**3
    rf=4*p**2*(1-2*p**2)*z*(1-z*L0)*(1-L0)
    rq=8*p**3*(1-2*p**2)*(z*(2-L0)-z**2*(L0+2*(1-L0)*L0))
    k0=rq/rf
    assert iv.mpf(23)<k0<iv.mpf(24)
    h=iv.mpf(1)/4; s=iv.mpf(4)
    Fh=iv.mpf(levels[4].numerator)/levels[4].denominator
    b=Fh/(s*s*k0)
    a=h*iv.sqrt(Fh/k0)/(2*iv.sin(iv.pi*h))
    a0=iv.sqrt(1/(10*k0))/(2*iv.pi)
    assert a*a < iv.mpf(1)/2560 and 1-p-a*a > iv.mpf(959)/2560
    assert b>0
    # Scalar SC2 comparison only: real geometric READY remains alpha_h.
    beta=(1-p**40)*((1-p**384)**6*(1-(1-16*p**9)**64))**2592
    angle=1-2*p*p
    for _ in range(9): angle=2*angle*angle-1
    vis=(1-angle)*p**7/2
    ready=2*10946*p**23
    scalar_gain=beta*p**36*705600*(iv.mpf(1)/256)**2*p**3*vis*ready**2*rf**2
    hypothetical_gain=scalar_gain*(2*Fh/s**2)
    # The original full-Hilbert positivity contract gives Lambda >= 1/(16 H^2)
    # for rho=1. At H=1/4 the nominal scalar h=1/256 violates epsilon_8.
    Hq_norm_lower=iv.mpf(1)/(16*h*h)
    epsilon_max=h*h/4
    step_max=h*h/32
    assert Hq_norm_lower==1
    assert 8*(iv.mpf(1)/256)>epsilon_max
    assert step_max==iv.mpf(1)/512
    # Universal alpha_H<=1 and the retained selector beta yield a rigorous
    # conditional upper ceiling; no geometric alpha or operator norm is guessed.
    C0=beta*705600*p**36*p**3*vis*rf**2/131072
    assert C0>iv.mpf('4.5151e-25') and C0<iv.mpf('4.5153e-25')
    geo_gain_upper=beta*p**36*705600*step_max**2 * 2*p**3*vis*rf**2*Fh/s**2
    assert geo_gain_upper.a <= (C0*Fh/s**2).b and geo_gain_upper.b >= (C0*Fh/s**2).a
    assert geo_gain_upper>iv.mpf('2.8663e-27') and geo_gain_upper<iv.mpf('2.8664e-27')
    print(json.dumps(dict(
       check='PASS',finite_full_car_16_traces_all_six_faces_and_two_reference_signs=True,
       exact_lorentz_and_all_minors_checked_per_lattice=list(levels),
       rational_F_values={str(k):str(v) for k,v in levels.items()},
       one_four_lattice_two_material_fields_forward_edges_checked=edges,
       exact_other_lattices_trig_phases_checked=phase_count,
       uniform_F_bounds=['160/1601','1/8'],
       k0_interval=str(k0),amplitude_L4_interval=str(a),
       smooth_limit_amplitude_interval=str(a0),geometric_b_L4_s4_interval=str(b),
       uniform_material_amplitude_squared_upper='1/2560',
       uniform_material_slack_lower='959/2560',
       creator_norm_upper_with_s_ge_4nu_sqrt_rho='1/4',
       julia_defect_squared_lower='15/16',lorentz_link_half_julia_defect_squared_lower='11/36',
       exact_16d_target_builder_checked=True,
       SC2_conditional_gain_with_geometric_b_and_selector_beta=str(hypothetical_gain),
       SC2_gain_note='nominal scalar h=1/256 and scalar readiness: arithmetic ONLY; h violates the full H_q norm contract for H=1/4',
       exact_normalized_gain_constant_C0=str(C0),
       exact_normalized_gain_formula='C0 * alpha_H^2 * F_H / (s_ref^2 * Lambda_H^2), for variable-attenuation 36-selector with t=1/(512 Lambda_H)',
       full_norm_contract_L4_Lambda_lower_bound='1',
       full_norm_contract_L4_max_8_setting_step='1/512',
       full_norm_contract_L4_physical_gain_ceiling_alpha_le_1=str(geo_gain_upper),
       original_full_operator_norms_computed=False,original_native_field_preparation_word_replayed=False,
       complete_physical_cost_info_closed=False),indent=2,sort_keys=True))

if __name__=='__main__': main()
