# Exact flat joint Ward and quarter-wave normal reduction

Existing SOURCE #310; no new task, physical law, or CORE/BOOK promotion.
Scientific input: supplied full L=4 sheet package and its literal symbol;
remote read `bdbac63270a52b3da3e3348502682a8fc48459b8`.

[Proof and scopes](sources/d0_joint_lattice_ward_resonance_2026-10-15/RESULT_RU.md)
[Exact verification](sources/d0_joint_lattice_ward_resonance_2026-10-15/verify.py)

The complete 34-component naked-star quadratic symbol annihilates an explicit
four-component backward coframe/forward connection-compensation lift at every
complex nonzero character. The dual identity is an exact linear-source Ward
identity on every periodic mesh. It is not nonlinear finite diffeomorphism
invariance, nor the previously rejected exact forward affine lift.

At the genuine phase (1,i,i,1), rank H=22, rank[H|C]=23 and rank J=28.
A canonical range inverse of the full J obeys ||R||_p <= (7+4sqrt(2))/3 < 5.
Six source compatibility rows remain: four translation-null and two others.
Near that phase an exact Schur map leaves two critical coordinates after
accounting for the four exact quadratic-null directions. Its first coefficient
is 2(k1+k2)diag(1,-1)/7. On k1+k2=0 the second coefficient is the full matrix
[[k0^2-3k1^2,-k0*k3-k1^2],[-k0*k3-k1^2,k3^2+5k1^2]]/7.
These give O(h^-1) or O(h^-2) modal inverse bounds under explicit
noncharacteristic conditions, including actual modes on L in 4N.
No full-torus bound, nonlinear refining curved sheet, or full GR is claimed.

81 exact checks, seven executed mathematical mutants, ordinary/optimized replay;
optional independent full-action autodifferentiation and remainder diagnostics
are explicitly floating-point, not interval proofs. The previous complete L=4
interval packet was replayed separately, including all 16 Bloch sectors.
Original #310/#202/#317 and the independent CONTROL snapshot are unchanged.
