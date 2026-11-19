"""Exact compressed selector and a reversible Boolean compiler for all 2^36 tapes."""
from bisect import bisect_right
from fractions import Fraction
from functools import lru_cache
from itertools import accumulate
from math import comb, lcm
from random import Random
from mpmath import iv
import json

from check_boundary_experiment import Golden

ZERO, ONE, P = Golden(0), Golden(1), Golden(0, 1)

class MultiDiagram:
    def __init__(self):
        self.nodes, self.unique = {}, {}

    def node(self, depth, low, high):
        if low == high:
            return low
        key=(depth,low,high)
        if key not in self.unique:
            ident=9+len(self.nodes)
            self.unique[key]=ident
            self.nodes[ident]=key
        return self.unique[key]

    @lru_cache(None)
    def hits(self, remaining):
        return int(remaining==0) if remaining<=0 else self.hits(remaining-1)+self.hits(remaining-2)

    def compile(self, cut, sizes):
        ends=list(accumulate(sizes))
        def label(rank):
            return bisect_right(ends,rank)+1 if rank<ends[-1] else 0
        @lru_cache(None)
        def exact(depth,remaining,out):
            if remaining<=0:
                return out if remaining==0 else 0
            return self.node(depth,exact(depth+1,remaining-1,out),exact(depth+1,remaining-2,out))
        @lru_cache(None)
        def tree(depth,remaining,rank):
            if remaining<=0:
                return label(rank) if remaining==0 else 0
            count=self.hits(remaining)
            if not count:
                return 0
            first,last=label(rank),label(rank+count-1)
            if first==last:
                return exact(depth,remaining,first) if first else 0
            low_count=self.hits(remaining-1)
            return self.node(depth,tree(depth+1,remaining-1,rank),
                             tree(depth+1,remaining-2,rank+low_count))
        return tree(0,cut,0)

    def output(self, root, tape):
        while root>=9:
            bit,low,high=self.nodes[root]
            root=high if tape[bit] else low
        return root

    def masses(self, root):
        @lru_cache(None)
        def go(v):
            if v<9:
                return tuple(ONE if i==v else ZERO for i in range(9))
            _,lo,hi=self.nodes[v]
            a,b=go(lo),go(hi)
            return tuple(P*x+P**2*y for x,y in zip(a,b))
        return go(root)

class BooleanDiagram:
    def __init__(self):
        self.nodes, self.unique = {}, {}

    def node(self, depth, low, high):
        if low==high:
            return low
        key=(depth,low,high)
        if key not in self.unique:
            ident=2+len(self.nodes)
            self.unique[key]=ident
            self.nodes[ident]=key
        return self.unique[key]

    def from_multiroot(self, m, root, bit):
        @lru_cache(None)
        def go(v):
            if v<9:
                if bit<4: return (v>>bit)&1
                if bit==4: return int(v!=0)
                return int(v!=0 and v%2==0)
            d,l,h=m.nodes[v]
            return self.node(d,go(l),go(h))
        return go(root)

    def compute_and_uncompute(self,tape,roots):
        # Scratch node v represents a clean target preloaded with zero.
        scratch={0:0,1:1}
        for v in sorted(self.nodes):
            d,l,h=self.nodes[v]
            x=tape[d]
            # y <- y XOR l XOR x*l XOR x*h, using one CNOT and two Toffolis.
            y=0
            y ^= scratch[l]
            y ^= x & scratch[l]
            y ^= x & scratch[h]
            assert y == (scratch[h] if x else scratch[l])
            scratch[v]=y
        output=sum(scratch[root]<<bit for bit,root in enumerate(roots))
        # The inverse gate sequence restores every node and keeps copied outputs.
        for v in sorted(self.nodes,reverse=True):
            d,l,h=self.nodes[v]
            x=tape[d]
            scratch[v] ^= x & scratch[h]
            scratch[v] ^= x & scratch[l]
            scratch[v] ^= scratch[l]
            assert scratch[v]==0
        return output


def expected_prefix(tape,cut,sizes):
    remaining=cut
    rank=0
    # Counts exact-price completions for earlier lexicographic branches.
    @lru_cache(None)
    def hits(r):
        return int(r==0) if r<=0 else hits(r-1)+hits(r-2)
    for bit in tape:
        if remaining<=0: break
        if bit:
            rank+=hits(remaining-1)
            remaining-=2
        else:
            remaining-=1
    if remaining!=0: return 0
    ends=list(accumulate(sizes))
    return bisect_right(ends,rank)+1 if rank<ends[-1] else 0


def tape_of_exact_rank(cut,rank):
    @lru_cache(None)
    def hits(r):
        return int(r==0) if r<=0 else hits(r-1)+hits(r-2)
    assert 0<=rank<hits(cut)
    tape=[]; r=cut
    while r>0:
        n=hits(r-1)
        if rank<n:
            tape.append(0);r-=1
        else:
            rank-=n;tape.append(1);r-=2
    assert r==0
    return tape+[0]*(cut-len(tape))


