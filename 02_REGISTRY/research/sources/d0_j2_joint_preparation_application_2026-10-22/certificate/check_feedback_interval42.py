#!/usr/bin/env python3
"""Outward interval existence certificate for the NEW literal addressed J2 endpoint.

Consumes the unchanged original CQ field/report code, rational collar and the
new rational-decimal root proposal. No old root certificate is replayed. The
endpoint price is exactly aJ[-528 sum_j log(1-r_j)] plus a field constant, with
the derived fixed nonzero original-null normalization aJ. A is arbitrary exact
decimal rational data from a numerical inverse; validity is proved only by the
complete outward bound ||I-A H||<1. Every 16+24+2 row is retained.
"""
from __future__ import annotations
from pathlib import Path
from decimal import Decimal, getcontext
from concurrent.futures import ProcessPoolExecutor, as_completed
import argparse, hashlib, json, sys, time
sys.dont_write_bytecode=True
from mpmath import iv
from certified_feedback import Feedback,ORIGINAL_MODEL,ORIGINAL_INPUTS

HERE=Path(__file__).resolve().parent
PINS={'certified_model_original.py':'6d5b41ce11a941fde95e722e708ebb02d689985c',
      'inputs.py':'2c12d84fb3454dbf3cda6d71852d0cd4e57e1f65'}
N=42
def require(condition, message="certificate predicate failed"):
    if not condition:
        raise AssertionError(message)
def gitblob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def verify_inputs():
    paths={'certified_model_original.py':ORIGINAL_MODEL,'inputs.py':ORIGINAL_INPUTS}
    for name,pin in PINS.items():
        require(gitblob(paths[name].read_bytes()) == pin, (name, pin))

def init_worker(center,digits,M,R):
    global MODEL,Z,SBASE,MARGIN,DJ
    iv.dps=digits;getcontext().prec=digits+30
    MODEL=Feedback(iv);Z=[iv.mpf(v) for v in center]
    SBASE=MODEL.price(Z).real
    DJ=iv.mpf('1e-19')
    MARGIN=iv.mpf(str(4*Decimal(M)*Decimal('1e-19')**2/Decimal(R)**4))
def price_shift(i,j=None,sign=1):
    v=Z.copy();v[i]=iv.mpc(v[i],DJ)
    if j is not None:v[j]=iv.mpc(v[j],DJ*sign)
    return MODEL.price(v).real
def row_task(i):
    diag=-2*(price_shift(i)-SBASE)/(DJ*DJ)+iv.mpf([-1,1])*MARGIN
    out=[(i,i,diag._mpi_)]
    for j in range(i+1,N):
        v=-(price_shift(i,j,1)-price_shift(i,j,-1))/(2*DJ*DJ)
        v+=iv.mpf([-1,1])*MARGIN
        out.append((i,j,v._mpi_))
    return out
def iv_from_raw(raw):
    out=iv.mpf(0);out._mpi_=raw;return out
def boundstr(x):
    return str(x)

def audit_saved(args):
    """Read-only matrix/ball arithmetic audit; no expensive Hessian replay.

    The saved binary interval endpoints are tied to the published inertia
    receipt by SHA256. Their derivation is the separately executed full run.
    This audit recomputes the preconditioned defect, Banach bounds and actual
    geometric protection, and never rewrites any scientific artifact.
    """
    verify_inputs();getcontext().prec=160;iv.dps=args.digits
    receipt=json.loads(args.output.read_text())
    inertia=json.loads((HERE/'J2_INERTIA_RESULT.json').read_text())
    rawbytes=(HERE/'J2_INTERVAL_HESSIAN_ENDPOINTS.json').read_bytes()
    require(hashlib.sha256(rawbytes).hexdigest() == inertia['interval_Hessian_sha256'])
    require(hashlib.sha256(args.center.read_bytes()).hexdigest() == receipt['rational_new_center_sha256'])
    raw=json.loads(rawbytes)
    H=[[iv_from_raw(tuple(tuple(t) for t in x)) for x in row] for row in raw]
    Ar=json.loads((HERE/'J2_RATIONAL_PRECONDITIONER.json').read_text())['entries']
    Ai=[[iv.mpf(x) for x in row] for row in Ar]
    Anorm=max(sum(abs(Decimal(x)) for x in row) for row in Ar)
    defect=iv.mpf(0)
    for i in range(N):
        rs=iv.mpf(0)
        for j in range(N):
            v=(iv.mpf(1) if i==j else iv.mpf(0))-sum(Ai[i][k]*H[k][j] for k in range(N))
            rs+=abs(v).b
        defect=max(defect,rs.b)
    R=Decimal(receipt['whole_complex_chart_radius']);M=Decimal(5)
    radius=Decimal(receipt['exact_root_ball_inf']);C=Decimal(N*N*48)*M/R**3
    q=defect+iv.mpf(str(Anorm*C*radius))
    ftext=receipt['center_first_source_inf_upper'].strip('[]').split(',')
    fmax=iv.mpf([s.strip() for s in ftext])
    drift=iv.mpf(str(Anorm))*fmax
    require(q < iv.mpf('.01') and drift < (1 - q) * iv.mpf(str(radius)))
    ztxt=json.loads(args.center.read_text())['z42'];model=Feedback(iv)
    b=[iv.mpf([str(Decimal(v)-radius),str(Decimal(v)+radius)]) for v in ztxt]
    e,U,ps=model.nodes(b)
    hol=U[1]*U[2]*(model.eta*U[1].T*model.eta)*(model.eta*U[2].T*model.eta)
    require(iv.det(e).a > iv.mpf('1.5') and hol[1, 2].real.a > iv.mpf('.002'))
    require(((ps[1][0] - ps[0][0]) / model.h).a > iv.mpf('.088') and model.amp.a > iv.mpf('.146'))
    require(model.aJ.b < 0)
    print(json.dumps({'status':'PASS_READ_ONLY_SAVED_INTERVAL_BANACH_AND_GEOMETRY_AUDIT',
      'Banach_contraction_inf':str(q),'center_drift_inf':str(drift),
      'full_Hessian_recomputed':False,'files_written':False,'GR_closed':False},indent=2))

