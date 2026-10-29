# Replay report: #334 `7261923` → `8daed32`

Checked 28 October 2026 against the exact source range stored in the parent
packet. PR #334 remained open and Draft at `8daed32d560df18837bcc69458a8fa538a9cf135`;
GitHub reported no checks for that PR head. The local source replay does not
claim owner CI.

## Exact changed checkers

| Source slice | Checker SHA-256 | Environment | Result | Receipt SHA-256 |
|---|---|---|---|---|
| `§7dd` retained-matrix-past algebra | `fb71526412848666723cc9561372d0548ed070fdeb87b48e78f225b49a4fb49c` | Python 3.9.6, SymPy 1.14.0 | 22 exact controls; normal and `-O` outputs byte-identical | `3480caabee6faaa986ff6aa97eb34757874248f5e9204b6a321f955f4480a3b9` |
| General direct-click mass-coordinate lift | `b6cafe1585008dde4f02d7b1532a6eff5b6d4813e32cbe8fcbd9de5cfb9a3773` | Python 3.13.5, SymPy 1.14.0, mpmath 1.3.0 | 109 exact/symbolic controls; normal and `-O` outputs match each other and owner JSON | `4f2253e74b024f10ee10f53c9ea4bbdba9eddebc94a27a4ad05998160f853009` |
| `§7de` fixed-boundary original full-price source | `9318066ea9ce011bc2c6eeaa381970131eb7138208df589c5dbc3353fcf8fb10` | Python 3.9.6, NumPy 2.0.2 | Both endpoint calculations pass with the declared error bounds | low: `78c41acd7dd771b15e2acfbffbf113024ee06d909200ae75b51760424ffa6416`; high: `4b05b28a3edcdc452528e1ecd44d1501312f47cd0f7be7a4be2d9f718e5d1b89` |
| `§7df` dust Cauchy constraint transport | `b79266d5f226552125b7e0500a43626665a78914b1ebb6c156dd1b983fea59fd` | Python 3.9.6, SymPy 1.14.0 | 28 exact controls; normal and `-O` outputs byte-identical to owner receipt | `42a9daf9a8eeebb4caad6ce386f3e666931c8d58ca0f6e4be0f1d88ad11ef8db` |

## Receipt correction

For the low `§7de` endpoint, the owner memo prints
`78c41acd7de771b15e2acfbffbf113024ee06d909200ae75b51760424ffa6416` as the
observed-receipt digest. The exact embedded JSON block, with its terminal LF,
and the independently rerun JSON both hash to
`78c41acd7dd771b15e2acfbffbf113024ee06d909200ae75b51760424ffa6416`. Their
parsed objects are identical. The printed digest therefore has a one-hex-digit
metadata discrepancy; the actual receipt is retained unchanged. The high
endpoint receipt and all scientific endpoint values match their recorded
hashes.

The endpoint source enclosures are positive at `nu=3/10`,
`[2.7116542905416325e-06, 3.4224091519646633e-06]`, and negative at
`nu=3/5`, `[-7.133383310467955e-07, -2.5834696237646147e-09]`. Its complete
homogeneous clock-source bound is `2^-240`; the derivative norm bound is 14
for the seven varying groups. Thus continuity yields one zero of the sum
direction, with first and last full groups fixed. It does not prove seven
separate Euler rows vanish.

## External Cauchy input

The `§7df` checker validates the tensor-identity and constraint-transport
algebra, not PDE existence. The cited primary paper states local existence
and uniqueness for the wave-gauge Einstein–dust Cauchy problem in Theorem 2.1,
and that constraint-compatible data give the original Einstein–dust system in
Corollary 2.2; it explicitly says the hyperbolic evolution can be localized.
The application here uses smooth data, zero initial spatial velocity relative
to the dust-orthogonal surface, and the stated Einstein constraints. See
[Choquet-Bruhat–Friedrich, *Motion of Isolated Bodies*](https://arxiv.org/abs/gr-qc/0605096).
The signature and coupling conversion remain an analytic part of the owner
proof; no imported coefficient is fitted by the checker.

## Scope

The four checks establish only the declared finite algebra and the two
endpoint enclosures. They do not run Lean, the original full128 history
compiler, or repository CI; they do not equate direct-click and full128
prices, prove physical admission, or close GR. Every output keeps
`GR_closed=false`.
