# Native compiler, source and initial-resource boundary

17 October 2026. Analytical continuation from `e397a0af8383e5026353d6d54382202bb5c57a00`.
Consumer: the [complete exit/action quotient](A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md), Sections 5–7. No new action, physical admission, helper, spectral replay or Lean theorem is asserted here.

The new result is an exact finite-word obstruction in a specified grammar, together with the resource bypass and the accuracy conditions under which the existing approximate compiler transfers the **full price source**. It is not an obstruction to D0 or to refinement limits.

## 1. Existing compiler: consume it rather than rebuild its extractor

The [addressed palette](A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md), Section 1, is copies of
`G=[[a,-p],[p,a]]`, CNOT and specified basis preparations, with all records retained. Physical addressability/preparation is a separate premise.
The original v5 proof already constructs approximate first-success/ready/CSWAP logic using positive powers of G, including coherent phases and all work registers. Its Section 4 proves

```text
||U_tilde-U|| <= epsilon,
||U_tilde,i-U_i|| <= epsilon B_i,
B_i=sum_j ||V_j,i||.
```

Only fixed control rotations are replaced; actual field-dependent return jets remain inputs. Its full-logdet bound retains the active-cut rank. Repeating the extractor is therefore not the next result.

The original text resource is
`02_REGISTRY/research/sources/d0_native_controller_v5_2026-10-14/proofs/NATIVE_COMPILER_AND_FULL_ARCHIVE_ACTION_RU.md`, SHA-256 `a123c96233c62a1a05cc01b0a5be706ca4cff10765f781797b7859c4d50547e4`.
It is now available as [readable repository text](sources/d0_native_controller_v5_2026-10-14/proofs/NATIVE_COMPILER_AND_FULL_ARCHIVE_ACTION_RU.md), byte-identical to the [v4/v5 capsule](sources/d0_v4_v5_verified_capsule_2026-10-14/MANIFEST.json). The eight concatenated parts have SHA-256 `91b030d62c93afa6bf2a23be28051d764e54f12a7e5a13cd75ed732427c913be`; decompressed JSON SHA-256 is `3062ab678735883022bdc011471ae438d5a30bdcb013acea549bfd572e97564f`. Only this one proof text was extracted after both capsule and text hashes were checked; no capsule program or old calculation was executed. Relevant text: Sections 0–4, especially lines 160–218 on source/rank and lines 168–197 on the field interface.

## 2. Exact obstruction for computational blanks, including the whole B

Put `A=Z[a]`, `a^4+a^2-1=0`, `p=a^2`. Every element of A is an algebraic integer; p is a unit because `p(p+1)=1`.
The literal golden gate/inverse, signs, CNOT and shift permutations, integer CAR creators, tensor products and finite controlled placements preserve A. With computational basis blanks and integral isometric input/output codes, every matrix coefficient and blank compression remains in A. Therefore `1/sqrt(32)` cannot be a matrix coefficient: its square `1/32` is a rational noninteger and hence not an algebraic integer.

The obstruction is not tied to one Walsh decomposition. Choose the strict constant coefficient `nu=p`, identity return matrices and periodic shifts `S_r` with side length at least 3. Retain the full 16 CAR coordinates. Then

```text
d=(p/h) sum_r c_r(S_r-I),
Delta=(p^2/h^2) sum_r(2I-S_r-S_r^*) tensor I16,
alpha=p^2 h^2/128,
B=I-(p^4/128) sum_r(2I-S_r-S_r^*) tensor I16.       (1)
```

Even the individual coefficient/Julia roots are integral at this datum: `sqrt(1-p^2)=a`, with roots `I+(a-1)N_r` or `I+(a-1)(I-N_r)` for the creator projections. A nearest-neighbour coefficient of the desired B is `p^4/128`. It is not integral: multiplying by the integral unit `p^-4` would make `1/128` integral. Thus no finite circuit in this **computational-blank integral grammar** has exactly the whole return B in (1).

This says neither that the datum (1) is physically admitted by the original engine nor that every D0 primitive belongs to this grammar. Independently supplied nonintegral states/code coordinates, other continuous native operations, or conditional normalization change its hypotheses. The [v8 owner](sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md), Section 2, explicitly supplies uniform32 preparation and gives only conditional approximate G/CNOT compilation.

## 3. The actual seed is an important resource bypass

The [literal engine](certificates/a4d_native_closed_record_engine.py), `seed()`, stores raw `m_1=m_15=1`; its norm squared is 2. Its normalized ray is not an integral basis blank. In mask coordinates, under the declared addressed-CNOT interface,

```text
(|1>+|15>)/sqrt2 = |1>_0 (|000>+|111>)_123/sqrt2,
CX_(1->2) CX_(1->3):
    (|1>+|15>)/sqrt2 -> |1>_0 |+>_1 |0>_2 |0>_3.     (2)
```

