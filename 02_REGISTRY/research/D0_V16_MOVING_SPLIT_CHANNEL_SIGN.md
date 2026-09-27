# D0 v16 moving-split / history channel sign

**Task:** WRK-D0-V16-MOVING-SPLIT-CHANNEL-SIGN  
**Status:** exact finite construction  
**Terminal:** D0-V16-MOVING-SPLIT-CHANNEL-SIGN-CERTIFIED  
**Execution baseline:** 5f6435eaaa93d42fb1956cb33b4badf3ceff0a1b

## 1. History requirement

On one fixed unitary tick,

\[
\operatorname{Tr}F_N(n)
=
\operatorname{Tr}F_Q^{\mathrm{emit}}(n).
\]

Therefore the sign below compares two declared history points. No Bondi quantity is identified with it.

## 2. Frozen carrier and windows

Use

\[
H=P\oplus Q,\qquad
\operatorname{rank}P=\operatorname{rank}Q=2
\]

with basis \((p_1,p_2,q_1,q_2)\), and freeze

\[
\Pi_{\mathrm{in}}=P,\qquad
\Pi_{\mathrm{out}}=Q.
\]

For rational Pythagorean pairs define

\[
U(c_1,s_1;c_2,s_2)=
\begin{pmatrix}
c_1&0&-s_1&0\\
0&c_2&0&-s_2\\
s_1&0&c_1&0\\
0&s_2&0&c_2
\end{pmatrix}.
\]

Take

\[
U_n=U(4/5,3/5;12/13,5/13)
\]

and

\[
U_{n'}=U(3/5,4/5;12/13,5/13).
\]

Only the first channel changes; the second is an exact spectator.

## 3. One-tick zero controls

At \(n\),

\[
A_n:=
\operatorname{Tr}(\Pi_{\mathrm{in}}F_N(n))
=
\frac{9}{25}+\frac{25}{169}
=
\frac{2146}{4225},
\]

and the same-tick conjugate emission trace is equal to it.

At \(n'\),

\[
B_{n'}:=
\operatorname{Tr}(\Pi_{\mathrm{out}}F_Q^{\mathrm{emit}}(n'))
=
\frac{16}{25}+\frac{25}{169}
=
\frac{3329}{4225},
\]

and the same-tick retained-to-archive trace is equal to it.

Thus each tick separately has global \(\sigma_N=0\).

## 4. History sign

Define

\[
\sigma^{\mathrm{budget}}_{n,n'}
=
\frac{B_{n'}-A_n}{B_{n'}+A_n}.
\]

Then

\[
\boxed{
\sigma^{\mathrm{budget}}_{n,n'}
=
\frac{1183}{5475}>0.
}
\]

Because the two frozen windows both have rank \(2\),

\[
\bar A_n=A_n/2,\qquad
\bar B_{n'}=B_{n'}/2,
\]

and therefore

\[
\boxed{
\sigma^{\mathrm{density}}_{n,n'}
=
\frac{1183}{5475}>0.
}
\]

The sign is not a rank-size artefact.

## 5. History-covariant swap

Under

\[
(P,Q,n,n',\Pi_{\mathrm{in}},\Pi_{\mathrm{out}})
\mapsto
(Q,P,n',n,\Pi_{\mathrm{out}},\Pi_{\mathrm{in}})
\]

the new input leak is the old \(B_{n'}\), and the new output emission is the old \(A_n\). Hence

\[
\boxed{
\sigma_{n',n}
[Q,P,\Pi_{\mathrm{out}},\Pi_{\mathrm{in}}]
=
-\sigma_{n,n'}
[P,Q,\Pi_{\mathrm{in}},\Pi_{\mathrm{out}}]
=
-\frac{1183}{5475}.
}
\]

The certificate recomputes this from the swapped decomposition.

## 6. Negative controls

1. Same-tick global sign is zero at both history points.
2. Sector-preserving history \(U_n=U_{n'}=I\) gives zero.
3. No temporal change \(U_n=U_{n'}\) gives zero even with nonzero channels.
4. Equal-rank windows preserve the nonzero sign after density normalization.
5. The unchanged \(25/169\) spectator contribution cancels from the numerator.
6. The finite ratio is not Bondi \(k(u)\), a flux, or an entropy rate.

## 7. Interpretation boundary

This construction closes the finite theorem-target that a nontrivial channel sign can live on a declared history while each global unitary tick remains balanced.

It does not construct

\[
\mathcal S:
(\operatorname{rank}P,\Lambda_{\mathrm{act}},
\varphi,R_\ast,\ldots)
\to(M_0,\tau_C).
\]

Certificate:

02_REGISTRY/research/certificates/d0_v16_moving_split_channel_sign_check.py
