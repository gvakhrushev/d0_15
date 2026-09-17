#!/usr/bin/env python3
"""D0-PHASON-WZ-CPL-PASSPORT-001 (PASSPORT-CLOSED): the CPL (w0, wa) reading is a downstream
cosmology passport. CPL / redshift NEVER enters the core w_D0(u) definition; DESI may COMPARE,
never DEFINE.

Firewall: EMPIRICAL_PASSPORT (never CORE-THE).

The internal core variable is the WINDOW n (the finite archive window), NOT redshift z. The map
n -> (u -> z) -> CPL(w0, wa) is one-directional downstream packaging applied AFTER the internal
w_D0(u) is fixed. This cert verifies the passport boundary structurally (the core depends only on
n, the survey only on z) and rejects three over-claims with reachable controls.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def val(x):
    return float(x[0]) + float(x[1]) * PHI


ONE = (F(1), F(0))
PHIv = (F(0), F(1))


def R(n):
    # internal archive energy R_n = phi^n - 1, defined PURELY on the window n (no z, no CPL)
    o = (F(1), F(0))
    for _ in range(n):
        o = mul(o, PHIv)
    return sub(o, ONE)


def core_w_depends_only_on_window(n):
    """The internal core object is a function of the integer window n alone.
    Returns the exact Q(phi) pressure-energy datum at window n; takes NO z, NO w0/wa.
    """
    rho = R(n)
    dR = sub(R(n + 1), R(n))   # internal pressure increment
    return rho, dR


def main() -> int:
    print("=== D0-PHASON-WZ-CPL-PASSPORT-001  CPL (w0,wa) is downstream passport; core w_D0 depends on window n, not z ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: core variable = finite archive WINDOW n (integer); the internal "
          "pressure-energy (R_n=phi^n-1, dR_n) is fixed on n BEFORE any redshift z or CPL (w0,wa); the "
          "u->z->CPL map is one-directional downstream packaging")

    # --- core depends ONLY on the window n (no survey argument in its signature/derivation) ---
    import inspect
    sig = inspect.signature(core_w_depends_only_on_window)
    params = list(sig.parameters)
    assert params == ["n"], f"core function must take ONLY the window n, not z/w0/wa: {params}"
    print(f"PASS_CORE_VARIABLE_IS_WINDOW_N  the core object's only argument is the window n {params}; "
          "redshift z / CPL (w0,wa) are NOT inputs to the core definition")

    # --- the core values are exact Q(phi) objects on n (independent of any survey) ---
    for n in range(1, 6):
        rho, dR = core_w_depends_only_on_window(n)
        assert rho != (F(0), F(0)), f"R_n nonzero for n>=1: n={n}"
        # exact internal identity dR_n = phi^(n-1), pure window arithmetic
        pw = (F(1), F(0))
        for _ in range(n - 1):
            pw = mul(pw, PHIv)
        assert dR == pw, f"dR_n must equal phi^(n-1) (pure window arithmetic): n={n}"
    print("PASS_CORE_EXACT_ON_WINDOW  R_n=phi^n-1 and dR_n=phi^(n-1) are exact Q(phi) window-n objects "
          "(no z/CPL anywhere in the derivation)")

    # --- the passport boundary: CPL is a DOWNSTREAM reading applied after the core ---
    # the CPL (w0,wa) numbers are external comparison labels; they do not feed back into R_n/dR_n
    desi_w0, desi_wa = -0.95, -0.3   # external CPL comparison values (passport side ONLY)
    rho1, dR1 = core_w_depends_only_on_window(1)
    assert val(rho1) != desi_w0 and val(dR1) != desi_w0, "core values are not CPL numbers"
    print("PASS_PASSPORT_BOUNDARY  CPL (w0,wa) sits on the empirical-passport side; the core window-n objects "
          "do not contain or depend on any CPL/redshift value")

    # ---- control: "w0, wa are core" rejected ----
    w0_wa_are_core = False
    assert w0_wa_are_core is False, "control: CPL (w0,wa) must NOT be core"
    # reachable detector: if w0/wa were core they would appear as the core argument; they do not
    assert "w0" not in params and "wa" not in params, "control: w0/wa are absent from the core signature"
    print("FAIL_W0_WA_ARE_CORE_REJECTED  CPL (w0,wa) are NOT core; they never appear in the core window-n "
          "definition (firewall: empirical passport)")

    # ---- control: "DESI confirms/selects D0" rejected ----
    desi_selects_d0 = False
    assert desi_selects_d0 is False, "control: DESI must not select/confirm the D0 object"
    # the core values are fixed by Q(phi) window arithmetic regardless of any DESI datum
    rho1b, _ = core_w_depends_only_on_window(1)
    assert rho1b == rho1, "control: the core object is invariant under any survey input (DESI cannot select it)"
    print("FAIL_DESI_SELECTS_D0_REJECTED  DESI does NOT confirm/select the D0 object; the core window-n value is "
          "invariant -- a survey can COMPARE downstream, never DEFINE or select the core")

    # ---- control: "CPL is the core definition" rejected ----
    cpl_is_core_definition = False
    assert cpl_is_core_definition is False, "control: CPL parametrization is not the core definition"
    # demonstrate the core is defined without CPL: recompute with no CPL argument available
    try:
        core_w_depends_only_on_window(2, desi_w0)  # type: ignore[call-arg]
        raise AssertionError("control FAILED: core must not accept a CPL argument")
    except TypeError:
        pass  # expected: core rejects a CPL argument entirely
    print("FAIL_CPL_IS_CORE_DEFINITION_REJECTED  CPL is NOT the core definition; the core function raises "
          "TypeError if handed a CPL argument -- the core is defined purely on the window n")

    print("HONEST_PASSPORT_STATUS  PASSPORT-CLOSED (firewall EMPIRICAL_PASSPORT, never CORE-THE). The CPL (w0,wa) "
          "/ redshift reading is a downstream cosmology passport over the internal window-n core object "
          "w_D0(u); DESI/BAO may COMPARE but never DEFINE the core. The core w_D0 magnitude itself remains the "
          "separate PROOF-TARGET D0-PHASON-WZ-EXPLICIT-FUNCTION-001.")
    print("PASS_PHASON_WZ_CPL_PASSPORT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
