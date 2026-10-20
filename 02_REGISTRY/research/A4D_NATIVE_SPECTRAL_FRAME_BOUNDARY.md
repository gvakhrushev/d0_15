# Native spectral completion: frame descent and an actual curved action obstruction

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310.
Input: `080cb15ceb6b273f1f4bb5ccaae50251307d257b`.
CONTROL/main baseline: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Status: **scoped constitutive/action obstruction**, not full core exhaustion.
Positive GR and global closure remain OPEN.

`A4DConstitutiveKernelClassification` independently defines

    Q_alpha(H) = I + H + alpha H^2,
    squaredFluxEnergy(alpha,H,psi) = <psi,Q_alpha(H)psi>/2.     (1)

It supplies a symmetric H and leaves alpha unselected. A separate owner,
`A4DDiscreteEnergyKernel`, constructs the real symmetric `fluxHMatrix N e`.
Here we evaluate (1) at that existing matrix to test this specific candidate
binding. We do not claim the kernel owner already selected this physical
map, replace H by a fitted physical operator, add a density, or install a
new native action/on-shell gate. Other maps into its abstract H slot remain
separate obligations.

The result is stronger than failure of one coefficient. **No nonconstant
scalar spectral function f(H) can pass the stated exact raw-frame descent
test on the declared full class.** For (1) there is also a quantitative
obstruction uniform in alpha and lattice size, on two fixed, genuinely
curved smooth background metrics. This is a necessary covariance test,
not an Einstein equation or an on-shell example.

## 1. Bind the spectral calculation to the literal native matrix

On the real cochain carrier of size 16 L^4, L=N+2, let v be the actual
constant scalar cochain: one in the empty Fock component at every site,
zero in the other 15 components. For every constant coframe e the capsule
proves the literal identities

    fluxHMatrix(e) v = tr(e) v,
    Q_alpha(H) v = (1+s+alpha s^2) v       when H v=s v,
    squaredFluxEnergy(alpha,H,v)
        = (1+s+alpha s^2) ||v||^2 / 2.                       (2)

The scalar occupation vector is the actual exterior-algebra unit and is
fixed by the owned exterior frame lift, as compiled in the preceding
[reference-weight capsule](certificates/a4d_native_reference_weight.lean).
The current checker verifies that capsule's source/output hashes as well.
Thus a scalar spectral function has the unavoidable scalar readout f(tr e).
For a general f this statement is the declared eigenvector functional-
calculus condition, not a new supported Lean spectral-calculus owner.

The same new capsule proves symmetry of the actual flux matrix at arbitrary
site-dependent e and the exact square form

    S_alpha(H,v) = (||v||^2 + <v,Hv> + alpha ||Hv||^2)/2.      (3)

This will permit a curved test without pretending that v remains a
constant-eigenvalue eigenvector on a varying background.

## 2. Two frame orbits force any scalar function to be constant

Use the actual raw solder Theta=eta+e, eta=diag(1,-1,-1,-1), and right action
Theta -> Theta Lambda. Its raw Gram is Theta eta Theta^T. Set

    Theta_minus = diag(1,-2,-1/2,-1/2), det=-1/2,
    Theta_plus  = diag(2,-1,-3/2,-3/2), det=-9/2.

Both are nondegenerate and have tr(Theta-eta)=0. Use the A/B boost with block
[[a,b],[b,a]], a>=1 and b^2=a^2-1, and identity on C,D. It is proper and
time-oriented: det Lambda=a^2-b^2=1 and Lambda_AA=a>=1. The generic Lorentz
identity and existence of b=sqrt(a^2-1) compile in Lean. Direct evaluation gives

    tr(Theta_minus Lambda-eta)=1-a,
    tr(Theta_plus  Lambda-eta)=a-1.                           (4)

These are two complete half-lines meeting at zero. Frame descent therefore
implies f(s)=f(0) for every real s: use a=1-s when s<=0 and a=1+s when s>=0.
**No continuity, analyticity, polynomial degree bound or finite-sampling
extrapolation is used.** `scalar_descent_forces_constant` proves this statement
with arbitrary f and the explicit connected A/B boost family as hypotheses.

This is a necessary scalar test only. A constant f does not automatically
supply a physical action: a constant identity counting weight still changes
a one-form's squared norm under the nonorthogonal exterior boost. The exact
control gives norm change 9/8 for a unit A one-form at a=5/4,b=3/4.

The admitted class must contain these two full frame orbits and the scalar
sector with its actual frame action. Restricted fields, independently owned
constraints/readouts, extra terms, or a different H(e) map are outside it.

## 3. Uniform obstruction for the existing quadratic spectral family

For p_alpha(s)=1+s+alpha s^2, the fixed rational boost a=5/4,b=3/4 gives

    D_minus = -1/4 + alpha/16,
    D_plus  =  1/4 + alpha/16,
    max(|D_minus|,|D_plus|) >= 1/4.                           (5)

The bound is sharp at alpha=0 and is compiled on the actual matrix readouts.
Since ||v||^2=L^4, the corresponding normalized owned action S/L^4 has
maximum defect at least 1/8. Any mesh-dependent alpha_h retains the same
bound. Fixed nonzero calibration and O(h) endpoint recording errors cannot
remove it.

For the constant scalar readout its coframe covector is p_alpha'(tr e) I.
At the two boosted frames the same vertical A/B tangent yields

    V_minus = -3/4 + 3 alpha/8,
    V_plus  =  3/4 + 3 alpha/8.                               (6)