Five independently supplied seed copies therefore contain five exact fair logical bits after two CNOTs each. This is a conditional decoder of supplied resources, not a circuit that prepares the seed from blanks, copies an unknown state, supplies its preparation adjoint/reflection, or derives an allowed cut. A single seed does not supply five independent fair bits.

There is exact denominator accounting. Let `K=Q(a)` and `O_K` be its algebraic integers. Starting with k independent normalized two-term seeds and otherwise computational blanks, any finite integral circuit followed by a computational event has

```text
Pr(event) in 2^(-k) O_K.                              (3)
```

Indeed its raw amplitudes are integral and share normalization `2^(k/2)`; a coordinate-event probability is a finite sum of squared amplitudes divided by `2^k`. If it equals `1/32`, then `2^(k-5)` is a rational algebraic integer, forcing `k>=5`. Equation (2) attains the fair-bit preparation count when the five copies/addresses are supplied. It does not implement the entire Q, reflection or B. Nonintegral event/code projectors are outside (3).

## 4. Fixed-palette continuity and the missing field interface

On one fixed carrier the finite words of a fixed countable matrix palette form a countable set. A continuous map from a connected field neighbourhood into this set is constant: any nonconstant real or imaginary matrix entry would have an interval, hence uncountable, in its image. Thus pointwise universality does not itself give a C1 realization of an arbitrary moving instrument. Discontinuous changes of word have no corresponding Euler derivative.

This does not freeze actual input amplitudes or native field-dependent generators. Changing pairings/trivializations can also create a real jet, which must be differentiated. The v5 theorem correctly retains actual geometric returns and compiles only constant controls. For a field-independent approximation `S_epsilon` to controller S, use its true unprepare `S_epsilon^*`:

```text
Q=S^* V(X) S, Q_epsilon=S_epsilon^* V(X) S_epsilon,
||Q_epsilon-Q|| <= 2 epsilon,
||partial_I Q_epsilon-partial_I Q||
    <= 2 epsilon ||partial_I V||,  1<=|I|<=2.         (4)
```

These bounds are for actual shared SELECT jets. They cannot manufacture the field-to-Julia/SELECT map from fixed-gate synthesis. A non-Hermitian approximate blank A is harmless for positivity: the canonical golden return `B_epsilon=I-2p^2 A_epsilon^* A_epsilon` still satisfies `p^3 I<=B_epsilon<=I`. Its derived Delta is `(I-B_epsilon)/alpha`, rather than a silently unchanged target Delta.

## 5. C2 word transfer and full-price error, including global Z

For fixed control replacements with total error epsilon, twice differentiated telescoping gives

```text
||U_tilde,ij-U_ij|| <= epsilon(C_ij+B_i B_j),
C_ij=sum_l ||V_l,ij||.                               (5)
```

The double-derivative product sum is bounded by `B_i B_j`; derivatives of replaced constant slots are zero in both words. Moving code, pairing, preparation and detector maps have their own jets.
For positive contraction rounds B and B_tilde let their errors through order two be `delta_0,delta_i,delta_ij`, and let `L_i,L_ij` bound both models' round jets. With `S=B^m`, all products in the ordered power rule give

```text
e_0=||S_tilde-S|| <= m delta_0,
e_i <= m delta_i+m(m-1)L_i delta_0,
e_ij <= m delta_ij+m(m-1)(L_i delta_j+L_j delta_i+L_ij delta_0)
        +m(m-1)(m-2)L_i L_j delta_0.                 (6)
```

Write `eta_I=||S_tilde,I-S_I||_1<=d e_I`, `Z=Tr S`, and require `a_Z=eta_0/Z<=1/2`. For `H=log(CZ)/beta`, fixed calibration, define
`b_i=eta_i/Z`, `c_ij=eta_ij/Z`, `r_i=|Z_i|/Z`, `r_ij=|Z_ij|/Z`, and `d_i=2(b_i+a_Z r_i)`. Then

```text
|H_tilde-H| <= 2a_Z/beta,
|H_tilde,i-H_i| <= d_i/beta,
|H_tilde,ij-H_ij| <= [2(c_ij+a_Z r_ij)
                     +d_i r_j+d_j r_i+d_i d_j]/beta. (7)
```

Both normalizer derivatives are retained; operator approximation alone cannot replace (7). If C differs, add the actual `log(C_tilde/C)/beta` value and its derivatives.
For `J=-M Tr log F`, `F=(1-z)I+zS`, put `a_z=1-z>0`, `s_i=||S_i||_1`, `f_i=||S_i||`, `s_ij=||S_ij||_1`, and use tildes for analogous norms. The resolvent identity gives

