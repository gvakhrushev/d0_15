# Full coherent history, one original CNOT, and the paid occupation source

22 October 2026. Existing #334 / constitutive / native-programme-v1.
This is a finite-programme comparison at the declared input, commitment and
tariff interface, not full GR or a new physical information rule.

## 1. Inputs and new substitution

Original input commit: 3fcabfa0688f581fbbe54c70a342c8a49b9ca5fb.
The original full128 constructor has Git blob
ee8de4635d24c668949ac9a0186616ab7d59f2ed. The existing all-nonblank
pointer-X owner has blob 62df559c93ca59d948abfb0ed33db3b90b63bf80;
its earlier price/source result is consumed, not reclaimed.
The hidden-Choi owner has blob 070876a02ddc9a22d80b882065f6982bd93bbdb5.
SOURCE_PINS.json gives immutable paths.

The new comparison uses ONE ordinary specified CNOT, placed before versus
after the same original U. It gives equality of the full across-field
coherent Gram and equal fixed primitive inventory. A marked boundary and
finite-history occupation recover the missing price datum.

## 2. Literal original rows and gate

Write alpha=2j+b, j=2ell+eta, with 0<=j<64 and b,eta in {0,1}.
Put p=phi^-1, p+p^2=1. The original constructor is

\[
 K_{2j}=\delta_{j0}I-2p^2N_j^\dagger a,\qquad
 K_{2j+1}=-2p\sqrt p\,N_j^\dagger a,\qquad a=N_0.
 \tag{1}
\]

On the owned chart a is Hermitian, and K_0=I-2p^2 a^2.
For every j>0 define, including dark rows,

\[
 L_j=-2p N_j^\dagger a,\qquad
 (K_{2j},K_{2j+1})=(pL_j,\sqrt p\,L_j).
 \tag{2}
\]

The factor -2p is compulsory. Let J be the odd j and take the original
CNOT from eta to b, equivalently pointer bit1 -> bit0:

\[
 T|j,b\rangle=|j,b\mathbin{\oplus}(j\bmod2)\rangle .
 \tag{3}
\]

It fixes both j=0 labels. No j>0 controlled-OR circuit or deleted slot
is involved. For the actual READY injection E, P=EE^dagger and Q=I-P,

\[
 TE=E,\quad TP=PT=P,\quad [T,Q]=0,\quad T=T^\dagger=T^{-1}.
\]

With rightmost operators acting first, compare

\[
 U_A=U_yT,\qquad U_B=TU_y .
 \tag{4}
\]

Each pays for exactly one same U and one same CNOT under an additive
state-independent primitive tariff. Pointer commitment is AFTER both
calls. Earlier irreversible commitment would be a different task.
Gate inventory alone does not prove equal autonomous initial controller
preparation or equal state-dependent physical work.

## 3. Complete coherent comparison and fixed-history extension

The READY maps are W_A=U_yE and W_B=TW_A. Therefore

\[
 W_B(y_-)^\dagger W_B(y_+)
 =W_A(y_-)^\dagger W_A(y_+) .
 \tag{5}
\]

For any common pure input, or common purification of a mixed/correlated
input, including a moving original RIGHT/preparer family Omega_y,
Psi_B(y)=(T tensor I)Psi_A(y). Its complete scalar across-field Gram
is identical, with every existing field and preparation derivative.
Thus Berry connection in the same input gauge, its curvature,
Fubini--Study metric and finite Bargmann products agree. No flatness
assumption is used.

For a fixed finite nonadaptive horizon with fresh declared READY pointers
and no subsequent control reading the changed labels,

\[
 V_{B,n}=(T_1\otimes\cdots\otimes T_n\otimes I)V_{A,n}.
 \tag{6}
\]

Inductively, each T acts on an emitted pointer and commutes with the
later DATA/fresh-pointer operations. No DATA reset or iid history
assumption is used. Nonhomogeneous fields at different uses are allowed.
All coherent comparisons between the two within-family field histories
are preserved. A port-sensitive stopping rule or changed future test
requires its own actual covariance/controller proof.

This is equality of the within-family field kernels, not equality of the
two states in the fixed symbol basis or of their ordered programme words.

## 4. Exact channel, cut and readout scope

The two sets of Kraus labels differ by the pointer permutation. Their
complete DATA channel Phi is the same, and K_0 and K_1 are unchanged.
Since each swapped pair consists of scalar multiples of the same L_j,
each named output support is unchanged, including a zero support.
The original registered support and the next-tick constructions from
that support and K_0 are preserved.

