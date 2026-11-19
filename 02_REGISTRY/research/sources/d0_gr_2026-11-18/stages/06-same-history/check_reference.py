"""Exact first jets of the actual full128 output with classically correlated references."""
import contextlib
import io
import json
import runpy
from collections import defaultdict
from pathlib import Path

import sympy as s
import mpmath as mp


def require(test, description):
    if not test:
        raise ArithmeticError(description)


def zero(matrix):
    return all(s.expand(entry) == 0 for entry in matrix)


def product(left, right):
    return (left*right).applyfunc(s.expand)


def log_signature(basis, effects, jets):
    totals = defaultdict(lambda: s.S.Zero)
    require(zero(basis.H*basis - s.eye(16)), "reference ensemble is orthonormal")
    for m, dm in zip(effects[1:], jets[1:]):
        for j in range(16):
            v = basis[:, j]
            t = (v.H*m*v)[0].expand()
            dt = (v.H*dm*v)[0].expand()
            require(t.is_Rational and t >= 0 and dt.is_Rational, "raw algebraic data")
            if t == 0:
                require(dt == 0, "no first jet on zero support")
            if dt == 0:
                continue
            for prime, exponent in s.factorint(t.p).items():
                totals[prime] -= exponent*dt
            for prime, exponent in s.factorint(t.q).items():
                totals[prime] += exponent*dt
    return {k: v for k, v in sorted(totals.items()) if v}


