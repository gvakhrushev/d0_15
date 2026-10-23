# Direct full-stencil plaquette C2 result

Replay:

```sh
python3 02_REGISTRY/research/sources/d0_opposite_null_julia_order_memory_2026-10-19/check_direct_plaquette_full_c2.py
```

The checker evaluates all original based faces affected by the marked links
on a periodic (L=3) four-dimensional stencil. Its candidate price is the
complete per-face (T(P)=P/2) Julia success/failure instrument with the 13
positive Choi/POVM effects retained; the face-assigned negative pointer is
Golden-refined, with all unselected pointer labels and Julia failures kept.
This is a specified mathematical price candidate, not a selected native D0
program.

For each of the six one-link face/generator assignments, the exact geometric
and candidate-price first coefficients are (-h^2) and (-C_{\rm Sh}),
respectively, with
\[
C_{\rm Sh}=\frac{\sqrt2(5-\sqrt5)}{192}>0.
\]
The common scale (h^2/C_{\rm Sh}) therefore matches the one-link jets.

For either four-link opposite-null commutator, all 21 affected faces give
geometric mixed coefficient (-h^2) and candidate-price mixed coefficient
(-C_{\rm Sh}); both first derivatives vanish. This holds for both
\([N_2,\bar N_3]=J\) and \([N_2,\bar N_2]=B\).

For the commuting control with adjacent (+J,-J) links, all 11 affected
faces have zero geometric jets, while the candidate-price first derivatives
vanish and its mixed derivative does not. After the same scale, the exact
spurious source is
\[
\alpha_{\rm comm}(h)=
\frac{\sqrt2 h^2}{(5-\sqrt5)\log p}
\left(4+10\log 12+\frac{\sqrt5-5}{2}\log p\right),
\qquad p=\frac{\sqrt5-1}{2},
\]
which is strictly negative since (0<p<1). Thus the candidate matches the
two designated commutators but fails the zero-curvature C2 control. This
rejects that particular source assignment as a universal geometric price
map; it does not reject the native D0 price or other instruments.

The script exits successfully when this hostile-control failure is detected;
its `FAILS candidate as required` line denotes the expected negative control.
The replay is exact SymPy algebra and does not claim full independent
coframe/link stationarity, physical instrument selection, refinement, or
positive GR closure.
