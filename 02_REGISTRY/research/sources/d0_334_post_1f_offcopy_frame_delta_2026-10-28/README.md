# #334 post-1f4 off-copy AF frame replay

This intake preserves the exact changed checker and its ordinary, optimized, and owner receipts for the 28 October 2026 #334 head `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`. The source proof is §7di954–960 of the existing same-representative artifact at the pinned commit. The two commits after `1f4b85f14292dfac07f61db27ff47a961e525d03` are `b8f30f7c2ad4bde2975c789c57ef8187d8219b7f` and `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`.

`check_7di_offcopy.py` is extracted byte-for-byte from the owner artifact, including its final LF (`de29e556ac1e4fe7a4881fb5e26f7fe0287a99c85b6f2cd5c9396192a8213f88`). The compact `replay/repo/` fixture contains only the exact inputs it reads: the pinned AF tree module, native execution grammar, incoming apparatus proof, and exact 7dg tree-function block. The fixture does not replace or claim to reproduce the full 2.6 MB owner document; the block itself is hash-checked by the checker.

## Replay

Run with Python 3.12 and SymPy 1.14 from this packet directory:

```sh
cd replay/repo
python3 ../../check_7di_offcopy.py > ../normal.json
python3 -O ../../check_7di_offcopy.py > ../optimized.json
```

The replay returned 171 exact controls, with 55 inverse/decoding calls, 11 forward frame calls, 73 total AF calls on 356 columns, and a rank-8 protected input with the full 324-dimensional identity complement. Ordinary and optimized outputs are byte-identical to each other and to `replay/owner_receipt.json` (SHA-256 `21e2008f370c4dfc87e52ed98425ca3f2a1361cf7ae18f6727674cb7dcf38522`).

The finite operator result removes the independent frame-source premise only for this explicit off-copy layout and its guarded frame-stage supports. The cross-support negative control remains nonzero; the former diagonal fourth frame is not retroactively neutralized. Physical AF instruction admission, growth/routing, complete `X_N`/price, exact finite stationarity, and GR closure remain open. `GR_closed=false`.

Exact source Git blobs and all packet file hashes are listed in `MANIFEST.json`.
