"""Structured source error of the actual common-amplitude L=4 CAR loader.

This is a scoped reference-bank/SC1 identity, not a full paid-price check.
The long native word and its heralded factories are consumed from their
owner; no claim is made to replay its approximately 60 million letters.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import json

import mpmath as mp
import sympy as sp


HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def exact_polynomial():
    """Check every SC1 coefficient, with independent reference amplitudes."""
    p, x, y = sp.symbols("p x y")
    z = sp.Rational(1, 2**20)

    def reduce_golden(expr):
        return sp.rem(sp.expand(expr), p*p+p-1, p)

    def report(a, b):
        E = p*p*(1+a)
        L = 4*E*(1-E)
        u = p+p*p*b
        B = 4*u*u*(1-u*u)
        A = L+(1-L)*B
        return z*(A+B)-z*z*A*B

    rx = [reduce_golden(c) for c in
          reversed(sp.Poly(report(x, 0), x).all_coeffs())]
    ry = [reduce_golden(c) for c in
          reversed(sp.Poly(report(0, y), y).all_coeffs())]
    need((len(rx)-1, len(ry)-1) == (2, 8), "actual SC1 degrees")
    need(rx[0] == ry[0], "one common SC1 offset")
    rf, rq = rx[1], ry[1]
    # Independent formulae used by the interval calculation, checked in Q(p).
    need(reduce_golden(rf-4*p*p*(1-2*p*p)*z*(1-z*4*p**3)*(1-4*p**3)) == 0,
         "geometric derivative formula")
    need(reduce_golden(rq-8*p**3*(1-2*p*p)*(z*(2-4*p**3)
         -z*z*(4*p**3+2*(1-4*p**3)*4*p**3))) == 0,
         "material derivative formula")

    bf, bm, f, m = sp.symbols("b_f b_m f m")
    # Coefficients of A(eps)*(rx(eps*f)-r0)
    #              +B(eps)*(ry(-eps*m)-r0).
    # f,m are the actual f_x/rho_x,m_x/rho_x. Multiplication by
    # mu_x=v_x*rho_x cancels rho_x pointwise in the recovered coefficient.
    coefficients = {n: sp.Integer(0) for n in range(10)}
    for i in range(1, len(ry), 2):
        for j in range(1, len(rx)):
            coefficients[i+j] += 2*ry[i]*bm**i*rx[j]*f**j
    for i in range(1, len(rx), 2):
        for j in range(1, len(ry)):
            coefficients[i+j] += 2*rx[i]*bf**i*ry[j]*(-m)**j
    coefficients = {n: reduce_golden(v) for n, v in coefficients.items()}
    target = reduce_golden(2*rf*rq*(bm*f-bf*m))
    need(sp.expand(coefficients[2]-target) == 0, "unmatched-reference source")
    need(coefficients[0] == 0 and coefficients[1] == 0, "double zero at eps=0")
    weights = [Fraction((-1)**(j-1)*comb(8,j), j*j) for j in range(1,9)]
    moments = [sum(w*Fraction(j**n) for j,w in enumerate(weights,1))
               for n in range(10)]
    need(moments[2] == 1, "quadratic moment")
    need(all(moments[n] == 0 for n in range(3,10)), "all seven higher moments")
    for variable in (f, m, bf, bm):
        need(sp.expand(sp.diff(coefficients[2], variable)
                       -sp.diff(target, variable)) == 0,
             "full coefficient differential: "+str(variable))

    # A frozen material support is not needed: f,m,cell volumes and rho may
    # all vary. This verifies the rho cancellation before differentiating.
    rho, volume = sp.symbols("rho volume", nonzero=True)
    local = volume*rho*target.subs({f:f/rho,m:m/rho})
    need(sp.expand(local-volume*target) == 0, "pointwise moving-density identity")
    # On a general dyadic mesh, the positive and negative material
    # references need not have identical chord errors. Retain degree ten.
    bp, bn = sp.symbols("b_positive b_negative")
    asym = {n: sp.Integer(0) for n in range(11)}
    for i in range(1, len(ry)):
        for j in range(1, len(rx)):
            asym[i+j] += ry[i]*(bp**i-(-bn)**i)*rx[j]*f**j
    for i in range(1, len(rx), 2):
        for j in range(1, len(ry)):
            asym[i+j] += 2*rx[i]*bf**i*ry[j]*(-m)**j
    asym = {n:reduce_golden(c) for n,c in asym.items()}
    leading = reduce_golden(rf*rq*((bp+bn)*f-2*bf*m))
    top = reduce_golden(rx[2]*ry[8]*(bp**8-bn**8)*f**2)
    need(sp.expand(asym[2]-leading)==0, "asymmetric leading coefficient")
    need(sp.expand(asym[10]-top)==0, "actual degree-ten alias")
    tenth = sum(w*Fraction(j**10) for j,w in enumerate(weights,1))
    need(tenth == -40320, "eighth-setting top alias has negative factorial")
    need(reduce_golden(rx[2]+(1+p)*rf)==0, "r20=-phi*r_f")
    need(reduce_golden(ry[8]+16*z*z*(1-4*p**3)*p**16)==0,
         "exact r08 coefficient")
    for variable in (f,m,bf,bp,bn):
        need(sp.expand(sp.diff(asym[2]+tenth*asym[10],variable)
                       -sp.diff(leading+tenth*top,variable))==0,
             "all asymmetric source and calibration derivatives")
    return {"geometric_degree":2,"material_degree":8,
            "full_difference_degree":max(n for n,c in coefficients.items() if c != 0),
            "all_polynomial_coefficients_checked":True,
            "independent_reference_and_field_differentials_checked":True,
            "moving_site_density_cancels_pointwise":True,
            "r_f_in_Qp":str(rf),"r_q_in_Qp":str(rq),
            "general_dyadic_asymmetric_degree":10,
            "exact_degree_ten_alias_moment":int(tenth),
            "r20_over_rf":"-phi","r08_in_Qp":str(ry[8]),
            "asymmetric_reference_all_coefficients_checked":True}


def exact_differential():
    # A positive selector multiplies both the common offset and raw gain.
    B, P0, alpha, t, bm, bf, F, M, k0, C = sp.symbols(
        "beta_s pi_0 alpha t b_m b_f F M k0 C", nonzero=True)
    gain = C*B*alpha**2*t**2*bm
    k = bf/bm
    effective = F-k*M
    nominal = F-k0*M
    pi = B*P0+gain*effective
    variables = (B,P0,alpha,t,bm,bf,F,M)
    for q in variables:
        rhs = (sp.diff(nominal,q)-(k-k0)*sp.diff(M,q)-M*sp.diff(k,q)
               +effective*sp.diff(gain,q)/gain
               +(P0*sp.diff(B,q)+B*sp.diff(P0,q))/gain)
        need(sp.simplify(sp.diff(pi,q)/gain-rhs) == 0,
             "complete normalized source: "+str(q))
    s, Bm, Bf = sp.symbols("s_ref B_m B_f", nonzero=True)
    shared = {bm:Bm/s**2, bf:Bf/s**2}
    need(sp.diff(k.subs(shared),s) == 0, "shared s_ref cancels in coupling")
    gs = gain.subs(shared)
    need(sp.simplify(sp.diff(gs,s)/gs+2/s) == 0,
         "shared s_ref remains in gain")

    # The exact coordinate option is a mathematical pullback, not an
    # unproved physical input normalization. Keep all 42 independent rows.
    e = sp.symbols("e0:16")
    u = sp.symbols("u0:24")
    q = sp.symbols("psi0:2")
    tau = sp.symbols("tau", positive=True)
    # Arbitrary geometry and arbitrary mixed quadratic matter coefficients;
    # this is a symbolic homogeneity/chain-rule check, not a replay of a
    # finite gravity root or of its not-yet-compiled physical field bank.
    geom = sp.Function("F_geom")(*(e+u))
    aa, bb, cc = (sp.Function(n)(*(e+u)) for n in ("A_m", "B_m", "C_m"))
    matter = aa*q[0]**2+bb*q[1]**2+cc*q[0]*q[1]
    actual = geom-(k0/tau)*matter
    pullback = (geom-k0*matter).subs({q[0]:q[0]/sp.sqrt(tau),q[1]:q[1]/sp.sqrt(tau)})
    for v in e+u+q:
        need(sp.simplify(sp.diff(actual-pullback,v)) == 0,
             "fixed-tau mathematical Euler pullback: "+str(v))
    need(sp.simplify((q[0]/sp.sqrt(tau)).subs(q[0],sp.sqrt(tau)*q[0])-q[0]) == 0,
         "right inverse rescales both material components")
    return {"normalization_and_offset_rows":len(variables),
            "alpha_selector_step_and_reference_rows_retained":True,
            "s_ref_coupling_derivative":0,"s_ref_log_gain_derivative":"-2/s_ref",
            "fixed_tau_mathematical_Euler_rows":42,
            "arbitrary_geometry_and_quadratic_matter_coefficients":True,
            "physical_coordinate_map_admitted":False}


def exact_site_structure():
    # Exact signed quarter turns of the actual L=4 SITE words. Check every
    # original directed site edge, not only an averaged/continuum gradient.
    phases = ((1,0),(0,1),(-1,0),(0,-1))
    edges = 0
    for mu in (0,1):
        for site in product(range(4),repeat=4):
            for nu in range(4):
                neighbour = list(site)
                neighbour[nu] = (neighbour[nu]+1)%4
                a = phases[site[mu]]
                b = phases[neighbour[mu]]
                square = sum((x-y)**2 for x,y in zip(a,b))
                need(square == (2 if nu==mu else 0), "actual periodic SITE chord")
                edges += 1
    need(edges == 2048, "all two-field directed edges")
    # Negative control for the ninth-degree shortcut: a small bitwise
    # phase error gives nonconstant cyclic chords, and the two physical
    # reference coordinates then disagree at some common SITE.
    mp.mp.dps = 80
    L = 8
    errs = (mp.mpf('0.00001'),mp.mpf('-0.00002'),mp.mpf('0'))
    budget = sum(abs(e) for e in errs)
    angles = [2*mp.pi*n/L+sum(errs[j]*((n>>j)&1) for j in range(3))
              for n in range(L)]
    ratios = [mp.sin((angles[(n+1)%L]-angles[n])/2)**2/mp.sin(mp.pi/L)**2
              for n in range(L)]
    eta = 2*budget/mp.sin(mp.pi/L)+budget**2/mp.sin(mp.pi/L)**2
    need(all(abs(r-1)<=eta for r in ratios), "phase bound includes periodic seam")
    need(max(ratios)-min(ratios)>mp.mpf('0.00001'),
         "asymmetric reference negative control is nontrivial")
    need(any(abs(a**8-b**8)>mp.mpf('0.00001') for a in ratios for b in ratios),
         "unequal references cannot silently discard the degree-ten alias")
    return {"L":4,"directed_edges_checked":edges,
            "both_material_signs_exact":True,"all_site_phases_exact":True,
            "general_dyadic_source_formula_includes_alias":True,
            "L8_phase_bound_and_nonzero_alias_control":True,
            "refining_physical_full_price_bound_proved":False}


def interval_calibration():
    owner = json.loads((HERE/"dyadic_car_loader_result.json").read_text())
    values = owner["controlled_plane_rotation_approximants"]
    need(owner["L"] == 4 and len(values)==1, "one radial approximation on L=4")
    v = values[0]
    mult, run, wraps = v["gray_block_size"],v["G_run_length"],v["wraps"]
    need((mult,run,wraps)==(8,7457170,6325786), "actual published native word")
    iv = mp.iv
    iv.dps = 100
    one = iv.mpf(1)
    p = (iv.sqrt(5)-one)/2
    z = one/2**20
    rf = 4*p**2*(one-2*p**2)*z*(one-z*4*p**3)*(one-4*p**3)
    rq = 8*p**3*(one-2*p**2)*(z*(2-4*p**3)
          -z*z*(4*p**3+2*(one-4*p**3)*4*p**3))
    k0 = rq/rf
    F = iv.mpf(16517734400)/162621047169
    H, s = one/4, iv.mpf(4)
    A = H*iv.sqrt(F/k0)/(2*iv.sin(iv.pi*H))
    beta = iv.atan2(A/p, iv.sqrt(one-(A/p)**2))
    theta = iv.atan2(p,iv.sqrt(p))
    actual_beta = mult*run*theta-2*iv.pi*wraps
    actual_A = p*iv.sin(actual_beta)
    Bm = 4*actual_A**2*iv.sin(iv.pi*H)**2/(H**2)
    bm = Bm/s**2
    bf = F/s**2
    tau = (actual_A/A)**2
    k = bf/bm
    delta = k-k0
    need(actual_beta>0 and actual_beta<iv.pi/2, "physical common radial quadrant")
    need(actual_A>0 and p*p-actual_A**2>0, "nonzero amplitude and filler reserve")
    need(delta>iv.mpf('-0.000095892926298') and delta<iv.mpf('-0.000095892926297'),
         "outward rational coupling-error enclosure")
    need(tau>iv.mpf('1.0000040951338097') and tau<iv.mpf('1.0000040951338098'),
         "outward rational gain-ratio enclosure")
    need(abs(delta)<iv.mpf('0.0000959'), "normalized fixed-map error coefficient")
    # The formula is proportional to the actual gain before differentiation;
    # no probability-error/gain estimate is being used.
    return {"G_run_length":run,"gray_block_size":mult,"wraps":wraps,
            "G_letters_not_individually_replayed":mult*run,
            "nominal_amplitude_interval":str(A),
            "actual_amplitude_interval":str(actual_A),
            "angle_error_interval":str(actual_beta-beta),
            "actual_material_reference_interval":str(bm),
            "original_k0_interval":str(k0),"effective_k_interval":str(k),
            "delta_k_interval":str(delta),"gain_ratio_tau_interval":str(tau),
            "relative_coupling_error_interval":str(k/k0-one),
            "mathematical_right_lift_matter_scale_interval":str(iv.sqrt(tau)),
            "fixed_map_defect_coefficient_upper":"0.0000959",
            "bound_multiplies":"norm(D material_action composed with actual right lift)",
            "rounding_enclosed_by_interval_arithmetic":True}


def main():
    result = {"schema":"d0.dyadic-reference-source/1","status":"PASS",
              "exact_SC1":exact_polynomial(),"complete_differential":exact_differential(),
              "exact_SITE":exact_site_structure(),"calibration":interval_calibration(),
              "conditions":{"one_common_actual_reference_on_all_eight_settings":True,
                "other_SC1_banks_and_their_actual_readiness_required":True,
                "current_geometric_field_bank_compiled_here":False,
                "all_independent_hardware_directions_closed":False,
                "full_CostInfo_bound_proved":False,"GR_closed":False},
              "inputs_sha256":{name:sha256((HERE/name).read_bytes()).hexdigest() for name in
                ("check_dyadic_car_loader.py","dyadic_car_loader_result.json",
                 "check_eight_readers.py")}}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