For C_A=QU_AP and C_B=QU_BP,

\[
 C_B=TC_A,\quad C_B^\dagger C_B=C_A^\dagger C_A,\quad
 C_BC_B^\dagger=T C_AC_A^\dagger T^\dagger .
 \tag{7}
\]

The paired cut-incidence Hodge is conjugate by I_P direct-sum T_Q.
Its spectral quantities and their field derivatives agree. The original
Book03 SCENE Hodge may read the intermediate ordered word or further
programme data; no blanket invariance of that different object is proved.

Full fine-pointer pinching E_f commutes with Ad_T:

\[
 E_f(TXT^\dagger)=T E_f(X)T^\dagger .
 \tag{8}
\]

Consequently the complete fine CQ outputs have equal von Neumann
entropy, and the pointer laws have equal Shannon entropy. The full
coherent outputs also have equal entropy, by their own unitary equivalence.
For the declared gain [S(output)-S(input)]/ln(phi), both initial
and output terms are therefore preserved, with their moving preparation
jets. The coherent and measured information are different quantities;
neither is substituted for the other. Another Book06 future algebra or
extra intermediate registration requires its own covariance check.

## 5. Original terminal charge and exact occupation effect

Keep the actual fixed 0/10 tariff attached to the named physical bit:

\[
 c_b=1+b,\qquad c_0=1,\quad c_1=2 .
\]

Common row-only charges cancel because T preserves j. Let

\[
 E_J=\sum_{j\in J,b}K_{2j+b}^\dagger K_{2j+b}
 =\sum_{j\in J}L_j^\dagger L_j
 =4p^2a^\dagger R_Ja,\qquad
 R_J=\sum_{j\in J}N_jN_j^\dagger .
 \tag{9}
\]

For a common DATA marginal rho, Q_J=Tr(rho E_J).
The swapped row probabilities are proportional to (p^2,p) versus (p,p^2).
Their terminal cost contrast is p-p^2=p^3, hence

\[
 \boxed{\Delta C^{\rm term}=C_A^{\rm term}-C_B^{\rm term}
       =p^3\operatorname{Tr}(\rho E_J).}
 \tag{10}
\]
\[
 d\Delta C^{\rm term}
 =p^3[\operatorname{Tr}(d\rho E_J)+\operatorname{Tr}(\rho\,dE_J)] .
 \tag{11}
\]

The same difference holds for the declared Cost--Info whose information
equality was proved above. No stationary input is substituted.

### Strict carrier boundary

The numerical witness uses the separately paid Choi16 preparation declared
by its owner,

\[
 |\Phi_{16}\rangle=\tfrac14\sum_{m=0}^{15}|m\rangle_D|m\rangle_{R_1}.
\]

R_1 is a declared 16-dimensional subspace of physical oldRIGHT128.
Thus rho_D=I16/16 and rho_R=I16/16 direct-sum 0_112. The RIGHT rank
is 16. Retaining unused carrier dimensions does not make it I128/128.

The operator/Gram identities hold for every common READY input, including
an actually admitted full-rank RIGHT preparation. The strict number below
is NOT a new check on the original full-rank RIGHT128 input.
A mathematical Phi16 tensor Phi8 spectator lift would make RIGHT
maximally mixed in 128 dimensions while leaving DATA expectations fixed,
but its extra carrier, paid native preparation, clock and full apparatus
effects are not supplied by the consulted owner.

### Literal CAR16 computation

Use CAR order (0,2,3,1), phases (i,i,-1,-i), nu=3/5 and
the proper role-1 boost U_b=exp(theta G), with
G=c_0 c_1^dagger+c_1 c_0^dagger and theta=ln(5/4).
Equivalently tanh(theta/2)=1/9.
Here U_b is the boost inside the constructor, not the full128 U in (4).

For x_r=nu c_r U_r phase_r, U_1=U_b and other U_r=I, the actual
blank row is

\[
 a=\frac1{16}\sum_r(x_r+x_r^\dagger-\nu c_r-\nu c_r^\dagger).
 \tag{12}
\]

Walsh Parseval on the ORIGINAL duplicated root column gives

\[
 R_J=\frac1{16}\sum_r
 [(I-x_rx_r^\dagger)+(I-x_r^\dagger x_r)
 +(I-\nu^2c_rc_r^\dagger)+(I-\nu^2c_r^\dagger c_r)] .
 \tag{13}
\]

