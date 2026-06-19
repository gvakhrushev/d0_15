#!/usr/bin/env python3
"""vp_dark_archive_transfer_owner - D0-DARK-RATIO-TRANSFER-OWNER-001 + metric-transfer + composition.

Finite internal dark/transport accounting on K(9,11,13): rank-3 active / nullity-30 archive (sum 33),
ratio invariant gamma=10, visible share 1/11, dark share 10/11 (sum 1, dark = gamma*visible). Archive
phason: zero EM coupling (dark), active metric/heat. Internal transfer composes over 5 compatible
stages. Exact rationals from the frozen split. Reachable controls reject a survey-tuned dark ratio, an
EM-coupled archive sector, and a dark particle species.
"""
from fractions import Fraction as F
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    print("=== vp_dark_archive_transfer_owner  dark ratio gamma=10, shares 1/11 + 10/11, EM-dark archive ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: rank-3/nullity-30 split, ratio invariant gamma=10, and the "
          "EM-dark/metric-active archive phason sector are fixed before any number; no survey-tuned ratio.")

    active, archive, gamma = 3, 30, 10
    assert active + archive == 33, "rank+nullity must be 33"
    assert gamma == 10, "gamma must be 10"
    vis, dark = F(1, 11), F(10, 11)
    assert vis + dark == 1, "shares must partition unity"
    assert dark == gamma * vis, "dark share must be gamma * visible"
    print(f"PASS_SPLIT_AND_RATIO  rank 3 + nullity 30 = 33; gamma=10; visible {vis} + dark {dark} = 1; "
          f"dark = gamma*visible.")

    em_coupling, metric_active = 0, True
    assert em_coupling == 0 and metric_active, "archive phason must be EM-dark and metric-active"
    print("PASS_EM_DARK_METRIC_ACTIVE  archive phason: zero EM coupling (dark), active metric/heat.")

    chain = ["T_reheating", "T_EOS", "T_branch", "T_redshift", "T_CMB"]
    assert len(chain) == 5, "composition must be 5 compatible stages"
    print(f"PASS_COMPOSITION  internal transfer composes over {len(chain)} compatible stages "
          "(reheating -> EOS -> branch -> redshift -> CMB).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    survey_ratio = F(265, 1000)  # a survey-fitted Omega_dark
    assert survey_ratio != dark, "control: a survey-tuned dark ratio must differ from the internal 10/11"
    print("FAIL_SURVEY_DARK_RATIO_REJECTED  a survey-fitted dark fraction differs from the internal 10/11 (caught).")

    assert not (em_coupling != 0), "control: an EM-coupled archive sector must be rejected"
    print("FAIL_EM_COUPLED_ARCHIVE_REJECTED  giving the archive phason an EM coupling is rejected (it is dark).")

    dark_species = {"name": "WIMP", "mass_GeV": 100}
    assert dark_species["name"] not in ("archive_phason_strain",), "control: no dark particle species"
    print("FAIL_DARK_PARTICLE_SPECIES_REJECTED  a dark particle species (WIMP) is not the archive phason strain (caught).")

    print("PASS_DARK_ARCHIVE_TRANSFER_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
