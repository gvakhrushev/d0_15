# Final review of the corrected paid-source packet

Reviewer: `/root/input_stationarity`
Date: 2026-10-21

## Pinned final files

| File | SHA-256 |
| --- | --- |
| `PROOF.md` | `0233f263571a40b345bf9fafe8ce198fa8d82f0976b38d69e0d44a96c4291dc8` |
| `check_saddle_and_weak_source.py` | `7a1129cb26cb2a19736bcaac3fbc5cfe264814429ea897a97a117271a2047514` |
| `RESULT.json` | `947bedc7b10aaaf9106b18c690c8f09a7e802de8135772870c8f99a964a83c7f` |

Both requests in the historical `REVIEW_INPUT_AGENT.md` are resolved.
The alternating-mode example now specifies the unit periodic interval,
`n h=1`, so its displayed strong and negative-norm equalities have the
correct volume normalization. The periodic negative norm now explicitly
uses mean-zero tests, equivalently the quotient by constants; this is
consistent with the zero-mean divergence source and the gradient
seminorm.

The checker is byte-identical to the independently reviewed and replayed
checker. `RESULT.json` is byte-identical to both the reviewed result and
the independent replay result. The two proof changes clarify the domain
and norm contract; they change no calculation or numerical input. No
additional replay was needed or performed for this final review. The
historical review remains unchanged and retains its original proof pin.

The previous acceptance therefore applies to this corrected proof:
the strict three-node paid comparison and the conditional positive
weak-source estimate, including its source sign and factor two, are
supported within their stated hypotheses. This does not establish
physical Book03 selection, the full mixed gauge/boundary inverse, strong
raw216 convergence, or closure of the D0-to-GR derivation.
`GR_closed=false`.