Thus every physical row is included without numerically taking its
individual Julia square root. With
S=c_1 U_b^2 c_1^dagger+U_b c_1^dagger c_1 U_b,

\[
 R_J=(1-\nu^2/2)I-\frac{\nu^2}{16}(S-I).
 \tag{14}
\]

On the fixed Choi16 DATA state put
mu=Tr(a^2)/16, M=Tr[a^2(S-I)]/16. Equations (9)--(10) yield

\[
 \Delta C^{\rm term}
 =4p^5[(1-\nu^2/2)\mu-\nu^2M/16].
 \tag{15}
\]

The exact fixture values are

\[
 \mu=141489/10240000,\quad
 \partial_\theta\mu=-4059/5120000,
\]
\[
 M=5952609/8192000000,\quad
 \partial_\theta M=13430331/2048000000 .
\]

Therefore

\[
 \boxed{\Delta C^{\rm term}
       =\frac{37073140119}{819200000000}p^5>0,}
 \tag{16}
\]
\[
 \boxed{\partial_\theta\Delta C^{\rm term}
       =-\frac{653413779}{204800000000}p^5<0.}
 \tag{17}
\]

Diagnostics: 0.004080667674739511 and -0.0002876869321169991.
These are terminal-price units at the declared fixed Choi16 state,
not the moving inverse-square stationary state used by the earlier owner.

### Exact arithmetic receipt

At this fixture,

\[
 U_b=(40I+G^2+9G)/40,\qquad
 \partial_\theta U_b=(41G+9G^2)/40 .
\]

Write a=(3/3200)H, da=(3/3200)D and S-I=S_int/1600.
The independent root Gaussian-BigInt reconstruction gives:

| Trace | Exact integer |
| --- | ---: |
| Tr H^2 | 251536 |
| Tr HD | -7216 |
| Tr H^3D | -98629472 |
| Tr H^2 S_int | 21164832 |
| Tr (HD+DH) S_int | 2385216 |
| Tr H^2 dS_int | 188623936 |

For example
dM=9(2385216+188623936)/(3200^2*1600*16).
These exact integers and rational reductions prove (16)--(17).
check_original_cnot_source.mjs also checks the literal CAR relations
and proper boost derivative. RESULT_CNOT.json records 44 executed
assertions, with no floating Julia root or numerical sign threshold.

## 6. The actual price mark supplies the missing datum

For the original terminal cost observable C define

\[
 M_C^{A,B}(y_-,y_+)=W_{A,B}(y_-)^\dagger C W_{A,B}(y_+).
\]

The unmarked Gram (5) is equal, but

\[
 \boxed{
 M_C^A-M_C^B=p^3\sum_{j\in J}L_j(y_-)^\dagger L_j(y_+).
 }
 \tag{18}
\]

Indeed C-T^dagger C T has values (-1,+1) on a changed pair, and
the two native coefficients give -p^2+p=p^3.
On the diagonal this is p^3 E_J.

Equivalently the analytical marked kernel
M_s=W_-^dagger exp(-sC)W_+ obeys -partial_s M_s|_0=M_C.
The scalar version includes the actual moving input on both sides and
thus every term of (11). The parameter s is a mathematical price mark;
it is not an imported physical time, phase oracle or free Hamiltonian.

For a retained additive history ledger, use its genuine total charge
observable. Nonterminal charges must stay in their own carrier or in
a proved insertion; they are not assigned to C by assertion.

## 7. Complete physical ledger and admissibility boundary

Separating only the proved terms, the full physical difference is

\[
 S_A-S_B=p^3Q_J+
 (C_A^{\rm other}-C_B^{\rm other})
 -(I_A^{\rm other}-I_B^{\rm other}).
 \tag{19}
\]

Every displayed term is differentiated. The same one-U/one-CNOT fixed
primitive tariff cancels. Identical real input and READY costs cancel
in a comparison, including identical field-dependent contributions;
they remain in each absolute programme.

Different autonomous ordered controller descriptions are not proved
equally priced by gate inventory. A constant difference shifts (16)
but not (17); a variable difference remains in (19).
A control-state-dependent CNOT work cost may differ when acting on
READY versus after U. State-dependent time, intermediate records,
failure, erasure, stopping and further information all retain their
own source. If the task commits immediately after U, the later coherent
T programme is not an admitted version of that task.

Thus (17) is a strict original terminal source, and a full declared
Cost--Info source under the explicit equality of its remaining terms.
It does not assert that unknown physical charges vanish.

## 8. Real finite-history occupation, without reset or iid replacement

