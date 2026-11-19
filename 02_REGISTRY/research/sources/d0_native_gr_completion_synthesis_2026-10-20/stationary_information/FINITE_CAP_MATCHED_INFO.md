# Finite capped complete tape: exact overlap and matched information

20 October 2026. Companion to `FULL_RECORD_TANGENT_AND_MATCHED_INFO.md`.
This supplies a strictly finite version of its information calculation.
It is a DIFFERENT capped task: stop at the first port1, or record an
explicit abort after N failures, N>=1. Every query, failure, work address,
clock and the abort remain; no conditional-success price is used.
This does not replace the owned unbounded first-success price or assert
that Book03 chooses either task or this information valuation.

Fix the same field-independent input, oldRIGHT, coherent three-query
interface and fixed postrotation, with c^2+s^2=1 and 0<q=s^2<1. Put

    f0=1-2t^2,                  f1=2t(1-t^2),
    alpha0=c f0-s f1,           alpha1=s f0+c f1,
    x=c alpha0,                d=1-x,
    r=4t^4(1-t^2),             d-s alpha1=2t^2.

All constants N,c,s are fixed under the field variations. Work on a
sufficiently small neighborhood of zero where d>0, alpha0 and alpha1
have the signs of c,s, and the same original positive query chart holds.
For fixed N there are finitely many tape slots and complete records.

## 1. Exact full-state overlap and actual CQ fidelity

The reference clean terminal amplitude after j failures and a success is
s c^j, 0<=j<N. Its actual clean projection is alpha1 alpha0^j times the
same input. The all-failure abort has reference amplitude c^N and actual
clean projection alpha0^N. Thus

    eta_N=sum_(j=0)^(N-1) s alpha1 x^j+x^N
         =1-[2t^2/d](1-x^N).                          (1)

The formula follows by the finite geometric identity, with no limit or
infinite expected-time assumption. It is the pure dilation overlap for
any fixed input purification. It is also the root fidelity of the actual
complete fine-pointer/CQ density relative to its clean reference: every
clean block contains the same normalized mixed logical/oldRIGHT density,
while every dirty block is orthogonal to reference support. The abort
block is explicitly present in the sum. No field-dependent access to
purification phases is assumed.

As x(0)=c^2=1-q and d(0)=q,

    eta_N=1-2 E_N t^2+O(t^3),
    E_N=[1-(1-q)^N]/q=sum_(j=0)^(N-1)(1-q)^j,
    Bures_N^2=4 E_N t^2+O(t^3),
    QFI_N|Sigma=16 E_N dt tensor dt.                  (2)

E_N is the exact reference expected number of executed trials, not the
maximum paid clock. In particular 1<=E_N<=N. For the stationary slice
Dt=0, Bures_N^2=O(||v||^4) and the field Fisher quadratic form vanishes.
These estimates have fixed-N local constants; no uniform claim for an
N selected as a field-dependent function is made.

## 2. Exact finite reverse relative entropy with abort

The clean reference probabilities are q(1-q)^j for success after j<N
failures, and (1-q)^N for abort. The corresponding ACTUAL full-record
clean weights are alpha1^2 alpha0^(2j) and alpha0^(2N). Their sum can be
less than one because the actual law also retains dirty-work histories.
Do not renormalize these weights.

The reverse full CQ entropy is therefore the FINITE sum

    D_N ln(phi)
     =sum_(j=0)^(N-1) q(1-q)^j
        [ln(q/alpha1^2)+j ln((1-q)/alpha0^2)]
       +(1-q)^N N ln((1-q)/alpha0^2).

The expected success count is 1-(1-q)^N=q E_N; the expected failure count
is (1-q)E_N. Consequently

    D_N=E_N {q ln(q/alpha1^2)
               +(1-q)ln((1-q)/alpha0^2)}/ln(phi)
       =[1-(1-q)^N] D_infinite
       =8 E_N t^2/ln(phi)+O(t^3).                    (3)

Here D_infinite denotes only the closed expression from the companion
note; the first two lines prove (3) finitely without executing or defining
an infinite apparatus. The formula is valid for arbitrary fixed mixed
logical/oldRIGHT input because its clean conditional density is unchanged.
It is an exactly calculated candidate valuation, not an actual native
Book03 Cost-Info binding.

The probability of at least one dirty event before stop/abort is exactly

    r sum_(j=0)^(N-1) alpha0^(2j)
       =r [1-alpha0^(2N)]/[1-alpha0^2].               (4)

To see this, the first dirty event on trial j+1 requires j clean failures,
each with scalar effect alpha0^2 I, followed by a dirty event of total
scalar probability r. Later events do not affect whether this happened.
This is positive for every small nonzero t and N>=1. Hence forward KL
against the clean reference remains infinite, even for this fully finite
experiment. A finite runtime does not cure a zero reference probability.

## 3. Same stabilization boundary with no unbounded runtime

For a fixed finite N the complete state has
sigma_N(y)=sigma_N*+t L_N+O(t^2). At a stationary root t=O(||v||^2), so
any C2 fixed record valuation has Hessian c H_t, and matched information
in (3) has zero field Hessian. Thus the absence of an independent positive
quadratic stabilizer is already a finite-experiment fact. Moving native
input/programme records, live CAR actuation and other upstream sources
retain exactly the exceptions stated in the companion note.
