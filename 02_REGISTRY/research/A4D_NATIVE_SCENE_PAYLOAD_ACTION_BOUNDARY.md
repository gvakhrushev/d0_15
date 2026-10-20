# G0 boundary: the joint scene and full-payload action fiber

Status: **EXACT TYPED-INTERFACE UNDERDETERMINATION / PHYSICAL ADMISSION OPEN**.
The Lean owner is
[`a4d_native_scene_payload_action.lean`](certificates/a4d_native_scene_payload_action.lean).
It combines the literal $K(9,11,13)$ scene-walk carrier with the existing
nondegenerate raw-coframe, Lorentz-affine-link and full archive-cochain types.
The cochain retains every Fock grade; no matter component is frozen.

## Exact observable fiber

For fixed refinement level $N$, let $E$ be the literal directed scene-edge
carrier and $Z_N$ the complete native payload. The product verification
state and record are $\mathrm{Vertex}_{33}\times Z_N$, with the repository's
identity-record equality test. On the observable transitions
\((u,z)\to(v,z)\) for \((u,v)\in E\), the exact image of all existing
`ActionProtocol` assignments is

\[
  \{c:E\times Z_N\to\mathbb R:\ c(e,z)\ge 1\}.
\]

Both directions are Lean-proved: every such profile extends to an actual
`ActionProtocol` on the product state, and every `ActionProtocol` induces a
profile with this lower bound. Once these edge readings are fixed, the
identity and path-concatenation laws determine exactly one additive value on
every valid scene walk. Thus path composition removes freedom in extending
edge readings to histories; it does not select the edge readings themselves.
A hostile subunit control proves that any profile below 1 on even one actual
edge/payload pair has no such action extension.

This is the complete **observable restriction** of the product interface, not
a classification of unrelated transitions between different payloads.

## Two full-field fillings with distinct response

The certificate constructs two nonnegative profiles on the same complete
payload $z=(b,\psi)$:

\[
 c_1(e,z)=1+\sigma_0(\psi)^2,\qquad
 c_2(e,z)=1+\sigma_0(\psi)^2+\sigma_1(\psi)^2.
\]

They use the actual scalar component at the two archive-phase anchors and
the actual derivatives of those polynomials on the full `ArchiveCochain`.
At the same state $\psi=\operatorname{anchorDirection}(N,1)$, every scene edge
has prices 1 and 2, respectively. Along that same full-cochain direction,
their first variations are 0 and 2. Along every curve of admissible
coframe/link backgrounds with matter fixed, both background variations are
zero; the one-anchor filling is stationary for all full-cochain directions,
while the two-anchor filling is not. The second filling therefore changes
the matter response without changing the background response or any
scene/path law.

Both profiles commute with the literal all-grade archive pullback
$\psi'(x,s)=\psi(\operatorname{groupProjection}(x),s)$. For the background/link
factor, the result holds for any supplied level map $B_N$, because these
two readings are independent of that factor. No physical metric/link
refinement is inferred from this observation.

## Consequence and exact remaining arrow

The product interface, scene composition, unit action gap, full payload and
the displayed archive cochain pullback do not determine a unique matter
response. This rules out treating any one of these conditions, or their
formal combination here, as the missing native selector. It is a scoped
underdetermination theorem for this explicit typed interface, not a
counterexample to a separately owned physical preparation law.

The fixed-payload product also fails a sharp memory test on the actual scene
return `[0,9,0]`: additive history costs at least 2, while the product state
returns to the identical endpoint `(0,z)` and every `ActionProtocol` assigns
that endpoint transition cost 0. Thus the complete cochain type being present
does not mean its retained state is updated by the path. An owner-derived
archive update or a richer internally retained state is necessary before
endpoint action can encode the return; neither is supplied by this product
protocol.

The next G0 theorem must derive the actual edge-cost restriction from the
closed native history/record preparation on the same $(q,D,b,m)$ carrier,
including its allowed variations and full metric/link refinement, or prove
that the owned constraints force a unique restriction. Until that map is
proved, neither filling is declared physically admitted. This certificate
does not derive a source, Ward identity, stress tensor, stationary Einstein
equation, curved physical solution, soundness/recovery, GR, or a global
terminal.
