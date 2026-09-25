# A4D crossed dressing and mismatch: what the matter letter sees

**Canonical task:** `EXP-A4D-CROSSED-DRESSING-MISMATCH-MATTER-ACTION`
**Start baseline:** `bd745be4e913e77665ba5c9e5ba08b4c968398d4`
**Research PR:** #137
**Terminal:** `DRESSING-MODULI-MATTER-VISIBILITY-CLASSIFIED`
**Checker:** `02_REGISTRY/research/certificates/a4d_crossed_dressing_mismatch_check.py`

This memo does not select a dressing. It classifies which already-known
moduli change the crossed letter \(F T_\kappa F^{-1}\).

## 0. Verdict

On the owned 16-state carrier, with \(T_b=I+N_b\) and \(N_b=C^\dagger(b)P_0\),

\[
\boxed{
F T_b F^{-1}=F' T_c F'^{-1}
\quad\Longleftrightarrow\quad
T_b=\operatorname{Ad}_{F^{-1}F'}T_c.
}
\tag{0.1}
\]

That is the iff. It splits the known moduli as follows.

| Modulus | After the crossed law |
|---|---|
| Distinct \(\kappa\), same \(F\) | Visible. \(F T_b F^{-1}=F T_c F^{-1}\) iff \(b=c\), because \(F\) is invertible and \(T\) is injective |
| Transverse skew with \([S,N_b]\neq 0\) | Visible. Same \(W\), same flat identity, different crossed letter already at order \(\varepsilon\) |
| Constant-potential spatial factor, site-independent \(b\) | Not visible. It commutes with \(N_b\), so it is isotropy of the crossed letter |
| A skew that commutes with \(N_b\) | Not visible. It is exactly the residual commutant in (0.1) |
| Resolution memory \(\Xi\) that changes the selected \(\kappa\) | Visible, by the first row. \(\Xi\) that does not change \(\kappa\) is invisible to this letter |

The adjoint action of a transverse orthogonal dressing does **not** stay inside
the family \(\{T_c\}\). It is not a relabeling of \(\kappa\).

## 1. Owned algebra used, and nothing else

From `A4DNilpotentAffineMatterLift.lean`:

- \(N_b N_c=0\);
- \(T_b T_c=T_{b+c}\), so \(T_b=T_c\) iff \(b=c\);
- \(\rho(L) T_b \rho(L)^{-1}=T_{Lb}\).

\(N_b\) sends the vacuum to \(\sum_i b_i\lvert\{i\}\rangle\) and kills every
other basis vector. The checker uses that matrix and no other convention.

No identification is made between \(T_b\) and a graded dressing, and none
between \(W_{\rm flux}\) and \(W^{\rm gr}\).

## 2. Same shadow, different crossed letter

Let \(F\) be the orthogonal matrix that rotates the vacuum and the
Role-\(A\) one-particle state by the rational angle \(3/5,4/5\):

\[
F=\begin{pmatrix}3/5&-4/5\\4/5&3/5\end{pmatrix}
\oplus I_{\text{rest}}.
\]

Then \(F^T F=I\), so

\[
W(F)=F^{-T}F^{-1}=I=W(I).
\]

Both dressings are the identity at first order on the exact pure-gauge
chart if this \(F\) is used only as a transverse increment (its generator
is skew, so it does not change \(H\)). The crossed letters differ:

\[
F T_{e_A} F^{-1}\neq T_{e_A}.
\]

The infinitesimal form is the same fact. For

\[
S=\lvert 0\rangle\langle A\rvert-\lvert A\rangle\langle 0\rvert,
\qquad S^T=-S,
\]

the checker computes \([S,N_{e_A}]\neq 0\). Therefore

\[
(I+\varepsilon S)T_b(I+\varepsilon S)^{-1}
=
T_b+\varepsilon[S,N_b]+O(\varepsilon^2)
\]

and the two first derivatives in the dressing direction disagree. Same
\(W\), same \(DW_0\), different matter letter.

## 3. The adjoint leaves the translation family

\(T_c-I=N_c\) has vanishing vacuum row: \(N_c\) never returns a state to
the vacuum. For the \(F\) of §2,

\[
F T_{e_A} F^{-1}-I
\]

has a nonzero vacuum row. Hence it equals \(T_c\) for no \(c\), including
\(c=0\). A transverse dressing produces a matter operator outside the
nilpotent translation family. Quotienting that difference as "the same
\(\kappa\) up to frame" is false: the owned frame law \(\rho(L)\) stays
inside the family, and this \(F\) does not.

## 4. What does descend

Let \(R\) be the forward cycle on an auxiliary \(\mathbb Z/3\), acting on a
spatial factor, and let \(N_b\) act on the Fock factor with \(b\)
site-independent. Then

\[
(R\otimes I)(I\otimes N_b)=(I\otimes N_b)(R\otimes I),
\]

so

\[
(F R) T_b (F R)^{-1}=F T_b F^{-1}
\]

whenever \(R\) commutes with \(T_b\). The constant-potential isotropy of the
pure-gauge dressing is this kind of spatial factor on the scalar block. For
site-independent \(b\) it is invisible to the crossed letter. The checker
records the commutation. It does not extend the claim to a site-dependent
\(b\): that case is not computed here, and the torsor identity in the
dressing memo is spatial.

A skew generator that commutes with \(N_b\) is likewise invisible. The
visibility statement is exactly the failure of that commutation, not a claim
that every skew is visible. The witness of §2 shows the visible set is
nonempty, so transverse skew cannot be quotiented as a whole.

## 5. Resolution memory

PR #130 already shows that distinct selected clusters give distinct
\(T_\kappa\), and that one invertible \(F\) cannot identify them. Section 2's
computation is the same fact at the level of the crossed letter: for any
invertible \(F\),

\[
F T_b F^{-1}=F T_c F^{-1}\iff b=c.
\]

So a resolution memory \(\Xi\) is visible to the crossed action precisely
when the two memories select different \(\kappa\). If they select the same
\(\kappa\), (0.1) says the crossed letters agree for the same \(F\). No
finer invariant of \(\Xi\) is claimed.

## 6. Composition

The finite product of two crossed letters at the same dressing is

\[
(F T_b F^{-1})(F T_c F^{-1})
=
F T_b T_c F^{-1}
=
F T_{b+c} F^{-1}.
\]

Nilpotence is what makes this a homomorphism in \(\kappa\). It is not a
semidirect product with the dressing: the dressing is outer, and §3 shows
the conjugate need not be a translation. The semidirect law that *is* owned
is the frame one, \(\rho(L) T_b \rho(L)^{-1}=T_{Lb}\), and it is a different
action from the transverse orthogonal witness.

Pull order is the Lean order: operators compose on the right of the state.
No other convention is used.

## 7. Hostile controls

| Control | Result |
|---|---|
| Flat, \(b=0\) | \(T_0=I\), and every dressing conjugates it to \(I\). The modulus is invisible when there is no mismatch |
| Pure shift / translation gauge | site-independent \(b\) commutes with the spatial cycle, so the torsor descends; the letter still depends on \(b\) |
| Two \(\kappa\) | \(T_b\neq T_c\) and \(F T_b F^{-1}\neq F T_c F^{-1}\) |
| Equal \(W\), distinct skew | §2 witness, rational \(3/5,4/5\) |
| L=2 / L=3 / Nyquist / corner / harmonic | not inputs of \(T_b\). They are not deleted; they do not appear in this letter, so they cannot be used to cancel the commutator |
| #130 rank jump | inherited: a jump in the selected \(\kappa\) is a jump in \(T_\kappa\), and §5 says the dressing does not hide it |
| Nontrivial holonomy | not an argument of \(N_b\). No claim that holonomy descends |

## 8. Not claimed

No preferred dressing, no Hessian, no stress, no Einstein equation, no
continuum limit, no physical time, no golden refinement. The commutant of
\(N_b\) inside all invertible operators is not computed beyond the two
witnesses: one visible skew, and the spatial factor that commutes.

## 9. Checker

`python3 02_REGISTRY/research/certificates/a4d_crossed_dressing_mismatch_check.py`

## 10. Correction of the fused joint letter

A proposed single product

\[
\ell^{+}=F\,T_{R}\,\rho(L)\,U\,F^{-1}
\]

does not specialize to the owned pure-gauge letter.

The owned letter on the exact chart is \(F U F^{-1}\). There is no
\(\rho(L)\) in it. Take the rigid point \(T_R=I\) and \(F=I\), and let
\(\rho\) swap Role \(A\) with Role \(B\) on the Fock factor. This
\(\rho\) commutes with a spatial cycle \(U\) because the two factors are
different, and \(\rho\neq I\). The fused product collapses to
\(\rho U\), while the owned letter collapses to \(U\). They differ.
The checker records this as `fused_formula_fails_rigid_limit`.

The frame law that is actually owned is the separate identity
\(\rho(L) T_b \rho(L)^{-1}=T_{Lb}\). It changes the translation vector.
It is not a third factor standing between \(T_R\) and \(U\).

The product that does survive the rigid limit is

\[
\boxed{
\ell(F,\kappa)=F\,T_{\kappa}\,U\,F^{-1}.
}
\tag{10.1}
\]

At \(\kappa=0\), \(T_0=I\), so \(\ell(F,0)=F U F^{-1}\). That is the
owned letter, including its right constant-potential isotropy: if \(R\)
commutes with both \(T_0\) and \(U\), the class \([c]\) cancels.

Two readings that this formula does not support:

- \(F=W\). An orthogonal dressing has \(W(F)=I\) and \(F\neq I\). The
  collapsed sector \(c=0\), \(\Xi\) trivial, \(\kappa=0\) still shows
  the pair \((FUF^{-1},\,W)\), not one object called both \(F\) and \(W\).
- \(\rho(L)\) inside the same conjugate. Removed by the witness above.

\(\Xi\) enters (10.1) only by choosing \(\kappa\). It is not given a
new transport law here. Site-dependent \(\kappa\) may fail to commute
with \(U\); (10.1) fixes the order \(T\) then \(U\) and does not claim
the opposite order is equal.

The order in (10.1) is the composition \((F T_\kappa F^{-1})(F U F^{-1})\).
It is not optional when \(\kappa\) varies by site. On a \(\mathbb Z/3\)
cycle, a site-independent \(N_b\) commutes with the cycle, so the two
orders agree. A bump \(b=e_A\) on one site and \(0\) on the others does
not: \(T U\neq U T\). The checker records this as
`sitewise_kappa_order_is_visible`. Reversing the product is a different
letter, not a rewriting of (10.1).


## 11. Exact normalizer of the nilpotent translation family

The previous sections used witnesses inside and outside the commutant.  The
whole normalizer can in fact be classified.

Let
\[
\mathcal E=\mathbb R\Omega\oplus V_1\oplus Z,
\]
where \(\Omega\) is the Fock vacuum, \(V_1\cong V\) is the one-particle
subspace, and \(Z\) is the sum of degrees \(2,3,4\).  Let
\[
\varepsilon=\langle\Omega|,
\qquad
j:V\overset{\sim}{\longrightarrow}V_1.
\]
Then
\[
N_b=j(b)\varepsilon,
\qquad
T_b=I+N_b.
\]

For any \(R\in GL(\mathcal E)\),
\[
\boxed{
R N_cR^{-1}
=
(Rj(c))(\varepsilon R^{-1}).
}
\tag{11.1}
\]

Define
\[
\mathcal T=\{T_b:b\in V\}.
\]

### Theorem — full normalizer

\[
\boxed{
R\mathcal T R^{-1}=\mathcal T
}
\tag{11.2}
\]
iff both

\[
\boxed{
R(\ker\varepsilon)=\ker\varepsilon
}
\tag{11.3}
\]
and
\[
\boxed{
R(V_1)=V_1.
}
\tag{11.4}
\]

**Necessity.**
For every nonzero \(c\), the right side of (11.1) must be a member of
\(\{j(b)\varepsilon\}\).  All nonzero members of that family have the same
kernel \(\ker\varepsilon\), so
\[
\ker(\varepsilon R^{-1})=\ker\varepsilon,
\]
which is (11.3).  Their ranges run through every line in \(V_1\), hence
\(R(V_1)=V_1\).

**Sufficiency.**
Equation (11.3) gives one scalar
\[
a_R\ne0
\]
such that
\[
\varepsilon R^{-1}=a_R^{-1}\varepsilon.
\]
Equation (11.4) gives
\[
C_R:=R|_{V_1}\in GL(V_1).
\]
Then
\[
R N_cR^{-1}
=
j(a_R^{-1}C_Rc)\varepsilon,
\]
so
\[
\boxed{
R T_cR^{-1}=T_{\alpha_R(c)},
\qquad
\alpha_R=a_R^{-1}C_R.
}
\tag{11.5}
\]

Thus the normalizer does not merely preserve the translation family; it acts
on the physical mismatch vector by the explicit invertible map
\[
\alpha_R\in GL(V).
\]

In blocks relative to
\[
\mathbb R\Omega\oplus V_1\oplus Z,
\]
the normalizer consists exactly of matrices of the form
\[
\boxed{
R=
\begin{pmatrix}
a&0&0\\
u&C&P\\
w&0&D
\end{pmatrix},
\qquad
a\ne0,\quad
C\in GL(V_1),\quad
D\in GL(Z).
}
\tag{11.6}
\]
The entries \(u,w,P\) are unrestricted subject only to invertibility of the
displayed diagonal blocks.

The induced action on \(\kappa\) ignores all three of those off-diagonal
blocks:
\[
\alpha_R=a^{-1}C.
\]

---

## 12. Exact commutant

The full commutant is now immediate.

\[
\boxed{
RT_b=T_bR\quad\forall b
}
\tag{12.1}
\]
iff \(R\) has the normalizer form (11.6) and
\[
\boxed{
C=aI_{V_1}.
}
\tag{12.2}
\]

Indeed, inside the normalizer,
\[
RT_bR^{-1}=T_b\quad\forall b
\iff
\alpha_R=I
\iff
a^{-1}C=I.
\]

This includes the already-found constant-potential spatial isotropy after
tensoring with the archive factor: it acts trivially on the Fock
\(\Omega\oplus V_1\) block and therefore lies in the commutant whenever the
site field \(b\) is invariant under that spatial action.

It also shows why “same \(W\)” is too weak.  Orthogonality of \(R\) does not
imply (11.3) or (11.4), and hence does not imply membership in the normalizer,
let alone the commutant.

---

## 13. Pointwise equality is weaker than global normalization

For one supplied pair \(b,c\), equality of two crossed letters does not
require \(R\) to normalize every \(T_d\).

For \(c\ne0\),
\[
\boxed{
R T_cR^{-1}=T_b
}
\tag{13.1}
\]
iff there exists \(\lambda\ne0\) such that
\[
\boxed{
\varepsilon R^{-1}=\lambda\varepsilon,
\qquad
Rj(c)=\lambda^{-1}j(b).
}
\tag{13.2}
\]

This is just uniqueness of a nonzero rank-one factorization:
\[
(Rj(c))(\varepsilon R^{-1})=j(b)\varepsilon.
\]

For \(c=0\),
\[
RT_0R^{-1}=I=T_b
\iff
b=0.
\tag{13.3}
\]

The distinction matters.  A dressing may accidentally map one selected
\(\kappa\) back into the translation family while sending another one outside
it.  The checker includes exactly such an exceptional witness.

---

## 14. Complete iff for two dressing/resolution pairs

Let two admissible pairs select
\[
(F_1,\Xi_1)\mapsto b=\kappa(\Xi_1),
\qquad
(F_2,\Xi_2)\mapsto c=\kappa(\Xi_2),
\]
and put
\[
\boxed{
R=F_1^{-1}F_2.
}
\tag{14.1}
\]

Then
\[
\begin{aligned}
F_1T_bF_1^{-1}
&=
F_2T_cF_2^{-1}
\\
&\Longleftrightarrow
T_b
=
RT_cR^{-1}.
\end{aligned}
\]

Therefore the **pointwise complete criterion** is:

- if \(b=c=0\), the crossed letters agree for arbitrary \(R\);
- if exactly one of \(b,c\) is zero, they do not agree;
- if both are nonzero, they agree iff (13.2) holds.

If the relative dressing belongs to the full normalizer, this reduces to the
clean linear form
\[
\boxed{
F_1T_bF_1^{-1}=F_2T_cF_2^{-1}
\iff
b=\alpha_R(c).
}
\tag{14.2}
\]

Thus resolution memory is visible exactly modulo the induced normalizer action
on its selected mismatch.  For the same dressing \(R=I\), this becomes
\(b=c\), recovering the earlier injectivity statement.

For equality of the **whole mismatch action family**, rather than one selected
vector, \(R\) must lie in the normalizer.  The exceptional pointwise case of
§13 is not enough.

---

## 15. Exact composition across different dressings/backgrounds

Take
\[
L_1=F_1T_bF_1^{-1},
\qquad
L_2=F_2T_cF_2^{-1},
\]
and again
\[
R=F_1^{-1}F_2.
\]

Without any assumption,
\[
\boxed{
L_1L_2
=
F_1\bigl(T_b\,R T_cR^{-1}\bigr)F_1^{-1}.
}
\tag{15.1}
\]

This is the exact pull-order formula.

If
\[
R\in N_{GL(\mathcal E)}(\mathcal T),
\]
then (11.5) and nilpotence give
\[
\begin{aligned}
L_1L_2
&=
F_1T_bT_{\alpha_R(c)}F_1^{-1}
\\
&=
\boxed{
F_1T_{\,b+\alpha_R(c)}F_1^{-1}.
}
\end{aligned}
\tag{15.2}
\]

Hence the closed crossed sector is the exact semidirect product
\[
\boxed{
N(\mathcal T)\ltimes_{\alpha}V,
}
\tag{15.3}
\]
with
\[
(R,b)\cdot(S,c)
=
(RS,\ b+\alpha_R(c))
\]
after choosing the corresponding common-reference convention.

The inverse law is
\[
\boxed{
(R,b)^{-1}
=
\left(R^{-1},-\alpha_{R^{-1}}(b)\right).
}
\tag{15.4}
\]

Outside the normalizer, (15.1) remains a perfectly well-defined operator
product, but it does not close in the nilpotent translation family.  That is
the exact boundary between “crossed mismatch action” and a larger operator
envelope.

---

## 16. Site-dependent extension and the old constant-isotropy witness

On the archive carrier, a spatial permutation/shift \(U\) acts on a field
\[
b:X\to V
\]
by pullback.  Conjugation sends the sitewise nilpotent family to
\[
b\mapsto U\cdot b.
\]

Therefore a constant-potential spatial cycle is in the stabilizer precisely
when
\[
U\cdot b=b.
\]

For site-independent \(b\), this holds and the torsor descends, reproducing
§4.  For the one-site bump in §10,
\[
U\cdot b\ne b,
\]
so the ordering remains visible.

Thus the previous positive and negative spatial controls are the sitewise
version of the same normalizer/stabilizer theorem, not unrelated examples.

---

## 17. Final classification after normalizer pressure

The earlier iff
\[
F T_bF^{-1}=F'T_cF'^{-1}
\iff
T_b=\operatorname{Ad}_{F^{-1}F'}T_c
\]
is now resolved into explicit finite data.

The complete classification is:

1. the global normalizer is exactly the simultaneous stabilizer of the vacuum
   hyperplane \(\ker\varepsilon\) and the one-particle subspace \(V_1\);
2. its induced action on mismatch is
   \[
   \alpha_R=a_R^{-1}R|_{V_1};
   \]
3. its commutant is exactly the subfamily with
   \[
   R|_{V_1}=a_RI;
   \]
4. one selected nonzero mismatch only needs the weaker rank-one criterion
   (13.2);
5. two pairs \((F,\Xi)\) induce the same crossed letter exactly by §14;
6. different-background composition closes in the translation family exactly
   when the relative dressing lies in the normalizer, with law (15.2);
7. outside that normalizer the crossed operator is still defined but exits
   \(\{T_b\}\).

This completes the requested normalizer/commutant and exact-composition
classification without selecting a preferred dressing.

The terminal remains
\[
\boxed{\texttt{DRESSING-MODULI-MATTER-VISIBILITY-CLASSIFIED}},
\]
now with a literal normalizer theorem rather than only visible/invisible
witnesses.


---

## 18. Ready lifecycle audit

The normalizer/commutant pressure is closed.

Final research surface:

- full normalizer of \(\{T_b\}\);
- full commutant;
- pointwise exceptional equality separated from family normalization;
- exact iff for two \((F,\Xi)\) pairs;
- exact different-background composition and inverse in the normalizer sector;
- site-dependent stabilizer control;
- exact rational checker extended with all four new hostile fixtures.

The canonical EXPENSIVE task is self-retired against the fresh worker queue.
No new claim registration or Lean source is added here.

Lifecycle: REVIEW.  Do not self-merge.
