# D0 v16 seam purification section map — structural no-go

**Task:** EXP-D0-V16-SEAM-PURIFICATION-SECTION-MAP  
**Class:** EXPENSIVE  
**Status:** exact type/dimensional no-go  
**Terminal:** D0-V16-UNADORNED-REMNANT-LIFETIME-SECTION-NOGO  
**Execution baseline:** 0bf35cff12a6bd90651e8786f73fb9e098c0a686  
**Review contract baseline:** 0bf35cff12a6bd90651e8786f73fb9e098c0a686

## 1. Question

The requested unaugmented section is

\[
\mathcal S:
(\operatorname{rank}P,\Lambda_{\rm act},\varphi,R_\ast,\text{history/window data})
\longrightarrow (M_0,\tau_C).
\]

The target is not to manufacture quantities with the dimensions of mass and time. The target is a typed, non-tautological selector from the finite D0 seam/history object to the external remnant mass coordinate and Bondi purification time.

The result of this task is a no-go for the declared unaugmented source object. The obstruction is not lack of a second dimensional scale. It is absence of two dimensionless semantic morphisms.

## 2. Consumed owners

The construction consumes the merged channel owners rather than reopening them.

1. D0_V16_ONE_TICK_BALANCE_TWO_SPLIT_OWNER:
   a fixed finite split and one global unitary tick obey
   \[
   \operatorname{Tr}F_N=\operatorname{Tr}F_Q^{\rm emit}.
   \]
   Therefore a remnant phase sign cannot be read from one unrestricted tick.

