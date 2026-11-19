# D0 → GR: causal closure of the native 65-label port-CQ source

**Date:** 22 October 2026. **Parent:** gvakhrushev/d0_15, scientific Draft PR #334.
**Read baseline:** b4a1c590ebb7c52e5be7618fa193d48a5176ad62.
**Status:** analytical finite-history identities + bounded original-CAR16 numerical application. Not a selected Book03 action, physical full42 writer, interval root certificate, or GR closure.

## 0. What is new in this continuation

The preceding owner already reduced the *literal* full128 port charge minus complete recorded quantum entropy gain to 65 merged labels, retaining a forced net coefficient p³ for each ordinary pair. We consume that identity unchanged.

This note supplies its explicit **causal value / preparation-covector / field-source system**, rather than leaving the remaining 65-label archive as an unnamed entropy. On the actual original CAR16 fixture, forward conditioning, direct complete history blocks, and a backward matrix-covector recurrence agree. The same calculation keeps a nonzero independent preparation equation. A separate theorem extends the previously computed two-tick rare-record logarithmic coefficient to a lower bound at **every fixed finite horizon**.

The entropy chain rule, efficient-measurement information identities, and differentiation of matrix entropy are standard tools, not discoveries claimed here. The contribution is this typed substitution into the unchanged native execution, its explicit response equations, numerical reproduction, and the finite-horizon extension.

## 1. Unchanged instrument, price, and information cut

Put p=(sqrt(5)−1)/2 and ell=ln(phi). Keep the original 128 Kraus slots K_(j,b), original CAR order (0,2,3,1), original phases (i,i,−1,−i), and all retained reference systems. For j≠0 the already proved relation is

    K_(j,0) = p M_j,        K_(j,1) = sqrt(p) M_j.

Keep K_(0,0) and K_(0,1) separate. The mathematical merged alphabet has 65 slots: blank, orphan, and 63 ordinary pairs, including structurally dark slots. Denote its Kraus maps by L_z and its *effective net weights* by

    d_blank=1,    d_orphan=2,    d_pair=p³.

These are NOT new physically paid fractional tariffs. The actual fine port tariff remains 1+b. The p³ is the exact remainder after subtracting the actual paired-bit entropy:

    (p²+2p) − H_phi(p²,p) = (p²+2p)−(2−p)=2p−1=p³.

For a normalized initial state Omega on DATA and any actually retained reference R, each map below means L_z tensor I_R. For a K-word w=(z_1,...,z_K), define

    L_w=L_(z_K)...L_(z_1),  X_w=L_w Omega L_w†,
    d(w)=sum_t d_(z_t),     eta(X)=Tr(X ln X),  0 ln0=0.

The consumed complete *port-CQ-gain component* is

    P_K(Omega) = sum_w d(w) Tr X_w
                 + [sum_w eta(X_w) − eta(Omega)] / ell.          (1)

It equals the original fine cost minus [S(Gamma_fine,K)−S(Omega)]/ell, not merely the entropy of a terminal DATA marginal. All chronological words, failures, and actual original fine ports remain in the underlying execution. This is a mathematical rewriting, not an erase operation.

The fixed-window scope is important. A merged-label-adapted stopping tree admits the corresponding boundary recursion. A stopping rule that reads a merged-away port bit needs a separate proof. History-dependent factory/controller costs outside the given port tariff are not included by fiat.

## 2. Exact causal closure of the complete remaining archive

For any unnormalized positive X, let

    X_z=L_z X L_z†,
    g_y(X)=sum_z d_z Tr X_z + [sum_z eta(X_z)−eta(X)]/ell.

Set P_0=0. Then

    P_(K+1),y(X) = g_y(X) + sum_z P_K,y(X_z).                    (2)

**Proof.** Substitute (1) for each subtree. The terms −eta(X_z) from the subtree roots cancel the +eta(X_z) in g_y. The remaining blocks are precisely the original chronological products of length K+1; their cost is the first letter's cost plus that of the continuation. No commutation or independence is used. Trace preservation gives sum_z Tr X_z=Tr X and also proves positive homogeneity P_K(aX)=aP_K(X), a≥0.

For normalized sigma, define the actual filter

    q_z(sigma)=Tr(L_z sigma L_z†),
    T_z(sigma)=L_z sigma L_z†/q_z(sigma)    when q_z>0.

Homogeneity gives the equivalent expectation recursion

    P_(K+1)(sigma)=g(sigma)+sum_z q_z(sigma) P_K(T_z(sigma)).     (3)

