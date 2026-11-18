# B91: first jet полного SOURCE и область входных колонок

**Результат.** Однобитный SAM в A46/B25 передаёт скалярный mean через A31, но не удовлетворяет исходному full-vector условию §7ej.MG3. Это не ограничение выбранного локального J: при прежнем binary affine field никакой real skew на всём SAM с произвольным фиксированным spectator не может дать требуемый вектор. Для реального полного ideal SOURCE предъявлен точный ненулевой linear witness по fresh coframe u/0/2, исключающий компенсацию другими полевыми направлениями. Существующая количественная native error bound слишком груба, чтобы превратить это свидетельство в доказанный ненулевой **actual compiled** defect.

Исходный проект уже содержит достаточную **двухбитную** карту MG2–MG3, точно проверенную ниже. Для целевого SOURCE дана граница на всех DATA columns при canonical source-private, но совпадение выбранной A23 vacuum extension с любым иным original full-column prefix и физический допуск остаются открытыми. Новая SOURCE-таблица/clock/price здесь не собираются. `physical_C_closed=false`, `GR_closed=false`.

## 1. Скалярная передача не равна векторной

В A46 для каждого из 2688 полевых coordinates имеется один born bit `v=(sqrt(p),p)`, `p²+p=1`, `Pr(1)=p²`; для всех остальных SAM и любого фиксированного spectator обозначим полный нормированный вход Φ. Пусть Π — projector на bit=1, X — **любой** real skew на всём разрешённом SAM⊗spectator. Оригинальный matched математический lift использует `P† B_s P` и поле `Y_b=Y0+s(b−p²)`; его ведущий CODE coefficient — `[Π,X]Φ`, а полный физический first jet требует Φ.

Положим `z=(I−2Π)Φ`, `H=[Π,X]`. H симметричен и block-off-diagonal по Π, поэтому `(I−2Π)H` skew. Следовательно

    <z,HΦ>=0,     ||z||=1,
    <z,Φ>=p−p²=p³,
    ||[Π,X]Φ−Φ|| ≥p³>0.                                  (1)

Это действует для любого общего X, включая смешивание SAM wires и фиксированного допустимого spectator; не предполагается, что X локален. Равенство достигается X=`u J_j`, `u=2p sqrt(p)`. Если дополнительно требовать точное scalar mean `<Φ,HΦ>=1`, проекция z ортогонально Φ имеет норму u, поэтому оптимальная граница усиливается до `p³/u`, достигаемой `X=J_j/u`. В исходной нескалированной MG1:

    ||[Π,J_j]Φ−uΦ||²=p⁶.

A31 корректно решает **другую** задачу: его Jacobian даёт right inverse среднего декодера и сохраняет scalar source. Он не превращает эту mean-строку в MG3 и не удаляет сохранённую SAM/DATA correlation. Никакого всеобщего GR no-go или запрета другого физического decoder из (1) не следует.

## 2. Точный witness на настоящем SOURCE target

Для current fresh Choi A46 выбрана оригинальная `S1/copy0`, slot 1372, site index 5=`(0,0,1,1)`, Julia address 21, input 0/output 4 — тот же исходный u/0/2 leaf, что в A30/B86. В идеальном bank этот Choi component равен `c·u_j(Y_b)`, где `c=1/sqrt(65568)` и для j=2 строго `u_j(Y0)=0`, `u_j(Y_b)=s(b_j−p²)`. Все остальные Choi copies имеют фиксированную anchor amplitude c на `(address,input,output)=(0,0,0)`; в каждом CAR фиксированный `(internal site=0,grade=1,fresh RIGHT=0)` имеет amplitude `d=sqrt(p)/128`, независимо от поля и банка.

Выберем **математический** norm-one output functional ℓ на 1440 Choi и 128 CAR source factors: на выбранной свежей Choi — указанный u-leaf, на остальных — их anchors. Фиксированный RAW frame включается в эту bra как unitary; SITE, old/reference и остальные носители сохраняются как output factors. A27 ideal product law и canonical private inputs дают для каждого b точное равенство

    ℓ Ψ_b = K·u_j(Y_b),
    K = c^1440 d^128 >0,    2^-13984 < K <2^-12416.       (2)

Эта конструкция использует один реальный source leaf и существующие амплитуды, а не новый physical selector или измерение. Она не выводит full-vector результат из одной скалярной компрессии: ℓ применяется к **полной выходной изометрии до SAM input-compression**, а не заменяет её.

