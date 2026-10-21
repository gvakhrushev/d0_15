# Existing restricted field-to-CAR execution

This packet records a pre-existing native field-dependent CAR transition in
the repository, then states exactly how far it composes with the new cap-one
CQ analysis. Its five source files are pinned as present at the common input
commit in `SOURCE_PINS.json`; the original certificate is cited as evidence,
not rerun here. The certificate itself records its own source head
`f1270f63cffa5fcfc27b469ff2517d8398d5362a`, distinct from the 92c00ccb
composition snapshot.

On the open timelike sector of the full 16-real-component exterior matter
field $m$, let $q$ be the Lorentz metric and $v=P_1m$, with
\[
k=v^Tq^{-1}v>0,\qquad n=v/\sqrt{k},\qquad
Q=-q+2vv^T/k,\qquad G=Q^{-1}.
\]
In its $Q$-orthonormal frame let $c_n$ be the exterior creator along $n$,
$b_n=c_n^\dagger$, $N=c_nb_n$, and let $H$ project onto spatial exterior
degree at least two. With $a^2=p$ and $p+p^2=1$, the native gate and retained
readout are
\[
U_n=a[(I-H)+H(I-2N)]+p[(I-H)(c_n-b_n)-H(c_n+b_n)],\qquad
P_n=I-N.
\]
The same-history state update is $m_+=U_nm$. The complete two-step chronology
keeps this original readout: $K=U_{n_+}U_n$,
$F=P_nK^\dagger(I-P_n)KP_n$, and
$J=-\log\det(I_{16}-zF)$ for $0<z<1$. Under the
explicit whole-pairing endpoint-isometry premise, put \(w=(m_+)^1\). When
\(w\ne0\), the next metric is uniquely
\[
q_+=-Q+2ww^T/(w^TGw).
\]
The differentiated transition retains all ten initial metric and all
sixteen matter coordinates; its moving CAR-frame jet includes
\(\dot U_n=[\rho_*(A),U_n]\). The paired chronology owner also differentiates
the actual second gate and its full chronological price. These are concrete
field-to-operation-to-record equations on this restricted \((q,m)\) domain.

The certificate states `physical_admission: false` and
`complete_H_J_R_closed: false`. Endpoint isometry is a premise, not a proved
physical admission law; the transition is singular when \(w=0\). The separate
field-to-instrument first-jet result proves a genuine field-tangent witness
but leaves the map from the constrained field tangent to the return Lie
algebras underdetermined; its receipt also says physical admission is false.

This restricted CAR transition is not yet the cap-N=1 eight-dimensional
\(U(E,b)\) query/report instrument used by the CQ source theorem. No owned
intertwiner has been supplied from the 42 coframe/link/matter directions of
that theorem to this 26-coordinate \((q,m)\) chart and then to its full
two-query report effects, record charges, clock and Book03 Info. Thus these
results supply a real partial field-to-operation arrow, but not the single
common physical execution required for closure.

One actual price test remains visible in the chronology owner. On its named
congruently transported factor path, the factor-imbalance derivative is
\(\dot J=0\), while the heat-plus-feedback derivative is
\[
\frac{d}{dt}\left[\beta^{-1}\log\operatorname{Tr}e^{-\beta\Delta_{Q_t}}+J_t\right]
=2(E_1-E_2)>10^{-4}\qquad(L\ge2).
\]
For that candidate, a stationary \(H+J+R\) price therefore requires the
same admitted process to derive \(\dot R=-2(E_1-E_2)\). This is a
candidate-specific residual; it neither proves a universal obstruction nor
identifies this chronological price with the cap-one Book03 valuation.

## Exact observer-pairing identity for the moving-solder control

The moving-solder control in [`NATIVE_FIELD_WRITER_BRIDGE.md`](../../d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_FIELD_WRITER_BRIDGE.md) is exactly the existing native observer pairing on one explicit timelike branch. Let its solder be `F_H = sqrt(kappa) e_H^-1 T^-1`, so `q_H = F_H eta_rest F_H^T` and `Q_H = F_H F_H^T`. Choose a fixed rest-aligned initial matter vector with first grade `c e_0`, `c != 0`, and set `m_H = rho(F_H) psi_0`. Then `v_H = P_1 m_H = c F_H e_0` and `k_H = v_H^T q_H^-1 v_H = c^2`. The observer owner’s definition gives

```text
Q(q_H,m_H) = -q_H + 2 v_H v_H^T/k_H
            = F_H(-eta_rest + 2 e_0 e_0^T)F_H^T
            = F_H F_H^T = Q_H.
```

Thus `Q_H` is not an arbitrary positive pairing on this chart. But the
existing whole-operator endpoint-isometry transition implies `Q_+ = Q`.
The exact moving-solder step `H -> H + eps chi` has
`(Q_{H+eps chi}-Q_H)_{01} = -kappa eps chi/4`, nonzero whenever the step is
nonzero. Therefore this rest-aligned moving-solder path cannot be produced by
that same endpoint-isometric CAR transition. This is a scoped incompatibility:
the chosen chart is timelike and is not identified with the primary null CAR
matter source. It neither excludes other observer inputs or transitions nor
proves physical admission. A viable route must derive the actual moving-pairing
transition and its full price, or identify a different admitted matter branch.

Replay: `python3 check_moving_solder_observer_binding.py`; its exact symbolic
receipt is `MOVING_SOLDER_OBSERVER_BINDING_RESULT.json`.

## Pinned owners

- `A4D_NATIVE_FIELD_TO_INSTRUMENT_JET_BOUNDARY.md` and its exact checker
  receipt: classification of the instrument first-jet family and its
  response-visible physical field tangent.
- `A4D_NATIVE_MATTER_OBSERVER_PAIRING.md` and
  `A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md`: full-matter pairing, conditional
  metric update, all-slot differential, moving CAR gate and chronological
  price source.
- `NATIVE_FIELD_WRITER_BRIDGE.md`: the pinned moving-solder control and the
  endpoint-isometry implication used in the scoped incompatibility above.
- `check_moving_solder_observer_binding.py`: exact algebraic replay for the
  rest-aligned timelike branch only.
- `a4d_native_field_instrument_jet_check.py` and
  `a4d_native_field_instrument_jet_results.json`: the original bounded exact
  certificate and its recorded admission boundary.

