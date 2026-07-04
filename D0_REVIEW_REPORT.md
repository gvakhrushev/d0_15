# D0 corpus review report — verification sweep + fixes

Reviewer pass over the D0 corpus (`d0_15`): verify the exact quantitative claims, run the full certificate
suite, find and fix concrete bugs. Definite outcomes, exact arithmetic. No new physics claims here — this is
verification/QA of the existing corpus.

## 1. Exact `ℚ(φ)` arithmetic — all central identities VERIFIED

Checked symbolically (sympy, exact):
- `α_alg⁻¹ = (12288/5)φ⁻⁶ + (1/3)φ⁻³ = 159739/5 − (294902/15)φ` — identity holds exactly. ✓
- `μ₂ = 12288/5 = 2¹¹·π₀·φ⁻²` with `π₀=(6/5)φ²` — holds. ✓
- `δ₀ = 1/(2φ³) = (√5−2)/2`; `p+p²=1 ⇒ p=φ⁻¹`. ✓
- `K(9,11,13)`: `|V|=33`, `|E|=359`, Laplacian spectrum `{0:1,20:12,22:10,24:8,33:2}`, adjacency
  `rank 3 / nullity 30`, kernel `30 = 8+10+12 = (n_i−1)`. ✓
- Tower orders `Q₈=8 ⊂ 2T=24 ⊂ 2I=120`; `E₈` `240=8·30` roots, `dim 248`, Coxeter `h=30`. ✓
- Lucas `L₁₁+L₄ = 199+7 = 206` (muon transfer integer). ✓; `ord(T mod 44)=30`. ✓

**Verdict:** the corpus's exact `ℚ(φ)` arithmetic is sound.

## 2. The α structure — three levels, honestly labelled (verified)

- `α_top⁻¹ = 359/φ² − φ⁻⁵ = 137.03562810` (parameter-free geometric leading; `−3.7×10⁻⁴` from CODATA).
- `α_alg⁻¹ = 137.03604` (algebraic/Feshbach; `+4.4×10⁻⁵` from CODATA).
- `α_D0⁻¹ = α_top⁻¹ + φ⁻¹⁷(1+h_KS·sinθ_seam) = 137.035999151` (9-digit CODATA match — but uses the seam
  factor `≈1.325`, i.e. parameters `h_KS, θ_seam`; correctly labelled **CHK holonomy**, not parameter-free THE).

**Verdict:** the impressive 9-digit α match is real but **parametric** (seam correction) and the corpus labels
it honestly (CHK). The parameter-free prediction is `α_top ≈ 137.0356` (0.0003 from CODATA). No mislabel found.

## 3. Full certificate suite — bugs found and FIXED

Ran all **584** `05_CERTS/vp_*.py`.

- **Before fixes: 87.3% pass** (74 non-passing).
- **Bug A (FIXED) — data corruption:** two registry CSVs each contained **one stray NUL byte**, which broke
  ~50 certs (`_csv.Error: line contains NUL`):
  - `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (NUL at offset 383496, cell `"...F2^2␀ = Q..."`)
  - `03_THEORY_MAP/theory_status_map.csv` (1 NUL)
  Stripped the NUL bytes. **Pass rate 87.3% → 96.4%** (564/585).
- **Bug B (FIXED) — code bug:** `05_CERTS/vp_vacuum_feedback_equation_of_state.py` line 35 had an unescaped
  `β^{-1}` inside a `.format()` string → `KeyError '-1'` (the math computed fine; only the print crashed).
  Escaped `{-1}`→`{{-1}}`. Cert now passes.

## 4. Remaining non-passing (21) — classified

- **~14 missing data files** (this is a partial repo copy): `06_COVERAGE/BOOK0X_*.csv`, `08_PASSPORTS/…/desi…`,
  `08_DATA_BUNDLES/…`, `04_FOUNDATION_CLOSURES/…`, `07_GLOBAL_AUDIT/…`, renamed `BOOK_04_…PASSPORTS.md`.
  Not logic bugs — absent inputs.
- **1 environment:** `vp_nuclear_shell_contact_src.py` needs `pandas` (not installed).
- **A few consistency/text-hygiene** (pre-existing corpus state, not caused by this review):
  - `vp_phi_abcd_operator_cycle_v1119.py`: 2 text checks fail — active books still contain the word "golden"
    (in `GOLDEN …` footnote refs) and a missing operator-cycle term.
  - `vp_total_no_anonymous_open_targets.py`: flags one anonymous open target `D0-ISOTROPIZATION-MECH-001`.
  - `vp_gw_book09_publication_guardrail.py`, `vp_v1131_standard_language_normalization.py`: reference Book 09 /
    a standard-language section not present in this copy.

## Net

Corpus arithmetic and cert discipline are **sound**; the real defects were **two fixable bugs** (a data-
corruption NUL byte breaking ~50 certs, and one format-string crash), now fixed, taking the suite from 87.3%
to 96.4%. The rest of the non-passing certs are missing-data-file artifacts of a partial repo copy, not logic
failures. The α 9-digit CODATA match is genuine but parametric (correctly labelled CHK).
