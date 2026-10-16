# Affine translation endpoints erase the order of native CAR returns

**Exact scoped obstruction, 16 October 2026.** The affine path law makes
pure translations commute. The actual four native full-CAR record returns do
not. Therefore no path-compositional unitary readout that depends only on the
translation endpoint can reproduce all four reference returns on one fixed
16-dimensional carrier.

This is stronger than the positive-ray subdivision obstruction for this
specific interface: it does not assume that the readout is scale-invariant or
normalizes a shift. It still does not exclude an operation that retains path
order in the existing matter/history state, depends on the linear link, or
uses another independently owned native input. It is not a whole-core
no-go, physical-admission theorem, source, or GR result.

## Exact clash

The owned affine composition is

\[
(D_1,b_1)(D_2,b_2)=(D_1D_2,\,b_1+D_1b_2).
\]

On the translation subgroup \(D=I\), the paths with shifts \(e_0\) then
\(e_1\) and \(e_1\) then \(e_0\) have the same endpoint \((I,e_0+e_1)\).
This equality is exact in the existing affine owner.

Let \(U_r=\operatorname{record}(I_4,e_r)\) be the actual CAR returns on all
sixteen exterior components. In the owner's occupation-mask basis, direct
exact reduction gives

\[
\bigl(U_0U_1-U_1U_0\bigr)_{0,3}=2p-2=\sqrt5-3\ne0,
\qquad p=\frac{\sqrt5-1}{2}.
\]

The exact checker binds these matrices to the existing record and preparation
owners, verifies all four returns are orthogonal, and checks the exact
commutator witness. No exterior grade or matrix entry is removed.

Suppose a unitary readout \(\mathcal U\) of the affine translation endpoint
were compositional, so that it sent concatenation to ordered multiplication,
and matched \(\mathcal U(I,e_r)=U_r\). Since the two affine paths above have
the same endpoint, composition would require \(U_0U_1=U_1U_0\), contrary to
the displayed entry. The same contradiction holds for an
anti-homomorphism: equal reversed endpoints still force the two image
operators to commute.

Equivalently, the two histories `01` and `10` have one affine endpoint and
different full-CAR return products. This is a concrete memory distinction:
the translation sum records the endpoint but not the order that the native
returns act on. The free ordered-history assignment
\(w\mapsto U_{w_1}\cdots U_{w_n}\) is a mathematical way to retain that order;
it is only a witness that a larger history carrier can preserve composition,
not a D0 transition law derived here.

## Consequence for the native preparation route

The shift-only, memoryless functor route is now closed for the four specified
reference records. A remaining physical route must preserve order through an
already owned state/history transition or use additional native variables in
its local operation. The full record engine already has a non-repeating
sixteen-component memory orbit, but no current owner maps affine path order
into that orbit or proves refinement-compatible joint evolution of
\((q,D,b,m)\). That bridge remains the actual open task; this result does not
add a stage variable, operation, action, source, or physical postulate.

The exact certificate is
[`a4d_native_affine_translation_record_order_check.py`](certificates/a4d_native_affine_translation_record_order_check.py),
with its machine-readable result at
[`a4d_native_affine_translation_record_order_results.json`](certificates/a4d_native_affine_translation_record_order_results.json).
It rechecks the transitive hashes of the upstream full-CAR preparation
certificate and records 20 exact controls. Reproduce with:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_affine_translation_record_order_check.py
```

The scope flags remain false for physical admission, source/Ward, and GR.
The existing #310 fixed-source/raw-owner terminal and independent #202/#317
criteria are unchanged.
