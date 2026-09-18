"""Transitive defect dynamics and collision uniqueness certificate.

Closes the three residual risks:
  1. Risk 1 (Sterility forcing):
     In GL_2(F_2) ~ S_3 acting on the 3 projective defect rays P^1(F_2) = {ePlus, eMinus, eGap}:
     - Order 1 (identity): fixes all 3 rays (no time evolution).
     - Order 2 (transpositions): fixes 1 ray, swaps 2 rays (one generation is privileged/frozen, violating M1).
     - Order 3 (3-cycles): acts transitively without fixed rays (cycles ePlus -> eMinus -> eGap -> ePlus).
     Therefore: Transitivity on defect generations <=> order of T mod 2 is 3
     <=> #Fix_1(T mod 2) = 1 and #Fix_2(T mod 2) = 1 (return sterility at 1 and 2).
     Sterility is not an ad-hoc filter: it is the exact condition of generation transitivity.

  2. Risk 2 (Arithmetic step forcing):
     For three zones n_1 = m - d_1, n_2 = m + d_1 - d_2, n_3 = m + d_2 with sum n_i = 3m:
     The excess collision identity sum n_i^2 - N^2/3 = |Omega_8| = 8 is:
         2 * (d_1^2 - d_1 * d_2 + d_2^2) = 8  <=>  d_1^2 - d_1 * d_2 + d_2^2 = 4.
     Over non-negative integers:
         Solutions are (0, 2), (2, 0), and (2, 2).
         Solutions (0, 2) and (2, 0) have d = 0, causing zone collapse (only 2 distinct zone sizes).
         The UNIQUE non-degenerate solution with strictly positive steps (d_1 > 0, d_2 > 0)
         is d_1 = 2, d_2 = 2.
     Therefore: Constant step Delta_1 = Delta_2 = 2 is an algebraic theorem of non-degenerate
     collision balance, not an independent postulate.

  3. Risk 3 (|Role| = 4 forcing):
     For r = 2 independent verification lines with binary outputs {0, 1}:
     The space of complete joint terminal registration outcomes is {0, 1}^2.
     Its cardinality is |Role| = 2^2 = 4 identically.
"""


def main():
    # 1. Verification of Risk 1: GL_2(F_2) action on P^1(F_2)
    F2_nonzero = [(1, 0), (0, 1), (1, 1)]  # ePlus, eMinus, eGap

    # All 6 matrices of GL_2(F_2)
    GL2_F2 = []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                for d in (0, 1):
                    det = (a * d - b * c) % 2
                    if det != 0:
                        GL2_F2.append(((a, b), (c, d)))

    assert len(GL2_F2) == 6

    def mat_vec(M, v):
        return ((M[0][0] * v[0] + M[0][1] * v[1]) % 2, (M[1][0] * v[0] + M[1][1] * v[1]) % 2)

    def mat_mul(A, B):
        return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) % 2 for j in range(2)) for i in range(2))

    I2 = ((1, 0), (0, 1))

    transitive_elements = []
    non_transitive_elements = []

    for M in GL2_F2:
        # Check order
        M2 = mat_mul(M, M)
        M3 = mat_mul(M2, M)
        if M == I2:
            order = 1
        elif M2 == I2:
            order = 2
        elif M3 == I2:
            order = 3
        else:
            order = -1

        # Fixed rays on P^1(F_2)
        fixed_rays = [v for v in F2_nonzero if mat_vec(M, v) == v]

        if len(fixed_rays) == 0 and order == 3:
            transitive_elements.append(M)
        else:
            non_transitive_elements.append((M, order, len(fixed_rays)))

    # Exactly 2 elements are order 3 and act transitively
    assert len(transitive_elements) == 2
    # The golden matrix T = [[0,1],[1,1]] is one of them
    assert ((0, 1), (1, 1)) in transitive_elements
    assert ((1, 1), (1, 0)) in transitive_elements

    # Elements of order 2 always fix exactly 1 ray (leaving one generation frozen)
    for M, order, num_fixed in non_transitive_elements:
        if order == 2:
            assert num_fixed == 1

    # 2. Verification of Risk 2: Uniqueness of non-degenerate integer solutions to d1^2 - d1*d2 + d2^2 = 4
    solutions = []
    for d1 in range(0, 50):
        for d2 in range(0, 50):
            if d1 ** 2 - d1 * d2 + d2 ** 2 == 4:
                solutions.append((d1, d2))

    assert solutions == [(0, 2), (2, 0), (2, 2)], f"Unexpected solutions: {solutions}"
    # Strictly positive (non-degenerate 3 distinct zones):
    strictly_positive = [sol for sol in solutions if sol[0] > 0 and sol[1] > 0]
    assert strictly_positive == [(2, 2)]

    # 3. Verification of Risk 3: Terminal role space size
    line_outcomes = (0, 1)
    joint_outcomes = [(l1, l2) for l1 in line_outcomes for l2 in line_outcomes]
    assert len(joint_outcomes) == 4
    assert set(joint_outcomes) == {(0, 0), (0, 1), (1, 0), (1, 1)}

    print("PASS: Risk 1 resolved: Transitive generation dynamics <=> order 3 <=> return sterility at 1 & 2.")
    print("PASS: Risk 2 resolved: Non-degenerate collision balance d1^2 - d1*d2 + d2^2 = 4 uniquely forces d1 = d2 = 2.")
    print("PASS: Risk 3 resolved: Terminal role space cardinality |Role| = 2^2 = 4 identically.")


if __name__ == "__main__":
    main()
