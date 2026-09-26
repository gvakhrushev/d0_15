# WRK-A4D-JOINT-RESONANCE-LINEAR-KERNEL

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lane: `EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-joint-resonance-linear-kernel`  
Primary artifact: `02_REGISTRY/research/A4D_JOINT_RESONANCE_LINEAR_KERNEL.md`  
Execution: `GitHub-first`

## Why delegated

This is a bounded exact linear-algebra certificate over the already-owned #208/#216 polarized matrices. It should produce a reusable basis/table for the expensive joint-Palatini lane without taking ownership of any nonlinear branch or continuum theorem.

## Objective

Turn the existing #208/#216 polarized matrices into an exact **joint** linear kernel census.

At each singular L=4 character, let

[
N=\ker H_{AA}.
]

Using Hessian symmetry/polarized pairing, construct the metric equation map on (N),

[
C=N\xrightarrow{H_{QA}}\text{metric-response space},
]

with the correct conjugate-character convention.

Certify:

[
N_0=\ker H_{AA}\cap\ker H_{QA}.
]

Do not infer \(H_{QA}\) from rank arithmetic alone; build the exact matrix/map.

In addition, build the **full mixed joint Hessian**

\[
\mathcal H_J=
\begin{pmatrix}
0&H_{QA}\\
H_{AQ}&H_{AA}
\end{pmatrix}
\]

for every orbit representative using the same polarized pairing. Report its exact rank and nullspace before quotient, then identify which null directions are genuine metric gauge/flat directions, physical IR modes, connection-invisible modes, or mixed modes.

Also certify directly from the finite star formula that

\[
E_Q(Q,I)\equiv0,
\]

so the first connection coefficient of any near-flat joint Puiseux/analytic germ must lie in \(N_0\).

## Required outputs

1. Reproduce all nine owned singular orbit types and their exact ((r_H,r_{\rm aug},d)).
2. For each type print:
   - (dim N);
   - (operatorname{rank}(H_{QA}|_N));
   - (dim N_0).
3. Confirm the expected dimensions:
   [
   (20,24,4)\to0,quad
   (22,24,2)\to0,
   ]
   [
   (22,23,1)\to1,quad
   (20,23,3)\to1,quad
   (16,20,4)\to4.
   ]
4. Give exact bases over (\mathbb Q(i)) for every (N_0\neq0) orbit representative.
5. Identify the #227 tangent (B=K_1+K_2+K_3) with its quarter-wave Role pattern and prove it lies in the source-visible part, not (N_0).
6. For each (N_0) basis vector compute the first linearized plaquette curvature. A zero-curvature vector may be a flat/gauge candidate; a nonzero-curvature vector is not.
7. Compute the exact full joint Hessian rank/nullity for each representative and give a basis decomposition into metric-only, connection-only, and mixed null vectors before quotient.
8. Verify the tangent-cone statement \(E_Q(Q,I)\equiv0\) and identify the #227 tangent as excluded at first connection valuation.
9. Do not label any vector gauge without checking it against the repository's actual Lorentz/metric quotient.

## Terminal

`J2-JOINT-LINEAR-RESONANCE-KERNEL-CENSUS-CERTIFIED`

The worker may report a more specific negative terminal if the expected 4/1/1 residual dimensions are wrong.

## Boundaries

No nonlinear branch search. No torsion-free constraint. No new action term. No #202 edits. No global Einstein claim.

## GitHub execution contract

Start from fresh current `main`. Run lifecycle start, open a Draft PR before substantive edits, self-retire at the exact terminal, refresh against main before Ready, and never self-merge.

## Chat handoff

Return PR, SHA, the orbit table, exact bases for all nonzero (N_0), and the classification of the #227 tangent.
