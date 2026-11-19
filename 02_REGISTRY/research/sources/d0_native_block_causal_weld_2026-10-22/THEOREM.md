# Original full128: native-block realization, exact minimal-work embedding and full paired-spectrum transport

22 October 2026. Repository `gvakhrushev/d0_15`; existing Draft PR #334,
`exp/a4d-joint-response-continuation-2026-10-16`.
Initial read snapshot: `f090c0124c389e95e163611624a0f88b921a892a`.
Concurrent minimal-dilation owner consumed at `52aa5274533d7fc1eaacc30f4af1cfedc175e9bf`.

## 0. Parent substitution

The integration obstacle is not another missing geometric root. The fixed
Boolean predicate-count word does not preserve the original full128 quantum
poststates. The scoped invariant-range/no-work intertwiner is impossible
when the original compression Delta is not a projection.

The concurrent `A4D_ORIGINAL_GOLDEN_HALMOS_NAIMARK_ALL128_CAUSAL_BOOK_WELD_2026_10_22.md`
constructs a minimal doubled-work projector plus a genuine 63-row isometry.
This packet CONSUMES it. Shared all128 reconstruction conclusions are not
claimed as an exclusive new discovery. The new application supplies the
explicit realization inside the original Julia/Walsh register, an exact
forward adjoint identity, a moving-source intertwiner, and the full paired
heat transport INCLUDING the old zero-mode complement.

All 128 labelled Kraus operators and all chronological products remain the
original ones. No new reporter, fitted source, deletion of nonblank branches,
DATA reset, or new geometric root is introduced. This is an explicit
completion of the original Stinespring COLUMN, not proof that its action on
unprepared columns is uniquely compelled by M1. Initialized-cut feedback is
completion-independent; compulsory physical active-cut/scene-heat/valuation
selection, the gravity variation image and general refinement remain open.
`GR_closed=false`.

## 1. Actual original row and its native Julia/Walsh completion