def certify(args):
    verify_inputs();getcontext().prec=160;iv.dps=args.digits
    start=time.monotonic()
    cbytes=args.center.read_bytes();center=json.loads(cbytes)
    ztxt=center['z42'];require(len(ztxt) == N)
    model=Feedback(iv);z=[iv.mpf(v) for v in ztxt]
    R=Decimal('5e-5');M=Decimal(5);radius=Decimal('1e-30')
    box=[iv.mpc([str(Decimal(v)-R),str(Decimal(v)+R)],[str(-R),str(R)]) for v in ztxt]
    value=model.price(box);price_bound=abs(value).b
    require(price_bound < iv.mpf(str(M)), ('entire original complex field chart', price_bound))
    report_bounds=[]
    for r in model.last_clicks:
        require(r.real.a > iv.mpf('1e-6') and r.real.b < iv.mpf('1e-5'))
        require(abs(r).b < iv.mpf('1e-5'))
        report_bounds.append(str(r))
    print('PASS whole complex price |S_J|<5, R=5e-5; seconds',round(time.monotonic()-start,1),flush=True)

    # Real-analytic full first source, rigorous complex-step remainder.
    df=Decimal('1e-40');marginF=iv.mpf(str(2*M*df*df/R**3))
    F=[]
    for k in range(N):
        v=z.copy();v[k]=iv.mpc(v[k],iv.mpf(str(df)))
        F.append(model.price(v).imag/iv.mpf(str(df)))
    fmax=max(abs(v).b for v in F)+marginF
    require(fmax < iv.mpf('1e-55'), ('new rational center source', fmax))
    print('PASS new center complete42 source',fmax,'seconds',round(time.monotonic()-start,1),flush=True)

    # Arbitrary proposal A: exact decimal rationals, never trusted as inverse.
    afile=HERE/'J2_RATIONAL_PRECONDITIONER.json'
    require(afile.is_file(),'The published exact rational preconditioner is required')
    Ar=json.loads(afile.read_text())['entries']
    require(len(Ar) == N and all((len(row) == N for row in Ar)))
    Ai=[[iv.mpf(v) for v in row] for row in Ar]
    Anorm=max(sum(abs(Decimal(v)) for v in row) for row in Ar)

    # All symmetric Hessian entries from the same scalar, independently bounded.
    H=[[None]*N for _ in range(N)];completed=0
    with ProcessPoolExecutor(max_workers=args.workers,initializer=init_worker,
             initargs=(ztxt,args.digits,str(M),str(R))) as pool:
        futures=[pool.submit(row_task,i) for i in range(N)]
        for task in as_completed(futures):
            for i,j,raw in task.result():
                H[i][j]=H[j][i]=iv_from_raw(raw)
            completed+=1
            print('Hessian rows',completed,'/',N,'seconds',round(time.monotonic()-start,1),flush=True)
    defect=iv.mpf(0)
    for i in range(N):
        rs=iv.mpf(0)
        for j in range(N):
            v=(iv.mpf(1) if i==j else iv.mpf(0))-sum(Ai[i][k]*H[k][j] for k in range(N))
            rs+=abs(v).b
        defect=max(defect,rs.b)
    C=Decimal(N*N*48)*M/R**3
    shift=C*radius
    q=defect+iv.mpf(str(Anorm*shift))
    drift=iv.mpf(str(Anorm))*fmax
    require(q < iv.mpf('.01'), ('complete Banach contraction', q))
    require(drift < (1 - q) * iv.mpf(str(radius)), ('strict ball self-map', drift, q))

    # Protect the actual larger displacement to the new endpoint separately.
    realball=[iv.mpf([str(Decimal(v)-radius),str(Decimal(v)+radius)]) for v in ztxt]
    e,U,ps=model.nodes(realball)
    det=iv.det(e)
    hol=U[1]*U[2]*(model.eta*U[1].T*model.eta)*(model.eta*U[2].T*model.eta)
    dtpsi=(ps[1][0]-ps[0][0])/model.h
    require(det.a > iv.mpf('1.5'))
    require(hol[1, 2].real.a > iv.mpf('.002'))
    require(dtpsi.a > iv.mpf('.088') and model.amp.a > iv.mpf('.146'))
    entryshift=iv.mpf(str(Decimal(N*48)*M*radius/R**3))
    require(H[0][0].a - entryshift > iv.mpf(2))
    require(H[5][5].b + entryshift < iv.mpf('-.7'))

    # A rigorous check of the numerical saddle inertia uses a rationalized
    # congruence frame. A direct interval Sylvester/LDL cert can be appended;
    # here only invertibility and two opposite coordinate signs are certified.
    receipt={
      'status':'PASS_RIGOROUS_INTERVAL_ALL42_LITERAL_ADDRESSED_J2_NONFLAT_RANK2',
      'snapshot':'af6e7eb8952564d86ddbfe910eb5f41d4a1b4e4b',
      'pinned_original_blobs':PINS,
      'rational_new_center_sha256':hashlib.sha256(cbytes).hexdigest(),
      'literal_price':'J2=-528 sum_(j=0,1) log(1-r_j), original unpadded42 r_j',
      'comparison_scalar':'aJ J2 plus a field-independent constant',
      'fixed_nonzero_comparison_gain_aJ':str(model.aJ),
      'complete_independent_field_rows':42,
      'rational_preconditioner_norm_inf':str(Anorm),
      'whole_complex_chart_radius':str(R),
      'whole_scalar_absolute_upper':str(price_bound),
      'whole_report_enclosures':report_bounds,
      'all_Hessian_entries_outward_interval':N*N,
      'center_first_source_inf_upper':str(fmax),
      'near_inverse_defect_inf':str(defect),
      'Hessian_Lipschitz':str(C),
      'Hessian_Lipschitz_times_radius':str(shift),
      'Banach_contraction_inf':str(q),
      'center_drift_inf':str(drift),
      'exact_root_ball_inf':str(radius),
      'exact_root_exists_unique_on_ball':True,
      'coframe_det_lower':str(det.a),
      'spatial_holonomy_12_lower':str(hol[1,2].real.a),
      'first_scalar_time_gradient_lower':str(dtpsi.a),
      'second_scalar_spatial_gradient_lower':str(model.amp.a),
      'normalized_coframe_Hessian_positive_lower':str(H[0][0].a-entryshift),
      'normalized_coframe_Hessian_negative_upper':str(H[5][5].b+entryshift),
      'two_opposite_free_field_Hessian_signs_certified':True,
      'numerical_16_negative_26_positive_is_not_interval_certified_here':True,
      'all_independent_preparation_equations_requires_same_N1_section_composition':True,
      'full_Book03_heat_Info_work_selected':False,
      'GR_closed':False,
      'elapsed_seconds':time.monotonic()-start
    }
    # Full interval matrix frozen as exact binary endpoints for review/replay.
    interval_matrix=[[[list(q) for q in H[i][j]._mpi_] for j in range(N)] for i in range(N)]
    args.matrix_output.write_text(json.dumps(interval_matrix)+'\n')
    args.output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--center',type=Path,default=HERE/'J2_CENTER_HIGH_PRECISION.json')
    p.add_argument('--output',type=Path,help='Explicit new receipt path for --recompute')
    p.add_argument('--matrix-output',type=Path,help='Explicit new interval matrix path for --recompute')
    p.add_argument('--workers',type=int,default=8)
    p.add_argument('--digits',type=int,default=115)
    p.add_argument('--audit',action='store_true',help='Read-only audit of saved intervals; no expensive Hessian replay')
    p.add_argument('--recompute',action='store_true',help='Expensive full scalar/Hessian replay; requires explicit new output paths')
    args=p.parse_args()
    require(not(args.audit and args.recompute),'Choose audit or recompute')
    if args.recompute:
        require(args.output is not None and args.matrix_output is not None,'--recompute requires --output and --matrix-output')
        require(args.output.resolve()!=(HERE/'J2_INTERVAL_RESULT.json').resolve(),'Frozen receipt may not be overwritten')
        require(args.matrix_output.resolve()!=(HERE/'J2_INTERVAL_HESSIAN_ENDPOINTS.json').resolve(),'Frozen interval matrix may not be overwritten')
        certify(args)
    else:
        require(args.output is None and args.matrix_output is None,'Audit is read-only and accepts no output paths')
        args.output=HERE/'J2_INTERVAL_RESULT.json'
        audit_saved(args)
if __name__=='__main__':main()
