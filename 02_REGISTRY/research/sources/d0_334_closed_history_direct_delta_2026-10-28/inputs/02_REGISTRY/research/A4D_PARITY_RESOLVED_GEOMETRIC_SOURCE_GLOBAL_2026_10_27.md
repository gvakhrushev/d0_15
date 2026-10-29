# Exact CAR parity / geometric-source identity on unrestricted holonomies

27 October 2026. SAME existing research owner #334, native-programme-v1.
Input: `28f2e2b0d6f96e073f20a8190f53c615a2a4a8eb`.
Status: exact geometric operator identity, local Lorentz covariance and a smooth C1 error estimate for the UNCHANGED full CAR trace. NOT selection of the complete physical Book action or universal GR closure.

## 1. Existing result consumed and premise removed

The existing `sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/proof.md`, equations (4)–(12), compares

    a(B,P) = -Tr_16[dGamma(B) Lambda(P)]/8

with the original odd-plaquette density

    f(B,P) = -tr_4[B (P-P^-1)]/4.

Its exact first-jet comparison uses the common-null Brinkmann stratum. The present result removes that restriction for the geometric scalar representation, supplies every induced jet, and derives a quantified global smooth limit for the original unmodified amplitude a. It does not silently identify an available geometric readout with the compulsory complete physical price.

Inputs are the SAME four-dimensional Role carrier, its full exterior CAR16 representation, the actual coframe bivector B, and proper-Lorentz plaquette P. No new field or observer is introduced.

## 2. Theorem 1: exact identity for all SL(4) holonomies

Let dim V=4, P in SL(V), B in sl(V). Let N be exterior degree, Pi=(-1)^N and Pi_o=(I-Pi)/2. Then

    Tr_(Lambda* V)[Pi_o dGamma(B) Lambda(P)]
      = tr_V[B(P-P^-1)].                                    (1)

Proof. The odd exterior character is

    Tr_(Lambda^odd V) Lambda(P)
      = tr P + det(P) tr(P^-1).

Differentiate P(t)=exp(tB)P. Since tr B=0 and det P=1, the two derivatives are tr(BP) and -tr(BP^-1). The representation derivative is dGamma(B)Lambda(P). This proves (1), without diagonalizability, a small-loop approximation, nilpotency, or a field equation.

Consequently the original geometric density has the EXACT representation

    f(B,P) = -Tr_16[Pi_o dGamma(B) Lambda(P)]/4.                (2)

This covers every original proper-Lorentz P and Lie-algebra B, and even the larger SL(4) class. Dimension four and oriented volume preservation are hypotheses, not consequences of this theorem.

In the original creator ordering (0,2,3,1), Pi is the existing operator

    Pi = product_(j=0)^3 (I-2 c_j c_j^dagger),

where c_j are creators. Pi_o has rank8, but the entire 16-dimensional carrier remains. A weighted trace is not a physical deletion of the complementary modes or their prices.

## 3. All field derivatives and the actual density map

Equation (2) is equality of functions on their entire matrix domain, not equality only on a solution set. For dP=YP, tr Y=0,

    D Lambda(P)[dP] = dGamma(Y) Lambda(P).

Therefore

    Df = -Tr_16 Pi_o [dGamma(dB)Lambda(P)
                      +dGamma(B)dGamma(Y)Lambda(P)]/4
       = -tr_4[dB(P-P^-1)
                +B(dP+P^-1 dP P^-1)]/4.                     (3)

Composition with the ACTUAL original B(e) and four-edge P(U) gives all16 coframe and all24 proper-link rows at every site, retaining every shared-edge occurrence and the derivative of an inverse link. All higher jets are also preserved. The original two material components are unchanged and must be composed through their own source owner.

Important map boundary: the inverse-leg source has

    B_rs=-(h^2 nu^2/d)N_rs, d=det[u_0,...,u_3].

Outside the old special family d is not constant. All of dB, including this density derivative, must be retained. Equation (3) does not identify B with N or assume det(e)=1 for arbitrary fields. No field-dependent normalization is discarded.

## 4. True local Lorentz covariance, not merely Euclidean unitary conjugacy

Under independently chosen original Lorentz frames L_x,

    U_xy' = L_x U_xy L_y^-1,
    P_x' = L_x P_x L_x^-1,
    B_x' = L_x B_x L_x^-1.

Exterior transport preserves degree; hence Lambda(L_x) commutes with Pi_o. Cyclicity proves invariance of (2), including nonunitary Lorentz boosts. Differentiation gives the finite geometric local-Lorentz Ward identity off shell.

This is a statement about the geometric scalar. It is not an unproved assertion of spacetime-diffeomorphism covariance of every complete Book heat, preparation, trace pairing, or observer state. Those retain their actual transport rules.

## 5. Exact missing term of the old UNWEIGHTED full trace

Define Str X=Tr(Pi X). Elementary even/odd splitting gives

    f = a + Str_16[dGamma(B)Lambda(P)]/8.                     (4)

The supertrace is also the exact character derivative

    Str[dGamma(B)Lambda(P)]
      = d/dt det(I-exp(tB)P)|_(t=0).

Jacobi's polynomial determinant identity, valid even when I-P is singular, gives

    a-f = tr_4[adj(I-P) B P]/8.                              (5)

