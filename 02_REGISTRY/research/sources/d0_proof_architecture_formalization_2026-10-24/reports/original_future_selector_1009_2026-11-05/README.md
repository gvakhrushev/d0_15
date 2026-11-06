# Original future-history selector: pinned 1009 replay

The original deterministic selector from #334 was replayed once, without a
new search question, on its published source blob `d111c5bfeae3c384a4fe725f4a6d19277ea0005a`
at commit `eebcb5e467742df3e9cf7fa9702042d7294aa742`. The verified uniform source
blob was `ee8de4635d24c668949ac9a0186616ab7d59f2ed`. The local wrapper and
source are trusted code, not a sandbox.

The output `histories.canonical.json` contains 128 distinct slot histories;
the length distribution is 11,111,6 for lengths 1,2,3. Its exact UTF-8 bytes
are `json.dumps(words,separators=(',',':'))` without a trailing newline, with
SHA-256 `7da6c5e307a8afac819f4096a8c173576b2498f9faede3e316ec21e7b0485e3a`,
matching the original owner. The replay's cumulative ranks are 11,122,128
modulo 1009; they are not ranks of separate length layers. The wrapper checks
the pivot set before writing, but the pivots themselves are not included as
an independent certificate in this report. `metadata.json` records the run,
versions and scope. An independent review checked these output bytes, the
histogram and the source blobs against the pinned Git tree.

`tools/extract_original_future_witness.py` reproduces this one-prime selection
from the pinned local source copies. It checks hashes before executing them,
locks the caller-specified Lean build lock and checks resources/processes.
The lock coordinates only users of that lock; the caller must keep other
checkouts and direct Lake runs idle. Library warning output may contain local
paths and must be reviewed before publication. The selected output directory
must not exist. The existing eight-prime owner verification is not repeated
or replaced here. This replay is not a proof that these histories are linearly
independent over `ℂ`; the localized effect membership and determinant
transfer remain open. Physical admission and #334 remain unchanged,
`GR_closed=false`.
