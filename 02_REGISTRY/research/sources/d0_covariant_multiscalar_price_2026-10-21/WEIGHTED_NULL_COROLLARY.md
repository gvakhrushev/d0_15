# The same rank-two null solution survives every fixed positive PF weight

21 October 2026. Direct composition within existing research owner #334.
The [actual weighted-price theorem](../d0_causal_native_weighted_synthesis_2026-10-21/weighted_dynamics/WEIGHTED_WARD_AND_DUST.md)
and the [crossing-streams witness](CROSSING_STREAMS.md) give the following
same-coordinate continuum result. No new query, weighting, physical field
or variational constraint is introduced.

## 1. Exact interface and first variation

Use the original independent coframe, Lorentz connection and two real
scalars, with signature (+---), fixed coordinate volume, and
\(f=eR(e,\omega)\), \(q=\sum_A g^{\mu\nu}\partial_\mu\psi_A\partial_\nu\psi_A\).
The actual continuum price is
\[
 S_\rho=B_0+M\int \rho\,F(\tau f/\rho,\tau q/\rho)\,d^4z.
\]
Here \(\rho>0\) is any prescribed smooth PF/count coefficient, held fixed;
\(M,\tau>0\) and all parameters of the SAME local \(F\) are spatially
constant and fixed in these field variations. Retain
\(D_{\rm field}B_0=0\). Work locally with a nondegenerate coframe and compact
support or compatible transported collar data.

At a background with \(R=q=0\) pointwise, write
\(a_0=F_x(0,0)\ne0\), \(b_0=F_y(0,0)\ne0\), \(k_0=-b_0/a_0>0\).
For EVERY ambient coframe, connection and scalar variation,
\[
 \left.DS_\rho\right|_{R=q=0}
 =M\tau\int[a_0\,\delta(eR)+b_0\,\delta q]\,d^4z
 =M\tau a_0\,\delta\!\int(eR-k_0q)\,d^4z.               \tag{1}
\]
The external \(\rho\) cancels pointwise before integration by parts.
Neither \(\delta R\) nor \(\delta q\) is set to zero. Equation (1) is
equality of full first covectors at this background, not an off-shell
equality of nonlinear actions.

Since \(a_0,b_0\) are constants, its complete field equations are
\[
 \omega=\omega_{\rm LC},\qquad
 eG_{\mu\nu}=k_0\sum_A\partial_\mu\psi_A\partial_\nu\psi_A,\qquad
 \partial_\mu(g^{\mu\nu}\partial_\nu\psi_A)=0\quad(A=1,2). \tag{2}
\]
The independent Lorentz equation is constant-coefficient Palatini.
After it, the ten metric equations and the Lorentz identity give all
sixteen coframe rows. Thus (2) includes all 16+24+2 original continuum
rows. The material query is undensitized; no extra factor \(e\) is added.

## 2. Exact sign and scale match

The [constitutive owner, sections 1 and 3](../d0_primary_normal_source_recovery_2026-10-21/constitutive/CONSTITUTIVE_COMPOSITION.md)
uses \(F(x,y)=-\alpha\beta[h_\varphi(r(x,-y))-h_\varphi(r_0)]\).
Thus the weighted operand \(y=+\tau q/\rho\) has its minus sign INSIDE
the report; the covariant proof uses the raw operand \(Y=-\eta^2q\).
With raw derivatives \(r_x,r_Y>0\), this gives exactly
\[
 -\frac{b_0}{a_0}=\frac{r_Y(0,0)}{r_x(0,0)}
 =-\lambda_-(2^{-20})=k_0.
\]
For \(p=\varphi^{-1}\), \(z_0=2^{-20}\), set
\(L_0=4p^3\), \(Q=1-z_0L_0\),
\(R_{\rm det}=1-z_0L_0(1+p^6)\). The SAME finite-fugacity value is
\[
 k_0=2p^{-5}(R_{\rm det}/Q+p^6)
     =23.416406751884074972895582\ldots .
\]
The actual fixed \(\tau\) need not numerically equal the earlier
\(\eta^2\): at zero operands both common scales multiply the full first
covector and leave this ratio unchanged. Neither is fitted to the solution.

