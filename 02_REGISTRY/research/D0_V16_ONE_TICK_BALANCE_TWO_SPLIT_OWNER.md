# D0 v16 one-tick balance and two-split owner

**Task:** `WRK-D0-V16-ONE-TICK-BALANCE-TWO-SPLIT-OWNER`  
**Status:** exact finite owner  
**Terminal:** `D0-V16-ONE-TICK-BALANCE-OWNER-CERTIFIED`

## 1. Theorem

Let a finite Hilbert space split orthogonally as
[
H=Poplus Q
]
and let a unitary tick be written in that split as
[
U=egin{pmatrix}A&B\\ C&Dend{pmatrix}.
]
Define the retained-to-archive and archive-to-retained Gram channels
[
F_N=C^dagger C,qquad F_Q^{m emit}=B^dagger B.
]

No equality of sector dimensions is assumed.

From (U^dagger U=I), the (P	o P) block is
[
A^dagger A+C^dagger C=I_P.
]
Taking finite traces gives
[
operatorname{Tr}(C^dagger C)
=operatorname{rank}P-operatorname{Tr}(A^dagger A).
]

From (UU^dagger=I), the (P	o P) block is
[
AA^dagger+BB^dagger=I_P.
]
Finite cyclicity gives
[
operatorname{Tr}(A^dagger A)=operatorname{Tr}(AA^dagger),
qquad
operatorname{Tr}(B^dagger B)=operatorname{Tr}(BB^dagger),
]
therefore
[
oxed{operatorname{Tr}F_N=operatorname{Tr}F_Q^{m emit}
=operatorname{rank}P-|A|_{m HS}^2.}
]

Hence the unrestricted fixed-tick ratio
[
sigma_N=
rac{operatorname{Tr}F_Q^{m emit}-operatorname{Tr}F_N}
{operatorname{Tr}F_Q^{m emit}+operatorname{Tr}F_N}
]
is exactly zero whenever the denominator is nonzero, and is defined as zero when both channels vanish.

The retained-sector budget is
[
oxed{
operatorname{Tr}igl((PUP)^dagger(PUP)igr)+operatorname{Tr}F_N
=operatorname{rank}P.}
]

The (Pleftrightarrow Q) companion identities are
[
operatorname{Tr}F_Q^{m emit}
=operatorname{rank}Q-|D|_{m HS}^2,
]
and
[
operatorname{Tr}igl((QUQ)^dagger(QUQ)igr)
+operatorname{Tr}F_Q^{m emit}
=operatorname{rank}Q.
]

## 2. Exact unequal-rank witness

The certificate uses (operatorname{rank}P=2), (operatorname{rank}Q=3), basis order
((p_1,p_2,q_1,q_2,q_3)), and two rational Pythagorean rotations:
[
(c_1,s_1)=(3/5,4/5),qquad(c_2,s_2)=(5/13,12/13).
]
Thus
[
U=
egin{pmatrix}
c_1&0&-s_1&0&0\\
0&c_2&0&-s_2&0\\
s_1&0&c_1&0&0\\
0&s_2&0&c_2&0\\
0&0&0&0&1
end{pmatrix}.
]
It is exactly orthogonal, hence unitary over the real subfield. The two channel traces are
[
operatorname{Tr}F_N
=operatorname{Tr}F_Q^{m emit}
=rac{16}{25}+rac{144}{169}
=rac{6304}{4225}.
]
The retained compression has
[
|A|_{m HS}^2
=rac{9}{25}+rac{25}{169}
=rac{2146}{4225},
]
so
[
rac{2146}{4225}+rac{6304}{4225}=2=operatorname{rank}P.
]
On the (Q) side, the fixed spectator contributes one unit to (|D|_{m HS}^2), and the companion budget is exactly (3=operatorname{rank}Q).

This explicitly rules out any hidden equal-dimension assumption.

## 3. Hostile controls

1. **Sector preserving.** (U=I) gives (B=C=0), both channel traces zero and (sigma_N=0) by convention.
2. **Nonunitary failure.** On the same (2+3) split, a deliberately nonunitary block with (C_{11}=1) and (B=0) has (operatorname{Tr}C^dagger C=1) and (operatorname{Tr}B^dagger B=0). Equality is therefore a unitarity consequence, not a block-shape tautology.
3. **Padding.** Appending any identity spectator inside (Q) appends zero rows/columns to (B,C) and an identity block to (D). The channel traces and the (P)-budget are unchanged; the (Q)-budget increases by exactly the added rank. Zero padding therefore cannot manufacture or destroy the carrier theorem.
4. **No phase inference.** The result is a fixed-tick balance/no-go only. It does not produce a remnant phase, a Bondi sign or a history sign.

## 4. Formal-owner status

The mathematical statement is proved above for arbitrary finite complex blocks by the two unitary block identities and finite trace cyclicity. The repository certificate independently checks the load-bearing identities and hostile controls using exact rational arithmetic.

No new Lean file is claimed in this worker. A generic Mathlib block-matrix formalization would require choosing and stabilizing a finite direct-sum/block API that is not needed for the theorem or its exact certificate. Therefore the status is explicitly **exact-certificate owner; Lean formalization not added by this bounded worker**.

Certificate:
`02_REGISTRY/research/certificates/d0_v16_one_tick_balance_two_split_check.py`.

## 5. Boundary

This owner certifies only the unrestricted one-tick balance and the two sector budgets. A nonzero sign must live on a history, declared window, moving split, sector restriction, or other non-global comparison. That constructive problem belongs to `WRK-D0-V16-MOVING-SPLIT-CHANNEL-SIGN`.
