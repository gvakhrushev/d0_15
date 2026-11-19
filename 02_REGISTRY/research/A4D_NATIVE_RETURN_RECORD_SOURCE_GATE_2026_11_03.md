# Один native return/record канал: полный дифференциал и точный остаточный gate

3 ноября 2026. Existing scientific [PR #334](https://github.com/gvakhrushev/d0_15/pull/334).
Pinned scientific input: `e63ef7a3073f4854a2fc8fd4c69bf004bc42d544`.
Phase: native realization / final source composition.
Consumer: B–D [краткого scoped contract](A4D_SCOPED_NATIVE_KAPPA_CONTRACT_2026_11_03.md),
existing `constitutive` and `native_sector`.

**Результат.** У текущего scalar-corner return есть ровно два дифференциальных
вклада: через текущий corner \(c\) и через настоящий Gram сохранённого прошлого
\(A\). На fixed-old chart нового §7eo второй вклад отсутствует. Поэтому этот
return не даёт нового независимого канала при добавлении свободного
same-c controller. На declared H.1 graph источник с положительным gain сохраняется
как constrained pullback; его native task/price selection остаётся отдельной
предпосылкой. Это application существующих теорем к новому §7eo, а не
повторный поиск roots и не универсальный no-go для operator-valued records.

## 1. Какие уже стоящие результаты реально потребляются

Главный [source owner](A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md)
на pinned input имеет следующую точную область.

| Вход | Использование здесь | Сохраняемая граница |
|---|---|---|
| §7eh.H.1; §7el.A AC1–AC3 | Реальный word, canonical births, paid fullStep, generated banks/cuts и полный growing clock | Task graph задан; forced выбор задачи не доказан |
| §7ei EI4, EI6–EI17; KAPPA K10–K12 | Все 16+24+2 source rows, независимые preparation legs, full norm и two-way κ transport | Declared regular H+J sector, не unrestricted Cost−Info |
| §7en FN2–FN7 | Точное whole-price conjugacy faithful same-layout complete-operator implementations | Новый layout, изменённый task и свободная scene не включаются автоматически |
| §7eo.C NG15–NG19 | Настоящий return с retained output Gram A | A не заменяется скаляром до дифференцирования |
| §7eo.F CD1–CD5 | Canonical old identity, normalized moving input, реальные adjoints и upstream rows | Independent READY/P0/visibility вне fixed H.1 |
| §7eo.G FA4–FA5 | Exact finite-comparison covector и source transport | Не любой нелинейный chord и не старый raw216 |
| §7eo.I.4 | Полный заданный Book03 §03.25 H+J | Равенство другим Cost−Info/H+J+R не дано |

Общий κ theorem содержит Einstein–two-CAR; его dust specialization не
является пределом всей уже имеющейся положительной конструкции.
Здесь эти результаты используются с их исходными гипотезами; вся большая
аналитическая цепочка заново не сертифицируется.

## 2. Выбран один канал: actual scalar-corner return с полной old Gram

Берём NG15 исходного owner, с исходным \(z=2^{-20}\), \(c>0\).
Его ACTUAL OUTPUT Gram и удобный для расчёта input Gram связаны явно:
для настоящего old-return map \(C_<:\mathbb C^r\to\mathbb C^m\)
\[
A_{\rm in}=C_<^*C_<,\qquad A_{\rm out}=C_<C_<^*,\qquad
\det(dI_m+zc^2A_{\rm out})
=d^{m-r}\det(dI_r+zc^2A_{\rm in}),\quad d=1-z.
\]
Далее **\(A=A_{\rm in}\)** на исходном rank-r input. Полная output convention
сохраняет \(J_{\rm out}=J_{\rm in}-(m-r)\log(1-z)\); константа не удаляется
из абсолютной цены. При fixed \(m,r,z\) дифференциалы и \(w\) обеих
conventions совпадают. Output Gram canonical isometry на большем carrier
есть проектор, не \(I_m\). В выбранной input convention:
\[
D=(1-z)I+zc^2A,\qquad
J(c,A)=-\operatorname{Tr}\log D,\qquad
w=\operatorname{Tr}(zc^2A D^{-1}).
\]
Даже при singular \(A\) матрица \(D\) положительно определена. Положительность
\(w\) требует ненулевого \(A\); на actual canonical \(A=I_r\) она выполнена.
Ни \(z\), ни input rank не варьируются в этом fixed-layout расчёте.

Из дифференциала logdet, без требования \([A,dA]=0\), следует
\[
\boxed{\displaystyle
dJ=-\frac{2w}{c}\,dc
     -zc^2\operatorname{Tr}(D^{-1}dA).}                       \tag{1}
\]

Первый член — уже существующий reporter source. Второй является единственным
дополнительным кандидатом **внутри этой конкретной формулы return**.
Это не исчерпывает независимые heat, matter, scene или реальные Cost−Info
terms полной физической цены.

Пусть \(t\) — действительно допустимый независимый controller с \(c_t\ne0\).
Компенсируя его так, чтобы \(dc=0\), получаем точный quotient covector:
\[
\boxed{\displaystyle
\mathcal J_\perp[v]
=J_Y[v]-\frac{c_Y[v]}{c_t}J_t
=-zc^2\operatorname{Tr}\!\left[
D^{-1}\left(A_Y[v]-\frac{c_Y[v]}{c_t}A_t\right)\right].}       \tag{2}
\]
Это уже учитывает, что тот же controller может менять сам архив \(A\).
Если он меняет лишь \(c\), остаётся \(-zc^2\operatorname{Tr}(D^{-1}A_Y[v])\).
Наличие ненулевого \(A_Y\) само по себе ещё не гарантирует ненулевой trace,
совместной внутренней стационарности или Einstein match.

## 3. Подстановка именно в новый native graph

### 3.1. Fixed-old текущий field chart

В §7eo.F CD1–CD2 прежняя история перед новым body имеет canonical-completion
endpoint identity на всём old carrier. На текущем chart, где этот old prefix
фиксирован, \(A\equiv I_r\); поэтому \(A_Y=A_t=0\) и
\[
\mathcal J_\perp\equiv0,\qquad
E_Y^J=L^*E_t^J,\qquad Lv=c_Y[v]/c_t.                         \tag{3}
\]
Положительный \(w\) не делает этот канал независимым. Это точная подстановка
в shared-map lemma [31 October](A4D_JOINT_THERMAL_STATIONARITY_AND_SHARED_SOURCE_LOSS_2026_10_31.md),
а не новый heat-balancing root.

Для **полной** цены такая факторизация следует лишь тогда, когда все её
меняющиеся аргументы проходят через тот же map. Здесь из (3) не делается
автоматический вывод о любых дополнительных heat/Cost−Info terms.
Вариант spatial heat уже имеет собственные
[ограничения](A4D_POST_CONTROLLER_SPATIAL_HEAT_SOURCE_TEST_2026_11_03.md);
его не подставляем вместо невычисленного return/record остатка.

### 3.2. Moving normalized input и generated reference

При настоящем normalized embedding \(i^*i=I_r\), passive birth inclusion
\(B_<\) и generated reference §7eo.F CD3(3) даёт
\[
C_{\rm phys}=i^*B_<^*(cI)B_<i=cI_r.
\]
Поэтому \(\delta_iC_{\rm phys}=c\,\delta(i^*i)=0\) при fixed \(c\);
это не пропущенная input derivative.

Если old unitary \(V\) также свободно варьируется около identity, положим
\(j=B_<i,\ M=j^*Vj,\ A=M^*M\); \(j^*j=I_r\).
Так носитель V согласован с фактическим passive birth embedding. В центре:
\[
dM=(dj)^*j+j^*dj+j^*(dV)j=j^*(dV)j,\qquad
dA=dM^*+dM=0.                                               \tag{4}
\]
Это использует реальную skew-adjoint unitary tangent, включая proper cut.

**Область (4) принципиальна:** она даёт только first source в canonical
центре, не тождество на окрестности всех freely changed old histories.
Proper-cut rotation \(M(t)=\cos t\) имеет
\(A'(0)=0\), но \(A''(0)=-2\). Такой second jet нельзя удалять.
Следовательно, иной реально выбранный moving old-history channel не исключён;
он ещё требует собственного полного stationary reduction и source match.

### 3.3. Независимый normal действительно имеет native происхождение

[Literal-word owner 31 October](A4D_NATIVE_WORD_NORMAL_SOURCE_2026_10_31.md)
уже построил actual forward words одинакового оплаченного primitive inventory
и длины с
\[
c_\pm=c(1-2s_n^2)\mp2u g_ns_n,\qquad
c=p^3,\quad u=2p\sqrt p,\quad c^2+u^2=1.
\]
Их whole heat равен на собственном пятиwire/rank-eight homogeneous-clock
carrier этого owner; их полные Book prices различаются через J.
Эти слова не объявляются тем же §7eo growing history без transport.
Native discreteness сама по себе normal не устраняет.
На corresponding reflected orbit \(c_t=-2u\), поэтому
\[
J_t=\frac{4wu}{c}>0.                                        \tag{5}
\]
Используется опубликованный endpoint-small native comparison theorem,
а не заново создаваемый непрерывный primitive angle. Его исходная норма
не подменяется raw code-edit или raw216 нормой.

Исполнимость этих слов сама по себе не доказывает принадлежность тому же
fixed-report task. Именно этот вопрос решает D, а не значение (5).

## 4. Почему положительный fixed-task результат остаётся верным

На H.1 требуется \(r=Q_h(Y)\). Исходные §7eh.E.3 и KAPPA §2 сохраняют
\[
\mathcal L=B+\lambda(r-Q_h(Y)),\qquad
\lambda=-B_r,\qquad
E_Y^{\rm graph}=B_Y+DQ_h^*B_r.                               \tag{6}
\]
Ненулевой \(B_r\) здесь — реальная реакция; это не свободное equation
\(E_r=0\). Если source-changing controller действительно отсутствует
в обоснованном task graph, shared-c no-go не требует его туда добавлять.
Значит (3) не опровергает constrained Einstein theorem.

Для полноты вариаций не нужно заново доказывать уже имеющееся:
§7en охватывает все faithful implementation variations своего строгого
same-layout complete-operator/marked fibre и доказывает полную price conjugacy.
Однако §7eo.F CD4 оставляет при расширении входов настоящие строки
\[
\begin{split}
\delta Q_{\rm READY}
 &=\lambda_{\rm vis}\sum_x\mu_xr_0\Delta
   (\delta a_f+\delta a_q-2\delta a_0),\\
\delta Q_0&=-\lambda_{\rm vis}(\Delta_y+\Delta_x)\delta P_0,\\
\delta Q_{\rm vis}&=4\delta\lambda_{\rm vis}.
\end{split}                                                  \tag{7}
\]
Их fixed H.1 не объявляет свободными. Если они допустимы физически,
их реальные уравнения требуется решить; если они generated/guarded,
требуется вывести именно это из native task data. То же относится к
действительно свободным seed/frame, scene, clock/layout.

## 5. Сильный, но достаточный для решения задачи source test

Для одной полной цены \(S(Y,n)\), где \(n\) содержит все реальные nuisance
coordinates, на разрешимой ветви \(E_n=0\) правильный объект —
\[
\mathcal E(Y)=E_Y(Y,n_*(Y))=d\,S(Y,n_*(Y)).
\]
Для \(S=F(c(Y,t))+R(Y,t)\), \(c_t\ne0\), исключение одного \(t\) даёт
\[
\boxed{\displaystyle
E_Y\big|_{E_t=0}=R_Y-\frac{c_Y}{c_t}R_t.}                    \tag{8}
\]
После этого всё ещё сохраняются остальные independent internal equations.
Даже вне shared clock может быть полное screening: у иллюстративной
\(S=\tfrac12t^2+\tfrac12(r-Y)^2\) уравнения \(E_t=E_r=0\)
делают \(E_Y=0\) для каждого \(Y\). Этот пример не объявляется моделью D0.

При невырожденном полном nuisance Hessian:
\[
H_{\rm red}=H_{YY}-H_{Yn}H_{nn}^{-1}H_{nY}.                  \tag{9}
\]
Gauge kernels требуют actual compatibility/quotient, не молчаливой
псевдообратной. Ненулевая (9) сама по себе не доказывает нелинейный match.
Нужен полный off-shell covector с faithful residual coverage и two-way
lift в одних нормах. Если gain стремится к нулю, ошибка контролируется
относительно настоящего gain; просто положительности на каждом шаге мало.

## 6. Где заканчивается вычисленное и начинается отсутствующий price input

Заданный master Book03 §03.25 действительно равен H+J; все его оплаченные
стадии и modes учтены. Добавление выбранного задним числом Shannon или R
не допустимо. В то же время §7eo.I.4 прямо не отождествляет этот master
со всеми прежними branch-price/Info conventions.

Для выбранного пользователем return/record/Cost−Info continuation имеется
готовый [BOOK_SOURCE_BINDING](sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/BOOK_SOURCE_BINDING.md),
§5.1. На настоящем полном алфавите историй:
\[
G=\sum_\omega(C_\omega-I_\omega)K_\omega^*K_\omega,\qquad
R_{\rm branch}=\sum_\omega\xi_\omega K_\omega^*K_\omega,
\]
\[
d\bar S=\operatorname{Tr}(\rho\,dG)
        +\operatorname{Tr}(d\rho\,G)+dW.                    \tag{10}
\]
В частности,
\[
dR_{\rm branch}=\sum_\omega\left[
d\xi_\omega K_\omega^*K_\omega+
\xi_\omega(dK_\omega^*K_\omega+K_\omega^*dK_\omega)\right].    \tag{11}
\]
В (11) нельзя оставить только Born/effect derivative и потерять real price,
moving Info, input или work contribution.

**Одна ближайшая подстановка:** для того же H.1 word получить из его
native task и full pricing выбранные \((C_\omega,I_\omega,W)\), либо
доказанное source-equivalent operator binding, и подставить их в (8),
затем решить оставшиеся внутренние строки. Это не обещание, что такого
вклада обязательно достаточно или что он ненулевой. Таблица не может
определяться из желаемого Einstein residual.

Если binding действительно сводит всю цену только к shared c, при свободном
controller этот вариант остановлен. Если выведенный guard исключает такой
controller, применяется существующий constrained source (6). Если binding
даёт independent residual, проверяется его Einstein match **до** расширения
материи/класса. Это варианты исхода одной проверки, не три новые программы.

## 7. Exact finite source не подменяет другой source contract

Новый §7eo использует полный covector
\[
\ell_h(v)=\sum_\alpha(J_hv)_\alpha
\frac{B(W_{\alpha,+})-B(W_{\alpha,-})}{2t_\alpha\Gamma_h}.     \tag{12}
\]
Каждая равная пара цен даёт точный нуль её компоненты. Весь полный базис
на одном paid centre даёт \(\ell_h=0\) точно; nonlinear multi-plane chord
не обязан совпадать с этим линейным определением.

FA5 даёт transport к прежнему κ-source:
\[
\|s_{\kappa,h}-\ell_h\|_{\mathrm{original},*}
\le\varepsilon_h.
\]
Отсюда source-null в κ-пределе при нужном контроле ошибки. Exact zeros
другого конечного Euler из этого не следуют. Все basis constants,
price-error / \((|t|\Gamma_h)\) и actual Jacobians сохраняются.
Обычные graph-source identities CD3–CD4 имеют собственное доказательство;
они не выводятся лишь из равенства конечных пар.

## 8. Проверка, потребитель и неизменённая граница

[Узкий exact checker](sources/d0_native_return_record_gate_2026-11-03/check_return_record_gate.py)
проверяет (1) по независимому det derivative, включая noncommuting
Hermitian dA, explicit input/output Gram transport, nonzero fixed-c record
control, moving-controller matrix compensation (2), canonical (4), normalized
moving input, Golden (5), compensated residual (2)/(8) и screening control.
Контроль \(A=\cos^2t\) предотвращает ложный перенос centre identity на chart.
Все выводы о D0 admission и Einstein match остаются аналитическими
обязательствами, а не hard-coded flags проверки.
[Наблюдаемый результат](sources/d0_native_return_record_gate_2026-11-03/result.json).

Изменение общего аргумента: C для declared H+J graph переиспользуется;
B сводится к конкретному независимому остатку (2)/(8), а D — к native
основанию graph и price binding. Exact finite roots не расходуются как
замена этим подстановкам. Новых roots, heat census, full128 suite или
геометрических коэффициентов здесь нет.

`GR_closed=false`, `unrestricted_D0_GR_closed=false`; исходные raw216,
assembly acceptance, `positive_gr` и lifecycle #334 не повышены.
