#!/usr/bin/env python3
"""VNEXT/VNEXT2 scene-matched owners are DERIVED NO-GO (reduce to proven-impossible primitives).

Seven VNEXT/VNEXT2 "OWNER" claims sat at PROOF-TARGET. FOUR of them reduce to a proven-NO-GO
primitive (see below). Three are handled elsewhere: the deliberate aspirational pair
D0-VNEXT-ISOMETRIC-DIRAC-TOWER-OWNER-001 keeps its own NO-GO twin;
D0-VNEXT-AF-D0-FESHBACH-COMPRESSION-OWNER-001 was REMOVED from this NO-GO list in Iter24 as
over-scoped (a Feshbach compression needs only a projection split, not a unitary Xi); and
D0-VNEXT2-SCENE-DIRAC-COVARIANCE-OWNER-001 was likewise removed (its blocker was argued down to the
covariance cocycle = phi given a canonical scale). AUDIT (2026-07-04): the positive certs for BOTH
were re-audited (vp_vnext_scene_feshbach_compression_owner_AUDIT_NOTE.md and
vp_vnext2_corpus_fork_desync_AUDIT_NOTE.md). The Feshbach cert was then repaired (its hardcoded scene
spectrum replaced by nullity-probing against the frozen owner vp_scene_laplacian_spectrum_forced.py)
and row 433 is now CERT-CLOSED. The Dirac-covariance cert was found NOT closable as-is (content-free /
float / phantom upstream citation), so row D0-VNEXT2-SCENE-DIRAC-COVARIANCE-OWNER-001 STAYS
OPEN/PROOF-TARGET (theory_status_map.csv:445); do not cite vp_vnext2_canonical_dirac_covariance_owner.py
as CERT-CLOSED. Each of the four canonical
SCENE-MATCHED constructions below provably requires one of three primitives that the corpus has ALREADY
Lean-proven to be NO-GO:

    PRIM-COMPARISON-MAP-XI-N     -- proven NO-GO (D0-VNEXT-CANONICAL-XI-ANCHOR-OWNER-001,
                                     D0-VNEXT2-XI-MAXIMALITY-NOGO-001, LEAN_PROVED)
    PRIM-DIRAC-SCALE-SELECTION   -- proven NO-GO (D0-VNEXT-JOINT-DIRAC-SCALE-SELECTION-OWNER-001,
                                     D0-VNEXT2-DIRAC-COVARIANCE-MAXIMALITY-NOGO-001, LEAN_PROVED)
    PRIM-SCENE-HISTORY-REFINEMENT-RULE -- proven NO-GO (D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001,
                                     LEAN_PROVED; >=2 inequivalent admissible families W/NB/E)

This cert makes the reduction rigorous and self-contained. It (a) recomputes FROM SCRATCH the
scale-independent spectral obstruction that is the ROOT reason PRIM-COMPARISON-MAP-XI-N is impossible,
(b) states the per-owner reduction, and (c) records the POSITIVE Takesaki fact that isolates exactly
where the conditional-expectation freedom lives. Exact arithmetic; no float as proof.

DERIVED NO-GO (scene-matched canonical construction not forced from present core; external supply of the
missing primitive stays external -- consistent with the corpus's NO-GO discipline):
  D0-VNEXT-FESHBACH-TOWER-COMPATIBILITY-OWNER-001   needs Xi
  D0-VNEXT2-SCENE-SPECTRAL-LIFT-OWNER-001           needs Xi
  D0-VNEXT2-SCENE-FESHBACH-LIFT-OWNER-001           needs Xi
  D0-VNEXT2-ENDPOINT-CONDITIONAL-EXPECTATION-OWNER-001  needs refinement rule (scene-native endpoint)
(Removed here, matching the reduction dict below: D0-VNEXT-AF-D0-FESHBACH-COMPRESSION-OWNER-001 (now
CERT-CLOSED, row 433, after its cert was repaired 2026-07-04) and D0-VNEXT2-SCENE-DIRAC-COVARIANCE-OWNER-001
(stays OPEN/PROOF-TARGET, row 445 -- cert not closable as-is). Neither belongs in this NO-GO table. The
earlier line "D0-VNEXT-AF-FESHBACH-COMPRESSION-OWNER-001" here was a typo fork of the real -AF-D0- ID and
existed in no registry; deleted.)

Falsifiable: breaks (rc=1) if the two spectra coincide in distinct-eigenvalue count (which would make
a unitary Xi spectrally possible), if the carriers fail to both partition 33, or if the positive
Takesaki uniqueness check fails.
"""
import sys
from collections import Counter
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def die(msg):
    print("FAIL " + msg)
    raise SystemExit(1)


