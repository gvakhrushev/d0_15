# Pinned integrator review: original full128 causal archive feedback

21 October 2026. Review of the bounded continuation of existing #334;
not an assembly acceptance, a physical execution selection or a new task.

## Reviewed bytes and target

| File | SHA256 |
|---|---|
| `FORWARD_ARCHIVE_BOOK_DETERMINANT.md` | `3c75cc1c7c9928d2209fe58a930105412860aa6c2503801dadcd1ea7b10a5e70` |
| `check_forward_archive_book.py` | `ad83124690c44ddbaf4c217d2d7db666a9057fd1b8a542509e88f32658a52015` |
| `SOURCE_PINS.json` | `c435a168d41c9d3d20593daa7360de78671e1f7b5b491cf37c77e1d575012476` |
| `CHECK_RESULT.json` | `38d40ba3ada024c1dcfceac823b7e7c0e67919e97525e1c9d49b973468a91df9` |

Input proof owners are pinned at
`086fab99d8aaed7f712e9a3d2858c516b61901fc`. Integration also preserves
the concurrent paid-word/secant continuation through `ea0ea3be`; none of
the eight source-pinned inputs changed in that fast-forward.

The target is exact equality of the *feedback component*, with its actual
absolute first-tick boundary and every finite source jet, between the
declared complete causal return of the original full128 unitary and the
original v8 determinant. It is not equality of two complete physical prices.

## Independent algebraic verification

For an arbitrary unitary colligation, I independently reconstructed the
finite recurrence and its energy identity. The retained terminal archive
is `W_n=[D^(n-1)C,...,C]`; hence `I-T_n* T_n=W_n*W_n`. The telescoping
identity `W_nW_n*=I-D^n(D*)^n` uses `CC*+DD*=I`, not normality of D.
Sylvester's identity proves the full determinant without discarding any
archive dimension.

The physical one-round delay must multiply the aligned transfer by xi.
On the same active clock window the corner is a zero initial output row,
the aligned T_n block, and a final input column with no in-window output.
Thus the defect is `diag(I-T_n*T_n,I_h)`. This is the exact origin of
`-128 h log(1-z)`. The final proof correctly executes and pays all n+1
encounters, routes the last output into a retained guard, and retains the
final archive. It does not advance an occupied state by wrapping a counter.

For the original reflection `U=I-2VV*`, the displayed V is isometric by
`p+p^2=1` and the literal complete SELECT row identity. Its blank column
reproduces both controller ports and all64 workspace outcomes. The
relations `DC=-CB` and `C*C=I-B^2` then give

    det_Q[I-z C(sum_(j=0)^(n-1)B^(2j))C*]
      = det_H[(1-z)I+z B^(2n)].

This proof makes no choice of bright eigenvectors and has no constant-rank
assumption. It therefore survives birth of dark modes and supports all
finite derivatives. At fixed z, the strict-clock boundary has zero field
source; at moving z, its first and second derivatives are essential.
The ordered power derivative in the proof retains noncommuting dB.

I also checked the stated first/second uniform gap estimates by directly
differentiating ordered powers. Their scope is a uniformly gapped fixed
chart. Applying that fixed-mesh limit to the closing-gap heat scaling
would be invalid; the proof explicitly keeps the limits separate. Its
finite source identity does not imply convergence of the absolute clock
boundary when the data dimension grows.

## Decisive replay

The integrator ran only the new checker, with its actual native row owner:

```bash
PYTHONPATH=/tmp/d0_pydeps python3 check_forward_archive_book.py \
  --repo /workspace/scratch/07af0e1491e7/d0_15 \
  --output /tmp/d0_stronger_clock_root.json
```

It passed all68 controls and reproduced `CHECK_RESULT.json` byte for byte.
The new comparison includes the actual2048-dimensional Fourier-block
comparator, all128 Kraus blocks, a noncommuting proper-link tangent, dark-rank birth,
the strict first tick and moving-z boundary. The largest reported native
finite identity error is `1.31e-18`; the independent centered second-source
check differs by less than `3.73e-11`. This consumes one original Fourier
character, not a new numerical replay of all256 spatial sites. These are numerical diagnostics,
not interval certificates; the theorem is established by the algebra above.
The author's normal and optimized runs also agree byte for byte. No old
geometry, rank, root or Lean suite was replayed.

## Scope corrections retained in the final proof

- The embedding has zero initial archive component. An independently
  prepared archive or density retains its real preparation source.
- The full causal return is coherent. Fresh measured128-outcome rounds
  have another record algebra and are not given this programme's entropy.
- One bin is a complete supplied native word boundary. All internal
  primitive ticks and any additional active clock residues remain payable.
- Native forward routing, physical clock/cut choice and the remaining
  absolute Book/Info/work ledger are still premises of a physical application.

**Review disposition:** the declared finite feedback/source substitution
is mathematically supported on its original carrier. The complete
physical-price identification and `GR_closed` remain unproved.
