"""Actual CX and NC1 columns, conditional motion, terminal subspaces and information."""
from fractions import Fraction as F
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'round82' / 'device'))
import check_prepaid_report as source

one, zero, a, p, v = source.one, source.Golden(), source.a, source.p, source.v
r, gap, xi = p*p, p-p*p, 2*a*p
G, act = source.ne.Gate, source.action
parser = (G('CX',(0,1)), G('G',(1,)), G('CX',(0,1)))
assert gap == source.p3 and one - xi*xi == gap*gap
canonical = {0:a, 1:p}
tail0 = act(canonical, G('G',(0,)), 1)
tails = (tail0, {0: one})


def register_word(n):
    # Immutable reference, protected spin and physical PORT never appear in a gate.
    y, t = 4, 5
    word = [G('CX',(y,t))]
    for j in range(n):
        f = 6+j
        word.extend((G('CX',(t,f)),G('G',(f,)),G('CX',(t,f))))
    ex = source.ne.Execution(6+n, (), (3,), tuple(word), source.ne.G_CX_SOURCE_I,
                             2, (0,1), report_bits=(t,))
    source.ne.execution_from_json(source.ne.canonical_json(ex),max_qubits=6+n,
                                  max_expanded_stages=len(word))
    assert len(word)==1+3*n


def inner(left, right):
    return sum((amp*right.get(address,zero) for address,amp in left.items()),zero)


def power(element, n):
    result = one
    for _ in range(n):
        result *= element
    return result


def attach_head(state):
    return {2*addr+b:amp*val for addr,amp in state.items() for b,val in enumerate(v)}


def do_parser(head):
    state = attach_head(head)
    overlaps = []
    for gate in parser:
        after = act(state,gate,2)
        overlaps.append(inner(state,after))
        state = after
    branches = [{i%2:z for i,z in state.items() if i//2==b} for b in (0,1)]
    for b in (0,1):
        expected = {i:x*head[b] for i,x in tails[b].items()} if b in head else {}
        assert branches[b] == expected
    return overlaps, branches


def check_sector(y,n):
    start = {2*y+i:amp for i,amp in canonical.items()}
    after = act(start,G('CX',(0,1)),2)
    assert inner(start,after) == (xi if y else one)
    head = {i%2:z for i,z in after.items()}
    q = p if y else r
    overlaps, branches = do_parser(head)
    masses = tuple(inner(branch,branch) for branch in branches)
    assert masses == (one-q,q)
    assert overlaps == [one-q+q*xi,a,one-q]
    for b in (0,1):
        at_known, _ = do_parser({b:one})
        assert at_known == ([one,a,one] if b==0 else [xi,a,zero])
        assert power(inner(canonical,tails[b]),2) == p
    # A single read head is retained. All further re-read outcomes must coincide.
    paths = [(b, masses[b]) for b in range(2)]
    mean_length = sum(mass*n*(1+b) for b,mass in paths)
    assert mean_length == n*(one+q)
    cold = sum((p if b==0 else r)*power(p,n) for b,_ in paths)
    assert cold == power(p,n)
    return [source.trace_distance(h) for h in overlaps]


def verify():
    assert p+r==one and p+2*r==one+r
    for n in range(1,13):
        register_word(n)
        low, high = (check_sector(y,n) for y in (0,1))
        contrasts = [source.minus(h,l) for l,h in zip(low,high)]
        assert contrasts[0][0]>F('.03954') and low[1]==high[1]
        assert contrasts[2][0]>F('.13802')
    # For any true H.1 with Q>=.23, h'(z)<.54 follows without evaluating logs:
    # ((1-z)/z)^50 < phi^27 at its maximum z0.
    # Golden-ring coefficients are integral, so clear the denominator at z0.
    numerator = 100*r+23*gap
    complement = 100*one-numerator
    assert source.enclosure(power(one+p,27)*power(numerator,50)-power(complement,50))[0] > 0
    coherent_contrast = source.minus(source.lcd(source.enclosure(r)),source.lcd(source.enclosure(p)))
    assert coherent_contrast[0] <= 0 <= coherent_contrast[1] and coherent_contrast[1] < F('1e-12')
    print('first parser, stage-wise contrasts:', [float(contrasts[0][0]), 0, float(contrasts[2][0])])
    print('old-to-new physical CX contrast:',float(source.enclosure(gap)[0]))
    print('late parser:',[float(source.enclosure(gap*gap)[0]),0,float(source.enclosure(gap)[0])])
    print('single retained head, all n: 2 leaves per old address, h_cold=p^n, delta_S=h(p^2)')


if __name__=='__main__':
    verify()