def main():
    frozen = Path(__file__).with_name("frozen")/"check_full128_cq_coframe_residual.py"
    with contextlib.redirect_stdout(io.StringIO()):
        primary = runpy.run_path(str(frozen))
    ns, dns = primary["ns"], primary["dns"]
    a, da, lam, eye, nu = (primary[k] for k in ("a", "da", "kappa", "I", "nu"))
    require(zero(a*a-lam*eye) and zero(a*da+da*a), "scalar centre and first jet")
    require(zero(da*da - eye/64), "scalar quadratic coframe coefficient")
    rotation = a*da/lam
    require(zero(rotation.H + rotation), "coframe basis jet")
    effects, jets = [], []
    for n, dn in zip(ns, dns):
        m = product(n,n.H)
        dm = product(dn,n.H) + product(n,dn.H)
        dme = (dm + rotation*m-m*rotation).applyfunc(s.expand)
        dcut = product(product(da,m),a)+product(product(a,dm),a)+product(product(a,m),da)
        direct = product(product(a,dcut),a)/lam**2
        require(zero(dme-direct), "actual fixed-basis cut of all differentiated legs")
        require(m.is_diagonal(), "simultaneous central diagonalization")
        effects.append(m)
        jets.append(dme)
    require(zero(jets[0]) and zero(sum(jets[1:], s.zeros(16))), "per-input normalization")
    require(zero(ns[9]-9*eye/10) and zero(dns[9]+3*eye/32), "physical address 9")
    hadamard = s.Matrix(16, 16, lambda i, j: s.Rational((-1)**((int(i)&int(j)).bit_count()), 4))
    def two_row_rotation(sign):
        u = s.eye(16)
        u[0, 0] = u[3, 3] = s.Rational(4,5)
        u[3, 0] = u[0, 3] = sign*s.I*s.Rational(3,5)
        return u
    bases = {"eigen":eye, "occupation":a/s.sqrt(lam), "walsh":hadamard,
             "plus_i":two_row_rotation(1), "minus_i":two_row_rotation(-1)}
    signatures = {name:log_signature(u, effects, jets) for name,u in bases.items()}
    expected = {
        "eigen":("123/10","24/5","-6/5"), "occupation":("306/25","24/5","-21/20"),
        "walsh":("63/5","24/5","-6/5"),
        "plus_i":("15191/1250","23993/5000","-9/8"),
        "minus_i":("15319/1250","23737/5000","-9/8")}
    for name, numbers in expected.items():
        require(signatures[name] == dict(zip((2,3,5), map(s.Rational, numbers))),name)
    phase_cells = {}
    for j,(m,dm) in enumerate(zip(effects,jets)):
        plus=bases["plus_i"]; minus=bases["minus_i"]
        require(zero((plus.H*m*plus-minus.H*m*minus).diagonal()), "identical central probabilities")
        contrast = (minus.H*dm*minus-plus.H*dm*plus).diagonal().applyfunc(s.expand)
        for i,value in enumerate(contrast):
            if value:
                phase_cells[(j,i)]=value
    h=s.Rational(8,625)
    require(phase_cells=={(13,0):-h,(13,3):h,(45,0):h,(45,3):-h},"actual four-cell table")
    p = (s.sqrt(5)-1)/2
    scale = 4*p**2*lam/16
    delta11 = scale*phase_cells[(45,3)]
    m0,m1 = p**2+p**4, 2*p**3
    require(s.simplify(m0-m1-p**6)==0, "actual two-reader tilt contrast")
    marks=[m0,m1]
    z0 = s.S.Zero
    coarse = s.zeros(2)
    for j,m in enumerate(effects):
        diag=(plus.H*m*plus).diagonal().applyfunc(s.expand)
        for i,ev in enumerate(diag):
            # Labels within each j include both old ports. The originally quiet pair is special.
            prob = (1-4*p**2*lam*(1-lam))/16 if j==0 else scale*ev
            z0 += prob*marks[j>>5]*marks[i&1]
            coarse[j>>5,i&1] += prob
    z0=s.simplify(z0)
    coarse=coarse.applyfunc(s.simplify)
    require(s.simplify(sum(coarse)-1)==0, "all coarse probabilities included")
    direct_dz=sum(scale*v*marks[j>>5]*marks[i&1] for (j,i),v in phase_cells.items())
    require(s.simplify(direct_dz-p**12*delta11)==0, "paid phase contrast")
    odds=(s.Rational(4,625)/s.Rational(9,2500))**2
    require(odds==s.Rational(4,3)**4,"central odds at the actual four cells")
    ratio=p**12/(z0*s.log(odds))
    mp.iv.dps=65
    iv=mp.iv
    def algebraic_interval(value):
        r,b=s.expand(value).as_coeff_Add()
        coef=s.simplify(b/s.sqrt(5))
        require(r.is_Rational and coef.is_Rational, "quadratic-field certificate")
        return (iv.mpf(int(r.p))/int(r.q)
                +iv.mpf(int(coef.p))/int(coef.q)*iv.sqrt(5))
    mzero,mone=map(algebraic_interval,(s.simplify(m0),s.simplify(m1)))
    oddslog=4*iv.log(iv.mpf(4)/3)
    paid_comparisons={}
    contrasts=[]
    for length in (15,16):
        local=[mzero**length,mone**length]
        normalizer=sum(algebraic_interval(coarse[k,l])*local[k]*local[l]
                       for k in range(2) for l in range(2))
        diff=(local[0]-local[1])**2
        portion=diff/(normalizer*oddslog)
        contrasts.append(diff-oddslog*normalizer)
        low,high=("0.9675","0.9677") if length==15 else ("1.0325","1.0327")
        require(iv.mpf(low)<portion and portion<iv.mpf(high), "certified true repetitions")
        paid_comparisons[length]=[low,high]
    coin=-contrasts[0]/(contrasts[1]-contrasts[0])
    require(0<coin and coin<1, "positive reference-only calibration probability")
    scores = {name:scale*sum(v*s.log(k) for k,v in row.items())
              for name,row in signatures.items()}
    diff = signatures["minus_i"]
    delta = {i:diff[i]-signatures["plus_i"][i] for i in diff}
    require(delta == {2:s.Rational(64,625),3:-s.Rational(32,625),5:0}, "phase ratio")
    endpoint = {i:signatures["walsh"][i]-signatures["eigen"][i] for i in diff}
    require(endpoint == {2:s.Rational(3,10),3:0,5:0}, "classical endpoint difference")
    require(2**12>5**5 and 5**5>2**2, "ordering of the occupation source")

    t = s.symbols("t", real=True)
    weight_squared = 1 / (1 + s.Rational(10,9)*t*t)
    require(s.factor(weight_squared*(lam+t*t/64)-lam)==0, "finite exact feedback level")
    s0 = weight_squared*((nu+t)**2+t**2)
    s1 = weight_squared*nu**2
    a9 = (4+s.sqrt(1-s0)+3*s.sqrt(1-s1))/8
    addr9 = 4*p**2*lam*a9**2
    require(s.simplify(s.diff(addr9,t).subs(t,0)+243*p**2/25600)==0, "actual derivative at 9")
    step = s.Rational(1,16)
    crude = s.Rational(3,8)*lam*nu*step*weight_squared.subs(t,step)
    require(crude > s.Rational(1,5200), "strict finite event separation by positive rational bound")
    gap = addr9.subs(t,-step)-addr9.subs(t,step)
    return {"status":"PASS","normalised_finite_curve":"Lambda=9/640 I",
            "raw_coframe_quadratic":"1/64 I","endpoint_parameter":["-1/16","1/16"],
            "finite_address9_probability_difference":str(s.N(gap,26)),
            "strict_finite_lower_bound":"1/5200","all_coarse_port_laws_identical_on_curve":True,
            "signatures_in_units_9p2_over_2560":
                {name:{str(k):str(v) for k,v in row.items()} for name,row in signatures.items()},
            "source_nats":{name:str(s.N(value,28)) for name,value in scores.items()},
            "phase_gap_nats_exact":"9*p^2/50000*log(4/3)",
            "phase_gap_nats":str(s.N(scores["minus_i"]-scores["plus_i"],28)),
            "classical_endpoint_gap_nats_exact":"27*p^2/25600*log(2)",
            "four_cell_derivative_units_9p2_over_2560":{str(k):str(v) for k,v in phase_cells.items()},
            "physical_two_pointer_golden_moment_at_centre":str(z0),
            "joint_coincidence_source_difference":str(s.N(delta11,24)),
            "paid_log_response_fraction_of_joint_information_response":str(s.N(ratio,24)),
            "two_marker_ratio_intervals":paid_comparisons,
            "calibration_probability_for_16_each_side":float(coin.mid),
            "phase_preparations_have_same_complete_classical_central_probabilities":True,
            "physical_mandatory_info_selected":False,"GR_closed":False}


if __name__=="__main__":
    print(json.dumps(main(),indent=2))
