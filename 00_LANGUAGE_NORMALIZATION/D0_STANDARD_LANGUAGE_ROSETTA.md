# D0 Standard-Language Rosetta Stone

This file normalizes D0 internal terminology into language already used by mathematicians and physicists. The rule is: standard object first; D0 mnemonic second.

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
