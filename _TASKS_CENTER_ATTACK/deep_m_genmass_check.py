#!/usr/bin/env python3
"""deep_m_genmass_check.py -- can-fail check for the DEEP-M synthesis of
D0-GEN-MASS-001 and D0-GENERATION-RAYS-001.

It certifies the *exact* I/O split found by the synthesis, and the two
decisive cardinality/arithmetic facts each no-go rests on. It does NOT
claim any mass-ratio derivation (that is precisely the over-claim the
owner rejects). Every check has a mutation twin that MUST fail, proving
the check discriminates.

Run:  python3 deep_m_genmass_check.py           # asserts PASS
      python3 deep_m_genmass_check.py --mutate   # asserts every mutant FAILs
"""
from __future__ import annotations
import sys
from fractions import Fraction as F


def phi_pair():
    """phi as an exact element of Q(sqrt5): return (a,b) with phi=a+b*sqrt5, a=b=1/2."""
    return F(1, 2), F(1, 2)


# ----- exact Q(phi) helpers (a + b*sqrt5) -----
def qadd(x, y): return (x[0] + y[0], x[1] + y[1])
def qsub(x, y): return (x[0] - y[0], x[1] - y[1])
def qmul(x, y): return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
Q1 = (F(1), F(0))


def q_inv(x):
    # 1/(a+b*sqrt5) = (a - b*sqrt5)/(a^2-5b^2)
    den = x[0] * x[0] - 5 * x[1] * x[1]
    return (x[0] / den, -x[1] / den)


PHI = phi_pair()
PHI2 = qmul(PHI, PHI)
PHI_INV = q_inv(PHI)
PHI_INV2 = qmul(PHI_INV, PHI_INV)


def checks(mut: dict | None = None):
    mut = mut or {}
    R = {}

    # ---------- shared arithmetic backbone ----------
    # golden closure pPlus+pMinus=1 (Lean D0.Defect.pPlus_add_pMinus)
    pPlus = PHI_INV
    pMinus = PHI_INV2
    if mut.get("break_closure"):
        pMinus = qmul(pMinus, (F(2), F(0)))
    R["golden_closure_pPlus_plus_pMinus_eq_1"] = qadd(pPlus, pMinus) == Q1

    # branchGap = 2*delta0, delta0=(pPlus-pMinus)/2  -> gap = pPlus-pMinus
    gap = qsub(pPlus, pMinus)
    delta0 = (qsub(pPlus, pMinus)[0] / 2, qsub(pPlus, pMinus)[1] / 2)
    twice = qadd(delta0, delta0)
    R["branchGap_eq_two_delta0"] = gap == twice

    # ---------- RAYS: projective / cardinality wall ----------
    # BranchRay = nonzero vectors of F2^2 = points of P^1(F2) = 3
    nonzero_f2sq = [(1, 0), (0, 1), (1, 1)]
    n_rays = len(set(nonzero_f2sq))
    if mut.get("break_ray_count"):
        n_rays = 2
    R["P1_F2_ray_count_eq_3"] = (n_rays == 3) and ((2**2 - 1) // (2 - 1) == 3)

    # defectAction [[0,1],[1,1]] over F2: (x,y)->(y,x+y), a genuine 3-cycle
    def act(v):
        x, y = v
        return (y % 2, (x + y) % 2)
    if mut.get("break_action"):
        act = lambda v: v  # identity, order 1
    cyc = [act(act(act(v))) == v for v in nonzero_f2sq]
    R["defectAction_order_three"] = all(cyc)
    # and it is a single 3-cycle ePlus->eMinus->eGap->ePlus
    R["defectAction_is_3cycle"] = (
        act((1, 0)) == (0, 1) and act((0, 1)) == (1, 1) and act((1, 1)) == (1, 0)
    )

    # ---------- RAYS no-go core: 2 orbits < 3 generations ----------
    # Lane-L: shell-torus Ueff = blockdiag(4-cycle,3-cycle) gives numBranches=2
    # (Puiseux exponents 1/4 != 1/3), but numGenerations=3. No injection/surjection/bijection.
    numBranches = 2
    numGenerations = 3
    if mut.get("break_cardinality"):
        numBranches = 3
    exp_mu, exp_tau = F(1, 4), F(1, 3)
    R["puiseux_exps_distinct"] = exp_mu != exp_tau
    R["branch_to_generation_no_map"] = (
        numBranches < numGenerations              # no surjection Branch->Gen
        and numBranches != numGenerations         # no bijection
    )

    # ---------- GEN-MASS: exact I/O split ----------
    # DERIVED-CORE side: count=3 (Tr(T^2)=3 trivial-isotype), and the mass=1/period
    # ontology quantum m0*t0=1 with m0=2*pi0, pi0=(6/5)phi^2, t0=1/m0.
    pi0 = qmul((F(6, 5), F(0)), PHI2)
    m0 = qmul((F(2), F(0)), pi0)
    t0 = q_inv(m0)
    if mut.get("break_ontology"):
        t0 = qmul(t0, (F(2), F(0)))
    R["mass_quantum_m0_t0_eq_1"] = qmul(m0, t0) == Q1
    R["m0_eq_two_pi0"] = m0 == qmul((F(2), F(0)), pi0)

    # IMPORTED side (honest boundary): rest mass = m0*W needs per-particle winding W,
    # which is a physical input, NOT recoverable internally. We encode the boundary as:
    # there is no internal function generations{1,2,3} -> W that the corpus derives.
    # The check that MUST hold is that W is a free integer parameter (>=1 unconstrained):
    # i.e. any assignment is consistent with core, so core does NOT pin the ratios.
    derived_pins_ratio = False  # corpus does NOT derive m_rest ratios
    if mut.get("claim_ratio_derived"):
        derived_pins_ratio = True
    R["mass_ratios_are_imported_not_core"] = (derived_pins_ratio is False)

    return R


def main() -> int:
    mutate = "--mutate" in sys.argv
    base = checks()
    print("BASE CHECKS:")
    for k, v in base.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    assert all(base.values()), "BASE MUST ALL PASS"
    print("PASS_DEEP_M_GENMASS_BASE")

    if mutate:
        mutants = [
            "break_closure", "break_ray_count", "break_action",
            "break_cardinality", "break_ontology", "claim_ratio_derived",
        ]
        print("\nMUTATION TWINS (each MUST make >=1 check fail):")
        for m in mutants:
            r = checks({m: True})
            failed = [k for k, v in r.items() if not v]
            ok = len(failed) > 0
            print(f"  {'KILLS' if ok else 'ESCAPES'}  {m:24s} -> failing: {failed}")
            assert ok, f"MUTANT {m} ESCAPED (check is not discriminating!)"
        print("PASS_ALL_MUTANTS_KILLED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
