#!/usr/bin/env python3
"""Pinned original N1 full-geometry Routh/Schur numerical application.

Consumes the existing rank-two theorem. This is NOT an interval certificate.
Run from a repository checkout or pass --source-dir. --root-json replays a
saved root without repeating its nonlinear solve; all original rows are checked.
"""
import argparse,hashlib,sys,time,json
from pathlib import Path
import numpy as np
from scipy.linalg import expm,svdvals
from scipy.optimize import least_squares
from scipy.optimize._numdiff import approx_derivative
SOURCE_REL=Path('02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21')
PINS={
 'check_full42_temporal_gauge_deflation.py':'3a0915231e9700aefa35335584c51f53dd2292e6',
 'check_full42_n1_single_internal.py':'da83e40379867f71b598fecd8430444ea027a4da',
 'full_n1_euler_analytic.py':'7ea28c981826c96b01bbdda67a92010dc7221095',
 'check_star_rank2_seam.py':'a57f0e3e845290923c2ac88d39ba5c08af4f6fd6',
 'check_diagonal_coframe_cauchy_recurrence.py':'487705f27a32ca1ee65348c5ddb2e4f4d32f5b55',
 '../d0_weighted_two_field_rank2_2026-10-21/native_master.py':'525b257ec671500bd02c4791f9579dbde2439f21'}
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--source-dir',type=Path)
ap.add_argument('--intervals',type=int,choices=(3,4,5),default=4)
ap.add_argument('--pf',help='Comma-separated positive fixed time weights; default all ones.')
inp=ap.add_mutually_exclusive_group()
inp.add_argument('--root-json',type=Path,help='Replay provenance-bearing UTF-8 root file.')
inp.add_argument('--saved-root',type=Path,help='Legacy x-only .npz root, rechecked against all original rows.')
ap.add_argument('--save-root-json',type=Path)
ap.add_argument('--root-only',action='store_true',help='Validate root without recomputing Hessians.')
ap.add_argument('--max-nfev',type=int,default=90)
ap.add_argument('--steps',type=float,nargs=2,default=(5e-6,2e-6))
ap.add_argument('--json',type=Path)
ap.add_argument('--matrix-npz',type=Path)
args=ap.parse_args()
src=args.source_dir.resolve() if args.source_dir is not None else None
if src is None:
    for candidate in (Path.cwd(),*Path(__file__).resolve().parents):
        if (candidate/SOURCE_REL/'full_n1_euler_analytic.py').is_file():
            src=candidate/SOURCE_REL;break
if src is None:ap.error('Cannot find original owner: pass --source-dir PATH.')
for relative,expected in PINS.items():
    data=(src/relative).read_bytes()
    got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if got!=expected:raise AssertionError(('changed scientific input',relative,got,expected))
sys.path.insert(0,str(src))
from check_full42_temporal_gauge_deflation import source_problem,checkpins
from full_n1_euler_analytic import full_source
from check_star_rank2_seam import LORENTZ as L,ETA

n=args.intervals
weights=[1.]*n if args.pf is None else [float(x) for x in args.pf.split(',')]
if len(weights)!=n or min(weights)<=0 or not np.all(np.isfinite(weights)):
    ap.error('One finite strictly positive PF weight per interval required.')
if min(args.steps)<=0 or args.steps[0]==args.steps[1] or not np.all(np.isfinite(args.steps)):
    ap.error('Two distinct finite positive difference steps required.')
start=time.monotonic()
checkpins()
h,rhos,fields,expand,residual,active,dropped=source_problem(n,weights)
print('starting actual original root',n,len(active),file=sys.stderr,flush=True)
root_mode='new_original_nonlinear_solve'
if args.root_json is not None:
    record=json.loads(args.root_json.read_text(encoding='utf-8'))
    if record['n']!=n or record['PF']!=weights or record['source_blobs']!=PINS:
        raise AssertionError('Saved root does not match intervals, weights, or source pins.')
    if abs(record['h']-h)>1e-14:raise AssertionError('Saved root uses a different original time mesh.')
    fitx=np.asarray(record['coordinates'],float);nfev=0
    root_mode='revalidated_saved_JSON_root'
elif args.saved_root is not None:
    with np.load(args.saved_root,allow_pickle=False) as archive:fitx=np.asarray(archive['x'],float)
    nfev=0;root_mode='revalidated_legacy_npz_root'
