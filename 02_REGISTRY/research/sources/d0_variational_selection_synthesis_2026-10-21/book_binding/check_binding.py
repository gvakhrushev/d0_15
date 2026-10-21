#!/usr/bin/env python3
"""Exact narrow composition test; no scientific files are rewritten."""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


class Qp:
    """Q[p]/(p^2+p-1), in the positive golden embedding."""
    def __init__(self, a=0, b=0):
        if isinstance(a, Qp):
            self.a, self.b = a.a, a.b
        else:
            self.a, self.b = F(a), F(b)

    def __add__(self, y):
        y = Qp(y)
        return Qp(self.a+y.a, self.b+y.b)

    __radd__ = __add__

    def __neg__(self):
        return Qp(-self.a, -self.b)

    def __sub__(self, y):
        return self + -Qp(y)

    def __rsub__(self, y):
        return Qp(y) + -self

    def __mul__(self, y):
        y = Qp(y)
        return Qp(self.a*y.a+self.b*y.b,
                  self.a*y.b+self.b*y.a-self.b*y.b)

    __rmul__ = __mul__

    def inverse(self):
        n = self.a*self.a-self.a*self.b-self.b*self.b
        if not n:
            raise ZeroDivisionError()
        return Qp((self.a-self.b)/n, -self.b/n)

    def __truediv__(self, y):
        return self * Qp(y).inverse()

    def __rtruediv__(self, y):
        return Qp(y) * self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** -n
        out, x = Qp(1), self
        while n:
            if n & 1:
                out = out*x
            x = x*x
            n //= 2
        return out

    def __eq__(self, y):
        y = Qp(y)
        return self.a == y.a and self.b == y.b

    def sign(self):
        # 2(a+bp)=(2a-b)+b sqrt(5), exact sign by rational squaring.
        a, b = 2*self.a-self.b, self.b
        s = lambda x: (x > 0)-(x < 0)
        if b == 0:
            return s(a)
        if a == 0:
            return s(b)
        if s(a) == s(b):
            return s(a)
        if b > 0:
            return s(5*b*b-a*a)
        return s(a*a-5*b*b)

    def decimal(self):
        with localcontext() as ctx:
            ctx.prec = 90
            dec = lambda q: Decimal(q.numerator)/Decimal(q.denominator)
            val = dec(self.a)+dec(self.b)*(Decimal(5).sqrt()-1)/2
            return format(val, '.36g')


checks = []


def check(name, proposition):
    if not proposition:
        raise RuntimeError('FAILED: '+name)
    checks.append(name)


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return list(map(list, zip(*a)))


def scaled(c, a):
    return [[c*x for x in row] for row in a]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def det2(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]


def gram(a):
    return mm(tr(a), a)


def normalized_det(w, z):
    n = gram(w)
    a = w[:2]  # initialized embedding is the first two output coordinates
    b = add(scaled(1-z, n), scaled(z, gram(a)))
    return det2(b)/det2(n), det2(b), n


