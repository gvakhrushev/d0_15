"""RIGOROUS a posteriori Banach/Newton certificate for 42 native N=1 field sources
on an explicitly rational fixed geometric/matter collar.

The finite mathematical functional and equations are the inherited ORIGINAL
six-face STAR + complete N=1 Golden CQ, NOT the unproved compulsory Book03 action.

Proof method:
  - mpmath.iv directed interval evaluation of F(c) and complex box
  - Cauchy derivative bound for holomorphic F in 42 variables
  - interval complex-step Jacobian enclosure at rational center
  - check fixed-point map c-AF maps a compact 42-cube into itself
    and is a strict contraction; hence a unique exact zero exists.
"""
import json,math,time
from pathlib import Path
import numpy as np
from mpmath import mp,iv
from scipy.optimize._numdiff import approx_derivative
from rational_fixture import newproblem
import mp_euler as own
ROOT=Path(__file__).resolve().parent

iv.dps=90
own.mp=iv
own.I=iv.eye(4)
own.ETA=iv.diag([1,-1,-1,-1])
own.G2=[own.ETA[a,a]*own.ETA[b,b] for a,b in own.PAIRS]
own.STAR=iv.matrix(6)
for a,(b,s) in own.STARMAP.items():own.STAR[own.PAIRS.index(b),own.PAIRS.index(a)]=s
own.L=[]
for i in (1,2,3):
 X=iv.matrix(4);X[0,i]=X[i,0]=1;own.L.append(X)
for i,j in ((1,2),(1,3),(2,3)):
 X=iv.matrix(4);X[i,j]=1;X[j,i]=-1;own.L.append(X)
own.P=(iv.sqrt(5)-1)/2;own.Z=iv.mpf(1)/2**20;own.LP=iv.log(1/own.P)

def abs_upper(a):
 return max(abs(mp.mpf(a.a)),abs(mp.mpf(a.b)))
def sup_complex(a):
 return abs_upper(a.real)+abs_upper(a.imag)  # triangle safe upper bound

def interval_checks(c,h,base,R):
 z=[iv.mpc([v-R,v+R],[-R,R]) for v in c]
 source=own.eval_euler(z,h,base)
 M=max(sup_complex(u) for u in source)
 assert M<mp.mpf('0.001'), ('complex box source bound',M)
 nodes=own.fields(z,h,base)
 # All denominators and the two nontrivial original report logs
 chart=[]
 for j in range(2):
  e=nodes[j]['e'];Uj=nodes[j]['U'];Un=nodes[j+1]['U'];f=iv.mpc(0)
  for r,s in own.PAIRS:
   A=Uj[r]; B=Un[s] if r==0 else Uj[s]
   Pm=A*B*own.v_inv(A)*own.v_inv(Uj[s]);Rmat=(Pm-own.v_inv(Pm))/2
   u,v=[k for k in range(4) if k not in (r,s)]
   beta=own.wedge(e[:,u],e[:,v]);vR=own.vec_b(Rmat)
   weighted=iv.matrix(1,6)
   for k in range(6):weighted[0,k]=beta[k]*own.G2[k]
   f+= (own.SGNS[r,s]*weighted*own.STAR*vR)[0]/h**2
  g=e.T*own.ETA*e;g_inv=g**-1;qq=iv.mpc(0)
  for a in range(2):qq+=(nodes[j]['v'][a,:]*g_inv*nodes[j]['v'][a,:].T)[0]
  x=-iv.mpf('0.05')*f;y=iv.mpf('0.05')*qq
  E=own.P**2*(1+x);ell=4*E*(1-E);b=own.P-own.P**2*y;B=4*b*b*(1-b*b)
  A=ell+(1-ell)*B;rval=own.Z*(A+B)-own.Z*own.Z*A*B
  # Cauchy domain of log((1-r)/r) is the complex open right half-plane
  assert mp.mpf(rval.real.a)>0 and mp.mpf((1-rval).real.a)>0
  quot=(1-rval)/rval
  assert mp.mpf(quot.real.a)>0,('log branch',j,quot)
  assert mp.mpf(rval.real.b)<mp.mpf('0.01')
  chart.append({'time_cell':j,'max_f':mp.nstr(sup_complex(f),12),
                'max_q':mp.nstr(sup_complex(qq),12),
                'report_real_min':mp.nstr(mp.mpf(rval.real.a),18),
                'report_real_max':mp.nstr(mp.mpf(rval.real.b),18),
                'log_argument_real_min':mp.nstr(mp.mpf(quot.real.a),15)})
 return M,chart

def jac_interval(c,h,base,t):
 # Real-centered holomorphic complex-step derivative: imaginary coefficient
 # plus an independently proven Cauchy error (sup below).
 J=[]
 for j in range(42):
  z=[iv.mpc(v) for v in c]
  z[j]+=iv.mpc(0,t)
  src=own.eval_euler(z,h,base)
  J.append([a.imag/t for a in src])
 return [[J[j][i] for j in range(42)] for i in range(42)]