else:
    sol=least_squares(residual,np.zeros(len(active)),method='trf',x_scale='jac',max_nfev=args.max_nfev,xtol=1e-12,gtol=1e-12,ftol=1e-12)
    fitx=sol.x;nfev=sol.nfev
if fitx.shape!=(len(active),) or not np.all(np.isfinite(fitx)):
    raise AssertionError('Invalid root coordinate vector.')
full,s0,nodes=residual(fitx,True)
print('root',max(abs(full)),'nfev',nfev,'seconds',time.monotonic()-start,file=sys.stderr,flush=True)
assert max(abs(full))<5e-10
if args.save_root_json is not None:
    args.save_root_json.write_text(json.dumps(dict(format='d0-original-n1-gauge-root-v1',
      n=n,PF=weights,h=h,source_blobs=PINS,coordinates=fitx.tolist(),
      all_original_scaled_Euler_max=float(max(abs(full))),numeric_not_interval=True),indent=2)+'\n',encoding='utf-8')
ginds=np.array([i for i in active if i%42<40])
m=len(ginds); nv=2*n
assert m==34*n-28
def recenter(theta,vs):
    dst=[dict(e=x['e'].copy(),U=x['U'].copy(),v=x['v'].copy()) for x in nodes]
    zz=np.zeros(42*(n-1));zz[ginds]=theta
    for j in range(1,n):
        z=zz[42*(j-1):42*j]
        dst[j]['e']+=z[:16].reshape(4,4)
        for a in range(4):
            if np.any(z[16+6*a:22+6*a]):
                A=sum(z[16+6*a+k]*L[k] for k in range(6))
                dst[j]['U'][a]=expm(h*A)@nodes[j]['U'][a]
    for j in range(n):dst[j]['v'][:,0]+=vs[2*j:2*j+2]
    return dst
def joint_source(z):
    dn=recenter(z[:m],z[m:]);s=full_source(dn,h,rhos,.05)
    allgeo=np.concatenate([np.r_[s['e'][j].ravel(),(h*s['U'][j]).ravel(),0.,0.] for j in range(1,n)])
    vs=[]
    for j in range(n):
        gg=np.linalg.inv(dn[j]['e'].T@ETA@dn[j]['e'])
        vs.extend(2*s['v'][j]*(gg@dn[j]['v'].T)[0,:])
    return np.r_[allgeo[ginds],vs]
z0=np.zeros(m+nv)
j0=joint_source(z0)
D=np.zeros((2*n,2*(n-1)))
for j in range(n):
    for a in range(2):
        if j+1<n:D[2*j+a,2*j+a]+=1/h
        if j>0:D[2*j+a,2*(j-1)+a]-=1/h
N=np.tile(np.eye(2),(n,1))
assert np.max(abs(D.T@N))<1e-12
true_scalar=D.T@j0[m:]
scalar_full=np.concatenate([s0['psi'][j] for j in range(1,n)])
assert max(abs(true_scalar-scalar_full))<1e-11
if args.root_only:
    result=dict(status='NUMERICAL_SAVED_ROOT_ALL_ORIGINAL_ROWS_REVALIDATED',n=n,h=h,PF=weights,
      source_blobs=PINS,root_mode=root_mode,full_original_rows=42*(n-1),gauge_reduced_rows=len(active),
      root_full_scaled_Euler_max=float(max(abs(full))),
      root_omitted_scaled_Euler_max=float(max(abs(full[dropped]))) if len(dropped) else 0.,
      root_true_scalar_price_Euler_max=float(max(abs(true_scalar))),
      numeric_not_interval=True,GR_closed=False,wall_seconds=time.monotonic()-start)
    rendered=json.dumps(result,indent=2)+'\n'
    if args.json is not None:args.json.write_text(rendered,encoding='utf-8')
    print(rendered,end='');sys.exit(0)

def spectrum(a):
    ev=np.linalg.eigvalsh((a+a.T)/2)
    return {'min_eigen':float(ev[0]),'max_eigen':float(ev[-1]),'min_abs_eigen':float(min(abs(ev))),'negative':int((ev<-1e-7).sum()),'positive':int((ev>1e-7).sum()),'near_zero':int((abs(ev)<=1e-7).sum())}
