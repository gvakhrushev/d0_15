# D0 v11.34 — Executed alpha scheme passport contract

## Claim ID

`D0-QFT-RG-ALPHA-001`

## Status

`BRIDGE-EXECUTED / SCHEME-CONTRACT-CERTIFIED`

## Scope

This is not a new alpha prediction.  It is the first executed QFT/RG bridge contract: a D0 electromagnetic bare-response token may be compared to an external `\overline{MS}` or on-shell alpha only after the scheme, scale, beta kernel, threshold convention, and external input are fixed.

## External standard language

A scheme-specific comparison must state:

```text
quantity: alpha
scheme: MSbar or on-shell
input scale: μ0
output scale: μ1
kernel: declared beta function
thresholds: declared / disabled
external input: cited value or data bundle
free repair parameters: none
```

## Executed minimal kernel

The v11.34 cert implements a one-loop QED running contract:

```math
\alpha^{-1}(\mu_1)=\alpha^{-1}(\mu_0)-\frac{2}{3\pi}\sum_f N_cQ_f^2\log\frac{\mu_1}{\mu_0}
```

with all active species explicitly listed.  The kernel is intentionally minimal; a full SM electroweak passport must replace it with a declared `\overline{MS}` electroweak matching package and threshold table.

## No-hidden-parameter guardrail

The cert fails if:

1. an undeclared threshold appears;
2. an adjustable beta coefficient is introduced;
3. the output value is overwritten by a target number;
4. the scheme name is absent;
5. the external input value is not recorded.

## Integration consequence

Any D0 coefficient claim facing PDG/RG comparison must now cite a scheme-passport row rather than a naked numeric agreement.
