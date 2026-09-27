# WRK-D0-V16-MOVING-SPLIT-CHANNEL-SIGN

Class: `WORKER`
State on registration: `PLANNED`
Parent: `CTRL-D0-V16-CHANNEL-DYNAMICS-INTEGRATION`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/d0-v16-moving-split-channel-sign`
Primary artifact: `02_REGISTRY/research/D0_V16_MOVING_SPLIT_CHANNEL_SIGN.md`
Execution: `GitHub-first`

## Why delegated

The one-tick balance proves that a nontrivial sign cannot live on one unrestricted fixed unitary block. The next bounded constructive problem is an explicit moving-split/windowed history whose sign is nonzero for a reason other than window-rank change.

## Objective

Construct exact finite (P_n,Q_n,U_n,P_{n'},Q_{n'},U_{n'}) and frozen input/output windows. Compute both total-budget and rank-normalized density signs. Prefer equal-rank windows. A positive result must show a nonzero sign and its history-covariant swap.

## Required gates

Reproduce the one-tick zero-sign control on the same carrier; freeze windows before reading the sign; rule out rank-size artefacts; verify
[
\sigma_{n,n'}[P,Q,\Pi_{in},\Pi_{out}]
=-\sigma_{n',n}[Q,P,\Pi_{out},\Pi_{in}]
]
for the declared history; show sector-preserving histories give zero; do not identify the finite sign with Bondi (k(u)).

## Terminals

Use `D0-V16-MOVING-SPLIT-CHANNEL-SIGN-CERTIFIED` for an exact construction passing all gates. Use `D0-V16-MOVING-SPLIT-CHANNEL-SIGN-NOGO` only after exact exhaustion of a declared complete carrier/window class.

## GitHub execution contract

Start from fresh current `main`; run `python tools/task_lifecycle.py start WRK-D0-V16-MOVING-SPLIT-CHANNEL-SIGN` first; open Draft PR before scientific edits; keep memo/certificate there; run guards; retire before Ready; set `Lifecycle: REVIEW`; never self-merge.

## Chat handoff

Return PR/head, exact matrices/projectors, both sign observables, swap/rank/sector controls, terminal or blocker, and validation.