Для matched идеального `F_s(P)=P† B_s P i`, `i=Φ⊗canonical_WORK`, (2) даёт точно для всех s и всех labels

    (I⊗ℓ) F_s(P) = Ks P†(Π_j−p²I)P Φ ⊗ |retained>,
    (I⊗ℓ) [F′_s(0)/s] = K[Π_j,X]Φ ⊗ |retained>,
    (I⊗ℓ) [Φ⊗∂_j A(Y0)] = KΦ ⊗ |retained>.

У (k≠j) та же contraction исходной source derivative равна нулю: выбранная амплитуда точно равна K·u_j, а все остальные anchors не зависят от поля. Поэтому на этом original SOURCE frontier, без неявной гипотезы о global source rank и без возможной компенсации другими `D_k A`, из (1) следует

    ||F′_s(0)/s − Φ⊗∂_j A(Y0)|| ≥ K p³ >0.              (3)

Это утверждение относится к ideal A46 product target и его matched analytic reference control, не к дискретной «производной угла native gate». Для norm-one **joint** будущего CODE/DATA effect эту полную output difference нельзя молча сжать до простого WORK-only expectation: последнее усреднение может стереть ортогональную SAM часть. Отдельный платный detector не заявлен.

У actual A46 подготовленная SOURCE isometry приближается с `η_prefix<2^-3232`. Для `||X||≤2` стандартный коммутатор даёт отклонение нормированной аналитической строки не более `2η_prefix||X||/s<2^-3200`. Имеющийся общий budget намного больше строгого, но крайне малого K из (2); он **не доказывает** ненулевость actual compiled vector defect. Это ограничение оценки, не утверждение его равенства нулю.

## 3. Уже принадлежащая проекту достаточная карта

§7ej.MG2–MG3 задаёт два born bits на одну координату:

    φ=(p,p√p,p√p,p²),  π_i=φ_i²,
    h_i=(1−2π_i)^−1, S=Σ_iπ_i h_i,
    V=diag(0,1,2,3)−3p²I,
    H_ii=0, H_ij=φ_iφ_j(h_i+h_j)/(1+S),
    X_ij=H_ij/(i−j), i≠j.

Независимая exact арифметика в Q(a), `a=√p`, `a⁴+a²−1=0`, проверяет `φᵀφ=1`, `<φ,Vφ>=0`, `Xᵀ=−X`, `[V,X]φ=φ`. Дополнительно

    ||X||_F² = 391/363−491√5/4356 <1,
    Σ_(i<j)(−X_ij)
      =13/33−√5/66 + √p(21+3√5)/22 <3/2.

Для m=2688 независимых пар получаем `[V_j,X_k]φ^⊗m=δ_jk φ^⊗m` как полное векторное равенство. Это **достаточная указанная исходная карта**, а не доказательство, что любой другой глобальный код обязан иметь два новых бита на каждую координату. §7ej.MG8–MG10 задаёт её six-plane palindrome и оплаченные native frames; A38/A41 дают отдельные G/CX plane/compiler components. Их корректная интеграция, inverse/padding и error/clock являются отдельной задачей, не новым действием или Info.

В частности, если выбрать шаг `σ=2^-80` и значения `σ(b_low+2b_high−3p²)`, все четыре исхода строго лежат внутри старого **асимметричного** B21 интервала `[−p²·2^-30,(1−p²)·2^-30]`. Это даёт прежние continuous chart slacks, но не позволяет переиспользовать бинарную SOURCE lookup таблицу с 2688 SAM bits: для явной карты нужны 5376 CODE bits и новый четырёхзначный каталог адресов/углов. От прежнего `g·2^-30>2^-3158` для нового шага следует только `gσ>2^-3208`; старый corner error `<2^-3231` тогда даёт лишь `<2^-23` после деления на `gσ`. Нельзя переносить старые finite-source price bounds без нового бюджета.

## 4. Полные DATA columns и настоящая граница private

Исходное требование §7ej.A-C относится к `A_ν(Y)=D_ν B(Y)` как полной operator map на SOURCE input columns, а не только к `B(Y)|born>`. Проверенные upstream результаты дают более широкую, но типизированную область:

