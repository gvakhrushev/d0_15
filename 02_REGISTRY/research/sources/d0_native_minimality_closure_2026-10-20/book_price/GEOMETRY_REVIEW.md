# Independent analytic acceptance of the native first-source transport

20 October 2026. Reviewer: `native_price_bridge`. Existing PR #334 and
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`; no new task, action,
controller, information binding or physical-closure claim.

## Frozen objects actually inspected

Paths are relative to this packet's `geometry/` directory.

| Object | SHA256 |
| --- | --- |
| `source_moment_collapse.md` | `9bfb61897324d438bff3458209f3fda321b2876af41b6178b96fdf04490773c4` |
| `check_source_moment_collapse.py` | `fd4edf0649492910eecf649fb1c133dafd2eb1b3d4b8df801a6e62a0f30691b8` |
| `SOURCE_MOMENT_RESULT.json` | `283d3f92890644469482f1f4de0c9885d380e9dff2ef8825fea40796400f7c08` |

I read the complete proof and checker, inspected the saved PASS251 result,
and independently checked the algebra below against the cited original
paired-Julia channel and physical-coframe HJR owners. I did not execute
this checker again and did not run an earlier certificate or suite.
PASS251 is the author's recorded execution; the acceptance here is an
independent analytic and implementation-scope review.

## Analytic checks

1. **Moving Stinespring source.** The two base moments imply
   `Delta_out V=V Delta`. With `A=V* dot V`, differentiating the actual
   isometry gives the necessary term `[f(Delta),A]`. The polynomial
   identity `Df_Delta[[Delta,A]]=[f(Delta),A]` then proves (2) for
   arbitrary ambient jets, including the Kraus jet. It does not assume
   that a value equality persists transversely to its equality stratum.
   The finite defect recurrence gives the sign and ordered insertions
   in (3); subunitality and the fixed native clock give (4).

2. **Actual complete Fourier trace.** At the homogeneous base, every
   undifferentiated Kraus matrix preserves momentum. Consequently the
   `kk` block of `(dot T*)(Delta)` is exactly
   `lambda_k (dot T*)(I)_kk=0`, even for spatially varying tangents.
   The literal paired-Julia sum, containing both adjoint orientations
   and both square-root defects, supplies bistochasticity. Mere Kraus
   completeness would not suffice. These facts give the full CAR16
   block trace cancellation and the all-depth scalar first-source
   statements (5)--(7), including the complete Riesz128 density.
   A moving preparation contributes zero to the difference because
   the undifferentiated operator difference is zero, not because its
   tangent is omitted.

3. **Finite controller and actual paid-port consumer.** Replacing the
   ideal acceptance by the actual field-independent finite-cap
   acceptance changes the matching factor to `B_*`. The text correctly
   retains the separate comparison error with the original `B`, and
   does not discard controller records or payment. For the original
   unthinned process, the cancellation
   `[(dot Phi*)(Delta)]_kk=0` and block trace preservation prove (7a):
   `d Cost_port,n=p beta dR` on the complete flat ambient chart. Both
   explicit field derivatives and the preparation term are retained.
   Other price components and Info are not identified by this equation.

4. **Operator distinction and physical scaling.** Summing the exact
   recurrence on the permitted `Omega_23` tangent gives (9), including
   its sign. The strictly positive limit (10) requires fixed `nu`.
   On the separate primary carrier `nu_h=h nu`, the same finite formula
   instead has `lambda=O(h^2)`, `s=O(h^2)` and `dot Delta=O(h^2)` at
   fixed physical momentum, hence `dot K_m=O(h^6)`; the stated uniform
   lattice bound is `O(h^3)`. Neither bound licenses summing an
   unnormalized `O(h^-4)` mode count. The exact trace cancellation does.
   Thus scalar/Riesz equality is not falsely promoted to operator
   equality or to a failure of the differently scaled primary carrier.

5. **Observer source on the same physical coframe.** The null-basis
   positive pairing differentiates to the stated negative `sqrt(2)`
   cross entries. Even Fourier averaging removes the sine terms and
   leaves `-2 sqrt(2) A(theta)`. Combining this with the original full
   `128*16=2048` feedback multiplicity gives the negative coefficient
   `-4096 sqrt(2) z beta` in (12). The full Riesz first-shell source is
   zero and the normalized heat source is bounded, so the extensive
   feedback source survives. This is a source of the specified bare
   HJR candidate, not of an already derived complete physical price.

## Accepted boundary

**PASS: no mathematical blocker found within the stated scope.** The new
result closes the first-source comparison for the actual flat full trace,
feedback and complete-Riesz contractions, and derives the original paid
port contribution `p beta dR` there. It does not prove full Book Info,
complete work/preparation price, primitive admission, an attained
physical minimum, a metric-only quotient, local second-order field
dynamics, or all40 source identity on the curved target. The observer
counter-source and operator example respect those boundaries. The
finite acceptance and refinement limits are not interchanged.
