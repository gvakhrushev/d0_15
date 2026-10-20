# Independent analytical review of the finite closed-record cut

20 October 2026. Reviewer: relational_history_bridge.
Read-only review of the two root-owned files; no mathematical checker,
old certificate suite or Lean build was run by this reviewer.

Reviewed inputs:

| File | SHA256 |
|---|---|
| finite_closed_record.md | 44e3f7844dc40c99c5218c7223fabc485e63fc251517c53f1d424dab222bfe28 |
| check_finite_closed_record.py | aa6d603038129139e0d944610d722123b776f01e52d72b3c8178636df4bd7b19 |

## Result

**The mathematical identities and stated source bounds pass analytical
review in their specified scopes.** The extra symmetric input/reference,
physical primitive admission and complete Book Info/work remain premises.
The review is not independent execution of the numerical certificate or
acceptance of the whole native/GR claim.

For a monomial of degree r−1, summing its coefficients in all partial
derivatives of the complete homogeneous polynomial h_r gives
sum_i(k_i+1)=d+r−1. Thus the exact identity
sum_i partial_i h_r=(d+r−1)h_(r−1) is correct, including zero eigenvalues.
Its matrix gradient is positive at F≥0, giving the claimed operator-norm
bound for every Hermitian first variation. Reindexing the differentiated
tail yields z E[(d+N)1_(N≥R)], with the stated N≥R rather than N>R.
The normalized-tail derivative includes the separate tau z E(d+N)
term. The moment-generating derivative gives
E[(d+N)a^N]≤M_a d/(1−aq), so equation (2), including its
1/[a(1−q)] contribution and denominator 1−e_R, follows. No eigenvalue
floor or differentiation of an unproved error estimate is used.

The physical count and source scales are consistent:
d=16·128·L^4=2048L^4, n=128L², m=2n, beta=m alpha=2p².
At z=2^(−20), nzd=L^6/4 and 8zd=L^4/64.
The proposed finite cut and log M_2 bound give
e_R≤1/(2L^(s+6)); multiplying the first-source bound by L^s leaves
O(z beta L^(−2)||delta Delta||). Its dependence on the actual Delta-jet
budget is explicitly retained. These are fixed-cut field derivatives,
not derivatives of an integer occupation cap selected as a function
of the field.

The same-carrier conditional insertion is
C_exit=nF+p beta Delta. It gives equation (7), and the stated fraction
of modes with mu≥4 follows from mean 8 and maximum 16. The lower
source coefficient 2 beta exp(−32 beta rho)L^6 in (10) follows from
f'_k=beta mu_k B_k^(m−1), R_k²≥1 and Tr mu=8d. The pressure coefficient
beta/[64(1−z)] is correct. The entropy derivative is
−x'_k log x_k/(1−x_k)²; concavity rho f'_k≤f_k and
x(−log x) increasing on [0,z] give the stated no-floor bound.
The conditional Cost-minus-this-entropy source is therefore eventually
Theta(L^6), whereas pressure and this entropy have O(L^4) sources.
This is a scoped test of the named candidate, not an exclusion of all
native Info laws.

Section 6 correctly keeps failed copies in the complete normalized
apparatus. The finite input normalization is
sum_(r≤R)z^r dim Sym^r(H). Its conditional all-return probability is
Z_R/Z_in,R. Each r-sector has one-copy marginal I/d, so the complete
additive known port price is
(E N_in,R/d)Tr C_op, without an independence assumption. For the
unrestricted generating ensemble its field-independent occupation gives
the Theta(L^6) price baseline but only the Theta(L^4) source (13).
The latter is not the conditional source (10). Tracing only the added
dual input reference leaves a full retained-output density whose
spectrum is preserved by the complete isometry, so its entropy is
field-independent for the stipulated fixed input. Pointer-only
entropy and complete Book Info are correctly kept separate.

The checker matches these analytical claims. Its exact polynomial
and shell-insertion sections precede bounded numerical flat-spectrum
controls; numerical checks are not presented as universal proofs.
The explicit __debug__ guard prevents running under Python -O with
silently disabled assertions.

## Preparation-domain clarification reviewed

The original reviewed proof hash was
4a05bedceafda2a5c2b8643df802ca123e539b0433ffbf5c1c33b8e87eae0d67.
The current pinned revision clarifies section 2: admitted variations
acting through A and its cut enter X; the symmetric input is fixed,
and an independent change in its coefficients has a separate source.
I read and accept this clarification. It changes no mathematical
formula and resolves the previously reported wording boundary.
No additional execution was requested or performed for this prose delta.
