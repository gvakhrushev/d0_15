# EXP-A4D-DISCRETE-PALATINI-TARGET-SPAN

Class: `EXPENSIVE`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `exp/a4d-discrete-palatini-target-span`
Primary artifact: `02_REGISTRY/research/MEMO_A4D_DISCRETE_PALATINI_TARGET_SPAN.md`
Execution: `GitHub-first`

## Why delegated

This is the independent top-down wall requested by the OTO strategy: use known Palatini/Einstein-Cartan structure as a classifier and ask whether the selected finite D0 action span already contains the required discrete seed, cosmological 0-jet and legal torsion-square sectors. Draft #203 contains useful exact checkpoints but was not a valid task execution and is not repository truth until reproduced/landed.

## Runtime / source gate

Do not continue the invalid `research/` execution as if it were canonical. Start from current `main` on the declared `exp/` branch. You may inspect #203 as a provisional source, but independently reproduce every imported terminal before relying on it.

Do not edit #202 or J2-bridge primary artifacts.

## Starting hypotheses to reproduce

Draft #203 reports:

- `j^2_flat Q(R)=0`;
- the naked Palatini-like seed is the owned `S_star`;
- open-torsion square is not full-affine invariant; legal torsion readouts come from joint residuals;
- the four channels `I_eta_adj, I_eta_opp, I_n_adj, I_n_opp` are independent on its sample matrix;
- adding a raw Lorentz volume `Vol_eta(Theta)=det Theta` raises the span by one on the flat-link locus.

The last point is NOT yet the final answer: raw `Vol_eta(Theta)` is only manifestly proper-Lorentz invariant. The task must decide whether the cosmological 0-jet can be written as a **full-affine legal** functional on the selected relative/resolved quotient (for example via the correct relative solder if valid), or whether Lambda requires a genuinely new physical datum.

## Objective

Classify the discrete target corresponding to Palatini + optional cosmological term + legal torsion-square against the selected action span

`{S_star, I_eta_adj, I_eta_opp, I_n_adj, I_n_opp}`

after the actual affine quotient.

## Required gates

1. Reproduce the flat-jet seed/completion split exactly.
2. Type the discrete Palatini target using only owned tensors.
3. Prove the full-affine transformation law of every proposed target term.
4. Test raw `Vol_eta`, relative-solder volume, and any graph-closure/resolved version; reject any term that is not legal on the selected quotient.
5. Determine the exact functional span by rational evaluation/rank plus structural proof where possible.
6. Separate `Lambda=0` and `Lambda!=0`.
7. Compare the connection/torsion Euler structure with the target Palatini/EC pattern without importing continuum equations as finite theorems.
8. Do not introduce Holst, phi coefficients, or an arbitrary new constitutive tensor merely to close the span.

## Desired terminal

One of:

- the selected finite action already spans the full-affine legal Palatini(+Lambda+T^2) target;
- Lambda alone requires one precisely identified additional legal invariant;
- or the target is obstructed by the affine quotient, with the smallest exact obstruction named.

## GitHub execution contract

Start from current `main`; run `python tools/task_dispatch.py EXP-A4D-DISCRETE-PALATINI-TARGET-SPAN`; open Draft PR first; checkpoint certificates before interpretation; no Lean/claims/release/BOOK promotion; never self-merge.

## Chat handoff

Return PR, SHA, exact span rank/basis, affine legality of the volume term, Lambda=0/Lambda!=0 verdict, and the single smallest remaining invariant/obstruction.
