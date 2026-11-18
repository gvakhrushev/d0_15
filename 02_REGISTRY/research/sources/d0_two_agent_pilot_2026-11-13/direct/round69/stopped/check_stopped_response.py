"""Prove bounds for the full stopped word on the CAR16 coframe of §7gb."""
from collections import defaultdict
from contextlib import redirect_stdout
from fractions import Fraction as F
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import runpy

import sympy as sp


def require(value, reason):
    if not value:
        raise ArithmeticError(reason)


def log_bounds(value):
    """Exact rational bounds for log on positive rationals, with binary reduction."""
    exponent = 0
    while value < 1:
        value *= 2
        exponent -= 1
    while value >= 2:
        value /= 2
        exponent += 1

    def unit(x):
        z = (x - 1) / (x + 1)
        terms = 20
        low = sum(2 * z**(2*i+1) / (2*i+1) for i in range(terms))
        return low, low + 2*z**(2*terms+1) / ((2*terms+1)*(1-z*z))

    low, high = unit(value)
    l2, h2 = unit(F(2))
    return low + min(exponent*l2, exponent*h2), high + max(exponent*l2, exponent*h2)


def log_sum(coefficients):
    lo = hi = F(0)
    for value, coefficient in coefficients.items():
        l, h = log_bounds(F(value))
        lo += min(coefficient*l, coefficient*h)
        hi += max(coefficient*l, coefficient*h)
    return lo, hi


