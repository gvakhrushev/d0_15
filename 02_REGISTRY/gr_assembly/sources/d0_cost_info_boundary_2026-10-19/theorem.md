# G0: boundary accounting for the Book 03 Cost−Info action

Status: **exact algebraic interface result; physical Cost/Info ownership remains
open**. This certificate resolves the composition boundary hidden in Book 03
§03.3.0, but does not select a new action, information readout, field map, or
physical source.

## Consumed statements

Book 03 §03.3.0 simultaneously states (i) that the code length of a composite
history is additive and (ii)

\[
S(\gamma)=\sum_{e\in\gamma}\operatorname{Cost}(e)
          -\sum_{v\in\gamma}\operatorname{Info}(v).
\]

Its prose describes `Info` as the distinguishability gained when a history
commits to a choice at a branch. The actual native scene history carrier is
the free path carrier on `K(9,11,13)`: singleton identity histories are
included, and composable paths are glued as `p ++ q.tail`. The underlying
owners are `ScenePathHistoryCanonicity.lean` and the complete additive action
fiber in [the existing history-boundary result](A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md).

## Literal vertex reading

If the displayed vertex sum means one `Info(v)` contribution for every listed
vertex, including the endpoints, then a singleton history has

\[
S([v])=-\operatorname{Info}(v).
\]

If singleton histories are action identities with value zero, this reading
already forces `Info(v)=0`. There is an independent composition defect. For
each actual two-step walk `u→v→w`,

\[
S([u,v,w])=S([u,v])+S([v,w])+\operatorname{Info}(v).
\]

The shared junction occurs once in the glued path and twice in the sum of the
two subpath vertex lists. Every vertex of the actual scene graph has an
incoming and outgoing edge, so additivity on all two-step compositions would
force `Info(v)=0` at every vertex. This is a conditional result about the
literal all-vertices convention; it does not show that the Book intended that
convention. The source's branch-choice wording could instead mean information
is attached to a transition event.

The companion Lean file proves the singleton formula, the exact two-step
defect, existence of an actual scene neighbor for every vertex, and the
all-vertices consequence. The exact finite checker covers all 718 directed
edges and all 15,708 two-step scene paths.

## Transition-event reading and its full boundary family

Let `Info(v_i)` be apportioned across the transition leaving or entering
`v_i`. For any real `θ`, define the weight on an actual directed scene edge by

\[
w_\theta(u,v)=\operatorname{Cost}(u,v)
 -\theta\operatorname{Info}(u)
 -(1-\theta)\operatorname{Info}(v).
\]

The history action is the sum of these edge weights. It vanishes on singleton
identities and is additive under every path composition: the two allocations
at the shared junction sum to one full `Info(v)`. In path form, the endpoints
receive coefficients `θ` and `1−θ`; every internal vertex receives coefficient
one. Thus `θ=1` is the source/branch-event convention suggested by “at each
branch the history commits to a choice.” The algebra also permits every other
`θ`; the current text does not explicitly state the endpoint convention or
identify its field-dependent physical owner.

For two allocations `θ,η`,

\[
S_\theta(\gamma)-S_\eta(\gamma)
 =(\theta-\eta)\bigl(\operatorname{Info}(v_n)
                       -\operatorname{Info}(v_0)\bigr).
\]

The difference is exactly an endpoint coboundary. Therefore all allocations
agree on closed histories, while an open history can distinguish them. Under
the Book weight `φ^{-S}`, the ratio of their open-history weights is
`φ^{-(θ−η)(Info(v_n)−Info(v_0))}`. This is not a physical gauge theorem: the
Book sum includes histories with memory classes, and no owner here proves that
the full readout removes endpoint reweighting. The result also does not weaken
the complete 718-dimensional edge-weight fiber; it identifies the exact
boundary freedom inside the displayed Cost−Info decomposition.

## Integration boundary

The files supplied in this turn are already integrated byte-for-byte in the
source packet
`sources/d0_af_full_feedback_first_source_2026-10-17/`, with the archive's
SHA-256, member map, provenance, and scoped replay results recorded there. This
new certificate consumes their source and recovery results without duplicating
them. It classifies one G0 interface issue raised by the Book's formula; it does
not establish that the AF source is the derivative of the selected full native
Cost−Info action.

The next load-bearing owner must bind the native branch/record event to its
`Info` value, say whether terminal and initial records contribute, and map that
same value through admitted field variations and refinement. Then the
source-subtracted contrast can be differentiated. No native metric variation,
Ward source, Einstein equation, or nonempty physical GR recovery follows from
the present interface result. The existing #310 exact-source/raw-owner terminal
is unchanged.

## Reproducible certificate

- Lean proof: [`a4d_native_cost_info_boundary.lean`](certificates/a4d_native_cost_info_boundary.lean)
- Exact finite controls: [`a4d_native_cost_info_boundary_check.py`](certificates/a4d_native_cost_info_boundary_check.py)
- Replay receipt: [`a4d_native_cost_info_boundary_results.json`](certificates/a4d_native_cost_info_boundary_results.json)
- Source pins and validation boundary: [`a4d_native_cost_info_boundary_certificate.json`](certificates/a4d_native_cost_info_boundary_certificate.json)

The Lean statements are research propositions over the existing scene/path
definitions. They do not amend `BOOK_03`, change the core definition, or install
`θ` as a new selector.