Let d=16, p=phi^-1, a=sqrt(p). The original constructor is
`d0_book_uniform_source_2026-10-21/check_uniform_book_source.py`,
blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed`.
The included unchanged five-function excerpt is SHA256-pinned by the checker.
The actual 64 block rows N_j obey

    sum_j N_j N_j^* = I_d,     A=N_0,     Delta=A^*A,

and the original fine labels alpha=2j+b have

    K_(2j)   = delta_(j0)I - 2p^2 N_j^*A,
    K_(2j+1) = -2p sqrt(p) N_j^*A.                         (1)

For each genuine original contraction X use its Julia block

    J(X)=[[X, sqrt(I-XX^*)],
          [sqrt(I-X^*X), -X^*]].                          (2)

The identity f(XX^*)X=Xf(X^*X), obtained first for polynomials and then
for the positive square root, proves J(X) unitary. Also J(X)^*=J(X^*).
The eight controlled blocks for each of the four original roles are

    J(X),J(X),J(X^*),J(X^*),-J(B),-J(B),-J(B^*),-J(B^*),    (3)

where B is that role's unchanged baseline. Let D be this 32-block direct
sum and H=Walsh32 tensor I_32. On the ORIGINAL 1024-dimensional
control32 x Julia-work2 x DATA16 register put W=HDH. Its first d rows
are EXACTLY the old coisometry N=(N_0,...,N_63), because

    W_((0,0),(lab,b))
      = (1/32) sum_k (-1)^(lab dot k) [D_k]_(0,b).          (4)

There is no Gram-Schmidt completion or fitted matrix here. The field
dependence X(Y) stays unchanged. Every original dark row stays present.

Let S_xor shift the control index by XOR 2. The pairs in (3) imply
D^*=S_xor D S_xor. Walsh conjugation gives Z_c=H S_xor H, a diagonal
sign on control bit1. Consequently

    W^*=Z_c W Z_c.                                       (5)

This is an exact all-column forward-sign identity. A Julia array,
Walsh block or sign operation is NOT thereby priced as one Golden tick.

## 2. Faithful original-register projection and all128 column

Let J:C^16 -> C^1024 be inclusion of the old blank lab/work index j=0,
and E=JJ^*. With N=J^*W define

    Q=W^*EW=N^*N,   Q^2=Q=Q^*,   rank Q=16,
    J^*QJ=Delta.                                         (6)

The compression Delta is not itself a projection. Use the original
Golden G=[[sqrt(p),-p],[p,sqrt(p)]] on the port and set

    U_can=G^* diag(I,I-2Q) G
         =[[I-2p^2Q,       -2p sqrt(p)Q],
           [-2p sqrt(p)Q, I-2pQ]].                       (7)

This is a self-adjoint unitary on port2 x 1024, dimension2048. Initialize
port0 and J, and read every (j,b). Its blocks are exactly (1), not merely
the same probabilities. In particular the nonblank operation retains
all its independently established 17-plus Kraus directions and

    sum_(alpha>=2) K_alpha^*K_alpha
      =4p^2 Delta(I-Delta).                              (8)

At the original fixture its stationary probability is
0.0207857243508978..., not zero.

The previous invariant-range no-go remains true: here QJ has the
nonblank components N_j^*A, so QJ is NOT JDelta. These directions are
already in the old native register; no additional physical ancilla
beyond that inventory is proposed.

Equivalently U_can=(I x W^*) B_E (I x W), with the fixed Boolean core
B_E=G^*diag(I,I-2E)G. In that frame the initialized projector is
P'(Y)=(I x W)P_pre(I x W^*). It MOVES. Replacing it by a fixed
full-address blank-port cut would change the Book action.

## 3. Exact original minimal-work isometry, not a new sqrt gate

Consume the concurrent positive Halmos factorization. On 0<Delta<I put
S=sqrt(Delta(I-Delta)) and, INSIDE the original register, define

    R=(I-JJ^*) QJ S^-1,
    T=[J,R]: C^16 + C^16 -> C^1024.                       (9)

Projection multiplication gives

    J^*R=0, R^*R=I,
    QJ=JDelta+RS, QR=JS+R(I-Delta).

For the last equality, multiply Q^2J=QJ and use invertibility of S and
its commutation with Delta. Thus

    T^*T=I_32,   QT=T Q_Delta,
    Q_Delta=[[Delta,S],[S,I-Delta]].                      (10)

Q and QJ have rank16, so range Q is inside range T; hence
Q=T Q_Delta T^*. The nonblank rows of R are

    R_j=N_j^*A S^-1=-K_(2j)S^-1/(2p^2), j>0, R_0=0.       (11)

They are precisely the concurrent owner's 63 refinement operators.
The whole composite map is already implemented by the native-block
completion (7). It does not require separately actuated sqrt(Delta)
or S^-1 gates. Physical admission still belongs to the original
Julia/Walsh/control interface; square-root uniqueness does not prove it.

No moving derivative is suppressed:

    S dS+dS S=dDelta-dDelta Delta-Delta dDelta,
    dR=(dQ J-J dDelta)S^-1-R dS S^-1.                     (12)

The checker verifies the differentiated equation (10). Freezing this R
at the original fixture loses a fine-Kraus rapidity derivative of maximum
entry about 0.02222083333. It is not source-neutral work.

## 4. Whole chronological histories, references and preparation

Equations (1) and (7) are identities on any supplied smooth original
word family. For arbitrary finite chronological histories, including
changing field inputs Y_t,

    K_alpha_n(Y_n)...K_alpha_1(Y_1)
      = Ktilde_alpha_n(Y_n)...Ktilde_alpha_1(Y_1).          (13)

All existing derivatives agree by product differentiation. Tensoring
with identity on oldRIGHT proves the same for arbitrary correlated
DATA/reference states, every unnormalized conditional output and the
full retained record. No outcome independence or DATA reset is used.

The previously proved original future-even algebra, primitive DATA
self-preparation rho*=Delta^-1/Tr Delta^-1 and its Poisson reaction,
and true 65-label predictor therefore remain consumers of the SAME
instrument. Their hypotheses and fresh-register costs remain explicit.

The literal terminal charge c_b=1+b is preserved label by label.
For the SAME supplied complete cost ledger and observer algebra, all
recorded price and preparation/field sources agree. If a different
circuit is actually enacted, its factory/control/work costs still need
to be accounted for: operator equality is NOT a proof of equal total
implementation price. We do not reconstruct Info from a desired
Einstein source.

## 5. Exact initialized-cut Book source and native commutator pullback

P_pre includes port0 x j0 x ALL d DATA inputs. For ANY unitary completion
of the original Stinespring column, the initialized feedback is

    F_pre|_DATA=I-K_0^*K_0=g(Delta),
    g(t)=4p^2 t(1-p^2t).                                 (14)

This is independent of unprepared columns, conditional on that
initialized projector really being the selected Book cut.
For passive retained-right rank r_R and the ordinary unnormalized trace,

    J_pre=-r_R Tr log(I-zeta g(Delta)),
    dJ_pre=Tr(M_Delta dDelta),
    M_Delta=4r_R p^2 zeta (I-zeta g(Delta))^-1
                         (I-2p^2Delta).                 (15)

Cyclicity of trace proves (15) without [dDelta,Delta]=0. Since
2p^2<1 and 0<Delta<I, M_Delta is positive definite. This does not make
all constrained field tangents dDelta positive.

With B=WJ and Omega=dW W^* skew-Hermitian, the actual native pullback is

    dDelta=B^*[E,Omega]B,
    dJ_pre=Tr([B M_Delta B^*,E] Omega).                   (16)

This supplies every direction of a GIVEN smooth native field map.
It does not identify a Fourier rapidity fixture with the full spatial
42-field writer. If J itself is physical and moving, also retain

    dDelta=(dJ)^*QJ+J^*(dQ)J+J^*Q(dJ).                    (17)

On the SAME explicit completion, the different cut
P_wide=port0 x I_1024 instead has

    F_wide=4p^3Q,
    J_wide=-16r_R log(1-4zeta p^3),   dJ_wide=0.           (18)

Thus a fixed Boolean spectrum cannot replace the initialized boundary
source. This comparison does not assert that both cuts are compelled
physical choices; it locates what the instrument alone fails to select.

## 6. Full paired heat: exact spectral completion of minimal work

On port x range T, U_can is intertwined with the concurrent minimal
64-dimensional Golden/Delta unitary U_min. On the orthogonal complement
U_can is identity. Therefore, up to the explicit moving basis,

    U_can = U_min direct_sum I_1984.                      (19)

The initialized cut is fully in the first summand and is matched by T.
For C=(I-P_pre)UP_pre, C^*C and CC^* have the same d positive eigenvalues
of F_pre on mutually orthogonal ranges. Hence on the original2048 carrier

    spec(C^*C+CC^*) = {each eigenvalue of g(Delta) twice,
                      0 with multiplicity2016}.

The genuine complete paired-cut traces are

    Z_native=r_R[2016+2 Tr exp(-beta g(Delta))],
    Z_minimal=r_R[ 32+2 Tr exp(-beta g(Delta))],
    Z_native=Z_minimal+1984 r_R.                           (20)

This is the source-preserving transport: retain that EXACT old zero
block. It is derived from the original carrier, not a fitted counterterm.
Dropping it because the channel is unchanged would alter the thermal
source. Once (20) is used, the entire initialized J and paired H and all
existing field jets coincide. Moving-basis terms leave traces by exact
unitary invariance, not because T was frozen.

For H_cut=log(Z_native)/beta,

    dH_cut=-2 Tr(exp(-beta F_pre) dF_pre)/Z_base,
    Z_base=2016+2 Tr exp(-beta F_pre).                     (21)

The passive right multiplicity multiplies J but cancels from this
normalized thermal derivative. Its absolute log(r_R)/beta contribution
is retained. This paired Hodge is NOT thereby the compulsory scene Hodge.

At the actual fixture and beta=2p^2:

    d_theta H_minimal= 0.000596492862448003,
    d_theta H_native = 0.000018496680718219935,
    difference       =-0.000577996181729783.               (22)

The heat-source mismatch is resolved by the exact transport (20), not
by claiming it vanishes or by treating minimal work as a new physical
carrier without the old complement.

## 7. Autonomous clock with moving tests

For a supplied L-block word U and actual prefixes V_t, take
P_t=V_t P_pre V_t^* before the last gate, P_L=P_pre, and one idle/wrap
slot. In the autonomous L+1-stage operator, every interior feedback block
is zero; the last gate block is unitarily equivalent to F_pre. All stages
remain in the ambient Hilbert space. Thus the feedback determinant has
NO factor L+1, whereas the whole paired heat has

    Z_base=2048(L+1)-32+2 Tr exp(-beta F_pre).              (23)

This follows by block multiplication and extends the existing Boolean
clock identity to the original full nonblank column. Moving tests are
not frozen. An explicit nine-block algebraic replay is

    G, W, S_E, Z_c, W, Z_c, Z_p, G, Z_p,

where S_E=diag(I,I-2E) and G^*=Z_pGZ_p. These are NOT nine paid native
ticks. Physical expansion must charge actual Julia/Walsh/control calls,
any enacted tests and the real clock inventory. Extra stages are not
automatically heat-source-neutral padding.

## 8. Validation and actual parent status

The independent checker uses the unchanged original constructor and
compares it with the full native matrix completion. It retains all128
formal labels and ALL16384 two-tick operator products and derivatives,
including dark slots. It tests rapidity theta=log(5/4) and single-tick
jets at 0,0.08,-0.12; the coordinate r=1/9 is NOT silently substituted
for rapidity. Moving stationary preparation is included in the two-tick
probability and port-cost sums.

71 explicit checks pass. Normal and python -O stdout are byte-identical.
The maximum direct matrix/history discrepancy is 2.665e-15; independent
finite-difference errors are reported separately in RECEIPT.json.
Exact symbolic controls check Golden algebra and a nonprojector
compression. General assertions above are algebraic proofs, not
floating-rank or interval claims. No Lean, external review or remote CI
success is asserted.

The actual original initialized source at r_R=128 is

    d_theta J_pre=-2.344012184324785e-6,

and the full-work cut source is zero. These are actual native rapidity
sources, NOT a computed full42 Einstein covector. The two-tick terminal
port cost is 2.0260525436844175 and its moving-input rapidity derivative
is -0.001890600542203736.

Closed by this composition: the minimal Halmos/63-row mathematical
factorization is explicitly realized inside the old native block register;
all causal maps and source jets are retained; the whole paired-cut spectral
transport is fixed by the actual1984-mode complement. No unpriced newly
specified sqrt(Delta) gate is needed to realize the composite column.

Still required for physical D0-to-GR: the actual definition of P_N and
Delta_N, the complete native valuation and independent apparatus equations,
and their true gravity-field pullback/refinement. Equality of the original
channel does not itself fix those choices or transplant the fixed diagonal
predicate-count Einstein consumer. Selecting a cut just because it gives
the desired source would be circular. The new result removes a named
implementation/carrier premise; `GR_closed=false` remains.

## Source ownership

- Native constructor blob ee8de4635d24c668949ac9a0186616ab7d59f2ed;
  unchanged excerpt blob ed8a505d00337037d7aec976098717c3a4c43308.
- A4D_BOOK_BOOLEAN_TO_ORIGINAL_FULL128_CAUSAL_WELD_GATE_2026_10_22.md,
  blob 98f7f43165a26b598579c25734efd80ea3872f62.
- Concurrent A4D_ORIGINAL_GOLDEN_HALMOS_NAIMARK_ALL128_CAUSAL_BOOK_WELD_2026_10_22.md,
  read at 52aa5274533d7fc1eaacc30f4af1cfedc175e9bf.
- A4D_ORIGINAL_FULL128_THREE_TICK_CANONICAL_FUTURE_EVEN_ALGEBRA_2026_10_22.md,
  blob 08b9b07eb01b1c59643aec1d484d165146762f6d.
- A4D_ORIGINAL_BOOK_BOOLEAN_TRACE_CLOCK_AND_GLOBAL_EINSTEIN_2026_10_22.md:
  consume the clock identity with the present original column, not its
  distinct fixed full-address cut.
- Existing native65 causal-source and original primitive self-preparation
  owners retain their stated cost, reference and preparation hypotheses.

Unitary dilation is standard quantum-channel mathematics, not a new D0
axiom or a new Stinespring theorem. For constructive context see
F. vom Ende, arXiv:2301.05488. The finite block proof here is self-contained.
