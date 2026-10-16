# The actual golden record on all sixteen matter components

Date: 12 October 2026. Existing #310, same T0/T1 proof packet.
Input SOURCE: `74d39bb196adf4470a1b058c3e84461acb34443d`.
Canonical main checked: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.

This continues the [matter observer construction](A4D_NATIVE_MATTER_OBSERVER_PAIRING.md)
by binding the **literal** `GoldenCoherentMemory.fullStep`, its price cut and
its blank-record plane to the actual full CAR/exterior fibre. It derives a
complete sixteen-dimensional realization from a unit matter observer and a
nonzero top-grade orientation resource. No independent extra four-component
matter field, replacement gate, new price or chosen spectral remainder is
introduced. The representation and the domain tests are constructive research,
not physical operation admission or a constitutive heat/source theorem.

Two new necessary tests fail for the unrestricted field route. Observer data
alone cannot supply a pointwise covariant realization of the **whole** fixed
record apparatus for full O(1,3). Adding the existing top-grade matter supplies
the required orientation, but its domain, including timelike grade one, is
not preserved by the actual full recording operator. A native closed sector
and the actual joint state/metric transition remain required.

## 1. Exact primitive tuple and its commutant

In the actual core order 00,01,10,11 retain

    U = fullStep(a,p),     P = diag(1,1,0,0),
    P_blank = diag(1,0,1,0),
    a>0, a^2=p, p+p^2=1, p>0.

The blank plane is the owner's input `(u,0,v,0)`, whereas P is the price cut
used in the existing full two-return feedback. They are distinct objects.
Every real matrix commuting with **all three** U,P,P_blank is a scalar.
This is an all-parameter statement for p!=0: the two diagonal cuts force the
commuting matrix to be diagonal; the nonzero p entries of U connect all four
indices and force equality of its four diagonal values. The companion Lean
capsule checks this actual tuple, not a submitted numerical matrix.

Let T have columns `(e00+e01,e10+e11,e00-e01,e10-e11)/sqrt(2)`.
Then the exact identities are

    T^T U T = diag(R_+,R_-),
    R_+ = [[a,-p],[p,a]],    R_- = [[a,-p],[-p,-a]],
    T^T P T = diag(1,0,1,0),
    T^T P_blank T = (1/2) [[I2,I2],[I2,I2]].             (1)

The parity C=diag(1,1,-1,-1) commutes with the gate and price cut, but not
with the blank-record plane. Keeping only U and P misses the preparation
obligation. Two genuine returns use the retained record, not a new blank.

## 2. Why a matter observer alone does not supply the whole local apparatus

At fixed Lorentz q and unit timelike n, the stabilizer in the actual full
Lorentz group is O(3), acting on E=n-perp. The complete native exterior
representation decomposes as

    2 trivial + 2 determinant + 2 standard + 2 determinant-standard. (2)

The scalar terms are grades 0 and the n part of grade 1; the determinant
terms are spatial grade 3 and grade 4. The vector terms are spatial grade 1
and n-wedged grade 2; the axial terms are spatial grade 2 and n-wedged grade 3.
Each displayed multiplicity is **two**, and every native grade is retained.

A full local factorization `Fock16 = apparatus4 tensor spectator4`, with
the same fixed U,P,P_blank acting on apparatus4, would require the O(3)
representation to act through their commutant, i.e. as I4 tensor R.
All its irreducible multiplicities would therefore be multiples of four,
contradicting (2). Even a single covariant faithful apparatus4 subspace is
impossible: its stabilizer action would be scalar by Section 1, whereas both
one-dimensional characters have multiplicity only two in the native fibre.

This is a **pointwise natural binding** obstruction from q,n alone. It does
not exclude a history orientation resource, multiple-site addressing,
additional retained field data, an explicitly oriented proper-Lorentz
sector or another independently admitted operational representation.
It is not a whole-core no-go and does not change the parent terminal.

For SO(3) the determinant distinction disappears: the native fibre is
`4 trivial + 4 standard = R4 tensor (R + E)`. An actual orientation resource
therefore permits the full local construction, rather than a dimension-only
identification of the primitive apparatus with four chosen coefficients.

## 3. Full CAR construction using existing top-grade matter

Use v=P1 m, k=v^T q^-1 v>0, n=v/sqrt(k), and the previously derived
positive G=Q^-1. Let S=C_*(G) be the undensitized full exterior Gram.
The existing heat weight is W=omega S, omega=sqrt(abs(det q)); the scalar
factor does not alter fibre adjoints or the construction below.

On the additional open sector m^4!=0 put

    Omega = m^4 / sqrt(<m^4,m^4>_S),
    volume_E = contraction_(G n)(Omega),
    K_spectator = R + E.

The orientation comes from an existing component of **the same full matter
field**. It is not supplied as an external sign, removed as gauge or inferred
from the timelike line. At this stage it is a resource premise on the sector,
not a theorem admitting that sector physically.

For scalar spectator 1 use the four orthonormal columns

    1,             n,              volume_E,        Omega.

For a G-unit spatial vector w use

    w,             n wedge w,      star_E w,        n wedge star_E w. (3)

These four rows, each on K_spectator, give a full isometry B from
`R4 tensor (R+E)` to all sixteen exterior components. The spatial Hodge in
(3) is determined by G and volume_E. A change of orthonormal basis of E acts
only on K_spectator and commutes with every operator in (1), so the resulting
operators are independent of that basis. Exterior naturality and normalized
top matter give covariance for all invertible coordinate maps, including
orientation reversals. A nonzero top grade is essential to that statement.

With B^dagger=B^T S define

    U_F = B[(T^T U T) tensor I_K]B^dagger,
    P_F = B[(T^T P T) tensor I_K]B^dagger,
    Blank_F = B[(T^T P_blank T) tensor I_K]B^dagger.     (4)

