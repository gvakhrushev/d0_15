# D0 Source-Native Lepton Green Closure — decision procedure

$$
\mathcal H_N \;\xrightarrow{\text{ABCD/Q}_8}\; \Omega_8\simeq Q_8 \;\xrightarrow{\;\iota_{\rm term}\;}\; \mathbb C^{V_9}\subset\mathbb C^{V(K)} \;\xrightarrow{\;\Gamma\;}\; \mathbb C^{E(K)} \;\to\; \mathcal H_{\rm term} \;\xrightarrow{\;U_{\rm eff}\;}\; \mathcal H_{\rm term} \;\xrightarrow{V_\ell}\; \mathcal H_{\rm term}\otimes\overline{\mathcal H_{\rm term}}
$$

> ## Decision: **OUTCOME-B**
> The frozen D0 source **does not** contain a source-native terminal Green theorem with a *unique* branch→row
> map. It **does** prove an exact two-completion **NO-GO** — the branch→generation row is underdetermined by
> the frozen Green-resolvent data — and names **exactly one** minimal missing operator,
> `PRIM-LEPTON-BRANCH-FIXING-OPERATOR` ( = `ℬ_row`). This document supplies the rigorous minimal-extension
> theorem (necessity + sufficiency + deletion-minimality) the corpus was missing.

Outcome **A** is firmly excluded: the only finite Green resolvent owner (`LeptonFiniteGreenResolventOwner`)
defines `Ueff` as a **hand-typed 7×7 literal** proved only at `z=0`; its `det(I−zU)=(1−z⁴)(1−z³)` factorization
is prose, and there is no branch-row uniqueness theorem. Per §0 a hand-built terminal matrix does not count as
a source-native closure. **Firewall:** `ℬ_row` introduces no numerical mass input; the decimal/mass map stays
an EFT/IR passport. No lepton masses, SM charges, redshift, or EOS are claimed.

## 1. Frozen source inventory

See `D0_LEPTON_SOURCE_MANIFEST.json` (literal paths + sha256 + status). Five distinct carriers are kept
disjoint (no morphism assumed without an explicit code map): `Ω₈` (8 role points), `ℂ^{V₉}` (vertices),
`ℂ^{E(K)}` (359 edges), `ℋ_N` (shell stages), and the 7-point shell-torus monodromy carrier.

## 2. Condensed ABCD → Q₈ (source-native)

`D0.Core.DyadABCD` defines `Role = Fin2×Fin2` (4 points A,B,C,D) and `Ω₈ = Role×Bool` (8 points), with
`|Role|=4`, `|Ω₈|=8`. `D0.Claims.VietaGaloisAbcd` shows A,B,C,D are the Vieta/Galois data of `x²−x−1`
(`φ+ψ=1`, `φψ=−1`, `φ²=φ+1`, `ψ²=ψ+1`, Galois swap `φ↦1−φ`). `D0.Claims.Q8DedekindMinimality` forces the role
group to be `Q₈` (the unique Hamiltonian group of order ≤8: `[Q₈,Q₈]=Z(Q₈)=Φ(Q₈)={±1}`) — *§0 caveat: its
group tables are hand-built; cited as a finite-catalog cert.*

## 3. Terminal-to-scene embedding

The embedding `ι_term: Ω₈ → V₉` is not the locus of the obstruction (its ambiguity is absorbed by the
`Aut_source` quotient); the live obstruction is downstream, in the carrier completion (§5, §10).

## 4. Incidence-derived edge carrier

`ℋ_E = ℓ²(E(K(9,11,13)))`, `dim 359`. Star lifts `Γ_{9,m}|q⟩ = m^{-1/2}Σ_{v∈V_m}|ι(q),v⟩` are isometries with
orthogonal images (verified numerically in the v15 unified-spine certs on the real 359-edge graph). The
induced isotypic ranks are `(1,3,4)` per side — forced, not posited.

## 5. Source-admissible return operators — cycle type forced, completion not