def cnot(v, control, target):
    v = list(v)
    v[target] ^= v[control]
    return tuple(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    pins = json.loads((here/'SOURCE_PINS.json').read_text())
    repo = Path(args.repo)
    for item in pins['sources']:
        got = hashlib.sha256((repo/item['path']).read_bytes()).hexdigest()
        check('source:'+item['path'], got == item['sha256'])

    p = Qp(0, 1)
    check('golden_equation', p*p+p == 1)
    check('positive_embedding', p.sign() == 1 and (1-p).sign() == 1)
    fib = [0, 1]
    for _ in range(21):
        fib.append(fib[-1]+fib[-2])
    check('actual_F20_F21', (fib[20], fib[21]) == (6765, 10946))
    n = 20
    fn, fn1 = fib[n], fib[n+1]
    check('first_crossing_complete', fn*p**(n+1)+fn1*p**n == 1)
    classes = [fn*p**(n+1), fn1*p**(n+2), fn1*p**(n+3),
               fn1*p**(n+3), fn1*p**(n+4)]
    check('five_class_complete', sum(classes, Qp(0)) == 1)
    check('all_five_positive', all(q.sign() == 1 for q in classes))

    z = Qp(F(1, 2**20))
    ell = 4*p**3
    q = 1-z*ell
    rr = 1-z*ell*(1+p**6)
    r0 = 1-q*rr
    check('actual_r0_strict_chart', r0.sign() == 1 and
          (Qp(F(1, 100000))-r0).sign() == 1)
    ready = 2*fn1*p**(n+3)
    check('report_keeps_complete_law', sum(classes[:2], Qp(0))+classes[4]
          +ready*(1-r0)+ready*r0 == 1)
    check('reference_report_complete', p+p*p == 1)
    k = (1-r0)**2+r0**2
    book_click = r0**2/k
    check('squared_law_is_distinct', book_click != r0)
    check('squared_law_click_strictly_smaller', (r0-book_click).sign() == 1)
    check('exact_squared_odds', book_click/(1-book_click) == (r0/(1-r0))**2)
    check('common_scalar_cannot_fix_odds',
          (Qp(7)*r0)**2/(Qp(7)*(1-r0))**2 == (r0/(1-r0))**2)
    unready2 = fn*p**(2*n+2)+fn1*(p**(2*n+4)+p**(2*n+8))
    ready2 = 2*fn1*p**(2*n+6)*k
    n2 = unready2+ready2
    book_ready = ready2/n2
    check('whole_squared_normalizer_positive', n2.sign() == 1)
    check('whole_READY_law_is_distinct', book_ready != ready)
    check('whole_READY_is_strictly_smaller', (ready-book_ready).sign() == 1)

    v = (1, 0, 0)
    ab = cnot(cnot(v, 0, 1), 1, 2)
    ba = cnot(cnot(v, 1, 2), 0, 1)
    check('actual_AB_code_cell', ab == (1, 1, 1))
    check('actual_BA_code_cell', ba == (1, 1, 0))
    check('both_retain_u', ab[1] == ba[1] == 1)

    eye = [[F(1), F(0)], [F(0), F(1)]]
    zero = scaled(F(0), eye)
    early = scaled(F(3, 5), eye)
    late = scaled(F(4, 5), eye)
    # Structural full-rank fixtures with common nonzero early corner.
    # The rational probabilities here are NOT asserted original factory data.
    raw = [early+late+zero, early+zero+late]
    check('raw_complete_isometries', all(gram(w) == eye for w in raw))
    check('same_nonzero_early_corner', raw[0][:2] == raw[1][:2] == early)
    check('late_code_ranges_distinct', raw[0][2:] != raw[1][2:])
    check('late_initialized_corner_zero', all(row == [0, 0]
          for row in zero))
    marked = [early+scaled(F(1, 2), late)+zero,
              early+zero+scaled(F(1, 2), late)]
    expected_n = scaled(F(13, 25), eye)
    check('actual_marked_normalizer_retained',
          all(gram(w) == expected_n for w in marked))
    zz = F(1, 2**20)
    expected_ratio = ((1-zz)+zz*F(9, 13))**2
    for kcode, w in enumerate(marked):
        ratio, rawdet, nmat = normalized_det(w, zz)
        check('normalized_ratio_code_'+str(kcode), ratio == expected_ratio)
        for tag, t in [
            ('scalar', scaled(F(7, 3), eye)),
            ('triangular', [[F(2), F(1)], [F(0), F(1, 3)]]),
            ('nonsymmetric', [[F(3, 2), F(-2, 3)], [F(1, 5), F(4, 3)]])]:
            newratio, newraw, newn = normalized_det(mm(w, t), zz)
            check('right_invariance_'+str(kcode)+'_'+tag, newratio == ratio)
            check('congruence_N_'+str(kcode)+'_'+tag, newn == mm(mm(tr(t), nmat), t))
            check('dropped_denominator_detected_'+str(kcode)+'_'+tag, newraw != rawdet)
    check('complete_code_contrast_zero', normalized_det(marked[0], zz)[0]
          == normalized_det(marked[1], zz)[0])

    # A non-scalar N makes the congruence test genuinely noncommutative.
    base_t = [[F(2), F(1)], [F(0), F(1, 3)]]
    base = mm(marked[0], base_t)
    ns = gram(base)
    tt = [[F(3, 2), F(-2, 3)], [F(1, 5), F(4, 3)]]
    check('noncommutation_control', mm(ns, tt) != mm(tt, ns))
    check('noncommuting_right_invariance',
          normalized_det(mm(base, tt), zz)[0] == normalized_det(base, zz)[0])

    result = {
        'status': 'PASS',
        'input_ref': pins['input_ref'],
        'checks': len(checks),
        'exact_domain': 'Fraction and Q[p]/(p^2+p-1)',
        'display_only': {
            'actual_r0': r0.decimal(), 'actual_READY': ready.decimal(),
            'squared_Book_READY': book_ready.decimal(),
            'squared_Book_click_given_READY': book_click.decimal(),
            'whole_squared_normalizer': n2.decimal()},
        'scope': 'Two distinct executions; scalar READY promotion rejected; same-range initialized-cut repair excluded; other Book/heat terms not identified.',
        'GR_closed': False,
        'passed': checks,
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