There is NO inverse of I-P, so common-null and degenerate plaquettes are included.

The correction is genuinely nonzero off the former special class. Take the direct sum of a boost with cosh=5/4, sinh=3/4 and a spatial rotation with cos=3/5, sin=4/5, and let B be that boost generator. Exact rational arithmetic gives

    a=-3/5, f=-3/4, f-a=-3/20.

Thus the old unweighted trace cannot be promoted to an exact global density by naming both expressions geometric. Equation (4), not an assumed equality, is the all-field completion. The old common-null proof remains valid on its stated stratum.

## 6. Theorem 2: global smooth C1 limit of the UNCHANGED native amplitude

For spectral matrix norm in dimension four, exterior degree three gives

    ||adj Y|| <= ||Y||^3,
    ||D adj(Y)[Z]|| <= 3||Y||^2||Z||.

With E=a-f, equation (5) therefore implies

    |E| <= (1/2)||I-P||^3 ||B|| ||P||,                        (6)

and its full differential satisfies

    |DE| <= (1/2)[3||I-P||^2||dP||||B||||P||
                 +||I-P||^3||dB||||P||
                 +||I-P||^3||B||||dP||].                    (7)

This is an actual derivative estimate, not differentiation of a value inequality.

On a bounded smooth coframe/connection class with actual sampled small-loop holonomies, suppose

    B_h=O(h^2), P_h-I=O(h^2),
    D_v B_h=O(h^2), D_v P_h=O(h^2)

uniformly for bounded smooth variations v. Equations (6)–(7) give O(h^8) value and first-source differences on each face. With O(h^-4) actual faces in a fixed four-volume,

    |S_h^(fullCAR)-S_h^(star)| = O(h^4),
    sup_(||v||smooth<=1)
       |D(S_h^(fullCAR)-S_h^(star))[v]| = O(h^4).              (8)

Here S_h sums the actual face densities with B_h ALREADY containing h^2. There is no extra volume weight inserted. Other physical source normalizations must be transported explicitly.

This supplies the original CAR operand itself to the previously owned smooth chiral/Palatini universality route in `A4D_GLOBAL_CHIRAL_GOLDEN_IR_EINSTEIN_HOLST_UNIVERSALITY_2026_10_20.md`, section2. It is not a repetition of the abstract route: (5)–(8) establish its comparison for this actual all-grade CAR character.

For this geometric component one can either use exact representation (2), or keep the original unweighted amplitude and use (8). The second statement requires NO new physical parity insertion. Neither statement proves a raw216 norm bound, controls arbitrary UV variations, constructs exact stationary roots on general metrics, or establishes stability/soundness/recovery of a full nonlinear continuum limit. Such upgrades need their actual norms and hypotheses.

## 7. Explicit internal parity computation and its cost boundary

Four addressed CNOTs from the original four occupancy bits to one fresh internal flag compute parity coherently. On ALL32 columns, the checker proves

    W^dagger W=I, W^2=I,
    i^dagger W^dagger Pi_flag=1 W i=Pi_o.

This is a finite circuit in the already used addressed-CNOT palette, not an external classical observer. Four is the LOGICAL CNOT count, not a claimed total charge for native routing, preparation, comparisons or archive work. The actual gate admission assumptions of that palette remain. Previously sealed records cannot be erased by invoking the inverse circuit.

Physical parity insertion into the complete query was NOT compiled here. In particular, a mathematical spectral projector or a finite flag circuit does not prove that the full Book action chooses a parity-weighted source. The full sixteen grades and all apparatus prices remain in their real carrier.

## 8. Immediate consumer and exact remaining boundary

The existing full cut-bootstrap result proves

    D B_C|Sigma = G_h (D F_h + lambda_- D Q_h), G_h>0,

on its original common-null family. The present theorem leaves that result and its actual physical premises intact; it does not extend its scope by fiat.

Newly completed: the original geometric density has a CAR16 representation on unrestricted proper-Lorentz holonomies, all its induced coframe/link jets, and a true local Lorentz Ward. The old unmodified full trace has a quantified global smooth C1 comparison. Matter still uses its original independent source map.

Still needed for universal physical GR: the selected complete native price must contain/transport this geometric contribution with its actual normalization and other sources, the full executable/field variation image must be admitted, and a controlled joint limit must be proved. No source equivalence of the COMPLETE price follows merely from this geometric character identity. No Einstein equation is inserted into the definition of admission.

## 9. Validation actually executed

Python 3.13.5, SymPy1.14.0 and mpmath90 digits; normal and python -O outputs are byte-identical. The checker uses raised exceptions, not removable asserts.

Exact checks include the original CAR ordering, all six symbolic Lorentz generator contractions, all16 coframe and all24 shared proper-link first rows in one generic homogeneous six-plaquette fixture, four independent Lorentz frames around a loop, the polynomial residual, and all32 columns of the parity flag word. A high-precision smooth sequence controls the value/source rates; the uniform proof is (6)–(8), not inference from samples.

The 40-row fixture is a bounded operator check, NOT a replay of the all-size nonlinear Euler/root owner. The huge READY circuit, original full128 protocol, Lean and CI were not rerun. `universal_GR_closed=false`.
