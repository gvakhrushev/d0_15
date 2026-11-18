"""Exact one-flag length for the convex isochoric witness; --table prints all weights."""
import argparse
import sys
from itertools import product


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    """Integer pairs denote a+bp; p^2=1-p."""
    a, b = x
    c, d = y
    return a*c + b*d, a*d + b*c - b*d


def addresses():
    return product(range(4), repeat=4)


def index(u, v, x, y):
    return ((u*4 + v)*4 + x)*4 + y


def witness():
    values = [(0, 0)]*256
    for u, v, x, y in addresses():
        if min(u, x, y) < 1 or sum(i == 3 for i in (u, x, y)) > 1:
            continue
        h = (13**(u-1), 0)
        for _ in range(x+y-2):
            h = mul(h, (3, 2))  # phi^3
        values[index(u, v, x, y)] = h
    assert sum(q != (0, 0) for q in values) == 80
    return values


def tensor_bit_transform(values, diagonal, off_diagonal):
    for bit in range(8):
        values = [add(mul(diagonal, t), mul(off_diagonal, values[m ^ (1 << bit)]))
                  for m, t in enumerate(values)]
    return values


def render(m, c, flag, size):
    """Emit the actual self-delimiting record in bounded chunks."""
    symbol = ("0", "10")
    bits = [int(ch) for ch in format(m, "08b")] + [c, flag]
    yield "".join(symbol[bit] for bit in bits)
    copied = 0 if c == 0 else flag
    repetitions, rest = divmod(size, len(symbol[copied]))
    assert rest == 0
    while repetitions:
        count = min(4096, repetitions)
        yield symbol[copied]*count
        repetitions -= count


def run(table, emit):
    h = witness()
    weight = tensor_bit_transform(h, (2, 1), (-1, -1))
    assert tensor_bit_transform(weight, (0, 1), (1, -1)) == h
    assert all(weight[index(u, v, x, y)] == weight[index(u, 0, x, y)]
               for u, v, x, y in addresses())

    rows = [(m, c, *(weight[m] if c == 0 else (0, 0)))
            for m in range(256) for c in range(2)]
    # F=0 occurs with p and F=1 with 1-p.  Their offsets can be chosen separately.
    base0 = max(-k-l for m, c, k, l in rows)
    base1 = max(-k for m, c, k, l in rows)
    assert (base0, base1) == (1290778, 797744) and base1 % 2 == 0
    common = (base1, base0-base1)
    assert common == (797744,493034)
    longest_suffix, longest_record, witness_record = 0, 0, None
    for m, c, k, l in rows:
        lengths = (base0+k+l, base1+k)
        assert min(lengths) >= 0
        expected = add(mul((0, 1), (lengths[0], 0)), mul((1, -1), (lengths[1], 0)))
        assert expected == add(common, (k, l))
        for flag, size in enumerate(lengths):
            # c=0 supplies a known retained zero; if c=1 use the retained flag.
            bit = 0 if c == 0 else flag
            token_length = 1+bit
            assert size % token_length == 0
            repetitions = size // token_length
            assert repetitions*token_length == size
            header = 8 + bin(m).count("1") + (1+c) + (1+flag)
            longest_suffix = max(longest_suffix, size)
            if header+size > longest_record:
                longest_record, witness_record = header+size, (m, c, flag, header, size)
    assert (longest_suffix, longest_record) == (2914096, 2914112)
    m, c, flag, header, size = witness_record
    assert sum(len(chunk) for chunk in render(m, c, flag, size)) == longest_record
    if emit is not None:
        m, c, flag = emit
        if not (0 <= m < 256 and c in (0,1) and flag in (0,1)):
            raise ValueError("Require a byte m, one coefficient bit and one flag bit.")
        k,l = weight[m] if c == 0 else (0,0)
        size = base0+k+l if flag == 0 else base1+k
        for chunk in render(m, c, flag, size):
            sys.stdout.write(chunk)
        return
    print("offsets conditional on flag 0/1:", base0, base1)
    print("max additional printed symbols, max retained header plus suffix:", longest_suffix, longest_record)
    print("attaining (m,c,flag,header,suffix):", witness_record)
    print("integer-pair extremes:", *( (min(v),max(v)) for v in zip(*weight) ))
    if table:
        for u, v, x, y in addresses():
            if v == 0:
                print(u, x, y, *weight[index(u, v, x, y)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", action="store_true", help="print every distinct spatial coefficient row u,x,y,k,l (independent of v)")
    parser.add_argument("--emit", nargs=3, type=int, metavar=("M","C","FLAG"),
                        help="emit one literal codeword without an added newline")
    args = parser.parse_args()
    run(args.table, args.emit)