Every native component participates; this is four complete copies of the
literal apparatus, not an operator on four components with twelve discarded
rows. U_F is S-orthogonal (and W-orthogonal). Both projections have rank eight.
The operator mixes form degrees. It is a representation of the record gate,
**not** the number-preserving affine/Lorentz link D_e or its cochain lift.

At rest q=eta,n=e_A,Omega=e_A wedge e_B wedge e_C wedge e_D, the columns in
(3), ordered by row and spectator 1,B,C,D, have occupation masks

    row 0: 0,2,4,8;      row 1: 1,3,5,9;
    row 2: 14,12,-10,6;  row 3: 15,13,-11,7.            (5)

The minus signs denote coefficients, not negative mask labels. This signed
permutation exhausts all sixteen states. Creation along n and its S-adjoint
give exactly both n-wedge maps in (3), consuming the literal CAR/exterior
operators. No spinor or particle identification is claimed.

## 4. Complete one-frame price and its joint derivative

For two returns at the **same prepared tuple** and its fixed pairing,

    F2=P_F (U_F^2)^dagger (I-P_F) U_F^2 P_F.

Its eigenvalues are 4p^3 four times and zero twelve times. Thus

    det(I16-zF2) = (1-4zp^3)^4,
    J2 = -4 log(1-4zp^3),    0<4zp^3<1.                (6)

All zero factors and all sixteen rows are included. At fixed existing p,z,
every q/m first jet of this one-frame prepared feedback price is zero on
the stated open sector; this is exact constancy, not a zero-jet extrapolation.
The full N-site block construction multiplies J2 by N without installing a
new normalization. A shared operator-frame change cannot supply the missing
order-one eigenphase remainder merely because B moves with matter.

This does not silently equate (6) with a **state-conditioned chronological**
program `U_F(q,m_next) U_F(q,m)`. That program first needs a genuine admitted
joint transition, endpoint-pairing transport, its actual blank/reference
and full price. Treating the updated field as input to the next gate is an
additional, testable step. The following exact controls kill the unrestricted
fixed-q attempt.

## 5. Full-domain tests for the actual record-induced matter update

Consider the candidate transition `m_next=U_F(q,m)m`, with q fixed, rather
than assigning its derivative independently. At rest the same-fibre input

    m=e_A + 2(e_A wedge e_B) + 2(e_A wedge e_C wedge e_D) + Omega

has timelike grade one, nonzero top grade and S norm squared ten. It lies in
the actual whole blank-record plane: `Blank_F m=m`. Thus the domain test
uses an allowed input of the literal blank-record preparation, not just an
arbitrary nonblank vector.
After the literal full gate (4),

    (m_next)^1 = a e_A - 2p e_B,
    ((m_next)^1)^T eta (m_next)^1 = a^2-4p^2=p-4p^2<0. (7)

The actual golden identities imply p>1/2, so (7) is strictly negative.
Dividing the whole state by sqrt(10) gives a genuine normalized input and
normalized output and retains the sign. The full gate is unitary; the
observer's timelike domain is not invariant under it. Dropping grade two
would hide precisely the term that causes the failure.

There is an independent orientation-domain failure. The valid input

    m=e_A -(a/p) volume_E + Omega

has timelike grade one and nonzero top grade. The same gate gives
`(m_next)^1=a e_A`, but `(m_next)^4=0`. The orientation information remains
in grade three, whose coefficient is `-a^2/p-p=-1/p`; unitarity has not
erased the full state. A rule using the current top grade alone no longer
defines its next blank plane. Recovery from history or other grades must
be actually constructed, not assumed as an uncharged reset or hidden sign.

Inputs violating these physical-looking sectors have not been silently
removed from native matter. These are exact finite **representation tests**,
not assertions that every tested state is a physically admitted preparation.
The converse is also explicit: physical admission excluding them, or an
owned joint q/link update restoring the sectors, has not been derived here.
Such a law cannot be selected solely to repair (7).

The mismatch is not confined to leaving k>0. The actual blank input
`m=e_A+(e_A wedge e_B)+(e_A wedge e_C wedge e_D)+Omega` has norm squared
four. Its output has grade-one vector `a e_A-p e_B`, Lorentz square
`p-p^2=p^3>0`, and nonzero top grade `-a Omega`. Nevertheless its positive
Q changes from I to `-eta+2vv^T/p^3`. The old record operator preserves the
initial pairing but is not an isometry from that pairing to the new one.
Thus even this regular state-conditioned second step cannot be equated with
the one-frame square used in (6). The actual endpoint-pairing/metric
transition must be derived; neither a reset nor a chosen compensating q
update is installed by this calculation.

## 6. Proof status and the next required arrow

The paired checker binds the actual core tuple, constructs every full CAR
column and degree, checks nonrest positive metrics, both orientation signs,
spatial-frame independence, full sixteen-dimensional covariance, projector
ranks and the complete determinant. It executes the two normalized sector
failures and compares frozen/reference/reset alternatives. The Lean capsule
proves the literal tuple's scalar commutant and the strict golden sign in (7).
The all-group multiplicity argument, exterior factorization and price
constancy are analytic with exact controls, not new supported CORE owners.

The next T0 obligation is a genuine **closed common preparation** on the
full joint carrier, including the state/record/metric transition, retained
orientation memory and all full-price arguments. This construction supplies
a concrete same-fibre representation to test; it does not claim an apparatus
compiled from M1 or a physically executable field-dependent gate. On that
actual transition derive the complete operator/pairing/chronological price
jet before comparing a source. Physical heat selection, source/Ward,
contrast/refinement, native Euler solutions and G1-G4 remain open. The full
goal and all original #310/#202/#317 terminals are unchanged.