For fixed nonadaptive horizon let rho_k be the actual unconditional
DATA state before use k. Since both channels coincide,

\[
 \rho_{k+1}=\Phi_k(\rho_k),\qquad
 \Delta C_n^{\rm term}
 =p^3\sum_{k<n}\operatorname{Tr}(\rho_k E_{J,k}).
 \tag{20}
\]

The complete retained fine-history entropy is unchanged by (6).
For homogeneous fields the missing datum is the actual occupation effect

\[
 O_n=\sum_{k=0}^{n-1}(\Phi^*)^k(E_J),\qquad
 \Delta C_n^{\rm term}=p^3\operatorname{Tr}(\rho_0 O_n).
 \tag{21}
\]

Its full source is

\[
 d\Delta C_n^{\rm term}
 =p^3\sum_{k<n}[\operatorname{Tr}(d\rho_k E_{J,k})
             +\operatorname{Tr}(\rho_k dE_{J,k})],
\]
\[
 d\rho_{k+1}=(d\Phi_k)(\rho_k)+\Phi_k(d\rho_k).
 \tag{22}
\]

The incoming d rho_0 remains. A changed port-sensitive stop tree requires
its own actual stopped occupation and controller; it is not covered by
declaring n to be a mean stopping time.

## 9. Bounded C1 weak-step consumer

Scale the same original contractions x_r=nu Y_r, with baseline nu c_r,
and put epsilon=nu^2. The actual Parseval identity gives

\[
 a=\nu D,\quad
 D=\tfrac1{16}\sum_r(Y_r+Y_r^\dagger-c_r-c_r^\dagger),
\]
\[
 R_J=I-\epsilon B,\quad
 B=\tfrac1{16}\sum_r(Y_rY_r^\dagger+Y_r^\dagger Y_r+I)\succeq0.
\]

On their legitimate Julia-contraction domain,

\[
 \boxed{p^3E_J=4p^5(\epsilon D^2-\epsilon^2 DBD).}
 \tag{23}
\]

For n epsilon<=T_0, the leading whole-history term is
4p^5 epsilon sum_{k<n}Tr(rho_k D_k^2), with exact remainder
R_epsilon=-4p^5 epsilon^2 sum Tr(rho_k D_k B_k D_k).

Assume on the actual fixed finite carrier and specified field jets that

\[
 \|D_k\|\le M_D,\ \|B_k\|\le M_B,\quad
 \|\dot D_k\|\le L_D,\ \|\dot B_k\|\le L_B,\quad
 \|\dot\rho_k\|_1\le L_\rho .
\]

At fixed epsilon,n, direct differentiation yields

\[
 |R_\epsilon|\le4p^5T_0\epsilon M_D^2M_B,
\]
\[
 |\dot R_\epsilon|
 \le4p^5T_0\epsilon[
 L_\rho M_D^2M_B+2M_DM_BL_D+M_D^2L_B].
 \tag{24}
\]

This is a derivative estimate, not a derivative inferred from a value
bound. One sufficient state-jet premise is
||dot Phi_k||_{1->1}<=epsilon L_Phi and ||dot rho_0||_1<=L_0.
CPTP trace-norm contraction on Hermitian inputs and (22) give
||dot rho_k||_1<=L_0+T_0 L_Phi.

If the actual processes and their jets make the leading Riemann sums
converge in C1, the limiting contribution is
4p^5 integral_0^{T_0}Tr[rho(t)D(t)^2]dt.
This is an actual quadratic occupation density, not a derivation of
physical time, the compulsory Book03 R term or the Einstein action.
Moving epsilon/cutoff and unbounded carriers require their extra sources
and uniform bounds. Raw216 uniformity is not asserted.

## 10. Parent conclusion and verification scope

The complete unmarked field-history Gram, DATA channel, blank return,
specified registered supports and paired-cut spectra are identical for
the two families. Their original terminal-price covectors are not.
Therefore these unmarked data alone cannot recover that price source
for both families. With the stated equality of other charges, the
same conclusion holds for the full declared Cost--Info source.

This does not prove different critical sets everywhere or invalidate
an algebra-valued ordered-word object that retains the price mark.
The constructive missing data are (18), (21) and (23): the actual
price-marked operator and occupation source.

The root exact checker was executed in the available JavaScript runtime.
No historical full128/all42/Lean/CI run is claimed. The full reference
scope, SCENE Hodge, controller/preparer/clock, all42 field writer and
raw216 conditions remain explicit. GR_closed=false.