def main():
    cut=36
    w=[Fraction((-1)**(j-1)*comb(8,j),j*j) for j in range(1,9)]
    scale=lcm(*(v.denominator for v in w))
    sizes=[int(scale*abs(v)) for v in w]
    d=MultiDiagram()
    root=d.compile(cut,sizes)
    actual=d.masses(root)
    expected=[ONE-Golden(sum(sizes))*P**cut]+[Golden(n)*P**cut for n in sizes]
    assert actual==tuple(expected)
    assert d.hits(36)==24157817 and d.hits(35)==14930352
    assert Golden(d.hits(36))*P**36+Golden(d.hits(35))*P**37==ONE
    b=BooleanDiagram()
    roots=[b.from_multiroot(d,root,k) for k in range(6)]
    boundaries=list(accumulate(sizes))
    ranks={0,d.hits(cut)-1}
    for x in boundaries:
        ranks.update((x-1,x))
    ranks={x for x in ranks if 0<=x<d.hits(cut)}
    tests=[tape_of_exact_rank(cut,x) for x in sorted(ranks)]
    tests += [[1]*cut,[0]*cut]
    rng=Random(8675309)
    tests += [[rng.randrange(2) for _ in range(cut)] for _ in range(1000)]
    for tape in tests:
        expected_label=expected_prefix(tape,cut,sizes)
        assert d.output(root,tape)==expected_label
        expected_full=expected_label | (int(expected_label!=0)<<4) | (int(expected_label!=0 and expected_label%2==0)<<5)
        assert b.compute_and_uncompute(tape,roots)==expected_full
        for report in ((0,1) if expected_label else (0,)):
            printed=report ^ ((expected_full>>5)&1)
            assert printed==(report if expected_label%2 else 1-report) if expected_label else printed==0
    # All Boolean nodes are constructed after their descendants, and each is
    # an exact Shannon multiplexer on its tape bit, hence the full circuit is
    # correct on ALL 2^36 input tapes by structural induction.
    assert all(l<v and h<v for v,(_,l,h) in b.nodes.items())
    n=len(b.nodes)
    # At zero field, along the original pure-matter tangent, the exact
    # j-th conditional source is sign(j)*j^2*h^2*K*DI_m. The correct 1%
    # normalized tolerance depends on the derivative span 7^2+8^2, not on
    # the extremely small absolute gain by itself.
    iv.dps=45
    pi=(iv.sqrt(5)-1)/2
    scaled=iv.mpf(scale)*pi**cut
    amplification=iv.mpf(113)/scaled
    eps=iv.mpf('0.00000050')
    eta=iv.mpf(4*n)*eps
    normalized_error=amplification*eta**2
    assert normalized_error<iv.mpf('0.01')
    assert normalized_error>iv.mpf('0.001')
    # A constructive exact heralded option: two independent X-measurement
    # |+> preparations and the original two-H/CCZ Toffoli for each instance.
    factory_limit=64
    one_limit=40
    gate_count=4*n
    b2=1-pi**(6*factory_limit)
    b3=1-(1-16*pi**9)**factory_limit
    beta=(1-pi**one_limit)*(b2**6*b3)**gate_count
    assert iv.mpf('0.99930')<beta<iv.mpf('0.99931')
    z=iv.mpf(1)/2**20
    ready=iv.mpf(2*10946)*pi**23
    cos2=1-2*pi**2
    for _ in range(9): cos2=2*cos2*cos2-1
    vis=(1-cos2)*pi**7/2
    L0=4*pi**3
    rf=4*pi**2*(1-2*pi**2)*z*(1-z*L0)*(1-L0)
    gain=pi**36*scale*(iv.mpf(1)/256)**2*pi**3*vis*ready**2*rf**2
    retained_gain=beta*gain
    assert iv.mpf('1.0540e-25')<retained_gain<iv.mpf('1.0541e-25')
    # Cap counts fresh v-births, under the stated LC1 implementation, not
    # physical edge prices: per Toffoli 2*(1+4L) plus 18L = 26L+2.
    max_births=gate_count*(26*factory_limit+2)+2*one_limit+2*cut+(n+8)+1
    # One CNOT, two Toffoli per node; same again in uncomputation;
    # Copy six result bits and create/restore the one constant-1 helper.
    # Two additional CNOTs compute the deterministic T from B and sign.
    out=dict(cut=cut,all_tapes=2**cut,exact_hit_words=d.hits(cut),
        overshoot_words=d.hits(cut-1),active_words=sum(sizes),allocations=sizes,
        multi_terminal_nodes=len(d.nodes),binary_shared_nodes=n,
        exact_retained_random_inputs=36,conditional_flag_output_bits=6,
        extra_zero_work_bits_upper_bound=n+8,
        one_constant_bit_reusable=True,
        logical_forward_and_reverse_toffoli_upper_bound=4*n,
        logical_forward_and_reverse_cnot_upper_bound=2*n+8,
        logical_not_upper_bound=2,
        total_logical_gates_upper_bound=6*n+10,
        exact_ideal_weighted_output_law=True,
        exact_heralded_toffoli_instances=gate_count,
        max_attempts_per_controlled_phase_and_x_test=factory_limit,
        max_attempts_for_known_one=one_limit,
        exact_independent_heralded_selector_ready_probability=str(beta),
        exact_physical_gain_SC2_with_recorded_failures=str(retained_gain),
        max_plus_resources=2*gate_count,
        known_zero_workspace_and_output=n+8,
        max_registered_native_word_births_with_lc1=max_births,
        birth_count_scope='specified LC1 tail, X-measurement and controlled-phase ancillas; excludes undisclosed routing, external field banks and other physical ancillas',
        zero_field_matter_source_error_amplifier=str(amplification),
        example_native_all_column_error_per_toffoli='0.00000050',
        example_selector_operator_error_upper_bound=str(eta),
        example_source_error_relative_to_matter_tangent=str(normalized_error),
        tolerance_scope='only fixed-selector output probabilities on scalar matter tangent, with field-independent measured selector and no feedback from dispatch garbage',
        test_tapes=len(tests),
        all_tapes_argument='BDD recursion plus exact reversible multiplexer identity and inverse',
        finite_native_decomposition_of_each_toffoli='requires declared all-column compiler, tolerances, routes and actual births',
        actual_cost_info_and_geometry_not_derived=True,
        born_probabilities_one_symbol='p for 0, p^2 for 10')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main()
