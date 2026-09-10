# SELF-UNFOLDING OBSERVABLE RELATIONS — VERIFIED CLOSURE REPORT

Commit: uncommitted working-tree result

Lean module:
- `D0.Cosmology.SelfUnfoldingObservableRelations`

Certificate:
- `vp_self_unfolding_observable_relations.py`

Claims promoted to `CORE-FORMALIZED`:
- `D0-SELF-UNFOLDING-OBSERVABLE-RELATIONS-001`
- `D0-DYNAMIC-ARCHIVE-MEASURE-REDSHIFT-RELATION-001`

## Closed internal relations

- registered depths compose additively and their multiplicative readouts obey a cocycle;
- `1 + zD0(o,e) = phi^(o-e)` depends only on relative refinement depth;
- repeating the same emission observation one tick later gives
  `Delta zD0 = (phi-1)(1+zD0)`;
- any constant one-step multiplier compatible with that same protocol is uniquely `phi`;
- from origin depth, `zD0(n,0) = archiveGrowth(n) = phi^n-1`;
- redshift drift, metric-scale increment, and relative archive-growth increment coincide;
- active time retention uses `phi^-1` while depth expansion uses `phi`, with product one;
- dynamical shares are `visible(n)=phi^(-n)` and `archive(n)=1-phi^(-n)`;
- eliminating depth gives `dynamicArchiveShare = zD0/(1+zD0)`;
- the first dynamical archive share is `phi^-2=2-phi`, not the static dimension share `10/11`.

## Mutation controls

- the monotone integer-depth coordinate fails the phi drift law at one tick;
- a free one-step multiplier different from `phi` fails at the zeroth comparison;
- the dynamical golden archive share is rejected as equal to the static `30/33` count.

## Exact boundary

`zD0` is an internal comparison of preregistered refinement depths. The theorem does not identify it
with astronomical redshift, does not define an SI time interval, and does not promote the internal
dynamical archive measure to an observed matter-density, lensing, or dark-energy fraction. Those
steps require the existing `PRIM-PHYSICAL-REDSHIFT-OBSERVABLE` and a physical light/detector
comparison passport.

The result nevertheless removes internal freedom: once that physical protocol instantiates this
depth comparison, redshift drift, expansion increment, and dynamical archive response cannot be
tuned independently.

## Gate

- `validate_csv`: PASS, 673 claims
- `d0_logic_chain`: PASS, 532/673 chained
- `d0_value_model`: PASS
- `d0_score --strict`: PASS, 76.9%, zero integrity demotions
- `check_cert_can_fail`: PASS
- new exact-Q(phi) certificate and mutation controls: PASS
- v15 closure certificates: PASS
- book assembly / Lean aggregate idempotence: PASS
- `lake build D0.All`: PASS, 4534 jobs
- `check_no_sorry_in_core`: PASS
