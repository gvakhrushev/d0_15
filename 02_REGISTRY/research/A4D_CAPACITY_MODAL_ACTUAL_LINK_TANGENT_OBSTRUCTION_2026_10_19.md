# Capacity mean versus Book03 pathwise MDL: an actual Palatini link witness

19 October 2026. **Exact finite, scoped source obstruction.** This sharpens the
modal-versus-mean comparison in the current #334 gravity route. It uses the
original six-based-plaquette Palatini density and its 40 independent local
field directions. It does not decide which history aggregation the full D0
execution selects.

## Result

Consider the capacity branch of the full addressed-record instrument, with

\[
e_i=p^2(1+t^2 f_x),\qquad f_x=h^{-4}P_{\star,h}(x),\qquad t,h>0,
\]

for each fine leaf \(i\) assigned to geometric cell \(Q_x\). At the flat
coframe/link point, all success outcomes \((i,a=0,b)\) are tied modal
histories. There is an actual proper-Lorentz link tangent in the original
40-variable carrier for which two neighboring cells have opposite nonzero
\(Df_x\). Along this tangent, the lower envelope of the tied pathwise MDL
actions cannot be stationary, even though the optimized mean capacity
\(\Gamma\) is smooth.

More precisely, in the original null frame let

\[
X_{01}=(E_{01}-E_{10})\eta,\qquad
\delta U_0(0)=X_{01}U_0(0),\qquad
\delta U_r(x)=0\ \text{otherwise},\qquad \delta e=0.
\]

At the flat point \(U_r(x)=I\), \(e_r^a=h\delta_r^a\), exact differentiation
of all six based plaquettes gives

\[
D P_{\star,h}(0)[V]=h^2,\qquad
D P_{\star,h}(-\hat 1)[V]=-h^2,
\]

and zero at every other cell. Thus \(Df_0=h^{-2}\) and
\(Df_{-\hat1}=-h^{-2}\). This is a genuine left-link variation of the
Palatini carrier, not a freely assigned pair of probability coordinates.

On a covered address cut with at least one fine leaf in each of those cells,
the capacity profile gives two tied modal path slopes. The existing exact
source identity for each tied success path is

\[
DS_{i,0,b}[V]=D\Gamma[V]
 +\frac{\varphi-\ell}{\ell}De_i[V],\qquad \ell=\log\varphi.
\]

Writing \(A=D\Gamma[V]\), the two slopes are \(A+d\) and \(A-d\), where

\[
d=\frac{\varphi-\ell}{\ell}\frac{p^2t^2}{h^2}>0.
\]

For \(m=\min_{\omega\text{ tied}}S_\omega\), its one-sided derivatives
satisfy

\[
D^+m(V)\le A-d,\qquad D^+m(-V)\le -A-d,
\]

so

\[
D^+m(V)+D^+m(-V)\le -2d<0.
\]

At least one direction decreases the pathwise minimum. This conclusion is
independent of \(D\Gamma[V]\), the cell weights, and the other tied branches.
Positivity follows from \(\log x<x-1\) for \(x>1\), hence
\(\varphi-\log\varphi>1\).

## Consequence and boundary

The capacity mean can still have the exact conditional Euler transfer
\(\operatorname{Crit}\Gamma=\operatorname{Crit}P\). The result above shows
that this does not establish the Book03 classical minimum-code condition for
the same pointer histories and same pathwise likelihood binding. Within the
declared AF geometric carrier, the required opposite-leaf tangent is an
actual allowed link variation; it cannot be removed by treating the leaves as
independent coordinates and then claiming a geometric constraint.

The deterministic copy `C_Y` is field-independent, so it adds no source jet
that could remove this cusp. It realizes the readout but does not change which
pointer histories are tied or their first derivatives.

This is not a global D0 no-go. It leaves open a physically derived
memory-algebra history map that changes the tied path classes, or a complete
same-run Cost−Info source whose own preparation, archive, clock, controller,
or work derivatives modify the slopes. Such terms must come from that same
execution. The free nonnegative capacity defects minimize to zero and cannot
be relabeled as an independent matter tensor. Any further restriction of the
original Lorentz-link tangent is also a separate native-execution premise.

**Consuming parent:**
[`MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md`](MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md),
modal-versus-mean gate. The exact pointer/capacity source is in
[`A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md),
§§6.10 and 6.13; the geometric source convention is the original
[`A4D_AF_STAR_FULL_LATTICE_STATIONARY_FAMILY_2026_10_17.md`](A4D_AF_STAR_FULL_LATTICE_STATIONARY_FAMILY_2026_10_17.md).

**Smallest decisive check:**
[`check_capacity_modal_link_tangent.py`](sources/d0_capacity_modal_link_tangent_2026-10-19/check_capacity_modal_link_tangent.py)
recomputes the local density jet from the original six-plaquette formula,
checks its exact support and signs, and verifies the two-sided directional
derivative inequality symbolically. [`RESULT.json`](sources/d0_capacity_modal_link_tangent_2026-10-19/RESULT.json)
records the exact command, Python/SymPy versions, base Git ref, and SHA-256 of
the principal input files. It does not certify physical selection of the
pointer history space or the whole D0 action.
