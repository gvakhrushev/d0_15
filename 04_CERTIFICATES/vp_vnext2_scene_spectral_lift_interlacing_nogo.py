#!/usr/bin/env python3
"""vp_vnext2_scene_spectral_lift_interlacing_nogo - D0-VNEXT2-SCENE-SPECTRAL-LIFT-OWNER-001 (SHARP NO-GO).

Upgrades the spectral-lift NO-GO from "no UNITARY Xi (distinct-count 5 vs 4)" to a strictly stronger
statement: NO isometric-corner / UCP compression realizes the AF-reduced Dirac^2 in the scene at the
claimed full dimension, for ANY scale c > 0. This is the bold constructive attack (Connes correspondence /
Stinespring corner, not a unitary) carried to its honest conclusion.

Setup (exact). Scene Laplacian spectrum of K(9,11,13): eigenvalues {0,20,22,24,33} with multiplicities
{1,12,10,8,2} (sum 33). AF-reduced Dirac^2 (scale-free): distinct {0, phi^2, phi^4, phi^6} with
multiplicities {1,3,8,21} (sum 33), overall scale c>0 free (lambda_0^2).

A compression V^* D_scene^2 V = M with V an isometry onto a k-dim subspace exists IFF the k eigenvalues of
M interlace the scene spectrum (Cauchy): d_i <= mu_i <= d_{i+(33-k)} (sorted ascending, 0-indexed). We test
the AF-reduced corner of every dimension k (truncating the top block) against every scale c.

RESULTS (all exact):
  - k <= 4: FEASIBLE. Small AF stages DO embed as interlacing corners (honest positive sub-result).
  - k = 5: INFEASIBLE. The phi^2 block forces c >= 20/phi^2 = 7.639... (to clear the scene's mult-12 wall at
    eigenvalue 20), while the phi^4 entry forces c <= 33/phi^4 = 4.815... (to stay under the scene's top 33).
    7.639 > 4.815 -> empty bracket. Infeasible for every k >= 5, including the full k = 33 lift the owner
    claims.
The mechanism is SPECTRAL BUNCHING (dynamic-range mismatch): the k=5 bracket is empty iff d[1]/d_top >
1/phi^2 = 0.382. The scene's nonzero spectrum has d[1]/d_top = 20/33 = 0.606 -- too bunched (too little
dynamic range) to host the AF GEOMETRIC ladder phi^2:phi^4:phi^6. This depends only on the eigenvalue RANGE,
not on how multiplicity mass is distributed: a SPREAD control (same multiplicities, d[1]/d_top = 2/33)
admits the k=5 corner, while permuting the scene's multiplicities (same eigenvalue set, same d[1]/d_top)
does not. No scaling reconciles the two under interlacing once k >= 5. So the full spectral lift is NO-GO
against all correspondences, not just unitaries.

Honest scope: this is a NO-GO for the FULL lift (the owner's claim). It explicitly certifies that small AF
stages (dim <= 4) DO embed — the obstruction is dimensional, biting at k = 5.

Falsifiable: breaks (rc=1) if a feasible c is found at any k >= 5, if the k=5 bracket is not empty, if the
k<=4 corners are reported infeasible, or if the scene multiplicities are altered.
"""
import sys
from fractions import Fraction as Fr

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# exact phi powers as elements of Z[phi]: phi^k = F_k*phi + F_{k-1}; compare via (a + b*phi) with phi=(1+sqrt5)/2
# For interlacing bracket arithmetic we need exact ordering of c*phi^j against integers -> use rationals with
# a high-precision phi surrogate is unsafe; instead compare symbolically using phi^2=phi+1.
# phi^2 = phi+1, phi^4 = 3phi+2, phi^6 = 8phi+5.  Numerically phi=(1+5**0.5)/2 for bracket endpoints, but the
# load-bearing inequality 20/phi^2 > 33/phi^4  <=>  20*phi^4 > 33*phi^2  <=>  20*phi^2 > 33 (divide phi^2>0)
# <=> 20*(phi+1) > 33 <=> 20phi > 13 <=> phi > 0.65, TRUE exactly. So the k=5 emptiness is EXACT.
PHI = (1 + 5 ** 0.5) / 2
SCENE = sorted([0] * 1 + [20] * 12 + [22] * 10 + [24] * 8 + [33] * 2)
N = len(SCENE)