Consequently

    P_K(Omega)=E_Omega sum_(t=0)^(K−1) g(sigma_t).               (4)

The growing archive is represented by the **distribution of its conditional states**, together with the accumulated price. It is NOT replaced by the average state E sigma_t. Even when that mean is the stationary rho_*, the conditional states and predictive probabilities change after each observed outcome.

This is an exact state-space recursion, not a proof that 65 labels form a 65-state Markov chain. The space of conditional density matrices is generally continuous. Exact enumeration may still have exponentially many branches. Individual trajectory evaluation uses a matrix state and an accumulated score, but finite-sampling precision is not free.

For an arbitrary correlated Omega_DR, the required state in (2)–(4) is the conditional **DR state**. DATA alone supplies future local outcome probabilities, but need not supply the complete DR entropy gain. For a pure retained input and one Kraus map per word, every conditional global state is pure; then the entropic component is exactly the Shannon entropy of the complete words, with the full probabilities generated by the DATA filter.

## 3. The preparation equation is an explicit matrix, not an omitted derivative

Work on a chart where the indicated entropy derivatives exist, with constant support rank. Logarithms of singular states are restricted to their support; local gradients are defined on that support face. In particular, no ordinary C² claim is made across rank births.

Define a preparation covector G_K by

    D_X P_K(X)[Z]=Tr(G_K(X) Z).

Let C=sum_z d_z L_z†L_z. At a full-rank initial input, or restricted to its support face, put

    G_g(X)=C + [sum_z L_z† ln(X_z) L_z − ln X]/ell.              (5)

The +I terms from differentiating eta cancel by trace preservation on the relevant face. The exact backward recurrence is

    G_0=0,
    G_(K+1)(X)=G_g(X)+sum_z L_z† G_K(X_z) L_z.                  (6)

An independent direct complete-word expression is

    G_K(Omega)=sum_w d(w)L_w†L_w
              + [sum_w L_w† ln(X_w)L_w−ln Omega]/ell.           (7)

Equations (6) and (7) are equal, not two different score choices.

A genuinely free trace-one, full-rank preparation must satisfy G_K=lambda I for this component alone, with every additional actual price included for the physical equation. A preparation constrained to a fixed-spectrum unitary orbit instead requires [G_K,Omega]=0. A generated input Omega(y) has the chain contribution Tr(G_K D_y Omega). A constraint reaction or a preparation price must be derived from the actual execution; neither is set to zero here.

## 4. Full field-source recursion, including all preparation dependence

Let A_K(X)=(partial_y P_K,y)(X) hold X fixed; this can be a covector with any finite number of field coordinates. Write

    dot X_z=(dot L_z)X L_z†+L_z X(dot L_z)†

for that fixed-X variation. The local source is

    A_g(X)=sum_z [d_z Tr(dot X_z)+(dot d_z)Tr X_z]
           + sum_z Tr[(ln X_z+I)dot X_z]/ell.                  (8)

For the unchanged Golden weights, dot d_z=0. Then

    A_0=0,
    A_(K+1)(X)=A_g(X)+sum_z {A_K(X_z)+Tr[G_K(X_z)dot X_z]}.    (9)

The full pulled-back source is therefore

    D_y P_K(Omega(y))=A_K(Omega)+Tr[G_K(Omega)D_y Omega].        (10)

The equations are valid for coframe, link, material, apparatus, and independent input directions **when their actual same-execution Kraus/input jets are supplied**. Their generality is not evidence that the missing native full42 field writer has been constructed. This calculation supplies the derivative mechanism, not that physical map.

Normalized forward conditioning provides a third computation. For each branch,

    dot q_z=Tr(dot X_z),
    dot sigma_z=(dot X_z−sigma_z dot q_z)/q_z,
    dot w_z=dot w q_z+w dot q_z.                               (11)

Differentiating (4) with both weight and state jets reproduces (10). Dropping dot w is a biased source calculation. Replacing sigma_t by rho_* is an independence/reset assumption absent from the original dynamics.

## 5. Reference information: a bounded value correction with a real source

For the same efficient recorded instrument acting on D only, compare (1) on Omega_DR with the DATA-only cut rho_D=Tr_R Omega. Use the same port cost in both.

Choose a mathematical purification E of Omega_DR only for the proof, not as a freely supplied physical resource. Conditional global DRE states remain pure. The chain rule yields

    P_K(rho_D)−P_K(Omega_DR)=I(W:R|E)/ell,
    0 <= P_K(rho_D)−P_K(Omega_DR) <= S(rho_D)/ell <= ln(d_D)/ell. (12)