def run():
 start=time.perf_counter()
 data=json.loads((ROOT/'mp_center.json').read_text());c=[iv.mpf(s) for s in data['center']]
 h,base=own.build();R=iv.mpf('1e-7');Mbox,charts=interval_checks(c,h,base,R)
 # Upper bound |F_i| <= M on polydisc radius R. Allow extra margin.
 M=mp.mpf('0.001');r=mp.mpf('1e-30');tt=iv.mpf('1e-20')
 # Cauchy: complex-step imaginary derivative differs by <= M*t²/R³/(1-(t/R)²).
 rem=M*mp.mpf('1e-40')/mp.mpf('1e-21')/(1-mp.mpf('1e-26'))
 assert rem<mp.mpf('2e-22')
 _,_,float_euler=newproblem()
 x0=np.zeros(42);Jd=approx_derivative(float_euler,x0,method='3-point',abs_step=2e-6)
 Af=np.linalg.inv(Jd)
 # Fixed point inverse A has *exact decimal* coefficients in this certification.
 Ad=[[iv.mpf(format(float(Af[i,j]),'.17g')) for j in range(42)] for i in range(42)]
 A_abs_rows=[sum(abs_upper(q) for q in row) for row in Ad]
 A_norm=max(A_abs_rows)
 assert A_norm<31
 f0=own.eval_euler(c,h,base)
 f0_norm=max(sup_complex(a) for a in f0)
 assert f0_norm<mp.mpf('3e-60'), f0_norm
 print('center residual certified',mp.nstr(f0_norm,15),'analytic M rectangle',mp.nstr(Mbox,12),'at',round(time.perf_counter()-start,2),'s',flush=True)
 Jiv=jac_interval(c,h,base,tt)
 print("jiv complete",round(time.perf_counter()-start,2),flush=True)
 # Each interval complex-step derivative is enclosed by a 40-significant-digit
 # rational decimal with explicit global absolute error < 1e-11. The analytic
 # Cauchy remainder from finite step is < 2e-22 and is included.
 from decimal import Decimal,localcontext
 Jstr=[];maximum_err=mp.mpf(0)
 for i in range(42):
  line=[]
  for j in range(42):
   v=Jiv[i][j]
   mid=(mp.mpf(v.a)+mp.mpf(v.b))/2
   ss=mp.nstr(mid,40)
   err=abs_upper(v-iv.mpf(ss))+rem
   maximum_err=max(maximum_err,err)
   line.append(ss)
  Jstr.append(line)
 assert maximum_err<mp.mpf('1e-11'),maximum_err
 print("max err",mp.nstr(maximum_err,6),"t",round(time.perf_counter()-start,2),flush=True)
 # Matrix multiplication uses exact finite DECIMAL rational inputs. With
 # 80-digit Decimal precision, the sum of 42 products is far below the
 # conservative 1e-30 arithmetic allowance in the source units here.
 with localcontext() as ctx:
  ctx.prec=80
  exactA=[[Decimal(format(float(Af[i,j]),'.17g')) for j in range(42)] for i in range(42)]
  exactJ=[[Decimal(Jstr[i][j]) for j in range(42)] for i in range(42)]
  q_rows=[]
  for i in range(42):
   row=Decimal(0)
   for j in range(42):
    e=Decimal(int(i==j))-sum(exactA[i][k]*exactJ[k][j] for k in range(42))
    row+=abs(e)
   q_rows.append(row)
  qapprox=max(q_rows)
  q0=mp.mpf(str(qapprox))+A_norm*42*mp.mpf('1e-11')+mp.mpf('1e-25')
 assert q0<mp.mpf('0.001'),q0
 print('q0 done',mp.nstr(q0,8),round(time.perf_counter()-start,2),flush=True)
 # Universal Cauchy Hessian bound on interior half polydisc: 8 M/R².
 # Jacobian infinity distance from center <= 42² * 8M/R² * r.
 q_variation=A_norm*(42*42*8)*M/(mp.mpf('1e-7')**2)*r
 q_total=q0+q_variation
 eta=A_norm*f0_norm
 assert q_total<mp.mpf('0.001'),(q_total,q0,q_variation)
 assert eta<(1-q_total)*r
 # Real physical coframe signature and rank-two matter are open conditions.
 # At center they can be rechecked exactly via interval minors; strict margins are huge.
 result={
 'status':'PASS_RIGOROUS_INTERVAL_NEWTON_FULL42_RATIONAL_COLLAR',
 'configured_price':'original six based STAR faces plus SAME complete Golden cap-N1 CQ price; NOT compulsory Book03',
 'variables':42,'mesh_cells':2,'collar':'specified rational matrices/charges in rational_root_center.json',
 'root_center_file':'mp_center.json',
 'complex_polydisc_radius':mp.nstr(mp.mpf('1e-7'),10),
 'complex_sup_source_bound_used':mp.nstr(M,12),
 'actual_complex_box_source_bound':mp.nstr(Mbox,18),
 'full_complete_CQ_query_chart':charts,
 'rigorous_center_source_inf_bound':mp.nstr(f0_norm,18),
 'preconditioner_inf_bound':mp.nstr(A_norm,15),
 'center_J_preconditioner_error_bound':mp.nstr(q0,18),
 'cauchy_J_change_bound_on_cube':mp.nstr(q_variation,18),
 'newton_contraction':mp.nstr(q_total,18),
 'newton_cube_radius':mp.nstr(r,9),
 'newton_center_shift_bound':mp.nstr(eta,20),
 'unique_exact_zero_in_cube':True,
 'total_elapsed_seconds':round(time.perf_counter()-start,3),
 'scope':{'exact_full42_mathematical_stationary_root':True,
          'original_Cauchy_transcendental_boundary_preserved':False,
          'fixed_chosen_rational_collar':True,'same_original_N1_CQ_price':True,
          'full_nonuniform_site_PF':False,'general_spacetime_refinement':False,
          'compulsory_Book03_physical_source_selected':False,
          'GR_closed':False}}
 path=ROOT/'INTERVAL_CERTIFICATE.json';path.write_text(json.dumps(result,indent=2)+'\n')
 print('Q0',mp.nstr(q0,15),'Qvar',mp.nstr(q_variation,15),'total',mp.nstr(q_total,15),'ETA',mp.nstr(eta,15),'elapsed',result['total_elapsed_seconds'])
 print(json.dumps(result,indent=2))
 return result
if __name__=='__main__':run()
