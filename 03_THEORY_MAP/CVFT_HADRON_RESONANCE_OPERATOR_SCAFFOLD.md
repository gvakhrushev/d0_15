# CVFT Hadron Resonance Operator Scaffold

Status: `OPERATOR-SCAFFOLD-COMPLETE`, not core, not certificate-closed and not
PDG-pass.

## Baryon Triple Carrier

The internal finite carrier is

```math
V_B=V_shell^{\otimes 3},\qquad \dim V_B=27.
```

The symmetric projector is

```math
\Pi_{S_3}={1\over 6}\sum_{\sigma\in S_3}P_\sigma,
\qquad
\Pi_{S_3}^2=\Pi_{S_3},\qquad
\Pi_{S_3}^\dagger=\Pi_{S_3}.
```

The symmetric carrier has dimension

```math
\dim \Pi_{S_3}V_B=\binom{3+3-1}{3}=10.
```

This is a 10D symmetric carrier / decuplet-candidate carrier.  It is not a
physical baryon resonance table until spin labels, flavour labels, frozen pole
set, mass/width transfer, GeV calibration and external PDG comparison are
provided.

## Allowed Pole Scaffold

```math
U_eff^B=\Pi_{S_3}(PUP)\Pi_{S_3}
```

or

```math
H_eff^B(E)=H_PP^B+H_PQ^B(E-H_QQ^B)^{-1}H_QP^B.
```

Allowed equations:

```math
\det(I-\zeta U_eff^B)=0,\qquad \det(E-H_eff^B(E))=0.
```

## Forbidden Promotions

- direct support-to-mass reading;
- random non-Hermitian resonance matrix;
- complex poles from bare positive `F`;
- post-hoc PDG sorting;
- changing `Lambda_act`;
- full baryon resonance table without spin/flavour transfer.