```text
|J_tilde,i-J_i| <= Mz eta_i/a_z+Mz^2 e_0 s_i/a_z^2,
|J_tilde,ij-J_ij| <= Mz eta_ij/a_z+Mz^2 e_0 s_ij/a_z^2
 +Mz^2(eta_j f_tilde,i+f_j eta_i)/a_z^2
 +Mz^3 e_0(s_tilde,j+s_j) f_tilde,i/a_z^3.           (8)
```

This is a full-carrier noncommuting bound: use `||F_tilde^-1-F^-1||<=z e_0/a_z^2` and four-term telescoping of `Tr F^-1 S_j F^-1 S_i`. No prepared probability replaces the thermal trace.

For the v8 scaling `d=O(h^-4)`, `m=2n=Theta(h^-2)`, round jets through order two bounded independently of h and `delta_I=O(epsilon)`, (6) gives `eta_k=O(d m^(k+1) epsilon)`. Assume beta is bounded above and away from zero, `Z>=Z_min>0`, fixed bounded M and `z<=z_max<1`. If additionally `r_i,r_ij=O(1)`, then

```text
epsilon=o(h^12) => h^-2 C2 error of H+J tends to zero. (9)
```

For J this uses `f_i=O(m)`, `s_i=O(dm)`, `s_ij=O(dm^2)` in (8); no rank is discarded. Without the bounded normalized trace-jet premise, the coarse estimates `r_i=O(dm)`, `r_ij=O(dm^2)` instead give the sufficient schedule `epsilon=o(h^20)`. These are conservative sufficient schedules, not lower bounds, efficient runtime claims or consequences of a fixed finite-level tolerance. They assume one shared admitted field-dependent SELECT family; pointwise compilation is insufficient.

## 6. Preparation, calibration and code complements remain actual inputs

For `R=Tr rho Delta`, use `rho=Psi Psi^*/Tr(Psi^*Psi)` in the actual common orthonormal trivialization, with all 128 reference coordinates retained. The whitening/pairing jets belong in Psi and Delta; the displayed formula does not freeze them. For a multi-index I of order at most two, the exact product-rule error is bounded by

```text
sum_(J subset I) [||rho_tilde,J-rho_J||_1 ||Delta_(I\J)||
                +||rho_tilde,J||_1 ||Delta_tilde,(I\J)-Delta_(I\J)||]. (10)
```

The mixed subsets occur twice as required. Thus all normalization/preparation jets remain. At fixed calibration, identical preparation with bounded normalized jets and round `delta_I=O(epsilon)` gives `Delta`-jet error `O(epsilon/alpha)=O(epsilon h^-2)`; its h^-2 R-source error is `O(epsilon h^-4)`. Other prepared families require their actual errors in (10).
When calibration moves the total first source is instead

```text
dH=beta^-1 dlog C-H dlog beta+Tr(dS)/(beta Z),
dJ=(J/M)dM-M Tr F^-1[(S-I)dz+z dS],
dB=-alpha dDelta-Delta d alpha, beta=m alpha.         (11)
```

Here m is fixed integer record count during a smooth field variation. A changing integer depth is a refinement schedule, not automatically a differentiable clock field. Extra compiler garbage may change C and the action on code complements. A code-subspace isometry estimate does not determine their full heat price. A spectator constant has zero source only at fixed dimension and fixed beta; neither a free inverse preparation nor an identity heat completion is obtained by declaring a compiler.

The next admissible use is therefore narrow: choose the genuine native field-dependent operations, supply the actual seed/address/cut resources and full complementary action, then compile the constant control slots with (6)–(11). This closes a quantitative approximation premise for that same action. It does not select physical Cost−Info, the full history ensemble, observer law or the Einstein terminal.

## Input pins

SHA-256 of the actual bytes read; paths are repository-relative. These are source pins, not new execution receipts.

| Input | SHA-256 |
|---|---|
| `03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean` | `76c7082b4f600f7b178579b8a2a859d6f692c96ce5a769920fb3ff427532292c` |
| `03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean` | `6ea993e22c8b7d0b8a93b9537d51893cb4aff45af858d82ec7f9005ead96e2d7` |
| `02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py` | `7aead2716c7bf7899a134eedbf4b87dbe1ef9c85900189b5afc8cdfeed13f0f9` |
| `02_REGISTRY/research/A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md` | `f09c24bb7b8ef5f512555257dcd9a335571c052b452482d2c31a3b8e586efdc5` |
| `02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md` | `f7ea30d997a58fa4e608d4403acae5f5e3d7e5da45116f9a7c3f62be5e99115c` |
| `02_REGISTRY/research/A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md` | `482cf99f280620e7aa6120432cd7b9764671c5ef3fb1c0c3b50d7228d66e08b3` |
| v5 original text resource named in Section 1 | `a123c96233c62a1a05cc01b0a5be706ca4cff10765f781797b7859c4d50547e4` |
