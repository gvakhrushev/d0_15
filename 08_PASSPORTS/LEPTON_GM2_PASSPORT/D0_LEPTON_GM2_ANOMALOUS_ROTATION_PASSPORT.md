# D0-LEPTON-GM2-001 — Lepton anomalous magnetic-moment scheme bridge

**Status.** `EXTERNAL-BRIDGE / ACTIVE-SCHEME-PASSPORT / NOT-A-NEW-PARTICLE-CLAIM`.

## Claim

The lepton anomalous magnetic moment comparison is not a core D0 constant and is not promoted by a naked numerical match. It is a scheme-dependent external bridge:

\[
  H_{ABCD}^{(\ell)}=D_DD_CD_BD_A,
  \qquad
  a_\ell^{D0,S}(\mu)=\mathfrak D_{SM}^{D0}(S,\mu,\Lambda_{act})\left[\operatorname{Tr}_K(H_{ABCD}^{(\ell)}\Gamma_{D0})\right].
\]

For the muon, the relevant finite support is the chiral lepton sector of the `V_11` shell. The bridge is locked by the already-fixed single action section

\[
  \Lambda_{act}=38m_ec^2,
\]

the detector half-gap

\[
  \delta_0={1\over 2\varphi^3},
\]

and the ABCD holonomy channel. No additional vector/scalar field, dark photon, supersymmetric particle, hidden threshold, or modified beta function may be introduced to repair the passport.

## Current external status guardrail

The external status of muon `g−2` changed materially after the 2025 Standard Model update: adopting the lattice-QCD average for leading-order HVP shifts the SM prediction upward and gives no significant tension with the experiment at the precision used in that update. Therefore D0 must not phrase this claim as "D0 explains an established anomaly". The correct statement is:

> D0 supplies a finite ABCD-holonomy / RG-forgetting passport for lepton magnetic moments. If a residual tension is present in a declared external scheme, the residual must be carried by this bridge without new hidden particles. If the declared SM scheme already agrees with experiment, the same bridge is a consistency passport, not a discovery claim.

## Executed bridge kernel

The scheme-side finite residual kernel uses the upward scale orientation for a muon-scale comparison, since

\[
  \Lambda_{act}=38m_e \approx 19.417960100000\,\mathrm{MeV} < m_\mu \approx 105.6583755\,\mathrm{MeV}.
\]

Thus the logarithmic bridge orientation is

\[
  \log\left({m_\mu\over\Lambda_{act}}\right),
\]

not the sign-reversed expression. The primitive D0 kernel cell is

\[
  K_{g-2}^{D0}(\mu)
  = {\alpha\over 2\pi}\,{\delta_0^4\over 30}\,
    \log\left({\mu\over\Lambda_{act}}\right).
\]

For \(\mu=m_\mu\):

\[
  K_{g-2}^{D0}(m_\mu) = 1.272943645057606e-08
  = 1272.943645\times 10^{-11}.
\]

This is **not** by itself the measured anomaly. It is the finite bridge kernel before the scheme-specific QED/EW/HVP/HLbL decomposition and the residual Hodge trace are declared:

\[
  a_\mu^{D0,S}(m_\mu)=a_\mu^{S,\mathrm{baseline}}+K_{g-2}^{D0}(m_\mu)\,\mathcal R_{\mathrm{residual}}^{D0,S}.
\]

A promoted empirical prediction requires an executed scheme passport for \(\mathcal R_{\mathrm{residual}}^{D0,S}\); until then this claim remains an external bridge passport, not a full numerical `CORE` prediction.

## Proof-cell obligations

| Field | Content |
|---|---|
| Claim ID | `D0-LEPTON-GM2-001` |
| Support object | `V_11` chiral lepton shell in the finite scene complex |
| Probe/gate | cyclic orientation operator \(O_{cyc}\), vertex/lepton response operator \(\Gamma_{D0}\) |
| Linear operator | ABCD holonomy \(H_{ABCD}=D_DD_CD_BD_A\) |
| Quadratic readout | normalized finite trace \(\operatorname{Tr}_K(H_{ABCD}\Gamma_{D0})\) inside the positive response grammar |
| External bridge | scheme-specific \(\mathfrak D_{SM}^{D0}(S,\mu,\Lambda_{act})\) |
| Forbidden shortcuts | new fields, modified beta functions, hidden thresholds, post-hoc EW constants, direct fit to the experimental central value |
| Falsification hook | a declared scheme passport requiring a nonzero new-field term, or a residual outside the finite bridge class after all external inputs are fixed |

## Relation to QFT

The QFT object is the scheme-dependent anomalous moment \(a_\mu^S\). D0 does not replace QED/EW/HVP/HLbL calculations. It provides a finite support and bridge grammar for the residual term and forbids interpreting an unexplained residual as evidence for new particles before the D0 finite holonomy/forgetting passport has failed.
