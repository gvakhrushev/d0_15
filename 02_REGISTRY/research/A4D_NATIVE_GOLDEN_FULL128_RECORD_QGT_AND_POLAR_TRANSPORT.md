# Обратная сцепка D0 → ОТО: информационная метрика и перенос из одного полного золотого record

17 октября 2026. Research continuation of existing Draft #334 / EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE. Scope: EXACT FULL128 ORIGINAL-KRAUS MATHEMATICS / N-TAPE SECOND SOURCE / NATIVE FULL16 FIRST-SHELL CONTROL. Not a physically selected Cost−Info, GR field law, new gate, claim, or the original all-ten h^-2/#216 terminal.

## 0. Реальные источники и потребитель

Consume, do not replay, A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md (actual SELECT vs reflector M, all128 golden Kraus and full relative transfer), A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md (physical GKSL channel), A4D_RELATIVE_RECORD_PRINCIPAL_ANGLES_AND_MOMENTS.md, A4D_NATIVE_RETAINED_RECORD_ADMISSION.md, A4D_TWO_SIDED_SPATIAL_RECORD_EINSTEIN_SOURCE.md and A4D_TWO_SIDED_NULL_BIANCHI_GLOBAL_COMPLETION.md (conditional nonlinear Einstein consumer). M denotes the ACTUAL reflected output column, not the SELECT N. Keep all64 coefficient/label columns, both ports, all16 CAR forms, reference128 spectator, original field jets and true clock.

## 1. A fixed golden basis change makes the entire real 128-output isometry transparent

Let p=phi^-1, q=p², a=sqrt(p), p+q=1, and stacked actual reflector columns M_alpha,x with sum_alpha M_alpha,x† M_alpha,x=I. The original 128 data operators are
K_0alpha=p delta_alpha0 I+q M_alpha,
K_1alpha=p sqrt(p)(M_alpha-delta_alpha0 I).

The constant real orthogonal matrix
R=[[sqrt(p),p],[-p,sqrt(p)]], R†R=I,
gives for EVERY alpha, without dropping either physical port,

    [K_0alpha;K_1alpha] = R [sqrt(p) delta_alpha0 I; p M_alpha].   (1)

This is a field-independent change of mathematical output coordinates, not an assumed physically executable coherent postprocessor. For the complete Stinespring isometry V_x made from the unchanged 128 K, V†V=I and EXACTLY

    C_yx = V_y†V_x = p I+p² M_y†M_x.                              (2)

From the actual original tape, s_min(C_yx)>=p-p²=p³ and ||C_yx||<=1 for all one-round native configurations in the same stored frame. Thus its positive and polar factors are canonical:
    H_yx=(C_yx†C_yx)^(1/2)>0,
    U_yx=C_yx H_yx^(-1) unitary.
No eigenvector choices or added operator are necessary. For real native arrays the local polar factor is orthogonal, continuously connected to SO(d) at the diagonal. At arbitrary n tape depth there is NO uniform invertibility theorem: do not transfer the one-round p³ bound to C_n.

## 2. New exact golden record quantum-geometric tensor (QGT)

Let H_v=d_v M, B_v=M†H_v skew-adjoint, W_v=(I-MM†)H_v. Define the FULL-native Berry connection and horizontal Hermitian tensor:
    A_v = V†d_v V = p² B_v,
    Q(v,w) = (d_v V)†(I-VV†) (d_w V).

Using (1) and golden p^4+p^3=p² yields the EXACT native identity

    Q(v,w) = p³ B_v†B_w+p² W_v†W_w.                              (3)

Proof: sum over all physical alpha and two ports of dK_v†dK_w equals p² H_v†H_w, while sum K† dK =p² M†H_v. Subtract A_v†A_w and decompose H_v=MB_v+W_v. In particular:

    p³ ||H_v||_HS² <= Tr Q(v,v) <= p² ||H_v||_HS².               (4)

