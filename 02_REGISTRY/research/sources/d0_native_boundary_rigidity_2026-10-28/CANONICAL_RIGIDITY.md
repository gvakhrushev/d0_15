# Strong deformation closure fixes both ultralocal kinetics and algebraic curvature

Bounded continuation of existing #334, `c4a92cb0f2326bf7ae2a8127c49f5b65ea71ce5a`.
Consumes `A4D_ROOT_CUT_TO_REFOLIATION_CLOSURE_2026_10_28.md` and its canonical
bracket, scalar-matter, and Legendre-elimination results. The method is the
Hojman–Kuchar–Teitelboim geometrodynamics reconstruction method, not a claim
of a new physical principle or historical priority. The contribution here is
an explicit principal-coefficient proof which removes two assumptions of that
repository theorem within a larger but still declared local class.

## Exact scope

Let Σ have spatial dimension three. Work on an open canonical chart of a
positive spatial metric q_ij and symmetric contravariant momentum density
π^{ij} of weight one, with the actual canonical symplectic form. Retain:

- arbitrary compactly supported smooth lapse and shift functions;
- the off-shell, strong hypersurface-deformation algebra with structure
  function q^{ij} and its fixed time normalization;
- spatially natural scalar-density Hamiltonians and no additional background
  tensors, scalar clocks in the gravitational density, or gravitational pairs;
- a separated local gravitational Hamiltonian

      H_g[N] = ∫ N [T(q,π) + √q U(q,R_ij)],                 (1)

  with T smooth and ultralocal, and U smooth in the algebraic Ricci tensor.

No evenness or polynomial restriction on T is imposed. U need not be affine
in scalar curvature, a polynomial, or even a function of scalar curvature
alone: it may initially depend on all Ricci invariants. It has no derivatives
of curvature and no momentum-curvature coupling. The local jet domain allows
independent first momentum jets and arbitrary Ricci values at fixed q.

In dimension three this covers all algebraic Riemann-curvature potentials,
because Riemann is determined by Ricci. It does not cover curvature-derivative
terms, general nonlocal spectral functionals, π-R couplings, extra canonical
pairs, restricted lapse families, or weak equality only on constraints.

## 1. The potential's principal lapse tensor

At a normal orthonormal coordinate frame at a chosen point, write symmetric
matrices

    Z^{ij} = ∂U/∂R_ij,
    S_ij = ∂T/∂π^{ij},
    L(X)_ij = ∂S_ij/∂π^{ab} X^{ab}.

Here derivatives use the full Frobenius pairing: off-diagonal symmetric
coordinates have multiplicity two. Let I be the 3×3 identity and define

    C_Z(S) = (SZ+ZS)/2 - tr(SZ)I/2 - tr(S)Z/2.              (2)

The principal metric variation is

    δR_ij = 1/2 [∂_k∂_i h^k_j + ∂_k∂_j h^k_i
                 -Δh_ij -∂_i∂_j tr(h)] + lower terms.

After twice integrating by parts in δ∫N√q U, contraction of the two-lapse-
derivative term with S is exactly

    √q C_Z(S)^{ij} ∂_i∂_j N.                              (3)

For Z=A I, (2) reduces to A(S-tr(S)I), recovering the previous f(R) and
Einstein curvature formulas with their correct signs.

Terms with no derivatives of the lapse cancel between N and M. Terms with
one lapse derivative contain derivatives of Z. Such terms do not contain
momentum derivatives, since U does not depend on π. Antisymmetrization of
(3), followed by one integration by parts, makes the coefficient of the
independent first momentum jet ∂_iπ precisely

    √q C_Z(L(∂_iπ))^{ij} w_j,
    w_j=N∂_jM-M∂_jN.                                    (4)

The potential's remaining terms do not change this coefficient. Equivalently,
one may evaluate at metric jets for which ∇R_ij=0; arbitrary Ricci values and
zero Ricci third jets are simultaneously realizable at a normal point.

## 2. Strong HDA forces a two-sided inverse identity

The geometric momentum generator is

    D_g[v] = -2∫v_j ∇_iπ^{ij},  v^i=q^{ij}w_j.

The owned lapse-separation argument turns equality for all N,M into equality
of the coefficient current. Independence of all ∂_iπ^{ab} then gives, for
every symmetric X,

    C_Z(L(X)) = -2 X/√q.                                  (5)

At a literal normal coordinate point √q=1; the displayed density factor
restores the invariant tensor-density convention. In six symmetric coordinates,
(5) is a full 6×6 matrix identity, not only a trace or one-channel constraint.

Both maps are square on Sym(3). Thus (5) forces both L and C_Z invertible.
Kinetic nondegeneracy has been derived, not assumed.

At fixed q,π, L is independent of the Ricci tensor. Therefore

    C_Z = -(2/√q) L^{-1}

is independent of every Ricci coordinate. The map Z→C_Z is injective, as

    C_Z(I) = -(Z+tr(Z)I)/2,
    Z = -2 C_Z(I) + tr(C_Z(I)) I/2.                        (6)