| Компонент | Доказанный target/domain | Не следует автоматически |
|---|---|---|
| A22 Choi | Все `2^22` DATA columns, включая padding и любую внешнюю entanglement, при **24 source-private**, начатых в объявленном RAW и идеальным первым шагом переведённых в 0; цель `O_Ω(G†)^⊗22`. | Равномерная точность на произвольных dirty private columns или промежуточная карта внутри незакрытого macro. |
| A24 CAR | Все `2^19` DATA+fresh-RIGHT columns при трёх predicate-private RAW→0; target `M(ψ)P_vac`, а `M` действует тождественно на fresh RIGHT. | Сброс неизвестного oldRIGHT или произвольные dirty predicate inputs. P_vac может нетривиально действовать на fresh RIGHT. |
| B45 SITE | Все 256 SITE columns с произвольными aux/port/Spin и внешней reference; отдельный clean scratch не нужен. | Сам по себе physical H.1 admission или совпадение цен разных histories. |
| A17 `D_ν` | Реальный finite retained logical processor и его закрытые prefixes, со своими all-column macro errors и настоящими READY/failure. Field-independent D не увеличивает нормы SOURCE derivatives. | Равенство любого другого owner `D_ν`, неописанный intermediate mark или полная H.1 alpha. |

Поскольку SOURCE copies и их private непересекаются, гибридная композиция A22/A24 с B45 сравнивает на **всех SOURCE DATA и SITE входных колонках**: actual prefix с выбранным идеальным произведением при объявленном canonical состоянии каждого source-private; SAM, DATA между собой, old и reference могут быть когерентно запутаны. Следующая идеальная source preparation не трогает ещё не использованный private, а предыдущая физическая ошибка учитывается телескопически. Для A46 восьми bank'ов применим тот же суммарный prefix budget `<2^-3232` и all-column G/CX replacement на данном fibre. Это усиление над проверкой одного born DATA state; оно не разрешает произвольные private inputs и не строит все потребные marked frontiers.

Особенно важно: A23 vacuum/Fourier `P_vac` — полное явно выбранное unitary-продолжение, и A24 контролирует **все 2^19 columns именно к этому продолжению**. A23 прямо не доказывает, что оно совпадает на всех колонках, исходных marks и оплаченной истории с иным ранее не предъявленным original vacuum-prefix. Для универсального owner `B(Y)` нужно либо доказать это равенство/разрешённый marked transport, либо использовать реально зарегистрированный descriptor с A23 extension. Равенство только исходного vacuum state недостаточно. Никакого нового terminal `WJ` требования здесь не добавляется.

## 5. Явный smooth target budget и оставшийся native gate

На фиксированном B21 continuous cube для выбранного полного `B̃(Y)` из A22/A24/B45 (на описанном all-DATA/private-canonical fibre) рационально проверены следующие достаточные оценки. `||U0||<17/16`, `||Θ||≤6s`, `||DΘ[h]||≤sqrt(6)||h||`; Duhamel даёт `||DU[h]||<3||h||`, `||D²U[h,k]||<7||h||||k||`. Exterior powers до степени 4 и factor 1/2 дают `C1<8,C2<80`.

Julia defect `I−CCᵀ,I−CᵀC>1/16` и уравнение Сильвестра дают `J1≤5C1`, `J2≤5C2+68C1²`. С учётом Frobenius blocks и нормировки `1/sqrt(32·2049)` получаем для одного Choi `Ω1<1, Ω2<112`, затем для полного `O_Ω`: `O1<3,O2<338`. Для CAR `L>1/3`, `||ψ||²<1/15` дают `m1<11/10,m2<21/10` и `O_m` bounds `<4,<12`.

В восьми SOURCE banks поле меняет 540 Choi и 32 CAR copies; остальные references, SITE и RAW frames в этом chart фиксированы. Произведение полных unitary targets удовлетворяет

    M1 ≤540·3+32·4 =1748 <2^11,
    M2 ≤1748²−(540·3²+32·4²)+540·338+32·12
       =3233036 <2^22.

Это именно operator bounds по полным DATA columns выбранной source extension; fixed processor D_ν и unitary frame их не увеличивают. При `σ=2^-80`, `R_v<104`, `||X||<1` они дают ideal MG6 full-vector axis remainder `<2^-44`. В отличие от B65 scalar Hessian эти bounds относятся к оператору B̃. Они не сертифицируют новую таблицу углов/слов: uniform values на бинарных вершинах не образуют smooth native compiler, а target comparison и control finite errors, делённые на настоящий σ и gain, нужно проверять заново.

`check_full_vector_jet.py` точно проверяет one-bit algebra, MG2 в Q(√p), настоящий fresh source/address и factor K, rational derivative constants и асимметричный chart/gain. SOURCE amplitude argument — аналитическое произведение исходных target formulas; гигантские matrices не развёрнуты. Независимая проверка конкретного нового G/CX control module выполняется отдельно; новый SOURCE catalogue, обязательные D_ν/old-cut maps, полный four-slot task, Cost−Info и refinement остаются открытыми. `GR_closed=false`.