def main():
    constructor = Path(__file__).with_name("primary_section_7gb.py")
    # Undo the two spelling changes for the Python 3.9 population-count fallback.
    original = constructor.read_bytes().replace(b'bin(lab & j).count("1")', b'(lab & j).bit_count()').replace(
        b'bin(bits).count("1")', b'bits.bit_count()')
    require(sha256(original).hexdigest() == '2ac8b4202c0212cf19a66c0a8940680cf94a405bdd99f2466936076faa7e9d66',
            'section 7gb source changed')
    output = StringIO()
    with redirect_stdout(output):
        base = runpy.run_path(str(constructor))
    require(json.loads(output.getvalue())['strictly_positive_by_integer_comparison'], 'upstream proof')
    ns, dns, a, da, lam, parity = (base[x] for x in ('ns','dns','a','da','kappa','pi'))
    dim = a.rows
    zero = sp.zeros(dim)
    normalizer = lam*(1-lam)
    column, row, dcolumn, drow = (zero.copy() for _ in range(4))
    rare_effect, rare_mass, speed_squared = zero.copy(), 0, 0
    mark_jet = defaultdict(lambda: sp.S.Zero)
    parity_logs = defaultdict(lambda: sp.S.Zero)
    counts = [0, 0]
    for n, dn in zip(ns[1:], dns[1:]):
        B = n.H*a
        dB = dn.H*a+n.H*da
        column += B.H*B
        row += B*B.H
        dcolumn += dB.H*B+B.H*dB
        drow += dB*B.H+B*dB.H
        speed_squared += sp.expand(sp.trace(dB.H*dB))/(dim*normalizer)
        m = (n*n.H).applyfunc(sp.expand)
        eigenvalues = list(m.diagonal())
        mark = sum(eigenvalues)/(dim*(1-lam))
        if not mark:
            require(m == zero, 'dark mark support')
            continue
        counts[0] += 1
        dmark = sp.expand(sp.trace(dn*n.H+n*dn.H))/(dim*(1-lam))
        mark_jet[mark] += dmark
        require(max(eigenvalues) <= 4*mark*(1-lam), 'likelihood-ratio ceiling')
        if max(eigenvalues) != min(eigenvalues):
            counts[1] += 1
            rare_mass += mark
            rare_effect += B.H*B/normalizer
        for index, mu in enumerate(eigenvalues):
            if mu:
                eig = mu/(1-lam)
                parity_logs[eig] -= parity[index,index]*eig/dim

    same = base['same']
    for actual in (column,row):
        require(same(actual,normalizer*sp.eye(dim)), 'normalized bistochastic channel')
    for actual in (dcolumn,drow):
        require(same(actual,zero), 'both differentiated identities')
    rare = F(32,3155)
    require(counts == [20,4] and rare_mass == rare, 'frequency of exceptional marks')
    require(same(rare_effect,sp.eye(dim)*rare_mass),'sum of exceptional effects')
    require(speed_squared == sp.Rational(8005,5679) < sp.Rational(6,5)**2,'measured Kraus speed')
    # Since a/sqrt(lam) anticommutes with parity, the minus sign above is essential.
    # Verify the complete logarithmic expression beta_1 = -rare*log(2) by prime exponents.
    prime_weights = defaultdict(lambda: sp.S.Zero)
    for eig, weight in parity_logs.items():
        for prime, exponent in sp.factorint(eig.p).items():
            prime_weights[prime] += weight*exponent
        for prime, exponent in sp.factorint(eig.q).items():
            prime_weights[prime] -= weight*exponent
    require({p:c for p,c in prime_weights.items() if c} == {2:-sp.Rational(32,3155)},'parity sign')
    require(sum(mark_jet.values()) == 0, 'normalized marks')
    h_lo,h_hi = log_sum({F(s): -F(dw) for s,dw in mark_jet.items()})
    # Exact one-round §7gb source divided by the probability of an active mark.
    L_lo,L_hi = log_sum({2:41,3:16,5:-4})
    Dlo,Dhi = F(12,631)*L_lo,F(12,631)*L_hi
    lo2,hi2 = log_bounds(F(2))
    require(2*hi2 < F(7,5), 'log 4 bound')
    require(F(7,5)**2+F(1,2)<F(8,5)**2,'root bound for k >= 2')
    require((2*F(6,5)*F(8,5))**2*rare/2 < F(7,25)**2,'cubic error constant')

    lo,hi = F(61803398874989,10**14), F(61803398874990,10**14)
    require(lo*lo+lo < 1 < hi*hi+hi, 'golden root bracket')
    lam = F(lam)
    def rates(p):
        b=4*p**3*lam**2
        v=4*p**3*lam*(1-lam)
        w=p*v
        return b,v,w,v/(1-b)
    b0,v0,w0,r0=rates(lo)
    b1,v1,w1,r1=rates(hi)
    u0,u1=(1-2*hi**2*lam)**2,(1-2*lo**2*lam)**2
    f0,f1=(w0+u0*r0)/(1-b0),(w1+u1*r1)/(1-b1)
    def tail_mean(r):
        return 1/(1-r)**2-1
    center0=f0*(Dlo+tail_mean(r0)*h_lo)
    center1=f1*(Dhi+tail_mean(r1)*h_hi)
    require(h_lo>0 and Dlo>0 and 0<r0<r1<1, 'monotonicity')
    error=f1*F(7,25)*((1+4*r1+r1*r1)/(1-r1)**4-1)
    require(F(1551,100000)<center0-error and center1+error<F(1681,100000),
            'infinite stopped coframe derivative enclosure')
    parity_error=f1*F(8,5)*rare*((1+r1)/(1-r1)**3-1)
    require(F(-166,10**6)<-f1*rare*hi2-parity_error and
            -f0*rare*lo2+parity_error<F(-128,10**6),'infinite stopped parity enclosure')
    # Word probabilities equal the reference product with zero or one exceptional mark.
    # The exceptional indicator has state-independent probability f on every visit.
    require((2*F(6,5)*F(8,5)*rare)**2/2 < F(7,250)**2, 'classical cubic error')
    class_error = error/10
    clo = f0*h_lo/(1-r0)**2-class_error
    chi = f1*h_hi/(1-r1)**2+class_error
    require(F(1636,100000) < clo < chi < F(1650,100000), 'classical stopped Shannon enclosure')
    logphi_lo = log_bounds(1/hi)[0]
    logphi_hi = log_bounds(1/lo)[1]
    for exponent, lower, upper in [(1,F(6799,100000),F(6858,100000)),
                                    (2,F(5099,100000),F(5144,100000))]:
        factor = 1+F(1,exponent)
        require(lower < factor*clo/logphi_hi < factor*chi/logphi_lo < upper,
                'extra charge for a stationary quiet leaf')
    for exponent, minimum in [(1,F(1591,100000)),(2,F(1546,100000))]:
        require((1+exponent)*clo-exponent*(center1+error)>minimum,
                'absolute response with one conditional record charge')
    print(json.dumps({
        'conditional_record': 'all original fine labels up to first even port; oldRIGHT retained',
        'active_marks': counts[0], 'nonscalar_marks': counts[1], 'average_speed_squared': str(speed_squared),
        'exceptional_mark_mass': str(rare), 'coframe_derivative_open_interval': ['0.01551','0.01681'],
        'parity_coefficient_open_interval': ['-0.000166','-0.000128'],
        'classical_record_derivative_open_interval': ['0.01636','0.01650'],
        'conditional_Born_Shannon_logZ_jet_plus_logphi_Dextra_cost': ['0.03272','0.03300'],
        'extra_charge_jet_if_quiet_weight_stationary': {
            'positive_price': ['0.06799','0.06858'], 'orthogonal_amplitude': ['0.05099','0.05144']},
        'generated_input_first_jet': 0, 'port_cost_first_jet': 0,
        'physical_C_closed': False, 'GR_closed': False
    }, indent=2))


if __name__ == '__main__':
    main()
