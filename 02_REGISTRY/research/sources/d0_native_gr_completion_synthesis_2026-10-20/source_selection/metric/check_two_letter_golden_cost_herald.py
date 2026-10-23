"""Exact native G/CNOT implementation of the owned all128 paid-cost mark."""
from pathlib import Path
from itertools import product
import argparse
import hashlib
import json
import platform
import sympy as S


def run():
    root = Path(__file__).resolve()
    while not (root / "AGENTS.md").is_file():
        if root.parent == root:
            raise RuntimeError("repository root not found")
        root = root.parent
    pins = {
        "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md":
            "dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d",
        "02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md":
            "ef69c2052237fbe8e916acf16691f9b14b4c1c2465a7837e838db2baeb95449d",
        "02_REGISTRY/research/A4D_NATIVE_GOLDEN_PAID_COST_HERALD_2026_10_21.md":
            "1be2441a2f6de42f271349e4b504c61cfd67318f3c609f7a9f19c75c4b22ed49",
        "02_REGISTRY/research/sources/d0_full128_normalization_closure_2026-10-21/PROOF.md":
            "42f96fc4cdb4f47878c4d260a003dd2819741c6b4e233581e184f28e9792ebcc",
    }
    checks = []

    def ok(condition, label):
        if not condition:
            raise RuntimeError(label)
        checks.append(label)

    def eq(left, right, label):
        diff = left-right
        good = (all(S.simplify(x) == 0 for x in diff)
                if isinstance(diff, S.MatrixBase) else S.simplify(diff) == 0)
        ok(good, label)

    for path, sha in pins.items():
        ok(hashlib.sha256((root/path).read_bytes()).hexdigest() == sha,
           "pin "+path)
    p = (S.sqrt(5)-1)/2
    a = S.sqrt(p)
    g = S.Matrix([[a, -p], [p, a]])
    flip = S.Matrix([[0, 1], [1, 0]])
    cx = S.diag(S.eye(2), flip)
    word = cx*S.kronecker_product(S.eye(2), g)
    eq(word.H*word, S.eye(4), "literal G then CNOT is a full isometry")
    eq(word*word.H, S.eye(4), "literal G then CNOT is a full coisometry")
    eq(word, S.diag(g, flip*g), "full stored-port blocks are G and XG")
    port_effect = S.diag(0, 0, 1, 1)
    eq(word*port_effect, port_effect*word, "every stored port sector is preserved")
    amplitudes = {}
    entropy = p+2*p**2
    for b in (0, 1):
        col = word[:, 2*b]
        eq(sum(S.conjugate(v)*v for v in col), 1,
           f"complete flag norm for port{b}")
        amplitudes[b] = [col[2*b+f] for f in (0, 1)]
        eq(amplitudes[b][0]**2, p**(1+b),
           f"original Golden probability cost mark for port{b}")
        eq(amplitudes[b][1]**2, 1-p**(1+b),
           f"actual complementary flag for port{b}")
        eq(sum(amplitudes[b][f]**2*(1+(b ^ f)) for f in (0, 1)),
           entropy, f"full flag entropy is the same for port{b}")
    eq(entropy, 2-p, "exact fixed full flag entropy coefficient")
    for bits in product((0, 1), repeat=2):
        all_flags = {}
        for flags in product((0, 1), repeat=2):
            amplitude = S.prod(amplitudes[b][f] for b, f in zip(bits, flags))
            all_flags[flags] = amplitude**2
        eq(sum(all_flags.values()), 1,
           f"two-round complete retained flag norm {bits}")
        eq(all_flags[(0, 0)], p**(2+sum(bits)),
           f"two-round same success map as original cost mark {bits}")
        conditional_entropy = sum(prob*(2+sum(b ^ f for b, f in zip(bits, flags)))
                                  for flags, prob in all_flags.items())
        eq(conditional_entropy, 2*entropy,
           f"two-round complete conditional entropy is constant {bits}")
    eps = S.Symbol("eps", positive=True)
    delta = S.diag(1, 2)  # Diagnostic only: the owned all-size identity is consumed.
    e1 = p*eps*delta
    e0 = S.eye(2)-e1
    gram = p*e0+p**2*e1
    eq(gram, p*S.eye(2)-eps*p**4*delta, "inherited original all128 success effect")
    eq(p**2*e0+p*e1, S.eye(2)-gram, "literal failures give the full complementary effect")
    ok(S.simplify(gram[0, 0]-gram[1, 1]) != 0,
       "same noncentral scalar-normalization obstruction remains")
    energy, denergy, deps = S.symbols("energy denergy deps", real=True)
    mean_cost = 1+p*eps*energy
    probability = p-eps*p**4*energy
    eq(probability, p-p**3*(mean_cost-1), "native one-round absolute known-cost calibration")
    dmean = p*(eps*denergy+deps*energy)
    dprob = -p**4*(eps*denergy+deps*energy)
    eq(dmean, -dprob/p**3, "joint energy and compatible clock-source calibration")
    # Omitting the control preserves total probability but kills the required mark/source.
    wrong_gram = p*(e0+e1)
    ok(S.simplify(wrong_gram[0, 0]-gram[0, 0]) != 0,
       "uncontrolled Golden coin is rejected by the inherited nonzero source")
    eq(S.diff(wrong_gram[0, 0], eps), 0, "omitted-control mutant has zero clock jet")
    ok(S.simplify(S.diff(gram[0, 0], eps)) != 0,
       "actual controlled recording keeps the inherited clock jet")
    # One original round, arbitrary changing port probability q1.
    q1 = S.Symbol("q1", real=True)
    new_increment = ((1-q1)+q1)*entropy
    old_increment = ((1-q1)+2*q1)*entropy
    eq(S.diff(new_increment, q1), 0, "one-flag full entropy has zero original-port source")
    eq(S.diff(old_increment-new_increment, q1), entropy,
       "same herald can have a different full information source")
    # Noncommuting conditional quantum RIGHT states: no classical RIGHT shortcut.
    sigma0 = S.diag(S.Rational(2, 3), S.Rational(1, 3))
    sigma1 = S.Matrix([[S.Rational(1, 2), S.Rational(1, 4)],
                       [S.Rational(1, 4), S.Rational(1, 2)]])
    ok(sigma0*sigma1-sigma1*sigma0 != S.zeros(2),
       "conditional oldRIGHT control is genuinely noncommuting")
    prior = [S.Rational(2, 5), S.Rational(3, 5)]
    old_right = prior[0]*sigma0+prior[1]*sigma1
    blocks = []
    new_right = S.zeros(2)
    for b, sigma in enumerate((sigma0, sigma1)):
        for f in (0, 1):
            block = prior[b]*amplitudes[b][f]**2*sigma
            blocks.append(block)
            new_right += block
            eq(S.trace(block), prior[b]*amplitudes[b][f]**2,
               f"full conditional RIGHT branch weight {b},{f}")
    eq(new_right, old_right, "all flag outputs retain the full quantum RIGHT marginal")
    eq(S.trace(S.diag(*blocks)), 1,
       "complete pointer plus quantum RIGHT state stays normalized")
    theta = S.Symbol("theta", real=True)
    r = (a*S.cos(theta)-p*S.sin(theta))**2
    eq(r.subs(theta, 0), p, "actual blank base probability")
    eq(S.diff(r, theta).subs(theta, 0), -2*a*p,
       "actual independently variable blank has a nonzero preparation jet")
    # h_phi'(p)=log_phi(p^2/p)=-1, using p^2=1-p exactly.
    eq((1-p)/p, p, "exact entropy derivative uses log_phi(p)=-1")
    prep_price_source = -(-1)*S.diff(r, theta).subs(theta, 0)
    eq(prep_price_source, -2*a*p, "zero-cost free blank fails its preparation Euler equation")
    ok(S.simplify(prep_price_source) != 0, "nonstationary blank is not frozen away")
    rvar = S.Symbol("rvar", positive=True)
    h = -(rvar*S.log(rvar)+(1-rvar)*S.log(1-rvar))/S.log(1/p)
    eq(S.diff(h, rvar).subs(rvar, S.Rational(1, 2)), 0,
       "constant-price free-flag optimum is the balanced output")
    eq(S.diff(h, rvar, 2), -1/(rvar*(1-rvar)*S.log(1/p)),
       "binary entropy is strictly concave on the open probability interval")
    eq((rvar*e0+(1-rvar)*e1).subs(rvar, S.Rational(1, 2)), S.eye(2)/2,
       "free-flag entropy optimum erases the original cost effect")
    eq(S.diff(rvar+(1-2*rvar)*q1, q1).subs(rvar, S.Rational(1, 2)), 0,
       "balanced optimum has no original-port source to invert")
    # Actual physical attenuation changes A, not an arbitrary scalar times F.
    y = S.Matrix([[S.Rational(2, 5), S.Rational(1, 10)],
                  [S.Rational(1, 10), S.Rational(1, 3)]])
    dy = S.Matrix([[S.Rational(1, 7), S.Rational(1, 11)],
                   [S.Rational(1, 11), -S.Rational(1, 13)]])
    ok(y*dy != dy*y, "proper complementary feedback control is noncommutative")
    z = S.Rational(1, 2**20)
    c = p
    rc = ((1-z)*S.eye(2)+z*c*y).inv()
    r1 = ((1-z)*S.eye(2)+z*y).inv()
    eq(c*rc-r1, (c-1)*(1-z)*rc*r1,
       "proper complementary weighted resolvent identity")
    source_difference = -128*z*S.trace((c*rc-r1)*dy)
    eq(source_difference, 128*z*(1-c)*(1-z)*S.trace(rc*r1*dy),
       "true marked versus unmarked feedback source difference")
    dpositive = S.eye(2)/5
    positive_difference = S.simplify(128*z*(1-c)*(1-z)*S.trace(rc*r1*dpositive))
    ok(positive_difference > 0, "positive true-return variation has a strict feedback-source change")
    bound = 128*z*(1-c)/(1-z)*sum(abs(v) for v in dy)
    ok(S.simplify(bound-abs(source_difference)) >= 0,
       "proper complementary source change satisfies the trace-norm upper bound")
    ok(S.simplify((S.eye(2)-c*y-c*(S.eye(2)-y))[0, 0]) != 0,
       "multiplying old F is rejected as the physical return attenuation")
    return {
        "status":"PASS",
        "input_snapshot":"2bbe9af6f3ce875898a28395c7c3ac2087a40277",
        "source_pins":pins,"checks":checks,"check_count":len(checks),
        "environment":{"python":platform.python_version(),"sympy":S.__version__},
        "scope":{"actual_full128_identity_consumed":True,
                 "original_full128_rows_replayed":False,
                 "forward_G_per_round":1,"forward_CNOT_per_round":1,
                 "controlled_G_assumed":False,"known_one_assumed":False,
                 "all_failures_retained":True,
                 "free_blank_preparation_Euler_solved":False,
                 "unpriced_free_flag_optimization_selects_Golden_mark":False,
                 "actual_extra_work_source_assumed_zero":False,
                 "physical_G0_addressability_derived":False,
                 "compulsory_Book_Info_derived":False,"GR_closed":False}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), ensure_ascii=False, indent=2)+"\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8", newline="\n")
    print(result, end="")
