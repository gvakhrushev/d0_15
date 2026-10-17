# Relative full-record principal angles and alternating Born history

**Consumer:** existing EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, Draft #334.
**Primary:** [A4D_RELATIVE_RECORD_PRINCIPAL_ANGLES_AND_MOMENTS.md](../../A4D_RELATIVE_RECORD_PRINCIPAL_ANGLES_AND_MOMENTS.md).

## Proven mathematical interfaces

- Two full-column-rank raw maps X0,X1:H→K define positive Grams Gi=Xi†Xi and canonical **subspace** projectors Pi=Xi Gi^-1 Xi†. The relative overlap C=(X1 G1^-1/2)† X0 G0^-1/2 has eigenvalues cos(theta_j) in the singular-value sense; det(C†C)=∏cos²(theta_j). These eigenvalues and the logarithmic comparison price depend on relative image subspaces, not independent inner weights of endpoint records.
- Put F=J0†(I−P1)J0=I−C†C. Alternating complete Lüders projective outcomes Q1=(I−P1), P0, Q1, P0,... on the **same full comparison carrier** give exact prefix probabilities Pr_n(ρ)=Tr(ρ F^n) for every n. Other outcomes are retained in the full protocol. No Schur-pivot scalar preparation, eigenvalue oracle, negative cycle-as-event or Fock extension.
- The peer strictly positive golden comparison gives p(1−z)^3 I≤C†C≤pI, z=2^-20, p=φ^-1. Therefore E=I−C†C/p=(F−p²I)/p has 0≤E≤δI, δ=1−(1−z)^3. The identity
  −log_φ det(C†C)=d+(1/log φ)Σ_(k≥1)Tr(E^k)/k
  has a tail ≤d δ^(m+1)/[(m+1)(1−δ)log φ] and a true noncommuting first source tail ≤d δ^m||dE||/[(1−δ)log φ].
- All E moments are algebraically obtained from the positive alternating-prefix F moments:
  Tr(E^k)/d=p^-k Σ_(j=0)^k binom(k,j)(−p²)^(k−j)Tr(F^j)/d.
  The absolute coefficient sum equals **(sqrt5)^k exactly** from the original golden p²+p=1. Signed coefficients occur only in classical postprocessing; they are not Born outcomes. With m=O(log(1/h)), sample resources are polynomial *conditional on independent basis preparations, measured projectors and real controlled source jets*.
- Horizontal input-frame gauge gives a sharper uniform metric-source transfer:
  ||dE[V]||≤(2||dP0[V]||+||dP1[V]||)/p.
  If the **actual native** subspace derivatives on the full field chart obey 2||dP0[V]||+||dP1[V]||≤B h^-r ||V||_(raw,l∞), then for d_h=O(h^-4) the original-style h^-2 **spectral truncation** source error is O(h^(-6-r)δ^m), with logarithmic moment order. The needed bound is NOT implied by spectral confinement, and spectral truncation source is not the original #216 E_Q(K)-E_Q(K_sm) gap.

## Reproduce exact finite controls

The dependency-free JavaScript helper uses native BigInt fractions (numerator/denominator reduction on every operation) and works in Node's ECMAScript modules:

    node 02_REGISTRY/research/sources/d0_relative_subspace_moments_2026-10-17/check_alternating_projection_moments.mjs

For an explicitly non-native rational 3D input in an ambient 6D, it tests two exact isometries and their real moving field jet, F=J0†(I−P1)J0, the source dF from dP1, genuine [F,dF]≠0, *six* path probabilities and *six* first sources. Published script blob SHA 8e3c5aec75cc6ec6065ed207f8d2ce1110e52911 was retrieved from the GitHub branch. The exact posted source was executed via ECMAScript V8 in the current session (with console output redirected to the test runner); **18/18 exact rational controls passed**. Deterministic [RESULT.json](RESULT.json) retains the exact fractions and verification scope. This is neither a remote Node CI result nor a full16 native-science replay.

