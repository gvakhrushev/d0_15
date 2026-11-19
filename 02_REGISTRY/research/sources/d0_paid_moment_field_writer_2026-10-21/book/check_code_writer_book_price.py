#!/usr/bin/env python3
"""Exact new AB/BA catalogue-prefix diagnostic; no external packages/old suites."""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

CHECKS = []


def require(name, value):
    if not value:
        raise RuntimeError(name)
    CHECKS.append(name)


def inner(a, b):
    return sum((v * b.get(k, F(0)) for k, v in a.items()), F(0))


def scaled(a, q):
    return {k: q * v for k, v in a.items() if q * v}


def added(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, F(0)) + v
        if not out[k]:
            del out[k]
    return out


def cell(s, gate):
    if gate == "A" and s & 4:
        return s ^ 2
    if gate == "B" and s & 2:
        return s ^ 1
    return s


def run(s, word):
    for gate in word:
        s = cell(s, gate)
    return s


def code_work(k):
    u, b = 0, 0
    for j in range(2):
        bit = (k >> j) & 1
        word = ("A", "B") if bit else ("B", "A")
        s = run(4, word)
        u |= ((s >> 1) & 1) << j
        b |= (s & 1) << j
    return u, b


def bank_amplitude(rows):
    ans = F(1)
    for k, item in enumerate(rows):
        label, bit = divmod(item, 2)
        ans *= F(1 if not bit or label < k else -1, 2)
    return ans


AMPLITUDES = [F(3, 5), F(12, 25), F(16, 25)]
CHARGES = [2, 6, 10]


def initial(h):
    # (factory record, passive input, c, u, code, all three rows, output)
    return (0, h, 0, 0, 0, (0, 0, 0), 0)


def branches(k, h):
    u, b = code_work(k)
    result = [{initial(h): AMPLITUDES[0]}, {}, {}]
    for rows in itertools.product(range(4), repeat=3):
        q = bank_amplitude(rows)
        late = (1, h, 1, u, b, rows, 0)
        result[1][late] = AMPLITUDES[1] * q
        retained = list(rows)
        output = retained[k]
        retained[k] = 0
        ready = (2, h, 1, u, b, tuple(retained), output)
        result[2][ready] = AMPLITUDES[2] * q
    return result


def complete(k, h, x=F(1)):
    ans = {}
    for f, v in enumerate(branches(k, h)):
        ans = added(ans, scaled(v, x ** CHARGES[f]))
    return ans


def output_x(v):
    value = F(0)
    for key, a in v.items():
        flipped = key[:-1] + (key[-1] ^ 1,)
        value += a * v.get(flipped, F(0))
    return value / inner(v, v)


