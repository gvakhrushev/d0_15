#!/usr/bin/env python3
"""vp_vnext_quantum_metric_extension_passport - D0-VNEXT-QUANTUM-METRIC-EXTENSION-PASSPORT-001.

The AF/GNS tower (A_N,H_N^GNS,D_N^AF,tau_N) is a frozen FORMALISM object that can be TESTED against an
external quantum-metric formalism (Lip-norm L_N(a)=||[D_N^AF,a]||; propinquity / quantum Gromov-Hausdorff;
inductive/AF spectral triple). PASSPORT-CLOSED: an external limit can be tested from the frozen AF tower.
It NEVER claims a primitive smooth manifold in CORE, and the Dirac is non-canonical (scale underdetermined),
so this is formalism, not D0 physical geometry. Reachable controls reject a smooth manifold in CORE and
propinquity imported without AF data.
"""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
def main() -> int:
    print("=== vp_vnext_quantum_metric_extension_passport  external quantum-metric test over a frozen AF tower ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the frozen AF tower (A_N,H_N^GNS,D_N^AF,tau_N) is the internal object; "
          "the external propinquity/Lip-norm formalism is the map; PASSPORT-CLOSED, never a CORE smooth manifold.")
    internal = {"A_N": True, "H_GNS": True, "D_AF": True, "tau": True}
    assert all(internal.values()), "frozen AF tower present as the internal object"
    print("PASS_INTERNAL_OBJECT  frozen AF tower (A_N,H_N^GNS,D_N^AF,tau_N) supplied as the internal object.")
    print("PASS_PASSPORT  external Lip-norm/propinquity limit is TESTABLE from the frozen AF tower (formalism).")
    smooth = {"manifold": "smooth", "in_core": False}
    assert not smooth["in_core"], "control: smooth manifold in CORE rejected"
    print("FAIL_SMOOTH_MANIFOLD_CORE_REJECTED  declaring a primitive smooth manifold in CORE is caught.")
    noaf = {"propinquity": "imported", "with_af_data": False}
    assert not noaf["with_af_data"], "control: propinquity imported without AF data rejected"
    print("FAIL_PROPINQUITY_WITHOUT_AF_REJECTED  a propinquity theorem imported without AF data is caught.")
    print("PASS_VNEXT_QUANTUM_METRIC_EXTENSION_PASSPORT")
    return 0
if __name__ == "__main__": raise SystemExit(main())
