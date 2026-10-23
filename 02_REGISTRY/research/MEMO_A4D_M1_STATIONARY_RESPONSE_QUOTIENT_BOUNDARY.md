# A4D M1 stationary response quotient boundary

**Packet:** `WRK-A4D-M1-STATIONARY-RESPONSE-QUOTIENT-COMPLETENESS`
**Lane:** `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`
**Execution:** PR #310, Draft, `IN_PROGRESS`
**Status:** `PARTIAL / OPEN`; no terminal is declared.

## Verdict

The quotient architecture is the correct replacement for an unbounded Bloch-stratum census, but the current owners do not prove a nonlinear stationary response quotient on the full joint-critical fiber. The strongest closed result is a finite exact tangent/finite-cell quotient statement together with an explicit nonlinear boundary.

The exact certificate is:

`02_REGISTRY/research/certificates/a4d_m1_stationary_response_quotient_boundary_check.py`

It is can-fail and records the following facts without promoting them:

- flat real period-four connection Hessian: rank `80`, nullity `16`;
- stacked connection plus metric readout: rank `88`;
- joint-invisible tangent dimension: `8`;
- response rank on the stationary kernel: `8`;
- curved finite-cell Y response defect: `89561/26250` relative to the flat `-1/2` TT coefficient;
- the #227 connection-stationary family has nonzero normalized metric response, but is not joint-critical and therefore is not a task-level NO-GO witness.

Thus the exact finite identity is only

```text
finite stationary tangent memory = 8 response-visible directions
                         + 8 owned joint-invisible directions.
```

The second summand is not gauge. Response invisibility does not identify a connection direction with a Lorentz gauge orbit.

## Correct quotient order

For the raw stationary carrier define, where the declared readout topology permits it,

```text
K ~obs K'  <=>  Resp_h(K) = Resp_h(K').
```

Gauge invariance must then be proved as a property of `Resp_h`; it must not be inserted by defining the carrier after quotienting. The quotient is an output of the observable relation, not a preselected tuple of moments. A candidate such as `(P w, D_G c, holonomy moments)` is therefore only a presentation to be tested, not the definition of the minimal memory.

The finite rank identity gives a valid local candidate presentation only on its declared carrier and stratum. It does not prove that every nonlinear stationary connection has a representative in that presentation, nor that the forgetting map reflects derivability for the full coupled equations.

## Exactness boundary

The requested nonlinear theorem would need all of the following under one fixed source convention and the unweighted owner sum norm:

1. a typed stationary fiber and local Lorentz action;
2. an internally constructed response memory independent of `Resp_h`;
3. factorization of every owned metric readout through that memory;
4. faithfulness, including reflection, for the forgetting map;
5. refinement-uniform realizability or an exact joint-critical obstruction.

The current finite owners establish item 3 only at finite tangent/cell scope. They do not establish items 4 or 5. The remaining compound blocker is therefore:

```text
JOINT-CRITICAL-REALIZABILITY-AND-OWNER-SUM-CONTROL
```

This is one blocker class, not an invitation to enumerate more Fourier sectors. It requires either a refinement-uniform nonlinear continuation theorem for the surviving joint-invisible carrier, or a smooth-background exact joint-critical counterexample with a certified nonzero normalized response gap.

## Why no NO-GO is minted

The curved #227 family is a named second object with nonzero response, but it satisfies only `E_K=0`. The lane contract explicitly excludes a response discrepancy from a merely connection-stationary sequence as a joint-critical NO-GO. The exact Y finite-cell obstruction likewise does not construct a refining exact joint-critical sequence with the required owner-sum gap.

Consequently neither

```text
A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED
A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO
```

is justified.

## H_TORUS disposition

`H_TORUS` remains a possible auxiliary lemma only. It is not needed for this boundary result and cannot be treated as a terminal, since its infinite-family scope requires a genuine spectral argument rather than finite sample coverage.

## Reopening hook

The lane can reopen positively if an artifact proves, for the full declared joint-critical class and the same source/comparator convention,

```text
||E_Q(Q_h,K_h) - E_Q(Q_h,K_h^sm)||_owner = o(h^2),
```

or negatively if it produces a smooth-background exact joint-critical sequence in the genuine Lorentz quotient with a nonzero `liminf` or exact limit after `h^-2` normalization. Any result limited to `E_K=0`, a designated small ball, a tangent rank identity, or a phase-averaged weak limit remains below both terminals.