There are NO invisible velocities of the complete reflected record M in its own positive information geometry. The physical fields may still be lost in the field-to-M Jacobian, which is not asserted injective. Q here is a metric on recorded changes, not automatically the physical Lorentz coframe metric.

For C(t)=V_(x+tv)†V_x, the full isometry implies
    C(t)†C(t)=I-t²Q(v,v)+O(t³),
    -log_phi det(C(t)†C(t))
      =t² Tr Q(v,v)/ln(phi)+O(t³).                              (5)
Its diagonal first Euler source is identically ZERO. A self-comparison is NOT a universal off-shell Einstein action: an independent comparative reference or a different owned action is necessary.

## 3. One native overlap also gives an operator-valued curved parallel transport

If the full isometry frame is changed at x,y by U_x,U_y, then
    C_yx -> U_y† C_yx U_x, polar(C_yx)->U_y† polar(C_yx) U_x.
Therefore ordered polar products around a native comparison loop transform by conjugation. For the SAME V,
    A_mu=p² M†d_mu M,
    F_mu,nu=d_mu A_nu-d_nu A_mu+[A_mu,A_nu]
           =Q_mu,nu-Q_nu,mu.                                  (6)

This is an exact operator identity from complete Kraus, not a claimed Lorentz LC curvature equation. Scalar trace Q alone loses the non-Abelian F information.

Negative gauge control: rotating only M->M U(x) but holding the direct sqrt(p)I branch fixed changes the native comparison plane; it is NOT a whole-frame gauge V->VU. True local Lorentz Ward requires a real joint transport of coframe, observer, all labels, preparation and input/output frames. The positive Hilbert polar lies in O(d)/U(d), not automatically the full noncompact Lorentz representation.

Exact independent noncommuting SO(3) isometry CLASS control (not a claim of native gate admission):
M(x,y)=exp(xX)exp(yY) with X=E21-E12, Y=E32-E23. At the origin F_xy=-p³[X,Y]!=0. The forward ordered polar plaquette 0→(t,0)→(t,t)→(0,t)→0 is I+t²p³[X,Y]+O(t³)=I-t²F_xy+O(t³). The 22 exact two-jet tests check this sign, full polar unitarity and nonzero rank2 curvature.

## 4. Complete retained n-tape first/second source without 128^n word sums

Actual owned relative transfer is
    T_yx(B)=sum_(all128) K_y† B K_x
           =p B+p² sum_(64) M_y† B M_x
           =B+epsilon_h L_rel,yx(B), epsilon_h=p² h²/64.        (7)

At x=y denote Phi=T_xx, Phi(I)=I. Vary y=x+tv at fixed x; define U(B)=d_t T(B)|0=p² sum(dM)† B M, and W(B)=d_t² T(B)|0=p² sum(d²M)† B M. For the COMPLETE retained tape comparison C_n(t)=T_t^n(I), set D_n=C_n'(0), E_n=C_n''(0). EXACT finite recurrences:

    D_0=E_0=0,
    D_(n+1)=Phi(D_n)+U(I),
    E_(n+1)=Phi(E_n)+2U(D_n)+W(I).                             (8)

The whole actual native n-tape positive tensor is

    Q_n(v,v)=-(E_n+E_n†)/2-D_n†D_n >=0.                        (9)

Proof: ordinary product differentiation for (8), and Stinespring isometry of the full product tape for positivity of (9). The computation takes O(n) applications of maps rather than enumeration of 128^n histories and retains all moving native controller/coframe/link/reference sources. It is a comparison sensitivity, NOT selected average pointer Shannon or original H+J+R action.

Exact class witness M_x=I, M_(x+tv)=exp(tX), X†=-X:
    D_n=-np²X,
    E_n=[np²+n(n-1)p^4]X²,
    Q_n=np³ X†X.                                                (10)
The potentially O(n²) terms in (9) cancel EXACTLY; freezing either the future record or the preparation source would give a false growth law.

