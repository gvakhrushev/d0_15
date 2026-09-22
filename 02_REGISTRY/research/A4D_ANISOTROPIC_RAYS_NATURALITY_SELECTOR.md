# E-RAYSEL — Anisotropic Finite Rays and Continuum Naturality

CONTROL disposition: **ACCEPT AS RESEARCH / A4D-EXTRA-RAYS-ERASED-BY-METRIC-NATURALITY**  
Source memo: `MEMO_28_A4D_ANISOTROPIC_RAYS_NATURALITY_SELECTOR.md`

## Frozen finite spaces

No new finite symmetry is introduced.

The accepted Euclidean degree-two constrained space remains
[
\mathcal E^{(2)}_{S_4}
=
\operatorname{span}\{E_\delta,E_\perp\}.
]

After explicit ((1,3)) signature, the finite Lorentz class remains
[
\mathcal E^{(2)}_{Lor}
=
\operatorname{span}\{E_\eta,E_{sp}\}.
]

These are exact finite results.

## Euclidean extra ray

The (E_\perp) ray uses
[
u=(1,1,1,1),
\qquad
P=I-\frac14uu^T.
]

In a continuum frame this becomes a preferred unit direction
[
N_F=\frac12(e_A+e_B+e_C+e_D)
]
and projector
[
P_F=I-N_FN_F^\flat.
]

A Hadamard orthogonal frame change preserves the same Euclidean metric jet but changes this projector.

An explicit degree-two jet gives
[
E_{\perp,F}[h]\ne E_{\perp,F'}[h].
]

Therefore a nonzero continuum (E_\perp) contribution does not descend to the metric jet alone.

## Lorentz extra ray

The (E_{sp}) ray retains a preferred unit timelike vector (T) or equivalently the spatial projector
[
S_T=I-TT^\flat.
]

A local Lorentz boost changes (T) and (S_T) while preserving the same Lorentz metric.

An explicit degree-two perturbation jet gives
[
E_{sp,T}[h]\ne E_{sp,T'}[h].
]

Hence a nonzero continuum (E_{sp}) contribution is also a metric-plus-frame law rather than a metric-only law.

## Conditional continuum selector

Let a normalized finite family be
[
E_N=a_NE_{iso,N}+b_NE_{extra,N}.
]

If:

- the normalized basis rays have nonzero finite continuum principal-symbol limits;
- the total response has a genuine metric-only locally Diff-natural continuum limit;

then the effective anisotropic continuum contribution must vanish:
[
\boxed{
\lim_N R_N(b_NE_{extra,N})=0.
}
]

If (b_N\to b) in the chosen normalization, then
[
\boxed{b=0}.
]

This selector is imposed by the continuum target type, not by an added finite symmetry.

## Important firewall

This does **not** prove
[
b_N=0
]
at every finite stage.

An externally chosen sequence (b_N\to0) is not a D0 derivation unless a separate internal theorem forces that decay.

The result selects only the continuum-admissible principal linearized ray:

- (E_\delta) in the Euclidean diagnostic class;
- (E_\eta) in the Lorentz class.

It does not construct a nonlinear Einstein tensor and does not replace the later Lovelock/Navarro stage.

Terminal result:
[
\boxed{\texttt{A4D-EXTRA-RAYS-ERASED-BY-METRIC-NATURALITY}}.
]
