# MEMO A4D — nonlinear stationary rigidity after affine/Cartan pressure

**Parent execution:** PR #182 `EXP-A4D-STAR-TRANSLATION-INVARIANT-ACTION-COMPLETION`  
**Status:** supporting research, IN_PROGRESS; not a terminal verdict  
**Scope:** accepted finite star density, exact rational/symbolic controls; no claim/release/BOOK promotion

## 0. Why this memo exists

The fixed observer-completed affine action from #178 is not an off-shell symmetry of the accepted star density, while #180 proves the full finite local proper-Lorentz quotient on the nondegenerate solder sector and #181 closes the first bounded-locality Cartan-Hodge on-shell rescue class.

That leaves two logically distinct questions which must not be conflated:

1. can the **action** be completed so that affine translations become exact gauge; and
2. independently, what stationary curved configurations does the accepted star functional (or a gauge-fixed relative-solder completion with the same physical ((v,L)) functional) actually possess?

This memo attacks the second question because a gauge-invariant completion can still change the stationary set.

The exact checker is:

`02_REGISTRY/research/certificates/a4d_cartan_nonlinear_rigidity_check.py`.

## 1. Local solder Euler map does not force flatness

Write the local density at identity solder as a bilinear contraction between the six complementary solder bivectors and six curvature bivectors. Treat the curvature components as a (6	imes6) array: six base faces times six internal bivector components.

The exact solder Euler map is

[
A_e:mathbb R^{36}	omathbb R^{16}.
]

The certificate gives

[
operatorname{rank}A_e=16,qquad
dimker A_e=20.
]

Therefore the coframe/solder Euler equation alone does **not** imply (C=0).

If one restricts the curvature array to pair-exchange symmetry, the curvature space has dimension (21). The solder Euler map has rank (10) on that space, leaving an (11)-dimensional kernel.

Adding the four-dimensional algebraic first-Bianchi relation

[
R_{01,23}-R_{02,13}+R_{03,12}=0
]

leaves a (20)-dimensional algebraic-curvature space and a (10)-dimensional solder-Euler kernel:

[
oxed{
dim{C:	ext{pair symmetry+Bianchi},,E_v(C)=0}=10.
}
]

An explicit nonzero exact witness in this kernel is

[
C_{01|01}=+1,qquad
C_{03|03}=-1,qquad
C_{12|12}=-1,qquad
C_{23|23}=+1,
]

with all other components zero.

This is only an algebraic/local statement. The dimension (10) is suggestive but is **not** promoted to a continuum Weyl-tensor identification. Realizability by finite plaquette links and the connection Euler equation remain separate gates.

## 2. The #178 curved witness is stronger than a symmetry counterexample

For the exact #178 links — one rational (01) boost and one (12) quarter rotation at the origin — the local solder quadratic form at the origin has

[
operatorname{rank}H_v=8,qquad
dimker H_v=8.
]

The general stationary solder matrix at fixed links has a zero fourth internal row. Equivalently,

[
det V_{m ker}equiv0.
]

The checker also reproduces that the witness contains (11) nonzero curved plaquette faces on the full (L=2) torus.

Hence the #178 witness is not merely off-shell at the particular flat solder representative. At its origin, **no nondegenerate stationary solder exists while those links are held fixed**.

This remains a statement about that exact fixed-link witness, not a global curved-vacuum no-go.

## 3. The flat checkerboard quotient-null modes do not nonlinearly bifurcate

The accepted flat (L=2) Hessian has exactly three nonzero Lorentz-null momentum sectors,

[
(-1,-1,+1,+1),quad
(-1,+1,-1,+1),quad
(-1,+1,+1,-1),
]

and each has two physical quotient-null directions after removing the ten flat gauge directions.

For each physical direction the connection generators are exact nilpotent null rotations, with

[
N^3=0,
]

so the finite exponential is the exact polynomial

[
exp(tN)=I+tN+rac12t^2N^2.
]

The important point is that zero quadratic action along such a path is not enough. The full Euler map must vanish.

For a general real polarization ((p,q)) in one physical two-plane, the second-order self-interaction produces a zero-momentum solder Euler source. Its projection on pure zero-momentum coframe null covectors is

[
(-32,-32,+32,+32)(p^2+q^2)
]

on the four components associated with the timelike role and the one participating spacelike role.

In particular every one of the three sectors has the same obstruction on the uniform (h_0{}^0) left-null covector:

[
E_{00}^{(2)}=-32(p^2+q^2).
]

Cross-products between distinct checkerboard characters carry a nonzero character and do not contribute to zero momentum. Therefore for all six physical amplitudes,

[
oxed{
E_{00}^{(2)}
=
-32sum_{j=1}^{3}(p_j^2+q_j^2).
}
]

Over the reals this vanishes only when every physical checkerboard amplitude vanishes.

The zero-momentum Hessian has rank (24), and the displayed source has a component along its left kernel. Hence no arbitrary (O(t^2)) correction of the full forty-component uniform solder+connection field can absorb this source.

### Result

The six extra flat (L=2) quotient-null directions are **not** tangent to a real analytic nontrivial stationary curved branch through the flat background.

