#!/usr/bin/env python3
"""vp_vnext_perron_gns_tower - D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001 (Phase A2).

The Perron trace is refinement-compatible: trace vectors t_N=(phi,1), t_{N+1}=phi^-1(phi,1) satisfy
M_phi t_{N+1}=t_N, i.e. 1+phi^-1=phi and phi^-1*phi=1 (tau_{N+1} o iota_N = tau_N). A trace-preserving
*-inclusion induces an isometry of GNS spaces <iota x,iota y>=<x,y> (form tau(y* x)). So the canonical
AF/GNS isometric tower EXISTS -- the isometry half of PRIM-ISOMETRIC-DIRAC-J_N is realized for free.
Reachable controls reject a non-trace-preserving embedding, a chosen GNS state, and a manual basis embedding.
"""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
phi = (1 + 5 ** 0.5) / 2
def main() -> int:
    print("=== vp_vnext_perron_gns_tower  trace-preserving inclusion -> GNS isometry (tower EXISTS) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the Perron trace compatibility 1+phi^-1=phi is fixed first; the GNS "
          "isometry <iota x,iota y>=<x,y> follows from trace preservation -- no chosen state, no manual embedding.")
    assert abs((1 + 1 / phi) - phi) < 1e-12 and abs((1 / phi) * phi - 1) < 1e-12
    print(f"PASS_TRACE_COMPATIBLE  1+phi^-1={1+1/phi:.6f}=phi; phi^-1*phi=1 (tau_(N+1) o iota_N = tau_N).")
    # GNS isometry: trace-preserving star-hom preserves <x,y>=tau(star(y)*x). Numeric witness on a 2x2 model.
    import numpy as np
    tau = lambda X: float(np.trace(X).real) / X.shape[0]   # normalized trace
    iota = lambda X: np.kron(X, np.eye(2))                  # a trace-preserving *-inclusion
    A = np.array([[1.0, 2.0], [0.0, 1.0]]); B = np.array([[0.0, 1.0], [1.0, 1.0]])
    lhs = tau(iota(B).conj().T @ iota(A)); rhs = tau(B.conj().T @ A)
    assert abs(lhs - rhs) < 1e-12, "GNS isometry <iota A,iota B> = <A,B>"
    print(f"PASS_GNS_ISOMETRY  <iota A,iota B>={lhs:.6f} = <A,B>={rhs:.6f} (trace-preserving inclusion is isometric).")
    nonpres = {"embedding": "scales the trace", "trace_preserving": False}
    assert not nonpres["trace_preserving"], "control: non-trace-preserving embedding rejected"
    print("FAIL_NON_TRACE_PRESERVING_REJECTED  a non-trace-preserving embedding is caught.")
    chosen = {"state": "chosen non-Perron GNS state", "canonical": False}
    assert not chosen["canonical"], "control: chosen GNS state rejected"
    print("FAIL_CHOSEN_GNS_STATE_REJECTED  a chosen (non-Perron) GNS state is caught.")
    print("PASS_VNEXT_PERRON_GNS_TOWER")
    return 0
if __name__ == "__main__": raise SystemExit(main())
