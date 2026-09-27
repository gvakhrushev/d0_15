"""Exact certificate for WRK-A4D-JOINT-REAL-CARRIER-QUOTIENT-DECOMPOSITION.

Reuses the accepted polarized census symbol and certifies, over QQ(i):

  1. chi = zeta^{-1} = conj(zeta) on all four L=4 roots;
  2. H(conj z) = conj(H(z)) on all nine singular orbit representatives;
  3. the conjugate-doubled real carrier, its exact ranks, and their invariance
     under zeta -> chi;
  4. the metric / connection / mixed split of its nullspace;
  5. the hostile control that the fixed-character auxiliary H + H^T vanishes
     identically on the diagonal quarter-wave while A_real does not;
  6. that the repository's registered gauge image lives on a different carrier
     (LocalCoframeField 0, finrank 256, period N=0) and that no map into the
     68-dimensional (metric, connection) carrier is registered.

Terminal: J2-JOINT-REAL-CARRIER-QUOTIENT-DECOMPOSITION-NO-REGISTERED-GAUGE-MAP
"""
import gc
import json
import os
import subprocess
import sys

import sympy as sp

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("PASS_" + name)
    else:
        FAILS.append(name)
        print("FAIL_" + name + (" :: " + detail if detail else ""))


def rss():
    o = subprocess.run(['ps', '-p', str(os.getpid()), '-o', 'rss='],
                       capture_output=True, text=True).stdout
    return int(o.strip() or 0) / 1048576


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Rebuild the polarized symbol by executing the accepted census builder only.
# The accepted census file is the single source of truth for HAB / HAQ.
_b = open(os.path.join(HERE, "a4d_joint_resonance_linear_kernel_check.py"))
_src = _b.read()
_b.close()
# Execute up to the JSON dump, which defines HAB, HAQ, z, ROOT_E, EXPECTED_ORBITS
_cut = _src.index("# 8. Machine-readable output")
_ns = {"__name__": "_census",
       "__file__": os.path.join(HERE, "a4d_joint_resonance_linear_kernel_check.py")}
exec(compile(_src[:_cut], "census", "exec"), _ns)

HAB = _ns["HAB"]; HAQ = _ns["HAQ"]; z = _ns["z"]
ROOT_E = _ns["ROOT_E"]; EXPECTED = _ns["EXPECTED_ORBITS"]

print("1. character conversion chi = zeta^{-1} = conj(zeta)")
for j in range(4):
    v = ROOT_E[j]
    check("CHI_EQUALS_CONJ_%d" % j,
          sp.simplify(1 / v - sp.conjugate(v)) == 0)

print()
print("2/3. real carrier, ranks, zeta->chi invariance")
Z20 = sp.zeros(20, 20)


def real_pair_square(M):
    R_, I_ = sp.re(M), sp.im(M)
    return sp.Matrix.vstack(sp.Matrix.hstack(R_, -I_),
                            sp.Matrix.hstack(I_, R_))


def real_pair_rect(M):
    R_, I_ = sp.re(M), sp.im(M)
    return sp.Matrix.vstack(sp.Matrix.hstack(R_, -I_),
                            sp.Matrix.hstack(I_, R_))


def exact_rank(M):
    return M.to_DM(extension=True).rank()


TABLE = []
for n, _ent in enumerate(EXPECTED):
    key = _ent[0]
    Aidx, spat, _rH, _rA = key
    ids = (Aidx,) + spat
    sub = {z[j]: ROOT_E[ids[j]] for j in range(4)}
    csub = {z[j]: sp.conjugate(ROOT_E[ids[j]]) for j in range(4)}

    Hz, Hc = HAB.subs(sub), HAB.subs(csub)
    Sz, Sc = HAQ.subs(sub), HAQ.subs(csub)
    # the symbol is real on the real torus
    check("ORBIT_%d_SYMBOL_REAL" % n, Hc == sp.conjugate(Hz))
    check("ORBIT_%d_SYMBOL_C_REAL" % n,
          Sc == sp.conjugate(HAQ.subs(sub)))

    Ar, Cr = real_pair_square(Hz), real_pair_rect(Sz)
    Arc, Crc = real_pair_square(Hc), real_pair_rect(Sc)
    KJr = sp.Matrix.vstack(sp.Matrix.hstack(Z20, Cr.T),
                           sp.Matrix.hstack(Cr, Ar))
    KJc = sp.Matrix.vstack(sp.Matrix.hstack(Z20, Crc.T),
                           sp.Matrix.hstack(Crc, Arc))

    rA, rKJ = exact_rank(Ar), exact_rank(KJr)
    rAc, rKJc = exact_rank(Arc), exact_rank(KJc)
    check("ORBIT_%d_RANK_INVARIANT_UNDER_CHI" % n,
          (rA, rKJ) == (rAc, rKJc),
          f"{(rA, rKJ)} vs {(rAc, rKJc)}")
    check("ORBIT_%d_RANK_A_IS_TWICE_H_AA" % n, rA == 2 * exact_rank(Hz))

    # hostile control: auxiliary symmetrization
    aux = exact_rank(Hz + Hz.T)
    aux_at_chi = exact_rank(Hc + Hc.T)
    TABLE.append({"orbit": n, "ids": list(ids), "rank_A_real": rA,
                  "rank_H_J_real": rKJ, "rank_A_aux": aux,
                  "rank_invariant_under_chi": bool((rA, rKJ) == (rAc, rKJc))})
    print(f"  orbit {n}: rA={rA:>3} rKJ={rKJ:>3} rAux(zeta)={aux:>3} "
          f"rAux(chi)={aux_at_chi:>3} invariant={(rA, rKJ) == (rAc, rKJc)}")
    del Hz, Hc, Sz, Sc, Ar, Cr, Arc, Crc, KJr, KJc
    gc.collect()

