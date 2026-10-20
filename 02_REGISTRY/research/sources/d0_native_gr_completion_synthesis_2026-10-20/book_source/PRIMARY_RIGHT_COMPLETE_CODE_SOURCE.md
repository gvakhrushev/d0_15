# Actual RIGHT likelihood, complete-code gain and its source

21 October 2026. Existing Draft
[#334](https://github.com/gvakhrushev/d0_15/pull/334),
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`;
native realization / `native-programme-v1`. Input
`ada0b43f6e31b19b22c266d303627b9549ecd04f` includes the published posterior application
`6f9285464419aa3d23ffdc30bbe7b5c9457730e6`.

Consumer: [the posterior application's physical binding](PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE.md#6-parent-substitution-and-the-remaining-physical-binding)
and [the parent](TWO_NATIVE_8D_DETERMINANT_SOURCE.md), §14.
The actual prior and posterior are now supplied. This continuation
constructs their operator likelihood on the same reference, transports
the complete code-relative source, and tests its use as a Book weight.
It does not select a physical code, Info law or RIGHT readout.

## 1. The actual operator map on the original reference

Keep DATA=site256×CAR16, RIGHT128, the original preparation C_t and
complete one-round instrument from
[the posterior owner](PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE.md).
Write N=128 and E=sqrt(N) C, so E*E=I_N. For any complete finite
instrument K_gamma acting identically on oldRIGHT, put

```text
B_gamma=C* K_gamma* K_gamma C, q_gamma=Tr B_gamma,
sum B_gamma=I_N/N.
```

The same statements apply to a genuinely complete finite stopped tree
with every abort retained. They do not authorize a new stopping rule.
Let mu_gamma>0, sum mu_gamma=1, be a SUPPLIED complete reference on
these exact leaves. If it is used as a physical code, its actual
encoder/price map is an additional input. In particular, port weights
alone do not supply label/coefficient/work weights.

The existing operator-likelihood construction has the concrete map

```text
M_gamma=E* K_gamma* K_gamma E/mu_gamma=N B_gamma/mu_gamma,
sum_gamma mu_gamma M_gamma=I_N.                              (1)
```

These matrices act on the coefficient copy of RIGHT; the physical
RIGHT operators are transposed under the original vectorization.
All spectra and traces below respect that convention.

For coarse leaves, mu_parent M_parent=sum_child mu_child M_child
whenever the actual instrument continuation has the corresponding
effect-sum identity. Thus the map is compatible with those supplied
coarsenings. This is an application of the owned naturality/likelihood
maps, not a selection of their measure or a new completion principle.

Polar decomposition retains the full branch map:

```text
K_gamma E=W_gamma sqrt(mu_gamma M_gamma).                   (2)
```

W_gamma is the actual partial isometry on the support. Equation(2)
also holds with kernels; a dark branch has zero positive factor.
Discarding W_gamma or averaging log M_gamma does not reconstruct the
native coherent branch vector, its phases or its first jet.

On the already certified faithful active chart set S_gamma=sqrt(N B_gamma).
The coherent jet is supplied explicitly, with no chosen eigenbasis:

```text
S_gamma DS_gamma+DS_gamma S_gamma=N DB_gamma,
W_gamma=(K_gamma E) S_gamma^(-1),
DW_gamma=[D(K_gamma E)-W_gamma DS_gamma] S_gamma^(-1).        (2a)
```

The positive Sylvester equation has a unique solution. In particular
D(K_gamma E) includes sqrt(N)[(DK_gamma)C+K_gamma DC]. These
formulas supply the entire native branch-jet input for the owned
direct Book source, conditional on its faithful memory/phase binding.
They do not establish that binding for the original algebra-valued
memory words. At uncontrolled rank changes keep the original smooth
amplitudes rather than assume a smooth polar map.

## 2. Full code-relative gain on the declared pointer cut

On the direct-sum algebra A_cq=direct_sum_gamma M_N set

```text
Omega=direct_sum_gamma B_gamma^T,
Tau_mu=direct_sum_gamma mu_gamma I_N/N.
```

Tau_mu is central on THIS algebra. Apply the already owned
[central gain theorem](../../d0_operational_gain_2026-10-15/RESULT.md):

```text
G_full=D_phi(Omega||Tau_mu)
      =D_phi(q||mu)+I_phi(R:Y),                              (3)
Tr[B_gamma log_phi M_gamma]
      =q_gamma[log_phi(q_gamma/mu_gamma)+i_gamma^R],
i_gamma^R=D_phi(B_gamma/q_gamma||I_N/N).
```

This follows by log(mu_gamma I_N/N)=log(mu_gamma/N)I within
each block. No commutation between distinct B_gamma is assumed.
All zero-probability terms retain their continuous value0.

For the matching LABEL code C_gamma=-log_phi(mu_gamma),

```text
A_cond=sum q_gamma C_gamma-G_full
      =H_phi(q)-I_phi(R:Y)=S_phi(Omega)-log_phi N
      =H_phi(Y|R).                                         (4)
```

The operational theorem's matching FULL operator cost is instead
-log_phi Tau_mu=C_gamma I+log_phi N. Its net is S_phi(Omega).
Thus (4) subtracts the fixed reference-capacity constant, not actual
preparation work. A constant log_phi N has zero source here, while
the physical cost of producing C_t can depend on t and remains due.

Identity(4) holds pointwise even for a supplied moving complete mu:
its code derivatives cancel between the matching cost and gain.
This removes unspecified label-code derivatives from THIS conditional
price. It neither chooses that physical contract nor cancels work
outside the matching code. Unnormalized Kraft mass cannot silently
replace the complete normalized reference in(3).

## 3. Exact source application without another spectral calculation

With fixed N and the actual normalization, (4) gives on a controlled
support chart

```text
D A_cond=-sum_gamma Tr[DB_gamma log B_gamma]/ln(phi).        (5)
```

All preparation and Kraus jets remain. Across rank birth use the
owned amplitude regularization; (5) is not a uniform refinement or
infinite-horizon estimate.

The preceding full-fine certificate already bounds both terms of(4)
on the original primary quadratic collar. In its
`wrong_omitted_conditional_normalizer_phi` field it bounds
i_1-h_1. Exact negation therefore gives

```text
d_theta A_cond|0=a_1 t+O(t³),
a_1 in [-6.359268283219129e-7,-6.35926827829028e-7].          (6)
```

The64 active B_gamma are faithful and the64 structural zeros remain.
No eigensolver or heavy old calculation is rerun for(6). This is the
complete declared periodic-storage L4 fixture, not arbitrary exterior
completion or a new all-mesh coefficient. Nonuniform code lengths
cannot alter(6) IF the same complete code-relative gain is selected;
genuine work and the physical aggregate still can.

The [bounded checker](check_primary_right_complete_code_source.py)
pins the original proof/checker/certificate and transports this exact
interval. Its independent rational three-block fixture tests(3)–(5)
with noncommuting posteriors and nonzero moving-code source on both
sides. The fixture is a hostile calculation control, not a replacement
for the native primary experiment.

## 4. The native paired-port test excludes standalone posterior gain

Reuse [the owned same-history binding](BOOK_SOURCE_BINDING.md#34-decisive-original-full128-nonblank-port-calculation),
not a new weight theorem. Every original nonblank pair obeys

```text
K_1k=p^(-1/2)K_0k, q_1k/q_0k=phi,
rho_(R|1k)=rho_(R|0k), i_1k^R-i_0k^R=0,
C_port,1-C_port,0=1.                                      (7)
```

If Info=i^R+I_extra and Cost=C_port+C_extra, the actual additional
ledger must therefore satisfy

| Same-history binding | Required Delta(I_extra-C_extra) |
| --- | ---: |
| Absolute amplitude | 3/2 |
| Absolute scalar probability | 2 |
| Extra marker on the executed native vector | 1 |

A common normalizer cancels from these differences. This is an exact
failed application of Info=i^R alone with only the known port cost;
it is not a no-go for a complete physical price.

The native conditional port reference (p,p²), if genuinely part of
the complete code, gives label-gain difference2. It repairs the
scalar pair but exceeds the amplitude requirement by1/2. No uniform
prior on64 labels or identification of those labels with RIGHT128
is introduced to fill the remaining code map.

## 5. An average gain is not a per-history exponential weight

Even after a complete mu is supplied, assigning the coarse branch
Info_gamma=log_phi(q_gamma/mu_gamma)+i_gamma^R would give

```text
phi^(-C_gamma+Info_gamma)=q_gamma phi^(i_gamma^R).           (8)
```

Under scalar normalization w/sum w, its law equals q only when
i_gamma^R is common on the positive support. Quadratic amplitude
normalization instead requires i_gamma^R+(1/2)log_phi q_gamma to be
common. The conditional expectation in(3) cannot be moved inside a
pathwise exponential.

There is a precise conditional refinement. If a physical spectral
RIGHT readout is actually executed and retained, let lambda_gamma,j
be its posterior eigenvalues, including multiplicities. Then

```text
P_gamma,j=q_gamma lambda_gamma,j,
mu_gamma,j=mu_gamma/N,
g_gamma,j=log_phi(P_gamma,j/mu_gamma,j)
           =log_phi(q_gamma/mu_gamma)+log_phi(N lambda_gamma,j).
```

With its genuinely matched complete code price, scalar weights on
these REFINED leaves equal P_gamma,j and coarsen to q. Absolute
amplitudes instead require the owned relation

```text
Info_amp,gamma,j=(C_gamma,j+g_gamma,j)/2+J,                  (9)
```

with actual phases and a common J retained. This is not a physical
derivation of(9). It states the necessary binding; the spectral test
is an additional programme, not a relabeling of the original leaf.

## 6. A fixed test suffices for the leading source, with exact admission scope

For the local leading coefficient, let P_gamma,j be fixed spectral
projectors of B_gamma(0), of ranks r_gamma,j and eigenvalues b_gamma,j.
They do not depend on t. The classical prior for this test is
r_gamma,j/N and the joint probability is Tr(P_gamma,j B_gamma(t)).
Since B_gamma(t)=B_gamma(0)+O(t²) and
d_theta B_gamma(t)=t R_gamma+O(t³), its gain source coefficient is

```text
sum_gamma,j Tr(P_gamma,j R_gamma)
                log_phi(N b_gamma,j/q_gamma(0))=i_1.        (10)
```

Thus no moving eigenbasis/controller is needed to reproduce the
certified leading i_1. What remains is an admitted, paid realization
of these fixed original-RIGHT tests, or an approximation with a
controlled mixed-jet error. Mathematical projectors do not provide
such a native word.

The literal original programme acts as identity on protected
oldRIGHT. Existing flag-copy owners act on active targets; their
placement does not supply oldRIGHT-as-control. Even seven supplied
RIGHT-to-fresh-flag CNOT placements would transport coherence to
the encoded joint RIGHT/flag carrier: forgetting the flags dephases
the original DATA–RIGHT marginal. Computational-basis readout then
uses the diagonal-gain functional built from diag B_gamma. Its source
is not established by(10). The exact Fourier witness proves that
gain's positive VALUE, not equality of its source to(10). All copies,
required observables and their work stay in the extended programme.

Finally A_cq is the declared classical pointer cut. The full coherent
Y–RIGHT marginal has offdiagonal blocks and generally does not
commute with Tau_mu. The central-prior theorem on A_cq cannot be
transferred to it by notation. Equation(2) preserves the branch maps
needed for that separate application.

## 7. Precise parent substitution

Parent §14 now consumes the actual operator likelihood(1)–(2), the
complete-code source identity(4)–(6), the exact failed standalone
RIGHT-gain binding(7), and the fixed-test leading-source map(10).
The full-code conditional price has a concrete source on the same
original primary carrier; nonuniform matching code derivatives are
no longer an unspecified contribution within that contract.

The physical target still requires the actual complete code/Cost map,
the selected algebra and event-level Info binding, paid RIGHT-test
placement if used, absolute Book normalization, full work and genuine
upstream equations. Neither conditional entropy nor spectral
optimization chooses that target. Same-initial field generation,
later history/refinement, compulsory native selection, full GR and
raw216 remain open. The [review receipt](PRIMARY_RIGHT_COMPLETE_CODE_SOURCE_REVIEW.md)
pins the bounded application. No task or positive acceptance is added.