## Single actionable admission gate

Compute J0,J1 / P0,P1 for one actual common-carrier native paired retained-history process (including reference128 and all16 grades). Before any GR comparison, check whether **both sharp Lüders range tests** are admitted by the actual golden/Julia instructions with old tape retained, and whether their differentiated source is the real costed native Cost−Info test/cut. The two isometric subspaces of a mathematical comparison do not prove this admission. If the projector requires a forbidden old-memory rotation, record the exact failure and do not treat the scalar logdet representation as the native action.

No new operator law, physical action, source stress, dimensional reduction, task, CORE/BOOK claim or full h^-2/#216 terminal is installed.

## New exact native-port selection controls

The proof memo now has a stronger **kill-first / constructive pair**, §§9–10:

* Whole-output port-only SO(2) golden rotation is exactly source-BLIND. From the actual W=W†=W^-1 and native port K0=pI+p²W, K1=sqrt(p)p(W−I), every full one-round Stinespring J obeys J†(G_port⊗I)J=sqrt(p)I, where G_port is the original golden real rotation. No curvature, matter or archive motion changes that overlap; −log_phi determinant is exactly the fixed carrier dimension. Neither cherry-picked label nor discarded failure is permitted in this inference.
* A different **signed native-port comparator** is source-sensitive. Let E_port1 be the actual complete original port1 effect (already owned exact: E_port1=p epsilon_h Delta_h), Z_port the fixed (+1/−1) output-port contrast, and add one orthogonal fully retained golden branch with amplitudes sqrt(p),p. Two full-isometric comparison images J_A=(sqrt(p)J,pJ) and J_B=(sqrt(p)J,p Z_port J) have

      C_signed=J_B†J_A=I−2p² E_port1=I−2p³ epsilon_h Delta_h.

  Since 0≤E_port1≤I, the cross operator is **uniformly positive** p³I≤C_signed≤I. For this *constructed mathematical comparison* its full source is

      d[−log_phi det(C_signed²)] =
      (4p²/log(phi)) Tr(C_signed^-1 dE_port1).

  The native full port effect, including all literal output labels, is real data: the relative comparison is NOT selected as physical Cost−Info, and coherent placement of Z_port on the retained output needs its own legal gate/price. Moreover this single positive-Delta channel is NOT Lorentz 4D−2×3D Einstein action; the merged #360 positive-A2 vs Lorentz source control still applies.

Exact locally reproduced / published source scripts (dependency-free Node-compatible JavaScript using the original golden quartic ring Z[a]/(a^4+a²−1), p=a²):

    node 02_REGISTRY/research/sources/d0_relative_subspace_moments_2026-10-17/check_native_port_only.mjs
    node 02_REGISTRY/research/sources/d0_relative_subspace_moments_2026-10-17/check_native_signed_port.mjs

The first script was fetched and evaluated in V8 with **31/31 exact checks** across six W/M pairs, retaining isometry and exact G-port scalar overlap. The second published blob SHA 8ef79a78bca44f136d3ebc261ea7ede0aa2e069b was fetched and evaluated in V8 with **58/58 exact checks** across the same six finite cases, full positive two-branch maps, exact p³ positivity identity and an actually nonzero first determinant jet from an independently varied M. The witness is a finite quartic matrix fixture, not a literal full16 native coframe root. The actual original native E_port1 formula is separately pinned to its existing proof; remote Node/CI and independent scientific acceptance are not claimed. The deterministic receipt is SIGNED_PORT_RESULT.json.

**Next physical gate:** Do not search more universal golden port rotations. Establish actual two-sided **spatial versus four-dimensional** record image subspaces (or reject their admissibility on the old tape); verify cross K, full gate/clock/Cost−Info first source and full Lorentz Ward, then compare against original all-ten raw h^-2 task. A port-only source-sensitive comparator is a genuine native-data bridge but not an Einstein-action selection.
