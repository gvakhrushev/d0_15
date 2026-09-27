# D0 v16 one-tick balance and two-split owner

**Task:** WRK-D0-V16-ONE-TICK-BALANCE-TWO-SPLIT-OWNER  
**Status:** exact finite owner  
**Terminal:** D0-V16-ONE-TICK-BALANCE-OWNER-CERTIFIED

## 1. Theorem

Let a finite Hilbert space split orthogonally as

\[
H=\operatorname{im}P\oplus\operatorname{im}Q
\]

and let a unitary tick be written in that split as

\[
U=
\begin{pmatrix}
A&B\\
C&D
\end{pmatrix}.
\]

Define

\[
F_N=C^\dagger C,\qquad
F_Q^{\mathrm{emit}}=B^\dagger B.
\]

No equality of sector dimensions is assumed.

From \(U^\dagger U=I\),

\[
A^\dagger A+C^\dagger C=I_P.
\]

From \(UU^\dagger=I\),

\[
AA^\dagger+BB^\dagger=I_P.
\]

Finite trace cyclicity gives

\[
\boxed{
\operatorname{Tr}F_N
=
\operatorname{Tr}F_Q^{\mathrm{emit}}
=
\operatorname{rank}P-\|A\|_{\mathrm{HS}}^2.
}
\]

Hence the unrestricted fixed-tick ratio

\[
\sigma_N=
\frac{\operatorname{Tr}F_Q^{\mathrm{emit}}-\operatorname{Tr}F_N}
{\operatorname{Tr}F_Q^{\mathrm{emit}}+\operatorname{Tr}F_N}
\]

is zero whenever the denominator is nonzero, and is defined as zero when both channels vanish.

The retained-sector budget is

\[
\boxed{
\operatorname{Tr}\bigl((PUP)^\dagger(PUP)\bigr)
+\operatorname{Tr}F_N
=
\operatorname{rank}P.
}
\]

The \(P\leftrightarrow Q\) companion identities are

\[
\operatorname{Tr}F_Q^{\mathrm{emit}}
=
\operatorname{rank}Q-\|D\|_{\mathrm{HS}}^2
\]

and

\[
\operatorname{Tr}\bigl((QUQ)^\dagger(QUQ)\bigr)
+\operatorname{Tr}F_Q^{\mathrm{emit}}
=
\operatorname{rank}Q.
\]

## 2. Exact unequal-rank witness

Use \(\operatorname{rank}P=2\), \(\operatorname{rank}Q=3\), basis
\((p_1,p_2,q_1,q_2,q_3)\), and

\[
(c_1,s_1)=(3/5,4/5),\qquad
(c_2,s_2)=(5/13,12/13).
\]

Then

\[
U=
\begin{pmatrix}
c_1&0&-s_1&0&0\\
0&c_2&0&-s_2&0\\
s_1&0&c_1&0&0\\
0&s_2&0&c_2&0\\
0&0&0&0&1
\end{pmatrix}
\]

is exactly orthogonal. The two channel traces are

\[
\operatorname{Tr}F_N
=
\operatorname{Tr}F_Q^{\mathrm{emit}}
=
\frac{16}{25}+\frac{144}{169}
=
\frac{6304}{4225}.
\]

The retained compression has

\[
\|A\|_{\mathrm{HS}}^2
=
\frac{9}{25}+\frac{25}{169}
=
\frac{2146}{4225},
\]

hence

\[
\frac{2146}{4225}+\frac{6304}{4225}
=
2
=
\operatorname{rank}P.
\]

The companion \(Q\)-budget is exactly \(3=\operatorname{rank}Q\).

## 3. Hostile controls

1. Sector preserving: \(U=I\) gives \(B=C=0\), both channel traces zero.
2. Nonunitary failure: on the same \(2+3\) split, a nonunitary block with \(C_{11}=1\), \(B=0\) gives traces \(1\) and \(0\). The equality is therefore a unitarity consequence.
3. Padding: adding identity spectators inside \(Q\) leaves both channel traces and the \(P\)-budget unchanged; only the \(Q\)-budget grows by the spectator rank.
4. No phase inference: the theorem is a fixed-tick balance/no-go only.

## 4. Formal-owner status

The generic finite proof follows from the two unitary block identities and finite trace cyclicity. The repository certificate checks the load-bearing identities and hostile controls using exact rational arithmetic.

No Lean file is claimed by this bounded worker. Status is exact-certificate owner; Lean formalization was not added.

Certificate:

02_REGISTRY/research/certificates/d0_v16_one_tick_balance_two_split_check.py

## 5. Boundary

A nonzero channel sign cannot be an unrestricted observable of one fixed unitary tick. It must live on a declared history, moving split, window, sector restriction, or other non-global comparison.