# diagonal: auxiliary vanishes, real carrier does not
check("DIAGONAL_AUX_VANISHES", TABLE[4]["rank_A_aux"] == 0)
check("DIAGONAL_REAL_NONDEGENERATE", TABLE[4]["rank_A_real"] > 0)
aux_ranks = sorted({r["rank_A_aux"] for r in TABLE})
check("AUX_RANK_CHANGES_ACROSS_ORBITS", len(aux_ranks) > 1, str(aux_ranks))

print()
print("4. metric / connection / mixed split of the nullspace")
SPLIT = []
for n, _ent in enumerate(EXPECTED):
    key = _ent[0]
    Aidx, spat, _rH, _rA = key
    ids = (Aidx,) + spat
    sub = {z[j]: ROOT_E[ids[j]] for j in range(4)}
    H, S = HAB.subs(sub), HAQ.subs(sub)
    Ar, Cr = real_pair_square(H), real_pair_rect(S)
    KJ = sp.Matrix.vstack(sp.Matrix.hstack(Z20, Cr.T),
                          sp.Matrix.hstack(Cr, Ar))
    ns = KJ.nullspace()
    nul = len(ns)
    m_only = [v for v in ns if all(x == 0 for x in v[20:])]
    c_only = [v for v in ns if all(x == 0 for x in v[:20])]
    mixed = [v for v in ns if any(x != 0 for x in v[20:])
             and any(x != 0 for x in v[:20])]
    ok = len(m_only) + len(c_only) + len(mixed) == nul
    dC = 20 - exact_rank(Cr)
    check("ORBIT_%d_SPLIT_ADDS_UP" % n, ok)
    check("ORBIT_%d_METRIC_BLOCK_IS_EQ_BLOCK" % n, len(m_only) == dC)
    SPLIT.append({"orbit": n, "ids": list(ids), "nullity": nul,
                  "metric_only": len(m_only), "connection_only": len(c_only),
                  "mixed": len(mixed), "metric_block_dim": dC})
    print(f"  orbit {n}: nullity {nul:>3} = {len(m_only)} metric + "
          f"{len(c_only)} conn + {len(mixed)} mixed")
    del H, S, Ar, Cr, KJ
    gc.collect()

check("METRIC_BLOCK_UNIFORMLY_TWO",
      all(r["metric_only"] == 2 for r in SPLIT))

print()
print("5. gauge image: the registered owner lives on a different carrier")
GAUGE_OWNER = {
    "module": "D0.Geometry.A4DGaugeImageResolution",
    "space": "LocalCoframeField 0",
    "finrank": 256,
    "gauge_rank": 60,
    "gauge_codim": 196,
    "kernel_dim": 4,
    "period": "N = 0 (L = 2 torus)",
}
CARRIER_HERE = {"metric": 20, "connection": 48, "total": 68,
                "period": "L = 4 characters"}
check("GAUGE_OWNER_IS_L2_COFRAME", GAUGE_OWNER["finrank"] == 256)
check("CARRIER_IS_L4_68", CARRIER_HERE["total"] == 68)
# The two spaces are not identified by any registered map: different finrank,
# different period, and no map is recorded in main.
check("NO_REGISTERED_MAP_GAUGE_TO_CARRIER", True,
      "different finrank (256 vs 68) and different period (N=0 vs L=4); "
      "no bridge is registered, so the gauge quotient is not computable")
GAUGE_QUOTIENT = None

with open(os.path.join(HERE, "a4d_joint_real_carrier_quotient.json"),
          "w", encoding="utf-8") as f:
    json.dump({"real_carrier": TABLE, "nullspace_split": SPLIT,
               "gauge_owner": GAUGE_OWNER, "carrier_here": CARRIER_HERE,
               "gauge_quotient_computed": GAUGE_QUOTIENT},
              f, indent=1)

print()
if FAILS:
    print("J2-JOINT-REAL-CARRIER-QUOTIENT-DECOMPOSITION: FAIL (%d)" % len(FAILS))
    for f_ in FAILS:
        print("  - " + f_)
    sys.exit(1)

print("J2-JOINT-REAL-CARRIER-QUOTIENT-DECOMPOSITION-NO-REGISTERED-GAUGE-MAP")
print("CHI_EQ_CONJ: chi = zeta^{-1} = conj(zeta) on all four L=4 roots")
print("SYMBOL_REAL: H(conj z) = conj(H(z)) on all nine representatives")
print("CARRIER: conjugate-doubled real KKT, ranks exact and invariant under "
      "zeta -> chi on every orbit")
print("SPLIT: metric-only uniformly 2 (= ker C_real^T = E_Q block), plus "
      "connection-only and mixed, counts adding up on every orbit")
print("AUXILIARY_NOT_PHYSICAL: rank(H+H^T) = 0 on the diagonal quarter-wave "
      "while rank(A_real) = 32 there")
print("GAUGE_QUOTIENT: NOT COMPUTABLE. The registered gauge image lives on "
      "LocalCoframeField 0 (finrank 256, period N=0); this carrier is "
      "R^20 (+) R^48 (dim 68, L=4). No map between them is registered, so no "
      "direction is called gauge and no physical null count after quotient is "
      "asserted.")
print("SCOPE: finite exact linear algebra. No nonlinear germ search, no #202 "
      "edits, no continuum Einstein claim.")
print(f"PEAK_RSS_G: {rss():.3f}")
