#!/usr/bin/env python3
"""Owned MG2 full-vector lift and actual two-bit G/CX control words.

This implements the new CODE controls, not the recompiled two-bit SOURCE
catalogue. Existing A46 SOURCE words are explicitly incompatible with it.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from functools import lru_cache
from itertools import combinations
import json,hashlib,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round46'));import independent_current_bank as parent
old=parent.old;a41=old.a41;e=a41.e;native=old.native
M=2688;SIGMA=F(1,1<<80);STEP=F(1,1<<1700)


def inverse(x):
    """Exact inversion in Q(a), a^4+a^2-1=0, by rational elimination."""
    x=e.Q4(x);basis=[e.Q4(tuple(int(i==j) for i in range(4))) for j in range(4)]
    columns=[(x*b).v for b in basis]
    rows=[[columns[j][i] for j in range(4)]+[F(i==0)] for i in range(4)]
    for j in range(4):
        pivot=next(i for i in range(j,4) if rows[i][j])
        rows[j],rows[pivot]=rows[pivot],rows[j]
        scale=rows[j][j];rows[j]=[v/scale for v in rows[j]]
        for i in range(4):
            if i!=j:
                scale=rows[i][j];rows[i]=[a-scale*b for a,b in zip(rows[i],rows[j])]
    out=e.Q4(tuple(row[4] for row in rows));assert x*out==1
    return out


@lru_cache(None)
def mg2():
    p=e.SIN;a=e.A;phi=[p,a*p,a*p,p*p];probs=[x*x for x in phi]
    hs=[inverse(e.Q4(1)-2*x) for x in probs];S=sum((x*h for x,h in zip(probs,hs)),e.Q4())
    denominator=inverse(1+S);lambdas={}
    for i,j in combinations(range(4),2):
        lambdas[i,j]=phi[i]*phi[j]*(hs[i]+hs[j])*denominator*F(1,j-i)
    return phi,probs,lambdas


def coefficients_json(x):return [[str(v.numerator),str(v.denominator)] for v in x.v]


def interval_mul_rat(interval,f,ctx):return ctx.mul(interval,ctx.rat(f.numerator,f.denominator))


def angle_certificate(lam,sign):
    """Select a positive Golden power and separately certify its grid cell.

    The half-plane target is atan(z), z=sign*t*lambda/4. Thus a two-bit
    zero-Walsh star targets the full Cayley rotation of angle 2 atan(z).
    """
    assert sign in (-1,1)
    z=lam*(sign*STEP/4);den=e.root(e.expr(1+z*z))
    c=e.expr(1)/den;s=e.expr(z)/den
    k=a41.select_positive_power(c,s)
    pn,q,cert=a41.uniform_grid();bits=20480;ctx=e.Dyadic(bits)
    lo,hi=ctx.evaluate((e.expr(z),))[0]
    angle=(a41.atan_signed(ctx,lo)[0],a41.atan_signed(ctx,hi)[1])
    pb=cert['precision_bits'];assert pb>=bits
    pi=[int(v,16) for v in cert['pi_interval_hex']];shift=pb-bits
    pi=(pi[0]>>shift,-((-pi[1])>>shift))
    tau=ctx.div(angle,(2*pi[0],2*pi[1]))
    j=(q*(tau[0]+tau[1])+ctx.S)//(2*ctx.S)
    assert 1<=k<=q and (k*pn-j)%q==0
    err=int(cert['abs_qgamma_minus_numerator_bound_numerator_hex'],16)
    cell=max(abs(j*ctx.S-q*tau[0]),abs(j*ctx.S-q*tau[1]))
    # 2 pi < 7. Includes full target interval and actual q*gamma-pn error.
    error=7*(F(cell,q*ctx.S)+F(k*err,q*(1<<pb)))
    assert error<F(1,1<<20075)
    return {'k_hex':hex(k),'signed_grid_index_hex':hex(j),
      'target_turn_interval_hex':[hex(tau[0]),hex(tau[1])],'precision_bits':bits,
      'half_angle_error':old.encode(error),'half_angle_error_lt':'2^-20075'}


@lru_cache(None)
def angle_library():
    _,_,lam=mg2();out={}
    for pair,value in lam.items():
        out['%d_%d'%pair]={str(sign):angle_certificate(value,sign) for sign in (1,-1)}
    return out


def code_wires(index):
    assert type(index) is int and 0<=index<M
    n=parent.production_configuration()['n']
    # Keep all A46 addresses; append one actually new RAW bit per coordinate.
    return (2+index,n+index)


def plane_blocks(pair,k,wires,macros):
    """Both CODE columns per bit, arbitrary other factors, no clean helper."""
    a,b=pair;sam=tuple(wires);assert len(sam)==2
    pivot,ops=old.plane_affine(a,b,sam)
    def lower(op):
        if op[0]=='CX':return native.gate(*op)
        return macros.x(op[1],next(q for q in sam if q!=op[1]))
    for op in ops:yield lower(op)
    yield from a41.star_blocks(sam,1<<pivot,k)
    for op in reversed(ops):yield lower(op)


def raw_control_blocks(index,sign,library=None):
    assert sign in (-1,1)
    lib=angle_library() if library is None else library;macros=native.Macros()
    pairs=list(combinations(range(4),2))
    for pair in pairs+list(reversed(pairs)):
        k=int(lib['%d_%d'%pair][str(sign)]['k_hex'],16)
        yield from plane_blocks(pair,k,code_wires(index),macros)


def count_blocks(factory):
    counts=Counter()
    for t in factory():counts.update(native.counts(t))
    return counts


@lru_cache(None)
def control_inventory():
    counts={sign:count_blocks(lambda sign=sign:raw_control_blocks(0,sign)) for sign in (-1,1)}
    length=max(sum(c.values()) for c in counts.values())+4
    return counts,length


def control_blocks(index,sign=0):
    assert sign in (-1,0,1)
    counts,length=control_inventory();used=0
    if sign:
        yield from raw_control_blocks(index,sign);used=sum(counts[sign].values())
    pair=code_wires(index);third=2+(index+1)%M
    # An extra EXISTING CODE coordinate supports exact identity padding.
    # Its complete padding word is identity on all columns; its calls count.
    yield from old.padding(length-used,(*pair,third))


def source_derivative_enclosure():
    """Rational consequences of the proved continuous-chart slack bounds.

    The analytical derivation is in FULL_VECTOR_REPAIR_RU.md. No evaluation
    of the new SOURCE vertices or recompilation is hidden in this function.
    """
    U=F(17,16)
    link_C1=2*U**3*3;link_C2=2*U**3*7+6*U**2*9
    assert link_C1<8 and link_C2<80
    omega1=F(30*8,256);omega2=F(6*(5*80+68*64),256)
    assert omega1<1 and omega2<112
    choi1=F(3);choi2=F(338);car1=F(4);car2=F(12)
    M1=540*choi1+32*car1
    M2=540*choi2+32*car2+M1*M1-(540*choi1**2+32*car1**2)
    assert M1<1<<11 and M2<1<<22
    # Rv < 2 sqrt(2688) < 104; do not replace it by 1.
    assert 4*M<104**2
    value=SIGMA*104*M1;jet=SIGMA*104**2*M2
    assert value<F(1,1<<62) and jet<F(1,1<<44)
    return {'link_contraction_first':link_C1,'link_contraction_second':link_C2,
      'one_Choi_vector_first':omega1,'one_Choi_vector_second':omega2,
      'full_bank_M1':M1,'full_bank_M2':M2,
      'two_bit_ideal_value_error':value,'two_bit_ideal_axis_jet_error':jet}


def build():
    phi,probs,lam=mg2();lib=angle_library();counts,length=control_inventory()
    L=F(3,2);delta=F(1,1<<20000)
    error=F(17,48)*L**3*STEP**3+504*delta
    assert error<F(1,1<<5099)
    # Proposed stricter SOURCE/corner budgets are obligations, NOT receipts.
    eB_required=F(1,1<<3300);eM_required=F(1,1<<3298);gs_lower=F(1,1<<3208)
    assert eM_required/gs_lower<F(1,1<<89)
    native_jet=2*eB_required*(L+504*delta/STEP)/SIGMA
    assert native_jet<F(1,1<<3218)
    # The two ACTUAL G/CX controls are not exact inverses. Charge their
    # mismatch directly, including the constant target, at the true sigma*t
    # divisor. Do not apply MG11's exact-inverse cancellation to these words.
    derivatives=source_derivative_enclosure()
    finite_extra=(eB_required+2*error)/(SIGMA*STEP)+F(4,3)*104*derivatives['full_bank_M1']*STEP**2
    finite_jet=derivatives['two_bit_ideal_axis_jet_error']+finite_extra
    assert finite_extra<F(1,1<<1519) and finite_jet<F(1,1<<44)
    pins=[Path(__file__),D/'round46/RESULT.json',D/'round46/independent_current_bank.py',
      D/'round22/full_choi_bank.py',D/'round24/full_car_source.py',
      D/'round38/gcx_post_macros.py',D/'round38/POST_ANGLE_CERTIFICATE.json',
      D/'round41/exact_target.py',D/'round41/sam_only_compiler.py',a41.CERT,
      D/'round22/FULL_RAW_CHOI_RU.md',D/'round24/FULL_CAR_SOURCE_RU.md',
      parent.B/'round21/CHART_ENVELOPE_RESULT.json',parent.B/'round25/targets.py',
      parent.B/'round45/SITE_NATIVE_RU.md',
      parent.B/'round65/B65_CENTRE_SOURCE_AND_BOUNDS_RU.md',
      parent.B/'round65/SCALAR_HESSIAN_ENVELOPE.json',
      D.parents[2]/'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md']
    return {'status':'EXPLICIT_TWO_BIT_FULL_VECTOR_CODE_CONTROLS_WITH_SOURCE_RECOMPILATION_OBLIGATION',
      'physical_coordinates':M,'new_CODE_bits':2*M,'additional_RAW_births_required':M,
      'new_total_early_births_if_integrated':parent.production_configuration()['n']+M,
      'pairing':'(old physical SAM 2+j, appended physical A46.n+j)',
      'sampler_stride':'2^-80','control_step':'2^-1700','vertices':'Y0+sigma*(low+2*high−3p²)',
      'vertices_inside_old_continuous_cube':True,
      'phi_Qa':[coefficients_json(v) for v in phi],
      'lambda_Qa':{'%d_%d'%pair:coefficients_json(v) for pair,v in lam.items()},
      'positive_G_power_library':lib,
      'raw_control_counts':{str(sign):{k:hex(v) for k,v in c.items()} for sign,c in counts.items()},
      'each_padded_control_calls_hex':hex(length),'all_four_controls_calls_hex':hex(4*length),
      'native_alphabet':['G','CX'],'SourceI_calls':0,'all_column_controls':True,
      'native_inverse_is_not_exact_inverse_of_compiled_forward':True,
      'control_vs_exp_tX_error':old.encode(error),'control_vs_exp_tX_error_lt':'2^-5099',
      'continuous_full_bank_derivative_bounds':{k:old.encode(v) for k,v in derivatives.items()},
      'required_new_SOURCE_prefix_error':'2^-3300','required_new_complete_corner_error':'2^-3298',
      'conditional_corner_over_new_gain_error_lt':'2^-89',
      'conditional_exact_control_bank_axis_jet_error':old.encode(native_jet),
      'conditional_actual_control_finite_jet_extra':old.encode(finite_extra),
      'conditional_actual_control_finite_axis_jet_error':old.encode(finite_jet),
      'actual_control_noninverse_error_divided_by_sigma_times_t':True,
      'old_A46_SOURCE_word_reusable':False,'new_SOURCE_vertices_compiled':False,
      'new_full_clock_and_heat_computed':False,'full_original_Dnu_admission_proved':False,
      'full_Control_word_expanded_or_executed':False,
      'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in pins}}


if __name__=='__main__':
    plan=build();(P/'FULL_VECTOR_CONTROL_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
    print(json.dumps({k:plan[k] for k in ('status','new_CODE_bits','additional_RAW_births_required','control_vs_exp_tX_error_lt')}))