def controls():
    words = [("B", "A"), ("A", "B")]
    for bit, word in enumerate(words):
        require(f"cell_{bit}_full_permutation", sorted(run(s, word) for s in range(8)) == list(range(8)))
        require(f"cell_{bit}_writes_known_bit_and_marker", run(4, word) == 6 + bit)
        cleanup = tuple(reversed(word)) + ("A",)
        require(f"cell_{bit}_paid_code_cleanup_keeps_marker", run(6 + bit, cleanup) == 6)
        require(f"cell_{bit}_cleanup_inventory", cleanup.count("A") == 2 and cleanup.count("B") == 1)
    require("ordered_words_remain_distinct", [run(s, words[0]) for s in range(8)] != [run(s, words[1]) for s in range(8)])
    weights = [q * q for q in AMPLITUDES]
    require("three_factory_effects_complete", sum(weights) == 1)
    z = F(1, 16)
    determinants, moments = {}, {}
    for k in range(3):
        require(f"code_{k}_actual_two_cell_output", code_work(k) == (3, k))
        cols = [complete(k, h) for h in range(2)]
        require(f"code_{k}_complete_isometry", [[inner(a, b) for b in cols] for a in cols] == [[F(1), F(0)], [F(0), F(1)]])
        for f, v in enumerate(branches(k, 0)):
            require(f"code_{k}_factory_{f}_same_probability", inner(v, v) == weights[f])
            if f:
                require(f"code_{k}_factory_{f}_marker_retained", all(key[3] == 3 for key in v))
        ready = branches(k, 0)[2]
        require(f"code_{k}_unused_catalogue_rows_retained",
                len(ready) == 64 and all(key[5][k] == 0 for key in ready)
                and all({key[5][j] for key in ready} == set(range(4)) for j in range(3) if j != k))
        observed = output_x(ready)
        require(f"code_{k}_nonconstant_selected_moment", observed == k - 1)
        moments[str(k)] = str(observed)
        for x in (F(1), F(1, 2)):
            cols = [complete(k, h, x) for h in range(2)]
            n = sum((weights[f] * x ** (2 * CHARGES[f]) for f in range(3)), F(0))
            gram = [[inner(a, b) for b in cols] for a in cols]
            require(f"code_{k}_mark_{x}_true_normalizer", gram == [[n, F(0)], [F(0), n]])
            corner = [[v.get(initial(h), F(0)) for v in cols] for h in range(2)]
            a = AMPLITUDES[0] * x ** CHARGES[0]
            require(f"code_{k}_mark_{x}_nonzero_shared_early_corner", corner == [[a, F(0)], [F(0), a]] and a != 0)
            det = (1 - z + z * a * a / n) ** 2
            if str(x) in determinants:
                require(f"code_{k}_mark_{x}_feedback_secant_zero", determinants[str(x)] == str(det))
            determinants[str(x)] = str(det)

    # Explicit record-block Householders realize the equal-stack-Gram map.
    # No physical gate admission is asserted for these mathematical unitaries.
    diffs = []
    for h in range(2):
        for f in range(3):
            v, w = branches(0, h)[f], branches(2, h)[f]
            delta = added(v, scaled(w, F(-1)))
            if delta:
                diffs.append(delta)

    def transport(v):
        out = dict(v)
        for d in diffs:
            out = added(out, scaled(d, -2 * inner(d, out) / inner(d, d)))
        return out

    for h in range(2):
        seed = {initial(h): F(1)}
        require(f"gram_transport_{h}_fixes_initial_cut", transport(seed) == seed)
        for x in (F(1), F(1, 2)):
            v, w = complete(0, h, x), complete(2, h, x)
            require(f"gram_transport_{h}_mark_{x}", transport(v) == w and transport(w) == v)
    require("gram_transport_preserves_priced_record_blocks",
            all(len({(key[0], key[1]) for key in d}) == 1 for d in diffs))
    require("gram_transport_does_not_preserve_fixed_report",
            output_x(branches(0, 0)[2]) != output_x(branches(2, 0)[2]))
    return {"factory_weights": [str(w) for w in weights], "charges": CHARGES,
            "mean_counted_cost": str(sum((weights[f] * CHARGES[f] for f in range(3)), F(0))),
            "selected_X_moments": moments, "normalized_Book_pencil_determinants": determinants,
            "fixture_scope": "Two actual AB/BA cells and full coherent three-row selector; rational abort weights are structural diagnostics, not native factory claims"}


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    pins_bytes = (here / "SOURCE_PINS.json").read_bytes()
    pins = json.loads(pins_bytes)
    for item in pins["sources"]:
        content = subprocess.check_output(["git", "show", item["source_ref"] + ":" + item["path"]], cwd=args.repo)
        require("historical_pin:" + item["path"], digest(content) == item["sha256"])
    result = {"status": "PASS", "diagnostics": controls(), "checks": CHECKS,
              "check_count": len(CHECKS), "proof_sha256": digest((here / "COMPLETE_CODE_WRITER_BOOK_PRICE.md").read_bytes()),
              "checker_sha256": digest(Path(__file__).read_bytes()), "pins_sha256": digest(pins_bytes)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
