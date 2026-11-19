"""Outward-interval certificate for the declared spectral H_C+J full42 root.

One global heat logarithm, exact original collar and exponential links.
Analytic Cauchy error bounds certify complex-step gradient and Hessian.
No physical compulsory D0 action or independent apparatus root is asserted.
"""
from pathlib import Path
import json,hashlib,time,sys
from mpmath import mp,iv
from spectral_model import Spectral42

ROOT=Path(__file__).resolve().parent
N=42

def require(v,what):
    if not bool(v):raise RuntimeError(what)

def up(x):
    return mp.mpf(x.b._mpi_[1])

def down(x):
    return mp.mpf(x.a._mpi_[0])

def nrm(A):
    return max(sum((abs(A[i,j]) for j in range(A.cols)),iv.mpf(0)).b for i in range(A.rows))

def s(x):return mp.nstr(x,42)

def main():
    t=time.monotonic();mp.dps=140;iv.dps=140
    raw=(ROOT/'original_model.py').read_bytes()
    original_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(original_blob=='6d5b41ce11a941fde95e722e708ebb02d689985c','original model changed')
    rec=json.loads((ROOT/'spectral_center.json').read_text())
    center=rec['z42'];require(len(center)==N,'dimension')
    m=Spectral42(iv)
    R=iv.mpf('1e-4');M=iv.mpf(100);delta=iv.mpf('1e-35');radius=iv.mpf('1e-25')
    cp=[mp.mpf(v) for v in center]
    # Rectangular complex enclosure contains the full radius-R polydisc.
    box=[iv.mpc(iv.mpf(v)+iv.mpf(['-1e-4','1e-4']),iv.mpf(['-1e-4','1e-4'])) for v in center]
    valuebox=m.price(box)
    require(abs(valuebox).b<M,'analytic scalar majorant')
    c=[iv.mpc(v) for v in center];f0=m.price(c).real
    singles=[];grad=[]
    gerr=2*M*delta**2/R**3;herr=8*M*delta**2/R**4
    gs=iv.mpf([-up(gerr),up(gerr)]);hs=iv.mpf([-up(herr),up(herr)])
    require(delta/R<iv.mpf('0.01'),'complex-step tail ratio')
    for i in range(N):
        z=list(c);z[i]+=iv.mpc(0,delta);v=m.price(z)
        singles.append(v.real);grad.append(v.imag/delta+gs)
    H=iv.matrix(N,N)
    for i in range(N):
        H[i,i]=-2*(singles[i]-f0)/delta**2+hs
        for j in range(i):
            z=list(c);z[i]+=iv.mpc(0,delta);z[j]+=iv.mpc(0,delta)
            H[i,j]=-(m.price(z).real-singles[i]-singles[j]+f0)/delta**2+hs
            H[j,i]=H[i,j]
        if i%7==6:print('validated Hessian rows',i+1,'elapsed',round(time.monotonic()-t,1),file=sys.stderr,flush=True)
    # The rounded inverse is an exact rational matrix. Its quality is checked,
    # not assumed from mpmath inversion accuracy or floating eigenvalues.
    mid=mp.matrix([[mp.mpf(H[i,j].mid._mpi_[0]) for j in range(N)] for i in range(N)])
    approx=mid**-1
    A=iv.matrix([[iv.mpf(mp.nstr(approx[i,j],90)) for j in range(N)] for i in range(N)])
    anorm=nrm(A);defect=nrm(iv.eye(N)-A*H)
    g=iv.matrix(grad);alpha=nrm(A*g)
    C=N*N*48*M/R**3
    b=defect+anorm*C*radius
    require(defect.b<iv.mpf('1e-12'),'verified inverse defect')
    require(radius<R/2,'Cauchy domain margin')
    require(b.b<iv.mpf('0.1'),'contraction on full42 ball')
    require((alpha+b*radius).b<radius,'strict self map')
    # Root is nonflat, orientation preserving and has rank-two scalar currents.
    rb=[iv.mpf(v)+iv.mpf(['-1e-25','1e-25']) for v in center]
    e,U,ps=m.nodes(rb);det=iv.det(e)
    require(det.a>0,'oriented nonsingular coframe')
    q=m.operands(rb)
    require(q[0].real.a>0 and q[2].real.b<0,'two genuinely nonzero curvature contractions')
    v0=(ps[1][0]-ps[0][0])/m.h
    require(abs(v0).a>0 and m.amp.a>0,'independent rank-two CAR currents')
    require((H[0,0]-C*radius).a>0 and (H[5,5]+C*radius).b<0,'two opposite Hessian signs throughout root ball')
    B=m.bands(rb)
    require(all(v.real.a>0 and v.real.b<1 for v in B),'full spectrum in (0,1)')
    Z=2*m.mult*sum(iv.exp(-m.beta*v) for v in B)
    theta=2/Z
    # Extended thermal Hessian is positive; Schur complement is certified H.
    theta_hessian=6/(m.beta*theta**2)
    require(theta_hessian.real.a>0,'unique global thermal stationary extension')
    old=json.loads((ROOT/'inputs/center_new.json').read_text())['z42']
    distance=max(abs(mp.mpf(a)-mp.mpf(bb)) for a,bb in zip(center,old))
    result={
      'status':'PASS_INTERVAL_FULL42_PAIRED_SPECTRAL_ROOT_AND43_THERMAL_LIFT',
      'source_snapshot':'4f5eec1632b0d1308d192ab7ae428f7532e2153b',
      'original_model_git_blob':original_blob,
      'dimension':N,'thermal_extension_dimension':N+1,
      'price':'6*((log(2*528*sum_four_bands(exp(-beta*f))))/beta-528*sum_four_bands(log(1-zeta*f)))',
      'beta':'2*phi^-2','zeta':'2^-20','band_multiplicity':528,'fixed_thermal_trace':0,
      'active_F_dimension':2112,'paired_Hodge_dimension':4224,
      'real_radius':s(up(radius)), 'complex_radius':s(up(R)), 'analytic_modulus_upper':s(up(abs(valuebox))),
      'analytic_majorant':100,'complex_step':'1e-35',
      'gradient_complex_step_error_upper':s(up(gerr)),
      'hessian_complex_step_error_upper':s(up(herr)),
      'A_norm_upper':s(up(anorm)),
      'inverse_defect_upper':s(up(defect)),
      'preconditioned_residual_upper':s(up(alpha)),
      'gradient_inf_upper':s(up(nrm(g))),
      'hessian_lipschitz_bound':s(up(C)),
      'contraction_upper':s(up(b)),
      'self_map_bound':s(up(alpha+b*radius)),
      'root_distance_from_center_upper':s(up(alpha/(1-b))),
      'shift_from_original_CQ_center':s(distance),
      'coframe_det_bounds':[s(down(det)),s(up(det))],
      'operand_bounds':[[s(down(v.real)),s(up(v.real))] for v in q],
      'hessian_diagonal_bounds':{'0':[s(down(H[0,0])),s(up(H[0,0]))],'5':[s(down(H[5,5])),s(up(H[5,5]))]},
      'thermal_theta_bounds':[s(down(theta.real)),s(up(theta.real))],
      'unique_full42_root_in_declared_ball':True,
      'nonflat':True,'saddle':True,'rank_two_CAR_currents':True,
      'complete_physical_apparatus_stationarity':False,
      'compulsory_Book03_scene_Hodge_identified':False,
      'GR_closed':False,
      'precision_decimal_digits':140,
      'hessian_entries_certified':1764,
      'distinct_action_evaluations_for_center_derivatives':904,
      'framework':'mpmath.iv outward interval arithmetic + analytic Cauchy bounds + Banach; not Lean or independent proof assistant'}
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