## 5. Actual full16/eight-momentum native first-source fixture and a decisive reference boundary

Consume the already-owned full SELECT+REFLECTION calculation from the genuine 128-output native owner (do not replace M by N): on each of all8 first-shell momenta and all16 grades,
    C_yx,h=(1-p² w_h f_yx/128)I16, w_h=4sin²(pi h),
    f_yx=nu_x²+nu_y²-nu_x nu_y(1+nu_x nu_y+b_x b_y),
    nu_j²+b_j²=1.                                              (11)

Keep y=(5/13,12/13) as an INDEPENDENT fixed native reference and vary the x-coframe on the normalized actual circle
    (nu_x(t),b_x(t))=((3/5)cos t+(4/5)sin t,
                      (4/5)cos t-(3/5)sin t).
Exactly
    f(0)=226/4225, f'(0)=1736/4225 != 0.                     (12)

On the ORIGINAL n_h=128/h² clock (n_h epsilon_h=2p²=beta), entire scalar n-tape comparison is c_h^n. The mathematical logdet price per system eigenmode and its actual comparative first source have the limit

    price_inf(t)=8pi²p² f(t)/ln(phi),
    price_inf'(0)=8pi²p²(1736/4225)/ln(phi)
                 =25.75141919001683... !=0.                   (13)

This is the real native-data relative-record differential on full16, not any Einstein scalar input. All x and y configurations in this fixture have spatially constant flat metric coframes. Thus the *unmodified direct relative price by itself* cannot be universally the pure Einstein-Hilbert action on this class: EH curvature vanishes there, while (13) is nonzero. A cosmological/independent matter/reference source or the proven TWO-SIDED 4D-minus-spatial comparison would change the functional and needs a physical binding. Different reference y changes the source; arbitrary y is not a universal physical selection.

When y=x(0), the exact diagonal derivative is zero and f_diag''(0)=41/25. Its positive information-metric coefficient is
    (1/2)price_inf''(0)
      =8pi²p²(41/50)/ln(phi)=51.39158512892472... .          (14)

The old k=0 Fourier negative control is preserved: literal native tape C_n(0)=I for all homogeneous x,y, whereas the independently constructed three-effect Einstein comparator has C_target(0)=sqrt(p)(1-z)I != I. Direct identity of the two complete instruments is excluded in that class; equality of appropriate source differences is a separate question.

## 6. One actual new consumer, not another operator catalogue

On the SAME native full128 retained tape, (3) gives a coercive positive metric of the recorded changes, (6) gives a covariant unitary relative record transport and non-Abelian curvature, (8)-(9) give the full-depth second source, and (13) gives a nonzero exact first-source example. These mathematical arrows are completed from the existing old reflectors and golden controller, without new Hilbert spaces, stress tensors, curvature actions, or a prescribed quantum measurement.

What remains ONE decisive physical-to-Einstein map is the ACTUAL admitted 4D/spatial 8+8 retained reference pairing and full cost:
    native actual 4D and two spatial Kraus/readout frames,
    -> independently fixed, physically costed cross K and clock/observer,
    -> same complete history Cost−Info with all moving source terms,
    -> signed Lorentz 4D−2×spatial source and genuine full Ward,
    -> nonlinear Einstein + independent matter and nonempty exact joint refinement,
    -> original ten packed unweighted h^-2 raw source comparator #216.

The native polar F in (6) is not secretly Lorentz Riemann; positive metric in (3) is not EH. They are a SHARED DATA CARRIER, giving explicit mathematical constraints for the final identifying morphism. Do not promote to GR while selection, Weyl/boost components, spin/matter 3-forms, strong source bounds and joint roots are open.

## 7. Narrow reproducible checks

