# Independent review of the original-record port-price packet

Reviewer: native_variational. Date: 2026-10-20. Scope: mathematical review of
`original_record_source.md` §§1, 3a, 4 and the finite Poisson-corrector kernel
proof; source inspection of the symbolic, gap, cluster and corrector checkers.
No repository changes and no new scientific claim are made here. Root owns the
final executions; this review does not claim an independent successful rerun.

Reviewed source directory, relative to the repository root:
`02_REGISTRY/research/sources/d0_native_price_source_synthesis_2026-10-20/`.
The proof and checker filenames below are relative to that directory.
The final proof was compared with the originally reviewed scratch version:
only its contribution/snapshot introduction, evidence-label wording,
repository-portable commands, and removal of the superseded preliminary probe
reference changed. No mathematical statement or argument changed. All four
listed checker copies have the identical reviewed bytes. This is exact review
evidence, not assembly acceptance.

**Verdict: PASS within the stated fixed-finite-carrier, isolated-gap and
initial-clock scope.** No sign, normalization, Schur-complement or clock
identification error was found. Preserve the following exact distinctions.

1. With `beta = n epsilon`, the actual paid port cost is
   `n + p Tr(rho F_cost)`. Its first feedback term is exactly
   `p (beta^2 - beta epsilon) Gamma_h / 2`, where
   `Gamma_h = Tr(rho L_h^* Delta_h)`. The coefficient
   `p beta^2 Gamma / 2` belongs to the successive small-step/initial-clock
   statement. At fixed integer `n`, only the baseline `n` has zero field
   derivative automatically. This is not a uniform theorem at fixed positive
   macroscopic clock.

2. The local paired-Julia normalization is `1/8` for the sixteen Kraus terms.
   The independent link equation is
   `K_* = -C(H) H' / (2 L(H))`, and the reduced coefficient is
   `G_eff = A - C^2/(4 L)`. At `H = 0`, `K_* = -H'/4`; the Levi-Civita value
   `+H'/2` is not stationary for this price. The single owned `C_v^*` Kraus
   square, with the half-weight occupied q state, supplies
   `G_eff >= nu^2/8` independently of K. The external prefactor
   `lambda nu^2/8` in Gamma remains present. The Schur elimination here concerns
   the initial-clock coefficient, not the full finite-clock action.

3. The gap certificate for the corrected stationary-link family is
   `-nu^2 k^2 a^2 P_bad / 32`. The Levi-Civita family's corresponding coefficient
   is `/8`; it must not be substituted for the stationary-link certificate.
   Since `K_*/H' = -1/4 + O(H^2)`, its linear perturbation is minus one half
   the Levi-Civita perturbation and the quadratic spectral splitting is one
   quarter as large, exactly as the gap checker verifies algebraically.

4. The scalar fixedRIGHT preparation on the whole isolated rank-eight cluster
   does not require its eigenvalues to remain degenerate. The spectral
   projector commutes with the full preparation Hamiltonian. If its perturbation
   B starts at second clock order and remains below the chosen spectral gap,
   the stationary trace has correction `Tr(P_0 B)/rank` and remainder
   `O(||B||^2/gap)`. Thus the projector repair leaves the second clock coefficient
   intact and first changes the stationary value at fourth clock order. Source
   versions use a finite parameter neighborhood with uniform gap and bounded
   parameter derivatives. Neither refinement-uniform bounds nor selection among
   other momentum sectors follow from this argument.

5. **Explicit translation to the actual paid cost.** Section 4 is written for
   `H_eff = Delta + p^3 F_n`, `Q = Delta - c Delta^2`. The identical whole-cluster
   argument for `R + Cost_port` uses
   `H_eff_cost = Delta + p F_n_cost`, `Q_cost = Delta`:
   replace `p^3` by `p` and `Q` by `Delta` throughout. Its unperturbed scalar
   function is `g_cost(Delta) = (1 + p beta) Delta`; its first perturbation is
   `p (beta^2 - beta epsilon) L^* Delta / 2`. Consequently the stationary
   scalar-cluster repair retains the **actual paid-cost** coefficient in item 1,
   not merely the conditional code-KL coefficient.

6. The finite Poisson-corrector kernel proof is sound. Self-adjoint paired T is
   Hilbert-Schmidt positive, with Dirichlet form
   `sum_W ||[W,X]||_HS^2 / 16`. The full Mat(16) CAR commutator sum has scalar
   kernel and smallest nonzero eigenvalue 2. Hence the traceless contraction
   gap can be bounded by
   `delta >= nu^2 sigma_min(B_H)^2 / 8`.
   The involution conjugation in `S = Ad_Gamma T` preserves the traceless space
   and its norm, so `||S|| <= 1-delta` there without a commutation assumption.
   Therefore `I-S` has the stated unique traceless inverse and the Neumann
   solution of the cubic corrector equation is valid. This finite internal
   inverse does not itself prove a uniform lattice ultraviolet or finite-clock
   theorem.

Reviewed input SHA-256 values (snapshot at review completion):

```text
3e038dd9fae47bee12e9df6c27ed2b0816c577a47e0581cf6b9f84e976f3cc0c  original_record_source.md
287e745fb180934213a17469ed5d93f100c5e6b09766207b899ce1904e6dddea  price_equivalence2_symbolic.py
ebddb3ebcb2b7254ab03cfa3c23e4a7bb225e349217724c9e1b92c7b1b44afb3  price_equivalence2_gap.py
0a0667b65733bc1649c1fa503aaa489f944942949c5a7d5128f37c7a405482ce  price_equivalence2_corrector.py
331fda7b0e49feabd3a078127c089ddedd204247c89de8585f950d51dc7e4a24  price_equivalence2_cluster.py
```
