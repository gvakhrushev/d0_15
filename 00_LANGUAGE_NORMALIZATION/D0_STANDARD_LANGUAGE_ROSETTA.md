# D0 Standard-Language Rosetta Stone

This file normalizes D0 internal terminology into language already used by mathematicians and physicists. The rule is: standard object first; D0 mnemonic second.

## ⚠ Collision warnings (read first)

Three D0 tokens look like established terms that mean something else. They are **not** those things:

| D0 token | What it means here | NOT to be confused with |
|---|---|---|
| **forcing** / "(forced)" | proof by contradiction (reductio ad absurdum) against the admissibility axiom **M1** | **Cohen forcing** (set theory / generic extensions) — unrelated |
| **LEM** (as a *status* word, "still LEM, not THE") | a result whose mechanism is established but a *limit / external-mechanism* step remains (a conditional result); written **`MECH-LIMIT`** going forward | the **Law of Excluded Middle** (logic) — unrelated. NOTE: `LEM` in the `DEF/LEM/THE` taxonomy *does* mean **Lemma** (standard, correct). |
| **THE** (as a *status* word / `[THE n.n]`) | **Theorem** (proved by reductio against M1) | the English article "the" |

The proof technique behind "forcing" is **standard proof by contradiction** — see BOOK_00 §00.8. The only D0-specific ingredient is the axiom **M1** (no obligatory external catalogue). The theory is not made harder by this vocabulary; the content is in M1 and in the finite objects, not in the proof method.

| D0 term | Preferred external term | Formal object / notation | Rule |
|---|---|---|---|
| `finite distinguishable registration` | finite measurement record / finite observable event | `finite quotient S_N, event projector Pi_a` | May be used after identifying the finite event algebra. |
| `D0-admissible observable` | admissible subfunctor of continuous test maps | `Obs^{D0}(S) ⊂ Obs(S), finite-stage factorization` | Use before any physical observable claim. |
| `archive complement / archive sector` | traced-out complement, environment, unresolved orthogonal complement | `H_total = H_obs ⊕ H_traced; conditional expectation or partial trace` | Use D0 word only after standard traced-out-complement phrase. |
| `active sector` | retained observable algebra / measured subsystem | `A_obs ⊂ B(H_N), retained sigma-algebra` | Use as synonym after algebra is specified. |
| `forgetting map` | coarse-graining, conditional expectation, partial trace, Wilsonian RG map | `E_N: A_{N+1}->A_N, Tr_env, Delta(rho)=sum Pi_a rho Pi_a` | Use standard term first; D0 term in parentheses. |
| `archive pressure` | effective source term from traced-out degrees of freedom | `P_archive, response-pressure kernel, stress/likelihood driver` | Never introduce as metaphor; specify operator and observable window. |
| `readout` | POVM/instrument outcome, positive trace functional | `R_a=D_a† D_a, P(a)=Tr(rho R_a)/Tr(rho sum R_b)` | Use readout only after positive operator is shown. |
| `terminal readout` | absorbing / terminal measurement channel | `rank-reducing CP instrument or quotient q:S_N->A` | Use in measurement context only. |
| `terminal-destructive readout` | rank-reducing absorptive channel / inelastic projection | `M_dest; Tr_HS(M_dest†M_dest)` | Must include operator and cost if numerical. |
| `witness` | marked basepoint / gauge-fixing section | `omega_0, chosen section of quotient` | Do not treat as mystical observer. |
| `tick` | discrete evolution endomorphism / time-step operator | `T_tick or U_N:N->N+1` | Use when finite ordered dynamics is meant. |
| `scene` | finite incidence complex / support complex | `K(9,11,13), clique complex, cochain complex` | Use external term first in formal sections. |
| `carrier` | representation space / carrier algebra / bundle of representations | `H_i, Lie algebra representation, cochain shell` | Specify representation and action. |
| `single-section` | single scale-section / no additional renormalization anchor | `Lambda_act section; one dimensionalization map` | Use for anti-parameter discipline. |
| `passport` | external comparison protocol / empirical comparison functor | `bare object -> bridge -> observable table` | Use for external validation only, not proof. |
| `bridge` | functor, coupling kernel, EFT matching map, continuum limit | `B: internal finite object -> external model object` | Must provide kernel/scheme/data when promoted. |
| `stiffness` | structural rigidity / log-sensitivity / hostile uniqueness | `d log O / d theta, negative controls` | Use to state uniqueness and failure tests. |
| `ambient-Hom leakage` | uncontrolled enlargement of morphism class | `Hom outside Obs^{D0}; non-admissible continuum map` | Use as formal violation of admissibility. |
| `ABCD` | four-role finite instrument / terminal role algebra | `A_Sigma, B_N, C_+, D_- or two-port outcomes` | Do not present as merely symbolic alphabet. |
| `Omega8` | signed four-role instrument extension | `ABCD x {+,-}` | Use after ABCD instrument is defined. |

### Proof and status vocabulary

