# Independent review of the late coframe and native-PF applications

Reviewer: `/root/universality_selection`

Date: 21 October 2026

Decision: **accepted within the stated fixed-input, source and operator scopes.**
The reviewer did not author either new application. This is an analytical
review plus one independent narrow symbolic coefficient check, not a replay
of the source owners' geometry or Golden-history suites.

## 1. Reviewed artifacts and input boundary

Paths in this table are relative to the parent synthesis packet.

| Artifact | SHA256 |
| --- | --- |
| `late_application/COFRAME_RESIDUAL.md` | `1d27ad581ab58bba570b674f9f03a3e64cb7ad52d725b5cf49af12f4086efa19` |
| `late_application/check_coframe_residual.py` | `762e6c3f1af3f947c3b9a18238653e25e21d2464293e40a9e06fd569302a0322` |
| `late_application/RESULT.json` | `ad62a373d66a5df6b9b71627ca1b6f533db171e71492a713e14e9400f866635d` |
| `late_application/NATIVE_PF_AND_CLOCK_APPLICATION.md` | `0f5a2f6e4015ee90140572da1e29c7459a3a912090c87f79d349eda02b5ae70e` |
| `paid_source/PROOF.md`, with clarified historical PF premise | `b7fce1f173b5fc4fa0787c4ecae6134d35f33a1771062214c4aa5c6d23d5da55` |
| `LATE_SOURCE_PINS.json` | `68da9148abeb8c38177fbc265e48b277e0fc51224a2388ef00a6dec21c87dc6e` |

I independently verified the four late frozen sources, including their byte
sizes, SHA256 and Git blob hashes, against commit
`c7e0c3d2f6bcfbcc8bd43034ff72da85b8cdd18a`. I also rechecked the original
twenty frozen sources against their separate `441bdef5` ref. The late
application does not relabel the original inputs or historical receipts.

## 2. The new coframe residual is an ambient Euler component

The canonical/null pullback is used consistently. At the double-zero
point, the complete N=1 field source is the nonzero gain `M tau (-a)`
times the ambient derivative of `sum(f_star+kappa q)`, with `kappa>0`.
The actual fixed-count, fixed-cost interface is essential to this statement;
it does not settle preparation or physical Book equations.

For the volume-preserving variation

    e(v)=diag(A v,B/v,r,r),     A B=1,

the actual scalar increments at the selected background are
`p_t=epsilon A^2 v_star^2`, `p_x=epsilon`. In the independent coframe
variation `p_t`, `p_x` and the links are held fixed. Differentiating

    q(v)=p_t^2/(A^2 v^2)-epsilon^2 v^2/B^2

before substituting that background gives

    q_v(v_star)=-4 epsilon^2 A^2 v_star,
    kappa q_v(v_star)=-2 A^2 v_star.

Consequently the exact row

    E_v=(L_h-R_h/v_star^2)/h^2-2 A^2 v_star

is correct. It is the genuine combination
`A E_(e00)-(B/v_star^2)E_(e11)` of the original coframe rows. Its zero
determinant variation distinguishes it from the solved radial scaling row.
Reimposing `p_t=epsilon A^2 v^2` during differentiation would change the
variation and would lose this Euler equation.

## 3. Independent coefficient derivation

I expanded the displayed exact temporal and spatial face functions directly.
With `dot g=exp(-r^2/2) partial_r g`, write

    f_h(v)=F0(v)+h F1(v)+O(h^2),
    F0(v)=r^2 dot k1+2 B r dot k2/v+2 A r v k1 k2+A B k2^2,
    F1(v)=r^2 ddot k1/2+B r ddot k2/v.

The absence of an order-h contribution from the spatial commutator follows
from its even leading expansion in h. The relevant exact derivatives are

    F0'(1)=2 r exp(-r^2/2)=2 A^2,
    F0''(1)=-2(r^2+1)exp(-r^2/2)/r,
    F1'(1)=-(3r^4+2r^2+3)exp(-r^2)/(4r^2).

For `v_star=1+h c+O(h^2)`, the owned scalar root gives

    c=-3(r^4-1)exp(-r^2/2)/(8r^3).

