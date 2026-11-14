#!/usr/bin/env python3
"""Ancilla-free SAM-only compiler for the full A37 SO target.

The four star lists remove two formal Householder sign flips algebraically.
No reflection/sign gate is emitted. Every actual emitted gate is G or CX on
SAM; zero-pattern Walsh gives exact identity off the selected plane.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import hashlib,json,sys
sys.dont_write_bytecode=True
import exact_target as e
P=Path(__file__).resolve().parent;D=P.parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')
CERT=B/'round80/UNIFORM_GOLDEN_GRID_CERTIFICATE.json'
CERT_SHA='3a73d409941cb916b36df5a2046e36499cc094fa338912a2c662a4c2a5d14ed9'


def uniform_grid():
    raw=CERT.read_bytes();assert hashlib.sha256(raw).hexdigest()==CERT_SHA
    cert=json.loads(raw);assert cert['status']=='PASS_RIGOROUS_UNIFORM_POSITIVE_GOLDEN_POWER_GRID'
    pn,q=int(cert['numerator_hex'],16),int(cert['denominator_hex'],16)
    assert gcd(pn,q)==1 and q.bit_length()==20080
    err=int(cert['abs_qgamma_minus_numerator_bound_numerator_hex'],16)
    assert q*err<1<<cert['precision_bits']
    return pn,q,cert


def elimination(v):
    """Chronological star rotations V_v v=e0 for positive unit v."""
    x=v[0];out=[]
    for j in range(len(v)-1,0,-1):
        y=v[j];r=e.root(x*x+y*y)
        out.append((j,x/r,-y/r));x=r
    return out


def target_stars(chi,h):
    """Chronological word, exactly R_chi R_h on ALL columns."""
    assert len(chi)==len(h)
    vh,vc=elimination(h),elimination(chi)
    yield from vh
    yield from reversed(vh)  # D V_h^T D: reverse and cancel both sign changes
    for j,c,s in vc:yield j,c,-s  # D V_chi D
    for j,c,s in reversed(vc):yield j,c,-s  # V_chi^T


def divided_angle(c,s,sam_bits):
    assert sam_bits>=2
    # Original c>0. Every subsequent c>=sqrt(1/2); no angle branch oracle.
    for _ in range(sam_bits-1):
        nc=e.root((1+c)/2)
        s=s/(2*nc);c=nc
    return c,s


def atan_positive(ctx,n):
    """Enclose atan(n/2^bits), 0<=n<2^bits, by exact interval series."""
    assert 0<=n<ctx.S
    if n==0:return (0,0)
    x=(n,n);one=ctx.rat(1)
    for _ in range(6):
        x=ctx.div(x,ctx.add(one,ctx.sqrt(ctx.add(one,ctx.mul(x,x)))))
    x2=ctx.mul(x,x);power=x;out=(0,0);k=0
    while power[1]>(1<<16):
        den=ctx.rat(2*k+1);term=ctx.div(power,den)
        out=ctx.add(out,term if k%2==0 else ctx.neg(term))
        power=ctx.mul(power,x2);k+=1
    rem=-((-power[1])//(2*k+1))
    return 64*(out[0]-rem),64*(out[1]+rem)


def atan_signed(ctx,n):
    return atan_positive(ctx,n) if n>=0 else ctx.neg(atan_positive(ctx,-n))


def select_positive_power(c,s,*,initial_bits=20480):
    """Concrete modular selection from exact algebraic c,s, c>0, |s/c|<1.

    Adaptive interval evaluation terminates: every expression is finite with
    positive radicands/denominators; the target is computable, and the fixed
    B80 pi interval is much narrower than the required 1/q precision.
    """
    pn,q,cert=uniform_grid();bits=initial_bits
    pi0=[int(v,16) for v in cert['pi_interval_hex']];pb=cert['precision_bits']
    while True:
        ctx=e.Dyadic(bits)
        try:
            cc,ss=ctx.evaluate((c,s));ratio=ctx.div(ss,cc)
            if not -ctx.S<ratio[0]<=ratio[1]<ctx.S:raise e.NeedPrecision()
            angle=(atan_signed(ctx,ratio[0])[0],atan_signed(ctx,ratio[1])[1])
            if bits<=pb:
                shift=pb-bits;pi=(pi0[0]>>shift,-((-pi0[1])>>shift))
            else:pi=tuple(v<<(bits-pb) for v in pi0)
            tau=ctx.div(angle,(2*pi[0],2*pi[1]))
            if 2*q*(tau[1]-tau[0])<=ctx.S:
                # Midpoint error <=1/(4q); nearest cell at q*midpoint.
                j=(q*(tau[0]+tau[1])+ctx.S)//(2*ctx.S)
                k=(j*pow(pn,-1,q))%q
                return k if k else q
        except e.NeedPrecision:pass
        bits*=2


def gate(op,*w):return {'op':op,'wires':list(w)}
def repeat(n,g):
    assert isinstance(n,int) and n>=1
    return {'op':'repeat','count':hex(n),'child':g}


def star_blocks(sam,j,k):
    """Exact R_{0j}(2^(m-1)*k*theta), identity off that plane."""
    sam=tuple(sam);m=len(sam)
    assert m>=2 and len(set(sam))==m and all(type(q) is int and q>=0 for q in sam)
    assert 1<=j<(1<<m) and type(k) is int and k>=1
    pivot=(j&-j).bit_length()-1;t=sam[pivot]
    affine=[gate('CX',t,sam[i]) for i in range(m) if i!=pivot and ((j>>i)&1)]
    yield from affine
    controls=[sam[i] for i in range(m) if i!=pivot]
    for mask in range(1<<(m-1)):
        parity=[gate('CX',q,t) for i,q in enumerate(controls) if (mask>>i)&1]
        yield from parity;yield repeat(k,gate('G',t));yield from reversed(parity)
    yield from reversed(affine)


def compile_target(chi,h,sam,selector=select_positive_power):
    """Executable reference on small vectors; not a production provider."""
    assert len(chi)==1<<len(sam)
    for j,c,s in target_stars(chi,h):
        cc,ss=divided_angle(c,s,len(sam));k=selector(cc,ss)
        yield from star_blocks(sam,j,k)


def production_word(*args,**kwargs):
    raise NotImplementedError('The production word is mathematically specified, not materialized or implemented as a Python provider')


def build():
    pn,q,grid=uniform_grid();m=2688;d=1<<m;L=1<<(m-1);stars=4*(d-1)
    upper_G=stars*L*q
    exact_CX=4*((d-1)*(m-1)*L+2*(m*L-d+1))
    upper_L=upper_G+exact_CX
    coarse=stars*(L*q+(m-1)*L+2*(m-1))
    assert upper_L<=coarse<(1<<25458)
    delta=F(1,1<<20000);error=stars*L*delta
    assert error<F(1,1<<14623)
    pins=[Path(__file__),P/'exact_target.py',CERT,B/'round80/certify_uniform_golden_grid.py',
          B/'round80/B80_UNIFORM_GOLDEN_GRID_RU.md',D/'round37/post_sam_reduction.py',
          D/'round30/marked_source_schedule.py',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',
          D/'round38/gcx_post_macros.py',D/'round38/POST_ANGLE_CERTIFICATE.json',
          B/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json',B/'round78/B78_ORIGINAL_H1_FN_ADMISSION_RU.md',
          D.parents[1]/'d0_native_readiness_amplification_2026-10-24/PHASE_COMPILER.md']
    return {'status':'MATHEMATICALLY_CONSTRUCTIVE_SAM_ONLY_FULL_COLUMN_COMPILER',
      'phase':'native realization; narrow outgoing SAM support and unitary type',
      'parent':'B78 all-column private-return/SAM-only post-unitary admission obstruction',
      'input_target':'actual A37 U*=R_chi R_h, h=(chi+M psi/||M psi||)/||chi+M psi/||M psi||||',
      'actual_M_evaluator':'literal actual A30 fixed-SAM G/CX word in Q(a), a^4+a^2-1=0; no assumed ideal reflection',
      'SAM_bits':m,'SAM_wires':'2..2689','new_births':0,
      'operator_scope':'entire real SAM Hilbert space, all columns; tensor identity on all original WORK and other wires',
      'all_actual_gates':['G positive powers','CX'],'native_variable_angle_or_reflection_gate':False,
      'full_matrix_target_identity':'V_chi^T (D V_chi D) (D V_h^T D) V_h = R_chi R_h; D eliminated before lowering',
      'chronological_star_lists':['V_h','D V_h^T D','D V_chi D','V_chi^T'],
      'star_count_hex':hex(stars),'power_upper_q_hex':hex(q),
      'one_small_angle_grid_error_strict_lt':'2^-20075 (B80), relaxed to 2^-20000',
      'uniform_full_operator_error_strict_lt':'2^-14623',
      'upper_G_calls_hex':hex(upper_G),'exact_CX_calls_hex':hex(exact_CX),
      'upper_total_calls_hex':hex(upper_L),'upper_total_calls_strict_lt':'2^25458',
      'target_angle_selection':'algebraic exact expression -> outward atan/pi interval -> modular inverse; terminating finite procedure',
      'actual_word_exactly_unitary_on_SAM':True,'all_column_private_return_exact_by_support':True,
      'production_target_table_or_words_evaluated':False,
      'production_Python_provider_implemented':False,
      'implementation_scope':'exact small reference fixtures and uniform integer bounds; unrestricted construction is a mathematical theorem',
      'not_claimed':['full four-slot/marked-task admission','same F_N fibre as A30/A39',
                      'full paid-history heat/clock/source integration','continuous native derivative',
                      'Cost-Info selection','refinement'],
      'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}}


if __name__=='__main__':
    out=build();(P/'SAM_ONLY_COMPILER_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','uniform_full_operator_error_strict_lt','upper_total_calls_strict_lt')}))
