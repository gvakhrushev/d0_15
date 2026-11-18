"""Golden midpoint encoding by rank, including B130 words with zero physical mass."""
from collections import Counter
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from math import comb, factorial, prod
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[7]
source = root/"02_REGISTRY/research/sources/d0_complete_code_source_2026-10-19/check_code_source.py"
spec = spec_from_file_location("owned_golden_code",source)
owner = module_from_spec(spec)
sys.modules[spec.name] = owner
spec.loader.exec_module(owner)


def type_interval(word, alphabet):
    """Colexicographic multiset rank followed by lexicographic within-type rank."""
    m = len(word)
    if m < 1 or any(symbol < 0 or symbol >= alphabet for symbol in word):
        raise ValueError("word outside this fixed alphabet")
    types = comb(alphabet+m-1,m)
    rank = sum(comb(value+i,i+1) for i,value in enumerate(sorted(word)))
    counts = Counter(word)
    size = factorial(m) // prod(factorial(c) for c in counts.values())
    offset, ways = 0,size
    for remaining,symbol in zip(range(m,0,-1),word):
        smaller = sum(count for k,count in counts.items() if k < symbol)
        offset += ways*smaller // remaining
        assert (ways*counts[symbol]) % remaining == 0
        ways = ways*counts[symbol] // remaining
        counts[symbol] -= 1
    assert 0 <= rank < types and 0 <= offset < size
    return Fraction(rank*size+offset,types*size), Fraction(1,types*size)


def encode(word, alphabet):
    start, mass = type_interval(word, alphabet)
    mid = owner.Q5(start+mass/2)
    left, width, letters = owner.Q5(), owner.one, []
    while owner.Q5(mass/2) < width:
        cut = left + width*owner.p
        if mid < cut:
            letters.append("F")
            width = width*owner.p
        else:
            letters.append("R")
            left = cut
            width = width*owner.p**2
    assert owner.Q5(start) <= left and left+width <= owner.Q5(start+mass)
    assert owner.Q5(mass/2)*owner.p**2 < width <= owner.Q5(mass)
    return "".join(letters)


if __name__=="__main__":
    for m in (1,2,3):
        words = list(product(range(4),repeat=m))
        bins = sorted(type_interval(w,4) for w in words)
        assert bins[0][0]==0 and bins[-1][0]+bins[-1][1]==1
        assert all(u+v==w for (u,v),(w,_) in zip(bins,bins[1:]))
        assert owner.prefix_free([encode(w,4) for w in words])
    alphabet = 128+64+64*64+64**2*128
    assert alphabet==528576
    # Short prefix, two full STOP cases, final-odd cap, and a physically dark root and tail.
    examples = [1, 128+63, 128+64+13*64+9, 128+64+64**2+(13*64+9)*128+27,
                128+64+64**2+(2*64+3)*128+5, alphabet-1]
    for m in (1,2,3):
        used = [tuple(examples[(i+j)%len(examples)] for j in range(m)) for i in range(len(examples))]
        assert owner.prefix_free([encode(w,alphabet) for w in used])
    print("PASS exact interval coverage and prefix property on small alphabets; actual 528576-label code on bright/dark schedule words")