**Proof.** The difference between the full pure DRE entropy gain H(W) and the DATA gain is I(W:RE)=S(rho_D)−sum_w q_w S(rho_D|w). The analogous difference for DR is I(W:E). Subtracting gives I(W:R|E). Nonnegativity is conditional-mutual-information positivity; the upper bound follows from I(W:RE)<=S(rho_D). No horizon-dependent approximation enters.

For an initial pure DR purification, E is trivial and (12) reduces to

    P_K(DATA)−P_K(pure DATA+R)=I(W:R)/ell,
    I(W:R)=S(rho_D)−sum_w q_w S(rho_D|w).                      (13)

An unrelated product spectator has zero correction. A correlated retained reference generally does not. The correction divided by K is uniformly bounded in **value** by ln(d_D)/(K ell). This alone proves no convergence of its field derivative; its exact finite source remains D I(W:R|E)/ell.

The ordinary efficient-measurement entropy-reduction/information relation is established literature (M. E. Shirokov, *Entropy reduction of quantum measurements*, arXiv:1011.3127). It is used here to type the original retained-reference comparison, not as a new D0 axiom.

## 6. Executed original native checks

The original five constructor functions were read through the GitHub connector and placed in `native_excerpt.py`. The source is the original CAR16 Fourier fixture at r=1/9, nu=3/5. Its stationary mixed input is rho_*=Delta^-1/Tr Delta^-1, including the full normalization derivative. This is NOT the separately constructed spatial DATA128/full42 writer.

The following values are numerical; no outward interval claim is made. Each P_K is the **declared original fine port-CQ-gain component**, reproduced through its exact 65-slot reduction. The effective weights (1,2,p³) must not be mistaken for literal primitive spending.

| Fixed K | P_K, mixed DATA / product spectator | d_r P_K, moving rho_* | d_r P_K, pure retained purification |
|---:|---:|---:|---:|
| 1 | 0.728700489392904 | 0.029033337025975 | 0.028153414296617 |
| 2 | 1.457400970617167 | 0.058066505317327 | 0.056306879166007 |
| 3 | 2.186101443673716 | 0.087099504950723 | 0.084460394451072 |

At K=2:

    full source                  0.058066505317326884
      = fixed-input field source 0.051013828320106
      + preparation reaction     0.007052676997218954.

The all-entry backward/direct preparation-covector discrepancy is 5.02e-14. The traceless preparation-covector Frobenius norm is approximately 0.0741612515951674; thus the supplied invariant marginal is not silently an unconstrained stationary input of this price. One explicit independently allowed mathematical density tangent has derivative 0.0077572129609405.

The fixed-native-boost central secant, recreating BOTH the instrument and its invariant input, is 0.0580665056315599. Its difference from the analytical source is about 3.14e-10.

The two-step actual merged predictive defect is

    2 H(Z_1)−H(Z_1,Z_2) = 6.5125406e-10 nats,
    d_r defect          = 2.43362164e-8.

It was checked independently as a direct joint KL sum, not only a subtraction of close entropies. The reference correction at the same horizon is I(W:R)=0.000339113699471 nats with derivative 0.000846752911699; its price-source effect is about 0.00175962615132. These are two DIFFERENT memory effects: prediction across time and correlation with the initial reference.

The direct fullfine replay covers K=1 and K=2, with 64 and 4096 positive words in the original 128 and 128²-slot alphabets. The merged K=3 calculation retains 35,937 positive words in the 65³-slot alphabet; equivalence to the fullfine K=3 score uses the analytical scalar-refinement theorem rather than a falsely claimed fullfine replay. All other structural slots remain zero outcomes, not postselected away.

Normal Python and Python -O outputs were byte-identical. Thresholds 1e-12, 1e-13, and 1e-14 for relative positive eigen-support gave matching reported values and sources at the stated tolerances. The first development run failed an unjustified diagnostic lower threshold for the predictive defect; `DEVELOPMENT_NOTES.md` retains that correction. No original 1764-entry interval root, Lean build, or remote CI was rerun.

## 7. New all-finite-horizon extension of the original logarithmic archive source

Consume the preceding exact original zero-boost owner: the genuine 128 instrument has 22 newborn fine labels, each zero at r=0 but with nonzero first Kraus jet. For the unchanged trace input I16/16,

    sum_newborn Pr(alpha;r)=C1 r²+O(r³),
    C1=99 p²/512000>0,       Phi_0(I16/16)=I16/16.              (14)

