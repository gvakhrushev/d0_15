# D0 v16 Architecture and Channel-Dynamics Synthesis

**Date:** 2026-09-27  
**Status:** `ARCHITECTURE-AND-CHANNEL-DYNAMICS-SYNTHESIS-CLOSED`  
**Binding correction:** the unrestricted one-tick global channel sign vanishes on a fixed split and one unitary tick.

No existing core status is lowered. No Bianchi/remnant, dusty-plasma, LIGO, or survey result is promoted by this synthesis. Layer 2's global-sign reading is superseded by the finite-budget + moving-split/history account.

## 1. One-tick balance

For a finite orthogonal split (H=\operatorname{im}P\oplus\operatorname{im}Q) and
[
U=\begin{pmatrix}A&B\\ C&D\end{pmatrix}
]
unitary, define
[
F_N=C^\dagger C,qquad F_Q^{\rm emit}=B^\dagger B.
]
Unitarity yields
[
A^\dagger A+C^\dagger C=I_P,qquad AA^\dagger+BB^\dagger=I_P,
]
hence
[
\operatorname{Tr}F_N
=\operatorname{rank}P-\operatorname{Tr}(A^\dagger A)
=\operatorname{rank}P-\operatorname{Tr}(AA^\dagger)
=\operatorname{Tr}F_Q^{\rm emit}.
]

Therefore the unrestricted fixed-tick ratio
[
\sigma_N=
\frac{\operatorname{Tr}F_Q^{\rm emit}-\operatorname{Tr}F_N}
{\operatorname{Tr}F_Q^{\rm emit}+\operatorname{Tr}F_N}
]
is zero whenever the denominator is nonzero, and is defined as zero when both channels vanish.

The nontrivial one-tick budget is
[
\operatorname{Tr}(U_{\rm eff}^\dagger U_{\rm eff})+\operatorname{Tr}F_N
=\operatorname{rank}P,qquad U_{\rm eff}=PUP.
]

**Binding no-go:** Phase A and Phase C cannot be opposite signs of one unrestricted global trace ratio on one fixed unitary block.

Dedicated owner task: `WRK-D0-V16-ONE-TICK-BALANCE-TWO-SPLIT-OWNER`.

## 2. Sign belongs to history/window

A nonzero channel sign requires a moving split, a declared window, a sector projector, compressed dynamics, or a family of ticks. For a declared history define
[
A_n=\operatorname{Tr}(\Pi_{\rm in}F_N(n)),qquad
B_{n'}=\operatorname{Tr}(\Pi_{\rm out}F_Q^{\rm emit}(n')).
]
The budget sign target is
[
\sigma^{\rm budget}_{n,n'}=
\begin{cases}
(B_{n'}-A_n)/(B_{n'}+A_n),&A_n+B_{n'}>0,\\
0,&A_n+B_{n'}=0.
\end{cases}
]
To separate intensity from changing window rank, also test
[
\bar A_n=A_n/\operatorname{rank}\Pi_{\rm in},qquad
\bar B_{n'}=B_{n'}/\operatorname{rank}\Pi_{\rm out},
]
and the analogous density-normalized sign.

The explicit finite construction and history-swap negative control are delegated to `WRK-D0-V16-MOVING-SPLIT-CHANNEL-SIGN`.

## 3. Two-split rule

**Observer split:** (P_{\rm obs}) is what an asymptotic/laboratory detector retains; purification is an observer-frame statement.

**Medium split:** (P_{\rm med}) is the still-active scene/cloud and (Q_{\rm med}) the archived/sink complement. The owned medium archive
[
B_n=A_0(1-\varphi^{-n})
]
is monotone increasing.

Thus (P_{\rm obs}=P_{\rm med}) is forbidden unless an explicit functor identifies them. Observer-frame return is not a decrease of the medium archive, and D0 core does not acquire a Page curve by relabelling.

## 4. Thermodynamic pair

Keep together
[
A_n=A_0\varphi^{-n},quad
B_n=A_0(1-\varphi^{-n}),quad
R_n=\varphi^n-1,
]
with
[
\Delta B_n>0,quad \Delta^2B_n<0,quad \Delta^2R_n>0.
]
For
[
L(V)=-d_\tau\log(1-z+ze^{-\kappa V}),qquad \kappa=\log\varphi,
]
the owned chart (0<z<1) has (L'(V)>0,L''(V)<0). A long external metastable remnant envelope does not alter these internal signs.

## 5. External bridge only

The 2026 remnant literature supplies a typed A/B/C dictionary: active loss, quiescence, and late purification/return. A sign comparison
[
\operatorname{sgn}k(u)\longleftrightarrow\operatorname{sgn}\sigma_{n,n'}
]
is only a theorem target after an explicit Bondi/readout functor and declared split/window history.

The corrected external lifetime lower bound carried by the bridge ledger is
[
\tau_C\ge \frac{4}{\alpha}\frac{M_0^4}{\hbar^{3/2}},
]
while exponential-area lifetime requires an additional metastability hypothesis. These are external envelopes, not D0 predictions.

Dusty plasma remains LAB-BRIDGE / PASSPORT-SEED. LIGO residuals remain passport/negative-control. Survey cosmology does not select internal parameters.

## 6. Section-map boundary

An internal capacity depth may be written
[
n_*=\frac{\log(1+R_*)}{\log\varphi},qquad
\tau_*=n_*\tau_0,qquad \tau_0=h/\Lambda_{\rm act}.
]
A comparison with external remnant mass/lifetime requires
[
\mathcal S:(\operatorname{rank}P,\Lambda_{\rm act},\varphi,R_*,\ldots)
\to(M_0,\tau_C).
]
No such section is owned. Fitting (n_*) to the universe age, a PBH mass, or a remnant lifetime is forbidden. The section/no-go problem is registered as `EXP-D0-V16-SEAM-PURIFICATION-SECTION-MAP`.

## 7. Binding hostile controls

1. one fixed global unitary tick cannot give unrestricted (sigma_N\ne0);
2. (k\ne\operatorname{Tr}F_N);
3. (S_{\rm rad}\ne B_n);
4. (P_{\rm obs}\ne P_{\rm med}) without an explicit functor;
5. no cosmological/PBH fit of (n_*);
6. no Planck-scale identification without a section;
7. dusty plasma is not tabletop quantum gravity;
8. toroidal bridge geometry is not (Omega_8);
9. (Lambda_{\rm act}) is not retuned to a remnant lifetime;
10. no LIGO confirmation claim.

Final tokens:
[
\texttt{ONE-TICK-BALANCE-LEMMA},quad
\texttt{TWO-SPLIT-RULE},quad
\texttt{CHANNEL-SIGN-ON-HISTORY-TARGET},
]
[
\texttt{REMNANT-LIFETIME-PASSPORT-TARGET},quad
\texttt{NO-SURVEY-FIT},quad
\texttt{NO-LIGO-CONFIRMATION}.
]