def die(msg: str) -> None:
    print("FAIL " + msg)
    raise SystemExit(1)


def corner_pattern(k):
    base = [(0.0, 1), (PHI ** 2, 3), (PHI ** 4, 8), (PHI ** 6, 21)]
    out = []
    tot = 0
    for val, m in base:
        take = min(m, k - tot)
        if take > 0:
            out.extend([val] * take)
            tot += take
        if tot >= k:
            break
    return sorted(out)


def feasible(k):
    """Return (feasible, c_lo, c_hi) for a k-dim AF corner interlacing the scene."""
    pat = corner_pattern(k)
    d = SCENE
    lo, hi = 0.0, 1e18
    for i in range(k):
        p = pat[i]
        if p > 0:
            lo = max(lo, d[i] / p)
            hi = min(hi, d[i + N - k] / p)
        else:
            if d[i] > 1e-9:
                return (False, lo, hi)
    return (lo <= hi + 1e-9, lo, hi)


def main() -> int:
    print("=== vp_vnext2_scene_spectral_lift_interlacing_nogo  UCP-corner lift obstruction (Cauchy) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the scene and AF-reduced spectra are fixed first; the interlacing "
          "bracket being empty for k>=5 (any scale) is the computed consequence.")

    # scene multiplicities sanity
    from collections import Counter
    cnt = Counter(SCENE)
    if dict(cnt) != {0: 1, 20: 12, 22: 10, 24: 8, 33: 2} or sum(cnt.values()) != 33:
        die(f"SCENE_SPECTRUM  wrong scene multiplicities: {dict(cnt)}")
    print("PASS_SCENE_SPECTRUM  scene Laplacian {0:1,20:12,22:10,24:8,33:2} (sum 33).")

    # (a) small corners k<=4 FEASIBLE (honest positive sub-result)
    small = [(k, feasible(k)) for k in (2, 3, 4)]
    if not all(f[0] for _, f in small):
        die(f"SMALL_CORNERS  AF stages k<=4 must embed (interlacing corner exists): {small}")
    print(f"PASS_SMALL_CORNERS_EMBED  AF stages dim 2,3,4 DO embed as interlacing corners of the scene "
          f"(e.g. k=4 bracket c in [{feasible(4)[1]:.3f},{feasible(4)[2]:.3f}]) — honest positive sub-result.")

    # (b) k=5 INFEASIBLE with the exact bracket
    f5, lo5, hi5 = feasible(5)
    if f5:
        die("K5_FEASIBLE  k=5 corner must be INFEASIBLE")
    print(f"PASS_K5_INFEASIBLE  k=5 bracket EMPTY: c_lo={lo5:.3f} (phi^2 block clears scene wall 20) > "
          f"c_hi={hi5:.3f} (phi^4 under scene top 33).")

    # (c) EXACT emptiness: 20/phi^2 > 33/phi^4  <=>  20*phi^2 > 33  <=>  20*(phi+1) > 33  <=> 20*phi > 13
    # exact in Z[phi]: 20*phi > 13 iff phi > 13/20 = 0.65; phi = 1.618... so TRUE, and this is exact.
    if not (20 * PHI > 13):
        die("EXACT_INEQUALITY  20*phi>13 must hold")
    lhs_exact = 20 * PHI ** 2  # = 20(phi+1)
    if not (lhs_exact > 33 + 1e-9):
        die("EXACT_INEQUALITY  20*phi^2>33 must hold (empties the k=5 bracket)")
    print("PASS_EXACT_EMPTINESS  20/phi^2 > 33/phi^4  <=>  20*phi^2 > 33  <=>  20*phi > 13  (exact in Z[phi]) "
          "-> the k=5 emptiness is not numerical rounding.")

    # (d) ALL k >= 5 infeasible (incl. full k=33 = the owner's claim)
    bad = [k for k in range(5, 34) if feasible(k)[0]]
    if bad:
        die(f"HIGHER_CORNERS  these k>=5 unexpectedly feasible: {bad}")
    if feasible(33)[0]:
        die("FULL_LIFT  full k=33 lift must be infeasible")
    print("PASS_ALL_HIGH_CORNERS_INFEASIBLE  every corner dim k=5..33 is infeasible for all scales — "
          "including the full k=33 spectral lift the owner claims.")

    # ---- reachable DISCRIMINATING control: the true cause is spectral BUNCHING, not mass concentration ----
    # The k=5 bracket is empty IFF d[1]/d_top > 1/phi^2 (= 0.382): the phi^2 block forces c >= d[1]/phi^2 and
    # the phi^4 entry forces c <= d_top/phi^4, so nonempty needs d[1]*phi^2 <= d_top. The scene has
    # d[1]/d_top = 20/33 = 0.606 > 0.382 -> its nonzero spectrum is too BUNCHED for the AF GEOMETRIC ladder.
    # A control with the SAME multiplicities but a SPREAD spectrum (small d[1]/d_top) MUST admit the k=5 corner;
    # inverting the mass (same eigenvalues {0,20,22,24,33}, permuted multiplicities) must NOT (same d[1]/d_top).
    def feasible_on(spectrum, k):
        pat = corner_pattern(k)
        d = sorted(spectrum)
        n = len(d)
        lo, hi = 0.0, 1e18
        for i in range(k):
            p = pat[i]
            if p > 0:
                lo = max(lo, d[i] / p)
                hi = min(hi, d[i + n - k] / p)
            elif d[i] > 1e-9:
                return False
        return lo <= hi + 1e-9
    spread = sorted([0] * 1 + [2] * 12 + [8] * 10 + [20] * 8 + [33] * 2)  # d[1]/d_top = 2/33 = 0.061 < 0.382
    if not feasible_on(spread, 5):
        die("SPREAD_CONTROL  a SPREAD spectrum (d[1]/d_top small) must ADMIT the k=5 corner")
    print("PASS_SPREAD_CONTROL_ADMITS  a control spectrum with the SAME multiplicities but a SPREAD range "
          "(d[1]/d_top = 2/33 = 0.061 < 1/phi^2) DOES admit the k=5 corner -> the true cause is the scene's "
          "spectral BUNCHING (d[1]/d_top = 20/33 = 0.606 > 0.382), i.e. too little dynamic range for the AF "
          "geometric ladder, NOT mass concentration.")
    inverted = sorted([0] * 1 + [20] * 2 + [22] * 8 + [24] * 10 + [33] * 12)  # same eigenvalues, permuted mults
    if feasible_on(inverted, 5):
        die("INVERTED_CONTROL  permuting multiplicities (same eigenvalues, same d[1]/d_top) must NOT open k=5")
    print("PASS_INVERTED_MASS_STILL_BLOCKED  permuting the multiplicities (same eigenvalue SET {0,20,22,24,33}, "
          "so same d[1]/d_top = 0.606) leaves k=5 infeasible -> confirms the obstruction is the eigenvalue "
          "RANGE (bunching), independent of how the mass is distributed across those eigenvalues.")

    print("PASS_VNEXT2_SCENE_SPECTRAL_LIFT_INTERLACING_NOGO — the full AF spectral lift is NO-GO against ALL "
          "UCP corners (not just unitaries): spectral bunching (d[1]/d_top = 20/33 > 1/phi^2) empties the "
          "Cauchy bracket at every k>=5. Small stages (k<=4) embed. Status sharpened; owner stays NO-GO.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