For any fixed finite K, let C_K be the total r² coefficient of every chronological word that has zero probability at r=0. Then

    C_K >= K C1.                                               (15)

**Proof.** At any specified tick t, the input at r=0 is still I16/16 by unitality. The event of a newborn label at that tick therefore has coefficient C1. A history with newborn labels at two specified ticks has amplitude O(r²) and probability O(r⁴). For fixed K, inclusion-exclusion gives probability K C1 r²+O(r³) for at least one newborn label. All such words are zero-probability words at r=0. Any additional formerly dark word made only of old-live labels has a nonnegative squared-amplitude r² coefficient. Adding it cannot lower C_K.

For the complete fine-pointer score with the original literal port tariff and a pure retained purification of I16/16,

    S_fine,K(r)=A_K(r)+(2 C_K/ell)r² ln r+O(r³|ln r|),
    d_r S_fine,K contains (4 C_K/ell)r ln r,
    4 C_K/ell >= 99 K p²/(128000 ell).                         (16)

Here A_K is analytic locally; (16) is a fixed-K expansion as r approaches zero from above. No K→infinity/r→0 interchange or uniform remainder is claimed. The actual code expenditure is analytic and cannot remove the displayed coefficient from this declared measured-record component.

This identifies an archive contribution that is extensive in the finite horizon's singular coefficient, in contrast to the bounded initial-reference correction (12). The two should not be conflated.

A separate original-matrix K=3 diagnostic found all 42³=74,088 old-live triple products nonzero, with smallest Frobenius norm 2.63e-7. It agrees numerically with C3=3C1 and source coefficient 0.00184176793737. This supports equality at K=3 on that fixture but is not an exact all-K equality certificate. The rigorous general conclusion is the lower bound (15), conditional on the already owned exact (14).

## 8. Concrete consumption by the existing GR target

The existing unpadded N1 constitutive target is

    D S_N1 = kappa {tau sum_s[a_s D f_B,s+b_s D q_s]
                    −sum_s V_s D rho_s}.

No new geometric root or freely chosen score is needed to state the comparison. On an actually identified execution the measured port-CQ part has the explicit source (10), its initial-input covector (6), and its original chronological memory contributions. Every genuinely additional selected Book03 heat, feedback, pathwise Info, factory, controller, work, and clock term must have its own source.

A valid assembly must identify the actual map from the original 42 fields and independent inputs to L_z and Omega, demonstrate that the physical valuation really contains the declared component (1), then compare the complete resulting covector to the N1 target. The formulas here are not permission to subtract a calculated mismatch or declare a new Info law.

**Closed here:** exact causal representation and source differentiation of the previously unresolved 65-label port-CQ archive for a supplied original instrument, a numerical original-native application through K=3, its explicit preparation reaction, and an all-finite-horizon logarithmic lower-bound extension.

**Not closed:** compulsory M1/G0 writer and controller admission, selected original Book03 scene heat/cut/pathwise Info, full42 same-execution physical equality, independent apparatus equations, raw216 uniform refinement, or universal GR. `GR_closed=false`.

## Source ownership and reproduction

- Original instrument: `02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py`, Git blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed`.
- Consumed exact tariff/refinement: `02_REGISTRY/research/sources/d0_native_stationary_memory_composition_2026-10-22/LITERAL_PORT_PRICE_REDUCTION.md`, publication `72bdcd4da644f4df1724b706a9c407281cd27b6e`.
- Prior complete-history source: `02_REGISTRY/research/A4D_NATIVE_COMPLETE_SOURCE_REDUCTION_2026_10_22.md`.
- Prior exact newborn coefficient: `02_REGISTRY/research/sources/d0_native_minimal_reflection_entropy_2026-10-22/check_native_two_tick_information_birth.py` and its analytical owner.
- Native unpadded target: `02_REGISTRY/research/A4D_UNPADDED_GOLDEN_N1_CONSTITUTIVE_LEGENDRE_COMPLETE_2026_10_22.md`.

Run from this packet directory:

```sh
OPENBLAS_NUM_THREADS=1 python check_native65_causal_source.py
OPENBLAS_NUM_THREADS=1 python -O check_native65_causal_source.py
OPENBLAS_NUM_THREADS=1 python check_archive_birth_extension.py
```

The supplied constructor is a connector-read executable excerpt, not a full Git checkout. Receipts explicitly preserve this provenance limitation. The package is local and is not evidence of a remote commit or merge.
