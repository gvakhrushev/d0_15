# Final scoped review of the 66-check clock packet

21 October 2026. Reviewer: Book-binding lane, independently of the author
of `PROOF.md` and `check_clock_bracket.py`. Existing d0_15 PR #334 only.

**Decision: ACCEPT the exact constant-frame kinematic statements and the
stated finite-stencil controls at their declared scope.** This does not
approve physical normal-clock admission, a canonical gravitational
constraint algebra, compulsory Book selection, or GR closure.

## 1. Final snapshot and independent replay

The final reviewed bytes are:

| File in this directory | SHA256 |
| --- | --- |
| `PROOF.md` | `5fde0047dbc4086759d97576291f1409d82f906253cf1c1ed4f8938e020cc929` |
| `check_clock_bracket.py` | `21728357ea286ae9d335f3c7cf8388fab0455438b816d344bd8098cad39b3bdd` |
| `RESULT.json` | `e25b95adb19ac042fbf8f0e8562db8acb2c270417575c8111ca0eceddbd03844` |

I independently ran the final checker with

    PYTHONPATH=/tmp/d0_synthesis_python OPENBLAS_NUM_THREADS=1 \
      python3 check_clock_bracket.py

It passed **66/66 active checks**. Captured stdout was byte-for-byte equal
to the final `RESULT.json`, with no stderr. The checker and result remained
unchanged through the replay. This is the current count; the older review's
historical 55-check replay is not the final count.

The proof's last wording correction was also inspected: the saddle is not
a minimum of the same counted-CQ price. The previous unproved wording about
the most probable implementation was removed. That change affects no
operator equation or checker byte. The hash above pins the corrected proof.

No large inherited suite, optimizer, gate search, or Lean build was rerun.

## 2. Mathematical checks and their limits

The original creator order `(0,2,3,1)` and all16 CAR components are retained.
The spatial Clifford matrices are Hermitian and obey the required
anticommutator. For the stated real one-parameter family
`H_N(a)=ND+a[D,N]`, its adjoint forces `a=1/2` when `[D,N]` is nonzero.
This is uniqueness within that family; it is not uniqueness among all
possible self-adjoint clock operators or subprincipal completions.

Direct composition gives

    [H_N,H_M] = -[V dot partial + (div V)/2 + Omega],
    V^j=q^ij(N M_i-M N_i),
    Omega=(1/4)[alpha^i,alpha^j]N_i M_j.

The signs, the half-density coefficient, and the independent spin term are
correct. The nonscalar constant-frame test correctly uses `q=E^T E` rather
than keeping delta. It establishes a positive spatial Clifford symbol;
it does not construct a Lorentzian physical time direction.

The actual one-sided creation/annihilation stencil is self-adjoint in the
specified periodic counting representation. Its nonzero first consistency
term is `(h/2)(c_i+a_i)partial_i^2`. The analytical smooth-sector O(h)
estimate is compatible with the exact polynomial fixture. The fixture
does not itself prove the general estimate, and neither implies uniform
operator-norm convergence on grid-scale modes. The explicit high-frequency
control correctly rejects that stronger claim.

The heat candidate is decisively different: for
`L_N=-(N partial_x^2+N'partial_x+N''/2)`, the coefficient of `partial_x^3`
in `[L_N,L_M]` is `2(N M'-M N')`. In constant spatial metric this is the
stated cubic principal symbol, up to the convention for i in symbols.
It rejects this particular symmetrized heat operator as the first-order
normal generator. It does not reject all uses of heat in the Book source.

Finally the frozen-frame dilation check is exact:

    X=x partial_x, N=1:
    [K_X,H_1]-H_(X dot grad 1)=i alpha^x partial_x != 0.

Thus normal-normal closure alone is not the full deformation algebra.
The proof correctly retains moving geometry, internal-frame compensation,
the full-process phase/presymplectic structure, the remaining brackets,
Ward identities, and canonical reconstruction hypotheses as requirements.
This review checks the algebra and the scope; it is not a new literature
audit of Teitelboim or HKT, nor application of their reconstruction to D0.

## 3. Separately authored positive extension

At the parent's request I separately **authored**, rather than independently
reviewed, the adjacent `MOVING_FRAME_IDENTITY.md`,
`check_frame_compensation.py`, and `FRAME_RESULT.json`. They are therefore
not being presented as independently certified by this review. Independent
root review of that addition remains appropriate.

For the explicitly declared half-density continuation

    H_N(alpha)=-i[N alpha^j partial_j+partial_j(N alpha^j)/2],

at the constant flat base, the addition derives the full operator identity

    [K_X,H_N]-H_(X dot grad N)
      = delta_alpha H_N[-alpha^i partial_(i X_j)].

The covariant comparison subtracts this field derivative. Both principal
and zero-order matrix coefficients were tested with arbitrary symbolic
functions X_i,N on the full16 carrier, rather than only one polynomial.
The authored narrow checker passes **50/50 active checks**, with ordinary
and optimized Python outputs identical. These checks include source pins,
the exact coefficient calculation, sign/half-density/spin omission controls,
and the old inverse-coframe moment map. They do not count as new physical
clock admission evidence.

The addition's snapshot is:

| Authored file | SHA256 |
| --- | --- |
| `MOVING_FRAME_IDENTITY.md` | `79bcfe288daee3923d934f32e0d376be1d5627fbcd429f5483917e8a99792aa0` |
| `check_frame_compensation.py` | `8f1801cad7b3f71b6482e75681c5b19586372d5e6143dbb900f1cb665fc07a8b` |
| `FRAME_RESULT.json` | `93f409b0309bdeca571b9d7b8587452e58a80f1298742e40b86d5e9d480c1b06` |

## 4. Actual native ownership of the coframe tangent

I read the original moment source and paid-code source, not only synthesis
claims. They supply the local diffeomorphism
`E=(D^T eta_R T)^(-1)` on the full sixteen coframe coordinates and exact
paid finite moment nodes from common declared resources. The variation
`delta E=E B`, `delta D=-D B^T`, `delta R=-B R` fits that chart. With B the
appropriate spatial strain matrix, it gives the requested inverse-frame
tangent, subject to the fixed slice and existing basis/calibration dictionary.

This is an owned **preparation of field-node moments and their actual price
secants**. It is not an owned transport gate on an existing field-spinor-
clock-archive state. The source expressly does not identify those preparations
with executed raw-coframe Julia operators or unknown-input channel action.
The writer's different instruction words do not prove one autonomous fixed
execution produces the chosen coframe deformation.

The spin lift has a second exact distinction. On full CAR16 the exterior
spatial rotation and the chosen Clifford lift differ by `beta_i beta_j/2`,
where `beta_i=c_i+a_i`; that term commutes with all spatial alpha matrices.
Consequently they induce the same vector rotation while acting differently
on the complete carrier, including its scalar vacuum. An actual comparison
must retain and handle this commuting internal remainder. The difference
does not rule out a compensated lift or gate synthesis, but the six proper
link moments alone do not implement the chosen Clifford lift.

The density source likewise owns exact transported representations with
the half-density endpoint factors and true moving adjoint. It does not
make actual preparation-density changes free physical operations. The
four consumed source files and SHA256 values are listed and checked in the
authored addition. No additional heat, cut, or actual price component has
been canceled by this calculation.

`physical_normal_clock_admission=false`;
`full_gravitational_constraint_algebra=false`;
`complete_Book_price_selection=false`; `GR_closed=false`.
