#!/usr/bin/env python3
"""Exact finite controls for the retained determinant-verification theorem.

The general entropy, compiler minimum and Gelfond--Schneider arguments are
analytical. These controls test the actual exterior no-click construction,
its complete outcome derivatives, finite stopped records and Golden anchor.
Only Python's standard library is used. No assertion is disabled by -O.
"""
from fractions import Fraction as Q
from itertools import combinations, product
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def zeros(n, m):
    return [[Q(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    a = zeros(n, n)
    for i in range(n):
        a[i][i] = Q(1)
    return a


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def givens(n, i, j, c, s):
    require(c*c+s*s == 1, "nonunitary Givens input")
    a = eye(n)
    a[i][i] = a[j][j] = c
    a[i][j], a[j][i] = -s, s
    return a


def kron(a, b):
    return [[a[i][j]*b[k][ell] for j in range(len(a[0]))
             for ell in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def det2(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]


def inv2(a):
    d = det2(a)
    require(d != 0, "singular 2x2 pencil")
    return [[a[1][1]/d, -a[0][1]/d],
            [-a[1][0]/d, a[0][0]/d]]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), Q(0))


def wedge2(v, dv):
    result = []
    for i, j in combinations(range(len(v)), 2):
        a = v[i][0]*v[j][1]-v[i][1]*v[j][0]
        da = (dv[i][0]*v[j][1]+v[i][0]*dv[j][1]
              -dv[i][1]*v[j][0]-v[i][1]*dv[j][0])
        result.append(((i, j), a, da))
    return result


def exterior_control():
    u = mm(givens(4, 0, 1, Q(8,17), Q(15,17)),
           mm(givens(4, 0, 2, Q(3,5), Q(4,5)),
              givens(4, 1, 3, Q(5,13), Q(12,13))))
    require(mm(transpose(u), u) == eye(4), "original query not unitary")
    cut = zeros(4, 4)
    cut[1][1] = cut[2][2] = Q(1)
    z = Q(9,25)
    # A fixed efficiency, acting only on the original Q cut. No sqrt(F).
    no = add(eye(4), scale(Q(-1,5), cut))
    yes = scale(Q(3,5), cut)
    frame = [row[:2] for row in u]
    f = mm(transpose(frame), mm(cut, frame))
    pencil = add(eye(2), scale(-z, f))
    d = det2(pencil)
    require(0 < d < 1 and f[0][1] != 0, "degenerate fixture")
    for first, second in [(0,1), (2,3)]:
        generator = zeros(4, 4)
        generator[first][second] = Q(1)
        generator[second][first] = Q(-1)
        du = mm(generator, u)
        dframe = [row[:2] for row in du]
        v = mm(no, frame) + mm(yes, frame)
        dv = mm(no, dframe) + mm(yes, dframe)
        outputs = wedge2(v, dv)
        require(len(outputs) == 28, "missing occupation outcome")
        require(sum((a*a for _, a, _ in outputs), Q(0)) == 1,
                "full exterior probability not one")
        require(sum((2*a*da for _, a, da in outputs), Q(0)) == 0,
                "full output derivative not normalized")
        no_click = [r for r in outputs if max(r[0]) < 4]
        direct_d = sum((a*a for _, a, _ in no_click), Q(0))
        direct_dd = sum((2*a*da for _, a, da in no_click), Q(0))
        df = add(mm(transpose(dframe), mm(cut, frame)),
                 mm(transpose(frame), mm(cut, dframe)))
        require(direct_d == d, "exterior event differs from full determinant")
        require(direct_dd == -z*d*trace(mm(inv2(pencil), df)),
                "complete event first source differs from logdet source")
        require(direct_dd != 0, "fixture does not test a source")
        # Off-shell query variations do not commute in the original carrier.
        require(mm(f, df) != mm(df, f), "fixture variation is commuting")
    return d


def native_block_control():
    # The original 4-tail x 2-scene block, not a chosen eigenmode model.
    e, b, z = Q(9,25), Q(25,169), Q(9,25)
    rr, ss, cc, tt = Q(4,5), Q(3,5), Q(12,13), Q(5,13)
    tail = [[rr,0,-ss,0], [0,rr,0,-ss],
            [0,ss,0,rr], [ss,0,rr,0]]
    scene = [[cc,-tt], [tt,cc]]
    step = kron(tail, scene)
    u = mm(step, step)
    require(mm(transpose(u), u) == eye(8), "original 8D block not unitary")
    retained = [0, 2]
    frame = [[row[i] for i in retained] for row in u]
    compressed = [frame[i] for i in retained]
    require(compressed == scale(1-2*b, [[1-e,-e],[-e,1-e]]),
            "actual native return compression")
    cut = eye(8)
    for i in retained:
        cut[i][i] = Q(0)
    f = mm(transpose(frame), mm(cut, frame))
    first = 4*b*(1-b)
    second = 4*e*(1-e)+(1-4*e*(1-e))*first
    require(trace(f) == first+second and det2(f) == first*second,
            "actual two-band source was not preserved")
    no = add(eye(8), scale(Q(-1,5), cut))
    yes = scale(Q(3,5), cut)
    v = mm(no, frame)+mm(yes, frame)
    outcomes = wedge2(v, zeros(16,2))
    require(len(outcomes) == 120, "native occupation outputs omitted")
    require(sum((a*a for _,a,_ in outcomes), Q(0)) == 1,
            "native exterior full-state normalization")
    no_click = sum((a*a for ix,a,_ in outcomes if max(ix) < 8), Q(0))
    require(no_click == (1-z*first)*(1-z*second),
            "fixed single-particle efficiency is not the original determinant")
    wrong_shared_coin = (1-z)+z*(1-first)*(1-second)
    require(wrong_shared_coin-no_click == z*(1-z)*first*second > 0,
            "one shared attempt coin must not masquerade as per-mode efficiency")


def stopped_control(d):
    q = 1-d
    for n in [1, 2, 3, 7, 12]:
        # All successes and the terminal unresolved record remain present.
        records = [(d*q**k, -q**k + (d*k*q**(k-1) if k else 0),
                    k+1, 1, k) for k in range(n)]
        records.append((q**n, n*q**(n-1), n, 0, n))
        require(sum((r[0] for r in records), Q(0)) == 1,
                "stopped distribution loses unresolved output")
        require(sum((r[1] for r in records), Q(0)) == 0,
                "stopped law derivative not normalized")
        e = sum((q**k for k in range(n)), Q(0))
        ep = sum((k*q**(k-1) for k in range(1,n)), Q(0))
        require(sum((prob*ticks for prob, _, ticks, _, _ in records), Q(0)) == e,
                "real stopped clock differs from geometric sum")
        # log(probability)=is_success*log(d)+failures*log(q).
        # Comparing its exact coefficients tests entropy without floating logs.
        require(sum((prob*success for prob, _, _, success, _ in records), Q(0)) == d*e,
                "success log coefficient in complete entropy")
        require(sum((prob*failures for prob, _, _, _, failures in records), Q(0)) == q*e,
                "failure log coefficient in complete entropy")
        require(sum((dp*success for _, dp, _, success, _ in records), Q(0)) == d*ep-e,
                "full-record first source: log d coefficient")
        require(sum((dp*failures for _, dp, _, _, failures in records), Q(0)) == q*ep+e,
                "full-record first source: log q coefficient")
        require(e-d*ep == n*q**(n-1), "finite horizon telescoping identity")
class Golden:
    """Exact a+b*p, p^2+p-1=0, with the actual positive p embedding."""
    def __init__(self, a=0, b=0):
        self.a, self.b = Q(a), Q(b)

    @staticmethod
    def cast(x):
        return x if isinstance(x, Golden) else Golden(x)

    def __add__(self, other):
        other = self.cast(other)
        return Golden(self.a+other.a, self.b+other.b)
    __radd__ = __add__

    def __neg__(self):
        return Golden(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-self.cast(other))

    def __rsub__(self, other):
        return self.cast(other) + (-self)

    def __mul__(self, other):
        other = self.cast(other)
        return Golden(self.a*other.a+self.b*other.b,
                      self.a*other.b+self.b*other.a-self.b*other.b)
    __rmul__ = __mul__

    def conjugate(self):
        return Golden(self.a-self.b, -self.b)

    def __truediv__(self, other):
        other = self.cast(other)
        norm = other*other.conjugate()
        require(norm.b == 0 and norm.a != 0, "invalid Golden denominator")
        v = self*other.conjugate()
        return Golden(v.a/norm.a, v.b/norm.a)

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, "noninteger Golden power")
        out, x = Golden(1), self
        while n:
            if n & 1:
                out = out*x
            x = x*x
            n //= 2
        return out

    def __eq__(self, other):
        other = self.cast(other)
        return self.a == other.a and self.b == other.b

    def sign(self):
        # a+b*p = (a-b/2)+(b/2)*sqrt(5).
        a, b = self.a-self.b/2, self.b/2
        if b == 0:
            return (a > 0)-(a < 0)
        if a == 0:
            return (b > 0)-(b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        delta = a*a-5*b*b
        require(delta != 0, "unexpected sqrt(5) rational equality")
        return ((delta > 0)-(delta < 0))*(1 if a > 0 else -1)


def golden_control():
    p = Golden(0,1)
    z = Q(1, 2**20)
    low, high = 4*p**3, 1-p**12
    require(low == 1-p**6, "Golden lower band")
    require(high == low*(1+p**6), "Golden upper band")
    a = (1-z*low)*(1-z*high)
    require(a+a.conjugate() == 2+336*z+5440*z*z,
            "native trace needed for conjugate separation")
    require((a-1).sign() < 0 and a.sign() > 0 and
            (a.conjugate()-1).sign() > 0, "native anchor domains")
    for m in [1, 2, 5, 528]:
        d = a**m
        q = 1-d
        require(d.b != 0 and q.b != 0, "native anchor became rational")
        require((d+d.conjugate()-2).sign() > 0,
                "native conjugate sum does not exceed two")
        require((q+q.conjugate()).sign() < 0, "q conjugate is not below -q")
    # Finite controls of the general rational-function irrationality lemma.
    q = 1-a
    for n in [2, 3, 4, 7, 8, 11]:
        ep = sum((k*q**(k-1) for k in range(1,n)), Golden())
        rr = n*q**(n-1)/ep
        require(rr.b != 0 and rr.sign() > 0, "R_N needs algebraic irrationality")
        require(rr != rr.conjugate(), "Gelfond--Schneider exponent lost irrationality")


def uniform_gap_control():
    # Rigorous rational enclosure; no floating logarithms or precision floor.
    lo, hi, z = Q(309,500), Q(6181,10000), Q(1,2**20)

    def q_at(x):
        low = 4*x**3
        high = low*(1+x**6)
        return z*(low+high)-z*z*low*high

    require(lo*lo+lo < 1 < hi*hi+hi, "p is not bracketed")
    require(q_at(hi)**5 < lo**137, "threshold must exceed 27.4")
    require(hi**549 < q_at(lo)**20, "base threshold must be below 27.45")
    require(q_at(hi) < Q(1,2**19), "local no-click deficit bound")
    require(Q(55,2**19) < Q(1,20), "finite-horizon threshold correction")
    require(Q(2,5)*(1-Q(1,2**19)) > Q(39,100),
            "uniform integer-price source gap")


def owned_history_partition_control():
    # Actual original complete tripartite scene, not a new transition model.
    groups = [0]*9 + [1]*11 + [2]*13
    edges = [[int(a != b) for b in groups] for a in groups]
    require(sum(map(sum, edges)) == 718, "original K913 edge carrier")
    paths = [(v,w) for v in range(33) for w in range(33)
             if edges[0][v] and edges[v][w]]
    via11 = sum(groups[v] == 1 for v,_ in paths)
    via13 = sum(groups[v] == 2 for v,_ in paths)
    require((len(paths), via11, via13) == (502,242,260),
            "original two-step continuation counts")
    p = Golden(0,1)
    normalizer = len(paths)*p**2
    require(p**2/normalizer == Q(1,502),
            "fixed-length common Golden factor did not cancel")
    require(via11*p**2/normalizer == Q(121,251) and
            via13*p**2/normalizer == Q(130,251),
            "native zone law is the exact suffix-count ratio")

    # Full Golden forbid-11 cylinders differ already at depth three
    # from the Fibonacci mechanical-word factors (slope p^2).
    full_language = {''.join(w) for w in product('01',repeat=3)
                     if '11' not in ''.join(w)}
    require(full_language == {'000','001','010','100','101'},
            "Golden full-cylinder support")
    alpha = p**2
    require((3*alpha-1).sign() > 0 and (2-3*alpha).sign() > 0,
            "every length-three mechanical factor has at least one 1")
    cuts = [Golden(0), 2*p-1, p, 3*p-1, Golden(1)]
    require(all((cuts[i+1]-cuts[i]).sign() > 0 for i in range(4)),
            "exact mechanical-word intercept partition")

    def golden_floor(x):
        out = 0
        while (x-(out+1)).sign() >= 0:
            out += 1
        return out

    samples = cuts[:-1]+[(cuts[i]+cuts[i+1])/2 for i in range(4)]
    sturmian = {''.join(str(golden_floor(r+(n+1)*alpha)-
                             golden_floor(r+n*alpha)) for n in range(3))
                for r in samples}
    require(sturmian == {'001','010','100','101'} and
            sturmian != full_language, "distinct owned cylinder languages")


def main():
    d = exterior_control()
    native_block_control()
    stopped_control(d)
    golden_control()
    uniform_gap_control()
    owned_history_partition_control()
    print(json.dumps({
        'status':'PASS',
        'generic_complete_exterior_outcomes':28,
        'original_8D_block_complete_exterior_outcomes':120,
        'original_fixed_rank_two_return_cut_and_bands':True,
        'shared_coin_countercontrol':True,
        'noncommuting_full_query_source_directions':2,
        'fixed_efficiency_no_moving_sqrt_F':True,
        'all_stopped_success_and_unresolved_records':True,
        'exact_complete_entropy_log_coefficients':True,
        'native_golden_anchor_and_conjugate_separation':True,
        'uniform_local_source_gap_over_all_integer_costs':'> 39/100 (analytical all-N bound)',
        'original_K913_two_step_counts':[502,242,260],
        'fixed_length_Golden_weight_cancels':True,
        'full_Golden_and_Sturmian_depth_three_supports_differ':True,
        'Book_residual_Beatty_average':'Not defined by the supplied owners: physical price table and a compatible history map are missing.',
        'arithmetic':'rational matrices and Q(p), p^2+p-1=0',
        'general_nonvanishing_method':'analytical Gelfond--Schneider theorem',
        'scope':'Declared binary stopping task, retained pure conditional work and integer stage costs.',
        'native_exterior_admission_proved':False,
        'compulsory_task_selected':False,
        'GR_closed':False
    }, indent=2))


if __name__ == '__main__':
    main()
