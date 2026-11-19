# Native two-Golden preparation and a phase-kernel descent witness

Input: PR #334 at `1d29848fa0775485f7d48ab63f4a6625f9b705ad`, consuming
the new source-owner §7cv (845–850). This is a concrete test of the additional
phase carrier. It does not replace the source owner's distinction between
horizontal Einstein soundness and construction of a stationary execution.

## 1. Actual finite preparation, every protected column retained

Use the existing G_CX_SOURCE_I capability profile with physical port 0,
ordinary work bit 1, protected Spin bits (2,3), immutable oldRIGHT bit 4.
Port and ordinary work start blank; Spin and oldRIGHT stay arbitrary,
including arbitrary entanglement with an outside reference. Write

    p=(sqrt(5)-1)/2, a=sqrt(p), p+p²=1,
    G=[a,-p;p,a], S=SWAP(0,1)=CX01;CX10;CX01.

The chronological word

    G0; S; G0; S

has exactly eight paid stages, 2G+6CX, no added phase gate, reset, measurement,
discard or free inverse. Its complete 32-column operator is

    U=G0 G1 tensor I_(Spin,oldRIGHT).

The genuine input rank is 8, not 32. On the input isometry its four coherent
ordinary-work amplitudes are

    v=(p,ap,ap,p²),
    w=(p²,p³,p³,p⁴),  sum w=1.                         (1)

Every record effect compressed to the entire eight-column protected input
is exactly w_b I_8. All four weights are strictly positive. These are
orthogonal coherent work labels; an actual subsequent reading/sealing
apparatus keeps its own paid stages and is not silently appended here.

## 2. Apply the supplied phase carrier on its stated mathematical chart

For the ambient first-port angle comparison set x=cos²(theta), 0<x<1,
and leave the second Golden factor fixed. The probabilities are

    w(x)=(px,p²x,p(1-x),p²(1-x)),
    J=dw/dx=(p,p²,-p,-p²)^T.                           (2)

At the actual native base x=p, (2) equals (1). This smooth angle is a
matrix-comparison parameter, not a newly permitted continuous native gate.
The same is true of the independent coherent phases below.

With a normalized protected state chi that does not depend on x or phases,

    Psi(x,phi)=sum_(b=00,01,10,11) sqrt(w_b(x)) e^(i phi_b)|b> chi.

The source-owner conditional-state beta is zero. Its exact form (847) is

    Pi=J^T phi, omega=dx wedge dPi.

J has column rank one. Every component of J is nonzero, so no vector
e_c-e_b for distinct b,c belongs to span(J): it has two zero components,
whereas every nonzero multiple of J has four nonzero components. The phase
kernel contains, in particular,

    k=(1,-1/p,0,0)^T, J^T k=0.                        (3)

This is a retained relative phase direction, not the global phase.
Along it x and Pi are both exactly unchanged. The carrier (847) by itself
therefore identifies those points in its presymplectic reduction.

## 3. The generator of the actual Golden gate fails descent on this chart

Take the fixed Hermitian operator

    H=sigma_y tensor I_ordinary,
    sigma_y=[0,-i;i,0], H²=I, ||H||op=1.

It is the actual first-port Golden generator: G=aI-i p sigma_y is the
finite rotation exp(-i theta_G sigma_y). This does not make arbitrary
fractional rotations native, identify H with a physical clock Hamiltonian,
or identify it with the missing normal generator H_N.

Its full-state expectation is exactly

    h=2sqrt(x(1-x)) [p sin(phi10-phi00)
                         +p² sin(phi11-phi01)].           (4)

At phi=(0,epsilon,0,0), differentiate in the phase-kernel direction (3):

    dh[k]=-2p sqrt(x(1-x))(1-cos epsilon).                 (5)

For every sufficiently small nonzero epsilon this is nonzero. Thus the
failure occurs arbitrarily close to the all-real native phase base, not
only on a distant phase chart. At epsilon=pi/2 and the actual x=p,

    dh[k]=-2a p² !=0.                                    (6)

Consequently h does not factor through (x,Pi), and no vector field on this
presymplectic chart can satisfy i_X omega=dh there: the left side vanishes
on k, while (5) does not. The choice epsilon=pi/2 is an exact mathematical
phase control, not a claimed admitted phase preparation on protected
oldRIGHT. H and the phases act only on ordinary output work; protected
Spin/oldRIGHT remain identity factors throughout.

The tangency failure is independently explicit. The full Hilbert evolution
dot(Psi)=-iH Psi gives, at the same phases,

    dot(w)=2sqrt(x(1-x))
           (-p,-p² cos epsilon,p,p² cos epsilon).          (7)

For epsilon nonzero and sufficiently small, this is not J dot(x), because
the first pair requires dot(x)=-2sqrt(x(1-x)) while the second requires
dot(x)=-2sqrt(x(1-x))cos epsilon. At epsilon=pi/2 the native-x velocity is
(-2ap²,0,2ap²,0), manifestly outside span(J).

At epsilon=0, by contrast, dh[k]=0 and dot(w) belongs to span(J). Thus a
check only at the original real native state would falsely suggest that
the generator descends on an open phase chart. This is a decisive negative
control for the newly supplied carrier's use by the bracket theorem.

## 4. Exact parent consequence and scope

The new phase construction supplies a genuine mathematical canonical
carrier after its presymplectic quotient; it is not interchangeable with
the earlier zero-form terminal graph. The calculation above consumes that
new carrier and tests a further required application: does an actual
represented Hamiltonian descend through its excess phases and preserve the
selected probability chart? Even the operator generating an existing native
Golden gate fails those properties on this specified phase extension.

This is not a universal no-go for a different observation chart, a larger
phase space, or a properly derived family of H_N. In particular one can
change the resolved probability coordinates and hence the kernel, but the
actual observation/field map and its physical admission must then be proved.
The source-owner (848) already states tangency and kernel descent as its
application hypotheses; this witness proves they are not supplied merely
by constructing (847). It does not invalidate its chain-rule correction or
turn vertical neutrality into an extra requirement for forward Einstein
soundness along genuine stationary executions.

The actual eight-stage word, all 32 columns, the eight protected input
columns, full effects, (2)–(3), (6)–(7), and the pointwise false-positive
control are verified exactly in `phase_native_check.py`. No physical phase
admission, local lapse Hamiltonian, strong HDA, full source selection or
GR closure is claimed.
