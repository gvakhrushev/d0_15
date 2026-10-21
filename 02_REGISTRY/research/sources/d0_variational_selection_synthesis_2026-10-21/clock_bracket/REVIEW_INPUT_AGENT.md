# Independent analytical review: native lapse bracket

Reviewed `check_clock_bracket.py` and `PROOF.md` in the bounded synthesis
packet. Reviewer: input-stationarity lane, independent of the bracket
derivation. Verdict: **PASS at the stated constant-frame kinematic scope**.
This is not approval of physical clock admission, a complete deformation
algebra, or D0 to GR closure.

Reviewed SHA256 pins:

* checker: `21728357ea286ae9d335f3c7cf8388fab0455438b816d344bd8098cad39b3bdd`;
* proof: `339ce4422f220d0dac6cc8617e540293fc6dd1bfb2f56515c4abaaa3826e2c0e`.

## 1. Coefficients and signs independently derived

Set `H_N=-i A_N`, with
`A_N=N alpha^i partial_i + a alpha^i N_i`, and
`{alpha^i,alpha^j}=2q^{ij}I` for constant q. Write
`W_i=N M_i-M N_i`. Direct composition gives the first-order coefficient
of `[A_N,A_M]` as

    [(1-a)alpha^i alpha^j+a alpha^j alpha^i]W_i
      = q^{ij}W_i I+(1/2-a)[alpha^i,alpha^j]W_i.

The genuine adjoint indeed forces a=1/2 for real nonconstant N on the
compact-support domain. The Hessian-of-lapse multiplication term is
`(N q^{ij}M_ij-M q^{ij}N_ij)/2 = div(V)/2`, with
`V^j=q^{ij}W_i`. The gradient-product term is
`a^2 [alpha^i,alpha^j]N_i M_j`, hence exactly
`(1/4)[alpha^i,alpha^j]N_i M_j`. The overall minus is required by
`(-i)^2=-1`. No factor of two or missing half-density term was found.

The constant-frame extension is valid with
`alpha^i=E_a^i alpha^a`, `q^{ij}=sum_a E_a^i E_a^j`. The positive
spatial q and real E are essential to the Hermitian interpretation; this
does not construct Lorentzian time or permit a variable frame to be
substituted while ignoring its derivative and connection terms.

## 2. Native stencil and replay

The actual one-sided stencil is
`c_i(T_i-I)/h+c_i^*(T_i^-1-I)/h`; it is self-adjoint on the periodic
counting inner product because the two shift differences are adjoints.
Its expansion is

    (c_i-c_i^*)partial_i
      +(h/2)(c_i+c_i^*)partial_i^2+O(h^2).

Thus the proof correctly keeps the nonzero O(h) defect. Its C4 smooth-data
bound on a common collar is sufficient. It does not imply uniform
operator-norm convergence, as the explicit pi/h mode already shows.
The polynomial fixture checks a nontrivial example on all16 components;
the general theorem is the analytical calculation above, not the fixture
alone. The physical source/refinement norm remains separate.

Independent run:

    PYTHONPATH=/tmp/d0_synthesis_python OPENBLAS_NUM_THREADS=1 \
      python3 /tmp/d0_clock_bracket_synthesis/check_clock_bracket.py

passed all55 assertions implemented as active checks. Output is preserved
in `REVIEW_REPLAY.json`. No old large suite, input optimizer, or Lean build
was rerun.

The heat-control statement is also correct: for
`L_N=-(N partial_x^2+N'partial_x+N''/2)`, the coefficient of
`partial_x^3` in `[L_N,L_M]` is exactly `2(N M'-M N')`. It fails the
desired first-order spatial-deformation test in this candidate class.

## 3. A sharper exact boundary: the frozen metric fails the other bracket

The packet correctly says that its normal-normal identity is not a full
HKT algebra. This can be made explicit rather than left as a generic caveat.
For flat q=I put

    L_V=V^i partial_i+div(V)/2
          +(1/8)[alpha^i,alpha^j]partial_i V_j.

For `V=N grad M-M grad N`, the spin term in L_V equals the packet's
Omega exactly. On a **frozen frame**, however, the principal part of the
shift-normal commutator is

    [L_V,H_N]_principal
      = -i [(V dot grad N)alpha^j
             -N alpha^i sym(partial_i V_j)]partial_j.

The second term is a genuine strain defect. It cannot generally equal
the principal part of `H_(V dot grad N)`. An exact example already generated
by the packet's lapse brackets is N1=1, M1=xy, giving
`V=(y,x,0)`, `divV=0`, and spin=0. For another constant lapse N=1,

    [y partial_x+x partial_y, D]
       = i(alpha^x partial_y+alpha^y partial_x) != 0,

whereas `H_(V dot grad 1)=0`. This proves the frozen-background candidate
fails the remaining canonical bracket even at flat fields. It is a scoped
countercontrol, not a no-go for a moving native metric/clock construction.
A genuine dynamic frame transport must supply the missing variation; the
phase space, symplectic structure and actual generators must still be proved.

This exact boundary supports the new route as a concrete test. It prevents
the valid Clifford identity from being reported as full hypersurface
deformation closure or as an Einstein dynamics theorem.

## 4. Input-price companion remains distinct

The separate finite all-input coherent-entropy price inequality uses the
same number n of attempted original rounds, not equal realized tick count:
the actual variable 1+b charge is included explicitly. It concerns a
homogeneous Fourier block, not the all42 fixed-collar family. Nothing in
this bracket calculation cancels that paid price or binds a Book03 cut.

`GR_closed=false`.
