#!/usr/bin/env python3
"""D0-TORAL-TIME-MARKOV-CONJUGACY-001 no-go certificate.

The topological obstruction is Lean-owned: a nontrivial connected torus cannot
be homeomorphic to a totally disconnected SFT.  This certificate guards the
independent matrix-level mismatch and prevents the old raw-conjugacy wording
from being silently reintroduced as an algebraic equality.
"""


def trace2(a):
    return a[0][0] + a[1][1]


def main() -> int:
    T = ((0, 1), (1, -1))
    N_tau = ((0, 1), (1, 1))

    assert trace2(T) == -1
    assert trace2(N_tau) == 1
    assert trace2(T) != trace2(N_tau)

    # The positive replacement is a factor/semiconjugacy or boundary quotient,
    # not a homeomorphism Torus2 ~= raw SFT.
    print("PASS_TORAL_SFT_TOPOLOGICAL_CONJUGACY_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