Same disjoint new source folder contains:
- check_native_record_qgt.py: 43 exact golden/2-port, noncommuting tensor/curvature, whole n-depth jet recursion, actual full16/eight-shell native first-source/diagonal second-jet checks; normal and Python -O stdout byte-identical.
- check_polar_holonomy.py: 22 exact noncommuting real SO3 two-jet polar-unitarity/plaquette controls. SO3 here is only a mathematical class fixture, NOT an already admitted native M.
- RESULTS.json: pinned outputs and failure controls.

No old root/kernel/L8 spectrum, broad CAR catalog, Lean or expensive heat certificate replay. Local finite checks illustrate the general tensor identity proved algebraically here; they do not install a physical comparison/Cost−Info law.


## 8. Лоренцев буст НЕ может целиком жить в компактной полярной части: строгий firewall

Полярный \(U_{yx}\) из §3 лежит в unitary/orthogonal group относительно уже имеющегося положительного record inner product. **Он не может быть faithful continuous representation всей группы \(\mathrm{SO}^+(1,3)\)** на фиксированном конечномерном положительном Hilbert carrier.

Элементарное доказательство без классификации представлений: в вещественной простой алгебре \(\mathfrak{so}(1,3)\) имеются spatial rotations \(J_i\) и boosts \(K_i\) с \([J_i,K_j]=\epsilon_{ijk}K_k\), \([K_i,K_j]=-\epsilon_{ijk}J_k\). Оператор \(\mathrm{ad}_{K_1}\) на real span \((J_2,K_3)\) имеет матрицу \(\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\) и два НЕнулевых вещественных собственных значения \(+1,-1\). Если бы существовало ненулевое дифференциальное представление \(\rho:\mathfrak{so}(1,3)\to\mathfrak u(N)\), простота делала бы \(\rho\) инъективным. Но \(\mathrm{ad}_{\rho(K_1)}\) на compact \(\mathfrak u(N)\) кососамосопряжённо относительно положительной формы \(-\mathrm{Tr}(XY)\) и потому не может иметь действительных ненулевых собственных значений на invariant image. Противоречие. Значит \(\rho=0\). Для связной \(\mathrm{SO}^+(1,3)\) соответствующий непрерывный конечномерный unitary group homomorphism тривиален.

Это **не no-go D0**: фактический native operator дополнительно имеет положительную \(H_{yx}=(C^\dagger C)^{1/2}\), а физическая Lorentz tetrad/observer pairing в native теории не положительно-унитарна для boosts. Но искомый полный Einstein bridge НЕ может просто объявить полярный record \(U_{yx}\) already-owned full Lorentz \(L_{yx}\). Должна быть доказана совместная непрерывная карта \(C\)+positive dressing/observer → physical Lorentz transport, со своей реальной source/clock стоимостью.

**Ещё один проверяемый конечный предел.** Из \(p^3\le s_i(C)\le1\) для любого one-round full-native comparison
\[
\operatorname{cond}(C)\le p^{-3}=\varphi^3=2+\sqrt5.
\]
У любого предполагаемого прямого vector-representation positive boost \(B(\eta)\), собственные singular values \(e^{|\eta|},e^{-|\eta|},1,1\), так что \(\operatorname{cond}(B)=e^{2|\eta|}\). Если кто-то предлагает идентифицировать \(H_{yx}\) с \(B(\eta)\) up to scalar and conjugation by a FIXED positive orthogonal frame, необходимо
\[
|\eta|\le\frac32\ln\varphi=0.7218177375894053\ldots.
\]
Это ограничивает только указанный *direct one-round singular-value matching*. Составной multi-round/product scheme или настоящая indefinite-metric coframe representation не подпадают под этот bound. Более того, one-round gap НЕ доказывает существование global invertible n-round polar source.

Следовательно, реальный выигрыш новой record geometry следующий: скалярная положительная часть \(H\) и операторный compact transport \(U\) построены из ОДНОГО actual \(C\), а причинно-лоренцева интерпретация должна пройти проверку через уже собственные observer/coframe/link источники. Попытки отождествить U напрямую со всеми six Lorentz generators математически закрыты; это снимает ещё один бесполезный этап поиска.