This is a nonlinear rigidity result. It sharply limits the interpretation of the flat rank drops: they are not, by themselves, evidence of a finite nonlinear propagating branch.

Scope: exact (L=2), accepted star density, local analytic continuation through the flat background. Finite-amplitude disconnected critical points and higher-(L) branches remain open.

## 4. A finite-amplitude homogeneous curved family is also excluded

To test disconnected finite curvature rather than perturbation theory, consider the exact homogeneous two-link family

[
L_0=B_{01}(t),qquad
L_1=R_{12}(u),qquad
L_2=L_3=I,
]

where

[
B_{01}(t)=
egin{pmatrix}
rac{1+t^2}{1-t^2}&rac{2t}{1-t^2}&0&0\
rac{2t}{1-t^2}&rac{1+t^2}{1-t^2}&0&0\
0&0&1&0\
0&0&0&1
end{pmatrix},
quad |t|<1,
]

and

[
R_{12}(u)=
egin{pmatrix}
1&0&0&0\
0&rac{1-u^2}{1+u^2}&rac{2u}{1+u^2}&0\
0&-rac{2u}{1+u^2}&rac{1-u^2}{1+u^2}&0\
0&0&0&1
end{pmatrix}.
]

For (tu
eq0), the exact odd plaquette curvature is nonzero. The Hodge-paired curvature two-form controlling the coframe Euler equation has the normal form

[
Omega
=
K
egin{pmatrix}
0&0&0&t\
0&0&0&-1\
0&0&0&u\
-t&1&-u&0
end{pmatrix},
]

with

[
K=
rac{4tu,[t^2u^2-t^2+u^2+1]}
{(1-t^2)^2(1+u^2)^2}.
]

For (|t|<1) and (tu
eq0), the bracket is positive and (K
eq0); (Omega) has rank (2). Its kernel is

[
kerOmega
=
operatorname{span}{k_A,k_B},
quad
k_A=(1,t,0,0)^T,quad
k_B=(0,u,1,0)^T.
]

Coframe stationarity forces the complementary solder legs into this plane:

[
V_2=a k_A+b k_B,qquad
V_3=c k_A+d k_B.
]

Full solder nondegeneracy requires (V_2,V_3) to be independent, hence

[
ad-bc
eq0.
]

Now vary one **literal** (L_0) edge at the origin in the spatial (23)-rotation Lorentz tangent, while evaluating the complete (L=2) periodic action. The exact connection Euler component is

[
oxed{
E_{L_0,mathrm{rot}_{23}}
=
2u(ad-bc).
}
]

Therefore for (u
eq0), connection stationarity forces (ad-bc=0), contradicting nondegenerate solder.

### Finite-amplitude scoped no-go

[
oxed{
egin{array}{c}
L_0=B_{01}(t), L_1=R_{12}(u), L_2=L_3=I,\
|t|<1, tu
eq0
end{array}
quadLongrightarrowquad
	ext{no homogeneous nondegenerate critical point}.
}
]

This is a whole exact two-parameter SO(^+) family, not a single witness and not a small-field expansion.

It is **not** a no-go for all finite-amplitude curved link configurations. Richer multi-link / inhomogeneous patterns remain open.

## 5. Consequences for the active action-completion task

These results do not select a translation-invariant completion. They instead constrain what any positive completion must accomplish dynamically.

In particular:

- “make translation gauge” is not enough; the completed theory must still possess a nondegenerate stationary sector if it is to describe nontrivial curved configurations;
- the original #178 witness cannot be recycled as a vacuum of a completed theory;
- the six special flat quotient-null modes do not provide an analytic route to finite curved vacua;
- a simple homogeneous boost+rotation finite-curvature branch is also eliminated.

If a relative-solder/Stückelberg completion is later selected and gauge fixing (b=0) reduces its physical functional exactly to the same (S_star(v_{m rel},L)), then these stationary-Euler obstructions transfer to that gauge-fixed physical problem. This is conditional on selecting such a completion; the present memo does not select it.

## 6. Next research target

The live mathematical target is now narrower:

> construct or refute a genuinely finite-amplitude, nondegenerate, curved critical point using a richer realizable plaquette pattern than the two-link homogeneous family.

The local solder Euler equation allows a nonzero ten-dimensional algebraic-curvature kernel, so a global flatness theorem has not been proved. The remaining task is to intersect three conditions on an actual periodic finite link field:

1. realizable plaquette/odd-curvature data;
2. nondegenerate solder Euler kernel at every site;
3. the literal finite connection Euler equation.

Promising next ansätze are multi-link nilpotent/null-rotation configurations because their exponentials truncate exactly and preserve rational symbolic control.

## 7. Not claimed

No universal curved-vacuum no-go.  
No selection of the relative-solder completion.  
No proof that affine translation is universally physical or universally gauge.  
No torsion-free/Levi-Civita theorem.  
No Weyl ownership despite the ten-dimensional algebraic kernel.  
No Einstein/GR/diffeomorphism/time/wave/graviton interpretation.  
No higher-(L) conclusion.

This memo is deliberately a supporting nonlinear-rigidity packet while PR #182 remains Draft / IN_PROGRESS.