Hence Z itself is independent of Ricci. Integrating ∂U/∂R=Z on each connected
curvature chart proves

    U(q,R_ij) = A^{ij}(q) R_ij + u0(q).                    (7)

Spatial naturality with no external backgrounds fixes A^{ij}(q)=-b q^{ij}
and u0(q)=c0, with constants b,c0. Indeed at q=I an orthogonally invariant
symmetric tensor is a scalar multiple of I, and arbitrary frame changes act
transitively on positive q. The same fact fixes any scalar function of q to
a constant. Invertibility in (5) excludes b=0. Thus

    U=-bR+c0.                                             (8)

This is the promised removal of the affine-curvature premise. It excludes,
within (1), R², R_ij R^{ij}, and arbitrary nonlinear algebraic curvature
functions through a full independent-momentum-jet test rather than by checking
only a special Einstein solution family.

## 3. The same identity fixes the whole kinetic Hessian

For Z=-b I, (5) has the unique solution

    L(X)=2/(b√q)[X-tr(X)I/2].                              (9)

This is independent of π, so T has no higher momentum terms. Integrating
its Hessian and using the same no-background spatial naturality gives

    T(q,π)= [π^{ij}π_ij - (tr_q π)^2/2]/(b√q)
               + κ tr_q π + C√q,                         (10)

where κ,C are constants. Thus quadratic momentum dependence is forced, and
the only time-odd term in this class is an ultralocal trace drift.

## 4. The trace drift is a canonical boundary term

Let Q(π)=π^{ij}π_ij-(tr_qπ)^2/2 and define

    Π^{ij}=π^{ij}-bκ√q q^{ij},
    W[q]=2bκ∫√q.

Then exactly

    ∫π^{ij}δq_ij = ∫Π^{ij}δq_ij + δW,
    ∇_iπ^{ij}=∇_iΠ^{ij}.

The Hamiltonian becomes

    H_g[N]=∫N [ Q(Π)/(b√q)-b√qR
                  +(C+c0+3bκ²/2)√q ].                    (11)

Indeed `Q(Π+bκ√q q^{-1})=Q(Π)-bκ√q tr_qΠ-(3/2)b²κ²q`.
The cosmological constant is `(C+c0+3bκ²/2)/(2b)`. The canonical action changes
by the retained endpoint term `W[q_final]-W[q_initial]`. Its physical value
must be accounted for; the proof does not call a real momentum-shift operation
free or erase a boundary price.

The companion [scalar-gradient rigidity proof](SCALAR_RIGIDITY.md) also
removes the previous quadratic-gradient and invertible-matter-coefficient
premises within the separated matter class. Its result and the existing
owner's Legendre elimination apply to (11). Consequently the full Einstein–sigma-model equation class follows under
the retained class assumptions, with the prior unfixed Newton normalization,
cosmological constant, field-space metric and scalar potential.

## 5. Exact controls and remaining D0 application

There is also a quantitative principal-coefficient consequence. At the same
fixed q and pi suppose

    C_Z(R) L = -2 I/sqrt(q) + E_R,   ||E_R|| <= epsilon,

and suppose the actual inverse L^-1 is controlled. Subtracting at two Ricci
values and using (6) gives

    ||Z(R1)-Z(R2)||_F <= 4 sqrt(3) epsilon ||L^-1||_op.

Indeed the inverse of Z -> -(Z+tr(Z)I)/2 has Frobenius norm two; evaluating
the difference operator at I costs ||I||_F=sqrt(3). This bound uses the
principal coefficient of the bracket current, not one integrated bracket
sample or source values without derivative control. It provides a sufficient
continuum-limit estimate only when its own native norms are established.

`check_canonical_rigidity.py` runs exact SymPy identities for:

- the complete Ricci principal contraction with arbitrary symmetric S,Z,N;
- symmetry and Frobenius self-adjointness of C_Z;
- the exact inverse (6);
- the full six-by-six Einstein/HDA principal identity, with off-diagonal
  Frobenius weight matrix diag(1,1,1,2,2,2);
- the full six-component trace drift and cosmological shift;
- realization of arbitrary Ricci components by the 3D algebraic Riemann tensor;
- nonzero principal defects for Ricci-square and scalar-curvature-square terms.
- the two-scalar spatial flux, reciprocal Hessian, nonlinear separated
  gradient anomaly, and an exactly closing nonseparable matter counterexample.

Executed with SymPy 1.14.0. This is exact algebra supporting the analytic jet
proof, not a native D0 Hamiltonian replay or proof of physical closure.

The new parent substitution is precise: the earlier kinetic-evenness and
curvature-affinity assumptions are unnecessary within the separated
ultralocal-kinetic/algebraic-curvature class. Actual root Book03 dynamics must
still supply the native phase space, full retained-boundary form, normal and
tangential generators, permissible local lapses, this locality/class map, and
the strong HDA identity or a controlled common limit. No status is promoted.