| D0 term | Preferred external term | Formal object / notation | Rule |
|---|---|---|---|
| `forcing` / `forcing-by-contradiction` / "(forced)" | proof by contradiction (reductio ad absurdum) against the admissibility axiom M1 | DEF-0.2.2 5-step schema; `assume ¬X ⇒ exogenous θ ⇒ ⊥M1 ⇒ X` | Say "forced (reductio against M1)" on first use. ⚠ NOT Cohen forcing. |
| `M1` | admissibility axiom: no obligatory external catalogue / no hidden exogenous parameter | `M1` (BOOK_00 §00.2, §00.8); kin to MDL / Kolmogorov but stronger (distinguishability-affecting) | Genuinely D0-specific. Keep the name; cite §00.2 as definition. |
| `⊥M1` / "violates M1" | contradicts the admissibility axiom (the contradiction that closes the reductio) | `θ exogenous ⇒ ⊥M1` | Use as the contradiction step of a reductio. |
| `exogenous parameter` (DEF 0.3.1) | external/hidden parameter | 3-clause: (1) not derived, (2) affects distinguishable outcomes, (3) not protocol-inevitable | Use the 3-clause form; looser than but related to hidden-variable / fine-tuning. |
| `DEF / LEM / THE` (taxonomy) | Definition / **Lemma** / Theorem | standard proof-object labels | `LEM` here = **Lemma** (standard). Keep. Distinct from the status word below. |
| `MECH-LIMIT` (was status `LEM`) | mechanism established; a limit / external-mechanism step remains (conditional result) | a claim below THE with a named limit/external gap | Replaces the status word "LEM". ⚠ the status word is NOT the Law of Excluded Middle. |
| `THE` (status / `[THE n.n]`) | Theorem (proved by reductio against M1) | proved claim | Keep; gloss on first use. ⚠ reads like the article "the". |
| `CHK` (status) | finite / computational check (verified, selection-owner may be open) | executable certificate result | Use for cert-verified-but-not-yet-THE. |
| `HYP` (status) | hypothesis / conjecture (open) | unproved statement | Honest open label. |
| `FORCING` (status) | forced-by-M1 (proved by reductio against M1) | release-status note | Display as "forced-by-M1". ⚠ NOT Cohen forcing. |
| `scene incidence` | incidence matrix of `K(9,11,13)` | `A`, `rank A=3`, `nullity A=30` | Use the matrix; "scene" = the complete tripartite graph. |
| `δ₀` (detector quantum) | the forced D0 constant `(√5−2)/2 = 1/(2φ³)` | `δ₀ = φ⁻¹ − ½` | Genuinely D0-specific. Keep; define as the norm-distance of the two cuts of unity. |
| `F_N` (feedback return) | residual non-unitarity of the retained sector after tracing the complement | `F_N = P_N U_N† Q_N U_N P_N` | Genuinely D0-specific operator. Keep; state operator. |
| `phason` | gapless quasicrystal mode / K₀ gap-label degree of freedom | gap-labelling group / `K₀` class | Standard condensed-matter / operator-K-theory term. |


### Additional dynamics / physics-front terms (Iter-22 completion)

| D0 term | Preferred external term | Formal object / notation | Rule |
|---|---|---|---|
| `golden tick` | discrete Floquet step / one period of the discrete evolution | `U_N : N -> N+1`, one Floquet period | Use "discrete Floquet step"; D0 mnemonic in parentheses. |
| `toral time` | modular (Tomita–Takesaki) flow / toral-automorphism time | `T=[[0,1],[1,-1]]`, hyperbolic toral automorphism | Use the automorphism / modular-flow term; "toral time" second. |
| `feedback-return operator` | Feshbach return / Schur-complement feedback operator | `F_N = P_N U_N† Q_N U_N P_N` (Schur complement of the traced block) | State as a Schur-complement / Feshbach map; keep `F_N`. |
| `finite detector` | finite measurement instrument | finite POVM / instrument `{R_a}` on the finite state space | Use "finite measurement instrument"; D0 word second. |
| `retained/archive split` | system/environment split | `H_total = H_obs ⊕ H_traced`, partial trace over the environment | Use "system/environment split"; the active/archive synonyms are defined above. |
| `archive` (dark kernel) | traced-out environment bath / nullity sector | `ker A`, `nullity = 30 = 8⊕10⊕12` for `K(9,11,13)` | "Traced-out environment"; keep `archive` for the specific nullity-30 sector. |

## Publication rule

A paragraph is publication-ready only if a reader can replace every D0-local term by its standard object without changing the theorem.

Examples:

- `archive` -> `traced-out complement (D0: archive)`;
- `forgetting` -> `conditional expectation / coarse-graining map (D0: forgetting)`;
- `passport` -> `external comparison protocol`;
- `carrier` -> `representation carrier or compact Lie carrier algebra`;
- `terminal destructive readout` -> `rank-reducing absorptive measurement channel` with its operator.

## Forbidden style

```text
archive pressure explains X
carrier gives Y
passport confirms Z
terminal readout removes N
```

Required rewrite:

```text
operator/source P_archive acts on finite response window W and induces observable X;
representation carrier g acts on cochain shell H_i and yields Y;
external comparison protocol maps bare D0 object O to measured quantity Z under stated bridge B;
rank-reducing absorptive channel M_dest has Hilbert-Schmidt cost N.
```
