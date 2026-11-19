"""Exact G1-G7 growing clocks for two address-controlled native NC1 suffixes."""
from dataclasses import dataclass
from decimal import Decimal as D, localcontext
from functools import reduce
from itertools import accumulate
import json

from check_heat_history import A, P, ONE, ZERO, const


@dataclass
class Mat:
    rows: int
    cols: int
    entries: dict

    def __matmul__(self, other):
        assert self.cols == other.rows
        by_row = {}
        for (i, j), z in other.entries.items():
            by_row.setdefault(i, []).append((j, z))
        out = {}
        for (i, k), a in self.entries.items():
            for j, b in by_row.get(k, ()):
                key = i, j
                out[key] = out.get(key, ZERO) + a*b
        return Mat(self.rows, other.cols, {k: z for k, z in out.items() if z != ZERO})

    def plus(self, other, sign=ONE):
        assert (self.rows, self.cols) == (other.rows, other.cols)
        out = self.entries.copy()
        for key, z in other.entries.items():
            out[key] = out.get(key, ZERO) + sign*z
        return Mat(self.rows, self.cols, {k: z for k, z in out.items() if z != ZERO})

    def tr(self):
        return Mat(self.cols, self.rows, {(j,i): a for (i,j),a in self.entries.items()})

    def tensor(self, b):
        return Mat(self.rows*b.rows, self.cols*b.cols,
                   {(i*b.rows+k,j*b.cols+h): x*y
                    for (i,j), x in self.entries.items() for (k,h), y in b.entries.items()})


def eye(n):
    return Mat(n,n,{(i,i): ONE for i in range(n)})


def diagonal(n, predicate):
    return Mat(n,n,{(i,i): ONE for i in range(n) if predicate(i)})


def block(rows, cols, placed):
    out = {}
    for off_i, off_j, b in placed:
        for (i,j), c in b.entries.items():
            key = i+off_i, j+off_j
            out[key] = out.get(key, ZERO) + c
    return Mat(rows,cols,{k: z for k,z in out.items() if z != ZERO})


v = Mat(2,1,{(0,0): A,(1,0): P})
g = Mat(2,2,{(0,0): A,(1,0): P,(0,1): -P,(1,1): A})
flip = Mat(2,2,{(0,1): ONE,(1,0): ONE})
reflect = (v@v.tr()).plus(v@v.tr()).plus(eye(2),-ONE)


def controlled(n, mask, op):
    on = diagonal(n, lambda i: i & mask)
    return eye(n).plus(on,-ONE).tensor(eye(2)).plus(on.tensor(op))


def clock(word):
    dims = [step.cols for step in word]
    offsets = list(accumulate([0]+dims))
    passive = [op if op.rows != op.cols else eye(op.cols) for op in word[:-1]]
    back = [None]*len(word)
    back[-1] = eye(dims[-1])
    for i in reversed(range(len(passive))):
        back[i] = back[i+1]@passive[i]
    details = [eye(dims[0])]+[eye(x.rows).plus(x@x.tr(),-ONE) for x in passive]
    closing = block(offsets[-1], dims[-1],
                    [(o,0,d@b.tr()) for o,d,b in zip(offsets,details,back)])
    t = block(offsets[-1],offsets[-1],
              [(offsets[i+1],offsets[i],op) for i,op in enumerate(word[:-1])]
              +[(0,offsets[-2],closing@word[-1])])
    prefix = eye(dims[0])
    cuts = []
    for i,op in enumerate(word):
        cuts.append((offsets[i],offsets[i],prefix@prefix.tr()))
        prefix = op@prefix
    cut = block(t.rows,t.rows,cuts)
    return t, cut, closing, back[0].tr()@prefix, offsets


def check():
    assert reflect@v == v and reflect@g@reflect == g.tr()
    # x,y live; both canonical births, two old square letters, arbitrary input
    # dimension two is a protected old spectator, not an inserted blank.
    old = eye(2)
    common = [old.tensor(v), old.tensor(g), eye(4).tensor(v), controlled(4,1,flip)]
    words = [common.copy(),common.copy()]
    gauges = [eye(op.cols) for op in common]
    boundary = eye(8)
    for mask_a, mask_b in [(2,1),(1,1)]:
        n = boundary.cols
        birth = eye(n).tensor(v)
        ca,cb = (controlled(n,m,flip) for m in (mask_a,mask_b))
        ja,jb = (controlled(n,m,reflect) for m in (mask_a,mask_b))
        turn = eye(n).tensor(g)
        end = jb@boundary.tensor(eye(2))@ja
        first = end
        middle = cb@first@ca
        last = turn@middle@turn.tr()
        assert end@birth == birth@boundary
        assert cb@last == end@ca
        for word,c in zip(words,(ca,cb)):
            word.extend([birth,c,turn,c])
        gauges.extend([boundary, first, middle, last])
        boundary = end
    t_a, p_a, r_a, cold_a, offsets = clock(words[0])
    t_b, p_b, r_b, cold_b, _ = clock(words[1])
    gauge = block(t_a.rows,t_a.cols,list(zip(offsets,offsets,gauges)))
    assert gauge.tr()@gauge == eye(t_a.rows)
    assert t_a.tr()@t_a == eye(t_a.rows) and t_b.tr()@t_b == eye(t_b.rows)
    assert r_a == r_b and gauge@r_a == r_b@boundary
    assert gauge@t_a == t_b@gauge and gauge@p_a == p_b@gauge
    _,_,_,cold_common,_ = clock(common)
    pcell = Mat(1,1,{(0,0): P})
    assert cold_a == cold_b == cold_common.tensor(pcell)

    # Actual independently parsed terminal rows on r,t, on each input s.
    one = Mat(2,1,{(1,0):ONE})
    zero = Mat(2,1,{(0,0):ONE})
    c = controlled(2,1,flip)
    u = c@eye(2).tensor(g)@c
    def norm(x):
        return (x.tr()@x).entries.get((0,0),ZERO)
    lam = const(4)*P**3
    for s in [0,1]:
        encoded = u@((g if s == 0 else g.tr())@v).tensor(v)
        assert norm(one.tr().tensor(one.tr())@encoded) == ZERO
        assert norm(one.tr().tensor(zero.tr())@encoded) == (lam if s == 0 else ZERO)
        assert norm(zero.tr().tensor(eye(2))@encoded) == (ONE-lam if s == 0 else ONE)
    with localcontext() as ctx:
        ctx.prec = 52
        phi = (D(1)+D(5).sqrt())/2
        l = 4/phi**3
        h = -l*l.ln()-(1-l)*(1-l).ln()
        gain = l-h/phi.ln()
        assert D('.46') < gain < D('.51')
        return dict(golden_basis="1,a,a^2,a^3; a^4+a^2=1", exact=True,
                    stage_dimensions=[op.cols for op in words[0]],clock_dimension=t_a.rows,
                    full_unitaries_checked=2,closing_on_all_terminal_columns=boundary.rows,
                    all_intermediate_gauges_and_generated_cuts=True,old_input_dimension=2,
                    fixture_common_word=["birth_x","G_x","birth_y","CX_x_y"],
                    alternative_controls=[["x","r"],["y","r"]],
                    cold_factor_for_two_suffixes_per_arm="p",
                    calibration_conditional_controls=["already registered T","known zero"],
                    suffix_per_arm={"births":2,"CX":4,"G":2},
                    invalid_probability="0",lambda_probe=str(+l),
                    conditional_entropy_if_control_zero_nats=str(+h),
                    parsed_price_gain=str(+gain),full_CD13=False)


if __name__ == "__main__":
    print(json.dumps(check(), sort_keys=True, indent=2))
