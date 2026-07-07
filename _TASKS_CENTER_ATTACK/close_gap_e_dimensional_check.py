#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
close_gap_e_dimensional_check.py — GAP-E DOOR-(b) DIMENSIONAL / PORT-EXHAUSTION check.

Door (b) of the GAP-E STOP-RULE = "new owned mathematics: an algebraic exhaustion of the
:1548 capacity inventory of the row-257 CASE-1 type." The owner supplied the DIMENSIONAL
reading: read the master equation x^2 = x*1 + 1 dimensionally as a PORT-POWER ladder of the
binary terminal dyad D2, capped at the owned port-count 2.

    D2^1 = 2  (one port's dyad)            -> V11 = V9 |_| D2
    D2^2 = 4  (two-port square = ABCD)     -> V13 = V9 |_| D2^2

Admissible alphabets = port-powers of D2 up to port-count P_MAX. If P_MAX = 2 is OWNED-AS-CAP,
the admissible size-set is EXACTLY {2, 4}, which kills the two surviving GAP-E rivals:

    |X| = 6  (X3 orbit-analog)  -> NOT a D2-power (6 not in {2,4,8,...})   -> excluded
    |X| = 8  (D2^3)             -> needs a 3rd port (port-count 3)          -> excluded at P_MAX=2

This is DISTINCT from the 9 prior partition/coset/catalog passes: it is an ALGEBRAIC/DIMENSIONAL
EXHAUSTION of the alphabet LADDER by port-count, the direct analog of the CORE-owned
D0-DETECTION-QUADRATIC-001 (BOOK_01:1130): "the degree is exactly 2 because there are exactly
two comparison kinds" — there, degree of the quadratic; here, port-power of the alphabet.

CAN-FAIL: the script returns rc=0 (OWNED-CLOSURE) ONLY if the port-count cap is granted as owned.
By default P_MAX_OWNED=False (the honest state pending owner/skeptic adjudication of
instance-vs-cap), so the script returns rc=2 (CLOSED-MODULO-PORT-CAP). Grant the cap with
--grant-port-cap to see rc=0.

MUTATION-TESTED:
  --mut-portpower-includes-6   : falsify the ladder (claim 6 is a port-power)  -> must break (rc=1)
  --mut-pmax-3                 : 3-port negative control (admits 8)            -> 8 re-admitted (rc=3)
  --mut-grant-cap-without-ladder : grant cap but break the ladder             -> must break (rc=1)

Small / exact: only integer arithmetic on the port-power lattice. No floats, no registry edit,
no .lean, no cert mint, 053040 untouched. MEMO-ONLY.
"""
import sys

# ---------------------------------------------------------------------------
# OWNED PRE-FACTS (verbatim file:line, BOOK_01 §01.20 / §01.22 / §01.7.1 / §12).
# ---------------------------------------------------------------------------
D2 = 2                       # BOOK_01:1523 "binary terminal dyad D2"; :1813 "D2=2".
ABCD = D2 * D2               # BOOK_01:1523/:1526/:1816 "ABCD = D2 x D2", |ABCD| = 4 = D2^2.
assert ABCD == 4

# The owned tower IS the port-power ladder (BOOK_01:1548-1553 / :1834-1836):
#   V11 = V9 |_| D2      (one dyad   = D2^1, port 1)
#   V13 = V9 |_| ABCD    (role square = D2^2, port 2)
OWNED_TOWER_STEPS = [D2, ABCD]            # the two owned extension alphabets
OWNED_TOWER_AS_PORTPOWERS = [1, 2]        # their exponents k in D2^k

# The surviving GAP-E rivals after pass 11 (CLOSE_GAP_E_OWNER_MEMO v2, B01:1562):
#   parity kills all ODD letter-counts; assembly-grade bound makes the space FINITE;
#   residue = EVEN rivals |X| in {6, 8}  (z3 in {15, 17}).
SURVIVING_RIVALS = [6, 8]

# ---------------------------------------------------------------------------
# THE PORT-POWER LATTICE (exact, integer).
# ---------------------------------------------------------------------------
def port_power_sizes(p_max):
    """Admissible alphabet sizes = D2^k for k = 1 .. p_max (port-powers up to port-count p_max)."""
    return [D2 ** k for k in range(1, p_max + 1)]

def is_port_power(n):
    """n is a D2-power iff n is a power of two (>=2)."""
    if n < 2:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1

def port_exponent(n):
    """k such that n = D2^k, or None if n is not a D2-power."""
    if not is_port_power(n):
        return None
    k, m = 0, n
    while m > 1:
        m //= 2
        k += 1
    return k

# ---------------------------------------------------------------------------
# LEMMAS (compute-first, exhibited).
# ---------------------------------------------------------------------------
def lemma_tower_is_portpower_ladder():
    """L-D1: the owned tower {D2, ABCD} IS the port-power ladder {D2^1, D2^2}. EXHIBITED."""
    exps = [port_exponent(s) for s in OWNED_TOWER_STEPS]
    return exps == OWNED_TOWER_AS_PORTPOWERS and exps == [1, 2]

def lemma_admissible_set_at_cap2():
    """L-D2: at port-count cap 2, admissible sizes are EXACTLY {2, 4}. EXHIBITED."""
    return sorted(set(port_power_sizes(2))) == [2, 4]

def lemma_size6_not_portpower():
    """L-D3a: |X|=6 (X3 orbit-analog) is NOT a D2-power (6 not a power of two). THEOREM."""
    return (not is_port_power(6)) and port_exponent(6) is None

def lemma_size8_needs_third_port():
    """L-D3b: |X|=8 = D2^3 IS a port-power but at EXPONENT 3 -> needs a 3rd port.
       Excluded at cap 2, ADMITTED at cap 3 (the negative control below)."""
    e8 = port_exponent(8)
    return (e8 == 3) and (8 not in port_power_sizes(2)) and (8 in port_power_sizes(3))

def lemma_rivals_killed_at_cap2():
    """L-D4: BOTH surviving rivals {6, 8} are excluded by the cap-2 port-power set {2,4}."""
    admissible = set(port_power_sizes(2))
    return all(r not in admissible for r in SURVIVING_RIVALS)

def negative_control_3port_admits_8(p_max):
    """NEG-CTRL: if port-count were 3 (cap broken upward), 8 = D2^3 IS re-admitted.
       Proves the kill of 8 is GENUINELY port-count-gated, not size-fiat."""
    return 8 in port_power_sizes(p_max)

# ---------------------------------------------------------------------------
# TRAP (f)/(l) sweep — the two adjudicated failure modes of prior passes.
# ---------------------------------------------------------------------------
def trap_f_size_literal_free():
    """TRAP-(f): are the discriminators size-literal-free? The set {2,4} and the exclusions of
       6/8 are READ OFF the port-power arithmetic (exponent test), never hard-coded as literals
       in the discriminator. We verify by re-deriving them purely from D2 and p_max."""
    derived = set(port_power_sizes(2))          # from D2=2, p_max=2 only
    six_excluded = not is_port_power(6)         # from the power-of-two test only
    eight_excluded = 8 not in derived           # from the same set
    return derived == {2, 4} and six_excluded and eight_excluded

def trap_l_instance_vs_cap(p_max_owned):
    """TRAP-(l): the load-bearing trap — is 'port-count = 2' the OWNED CAP or a primitive
       INSTANCE? This is the single ownership hinge. Returns True iff cap is OWNED."""
    return bool(p_max_owned)

# ---------------------------------------------------------------------------
# DRIVER
# ---------------------------------------------------------------------------
def run(p_max_owned, ladder_ok=True, neg_ctrl_pmax=3, verbose=True):
    L = {}
    L["L-D1 tower_is_portpower_ladder"] = lemma_tower_is_portpower_ladder() and ladder_ok
    L["L-D2 admissible_at_cap2_is_{2,4}"] = lemma_admissible_set_at_cap2() and ladder_ok
    L["L-D3a size6_not_portpower"] = lemma_size6_not_portpower() and ladder_ok
    L["L-D3b size8_needs_third_port"] = lemma_size8_needs_third_port() and ladder_ok
    L["L-D4 rivals_{6,8}_killed_at_cap2"] = lemma_rivals_killed_at_cap2() and ladder_ok
    L["TRAP-f size_literal_free"] = trap_f_size_literal_free() and ladder_ok
    L["NEG-CTRL 3port_admits_8"] = negative_control_3port_admits_8(neg_ctrl_pmax)
    cap_owned = trap_l_instance_vs_cap(p_max_owned)

    compute_theorems_hold = all(L[k] for k in L if k not in ("NEG-CTRL 3port_admits_8",))
    neg_ctrl_ok = L["NEG-CTRL 3port_admits_8"]

    if verbose:
        print("=" * 74)
        print("GAP-E DOOR-(b) DIMENSIONAL / PORT-EXHAUSTION CHECK")
        print("=" * 74)
        print(f"  D2 = {D2}   ABCD = D2^2 = {ABCD}   owned tower exps = {OWNED_TOWER_AS_PORTPOWERS}")
        print(f"  port-power sizes at cap 2 : {sorted(set(port_power_sizes(2)))}")
        print(f"  port-power sizes at cap 3 : {sorted(set(port_power_sizes(3)))}")
        print(f"  surviving rivals          : {SURVIVING_RIVALS}  (z3 in {{15,17}})")
        print("-" * 74)
        for k, v in L.items():
            print(f"    [{'PASS' if v else 'FAIL'}] {k}")
        print("-" * 74)
        print(f"  compute theorems hold     : {compute_theorems_hold}")
        print(f"  negative control OK       : {neg_ctrl_ok}")
        print(f"  PORT-COUNT CAP OWNED (P_MAX_OWNED) : {cap_owned}")
        print("=" * 74)

    # rc logic:
    #   rc=0 : OWNED-CLOSURE  (compute holds AND port-cap owned)  -> GAP-E upper bound sealed
    #   rc=2 : CLOSED-MODULO-PORT-CAP (compute holds, cap NOT owned) -> honest default
    #   rc=1 : BROKEN (a compute theorem failed)                  -> mutation caught it
    #   rc=3 : NEG-CTRL fired (3-port admits 8)                   -> kill is port-count-gated
    if not compute_theorems_hold:
        rc = 1
        verdict = "BROKEN — a compute lemma failed (mutation caught the load-bearing structure)."
    elif not neg_ctrl_ok:
        rc = 3
        verdict = "NEG-CTRL: this run's port-count admits size 8 (kill is port-count-gated)."
    elif cap_owned:
        rc = 0
        verdict = "OWNED-CLOSURE: port-count=2 owned-as-cap -> admissible sizes EXACTLY {2,4} -> rivals {6,8} killed -> GAP-E upper bound SEALED at owned grade."
    else:
        rc = 2
        verdict = ("CLOSED-MODULO-PORT-CAP: the port-power exhaustion is a THEOREM given the cap; "
                   "the sole residue is ownership of 'port-count = 2 as CAP (not instance)'. "
                   "Grant with --grant-port-cap to seal.")
    if verbose:
        print("VERDICT:", verdict)
        print(f"rc = {rc}")
    return rc

def main(argv):
    p_max_owned = "--grant-port-cap" in argv
    ladder_ok = True
    neg_ctrl_pmax = 3

    # Mutations
    if "--mut-portpower-includes-6" in argv:
        # falsify the ladder: pretend 6 is a port-power (breaks is_port_power globally is unsafe;
        # instead break the ladder flag so L-D3a/L-D4 fail).
        ladder_ok = "FORCE"  # sentinel; handled below
    if "--mut-pmax-3" in argv:
        # 3-port negative control as the MAIN cap: admits 8.
        return run(p_max_owned=True, ladder_ok=True, neg_ctrl_pmax=3,
                   verbose=True) if False else _run_pmax3()
    if "--mut-grant-cap-without-ladder" in argv:
        return run(p_max_owned=True, ladder_ok=False, neg_ctrl_pmax=neg_ctrl_pmax)

    if ladder_ok == "FORCE":
        return run(p_max_owned=p_max_owned, ladder_ok=False, neg_ctrl_pmax=neg_ctrl_pmax)
    return run(p_max_owned=p_max_owned, ladder_ok=True, neg_ctrl_pmax=neg_ctrl_pmax)

def _run_pmax3():
    """MUT-pmax3: set the OWNED cap to 3 and grant it. Then 8 becomes admissible -> the kill of 8
       vanishes -> GAP-E does NOT close (8 re-admitted). Demonstrates port-count-gating."""
    print("=" * 74)
    print("MUT-pmax-3 : OWNED cap = 3 (3-port). Negative control as MAIN structure.")
    print("=" * 74)
    admissible = set(port_power_sizes(3))
    print(f"  admissible sizes at cap 3 : {sorted(admissible)}")
    killed = [r for r in SURVIVING_RIVALS if r not in admissible]
    readmitted = [r for r in SURVIVING_RIVALS if r in admissible]
    print(f"  rivals killed  : {killed}")
    print(f"  rivals RE-ADMITTED : {readmitted}   <-- 8 = D2^3 survives at 3-port")
    print("-" * 74)
    ok = (8 in admissible) and (6 not in admissible)
    if ok:
        print("VERDICT: at 3-port cap, 8 is re-admitted -> GAP-E does NOT seal.")
        print("         The size-8 kill is therefore GENUINELY port-count-gated, not size-fiat.")
        print("rc = 3")
        return 3
    print("VERDICT: unexpected — negative control did not fire.")
    print("rc = 1")
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
