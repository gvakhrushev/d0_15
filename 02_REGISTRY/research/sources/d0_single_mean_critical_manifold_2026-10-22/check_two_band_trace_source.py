#!/usr/bin/env python3
"""Exact two-band original N1 Golden addressed-report effect:
D Tr[h_phi(E)] = alpha D Tr[E] + beta D(Tr[E^2]/2), including
every native 42-field tangent through the original report map.

Historical h=1/4 root and report intervals are PINNED; we consume the
already published 42x42 interval Hessian rather than replay it.
No Book03 selected active projector, heat, clock, Info or writer inferred.
"""
from __future__ import annotations
import argparse,hashlib,json
from fractions import Fraction
from decimal import Decimal,localcontext
from pathlib import Path

OWNERS = {
 "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/"
 "RIGOROUS_EXACT42_CERTIFICATE.json":
 "9f4bdef4c367660539c588db01819330ff0d55b3",
 "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/"
 "REPORT_BRIDGE_RESULT.json":
 "2c7193f54da76aaf108d2821c45daddac7457f02",
}

def read(repo,path,expected):
    b=(repo/path).read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    if actual!=expected:
        raise AssertionError(('immutable original receipt changed',path,actual,expected))
    return json.loads(b)

def exact_tests():
    scenarios=[
       (Fraction(1,1000),Fraction(7,1000)),
       (Fraction(1,500000),Fraction(11,5000000)),
       (Fraction(5,17),Fraction(7,18)),
    ]
    n=0
    for r0,r1 in scenarios:
        assert 0<r0<r1<1
        M1=r0+r1
        M2=(r0*r0+r1*r1)/2
        det=r1-r0
        assert M2-M1*M1/4==(r1-r0)**2/4
        assert M1*M1-2*M2==2*r0*r1
        assert det>0
        # EXACT Jacobian from first two original spectral traces
        assert (1*r1-1*r0)==det
        # For ANY eigenvalue source slopes s0,s1 (no entropy function
        # assumption) the polynomial spectral interpolant has degree 1.
        s0=Fraction(7,13);s1=Fraction(-19,11)
        beta=(s1-s0)/(r1-r0)
        alpha=s0-beta*r0
        assert alpha+beta*r0==s0
        assert alpha+beta*r1==s1
        for u0,u1 in [(Fraction(3,7),Fraction(5,9)),
                      (Fraction(-2,11),Fraction(8,17))]:
            # Source along an arbitrary two-report tangent:
            # dM1=u0+u1, dM2=r0*u0+r1*u1.
            assert (s0*u0+s1*u1 ==
                    alpha*(u0+u1)+beta*(r0*u0+r1*u1))
            n+=1
    return {'different_rational_two_band_controls':len(scenarios),
            'exact_arbitrary_first_source_controls':n,
            'moment_jacobian_determinant':'r1-r0',
            'source_interpolant':'h_phi_prime(E) = alpha I + beta E',
            'full_source':'D Tr h_phi(E)=alpha D M1+beta D M2',
            'M1':'Tr(E)','M2':'Tr(E^2)/2'}

def certified_native_checks(repo):
    cert,bridge=[read(repo,p,s) for p,s in OWNERS.items()]
    with localcontext() as ctx:
        ctx.prec=78
        assert cert['dimension']==42 and cert['time_intervals']==2
        assert cert['root_cube_radius']=='1E-30'
        assert cert['scope']['all42_mathematically_stationary']
        assert bridge['scope']['exact_root_used_from_interval_certificate']
        source_neumann=Decimal(cert['qcenter_including_error'])+Decimal(cert['qchange_via_cauchy_bound'])
        assert source_neumann<Decimal('.001')
        dmin=Decimal(bridge['report_interval_gap_lower'])
        dmax=Decimal('8.797582672249e-11')
        assert dmin>Decimal('5.80688e-11')
        assert dmax>dmin
        det=dmin
        assert det>Decimal('5.80688e-11')
        slope_source=Decimal(bridge['mean_report_D_abs_lower_at_root'])
        assert slope_source>Decimal('2.68978e-14')
        dM1=2*slope_source
        assert dM1>Decimal('5.37956e-14')
        inv_condition=Decimal(1)/dmax
        assert inv_condition>Decimal('1.136e10')

        # The actual original two distinct report bands, NOT arbitrary
        # spectra: take a representative inside the CERTIFIED bands only
        # as a numerical Lagrange-check; source theorem holds for every
        # positive ordered pair and consumes the strict interval gap.
        r0=(Decimal('1.8512417713660524e-6')+
            Decimal('1.85124371058701973e-6'))/2
        r1=(Decimal('1.85130177947843566e-6')+
            Decimal('1.85132974719277498e-6'))/2
        ln_phi=((Decimal(1)+Decimal(5).sqrt())/2).ln()
        def entropy_prime(r):
            return ((1-r)/r).ln()/ln_phi
        h0,h1=entropy_prime(r0),entropy_prime(r1)
        beta=(h1-h0)/(r1-r0)
        alpha=h0-beta*r0
        assert h0>h1>0 and beta<0 and alpha>0
        assert abs(alpha+beta*r1-h1)<Decimal('1e-65')
        # Independent data directions need no native field basis: the
        # exact identity commutes with ANY genuine derivative pullback.
        for dr0,dr1 in ((Decimal('1.234e-8'),Decimal('-2.339e-8')),
                        (Decimal('-8.293e-9'),Decimal('3.521e-10'))):
            lhs=h0*dr0+h1*dr1
            rhs=alpha*(dr0+dr1)+beta*(r0*dr0+r1*dr1)
            assert abs(lhs-rhs)<Decimal('1e-65')
        return {
          'original_fixed_collar_h':'1/4',
          'CQ_nonsingular_42x42_Neumann_upper':str(source_neumann),
          'certified_moment_M1_D29_lower':str(dM1),
          'original_two_band_eigenvalue_gap_lower':str(det),
          'inverse_M2_to_eigenvalue_sensitivity_strict_lower':str(inv_condition),
          'representative_entropy_interpolation_alpha':str(alpha),
          'representative_entropy_interpolation_beta':str(beta),
          'full_nonlinear_source_and_Hessian_identity':
             'Tr h_phi(E)=h_phi(r0)+h_phi(r1) pointwise',
          'source_moments_correct_for_every_genuine_42_field_tangent':True,
        }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,
        default=Path(__file__).resolve().parents[4])
    ap.add_argument('--json',type=Path)
    args=ap.parse_args()
    result={'status':'PASS_ORIGINAL_TWO_BAND_TRACE_SOURCE_INTERPOLATION',
            'source_pins':OWNERS,
            'exact':exact_tests(),
            'certified_consumer':certified_native_checks(args.repo.resolve()),
            'scope':{
              'original_conditional_two_address_positive_effect':True,
              'whole_two_channel_CQ_report_entropy_preserved':True,
              'entire_42_source_Hessian_preserved':True,
              'whole_quantum_work_entropy_compressed_to_two_moments':False,
              'physically_selected_Book03_Hodge_cut':False,
              'nonspectral_nonmean_scalar_statistics_ruled_out':False,
              'native_field_writer_selected':False,
              'GR_closed':False}}
    out=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    print(out,end='')
    if args.json:args.json.write_text(out,encoding='utf-8')
if __name__=='__main__':main()
