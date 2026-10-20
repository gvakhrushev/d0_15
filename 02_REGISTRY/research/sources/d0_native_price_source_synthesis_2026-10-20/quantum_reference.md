# Exact coherent relative-reference price: quadratic weak-reference source

Independent source-bookkeeping supplement to `paired_feedback.md` §8, within existing #334. This is an accounting theorem for a specified quantum relative price, NOT a physical selection of Info or a replacement for the complete H+J+R action.

Let S0(y) be a real skew d×d matrix on a bounded C² field chart and set

    S=σS0, D=(I+σ²S0²)^(1/2),
    Rσ=[[σS0,D],[-D,-σS0]],
    ρin=diag(I_d/d,0).

Assume a uniform strict contraction margin, and hold σ fixed under field variation. Rσ is the same orthogonal quarter turn used by the paired feedback. Its COMPLETE coherent output, without measuring or dephasing the reference port, is

    ρσ=Rσ ρin Rσ^T
       =(1/d)[[σ² A, -σS0 D],
               [σD S0, I−σ² A]],       A=S0 S0^T=−S0².      (1)

Its eigenvalues are d copies of1/d and d zeros, so Tr(ρσ logρσ)=−log d EXACTLY. There is no entropy singularity from the moving zero eigenspace.

Supply one FIXED faithful reference operator, block diagonal in the actual natural reference cut,

    μ=diag(μ_U,μ_L)>0, Tr μ=1.

μ_U and μ_L need not commute with S0 or A. Since logμ is block diagonal, the off-diagonal coherences in (1) contribute zero to Tr(ρσ logμ), without being discarded. The full Umegaki relative price therefore obeys the exact identity

    D(ρσ||μ)
      = −log d−(1/d)Tr logμ_L
        −(σ²/d)Tr[A(logμ_U−logμ_L)].                    (2)

For the Golden code reference μ_U=p I_d/d, μ_L=p² I_d/d, division by logφ gives particularly

    D_phi(ρσ||μ)=2−(σ²/d)Tr A.                         (3)

This is also the original mean cost1/2 for the natural upper/lower branches. Equation (3) is a concrete SAME fixed-prior relative-price identity, not a proof that native acquired Info selects that quantum relative price.

Every first and second y derivative of (2) is O(σ²), uniformly on the bounded chart. Unlike fine-pointer Shannon, no positive floor for individual A_jj is needed: the entire quantum entropy is constant and the reference log is fixed. Thus, IF this is the actual declared reference charge, σ_h=h³ gives relative source O(σ_h/h²)=O(h) against the paired Palatini scale σ_h h², with full coherence retained.

For a more general fixed input τ on the upper block, possibly entangled with an explicitly retained spectator, the complete output has diagonal blocks σ² S0 τ S0^T and D τ D. Its spectrum remains that of τ. Against any fixed faithful reference block diagonal in the SAME port (acting also on the spectator if present), expansion D=I+(σ²/2)S0²+O_C²(σ⁴) gives the same O_C²(σ²) source bound, though the exact quadratic formula (2) need not hold. A moving input or moving μ adds its own full source; its flat term cannot be declared constant.

## Hostile off-block reference: a real linear source

Block diagonality is substantive. For d=2 let J=[[0,−1],[1,0]], S0=xJ and

    O=[[0,J],[-J,0]],   O^T=O, O²=I4,
    μ=(I4+(3/5)O)/4 >0.

Then logμ=−log5 I4+log2 O. The exact coherent state (1) satisfies
Tr(Oρσ)=−2σx sqrt(1−σ²x²), so

    D(ρσ||μ)=log(5/2)+2log2 σx sqrt(1−σ²x²).            (4)

Its x derivative is 2log2 σ+O(σ³). This is an O(σ) unwanted source, which does NOT vanish relative to σh². Therefore the natural-cut/fixed block-diagonal reference must be part of the real accounting hypothesis. The complete coherent state itself differs from its σ=0 state at orderσ; one cannot extrapolate pointer probabilities of orderσ² to arbitrary quantum functionals.

The construction is compatible with the independently executed calibration factor in structural §8: no intermediate which-arm label is copied from the unknown coherent data. It does not show that calibration price equals the physical cost of the reference used inside the main word.

Checker: `check_quantum_reference.py`. It checks the full coherent matrix, constant spectrum through its scaled-projector identity, the exact quadratic relative price with general block-log operands, the original Golden cost formula, and the faithful off-block hostile control. No physical Info selection.