Their difference is 3/2 for every alpha. The checker verifies all ten Gram
Jacobian rows, all sixteen covector entries, and the off-diagonal packed
factor two in K=2 T Theta eta. The Gram Jacobian has rank ten and kills
these vertical directions; adjoining a nonzero tested covector gives rank
eleven. Calling the readout derivative a fitted metric stress cannot erase
this obstruction. No physical matter source is defined by that covector.

The effect also occurs arbitrarily near the flat coframe. For
e_delta=diag(0,-delta,0,0), the exact boosted difference is

    (a-1) delta [-1 + alpha delta(a+1)].                       (7)

For each fixed alpha, choose a>1 close to one and then small nonzero delta.
The defect is nonzero while both frames approach the flat coframe. The
finite weights can be kept positive by continuity at Q_alpha(0)=I. For
alpha>1/4 the existing owner already proves strict positivity for every
symmetric H, so positivity does not repair the global frame failure.

## 4. Fixed genuinely curved probes at every L in 4N

Take the same two constant solders, but now use the independent smooth
coframe profiles on the unit periodic four-torus

    rho(x)=1+cos(2 pi x_C)/10,
    Theta_±(x)=rho(x) Theta_±,
    g_±(x)=rho(x)^2 Theta_± eta Theta_±^T.                    (8)

rho lies in [9/10,11/10], so both metrics are uniformly nondegenerate.
Applying the same constant proper boost preserves each g_± pointwise.
These are exactly sampled raw coframes, with v still the constant scalar
field. They are not declared native joint solutions.

Let A_C rho(x)=[rho(x)+rho(x-h e_C)]/2. The actual, generically compiled
scalar block from the preceding capsule gives

    H(e_-)v = scalar(m_-),  m_-=2-3rho/2-A_C rho/2,
    H(e_+)v = scalar(m_+),  m_+=2-rho/2-3A_C rho/2.

The boosted scalar blocks are m_- - rho/4 and m_+ + rho/4. Formula (3), not
an assumed eigenvalue formula on variable e, now computes the action exactly.
The finite geometric-series identities give, for every L>=3,

    mean rho = 1,
    mean rho^2 = 1+1/200,
    mean(rho A_C rho) = 1+(1+cos(2pi/L))/400.

They follow by summing the nonconstant characters of frequencies one and
two; those characters are nontrivial at all L in 4N. With q=cos(2pi/L), put

    b_-=(215+2q)/3200 >= 213/3200 > 0,
    b_+=(191-6q)/3200 >= 37/640 > 0.

The exact normalized action defects are

    Delta S_-/L^4 = -1/8 + alpha b_-/2,
    Delta S_+/L^4 =  1/8 + alpha b_+/2.                       (9)

For alpha>=0 the second is at least 1/8; for alpha<=0 the first is at most
-1/8. Thus the sharp maximum absolute defect is again **at least 1/8**, for
every alpha and every L in 4N. The positive-coefficient inequality is compiled;
the all-size coefficients use the explicit finite character calculation.
Independent exact site controls cover L=4,8,12,16, without using them as the
proof of the all-size assertion.

Curvature is checked separately. For constant g0 and g=rho^2 g0 in four
dimensions, direct computation of all 64 Christoffels and 16 Ricci entries
gives R=-6 rho''/(g0_CC rho^3), in the usual coordinate Ricci convention.
At x_C=0 the two scalar curvatures are -9600 pi^2/1331 and
-3200 pi^2/3993. In particular both backgrounds are genuinely curved.
The sign convention does not affect their nonzero curvature. No connection
Euler equation, native on-shell status or physical realization is inferred.

## 5. Protected exceptions and verification

The arbitrary-function theorem concerns exact frame descent for a fixed f.
It does not imply a uniform asymptotic obstruction for every sequence f_h.
For example, the external logical control f_h(s)=1+h sin(s/h) has f_h(0)=1
and f_h'(0)=1 while |f_h(s)-1|<=h for every s. Its scalar frame defects are
at most 2h. It is not adopted as a native law or positive GR realization.
A shared flat first jet alone does not exclude collapsing spectral responses.
In contrast, the owned quadratic family retains the uniform bound (9).

A second hostile control is 1+s-16s^3: it passes the two scalar samples
s=±1/4 but is nonconstant and fails another point on the same frame orbits.
Thus two finite probes prove (5) for the quadratic family, not the theorem
for arbitrary f. Field-only roots also are not joint solutions: at alpha=0,
s=-1 the kernel value vanishes while its coframe derivative does not.

The [Lean capsule](certificates/a4d_native_spectral_frame.lean) compiles
fourteen propositions with 58 transitive D0 source pins and only propext,
Classical.choice and Quot.sound. [Output](certificates/a4d_native_spectral_frame_output.txt)
and [receipt](certificates/a4d_native_spectral_frame_results.json) preserve the
actual kernel results. The [checker](certificates/a4d_native_spectral_frame_check.py)
and [ledger](certificates/a4d_native_spectral_frame_certificate.json) run 57
exact grouped controls and bind the
actual operators, all metric slots, exterior action, curved samples and
curvature computation. Immutable replay must reject a falsely zero action gap.

The result excludes a concrete nonlinear completion of the actual flux
operator on the stated frame/field class. It does not exhaust all native
shape-sensitive actions or supplied operator maps. Native action/variation
and refinement transfer, own source/Ward, curved joint existence, soundness,
recovery and the original #310/#202/#317 terminals remain open.
