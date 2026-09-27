# WRK-D0-V16-ONE-TICK-BALANCE-TWO-SPLIT-OWNER

Class: `WORKER`
State on registration: `PLANNED`
Parent: `CTRL-D0-V16-CHANNEL-DYNAMICS-INTEGRATION`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/d0-v16-one-tick-balance-two-split-owner`
Primary artifact: `02_REGISTRY/research/D0_V16_ONE_TICK_BALANCE_TWO_SPLIT_OWNER.md`
Execution: `GitHub-first`

## Why delegated

The final synthesis contains a load-bearing finite identity: on one fixed split and one unitary tick the unrestricted retained-to-archive and archive-to-retained Gram-channel traces are equal. It is bounded enough for an exact independent owner and formalization attempt.

## Objective

For arbitrary finite orthogonal (H=P\oplus Q) and unitary block (U), certify
[
\operatorname{Tr}(C^\dagger C)=\operatorname{Tr}(B^\dagger B)
=\operatorname{rank}P-\|A\|_{HS}^2
]
and
[
\operatorname{Tr}((PUP)^\dagger(PUP))+\operatorname{Tr}F_N=\operatorname{rank}P.
]
Do not assume equal sector dimensions. Prove the unrestricted fixed-tick sign is zero and give the (P\leftrightarrow Q) companion identities.

## Required hostile controls

Use an unequal-rank unitary example; a sector-preserving unitary with both channels zero; and a deliberately nonunitary block matrix where the equality can fail. Padded poles/zero padding must not change the carrier statement. Do not infer remnant phases or moving-split signs.

## Terminal

Use `D0-V16-ONE-TICK-BALANCE-OWNER-CERTIFIED` only with exact certificate controls and a formal owner where feasible; if formalization remains blocked, state exact-certificate status explicitly.

## GitHub execution contract

Start from fresh current `main`; run `python tools/task_lifecycle.py start WRK-D0-V16-ONE-TICK-BALANCE-TWO-SPLIT-OWNER` first; open Draft PR before scientific edits; keep memo/certificate/formalization there; run guards; retire before Ready; set `Lifecycle: REVIEW`; never self-merge.

## Chat handoff

Return PR/head, theorem, hostile controls, certificate/formal owner status, validation and any formalization blocker.
