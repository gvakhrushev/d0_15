#!/usr/bin/env python3
"""Original native N=1 full nonlinear F source, all six actual based G2STAR
faces, two independent CAR scalar gradients: exact temporal Lorentz Noether
Gauss-source transport on a homogeneous spatial stencil.

The exact theorem is algebraic; seven numerical all-operator tests check
the genuine original source derivative, not selected GR roots/Book03.
"""
import json,sys,hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import expm

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PINS={
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py":
    "a57f0e3e845290923c2ac88d39ba5c08af4f6fd6",
"02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py":
    "525b257ec671500bd02c4791f9579dbde2439f21"}
def pins():
    for path,expect in PINS.items():
        data=(ROOT/path).read_bytes()
        sha=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        if sha!=expect:raise AssertionError((path,sha,expect))

sys.path.insert(0,str(HERE))
sys.path.insert(0,str(ROOT/"02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21"))
from check_star_rank2_seam import star_density,matter_query,LORENTZ,ETA,I
from native_master import GoldenMaster
native=GoldenMaster(55)
TAU=.007
H=.087

def cell(rng):
    e=(np.eye(4)+rng.normal(0,.08,(4,4))).astype(complex)
    assert np.linalg.det(e).real>0
    U=np.array([expm(H*sum(rng.normal(0,.2)*Z for Z in LORENTZ))
                for _ in range(4)],dtype=complex)
    gradients=np.array([rng.normal(0,.015,4),rng.normal(0,.015,4)],dtype=complex)
    return dict(e=e,u=U,v=gradients)

def one(seed):
    rng=np.random.default_rng(seed)
    prev,cur,nxt=[cell(rng) for _ in range(3)]
    fprev=star_density(prev,cur,H)
    fcur=star_density(cur,nxt,H)
    qprev=matter_query(prev)
    qcur=matter_query(cur)
    rho_prev,rho_cur=1.,1.8
    # Same CURRENT real native GoldenMaster sigma-minus:
    # F_N(-TAU*f_canonical/rho, +TAU*q/rho);
    # do not replace it by a sigma-plus or an affine cost.
    cprev=-TAU*float(native.fx(-TAU*fprev.real/rho_prev,
                                  TAU*qprev.real/rho_prev))
    ccur=-TAU*float(native.fx(-TAU*fcur.real/rho_cur,
                                TAU*qcur.real/rho_cur))
    dcur=TAU*float(native.fy(-TAU*fcur.real/rho_cur,
                               TAU*qcur.real/rho_cur))
    imagstep=1e-20

    def first_source(actions):
        copies=[dict(e=v['e'].copy(),u=v['u'].copy(),v=v['v'].copy())
                for v in (prev,cur,nxt)]
        for time,slot,axis,variation in actions:
            if slot=="u":copies[time]['u'][axis]+=1j*imagstep*variation
            else:copies[time]['e']+=1j*imagstep*variation
        dp=star_density(copies[0],copies[1],H).imag/imagstep
        dc=star_density(copies[1],copies[2],H).imag/imagstep
        dq=matter_query(copies[1]).imag/imagstep
        return cprev*dp+ccur*dc+dcur*dq

    tests=[]
    for j,Z in enumerate(LORENTZ):
        eco=first_source([(1,"e",None,Z@cur['e'])])
        esp=first_source([(1,"u",i,Z@cur['u'][i]-cur['u'][i]@Z)
                           for i in (1,2,3)])
        gout=first_source([(1,"u",0,Z@cur['u'][0])])
        gin=first_source([(0,"u",0,-prev['u'][0]@Z)])
        err=eco+esp+gout+gin
        if abs(err)>2e-12:raise AssertionError((seed,j,err))
        tests.append(dict(generator=j,coframe=eco,spatial_links=esp,
                          outgoing_temporal=gout,incoming_temporal=gin,
                          exact_Ward_error=err))
    return dict(seed=seed,
                complete_native_source_weights=[cprev,ccur,dcur],
                all_six_Ward_max_error=max(abs(x["exact_Ward_error"]) for x in tests),
                actual_nonzero_temporal_Gauss=max(abs(x["outgoing_temporal"])
                                                  for x in tests),
                rows=tests)

def run():
    pins()
    cases=[one(i) for i in range(5,12)]
    maxerr=max(c["all_six_Ward_max_error"] for c in cases)
    nonzero=max(c["actual_nonzero_temporal_Gauss"] for c in cases)
    assert maxerr<2e-12 and nonzero>1e-9
    return dict(status="PASS_ORIGINAL_N1_GOLDEN_TEMPORAL_GAUSS_SOURCE",
      immutable_old_G2STAR_and_GoldenMaster_pins=True,
      seven_genuine_full4_fixtures=True,
      six_generator_checks_per_fixture=6,
      actual_nonlinear_same_price=True,
      largest_exact_Lorentz_Ward_residual=maxerr,
      largest_nonzero_temporal_Gauss=nonzero,
      consequence="all coframe/spatial-link Euler zero implies temporal Gauss covariantly constant; initial true Gauss zero is still required",
      cases=cases,
      scope=dict(physical_Book03_selected=False,
                 native_time_collars_admitted=False,
                 native_full42_finite_root=False,
                 whole4D_Book_stress_proved=False,GR_closed=False))

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