The shell-torus monodromy `U_eff` on 7 points has order 12. Among the **15 partitions of 7, the cycle type
`[4,3]` is the UNIQUE one of order 12** (`return_orders_forced`, by `decide`). So the **return orders `(4,3)`
are source-forced** and `det(I−zU_eff)=(1−z⁴)(1−z³)` is the only order-12 possibility. But the *placement* of
the cycle type on the carrier is free: `σ_A=(0123)(456)` and `σ_B=(012)(3456)` are both order 12 with the same
cycle type (hence the same resolvent invariants) yet distinct (`LeptonBranchAssignmentNoGo`). The resolvent
**cannot** separate them.

## 6–8. P/Q/U, feedback, Feshbach

Cited from the existing tick/Feshbach owners (`FeshbachSchurTimeDelayOwner`, the v15 `Feshbach` factorization).
The Feshbach reduction `det(I−zU)=det(I−zD)det(I−zW_eff)` is established at the algebraic-identity level; it does
not by itself separate `σ_A` from `σ_B` (both share `D`-spectrum and resolvent).

## 9–10. Green kernel, exhaustive branch-row test, and the no-go

The rank→exponent row is forced: of the `3!=6` assignments `(E₀,E₄,E₃)↔(e,μ,τ)`, **exactly one** respects the
orbit-size↔exponent constraint `(1↔0, 4↔1/4, 3↔1/3)` (`exhaustive_row_test`). But the carrier completion
remains 2-fold (`σ_A`/`σ_B`), so the *full physical* branch→generation map is underdetermined — a two-completion
NO-GO.

## 11. Fibonacci / Pisot

The φ-replication recurrence and Pisot tail are established in `D0.UnifiedFiniteCore.PhiReplication`
(`A_{n+1}−φA_n=ψⁿA_1`, `|ψ|<1`), to be applied only as an internal normalized branch amplitude — never fit to a
mass.

## 12. Minimal-extension theorem — `ℬ_row`

`D0.LeptonClosure.BranchRowMinimalExtension.branch_row_minimal_extension` proves, by `decide`:

- **Necessity** — `≥2` admissible completions (`σ_A≠σ_B`) share every resolvent invariant.
- **Sufficiency** — imposing `ℬ_row` collapses the admissible completions to **exactly one**.
- **Deletion-minimality** — removing `ℬ_row` restores `≥2`.

### `ℬ_row` specification (the one minimal missing operator)

| field | value |
|---|---|
| **domain** | the 7-point shell-torus carrier (`Fin 7`), partitioned by `U_eff=blockdiag(P₄,P₃)` into a 4-orbit and a 3-orbit |
| **codomain** | the 3 generations `{e,μ,τ}` with exponent row `(0,1/4,1/3)` |
| **covariance** | `U_eff`-equivariant; breaks the `S₇`-conjugacy carrying `σ_A↦σ_B` (non-narrowing — not `Cent(U_eff)`) |
| **spectrum** | compatible with `det(I−zU_eff)=(1−z⁴)(1−z³)`: 4th roots (capacity block) ⊕ 3rd roots (rank block) |
| **action** | orbit→exponent (`4-orbit↦1/4↦μ`, `3-orbit↦1/3↦τ`, fixed/unramified↦`0`↦`e`), picking exactly one of `σ_A`,`σ_B` |
| **separates** | the size-4 orbit `{0,1,2,3}` from the size-3 orbit `{4,5,6}` **and** the two equal-order-12 completions `σ_A`,`σ_B` |

Concretely `ℬ_row(σ) = [\,0 \in \text{size-4 orbit of }σ\,]` separates `σ_A` (true) from `σ_B` (false) — the exact
information the resolvent omits.

## Reproducibility

```sh
# from 09_LEAN_FORMALIZATION
lake build D0.LeptonClosure.BranchRowMinimalExtension
# certificate (source-native, builds permutations not matrices; can fail)
python 05_CERTS/d0_branch_row_minimal_extension_verify.py
# manifest
python tools/gen_lepton_source_manifest.py
```
