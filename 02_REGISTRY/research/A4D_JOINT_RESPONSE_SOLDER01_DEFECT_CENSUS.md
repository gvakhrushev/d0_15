# A4D joint-response (NF) defect census in the complete 0/1 solder class

**Bounded companion result.** This memo was produced by companion Draft PR #283
for `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE` and is integrated into
main as a partial exact/scout research artifact without retiring that EXP task.
The main nonlinear execution remains PR #240 and its memo
`02_REGISTRY/research/MEMO_A4D_JOINT_RESPONSE_DECOUPLING_MICROSTRUCTURE.md`.
The census is evidence about the frozen joint symbol only; it is not a
joint-critical or response terminal.

**Context consumed.** The (NF) identity of the main memo states that every
direction of the joint symbol kernel \(J=[H;C]\) has vanishing tested
response moment \(n^{*}D_QH[q]n\). The main execution certified exactly two
(NF) defects in a fixed eleven-solder family (the upper shear at
\((-1,1,-1,1)\) and the chain \(I+E_{01}+E_{13}\) at \((-1,1,1,-1)\), each
with moment \(-2\) on \(q_{11}\) after the committed witness normalisation)
and isolated the shear defect along one unipotent slice. The present
certificate asks how isolated the phenomenon is inside a complete finite
class fixed before any rank is read.

## 1. The class

The **unit-diagonal 0/1 solders**: all sixteen entries are \(0\) or \(1\) and
the diagonal entries are \(1\). The class has \(2^{12}=4096\) members. The
metric channel needs a nondegenerate solder, and
\(\det(S^{T}\eta S)=\det(S)^{2}\det(\eta)\), so the \(2104\) members with
\(\det S=0\) are excluded; exactly \(1992\) are screened at all
\(4^{4}=256\) characters of the L=4 grid. All solders are constant.

## 2. Census (scout)

The numeric mirror of the certified symbol assembly is validated against the
exact symbolic implementation first: the bracket-form deviation is exactly
\(0\), the metric-block deviation stays below machine precision, and the
certified singular counts of all ten control solders are reproduced. The
complete census then gives

| quantity | value |
|---|---|
| nondegenerate solders screened | 1992 |
| singular (solder, character) pairs | 11424 |
| pairs with nonzero response moment | 1602 |
| solders carrying at least one failure | 505 |

The failures split by kernel dimension as \(888\) one-dimensional, \(594\)
two-dimensional and \(120\) three-dimensional, and by character type as
\(780\) real (\(\pm1\)), \(228\) pure-imaginary (\(\pm i\)) and \(594\)
mixed. The six real characters of mixed sign carry \(148\), \(148\), \(148\),
\(112\), \(112\) and \(112\) failures; the diagonal quarter-wave characters
carry none, consistent with the all-solder diagonal annihilation theorem of
the main memo.

## 3. Exact verification

Every one of the \(1602\) candidate pairs is verified over \(\mathbb Q(i)\):
the exact rank equals the scout rank and at least one scout moment block is
exactly nonzero on the exact kernel. The first confirmed block of every pair
is recorded in
`certificates/a4d_joint_response_solder01_defect_census.json`. Examples:

- the solder \(I+E_{01}+E_{02}+E_{03}\) at \((i,i,i,-1)\) has exact rank 23
  with exact blocks \(q_{03}=-64\), \(q_{13}=32\), \(q_{23}=32\) on the exact
  kernel basis; the primitive witness (content \(4\)) carries the moments
  \((-4,+2,+2)\);
- the solder \(I+E_{01}+E_{13}+E_{21}+E_{30}+E_{31}+E_{32}\) at
  \((1,1,-1,-1)\) has exact rank 23 and primitive moment \(-4\) on \(q_{00}\);
- two- and three-dimensional kernels occur as well:
  \(I+E_{20}+E_{21}+E_{30}+E_{31}+E_{32}\) at \((i,i,i,1)\) has a
  two-dimensional kernel with exact \(q_{03}\)-block
  \(\begin{pmatrix}0&-i/4\\ i/4&0\end{pmatrix}\), and
  \(I+E_{01}+E_{02}+E_{10}+E_{21}+E_{30}+E_{31}+E_{32}\) at \((-i,1,-i,-i)\)
  has a three-dimensional kernel with a \(q_{01}\)-block of entries
  \(\pm16i\).

## 4. Reproduction of the certified family

On the ten declared control solders the census reproduces every certified
family datum exactly: the flat solder's twenty kernels - eighteen
one-dimensional and the two diagonal four-dimensional ones - have all ten
moment blocks exactly zero; the upper shear and the chain carry their cut
defects with exact moment \(-2\) on \(q_{11}\); every other family singular
pair has ten exactly vanishing blocks.

## 5. Consequences

* The two family defects are not isolated rarities. Within a complete finite
  solder class, a quarter of the nondegenerate members carry at least one
  tangent-level (NF) failure, and the failures are not confined to the two
  known characters: the six real characters of mixed sign and the
  three-plus-one imaginary families also fail.
* Any "joint-critical replacement for (NF)" cannot be a tangent-level
  identity. The tangent-level statement fails at \(1602\) exactly certified
  points in this class alone; the replacement must control the nonlinear
  joint-critical set, exactly as the order-\(u^{5}\) cuts of the two family
  defects already show.
* The response-decoupling NOGO route gains \(1602\) potential seeds, each of
  which needs its own nonlinear cut analysis. Only the two family defects are
  cut today; nothing here produces a joint-critical sequence.

\[
\boxed{\texttt{NF-DEFECTS-ARE-NOT-CONFINED-TO-THE-ELEVEN-SOLDER-FAMILY}}
\]

## 6. Boundary

Constant solders, the unit-diagonal 0/1 class, the L=4 grid, and the tangent
level of the joint symbol only. The zero-moment side of the census is exact
for the ten declared control solders and scout-level elsewhere (the numeric
moment magnitudes there are at machine zero, versus \(0.047\) for the
smallest certified failure - a separation of fourteen orders of magnitude);
no other solder class and no off-grid character is covered. No joint-critical
sequence is produced, no cut is computed for the new defects, no \(\#216\)
comparator gap is computed, and no response terminal follows. No
claim/release status, BOOK entry or downstream task is touched.

## 7. Certificate

`certificates/a4d_joint_response_solder01_defect_census_check.py` reruns the
four gates and writes
`certificates/a4d_joint_response_solder01_defect_census.json`; it prints
`NF-DEFECTS-ARE-NOT-CONFINED-TO-THE-ELEVEN-SOLDER-FAMILY` and
`PASS_ALL_CANDIDATES_EXACTLY_CONFIRMED` on success. The certificate is
self-contained with respect to the execution branch: it loads the two merged
`#216` owner modules directly and carries verbatim copies of the four exact
assembly functions of the certified branch module
`a4d_joint_response_shear_l4_support_check.py` (branch commit `d37df8ce`),
which is not yet on main.
