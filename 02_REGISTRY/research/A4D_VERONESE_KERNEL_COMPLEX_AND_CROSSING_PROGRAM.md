# A4D — Veronese kernel complex and divisor/crossing program

Status: CONTROL synthesis. Theorem and proof obligations are separated below.

## Owned algebraic core

Use merged #270:
\[
d_r=z_r^{-1}-1,\quad C(d)=H_{AQ}(d),\quad q_0(d)=\operatorname{vec}_{sym}(dd^T).
\]
On its stated nontrivial-character carrier #270 owns
\[
\operatorname{rank}C(d)=9,\qquad \ker C(d)=\operatorname{span}\{q_0(d)\},
\qquad (D_jC)q_0=-C(D_jq_0).
\]

The coefficientwise strengthening is #281/#282:
\[
C(d)=\sum_{r=0}^3d_rC_r,
\]
with all 20 cubic monomial coefficients of \(C(d)q_0(d)\) required to vanish
as 24-vectors (480 exact scalar checks). Until #282 merges, its ledger is
evidence under review, not a new owner.

Define
\[
P_d:\mathbb C\to\operatorname{Sym}^2\mathbb C^4,\qquad P_d(f)=f\,dd^T.
\]
Then the owned null identity is the complex
\[
\mathbb C\xrightarrow{P_d}\operatorname{Sym}^2\mathbb C^4
\xrightarrow{C(d)}\mathbb C^{24},\qquad C(d)P_d=0.
\]
This replaces the old mechanism-level interpretation based on nine sampled
orbit points or the retired rank-sum 11.

## Correct obstruction object

For \(d\neq0\), define
\[
\mathcal H_C(d)=\ker C(d)/\operatorname{im}P_d.
\]
Where #270's rank/kernel theorem applies, \(\mathcal H_C(d)=0\). Thus the
moving germ \(q_0\) is in the image of the first arrow, not a stress class.

PR #278 fixes the carrier interpretation independently. The historical raw
\(\sqrt{8/5}\) residual is a cross-character forcing result. On the
registered physical character the actual moving-germ forcing satisfies
\[
w_j(\chi)=-H_{AQ}(\chi)D_jq_0(\chi)
\]
and has zero physical obstruction class. Frozen/cross-carrier detune
residuals are therefore not metric stress.

## Mandatory open boundary

Do NOT infer that one equation \(d_r=0\) automatically implies
\(\dim\ker C(d)>1\). The exact determinantal stratification of the polynomial
family \(C(d)\) is not yet owned.

The proposed role divisor
\[
\Delta_{\rm role}=\bigcup_r\{d_r=0\}=\bigcup_r\{z_r=1\}
\]
is a candidate crossing locus, not yet the proven rank-jump locus of \(C(d)\).

Likewise, #279's 505 solders are exact defects of a varying-solder joint
symbol \(J=[H;C]\), not additional classes of \(\mathcal H_C(d)\) without a
transfer theorem. #240's \(q_{11}\) shear is a nonzero joint response witness,
not yet a proved divisor-homology generator.

## Three sectors

### Generic metric-null chamber
Where #270 applies,
\[
\ker C(d)=\operatorname{im}P_d,\qquad \mathcal H_C(d)=0.
\]
A stronger Zariski-open statement specifically on \(\prod_rd_r\neq0\) may be
promoted only after the polynomial rank-stratification theorem.

Target envelope theorem: along a connection-stationary sheet whose registered
carrier remains in one exact metric-null chamber, metric response is
independent of uniqueness of the connection lift, modulo separately
identified connection-only cokernel classes. This is still a proof obligation.

### Candidate role divisor / joint defects
Compute determinantal geometry of \(C(d)\) first: rank-drop ideal/locus, then
classify \(\mathcal H_C(d)\) on each irreducible stratum. Only after that may
#240 \(q_{11}\) or #279 defects be identified with extra metric homology.
Rank stratification comes before transfer; finite orbit census is not a
substitute.

### Connection-only sector
The quarter-wave/Y/N0 lane is not metric homology of \(C(d)\). #275 reduces
its residual seam to the realification of connection invisible \(N_0\) owned
by #260. Treat it as a cokernel/joint-connection sector of an extended complex
involving \(A\), not as an element of \(\ker C/\operatorname{im}P\).

## Crossing replaces census as the stress question

For
\[
Q_\varepsilon=\eta+\varepsilon\operatorname{Re}(q_0(z)e^{ikx}),
\]
\(Cq_0=0\) and transport alone do NOT prove \(E_Q=-\tfrac12G\) on a nonlinear
stationary sheet. Stress is a separate Euler-response statement.

Target crossing theorem:
1. identify exact rank/homology strata of \(C(d)\);
2. continue a fixed-source connection-stationary sheet inside one stratum;
3. prove envelope response there without assuming unique \(K\);
4. identify first possible response change with crossing a proven
   homology/rank locus or entering the separately owned connection-only
   cokernel sector.

Until certified, do not say FUGU is stress, #279 classifies the divisor, or
Einstein response follows globally.

## Exact proof obligations

### A. Coefficientwise Veronese identity — executing as #282
Certify \(C_r\), all 20 cubic monomials of
\(C(d)\operatorname{vec}_{sym}(dd^T)\), and Laurent substitution
\(d_r=z_r^{-1}-1\). Do not enlarge #282 into divisor/stress work.

### B. Determinantal rank/homology stratification — next bounded theorem
Over an exact polynomial/rational field:
- determine generic rank of \(C(d)\);
- certify the rank-drop locus;
- decide whether \(\bigcup\{d_r=0\}\) equals, contains, intersects, or is
  independent of that locus;
- on every stratum report \(\dim\ker C\), \(\dim\mathcal H_C\), and explicit
  generators modulo \(dd^T\);
- no solder census, floating SVD, stress, or nonlinear-response inference.

### C. Joint-defect transfer
Only after B, test whether #240 \(q_{11}\) and representative exact #279
defects map to new homology generators under a precisely owned carrier map.
A failed transfer is informative and must not be repaired by renaming carriers.

### D. Chamber envelope theorem
Using exactness \(\mathcal H_C=0\) on a certified chamber, prove the
stationary-sheet envelope statement with fixed source and explicit connection
continuation. State which connection-only cokernel directions remain outside.

### E. Crossing theorem
Prove or refute that response differing from the designated sheet requires
crossing the certified metric rank/homology locus or entering the separate
connection-only sector. This can replace the old UV/IR and orbit-census
narrative only after proof.

## Existing execution map

- #270: algebraic owner of metric-null line and transport.
- #282: coefficient ledger only.
- #278: cross-carrier residual diagnostic; same-carrier moving germ absorbed.
- #279: exact joint-defect census; mechanism awaits transfer theorem C.
- #240: shear response/realizability owner; structural use after B/C.
- #260/#275: separate connection-only/N0 nonlinear lane.
- #232: local-uniqueness no-go is compatible with an envelope theorem that
  does not require uniqueness.

## Interpretation firewall

Veronese, complex, homology, divisor, optical chamber, and crossing name
algebraic structures/proof programs here, not physical claims by terminology.

- \(C(d)P_d=0\): owned algebra.
- \(\mathcal H_C=0\): owned only where #270 kernel theorem applies.
- exact rank-jump locus: open until B.
- #240/#279 identification with divisor homology: open until C.
- envelope theorem: open until D.
- Einstein/stress crossing: open until E.

No BOOK/claim promotion follows from this CONTROL synthesis alone.