Substitution into the fixed-matter source yields

    E_v=h[c(F0''(1)-2 A^2)+F1'(1)]+O(h^2)
       =h exp(-r^2)(3r^2+1)(r^4-3)/(4r^4)+O(h^2).

An independent short SymPy calculation, starting from those finite-face
Taylor expansions rather than calling the author's checker, returned the
same derivatives, projected-root coefficient and factored Euler coefficient.
It also verified the exact value `-2/exp(1)` at `r=1`. No grid, full-matrix
geometry, factory or history-enumeration suite was run for this review.

Thus the counterexample at a free `r=1` anchor is valid for all sufficiently
small positive h. The cancellation of the unprojected scalar's order-h value
at `r=1` does not cancel this derivative. On `1<=r<=6/5`, the factor bound
`(3r^2+1)(3-r^4)/(4r^4)>=193/432`, together with
`exp(-r^2)>=exp(-36/25)`, proves the claimed uniform negative leading
coefficient. The smooth compact implicit section supplies the uniform
remainder premise. Other corrected coframe/link representatives are not
excluded by this result.

## 4. The remaining 39 rows cannot be replaced by a restricted gradient

For `C(y)=(f_z(y),q_z(y))`, the affine action is a fixed coefficient
combination of C. On `Sigma=C^-1(0)` its tangent derivative is therefore
zero at every point, while its ambient covector `DC(y)^T lambda` need not
vanish. The displayed nonzero `E_v` is a concrete instance.

The new double-zero theorem, both solved material equations and the radial
equation remain valid. The other fifteen coframe and twenty-four link
components have not been solved. Correcting the point on Sigma while solving
the original remaining ambient covector is a meaningful target; minimizing
or differentiating the already constant restricted action is not that
target. The proposed coupled linear test correctly retains `D C delta y=0`
alongside the ambient residual equation, with gauge, currents and boundary
compatibility still to establish.

The endpoint warnings are substantive. A link correction contributes to
adjacent anchored faces, and a preserved constant-current scalar history
with fixed endpoints must preserve `epsilon sum_j h A_j^2 v_j^2`. The local
root theorem does not provide either whole-slab condition. No null-link
Brinkmann cancellation is transferred to the different noncommuting boosts.

## 5. PF premise: now supplied for the stated native sequence

The density is precisely `rho=L^4 N_(n,z)/F_(n+1)` for unchanged original
Golden box addresses, at `n_L=64 s(L)+128`. It is not the site probability
`h^4 rho`, an absolute regular weight, a full128 invariant input density or
a freely chosen smooth prior. The existing discrepancy theorem already
provided an eventual positive density on suitable depth schedules. The
new consumer supplies the stronger explicit all-L schedule.

For `L>=4`, the consumed `||rho-1||_infinity<9h^3` gives
`rho>55/64`, `||rho^-1||<64/55` and `||rho^-1-1||<18h^3`.
With the original compact source-chart and current bounds,

    ||(f_h/rho_h)V_A||_2 <= (64/55) C_f C_V h.

Applying the already proved summation-by-parts estimate gives exactly

    ||R_A(rho)||_-1 <= (128/55) L_F tau C_f C_V h.

For the PF-only comparison at fixed f and V,
`|k_rho-k_1|<=18 L_F tau C_f h^4`; the same factor-two divergence estimate
then gives

    ||R_A(rho)-R_A(1)||_-1 <= 36 L_F tau C_f C_V h^4.

Both constants and orders are correct. These are the owned normalized
material rows, not a new normalization of the full physical price. The
actual common scalar factors, moving preparations and implicit dictionaries
retain their own source obligations. A uniform componentwise current bound
gives the additional strong PF-only order h^3; strong total order h also
uses the source owner's smooth rank-two estimate and is not inferred from
the negative norm alone.

The alternating order-one PF-jump fixture remains a valid positive-weight
counterexample outside this specific sequence. It cannot be used to reject
the new schedule. Conversely, the theorem does not force native selection
or payment of that schedule's large AF inventory. Neither the strong nor
weak material estimate supplies the remaining field rows or a coupled inverse.

## 6. Finite clock transfer and its limits

Under the stated common representation, bounded-coefficient and true-adjoint
contract, `||E_h||<=C_E h^2` and `||D_1||<=C_D/h` imply

    ||e_N||<=||N|| C_E h^2,
    ||H_(1,N)||<=||N|| C_D/h.

The exact three-term commutator difference consequently has norm at most

    ||N|| ||M|| [4 C_E C_D h+2 C_E^2 h^4].

The factor four comes from the two cross commutators; the factor two from
the quadratic error commutator. The proof and constants are correct. Fixed
count weights and fixed lapse profiles, together with the consumed first
field-jet bounds, also give the stated order h first field derivative.
Spatial differences of fixed counts do not control variations of a physical
volume, preparation or lapse; their chain-rule terms remain separate.

The note correctly distinguishes finite-matrix operator-norm comparison
from convergence to a differential operator on smooth tests. The old
one-sided defect, spin term and Nyquist countercontrol remain. A weighted
positive-form bound for `D*D` is not a proof that the literal stored D is
self-adjoint or an admitted clock. Passive conjugation transports states,
norms and adjoints together; it is not free physical re-preparation.
Variable-frame comparison needs its own continuum frame/connection terms.

Operator norms do not acquire a factor solely from enlarging a spectator
carrier; an unnormalized trace may. The note retains the original owner's
separate trace-dimension, spectral-gap and deeper-schedule conditions rather
than claiming complete Book price convergence from the commutator estimate.

## 7. Acceptance and historical scope

The clarified sentence in `paid_source/PROOF.md` correctly retracts the
overbroad absence claim about a native PF lower bound. The conditional weak
theorem and its old code/results are unchanged. Historical reviews keep the
earlier proof hashes they actually covered; this review accepts the explicit
later PF-premise clarification and the two new applications at the hashes
listed above.

The new coframe residual checker is a narrow exact series/source check.
The PF/clock application is an analytical composition of frozen inequalities
and contains no claimed new numerical replay. The two contributions support
the revised main strategy without claiming an all42 exact root, physical
Book selection, native clock admission or a complete gravitational
constraint algebra. **`GR_closed=false`.**
