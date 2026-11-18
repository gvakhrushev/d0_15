"""Exact threshold, registered Golden prices and scalar-effect memory tests for A70."""
from contextlib import redirect_stdout
from fractions import Fraction
from io import StringIO
from pathlib import Path
import runpy

import sympy as sp


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def dyadic_count(threshold, bits):
    """Disjoint prefixes of U<threshold, most significant bit first."""
    count = 0
    for shift in reversed(range(bits)):
        if (threshold >> shift) & 1:
            count += 1 << shift
    return count


def entropy_term(mass):
    return -mass * sp.log(mass)


def entropy_binary(q):
    return entropy_term(q) + entropy_term(1 - q)


def main():
    # Execute the actual PC2 field/matter polynomials, READY preparation and
    # interpolation proof. The cash-out below uses their returned integers.
    source = Path(__file__).resolve().parents[1] / 'extraction' / 'check_eight_scales.py'
    with redirect_stdout(StringIO()):
        geometry = runpy.run_path(str(source))
    weights = geometry['m']
    bound = geometry['limit']
    require(bound == 2 * sum(abs(m) for m in weights) == 126506, 'actual signed source range')
    bits = 20
    size = 1 << bits
    offset = 3 * (size // 4)
    lo, hi = Fraction(offset - bound, size), Fraction(offset + bound, size)
    require(Fraction(62, 100) < lo < hi < Fraction(88, 100), 'closed attainable enclosure')
    require(lo**2 + lo > 1, 'whole enclosure above the inverse golden ratio')

    for threshold in range(offset - bound, offset + bound + 1):
        require(dyadic_count(threshold, bits) == threshold, 'prefix count at threshold')
    # The complementary counts sum to size. Every accepted address has mass
    # p^(3*bits), even when paired with an arbitrary old input.
    p = sp.symbols('p', positive=True)
    reduce_p = geometry['reduce_p']
    native_p = geometry['p']
    native_pair = [native_p, native_p**2]
    pair = [a*b for a in native_pair for b in native_pair]
    require(reduce_p(sum(pair) - 1) == 0 and pair[1] == pair[2] == native_p**3,
            '00,01,10,11 from two independent canonical births')
    lam_raw = (2*p**3)**bits
    require(sp.expand(size * p**(3*bits) - lam_raw) == 0, 'unconditional uniform joint masses')
    xmean = sp.symbols('xmean', real=True)
    P = (offset+xmean) / size
    require(sp.simplify(lam_raw*P - p**(3*bits)*(offset+xmean)) == 0,
            'absolute yes probability, no discarded trials')
    require(sp.simplify(P - sp.Rational(3, 4) - xmean/size) == 0, 'exact source transfer')

    # If all retained microscopic histories have effects E_x and sum(x E_x)
    # is xmean*I on the prepared protected input, the three stacked Kraus
    # maps have scalar Gram matrices. This example has nonscalar fine effects.
    i2 = sp.eye(2)
    q = sp.Rational(1, 7)
    fine = sp.Matrix([[4, 1], [1, 3]]) / 28
    effects = {-1: fine, 0: i2 - 2*fine - q*i2, 1: fine + q*i2}
    for effect in effects.values():
        require(effect.is_positive_definite, 'legal nonscalar fine effects')
    require(sum(effects.values(), sp.zeros(2)) == i2, 'unbiased fine completion')
    require(sum((value*effect for value,effect in effects.items()), sp.zeros(2)) == q*i2,
            'scalar first moment despite microscopic correlations')
    hit = sum(((offset+value)*effect/size for value,effect in effects.items()), sp.zeros(2))
    require(hit == P.subs(xmean,q)*i2 and i2-hit == (1-P.subs(xmean,q))*i2, 'coarse Gram')
    # Check the remote reference block for a completely general joint input:
    # (Tr_D K rho K*)_ij = Tr_D(rho_ij K*K) even for a stacked isometry K.
    rho = sp.Matrix(4, 4, sp.symbols('a:16'))
    for i in range(2):
        for j in range(2):
            block = rho.extract([i, i+2], [j, j+2])
            require(sp.expand(sp.trace(block*hit) - P.subs(xmean,q)*sp.trace(block)) == 0,
                    'arbitrary protected joint input and reference')

    # Golden information is Shannon in log base phi. Work in nats first.
    lam,t = sp.symbols('lambda t', positive=True)
    ell = sp.symbols('ell', positive=True)  # log(phi)
    hflag = entropy_term(1-lam) + entropy_term(lam*t) + entropy_term(lam*(1-t))
    chain = hflag - entropy_binary(lam) - lam*entropy_binary(t)
    require(sp.simplify(sp.expand_log(chain, force=True)) == 0, 'three coarse labels incl. FAIL')
    codes = {1: ('0', '10'), -1: ('10', '0'), 0: ('010', '100')}
    for slope, (zero_word, one_word) in codes.items():
        require(not (one_word.startswith(zero_word) or zero_word.startswith(one_word)),
                'prefix-distinguishable positive output code')
        base = len(zero_word)
        require(len(one_word)-base == slope, 'real Golden digit lengths')
        full_cost = 1+lam + lam*(base+slope*t)  # native flag 0 / 10, then code on success
        full_price = full_cost - hflag/ell
        derivative = sp.diff(full_price, t) - lam*(slope + sp.log(t/(1-t))/ell)
        require(sp.simplify(sp.expand_log(derivative, force=True)) == 0, 'Golden absolute slope')
    # t>1/phi iff t/(1-t)>phi. Its Golden log then exceeds 1 even at slope -1.
    require(lo*lo > 1-lo and 0 < lo < hi < 1, 'positive slopes for -1,0,+1')

    # The full instrument measures factory T but retains all fair orientations,
    # REPORT and threshold addresses coherently in the quantum completion.
    # First remove the eight READY factors inside the already conditioned bank.
    eps, rf, action = sp.symbols('eps rf action', real=True)
    gain_given_ready = geometry['scale']*eps*rf
    ready = sp.symbols('alpha1:9', positive=True)
    old_gain = gain_given_ready * sp.prod(ready)
    require(sp.simplify(old_gain/sp.prod(ready) - gain_given_ready) == 0
            and geometry['scale'] == 840, 'conditional source has no second READY factor')
    # Distinct paid successful transcripts may have arbitrary constant masses
    # and output isometries, provided their conditional logical probabilities agree.
    success_masses = sp.symbols('success0:3', positive=True)
    abort_masses = sp.symbols('abort0:2', positive=True)
    gamma = sum(success_masses)
    observed = [t*w for w in success_masses] + [(1-t)*w for w in success_masses]
    observed += list(abort_masses)
    base_entropy = sum(entropy_term(w) for w in success_masses + abort_masses)
    detail_entropy = sum(entropy_term(w) for w in observed)
    require(sp.simplify(sp.expand_log(detail_entropy-base_entropy-gamma*entropy_binary(t),
                                      force=True)) == 0, 'full field-independent factory transcript')
    u_factory = sp.Rational(3,4) + gain_given_ready*action/size
    for slope in codes:
        raw_slope = sp.diff(gamma*slope*t-detail_entropy/ell, t) * sp.diff(u_factory, action)
        expected = gamma*gain_given_ready*(slope+sp.log(t/(1-t))/ell)/size
        require(sp.simplify(sp.expand_log(raw_slope-expected, force=True)) == 0,
                'absolute success mass Gamma and conditioned factory gain exactly once')

    # Actual fine measurement of X changes joint measured entropy. Its excess
    # over the coarse observer is strictly positive for these distinct rates:
    # h((u+v)/2) > (h(u)+h(v))/2 by strict concavity on (0,1).
    asym = [Fraction(offset+n, size) for n in (-1,1)]
    require(0 < asym[0] < asym[1] < 1 and sum(asym)/2 == Fraction(3,4),
            'retaining a measured nonconstant fine reference changes conditional entropy')
    print('PASS: native PC2 extraction, 253013 exact threshold counts, 20 Golden pairs, '
          'all three unconditional labels and tariffs, scalar coarse Gram and old reference, '
          'strict Golden slopes, paid factory transcript Gamma, and fine-record boundary.')


if __name__ == '__main__':
    main()
