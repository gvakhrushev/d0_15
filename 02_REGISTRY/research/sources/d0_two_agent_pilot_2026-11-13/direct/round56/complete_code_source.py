#!/usr/bin/env python3
"""Apply the selected Book graph-price source to the regular paid family.

The four-slot full-skew source is analytic on a fixed layout. Existing
native finite comparisons cover only their declared catalogue. Neither
is a physical Cost-Info identification; the owner's 7fu correction applies.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round55'))
import regular_comparison_task as task
O = task.source.s.old.B
OWNER = D.parents[2]/'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
CLOCK = D.parents[2]/'sources/d0_retained_response_concentration_2026-10-28/GROWING_CLOCK_RU.md'


def bounds():
    """Rational envelopes; conditional on the pinned source/clock proofs."""
    family = task.FieldTask(task.FieldCentre()).family
    cfg = family.cfg
    upper = task.source.upper_inventory_and_error()
    sigma, step, gs, z = (F(1, 1 << k) for k in (80, 1700, 3208, 20))
    gradient = F(1, 1 << 3083)+F((1 << 25)*52, 1 << 32)
    hessian, rv = 1 << 25, 104
    eM = upper['full_canonical_compressed_error']
    eW = upper['replacement_error']
    eB = upper['full_SOURCE_DATA_fibre_prefix_error']
    eU = cfg['post_error']
    scalar = hessian*sigma*rv**2
    oscillation = gradient*sigma*rv+F(1, 2)*hessian*sigma**2*rv**2
    weight = F(3, 2)*F(1, 1 << 3061)*4*(1 << 15)*oscillation/sigma
    corner = F(3, 2)*eM/gs
    spread = 156*1748*sigma+2*eB
    tau = 2*gradient*rv+hessian*sigma*rv**2+eM/gs
    kernel = F(3, 4)*(tau*(2*spread**2+2*eW)+eW/gs)
    feedback = 52*(2*(scalar+weight+corner)+2*kernel+4*eU/gs)

    # Four actual pre-retention square stages, not four extra clock edges.
    # ||X_a||op <= 52 on the B109 raw unit ball, so sum <=208.
    # D >= 2^n 2^K; G16: |DH| <= 6||DT||_1/(359D).
    # Gamma > gamma0*p^K, (2p)^(-K) < 2^(-K/4).
    gamma0 = F(8, 3)*z*gs
    analytic_heat = F(6*208, 359)/gamma0*F(1, 1 << (cfg['K']//4))
    master = feedback+analytic_heat
    # Original beta=2p²<1. Bound beta by 1, never change its value.
    statistical = feedback+analytic_heat

    # This distinct bound applies to actual A55 native finite +/- rows.
    finite_heat = F(6*cfg['Nbase'], 359)/(step*gamma0)*F(1, 1 << (cfg['K']//4))
    native_stat_axis_l2 = F(1, 1 << 102)+104*finite_heat
    assert feedback < F(1, 1 << 34)
    assert analytic_heat < F(1, 1 << 40672)
    assert master < F(1, 1 << 34) and statistical < F(1, 1 << 34)
    assert finite_heat < F(1, 1 << 8139)
    assert native_stat_axis_l2 < F(1, 1 << 101)
    return {'feedback_full_raw_dual': feedback,
            'analytic_heat_full_raw_dual': analytic_heat,
            'master_full_raw_dual': master,
            'oriented_statistical_full_raw_dual': statistical,
            'finite_native_heat_per_axis': finite_heat,
            'finite_native_statistical_four_axis_l2': native_stat_axis_l2}


def section_packet(request):
    """Bind graph accounting to one finite request, without executing it."""
    bound_task = task.FieldTask(request.field)
    out = bound_task.packet(request)
    out.update({
        'source_scope': 'selected Book operator/statistical price on this actual finite graph',
        'beta': '2*p^2', 'z': '2^-20', 'p': 'phi^-1', 'ell': 'log(phi)',
        'heat_partition': 'Z_H=359*D+2*Tr_(33D) exp(-beta*Delta0)',
        'full_graded_heat_modes': '425*D',
        'return_partition': 'Z_J=det(I-z*Fhat)^(-1)',
        'proper_return_determinant': '1-z+z*C(request)^*C(request)',
        'determinant_power': -1,
        'master': 'B=log(Z_H)/beta+log(Z_J)',
        'statistical': 'A_stat=-(log(Z_H)+log(Z_J))/ell',
        'source_identity_fixed_beta': '-ell*dA_stat=dB-p^3*dH=dJ+beta*dH',
        'finite_pair_identity': '-ell*(A_plus-A_minus)=(B_plus-B_minus)-p^3*(H_plus-H_minus)',
        'actual_return_gain': 'Gamma(Y)=4*z*p^K*c_ref*g*sigma/(1-z+z*p^K*c0(Y)^2)',
        'statistical_gain': 'Gamma_stat=Gamma(Y)/ell; use -dA_stat/Gamma_stat',
        'comparison_normalization': 'same centre Gamma(Y) in both endpoints; no derivative of Gamma',
        'whole_physical_Cost_Info_identified': False,
        'scope_correction_owner': '7fu supersedes physical-C acceptance language in 7fs/7ft',
        'physical_C_closed': False, 'GR_closed': False})
    return out


def build():
    paths = [Path(__file__), OWNER, CLOCK,
             D/'round4/C_BINDING_AUDIT_RU.md',
             D/'round55/regular_comparison_task.py', D/'round55/RECEIPT.json',
             O/'round109/B109_FULL_CODE_SKEW_RECOVERY_RU.md',
             O/'round109/B109_FULL_SKEW_RECOVERY_CHECK.json']
    return {
        'status': 'REGULAR_FAMILY_SELECTED_FULL_CODE_SOURCE_WITH_ORIGINAL_STATISTICAL_ORIENTATION',
        'example_bound_request': section_packet(task.Request(task.FieldCentre())),
        'analytic_control_space': 'four independent real skew(CODE) slots; raw nonquotient norm B109',
        'analytic_target': 'DI_tau(Y) composed with ell(Pf)-ell(Qf)/2+ell(Qb)/2',
        'analytic_H_plus_J_and_oriented_statistical_error_lt': '2^-34',
        'analytic_heat_dual_error_lt': '2^-40672',
        'finite_native_MG2_statistical_four_axis_l2_error_lt': '2^-101',
        'native_finite_catalogue_equals_full_skew_space': False,
        'physical_iota_Vh_identified': False,
        'one_fixed_mesh_not_a_refining_limit': True,
        'physical_C_closed': False, 'GR_closed': False,
        'source_sha256': {str(p): sha256(p.read_bytes()).hexdigest() for p in paths}}


if __name__ == '__main__':
    bounds()
    result = build()
    (P/'COMPLETE_CODE_SOURCE_PLAN.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'])
