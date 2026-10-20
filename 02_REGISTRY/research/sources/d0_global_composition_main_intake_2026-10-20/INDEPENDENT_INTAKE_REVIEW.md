# Final ordinary-certificate and route review

Date: 20 October 2026.
Reviewer: `/root/checkpoint_integration`.
Method: read-only static inspection and byte/hash/tree comparison; no scientific replay.

**ACCEPT the reviewed final certificate closure and current route edits.** This review supplements the independent operational/writer review already frozen inside the packet. It is kept outside that packet to avoid a pin cycle.

## Certificate closure

Source worktree: `d0_global_synthesis`, based on `685cda165e905e29e37b55abd54dad17ea0f274c` at review.

| Artifact | SHA-256 |
|---|---|
| `02_REGISTRY/research/certificates/a4d_global_result_composition_check.py` | `e35d3d62eb49c5cc6ad6fc3ffed9cd96fabf8198430a503901446458700c24cf` |
| `02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/SHA256SUMS.json` | `850991b87275941b75548a552ee4e84b8b9e7a313021155277b7c5b1b1efbae3` |
| Packet `replay_packet.py` | `ce8deda36f4a8ef9abff399582a4376693aa04c2339f8f3d097dfd58165f176b` |
| Packet `FROZEN_REPLAY.json` | `dca4a97c07dab531ce9ac7a74e27cfaaf943d6f1c94650fc05c5576a258cca4d` |
| Primary `A4D_GLOBAL_RESULT_COMPOSITION_2026_10_20.md` | `aa593fa464a4d7e067d0a1ba763121fd229192b6d5c79d6f9b20d06469cb1d25` |

The manifest has **46 distinct canonical file pins; all 46 hashes match**. The wrapper has one top-level literal list of **47 unique string INPUTS**. Its set is exactly the 46 pinned canonical paths plus the hash-manifest path. That set also equals the complete actual packet-file inventory plus the primary note. There are no missing inputs, unlisted packet files or old deleted-root aliases. The only parent-relative manifest path resolves to the intended primary note inside the repository.

The ordinary entry point is not its own input, and the hash manifest does not attempt to hash itself. The committed entry point and manifest remain independently visible to normal Git/CI provenance. All 32 original snapshots are included in the literal closure and runtime pin map. The prior review independently matched their source tree entries, raw SHA-256 and Git blobs; their current pins remain unchanged.

The wrapper derives the repository root correctly from `parents[3]`, invokes only the packet replay with the current interpreter and `-B -O`, and propagates failure. The replay still has the independently reviewed explicit checks, before/after pin verification, size/SHA/Git-blob verification, complete JSON comparison and fixed `2e-11` floating tolerance. Its floating branch rejects booleans. It never rewrites expected results. Its three producers are the new operational, holonomy and full-price controls; no old raw216, geometric, full128-spectrum or Lean suite is called by this wrapper.

I did not rerun the 13 groups. The root's final replay report is execution evidence; this report is independent static acceptance of its frozen inputs and contract. A direct byte recheck at the end found the wrapper and manifest unchanged.

## Main/CONTROL route review

Reviewed worktree: `d0_global_main_intake`.
CONTROL base: `f396dc0fa862ccd950d17bd2e03640d7df87da8c`.
Main input: `90db3fe60c9b543b30e83008e3607899e8574738`.

| Route file | Change versus CONTROL base | Reviewed SHA-256 |
|---|---|---|
| `AGENTS.md` | 30 inserted lines; no removal | `488726b4aa4b9de5abeda5b260688a9715809de0befa942c00cad200a34e4fe0` |
| `00_WORK/README.md` | 10 inserted lines; no removal | `437661a753021c3f594b3ea9724435597d30d6d24ce7f2ab679cf01693fce9df` |
| `00_WORK/tasks/CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE.md` | 37 appended lines; no removal | `d870d2ab867bc7b08df21c3063d7a47a430ebc646709acaef0fe8f9e13f2c6e7` |
| `02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md` | 39 inserted lines; no removal | `dd20d12556244f94b2a5df860cff2f61c1265ec92eaf9cdd687ad50ee140bbae` |
| Root `README.md` | Requested reorganization of the opening synthesis; unchanged historical body | `f7e48068d37d16baf721c9ec80ec45bf23582e7a1ad49197e931fb45a5863152` |

The AGENTS paragraph on the same-carrier full-field minimum exclusion is restored **byte-identically** from main. All prior CONTROL AGENTS content, including its mandatory TRIZ/Golden-Beatty checkpoint, survives the insertion. The other three insertion-only documents likewise preserve their complete prior content. The task remains the existing CONTROL owner; no new task, lifecycle transition or scientific owner is introduced by the append.

The root README is not claimed insertion-only. It replaces and reorganizes the opening narrative into the requested composed argument. Its entire body from the first horizontal rule onward is byte-identical to the CONTROL base. The new opening retains the primary positive family, full-price boundaries, stopped versus field-minimum distinction, fixed-Q scope, existing #334, TRIZ/Beatty handoff, preserved strategy and universal-response premises. It explicitly leaves physical GR, raw216, `positive_gr`, `GR_closed` and the scientific parent open.

All route texts retain actual observation sensitivity, preparation and readiness; distinguish observation from field writing; consume the parallel original Julia all-jet result with its ownership; and require full continuation partition weights in the proposed prospective valuation test. They do not turn equal minimum continuation prices, a classical decoder, finite checks or a source-neutral completion into the missing physical premise.

The reviewed tracked diff from current main does not touch any expensive registered-suite trigger (`04_CERTIFICATES`, root `01_BOOKS`, claim/assumption/alias CSVs, requirements or the relevant global runners). The new research packet itself does not add such a trigger. This does not promise that ordinary research CI selects only the new wrapper: final conservative dependency selection and every selected replay remain required. No selection rules or mutation guards are weakened.

## Remaining integration boundary

This acceptance covers the exact source packet and the five route-file versions above. Publication SHA, byte-identical source copy into the final intake and its final committed CI selection are subsequent integration evidence, not asserted completed by this read-only review. No repository file, remote state, frozen receipt, claim or acceptance was modified here.

Machine-readable audit: `d0_global_certificate_final_audit.json`, SHA-256 `35b21425e83c66cdc31e6e329f1543f8376763feb8003f19d5f692958cf3c567`.