For any further supplied cap law \(F_N(x,y)=V_N(r(x,-y))+\text{constant}\),
\[
 a_N=V_N'(r_0)r_x(0,0),\qquad
 b_N=-V_N'(r_0)r_Y(0,0),\qquad -b_N/a_N=k_0.             \tag{3}
\]
The same conclusion holds for each finite cap with \(V_N'(r_0)\ne0\),
provided its actual parameters and \(a_N\) are spatially constant and its
baseline has zero field source. The actual cap-one owner supplies this
interface. For higher caps this remains a condition on the supplied
execution: heterogeneous occupation/compiler slopes cannot be discarded.
A pointwise common ratio with varying \(a_N(z)\) is insufficient; the
connection equation then contains derivatives of that coefficient.

## 3. The existing two-field witness meets every equation

Use the witness's chart \((b,u,v,w)\), with \(b>0\), constant \(d>0\), and put
\(E(b)=\exp(db^2/2)\):
\[
 ds^2=bE\,db^2-(E/b)\,du^2-b^2(dv^2+dw^2),\qquad
 \psi_1=b^2/2,\quad\psi_2=u,\quad\Lambda=d/b^2.
\]
Its proved identities are \(R=q=0\), \(G=\Lambda\sum_A d\psi_A^2\),
and conservation of both covariant currents. Use the same native chart
\[
 \frac{dt}{db}=\frac d{k_0}E(b),\qquad
 e_{\rm native}=\frac{k_0b^2}{d},\qquad e_{\rm native}\Lambda=k_0.
\]
Here \(t\) is a coordinate, distinct from the fixed query scale \(\tau\).
The two original currents obey (2):
\(g^{tt}\partial_t\psi_1=d/k_0\) and
\(g^{uu}\partial_u\psi_2=-b/E(b)\), whose divergences both vanish.
The metric and actual Levi-Civita connection satisfy the other rows.

Consequently this SAME native representative is stationary for \(S_\rho\)
for every prescribed smooth positive \(\rho(t,u,v,w)\), and for each cap
meeting (3)'s spatial-constancy conditions. Both scalar gradients remain
independent and active. Their opposite norms cancel only in total \(q\);
the source tensor has rank two, with
\(R_{\mu\nu}R^{\mu\nu}=2d^2b^{-2}e^{-db^2}>0\).
For this nonzero source, the metric equation requires exactly the ratio
\(k_0=-F_y(0,0)/F_x(0,0)\). No rank-one dust reduction or weighted Ward identity is
needed to prove this corollary.

## 4. Boundary and provenance

This transfers the existing explicit non-VSI solution to the actual
weighted continuum interface. It does not transfer the full off-null
fixed-measure stationary set, all-cap non-null rigidity, or any Hessian
equality. It constructs no exact finite-lattice representative and no
new field writer, compulsory Book valuation or independent upstream
stationary point. Arbitrary old collars need not survive the witness's
coordinate normalization; compact support or its transported collar is
required. The result concerns the full continuum field source at the
declared fixed interface.

Consumed immutable inputs, with no mathematical suite replay:

- Weighted theorem above at commit 401eafb2958e9d9626db833a25f02b35b3871c16,
  Git blob b72f96ec4e2e3d1413934532f5c018a68db93747; sections 2, 5 and 7.
- [Covariant proof](PROOF.md): Git blob
  fea122b537a847ac25b3ae0dbd3ae09c7353476e; SHA256
  e7a71e11ac1f8d6fd8fc49101aa231ccea4c5c23352f913a041d33995ebeccb2.
- [Witness](CROSSING_STREAMS.md): Git blob
  45329a4c9f556fcdf5321e90b2fc438bd2209a4a; SHA256
  c2cc72d1bcacbee21271c99549d70f86ee708439502211a1555d027e68b83326.
