#!/usr/bin/env python3
"""Original full-CAR R2 geometric and two-copy matter tensor polynomials.

Multiplication denotes disjoint-copy tensor multiplication, never multiplication
of moment operators on the same copy. Addition pads with identities separately
in Choi and matter slots. The scalar evaluator is the identical-copy moment.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import json

ORDER = (0, 2, 3, 1)
ETA = ((0, 1, 0, 0), (1, 0, 0, 0), (0, 0, -1, 0), (0, 0, 0, -1))


def parity(order):
    return (-1)**sum(order[i] > order[j] for i in range(len(order))
                     for j in range(i+1, len(order)))


def masks(mask):
    return [i for i in ORDER if mask & (1 << i)]


def det_plain(matrix):
    n = len(matrix)
    return sum(parity(p) * product(matrix[i][p[i]] for i in range(n))
               for p in permutations(range(n)))


def product(xs):
    out = 1
    for x in xs:
        out *= x
    return out


def exterior_plain(matrix):
    return [[det_plain([[matrix[r][c] for c in masks(j)] for r in masks(i)])
             if len(masks(i)) == len(masks(j)) else 0 for j in range(16)]
            for i in range(16)]


class Circuit:
    def __init__(self):
        self.nodes = []
        self.cache = {}
        self.zero = self.constant(0)
        self.one = self.constant(1)

    def intern(self, key, node):
        if key not in self.cache:
            self.cache[key] = len(self.nodes)
            self.nodes.append(node)
        return self.cache[key]

    def constant(self, a, b=0):
        a, b = F(a), F(b)
        return self.intern(('const', a, b), {'op': 'const', 'a': str(a),
                                           'b': str(b), 'degree': [0, 0]})

    def variable(self, name, kind):
        return self.intern(('var', name), {'op': 'var', 'name': name,
                           'kind': kind, 'degree': [0, 1] if kind == 'matter_X' else [1, 0]})

    def add(self, *args):
        args = tuple(x for x in args if x != self.zero)
        if not args:
            return self.zero
        if len(args) == 1:
            return args[0]
        # Do not commute nonidentical copy roles or rewrite retained occurrences.
        degree = [max(self.nodes[x]['degree'][j] for x in args) for j in range(2)]
        return self.intern(('add', args), {'op': 'add', 'args': args, 'degree': degree})

    def mul(self, *args):
        if self.zero in args:
            return self.zero
        args = tuple(x for x in args if x != self.one)
        if not args:
            return self.one
        if len(args) == 1:
            return args[0]
        degree = [sum(self.nodes[x]['degree'][j] for x in args) for j in range(2)]
        return self.intern(('mul', args), {'op': 'mul', 'args': args, 'degree': degree})

    def scale(self, a, node):
        return self.mul(self.constant(a), node)

    def sub(self, x, y):
        return self.add(x, self.scale(-1, y))

    def identity(self, n):
        return [[self.one if i == j else self.zero for j in range(n)] for i in range(n)]

    def matrix_constant(self, matrix):
        return [[self.constant(x) for x in row] for row in matrix]

    def mm(self, a, b):
        return [[self.add(*(self.mul(a[i][k], b[k][j]) for k in range(len(b))))
                 for j in range(len(b[0]))] for i in range(len(a))]

    def matrix_sum(self, *terms):
        return [[self.add(*(t[i][j] for t in terms)) for j in range(len(terms[0][0]))]
                for i in range(len(terms[0]))]

    def matrix_scale(self, a, matrix):
        return [[self.scale(a, x) for x in row] for row in matrix]

    def sharp(self, matrix, eta):
        return self.mm(self.mm(eta, list(map(list, zip(*matrix)))), eta)

    def r2(self, matrix, eta):
        h = self.matrix_sum(self.mm(self.sharp(matrix, eta), matrix),
                            self.matrix_scale(-1, self.identity(4)))
        correction = self.matrix_sum(self.identity(4), self.matrix_scale(F(-1, 2), h),
                                     self.matrix_scale(F(3, 8), self.mm(h, h)))
        return self.mm(matrix, correction)

    def determinant(self, matrix):
        n = len(matrix)
        return self.add(*(self.scale(parity(p), self.mul(*(matrix[i][p[i]] for i in range(n))))
                          for p in permutations(range(n))))

    def exterior(self, matrix):
        return [[self.determinant([[matrix[r][c] for c in masks(j)] for r in masks(i)])
                 if len(masks(i)) == len(masks(j)) else self.zero for j in range(16)]
                for i in range(16)]


def build():
    c = Circuit()
    eta = c.matrix_constant(ETA)
    heta = c.matrix_constant(exterior_plain(ETA))
    u = [[c.variable(f'u/{r}/{i}', 'choi_coframe') for i in range(4)] for r in range(4)]
    creators = []
    for r in range(4):
        matrix = [[c.zero]*16 for _ in range(16)]
        for inp in range(16):
            for i in range(4):
                if not inp & (1 << i):
                    sign = (-1)**sum(bool(inp & (1 << j)) for j in ORDER[:ORDER.index(i)])
                    matrix[inp | (1 << i)][inp] = c.scale(sign, u[r][i])
        creators.append(matrix)
    links = {}
    link_targets = {}
    for location, role in [('base', r) for r in range(4)] + [
            (f'plus{r}', s) for r in range(4) for s in range(4) if r != s]:
        key = (location, role)
        matrix = [[c.variable(f'M/{location}/{role}/{i}/{j}', 'choi_link')
                   for j in range(4)] for i in range(4)]
        projected = c.r2(matrix, eta)
        lifted = c.exterior(projected)
        links[key] = lifted
        link_targets[f'{location}/{role}'] = {'raw': matrix, 'R2': projected, 'exterior': lifted}
    faces = []
    for r in range(4):
        for s in range(r+1, 4):
            # The inverse slot is the owning polynomial sharp, not a matrix inverse off SO.
            plaquette = c.mm(c.mm(c.mm(links['base', r], links[f'plus{r}', s]),
                                   c.sharp(links[f'plus{s}', r], heta)),
                             c.sharp(links['base', s], heta))
            d = c.matrix_sum(c.mm(creators[r], c.sharp(creators[s], heta)),
                             c.matrix_scale(-1, c.mm(creators[s], c.sharp(creators[r], heta))))
            trace = c.add(*(c.mul(d[i][j], plaquette[j][i])
                            for i in range(16) for j in range(16)))
            faces.append({'roles': [r, s], 'root': c.scale(F(-1, 8), trace),
                          'links': [['base', r], [f'plus{r}', s],
                                    [f'plus{s}', r], ['base', s]]})
    # h=1/4, nu=3/5. Inverse PF is applied once outside both roots.
    geometric = c.scale(F(400, 9), c.add(*(f['root'] for f in faces)))
    matter_x = {f'{loc}/{a}': c.variable(f'X/{loc}/{a}', 'matter_X')
                for loc in ['base'] + [f'plus{r}' for r in range(4)] for a in (0, 15)}
    terms = []
    for a in (0, 15):
        for r in range(4):
            for s in range(4):
                metric = c.add(*(c.scale(ETA[i][j], c.mul(u[r][i], u[s][j]))
                                 for i in range(4) for j in range(4) if ETA[i][j]))
                dr = c.sub(matter_x[f'plus{r}/{a}'], matter_x[f'base/{a}'])
                ds = c.sub(matter_x[f'plus{s}/{a}'], matter_x[f'base/{a}'])
                terms.append(c.mul(metric, dr, ds))
    # Psi=(S/(2 sqrt(p))) <X>, S=256. Thus S²/(4p nu² h²), 1/p=1+p.
    matter = c.mul(c.constant(F(256**2*100, 9), F(256**2*100, 9)), c.add(*terms))
    assert c.nodes[geometric]['degree'] == [82, 0]
    assert c.nodes[matter]['degree'] == [2, 2]
    return {'schema': 'd0-original-source-tensor-dag-v1', 'scope': 'one genuine local stencil; not a native writer',
            'constants': {'h': '1/4', 'nu': '3/5', 'CAR_sites_S': 256, 'julia_dimension_d': 32,
                          'golden': 'p^2+p=1, 0<p<1', 'eta': ETA, 'creator_order': ORDER},
            'roots': {'H_f_before_inverse_PF': geometric, 'H_q_before_inverse_PF': matter},
            'faces': faces, 'link_nodes': link_targets, 'nodes': c.nodes,
            'tensor_semantics': 'each multiplication concatenates disjoint Choi and disjoint matter slots; add pads identities at the right within each type; factor regrouping is a mathematical permutation, not a free native gate',
            'leaf_semantics': {'choi_coframe': 'Ad/2 (|anchor><a,0,grade1_i|+adjoint), expectation u_i',
                               'choi_link': 'Ad (|anchor><a,grade1_j,grade1_i|+adjoint), expectation M_ij from J(Lambda(M)/2)',
                               'matter_X': '(|site,1><site,A|+adjoint) tensor I_RIGHT, full norm 1'},
            'inverse_PF': 'multiply each conditional site root by its actual 1/rho_x exactly once',
            'physical_C_closed': False, 'GR_closed': False}


def evaluate(dag, variables, p, gradient=False):
    values = []
    for n in dag['nodes']:
        if n['op'] == 'const':
            value = float(F(n['a'])) + float(F(n['b']))*p
        elif n['op'] == 'var':
            value = variables[n['name']]
        elif n['op'] == 'add':
            value = sum(values[k] for k in n['args'])
        else:
            value = product(values[k] for k in n['args'])
        values.append(value)
    output = {}
    for name, root in dag['roots'].items():
        output[name] = {'value': values[root]}
        if gradient:
            adj = [0.0]*len(values)
            adj[root] = 1.0
            for i in range(len(values)-1, -1, -1):
                if adj[i] == 0:
                    continue
                n = dag['nodes'][i]
                if n['op'] == 'add':
                    for k in n['args']:
                        adj[k] += adj[i]
                elif n['op'] == 'mul':
                    args = n['args']
                    for j, k in enumerate(args):
                        adj[k] += adj[i]*product(values[t] for l, t in enumerate(args) if l != j)
            output[name]['gradient'] = {n['name']: adj[i] for i, n in enumerate(dag['nodes'])
                                       if n['op'] == 'var'}
    return output


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    result = build()
    (here/'SOURCE_TENSOR_DAG.json').write_text(json.dumps(result, separators=(',', ':'))+'\n')
    print(json.dumps({'nodes': len(result['nodes']), 'link_operands': len(result['link_nodes']),
                      'leaves': sum(n['op'] == 'var' for n in result['nodes']),
                      'root_degrees': {k: result['nodes'][v]['degree'] for k, v in result['roots'].items()}}))