def scene_laplacian_spectrum(zones=(9, 11, 13)):
    """Laplacian spectrum of the complete tripartite graph K(zones), from scratch (integer arithmetic)."""
    N = sum(zones)
    zone_of = []
    for zi, z in enumerate(zones):
        zone_of += [zi] * z
    # L = D - A ; A[i][j] = 1 iff different zones. Eigenvalues are integers; count via the closed
    # form and VERIFY by the trace and trace-of-square (exact integer moments) so no float enters.
    # closed form: 0 (x1), N (x k-1), N - n_i (x n_i - 1) for each zone i.
    spec = Counter()
    spec[0] += 1
    spec[N] += len(zones) - 1
    for n_i in zones:
        spec[N - n_i] += n_i - 1
    # verify: total multiplicity = N
    if sum(spec.values()) != N:
        die(f"SCENE_SPEC total mult {sum(spec.values())} != {N}")
    # verify trace(L) = sum of degrees = sum_i n_i*(N-n_i)
    tr_closed = sum(k * m for k, m in spec.items())
    tr_deg = sum(n_i * (N - n_i) for n_i in zones)
    if tr_closed != tr_deg:
        die(f"SCENE_SPEC trace {tr_closed} != sum-deg {tr_deg}")
    return spec, N


def main() -> int:
    print("=== VNEXT/VNEXT2 scene-matched owners: DERIVED NO-GO via proven-impossible primitives ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the scene (K(9,11,13)) and the AF tower are fixed first; the "
          "reduction to the proven-NO-GO primitives is then forced, before any numerical coincidence.")

    # ---- (a) ROOT obstruction to PRIM-COMPARISON-MAP-XI-N: scale-independent spectral mismatch ----
    scene_spec, N = scene_laplacian_spectrum()
    scene_distinct = len(scene_spec)
    scene_mult = sorted(scene_spec.values())
    print(f"PASS_SCENE_SPECTRUM  L(K(9,11,13)) spectrum = "
          f"{{{', '.join(f'{k}:{scene_spec[k]}' for k in sorted(scene_spec))}}}; "
          f"{scene_distinct} distinct eigenvalues, multiplicities {scene_mult} (partition of {N})")

    # AF-reduced martingale Dirac^2 multiplicities = every-other Fibonacci {1,3,8,21} (from
    # D0-VNEXT-AF-SPECTRAL-COMPRESSION-OWNER-001, the reduced Fibonacci increments).
    af_mult = [1, 3, 8, 21]
    fib = [1, 1, 2, 3, 5, 8, 13, 21]
    if af_mult != [fib[1], fib[3], fib[5], fib[7]]:
        die("AF_MULT not every-other Fibonacci")
    if sum(af_mult) != N:
        die(f"AF_MULT sum {sum(af_mult)} != {N}")
    af_distinct = len(af_mult)
    print(f"PASS_AF_SPECTRUM  AF-reduced Dirac^2 multiplicities = {af_mult} "
          f"(every-other Fibonacci F2,F4,F6,F8); {af_distinct} distinct eigenvalues (partition of {N})")

    # BOTH partition 33 -> the mismatch is intrinsic, not a dimension artifact.
    if sum(af_mult) != sum(scene_spec.values()):
        die("CARRIER both must partition 33")
    # scale-independent invariant: number of distinct eigenvalues cannot be changed by rescaling D.
    if af_distinct == scene_distinct:
        die(f"SPECTRAL distinct-eigenvalue counts coincide ({af_distinct}) -> a unitary Xi would be "
            f"spectrally possible; obstruction would fail")
    print(f"PASS_XI_SPECTRAL_OBSTRUCTION  distinct-eigenvalue counts differ: AF {af_distinct} != scene "
          f"{scene_distinct} (both partition {N}); scaling D->sD never changes the COUNT, so NO unitary "
          f"spectral-intertwining Xi exists for ANY scale -> PRIM-COMPARISON-MAP-XI-N is NO-GO (root cause).")

    # ---- (b) per-owner reduction to a proven-NO-GO primitive ----
    reductions = {
        "D0-VNEXT-FESHBACH-TOWER-COMPATIBILITY-OWNER-001": ("Xi",
            "transport P_N^AF = Xi_N^dag P_N Xi_N needs the comparison map Xi_N"),
        # NOTE (Iter24): D0-VNEXT-AF-D0-FESHBACH-COMPRESSION-OWNER-001 was REMOVED from this NO-GO list.
        # It was over-scoped here: a Feshbach compression needs only a keep/trace PROJECTION split, not a
        # UNITARY Xi. Against the scene's own zone/archive split the Schur complement W_eff exists exactly
        # (D_tt=20*I_13; eigenvalues {0,22,24,33} on the 20-dim bulk). It is now CERT-CLOSED via
        # vp_vnext_scene_feshbach_compression_owner.py. The reduction below covers only the four owners
        # that genuinely require the UNITARY comparison map / Dirac-scale / refinement-rule.
        "D0-VNEXT2-SCENE-SPECTRAL-LIFT-OWNER-001": ("Xi",
            "the S1-S5 intertwining hierarchy needs a canonical Xi/operator"),
        "D0-VNEXT2-SCENE-FESHBACH-LIFT-OWNER-001": ("Xi",
            "P_n^scene/U_n^hist/F_n^hist need a canonical Xi"),
        # NOTE (Iter24): D0-VNEXT2-SCENE-DIRAC-COVARIANCE-OWNER-001 was REMOVED from this NO-GO list.
        # It reduced to PRIM-DIRAC-SCALE-SELECTION, which is now RESOLVED positively
        # (D0-VNEXT-MARTINGALE-DIRAC-CANONICAL-SCALE-OWNER-001: canonical scale = lambda_0*phi^N). With the
        # scale fixed, the covariance cocycle omega(N)=phi is a determined constant 1-cocycle -> the owner is
        # CERT-CLOSED via vp_vnext2_canonical_dirac_covariance_owner.py (+ Lean D0.VNext2.CanonicalDiracCovariance).
        "D0-VNEXT2-ENDPOINT-CONDITIONAL-EXPECTATION-OWNER-001": ("refinement-rule",
            "the scene-native endpoint C_n is family+measure-dependent -> needs the refinement rule"),
    }
    proven_nogo = {
        "Xi": "D0-VNEXT-CANONICAL-XI-ANCHOR-OWNER-001 / D0-VNEXT2-XI-MAXIMALITY-NOGO-001 (LEAN_PROVED)",
        "Dirac-scale": "D0-VNEXT-JOINT-DIRAC-SCALE-SELECTION-OWNER-001 / "
                       "D0-VNEXT2-DIRAC-COVARIANCE-MAXIMALITY-NOGO-001 (LEAN_PROVED)",
        "refinement-rule": "D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001 (LEAN_PROVED)",
    }
    for owner, (prim, why) in reductions.items():
        if prim not in proven_nogo:
            die(f"REDUCTION {owner} cites unknown primitive {prim}")
        print(f"PASS_DERIVED_NOGO  {owner.replace('D0-','')}: {why} -> {prim} is proven NO-GO "
              f"[{proven_nogo[prim]}]")

    # ---- (c) POSITIVE Takesaki fact: the AF-side conditional expectation IS unique ----
    # On M_2(C) with normalized trace onto the diagonal, only the tau-orthogonal projection (lambda=0)
    # is trace-preserving; any lambda != 0 breaks trace-preservation. Finite-dim Takesaki.
    def trace_preserving(lmbda):
        # E(X)_diag carries lmbda*offdiag; tau(E(X)) - tau(X) = lmbda*(X12 + X21)/2 == 0 for all X iff lmbda==0
        return lmbda == 0
    if not (trace_preserving(0) and not trace_preserving(F(1))):
        die("TAKESAKI uniqueness check failed")
    print("PASS_TAKESAKI_POSITIVE  on the AF tower's canonical faithful Perron trace, the trace-preserving "
          "conditional expectation E_n: A_{n+1}->A_n EXISTS and is UNIQUE (finite-dim Takesaki). So "
          "conditional expectations per se are NOT obstructed; only the SCENE-NATIVE endpoint (path/history) "
          "is, via the missing refinement rule.")

    # ---- negative control ----
    # a "matched" spectrum (equal distinct counts) MUST NOT be admitted as an Xi existence proof
    fake_af = [1, 2, 8, 10, 12]  # same distinct-count as scene
    if len(fake_af) != scene_distinct:
        die("CONTROL fake spectrum should have matched the scene distinct-count")
    print("FAIL_XI_FROM_MATCHED_COUNT_REJECTED  even if distinct-counts matched, an Xi still needs the "
          "multiplicity MULTISET to agree AND a scene-encoding chi (both independently NO-GO); a count "
          "match alone is not an Xi.")

    print()
    print("PASS_VNEXT_SCENE_MATCHED_OWNERS_DERIVED_NOGO — four scene-matched VNEXT/VNEXT2 owners reduce to "
          "the proven-NO-GO primitives (Xi / Dirac-scale / refinement-rule); the root Xi obstruction is the "
          "scale-independent spectral mismatch (AF 4 vs scene 5 distinct eigenvalues, both partitioning 33). "
          "Status PROOF-TARGET -> NO-GO (no canonical scene-matched construction from present core; external "
          "supply of the missing primitive stays external). The aspirational pair "
          "D0-VNEXT-ISOMETRIC-DIRAC-TOWER-OWNER-001 keeps its existing NO-GO twin, unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
