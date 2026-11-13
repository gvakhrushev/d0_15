"""Target-specific numerical Solovay--Kitaev words over the owned SO(3) alphabet.

Only signed letters +/-1,+/-2 are emitted.  +1=R_(0,1)(32 theta_G),
+2=R_(0,2)(32 theta_G), with 2x2 plane block [[cos,-sin],[sin,cos]].
Thus their Hamilton quaternion axes are +z and -y, and the lift angle is
16 theta_G.  Word lists/DAG children are CHRONOLOGICAL: later factors
multiply on the LEFT.  Quaternion signs are identified only as SO(3)
lifts.  No physical primitive, certified error, or admission is supplied.

The finite base net is heuristic, not an asserted covering certificate.
Every reported result is an explicit finite signed word/DAG with its own
high-precision numerical endpoint.  The caller must independently certify
the actual algebraic SO(3) matrix and physical macro expansion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.spatial import cKDTree


def qmul(a, b):
    """Hamilton product a*b; its SO(3) matrix is R(a)R(b)."""
    a0, ax, ay, az = a
    b0, bx, by, bz = b
    return (a0*b0-ax*bx-ay*by-az*bz,
            a0*bx+ax*b0+ay*bz-az*by,
            a0*by-ax*bz+ay*b0+az*bx,
            a0*bz+ax*by-ay*bx+az*b0)


def qinv(q):
    return (q[0], -q[1], -q[2], -q[3])


def qnorm(q):
    return mp.sqrt(sum(x*x for x in q))


def unit(q):
    n = qnorm(q)
    return tuple(x/n for x in q)


def near_identity_lift(q):
    q = unit(q)
    return tuple(-x for x in q) if q[0] < 0 else q


def so3(q):
    w, x, y, z = unit(q)
    return mp.matrix([[1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
                      [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
                      [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]])


def so3_error(qtarget, qactual):
    """SO(3) operator error from the relative quaternion, not 1-dot."""
    q = unit(qmul(qtarget, qinv(unit(qactual))))
    return 2*mp.sqrt(sum(x*x for x in q[1:]))


def np_left_mul(a, bs):
    av = np.asarray(a[1:])
    out = np.empty_like(bs)
    # Explicit three-term contraction avoids stale BLAS float-status warnings.
    out[:, 0] = a[0]*bs[:, 0] - np.sum(bs[:, 1:]*av, axis=1)
    out[:, 1:] = a[0]*bs[:, 1:] + bs[:, 0, None]*av + np.cross(av, bs[:, 1:])
    return out


class BaseNet:
    """Finite reduced words plus a bounded nearest-product query."""
    def __init__(self, generators, depth=11, pivots=128, seed=20261026):
        self.depth = int(depth)
        self.pivot_count = int(pivots)
        signed = (1, -1, 2, -2)
        gf = {s: np.asarray([float(v) for v in generators[s]]) for s in signed}
        quats = [np.asarray([[1., 0., 0., 0.]])]
        parents = [np.asarray([-1], dtype=np.int64)]
        letters = [np.asarray([0], dtype=np.int8)]
        layer_q = quats[0]
        layer_ids = np.asarray([0], dtype=np.int64)
        layer_last = letters[0]
        offset = 1
        for _ in range(self.depth):
            qs, ps, ls = [], [], []
            for s in signed:
                mask = layer_last != -s
                qs.append(np_left_mul(gf[s], layer_q[mask]))
                ps.append(layer_ids[mask])
                ls.append(np.full(int(mask.sum()), s, dtype=np.int8))
            layer_q = np.concatenate(qs)
            if not np.isfinite(layer_q).all():
                raise ArithmeticError('Nonfinite base-net quaternion')
            layer_q /= np.linalg.norm(layer_q, axis=1)[:, None]
            layer_last = np.concatenate(ls)
            layer_ids = np.arange(offset, offset+len(layer_q), dtype=np.int64)
            offset += len(layer_q)
            quats.append(layer_q)
            parents.append(np.concatenate(ps))
            letters.append(layer_last)
        self.q = np.concatenate(quats)
        self.parent = np.concatenate(parents)
        self.last = np.concatenate(letters)
        self.tree = cKDTree(np.concatenate((self.q, -self.q)), compact_nodes=True)
        rng = np.random.default_rng(seed)
        chosen = rng.choice(len(self.q), max(0, self.pivot_count-1), replace=False)
        self.pivots = np.concatenate((np.asarray([0]), chosen))
        self.pq = self.q[self.pivots]
        self.pqi = self.pq.copy()
        self.pqi[:, 1:] *= -1
        self.calls = 0

    def letters(self, index):
        result = []
        while index:
            result.append(int(self.last[index]))
            index = int(self.parent[index])
        result.reverse()
        return tuple(result)

    def approximate(self, target):
        """Find B*A~target; return chronological word(A),word(B)."""
        tf = np.asarray([float(v) for v in unit(target)])
        desired_b = np_left_mul(tf, self.pqi)
        distances, indices = self.tree.query(desired_b, k=1, workers=1)
        winner = int(np.argmin(distances))
        aidx = int(self.pivots[winner])
        bidx = int(indices[winner]) % len(self.q)
        self.calls += 1
        return self.letters(aidx)+self.letters(bidx)


@dataclass(frozen=True)
class Word:
    node: int
    length: int


class SKCompiler:
    def __init__(self, multiplier=32, dps=100, net_depth=11, pivots=128):
        if multiplier != 32:
            raise ValueError('This packet owns only the multiplier-32 alphabet')
        mp.mp.dps = int(dps)
        self.dps = int(dps)
        self.multiplier = multiplier
        self.p = (mp.sqrt(5)-1)/2
        self.a = mp.sqrt(self.p)
        self.theta = mp.atan2(self.p, self.a)
        c, s = mp.cos(multiplier*self.theta/2), mp.sin(multiplier*self.theta/2)
        self.generators = {1: (c, mp.mpf(0), mp.mpf(0), s),
                           2: (c, mp.mpf(0), -s, mp.mpf(0))}
        self.generators[-1] = qinv(self.generators[1])
        self.generators[-2] = qinv(self.generators[2])
        self.nodes = [{'kind': 'seq', 'letters': [], 'length': 0}]
        self.endpoints = [(mp.mpf(1), mp.mpf(0), mp.mpf(0), mp.mpf(0))]
        self.seq_cache = {(): Word(0, 0)}
        self.inv_cache = {0: Word(0, 0)}
        self.compile_cache = {}
        self.max_base_error = mp.mpf(0)
        self.net = BaseNet(self.generators, depth=net_depth, pivots=pivots)

    def sequence(self, letters):
        key = tuple(int(s) for s in letters)
        if any(s not in self.generators for s in key):
            raise ValueError('Unknown alphabet letter')
        # Adjacent exact inverse cancellation is an ordinary word identity.
        reduced = []
        for s in key:
            if reduced and reduced[-1] == -s:
                reduced.pop()
            else:
                reduced.append(s)
        key = tuple(reduced)
        if key in self.seq_cache:
            return self.seq_cache[key]
        q = self.endpoints[0]
        for s in key:
            q = qmul(self.generators[s], q)
        result = Word(len(self.nodes), len(key))
        self.nodes.append({'kind': 'seq', 'letters': list(key), 'length': len(key)})
        self.endpoints.append(q)
        self.seq_cache[key] = result
        return result

    def inverse(self, word):
        if word.node in self.inv_cache:
            return self.inv_cache[word.node]
        node = self.nodes[word.node]
        if node['kind'] == 'inv':
            child = int(node['child'])
            return Word(child, int(self.nodes[child]['length']))
        result = Word(len(self.nodes), word.length)
        self.nodes.append({'kind': 'inv', 'child': word.node, 'length': word.length})
        self.endpoints.append(qinv(self.endpoints[word.node]))
        self.inv_cache[word.node] = result
        self.inv_cache[result.node] = word
        return result

    def concatenate(self, *words):
        children = [w for w in words if w.length]
        if not children:
            return Word(0, 0)
        if len(children) == 1:
            return children[0]
        q = self.endpoints[0]
        for w in children:
            q = qmul(self.endpoints[w.node], q)
        length = sum(w.length for w in children)
        result = Word(len(self.nodes), length)
        self.nodes.append({'kind': 'cat', 'children': [w.node for w in children],
                           'length': length})
        self.endpoints.append(q)
        return result

    def iter_letters(self, word):
        """Expand only when explicitly requested; inverse reverses chronology."""
        stack = [(word.node, False)]
        while stack:
            index, inverse = stack.pop()
            node = self.nodes[index]
            if node['kind'] == 'seq':
                seq = node['letters']
                yield from (-s for s in reversed(seq)) if inverse else seq
            elif node['kind'] == 'inv':
                stack.append((int(node['child']), not inverse))
            else:
                cs = node['children']
                stack.extend((int(i), inverse) for i in (cs if inverse else reversed(cs)))

    @staticmethod
    def balanced_commutator(residual):
        """Return v,w with v*w*v^-1*w^-1=residual in the near+I lift."""
        r = near_identity_lift(residual)
        rv = mp.sqrt(sum(x*x for x in r[1:]))
        if not rv:
            identity = (mp.mpf(1), mp.mpf(0), mp.mpf(0), mp.mpf(0))
            return identity, identity
        # sin(phi)^2=sin(eta/2), where cos(eta)=r[0].
        s2 = rv/mp.sqrt(2*(1+r[0]))
        s = mp.sqrt(s2)
        c = mp.sqrt(1-s2)
        v0 = (c, s, mp.mpf(0), mp.mpf(0))
        w0 = (c, mp.mpf(0), s, mp.mpf(0))
        comm = qmul(qmul(qmul(v0, w0), qinv(v0)), qinv(w0))
        axis0 = tuple(x/rv for x in comm[1:])
        axis1 = tuple(x/rv for x in r[1:])
        dot = sum(x*y for x, y in zip(axis0, axis1))
        cross = (axis0[1]*axis1[2]-axis0[2]*axis1[1],
                 axis0[2]*axis1[0]-axis0[0]*axis1[2],
                 axis0[0]*axis1[1]-axis0[1]*axis1[0])
        if 1+dot > mp.mpf(10)**(-mp.mp.dps//2):
            align = unit((1+dot, *cross))
        else:
            # An explicit pi rotation about a perpendicular axis.
            k = min(range(3), key=lambda i: abs(axis0[i]))
            e = tuple(mp.mpf(int(i == k)) for i in range(3))
            perp = (axis0[1]*e[2]-axis0[2]*e[1],
                    axis0[2]*e[0]-axis0[0]*e[2],
                    axis0[0]*e[1]-axis0[1]*e[0])
            align = unit((mp.mpf(0), *perp))
        return (qmul(qmul(align, v0), qinv(align)),
                qmul(qmul(align, w0), qinv(align)))

    def compile(self, target, depth):
        target = near_identity_lift(target)
        key = (int(depth), tuple(mp.nstr(v, self.dps-8) for v in target))
        if key in self.compile_cache:
            return self.compile_cache[key]
        if depth == 0:
            result = self.sequence(self.net.approximate(target))
            self.max_base_error = max(self.max_base_error,
                                      so3_error(target, self.endpoints[result.node]))
        else:
            previous = self.compile(target, depth-1)
            residual = near_identity_lift(qmul(target, qinv(self.endpoints[previous.node])))
            if mp.sqrt(sum(v*v for v in residual[1:])) < mp.mpf(10)**(-self.dps+20):
                result = previous
            else:
                v, w = self.balanced_commutator(residual)
                vh, wh = self.compile(v, depth-1), self.compile(w, depth-1)
                # Endpoint [vh,wh]*previous: chronological previous,w^-1,v^-1,w,v.
                improved = self.concatenate(previous, self.inverse(wh), self.inverse(vh), wh, vh)
                result = min((previous, improved),
                             key=lambda a: so3_error(target, self.endpoints[a.node]))
        self.compile_cache[key] = result
        return result

    def target_plane01(self, angle):
        return (mp.cos(angle/2), mp.mpf(0), mp.mpf(0), mp.sin(angle/2))

    def numerical_report(self, name, target, word, depth):
        q = self.endpoints[word.node]
        error = so3_error(target, q)
        return {'name': name, 'depth': depth, 'root': word.node,
                'abstract_letter_length': word.length,
                'SO3_operator_error_numerical': mp.nstr(error, 45),
                'error_times_abstract_length': mp.nstr(error*word.length, 45),
                'endpoint_quaternion': [mp.nstr(v, self.dps) for v in q],
                'endpoint_SO3': [[mp.nstr(v, self.dps) for v in row]
                                 for row in so3(q).tolist()]}

    def bundle(self, reports):
        reachable = set()
        stack = [int(r['root']) for r in reports]
        while stack:
            i = stack.pop()
            if i in reachable:
                continue
            reachable.add(i)
            node = self.nodes[i]
            stack.extend(node.get('children', []))
            if 'child' in node:
                stack.append(node['child'])
        ordered = sorted(reachable)
        remap = {old: new for new, old in enumerate(ordered)}
        output_nodes = []
        for old in ordered:
            n = dict(self.nodes[old])
            if 'children' in n:
                n['children'] = [remap[v] for v in n['children']]
            if 'child' in n:
                n['child'] = remap[n['child']]
            output_nodes.append(n)
        output_reports = []
        for r in reports:
            out = dict(r)
            out['root'] = remap[int(out['root'])]
            output_reports.append(out)
        return {'schema': 'd0.so3-sk-signed-word/1',
                'semantics': 'chronological children; later matrices multiply on left',
                'alphabet': {'1': 'R01(32 theta_G)', '2': 'R02(32 theta_G)',
                             '-1': 'inverse of1', '-2': 'inverse of2'},
                'theta_G': mp.nstr(self.theta, self.dps),
                'generator_quaternions': {str(k): [mp.nstr(v, self.dps) for v in q]
                                         for k, q in self.generators.items()},
                'dps': self.dps, 'net_depth': self.net.depth,
                'net_points': len(self.net.q), 'net_product_pivots': len(self.net.pivots),
                'net_calls': self.net.calls,
                'max_base_SO3_error_numerical': mp.nstr(self.max_base_error, 30),
                'certified_error': False, 'physical_admission': False,
                'nodes': output_nodes, 'targets': output_reports}


def meaningful_convention_checks(compiler):
    tolerance = mp.mpf(10)**(-compiler.dps+20)
    c, s = mp.cos(32*compiler.theta), mp.sin(32*compiler.theta)
    assert mp.norm(so3(compiler.generators[1])-mp.matrix([[c,-s,0],[s,c,0],[0,0,1]])) < tolerance
    assert mp.norm(so3(compiler.generators[2])-mp.matrix([[c,0,-s],[0,1,0],[s,0,c]])) < tolerance
    a = compiler.sequence((1,2,-1))
    assert tuple(compiler.iter_letters(compiler.inverse(a))) == (1,-2,-1)
    direct = compiler.endpoints[0]
    for letter in compiler.iter_letters(a):
        direct = qmul(compiler.generators[letter], direct)
    assert so3_error(direct, compiler.endpoints[a.node]) < tolerance
    for target in (compiler.target_plane01(mp.mpf('.003')), unit((1, .002, -.003, .001))):
        v, w = compiler.balanced_commutator(target)
        actual = qmul(qmul(qmul(v,w),qinv(v)),qinv(w))
        assert so3_error(target,actual) < tolerance


def verify_bundle_matrix(bundle, dps=150):
    """Independent numeric endpoint check from embedded native G**32.

    Uses only the serialized signed-word DAG and ordinary 3x3 matrices;
    no recursive compiler, quaternion endpoint, half-angle, or Euler
    decomposition is used.  These are numerical bounds, not intervals.
    """
    with mp.workdps(dps):
        p = (mp.sqrt(5)-1)/2
        a = mp.sqrt(p)
        g1 = mp.matrix([[a,-p,0],[p,a,0],[0,0,1]])**32
        g2 = mp.matrix([[a,0,-p],[0,1,0],[p,0,a]])**32
        alphabet = {1:g1, -1:g1.T, 2:g2, -2:g2.T}
        endpoints = []
        lengths = []
        for index, node in enumerate(bundle['nodes']):
            kind = node['kind']
            if kind == 'seq':
                u = mp.eye(3)
                for letter in node['letters']:
                    if type(letter) is not int or letter not in alphabet:
                        raise ValueError('Malformed serialized signed letter')
                    u = alphabet[letter]*u
                length = len(node['letters'])
            elif kind == 'inv':
                child = int(node['child'])
                if child >= index:
                    raise ValueError('DAG is not topologically ordered')
                u = endpoints[child].T
                length = lengths[child]
            elif kind == 'cat':
                u, length = mp.eye(3), 0
                for child in node['children']:
                    if type(child) is not int or child >= index:
                        raise ValueError('DAG is not topologically ordered')
                    u = endpoints[child]*u
                    length += lengths[child]
            else:
                raise ValueError('Unknown serialized node kind')
            if length != node['length']:
                raise ValueError('Incorrect expanded length')
            endpoints.append(u)
            lengths.append(length)
        targets = {'theta_G':mp.matrix([[a,-p,0],[p,a,0],[0,0,1]]),
                   'quarter':mp.matrix([[0,-1,0],[1,0,0],[0,0,1]])}
        result = []
        for report in bundle['targets']:
            u = endpoints[report['root']]
            difference = u-targets[report['name']]
            frobenius = mp.sqrt(sum(v*v for v in difference))
            result.append({'name':report['name'],
                'abstract_letter_length':lengths[report['root']],
                'independent_matrix_Frobenius_error_numerical':mp.nstr(frobenius,55),
                'independent_error_times_abstract_length':mp.nstr(frobenius*lengths[report['root']],55),
                'orthogonality_Frobenius_residual':mp.nstr(mp.norm(u.T*u-mp.eye(3)),15)})
        return {'dps':dps, 'method':'direct 3x3 native Golden powers and serialized DAG',
                'is_interval_certificate':False, 'targets':result}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--net-depth', type=int, default=11)
    p.add_argument('--pivots', type=int, default=128)
    p.add_argument('--dps', type=int, default=100)
    p.add_argument('--levels', type=int, default=7)
    p.add_argument('--tol', default='1e-24')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    started = time.monotonic()
    compiler = SKCompiler(dps=args.dps, net_depth=args.net_depth, pivots=args.pivots)
    meaningful_convention_checks(compiler)
    reports = []
    for name, angle in (('theta_G', compiler.theta), ('quarter', mp.pi/2)):
        target = compiler.target_plane01(angle)
        report = None
        for depth in range(args.levels+1):
            word = compiler.compile(target, depth)
            report = compiler.numerical_report(name, target, word, depth)
            print(json.dumps({k: report[k] for k in ('name','depth','abstract_letter_length',
                  'SO3_operator_error_numerical','error_times_abstract_length')}), flush=True)
            if mp.mpf(report['SO3_operator_error_numerical']) <= mp.mpf(args.tol):
                break
        reports.append(report)
    bundle = compiler.bundle(reports)
    bundle['independent_matrix_verification'] = verify_bundle_matrix(bundle, max(150,args.dps+40))
    bundle['elapsed_seconds'] = time.monotonic()-started
    bundle['compiler_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if args.output:
        args.output.write_text(json.dumps(bundle, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'status': 'NUMERICAL_WORDS_RETURNED',
                      'elapsed_seconds': bundle['elapsed_seconds'],
                      'DAG_nodes': len(bundle['nodes']),
                      'net_calls': compiler.net.calls,
                      'independent_interval_certificate_required': True}), flush=True)


if __name__ == '__main__':
    main()
