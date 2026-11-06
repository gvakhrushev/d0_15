# Original book inputs for historical research replay

The maintained books are editable exposition. Twenty-seven existing research checks
also use complete book-file hashes as part of their historical evidence. Those
checks must keep reading their original inputs when the exposition changes.

`HISTORICAL_INPUT.json` binds the unchanged checker and receipt bytes from
published commit `30ffef0f5a4353874f8966a4b69d09e534f3c47d` to the exact original
Book 00/01/02/03/06 bytes at published commit
`34dc2ddd6cf40803b95cf8afe66f9dd87f0bf22a`. Each book has both its Git blob and
SHA-256. Existing Book 01/03/06 snapshots are reused; only Book 00/02 are copied
here. The expected scientific receipts and original checkers are unchanged.

The existing isolated research runner applies the binding only to its twenty-seven
named, byte-checked entrypoints. It validates the exact snapshot, checker and
receipt before writing any overlay; then it restores the edited book bytes and
detects input mutations. The overlay composes with the previously registered
native-checkpoint inputs. Its logs explicitly report
`HISTORICAL_BOOK_INPUT_REPLAY_NOT_CURRENT_BOOK_PROOF`, original and maintained
hashes, and the bound receipt. This validates the recorded calculation at its
original scope; it does not certify current narrative prose or promote a claim.

A direct invocation of a historical checker against revised current books can
therefore report its expected source mismatch. Use the existing isolated runner
for the historical replay, and the repository's structural, link and
claim-strength checks for the editorial changes. Do not refresh old expected
hashes to make revised prose look like original evidence. Other checkers retain
their existing execution mode; this binding is not a general source fallback.

Focused implementation controls:

```bash
python tools/test_historical_book_inputs.py
python tools/test_run_research_certs.py
python tools/test_research_input_closure.py
```

For final integration use the normal committed-input research runner. Its
dependency selector keeps affected consumers selected and adds the explicit
historical-book binding; it does not suppress a source mismatch or change the
scientific replay's acceptance boundary.
