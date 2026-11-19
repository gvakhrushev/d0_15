# Reconstructed nonlinear Born–Book shape, clock and typed odds gate

21 October 2026. Companion to `RESTORED_ALL_FLAG_PRICE.md`; same pinned
repository, original detector and reconstruction status. Natural logarithms
are used below unless base phi is written explicitly.

## 1. Exact rotation law and a failed scalar-source identification

Take the original J=E23-E32 and P=exp(theta J). For the original detector,
write x=Tr(P)/4=(1+cos theta)/2 and
y=Tr(J^T P)/(2 sqrt(2))=sin theta/sqrt(2). The local coordinate
u=y/x=sqrt(2)tan(theta/2) has x=1/(1+u^2/2). On |u|<1 both marked
amplitudes are positive. After stripping the actual all-good factor 4^(-n)
for this purely algebraic comparison, the two positive functions are

    v_+(u)=(1+u)^2/[24(1+u^2/2)^2],
    v_-(u)=(1-u)^2/[24(1+u^2/2)^2],
    ell(u)=log(v_+/v_-)=4 atanh u.

The stripping is not declared free or physically implemented. Even after
allowing any constant multiplicity and a constant offset, matching the
linear derivative forces 48, because v_+'(0)=1/12 and ell'(0)=4.
But v_+'''(0)=-1/2, whence

    48 v_+'''(0)=-24 != 8=ell'''(0).                    (1)

This rules out the proposed all-neighbourhood equality; it does not rule
out a different independently derived complete price.

There is a stronger exact even-background control. The odd part of
`48 v_+-ell` is

    F(u)=4[u/(1+u^2/2)^2-atanh u],
    F'(u)=-u^2(u^4-6u^2+32)/[2(1-u^2)(1+u^2/2)^3].    (2)

The polynomial `u^4-6u^2+32=(u^2-3)^2+23` is strictly positive.
Thus F'(u)<0 for 0<|u|<1 and F(0)=0. No arbitrary even background
function, including a field-dependent even cost, can remove this odd
defect. This conclusion applies to the specified constant-multiple Golden
marked-probability candidate. It is not a classification of all Book Info.

## 2. The correct typed two-event equation

Let the two positive alternatives have independently specified complete
prices S_+=C_+-I_+, S_-=C_--I_- and retained continuation factors. If
they genuinely factor at the probability level, their relative law has

    q_+/q_-=r phi^[-(S_+-S_-)].

If instead scalar Book weights phi^(-S) are amplitudes multiplying two
separate fixed retained branch vectors, the Born square gives the exponent
2 and r contains the ratio of their squared norms/continuation factors.
Consequently the exact common notation is

    G=log(q_+/q_-)-log r
      +eta log(phi)[(C_+-C_-)-(I_+-I_-)]=0,              (3)

with eta=1 for probability weights and eta=2 for amplitude weights under
the stated factorization. These are different types, not adjustable
coefficients. Coherent sums of multiple histories need their actual Gram
cross terms and need not obey either simple factorization. All moving
preparations, endpoints and suffix factors stay in r or the actual prices.
Equality at one point or equality of one first derivative is weaker than
(3) on an admitted neighbourhood; full source equality requires dG=0
in every relevant variation. Neither C nor I may be defined retrospectively
from the desired odds to claim physical binding.

## 3. A common per-block normalizer survives a variable stopping clock

Fix a fully specified stopping rule and record space. Suppose the complete
normalized history law is P_y(omega), its executed length T(omega) is a
fixed function of the record, and every actual block weight factors as
`w_z(y)=N(y) q_z(y)`. Then the same complete raw history weight and its
normalized law are

    W_y(omega)=N(y)^T(omega) P_y(omega),
    Z(y)=sum_omega W_y(omega), Q_y=W_y/Z.

For a finite cap all sums are finite. For an uncapped rule require almost
sure termination and a neighbourhood admitting differentiation of the
weighted sums; finite ET at one point alone is not a sufficient domination
hypothesis. At a background N=1, P normalized implies Z=1 and

    d log Z=E_P[T] d log N,
    d log Q(omega)-d log P(omega)
          =(T(omega)-E_P T) d log N.                   (4)

This is a source identity for actual unchanged stopping histories. A
background calibration N=1 does not make their derivatives equal.
For fixed T the centred clock term vanishes; for variable T it need not.
Separate preparations, terminal charges or history-dependent block
normalizers require their own retained terms rather than being hidden
inside a common N. No stop rule, entropy law or price is selected here.

## 4. Reconstruction boundary

Equations (1)–(4) are rederived and checked anew. They do not restore an
unavailable patch/bundle or certify its historical test counts. The
full-flag positive measurement theorem and this negative scalar candidate
test are compatible: observability and actual source selection are distinct
claims about the same proposed completion route.
