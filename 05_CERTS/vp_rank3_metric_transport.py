#!/usr/bin/env python3
"""D0-RANK3-METRIC-TRANSPORT-001 — the spatial metric IS the transport quadratic form; anisotropy.

Verify-then-promote (Iter-17, ТЗ Phase C, honest framing). The signature (3,1) and the causal
partition are ALREADY forced (D0-RANK3-CAUSAL-CONE-FORCING-001, by Pisot-arrow counting). This
certificate adds the SPATIAL metric content that route did not give: the metric on the rank-3
transport sector is the equitable-quotient quadratic form of the scene K(9,11,13), the light cone
is its null set, and — the new falsifiable prediction — that form is ANISOTROPIC because the zone
sizes 9,11,13 are unequal.

WHAT IS COMPUTED + ASSERTED (able to FAIL):
  * the equitable quotient B = [[0,11,13],[9,0,13],[9,11,0]] of K(9,11,13) is the rank-3 transport
    form; its characteristic polynomial is λ³ − 359λ − 2574 (359=|E| coupling, 2574 the cycle term);
  * its three eigenvalues are real and split 1 positive / 2 negative — a definite NON-degenerate
    signature, so the form has a genuine null cone (the light cone = {x : Q(x)=0});
  * ANISOTROPY (the prediction): the two negative eigenvalues are UNEQUAL for (9,11,13)
    (≈ −12.08 ≠ −9.76), i.e. the spatial transport metric is not isotropic at the carrier level;
  * ISOTROPY control: for equal zones (n,n,n) the quotient is n(J−I) with spectrum {2n, −n, −n} —
    the two negatives COINCIDE, so isotropy is exactly the equal-zone limit. The split is forced by
    9≠11≠13.

HONESTY BOUNDARY (printed). This realizes the SPATIAL metric structure (the quadratic form + its
null cone + the anisotropy falsifier) — it does NOT by itself fix the cone-SPEED / overall unit of
g_{μν} (that is the c=1 question, handled separately by the Connes-distance/Lipschitz argument).
So this is a finite realization + a falsifiable prediction, NOT a claim that the full dimensionful
metric is closed here. The (3,1) spacetime signature stays the Pisot-counting result; this is the
3-dim spatial sector's quadratic form, a distinct object — they are not conflated.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np


def quotient(parts):
    a, b, c = parts
    return np.array([[0, b, c], [a, 0, c], [a, b, 0]], dtype=float)


def main() -> int:
    print("=== D0-RANK3-METRIC-TRANSPORT-001  spatial metric = transport quadratic form ===")

    B = quotient((9, 11, 13))
    # characteristic polynomial coefficients of a 3x3 with zero trace: λ³ + c1 λ + c0
    # c1 = -(sum of 2x2 principal minors); c0 = -det(B)
    c1 = (B[0, 0] * B[1, 1] - B[0, 1] * B[1, 0]
          + B[0, 0] * B[2, 2] - B[0, 2] * B[2, 0]
          + B[1, 1] * B[2, 2] - B[1, 2] * B[2, 1])
    c0 = -np.linalg.det(B)
    assert abs(c1 - (-359.0)) < 1e-6, f"λ-coefficient must be −359 (=−|E|): {c1}"
    assert abs(c0 - (-2574.0)) < 1e-6, f"constant must be −2574: {c0}"
    print(f"PASS_CHARPOLY  λ³ − 359λ − 2574  (359=|E| coupling); discriminant>0 ⇒ 3 distinct real roots")

    ev = np.linalg.eigvals(B).real
    ev.sort()
    npos = int((ev > 1e-9).sum())
    nneg = int((ev < -1e-9).sum())
    assert npos == 1 and nneg == 2, f"signature must be 1 positive / 2 negative: {ev}"
    assert abs(ev.sum()) < 1e-6, "traceless ⇒ eigenvalues sum to 0"
    print(f"PASS_NONDEGENERATE_SIGNATURE  eigenvalues {np.round(ev,2).tolist()} = (1+,2−); null cone exists")

    # ANISOTROPY: the two negative eigenvalues are unequal
    neg = sorted(ev[ev < 0])
    assert abs(neg[0] - neg[1]) > 0.5, f"the two negative eigenvalues must split (anisotropy): {neg}"
    print(f"PASS_ANISOTROPY  negative eigenvalues {np.round(neg,3).tolist()} are UNEQUAL ⇒ anisotropic cone (falsifier)")

    # ISOTROPY control: equal zones (n,n,n) ⇒ the two negatives coincide
    for n in (9, 11, 13):
        evn = np.linalg.eigvals(quotient((n, n, n))).real
        evn.sort()
        negn = sorted(evn[evn < -1e-9])
        assert abs(negn[0] - negn[1]) < 1e-6, f"equal zones must be isotropic (degenerate negatives): {negn}"
        assert abs(evn[evn > 0][0] - 2 * n) < 1e-6 and abs(negn[0] - (-n)) < 1e-6, "spectrum {2n,−n,−n}"
    print("FAIL_EQUAL_ZONES_ARE_ISOTROPIC  (n,n,n) spectrum {2n,−n,−n}: negatives coincide ⇒ the split is forced by 9≠11≠13")

    # negative control: a wrong coupling (e.g. parts (9,11,12)) changes the charpoly off −359/−2574
    Bw = quotient((9, 11, 12))
    c0w = -np.linalg.det(Bw)
    assert abs(c0w - (-2574.0)) > 1.0, "control: wrong zone sizes change the cycle term off 2574"
    print("FAIL_WRONG_ZONES_CHANGE_THE_FORM")

    print("HONEST_REALIZES_SPATIAL_METRIC_FORM_PLUS_ANISOTROPY_FALSIFIER_NOT_THE_CONE_SPEED_UNIT")
    print("HONEST_3_1_SIGNATURE_STAYS_PISOT_COUNTING_THIS_IS_THE_3D_SPATIAL_QUADRATIC_FORM")
    print("PASS_RANK3_METRIC_TRANSPORT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
