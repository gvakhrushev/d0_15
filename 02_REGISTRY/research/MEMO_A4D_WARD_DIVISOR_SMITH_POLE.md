# A4D Ward locus is a divisor; linear Res withdrawn

**Lane:** EXP-A4D joint Palatini / resonance response
**Class:** RESEARCH / SYNTHESIS
**Status:** durable record of session certificates, 2026-09-28
**Firewall:** no BOOK/claim promotion, no Einstein identification, no finite T_μν.

## Terminal

```text
A4D-WARD-LOCUS-IS-DIVISOR
A4D-SMITH-POLE-ORDER-AT-MOST-TWO
A4D-LINEAR-Q-ON-FLAT-GIVES-NO-RES
```

Withdrawn (do not reuse):

```text
A4D-ORTH3-SIMPLE-POLE-RES-110   # inconsistent Q assembly on background connection
A4D-RESONANCE-IS-TWO-POINTS     # contradicted by the two-phase rank scan
```

## 1. Closed, exact

On the diagonal family `Z = (z,z,z,z)` the connection Hessian satisfies

```text
det A(z) = (z^2 + 1)^12 / (16 z^12)
```

Zero order at `z = ±i` is 12. At the spike `rk A = 16`, geometric nullity 8.
Algebraic multiplicity 12 versus geometric 8 is Jordan / Smith data, not a
bookkeeping error.

The local degeneration matrix on the line `z = i + w`,

```text
M = N_L A'(i) N_K     (8 x 8)
```

has `rank M = 4`. Therefore `A^{-1}` is allowed a pole of order 2.

Column-order histogram of `A(i(1+δ))^{-1}` (four dyadic δ):

```text
p = 1 :  6 columns
p = 2 : 18 columns
```

This is coarser than the first Smith guess `(4 x δ^2) ⊕ (4 x δ)`. The
existence of order-2 poles is certified; the exact Smith blocks are not.

## 2. Locus is a divisor

Exact ranks of `A(Z)` on the character torus (selected probes):

| Z | rk A | nullity |
|---|---|---|
| `(i,i,i,i)`, `(-i,-i,-i,-i)` | 16 | 8 |
| opposite-phase pair, others at `i` | 20 | 4 |
| same-sign pair `π/2,π/2` | 22 | 2 |
| single phase shift | 24 | 0 |
| IR `z = 1` | 24 | 0 |
| half-wave all `-1` | 16 | 8 |

Working divisor law (hypothesis, matches every probe so far):

degeneration requires both counters `n_{+i}` and `n_{-i}` even and
`n_{+i}+n_{-i} ≥ 2`; then `nullity = 2 * max(n_{+i}, n_{-i})`.
Odd counters kill the kernel. This is not proved for the whole torus.

`#227` occupies the full-spike stratum `Σ_16`. A two-role lock with
`Z_r Z_s = -1` occupies `Σ_20`. Designated slow `#241` lives in `Σ_24`.

## 3. What is dead

- Germ tower: `M_1 = 0`, `M_k ∈ im C` on orbits 5/7 (`#303` / D2).
- `F_7`: in `im A` already at the spike; metric readout identically 0
  in every linear channel tested.
- Linear `Q^T (-A^{-1} F)` on the *flat* background: after evaluating the
  mixed block at vanishing background connection, both Orth3 and F7 give
  `dE_Q = 0`. The number `Res ≈ 110.85` came from a Q that still depended
  on a background connection and is withdrawn.

This matches the owned identity `E_Q(q, I) = 0` (`#249`): the first metric
response of a connection forcing on flat solder is second order in the
connection, not a linear pairing.

## 4. What is open

1. Second-order metric readout of the spike forcing on `Q_h = η + h α`
   (the `#275` `t^3 h` channel). That is the only remaining linear-vs-jet
   place where a residue could reappear.
2. Proof or counterexample of the even-counter divisor law on the full torus.
3. Exact Smith form of `A(z)` at `z = i`, not only `rank M` and a histogram.
4. Whether the 18 order-2 columns are metric-visible after the second-order
   pairing is rebuilt on `Q_h`.

## 5. Law (synthesis, not a claim)

The Ward object, if it exists, is the polar part of the *second-order*
response along the stratified divisor `{det A = 0}`, with pole order at
most 2. It is not a finite spacetime `T_μν`, not `F_7`, and not a Cauchy
kernel supported only at two points.

Designated Einstein is the statement that a smooth IR packet has no mass on
that divisor. `#227` is an atom on `Σ_16`.

## 6. Reproduction pointers

Session artifacts (not yet owner scripts on main):

- `det A` closed form: `a4d_detA_and_locus.py`
- locus ranks: `d0_a4d_locus_scan.json`
- `rank M = 4`: `d0_a4d_local_pole.json`
- `A^{-1}` histogram: `d0_a4d_Ainv_orders.json`

Do not treat `d0_a4d_residue.json` (`Res ≈ 110`) as an owner. It is the
withdrawn assembly.

## 7. Relation to live PRs

- `#260` (draft): even / odd germs on N0. Compatible: N0 sits in the spike kernel.
- `#202` (draft): curved stationary search. Different carrier.
- `#310` (draft): resonance resolvent / uniformity. Consume this memo; do not
  import the withdrawn residue.
