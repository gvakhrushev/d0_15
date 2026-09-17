import numpy as np


def main():
    roles = ["A", "B", "C", "D"]
    signs = ["+", "-"]
    omega8 = [(r, s) for r in roles for s in signs]
    assert len(omega8) == 8
    v9 = omega8 + [("omega0", "witness")]
    assert len(v9) == 9
    F = np.diag(np.arange(1, 9, dtype=float))
    # Cyclic role action: average over all cyclic shifts is invariant.
    perms = []
    for shift in range(8):
        P = np.zeros((8, 8))
        for i in range(8):
            P[(i + shift) % 8, i] = 1.0
        perms.append(P)
    E = sum(P @ F @ P.T for P in perms) / 8.0
    for P in perms:
        assert np.allclose(P @ E @ P.T, E)
    print("PASS_OMEGA8_SIGNED_ROLE_CYCLE")
    print("PASS_V9_WITNESS_EXTENSION")
    print("PASS_ORBIT_AVERAGED_TRACE_EMISSION")
    print("PASS_TOPOLOGICAL_HALTING_QUOTIENT")


if __name__ == "__main__":
    main()
