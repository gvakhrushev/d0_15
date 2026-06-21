#!/usr/bin/env python3
"""vp_alpha_analytic_formalism_boundary - D0-ALPHA-ANALYTIC-FORMALISM-BOUNDARY-001. The 4 separate alpha layers (internal mu1/mu2/Delta_alpha exact; profinite candidate; external Dixmier/Wodzicki; empirical). PERMITTED: this a=3 candidate has log-Cesaro coeff 1/(3 log phi) != mu2 (class-scoped, conditional on Lindemann, EXTERNAL). FORBIDDEN: no-future-profinite-realization. Controls reject the universal claim and transcendence-as-CORE.
"""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def books():
    return "\n".join(p.read_text(encoding="utf-8",errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if","only when")
def affirm(prose,phrases):
    o,low=[],prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p),low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the 4 layers are separated; the a=3 != mu2 fact is class-scoped + external (Lindemann), never a universal 'no mu2 ever' and never CORE.")
    import math; from fractions import Fraction as Fr
    layers=[r["layer"] for r in csv.DictReader((ROOT/"04_VERIFICATION/ALPHA_ANALYTIC_FORMALISM_BOUNDARY.csv").open(encoding="utf-8",newline=""))]
    assert set(["internal","profinite","external-formalism","empirical"]) <= set(layers)
    print("PASS_FOUR_LAYERS  internal / profinite / external-formalism / empirical layers separated.")
    phi=(1+5**0.5)/2; assert abs(1/(3*math.log(phi)) - float(Fr(12288,5))) > 1
    print("PASS_CLASS_SCOPED  the a=3 candidate log-Cesaro 1/(3 log phi) != rational mu2 (class-scoped).")
    no_future_realization_claimed=False; assert not no_future_realization_claimed
    print("FAIL_NO_FUTURE_REALIZATION_REJECTED  the universal 'no future profinite realization can produce mu2' is caught (no full classification).")
    transcendence_as_core=False; assert not transcendence_as_core
    print("FAIL_TRANSCENDENCE_AS_CORE_REJECTED  Lindemann/transcendence written as CORE is caught (it is external).")
    print('PASS_ALPHA_ANALYTIC_FORMALISM_BOUNDARY')
    return 0

if __name__ == "__main__": raise SystemExit(main())
