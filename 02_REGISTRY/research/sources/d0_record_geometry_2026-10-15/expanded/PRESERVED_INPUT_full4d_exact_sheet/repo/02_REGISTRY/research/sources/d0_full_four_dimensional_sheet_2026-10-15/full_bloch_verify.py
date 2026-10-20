"""Interval certification of ALL 6144 connection directions at the exact root.
Bloch blocks are a computational decomposition, not a frequency cutoff.
"""
from interval_check import *
from blas_bounds import complex_left_residual

class C:
 def __init__(self,r,i=0):self.r=r if isinstance(r,I) else I(r);self.i=i if isinstance(i,I) else I(i)
 def __add__(a,b):return C(a.r+b.r,a.i+b.i)
 def __sub__(a,b):return C(a.r-b.r,a.i-b.i)
 def __matmul__(a,b):return C(a.r@b.r-a.i@b.i,a.r@b.i+a.i@b.r)
 def bound(a):return np.nextafter(a.r.absup()+a.i.absup(),np.inf)

def assemble(bb,t,u):
 # Exact fourth roots of unity; multiplication is sign/swap only.
 R=I(np.zeros((384,384)));J=I(np.zeros((384,384)))
 for (i,j),mat in bb.items():
  k=(t*i+u*j)%4
  if k==0:R=R+mat
  if k==1:J=J+mat
  if k==2:R=R-mat
  if k==3:J=J-mat
 return C(R,J)

def run(write=False):
 a=np.asarray(json.load(open(ROOT/'center.json'))).reshape(16,24);rad=2.**-42
 H,bb=hessian_enclosure(a,rad,True)
 # Preconditioner is generated from midpoint, then frozen as exact dyadic data.
 from point_interval import residual_interval
 B=np.linalg.inv((H.l+H.h)/2);F=residual_interval(a)
 c=rowsup((I(np.eye(384))-I(B)@H).absup());disp=float((I(B)@F.reshape(384,1)).absup().max());image=float(np.nextafter(disp+np.nextafter(c*rad,np.inf),np.inf))
 if not (c<1 and image<rad):raise AssertionError('2D exact root not certified')
 root={'radius':rad,'contraction_upper':c,'displacement_upper':disp,'image_radius_upper':image,'variables':384,'all_connection_rows':6144,'test':'strict outward Banach enclosure'}
 print('EXACT ROOT',root,flush=True)
 blocks=[];total=0.;precs={}
 for t in range(4):
  for u in range(4):
   z=assemble(bb,t,u);mid=(z.r.l+z.r.h)/2+1j*(z.i.l+z.i.h)/2
   inv=np.linalg.inv(mid);Bz=C(inv.real,inv.imag);err=rowsup(complex_left_residual(inv.real,inv.imag,z.r,z.i))
   bn=rowsup(Bz.bound());norm=float(np.nextafter(bn/np.nextafter(1-err,-np.inf),np.inf));total=float(np.nextafter(total+norm,np.inf))
   print('BLOCH',t,u,'eta',err,'inverse norm bound',norm,flush=True)
   if not err<1:raise AssertionError('uncertified full-rank block')
   blocks.append({'q0':t,'q3':u,'rows':384,'defect_infinity_upper':err,'inverse_norm_upper':norm})
   precs[f'{t}_{u}_real']=inv.real;precs[f'{t}_{u}_imag']=inv.imag
 # Preconditioners are free dyadic witnesses, regenerated and validated per run.
 report={'status':'PASS_EXACT_TWO_COORDINATE_ROOT_AND_FULL_4D_NONDEGENERACY','root':root,'blocks':blocks,'full_connection_dimension':6144,'full_coframe_parameter_dimension':4096,'full_metric_parameter_dimension':2560,'full_inverse_infinity_upper':total,'mesh':4,'physical_GR_closed':False,'all_mesh_uniformity_claimed':False,'new_Lean_compilation':False,'interval_endpoint_aliasing_fixed':True}
 if write:json.dump(report,open(ROOT/'full_receipt.json','w'),indent=2)
 if not (len(blocks)==16 and total<2.**24):raise AssertionError('full-spectrum gate')
 print('FULL PASS',total)
 return report
if __name__=='__main__':run()