def analyze(step):
    t=time.monotonic()
    raw=approx_derivative(joint_source,z0,method='3-point',abs_step=step)
    rawsym=float(np.max(abs(raw-raw.T)))
    H=(raw+raw.T)/2
    P=H[:m,:m];Q=H[:m,m:];W=H[m:,m:]
    Wi=np.linalg.inv(W)
    Klocal=P-Q@Wi@Q.T
    B=Q@Wi@N
    K=N.T@Wi@N
    Heff=Klocal+B@np.linalg.solve(K,B.T)
    direct=P-(Q@D)@np.linalg.solve(D.T@W@D,D.T@Q.T)
    blocks=[34]*(n-2)+[40]
    offsets=np.r_[0,np.cumsum(blocks)]
    distant=[]
    for i in range(len(blocks)):
        for j in range(len(blocks)):
            if abs(i-j)>1:distant.append(np.max(abs(Klocal[offsets[i]:offsets[i+1],offsets[j]:offsets[j+1]])))
    pivots=[];prev=None
    for i in range(len(blocks)):
        sl=slice(offsets[i],offsets[i+1]);pivot=Klocal[sl,sl].copy()
        if i:
            old=slice(offsets[i-1],offsets[i]);cross=Klocal[sl,old]
            pivot-=cross@np.linalg.solve(prev,cross.T)
        pivots.append(spectrum(pivot));prev=pivot
    border=K+B.T@np.linalg.solve(Klocal,B)
    inv_wood=np.linalg.inv(Klocal)-np.linalg.solve(Klocal,B)@np.linalg.solve(border,B.T@np.linalg.inv(Klocal))
    inverse_res=float(np.max(abs(Heff@inv_wood-np.eye(m))))
    ans={'step':step,'max_raw_hessian_asymmetry':rawsym,'W':spectrum(W),'Klocal':spectrum(Klocal),'geometric_blocks':blocks,'block_pivots':pivots,'nonneighbor_Klocal_max':float(max(distant)) if distant else 0.,'B_singular_values':[float(x) for x in svdvals(B)],'current_K':K.tolist(),'border_2x2':border.tolist(),'border_spectrum':spectrum(border),'Heff':spectrum(Heff),'schur_identity_max':float(np.max(abs(Heff-direct))),'woodbury_inverse_residual_max':inverse_res,'wall_seconds':time.monotonic()-t}
    return ans,H,Heff
r1,H1,E1=analyze(args.steps[0])
print('actual Hessian first pass',json.dumps(r1),file=sys.stderr,flush=True)
r2,H2,E2=analyze(args.steps[1])
out={'status':'NUMERICAL_ACTUAL_ORIGINAL_N1_ALL_GEOMETRY_TWO_CAR_BORDER','n':n,'h':h,'PF':weights,'full_original_rows':42*(n-1),'gauge_reduced_rows':len(active),'geometric_rows':m,'root_full_scaled_Euler_max':float(max(abs(full))),'root_true_scalar_price_Euler_max':float(max(abs(true_scalar))),'root_geometric_Euler_max':float(max(abs(j0[:m]))),'max_root_update':float(max(abs(fitx))),'source_f':s0['f'].tolist(),'source_q':s0['q'].tolist(),'nfev':int(nfev),'passes':[r1,r2],'hessian_step_change_max':float(np.max(abs(H1-H2))),'effective_hessian_step_change_max':float(np.max(abs(E1-E2))),'source_notes':['Original all40 coframe/Lorentz curvature chain retained; no independent f,k substitute.','Fresh left exp(h delta X)Ustar chart at actual root.','Scalar price gradient is psi, not h psi; velocity constraint D includes 1/h.','One fixed normalized N1 CQ price; full physical Book03 and uniform continuum not asserted.'],'numeric_not_interval':True,'GR_closed':False,'wall_seconds':time.monotonic()-start}
out.update(source_blobs=PINS,root_mode=root_mode,
    root_omitted_scaled_Euler_max=float(max(abs(full[dropped]))) if len(dropped) else 0.)
out['source_notes'].append('W is the actual velocity Hessian, twice the parent flux Hessian; the 2x2 border is half its G2.')
if args.json is not None:args.json.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
if args.matrix_npz is not None:
    np.savez(args.matrix_npz,H_step1=H1,H_step2=H2,Heff_step1=E1,Heff_step2=E2,
             D=D,N=N,geometric_indices=ginds,root_coordinates=fitx)
print(json.dumps(out,indent=2),flush=True)
