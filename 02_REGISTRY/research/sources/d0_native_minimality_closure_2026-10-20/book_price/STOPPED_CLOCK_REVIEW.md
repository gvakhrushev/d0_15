# Independent analytic acceptance of the retained stopping-clock source

20 October 2026. Reviewer: `native_price_bridge`. Existing PR #334,
`native-programme-v1`, and
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.

This records the independent analytic review already completed and sent
to the author and parent. It changes no frozen scientific file and
records no new execution or replay.

## Frozen objects

Paths are relative to this packet's `prospective/` directory.

| Object | SHA256 |
| --- | --- |
| `STOPPED_CLOCK_SOURCE.md` | `75845813d20ecf7b585fb7b7a7bef8b8170a711e94a56bb0df0cc3546622a036` |
| `check_stopped_clock_source.py` | `bdab1158efc863a8d631c50ae7f30f7c3780df744e74441a88ed298bc059f0c9` |
| `RESULT.json` | `b226373c813903af983ac1f438c4b7d6485d81dda32f13f2225284d20d0ee35f` |
| `INPUTS.json` | `8de593a2da6afe859e86f5b42a212b53705dcf5ce3def77ae15c22c02c4ea733` |

I read the complete proof and independently checked the formulas and
scope below against the already read literal full128 paid-port owners.
I inspected the saved PASS67 receipt and verified its proof, checker and
input-manifest hash bindings. The checker hash identifies the author's
executed program; this review does not claim a separate execution or a
complete independent code audit. No historical suite, previous scalar
stopping calculation or Kraus replay was run.

## Checked mathematical content

1. **Exact retained process and actual price mark.** The orthogonal
   stopped prefixes in (3) have amplitudes `K_alpha B^j`, and their
   literal port prices are `j+1+b_alpha`. The unique blank has price1;
   every port1 leaf, including blank-label/port1, is a nonblank exit.
   Summing those effects gives
   `G_x=x(E-E1)+x^2 E1` and
   `F_cost,x=G_x(I-xQ)^(-1)` in (5)--(6). The simplification uses the
   aggregate effects as functions of Delta. It does not assume that
   individual terminal Kraus matrices commute.

2. **Complete first source and finite cap.** Equation (7) retains both
   differentiated factors and the ordered resolvent insertion. Its
   clock-calibration and preparation derivatives in (7)--(8) are
   explicit. The complete finite-cap transform in (10) includes the
   unresolved branch, so its value at x=1 is I. The tail estimates
   follow from `0<=F_cost,x<=xI`, `0<=Q<=I`, and the ordered derivative
   of `(xQ)^N`. They are asserted for fixed x<1, not uniformly at the
   unmarked boundary or a closing spectral gap.

3. **Clock inverse without a commuting-source shortcut.** The identity
   `F_clock,s=I-(1-s)(I-sQ)^(-1)` proves (12)--(14), including
   `dF=-s(1-s)R_s(dQ)R_s` at fixed s. This map is invertible on the
   full Hermitian tangent space. The actual native window `B>=p^3 I`
   makes the subsequent Sylvester inverse for dB valid. Recovery is
   from the full operator-valued statistic, not from one prepared
   scalar expectation or an uncharged tomography operation.

4. **Moving kernel and the unlimited boundary.** At fixed finite
   carrier, the eventual-exit effect is P_plus. The full determinant
   therefore has constant field value at fixed rank and fixed z even
   when the projector moves. Its prepared contraction need not have
   zero source. In (18), a horizontal frame carrying P0 contributes
   at most `2||dP0|| q_*^N`; differentiating the positive-support power
   contributes at most
   `N q_*^(N-1)||P_plus(dQ)P_plus||`. The proof does not identify this
   fixed-horizon-to-infinity limit with the finite-beta refinement.

5. **Whole paid moment and dark mass.** Differentiating the complete
   finite-cap transform yields (19), hence
   `C_stop,N=N P0+C_plus(I-Q^N)`. In contrast, the derivative of the
   finite-exit transform alone is C_plus. The actual unlimited price
   is infinite whenever the input has positive dark mass. The text
   keeps this distinction and the source of `N P0`. The Moore--Penrose
   derivative in (21) has both support/kernel off-diagonal terms with
   the correct signs. A finite source using C_plus is restricted to
   an entire prepared family that remains in the positive support.

6. **Prospective attainment boundary.** The pathwise inequality (22)
   proves earliest reporting minimizes the known port cost among
   policies that continue the same native rounds and cannot certify
   the same first-event-or-cap task earlier. It does not minimize an
   unspecified full Cost-Info objective, prove that this task is
   compulsory, or provide primitive controlled-halt implementation.

## Acceptance

**PASS: no mathematical blocker found within the stated scope.** The
new stopped-record transform preserves the original complete outcomes
and oldRIGHT components, recovers the blank spectrum and its full first
jet before the unmarked limit, and derives the actual known port-cost
operator. A supplied closed-record ensemble can consume it without
inventing a replacement clock law.

Full Book Info, complete controller/preparation/work valuation, physical
halting admission, mandatory task selection, global prospective minimum
attainment and the all40 GR source identity remain unproved. The receipt
itself states those limits. Its PASS67 result is the author's targeted
exact execution; this independent acceptance is analytical and involves
no repeated checker or historical-suite run.