2. D0_V16_MOVING_SPLIT_CHANNEL_SIGN:
   a declared two-point history has an exact finite nonzero sign,
   \[
   \sigma^{\rm budget}_{n,n'}
   =\sigma^{\rm density}_{n,n'}
   =\frac{1183}{5475},
   \]
   while both individual ticks remain balanced. The same owner explicitly does not identify this ratio with Bondi \(k(u)\).

These results close the finite channel-history carrier needed by this task. They do not provide an external clock or an absolute mass coordinate.

## 3. Metrological ledger

The Book 03 single-section theorem gives one dimensional anchor,

\[
\Lambda_{\rm act}=38m_ec^2,
\]

with

\[
\tau_0=\frac{h}{\Lambda_{\rm act}},
\qquad
\ell_0=c\tau_0,
\qquad
m_{\rm act}:=\frac{\Lambda_{\rm act}}{c^2}.
\]

All declared task inputs other than \(\Lambda_{\rm act}\) are dimensionless:

- \(\operatorname{rank}P\): finite integer;
- \(\varphi\): algebraic dimensionless invariant;
- \(R_\ast\): dimensionless capacity ratio;
- finite projectors, trace ratios and history/window signs: dimensionless.

Book 07 may additionally export the already-owned dimensionless depth \(D_L\),

\[
\ell_P^{D0}=\frac{\ell_0}{D_L},
\qquad
G_N^{D0}=\frac{c^3(\ell_P^{D0})^2}{\hbar}.
\]

Granting this entire gravity metrology chain does not add an independent scale. It also does not select a particular remnant state.

## 4. Internal freeze of \(R_\ast\)

The no-go is not allowed to hide behind an unfrozen capacity parameter.

The concrete Lean owner D0.Synthesis.SceneTraceHeatCapacity supplies a proper saturated co-vertex region on the frozen \(K(9,11,13)\) scene:

\[
\operatorname{BoundaryCutWeight}(S_{\rm cv})=20,
\]

hence

\[
C(\partial S_{\rm cv})=\frac{20}{4}=5.
\]

The region is the complement of one vertex in the 33-vertex scene, so

\[
|S_{\rm cv}|=32.
\]

Freeze the capacity-density ratio

\[
\boxed{
R_\ast^{\rm cv}
:=
\frac{C(\partial S_{\rm cv})}{|S_{\rm cv}|}
=
\frac{5}{32}.
}
\]

This is entirely internal: no PBH mass, cosmological age, survey value, LIGO event or laboratory datum enters. It is a declared finite saturated-seam witness, not a fitted remnant parameter.

The corresponding internal depth is therefore

\[
\boxed{
n_\ast^{\rm cv}
=
\frac{\log(1+5/32)}{\log\varphi}
=
\frac{\log(37/32)}{\log\varphi}.
}
\]

Nothing in the no-go below depends on choosing a different \(R_\ast\): the point is stronger. Even after one internal \(R_\ast\) is frozen explicitly, the absolute mass selector and Bondi clock remain absent.

## 5. Rank-one factorization lemma

Let

\[
x=(\operatorname{rank}P,\varphi,R_\ast,\text{history/window data},D_L,\ldots)
\]

denote the dimensionless source data.

Under the existing rank-one metrology, every scale-covariant mass/time section must have the form

\[
\boxed{
M_0=m_{\rm act}\,\mu(x)
=\frac{\Lambda_{\rm act}}{c^2}\,\mu(x)
}
\]

and

\[
\boxed{
\tau_C=\tau_0\,b(x)
=\frac{h}{\Lambda_{\rm act}}\,b(x)
}
\]

for dimensionless functions \(\mu,b\).

This is a useful positive theorem: a future section cannot introduce another dimensional scale. But dimensional covariance determines only the powers of \(\Lambda_{\rm act}\); it does not determine the dimensionless functions \(\mu\) and \(b\).

### Hostile non-uniqueness

If \((\mu,b)\) satisfies only the declared metrological typing and positivity constraints, then for any positive nontrivial internal invariant \(q(x)\),

\[
(\mu,b)\mapsto(q\mu,b)
\]

and

\[
(\mu,b)\mapsto(\mu,qb)
\]

have exactly the same dimensional covariance.

Examples of available dimensionless multipliers are \(\varphi\), \(1+R_\ast\), or a positive finite rank. Therefore the single-section theorem fixes unit powers but cannot, by itself, select the semantic section.

The certificate gives an exact finite witness of this non-uniqueness.

## 6. Time side: internal depth is not Bondi time

The synthesis already owns the internal capacity depth

\[
n_\ast=\frac{\log(1+R_\ast)}{\log\varphi},
\qquad
\tau_\ast=n_\ast\tau_0.
\]

This closes an internal tick-time object. It does not close

\[
\tau_\ast=\tau_C.
\]

The reason is typed, not numerical. The two-split rule distinguishes the internal/medium history from the asymptotic observer frame. Bondi retarded time belongs to the observer completion at null infinity. No current D0 owner supplies a functor

\[
\mathcal B_{\mathscr I^+}:
\text{FiniteObserverHistory}\longrightarrow
\text{BondiRetardedTime}.
\]

Consequently \(n_\ast\tau_0\) cannot be promoted to the Bianchi purification time by matching units.

A required future dimensionless clock selector would be

\[
b_{\rm Bondi}(x)>0,
\qquad
\tau_C=\tau_0 b_{\rm Bondi}(x).
\]

It may later be related to \(n_\ast\), but that relation is exactly the missing theorem.

## 7. Mass side: boundary capacity is not closure-density mass

Book 07 keeps two distinct objects.

The horizon capacity is a boundary-cut object,

\[
C(\partial S)=\frac{\operatorname{BoundaryCutWeight}(S)}{4},
\]

equivalently \(C_\partial=A_{D0}/4\) when \(A_{D0}\) is measured in D0/Planck area quanta.

Core mass, by contrast, is typed as cycle-closure density,

\[
\varrho_k(x)
=
\frac{\sum_{P\in\mathrm{Cycles}(x)}\tau(P)^{-1}}
{\operatorname{Vol}(U_k)}.
\]

No current theorem identifies

\[
\operatorname{rank}P,\quad R_\ast,\quad
C(\partial S),\quad A_{D0}
\]

with a unique value of the closure-density mass coordinate.

This distinction is visible in the empirical horizon passport as well: Book 07 §07.48 takes \(M_1,M_2,\chi_{\rm eff}\) as external passport inputs and predicts a dimensionless mass-defect fraction. It does not generate the absolute masses.

Therefore the missing mass selector is a dimensionless morphism

\[
\mu_{\rm BH}:
\text{SeamHistory}\longrightarrow\mathbb R_{>0}
\]

with a theorem identifying its output with the closure-density / black-hole mass coordinate. Only then would

\[
M_0=\frac{\Lambda_{\rm act}}{c^2}\mu_{\rm BH}
\]

be a typed D0 mass section.

## 8. Why the existing Planck/Newton bridge does not close the gap

Grant the full existing chain

\[
D_L\to\ell_P^{D0}\to G_N^{D0}.
\]

This supplies calibrated gravity units from the same action section. It still does not choose an object-specific horizon radius, area, or closure density.

A continuum construction such as

\[
A_{\rm phys}
\to r_H
\to M_0
\]

would additionally require:

1. a finite selector from the declared seam/history state to a particular boundary area \(A_{D0}\);
2. a shape/completion theorem converting that area into a continuum horizon radius;
3. a black-hole mass identification in that completion.

Those are semantic morphisms. They are not a second dimensional anchor, but they are new structure not contained in the declared source tuple.

Thus "D0 has \(\ell_P\) and \(G_N\)" does not imply "this seam has a unique \(M_0\)."

## 9. Why the external lifetime law cannot be used as the selector

The external remnant relation

\[
\tau_C\ge \frac{4}{\alpha}
\frac{M_0^4}{\hbar^{3/2}}
\]

is an external comparison law in its own conventions. It is a predicate on \((M_0,\tau_C)\) after the section exists.

Solving that formula for \(M_0\) after setting \(\tau_C:=\tau_\ast\) would reverse the dependency:

\[
\text{external remnant law}
\longrightarrow
M_0.
\]

That makes the external envelope define the D0 section and violates the task's hostile-control rule. The metastable exponential branch is even more explicit: its additional lifetime parameter belongs to the external envelope, not the D0 source object.

Therefore Bianchi may test a completed section but cannot choose it.

## 10. Structural no-go theorem

Define the unaugmented source type

\[
X_{\rm D0}:=
(\operatorname{rank}P,\Lambda_{\rm act},
\varphi,R_\ast,\text{finite history/window data})
\]

together with any already-owned dimensionless gravity invariants such as \(D_L\).

Then:

1. rank-one metrology canonically supplies the mass unit \(m_{\rm act}\) and time unit \(\tau_0\);
2. the finite channel owners supply channel budgets and history signs;
3. the seam owner supplies boundary capacity;
4. none supplies a morphism from seam/history to closure-density black-hole mass;
5. none supplies a morphism from finite observer history to Bondi retarded time;
6. dimensional covariance leaves arbitrary dimensionless factors in both outputs.

Hence there is no **owned, unique, non-tautological** section

\[
\mathcal S:X_{\rm D0}\to(M_0,\tau_C)
\]

in the current unaugmented object set.

\[
\boxed{\texttt{D0-V16-UNADORNED-REMNANT-LIFETIME-SECTION-NOGO}}
\]

This is a structural no-go for the current source type, not a claim that no extension can ever close the bridge.

## 11. Minimal augmentation that would reopen the positive branch

No second scale is required. The smallest missing structure is two dimensionless typed morphisms:

\[
\mu_{\rm BH}:
\text{SeamHistory}\to\mathbb R_{>0},
\]

\[
b_{\rm Bondi}:
\text{FiniteObserverHistory}\to\mathbb R_{>0}.
\]

Then the only scale-compatible section is

\[
\boxed{
\mathcal S(x)=
\left(
\frac{\Lambda_{\rm act}}{c^2}\mu_{\rm BH}(x),
\frac{h}{\Lambda_{\rm act}}b_{\rm Bondi}(x)
\right).
}
\]

The future proof obligation is therefore sharply smaller than "derive a lifetime": construct and uniquely own these two dimensionless morphisms, including the observer/medium split functor.

## 12. Status consequences

- ONE-TICK-BALANCE-LEMMA: owned by merged exact certificate.
- CHANNEL-SIGN-ON-HISTORY: owned by merged exact finite construction.
- A/B/C remnant dictionary: bridge only.
- \(\tau_\ast=n_\ast\tau_0\): internal definition only.
- Remnant lifetime: remains PASSPORT.
- No PBH, universe-age, H0, DESI, LIGO or lab datum is used to select \(R_\ast\), \(\mu_{\rm BH}\), or \(b_{\rm Bondi}\).
- D0-METRO-002 is not weakened: the no-go respects and uses its one-scale theorem.

Certificate:

02_REGISTRY/research/certificates/d0_v16_seam_purification_section_nogo_check.py
