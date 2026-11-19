# Cost−Info: действие истории, полный открытый вакуум и determinant-срез

17 октября 2026. Продолжение существующего Draft #334, без новой задачи.
Научный вход: `d1b76082948d5b59961b7068e1ba2c70187efb7f`.

## 0. Результат и граница

Собраны существующие code/gain/normalizer результаты на одном настоящем процессе. Получены: (1) точная нулевая вакуумная секция ПОЛНОЙ ожидаемой Cost−Info открытого Julia128 дерева при его same-history likelihood binding; (2) её действительная амплитудная сингулярность t² log(1/t²); (3) строгий finite same-program source discriminator с полным H+J+R; (4) положительная каноническая коллективная реализация исходного determinant как вероятности и Cost−Info конкретной макроветви.

Это не полное D0→GR. Коллективная top-exterior подготовка и исполнение её подъёма не объявляются уже физически допущенными literal-v8; это явно описанный другой тест заданных U,P. Его дополнительные ресурсы не бесплатны. Скалярный counter-sector не объявляется M1-допущенным физическим миром. Не выбирается новая Info, не изменяются claims и original fixed-g/tau/raw-h^-2/#216.

Содержательная поправка синтеза: действие отдельной истории, среднее её действия и действие суммарного класса историй — разные функционалы. Их нельзя переносить между участками доказательства только по названию Cost−Info.

## 1. Потреблённые владельцы

Относительно корня на входном SHA:

- BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md в 01_BOOKS, §§03.3.0–03.3.2, 03.8, 03.10: S(gamma)=Cost−Info, w=phi^(−S), algebra-valued сумма с голономией до Born и отдельный feedback-компонент.
- 02_REGISTRY/research/A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md: логарифмический gain при том же w=q.
- A4D_NATIVE_PARTITION_CORRECTED_BRANCH_INFORMATION.md: настоящий raw-normalizer source.
- A4D_RETAINED_HISTORY_READOUT_AND_NORMALIZER.md: local gain-sum, полное Julia128 дерево и иной return cut.
- A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md: отмена кода до вариации, полная pointer-цена.
- A4D_NATIVE_OPERATIONAL_GAIN_AND_MEMORY.md и A4D_NATIVE_FEASIBLE_GAIN_AND_ACTION_SOURCE.md: complete и feasible gain не взаимозаменяемы.
- A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md: все128 исходов и их операторные карты.
- sources/d0_complete_record_channel_2026-10-17/check_flat_relaxation.py: буквальный `_native_rows`, blob 1b3ab5605d323364ec83dac110f294b0edd37996. Старый checker не исполняется.
- sources/d0_spatial_tensor_vacuum_2026-10-17/RESULT_RU.md: уже доказанный scalar D-vacuum.
- A4D_AF_FULL_SOURCE_EINSTEIN_NORMAL_FORM_2026_10_17.md: полный graph-source, который не исчезает от смены переменных.

Стандартный внешний контекст determinant-реализации: I. Klich, Full Counting Statistics: An elementary derivation of Levitov's formula, arXiv:cond-mat/0209642. Для measured relative entropy: Berta–Fawzi–Tomamichel, arXiv:1512.02615. Общая фермионная determinant-математика не заявляется изобретением D0. Нужное конечное доказательство дано ниже, без импорта физического допуска.

## 2. Формула, которую действительно уже фиксирует Cost−Info

На одном конечном срезе пусть w>0, N=sum w, q=w/N, mu=phi^(−C), ell=log(phi). Book-равенства w=phi^(−S), S=C−I дают

    I_omega=[log(q_omega/mu_omega)+log N]/ell,
    S_omega=[−log q_omega−log N]/ell,
    Sbar=[H(q)−log N]/ell,
    dSbar=[−sum dq_omega log q_omega−dlog N]/ell.       (1)

Это потребление существующих теорем, не новая Info. Любой синтаксический code и все его jets сокращаются ДО вариации, если Cost и gain действительно относятся к нему. Иной физический расход не объявляется включённым в (1) по одному названию.

Полное trace-preserving дерево имеет

    sum_child K_(omega child)*K_(omega child)=K_omega*K_omega.

При явном binding w=Tr(rho K_omega*K_omega) полный конечный prefix-free cut имеет N≡1. Поэтому Sbar=H(q)/ell. Бесконечные stopping cuts здесь не используются.

Но на действительном событии E с единственной условной макрометкой q_E=1 и raw mass N_E=Pr(E):

    S_E=−log Pr(E)/ell.                                (2)

Его комплемент сохраняется в опыте. Средняя цена полного бинарного теста — h(Pr E)/ell, НЕ (2). Их derivatives соответственно −dPr(E)/(ell Pr(E)) и log[(1−Pr(E))/Pr(E)]dPr(E)/ell.

Для положительной scalar группировки классов pi:Omega→X также

    W_x=sum_(omega in x) w_omega,
    S_eff(x)=−log W_x/ell,
    dS_eff=E[dS|x],
    d²S_eff=E[d²S|x]−ell Cov(dS,dS|x),
    E[S|x]=S_eff(x)+H(omega|x)/ell.                     (3)

Это конечный chain rule. Book-сумму амплитуд с голономией нельзя заменить scalar grouping без настоящего положительного readout.

Если настоящий operator cost равен −Tr sigma log mu/ell, то C−I_feasible=[S_vN(sigma)+D(sigma||mu)−D_feasible(sigma||mu)]/ell. Последний deficit не свободен; он определяется допустимыми тестами. Он не зануляется информационной полнотой. Этот альтернативный контракт не подставляется вместо (1).

## 3. Полная открытая Cost−Info: точное семейство всех первых нулей

На исходном finite graded exterior-difference носителе, где возвраты сохраняют скаляры, постоянная нормированная scalar section o удовлетворяет

    d_h o=0, d_h^dagger o=0, D_h o=0.                  (4)

Первое — возврат постоянной функции, второе — degree-lowering adjoint с настоящей block-graded pairing. При движении положительной меры меняется общий нормирующий множитель, а (4) сохраняется. Весь reference128 может быть тензорно сохранён.

У фактического round A=hD/16, W=Q*(I−2P_blank)Q, N_k=Q_(blank,k) и

    W_(k,0)=delta_(k,0)I−2N_k* A,
    K_(0,k)=p delta_(k,0)I+p²W_(k,0),
    K_(1,k)=sqrt(p)p(W_(k,0)−delta_(k,0)I).             (5)

Отсюда K_(0,blank)o=o, а все остальные127 Kraus maps уничтожают o. После любого конечного числа fresh-record rounds имеется один определённый полный word omega0; ничего не reset и не стёрто. При открытом likelihood binding (1):

    q=delta_omega0, N=1, Sbar_open=0.                  (6)

Это верно для любого полного положительного кода данного дерева. Cost успешной истории может быть ненулевой; в этом именно net-контракте она совпадает с gain.

**Теорема.** Если (4) действительно входит в разрешённый вариационный носитель данного опыта, все его конфигурации являются глобальными минимумами неотрицательной Sbar_open. Все coframe/link/observer/preparation first sources равны0. При разрешённой vacuum optimization подготовки inf_rho Sbar_open(g,rho)=0 для каждой геометрии этого класса.

Доказательство первых derivatives не использует log(0): на finite smooth amplitude chart каждый новый исход имеет вероятность O(||delta||²), поэтому −qlog q=O(||delta||²|log||delta|||). Полный первый derivative равен0, включая rank birth. Вариации исходного data/operator носителя не ограничиваются волновым ansatz.

Это завершённая граница данной кандидатной цены: она не выбирает vacuum Einstein equations. Это НЕ общий D0 no-go, потому что физическое admission scalar section и выбор всего self-verification programme этим не установлены.

Coherent tape на этой секции тоже фиксирован в pure blank; это не утверждение о другом AF/GNS algebra readout. Return-to-the-same-scalar event имеет N_ret=1, но иной reference/return ensemble может иметь другой N.

## 4. Настоящая регулярность вакуума — C1, не C2

Пусть psi0 — (4), а psi1 — нормированная positive-energy eigenstate Delta с lambda>0. Для psi(t)=sqrt(1−t²)psi0+t psi1 и настоящего B=I−epsilon Delta/2 после n rounds:

    q_omega0=1−a_n t²,
    q_omega=t² r_omega для omega != omega0,
    a_n=sum r_omega=1−(1−epsilon lambda/2)^(2n)>0.

Nonblank cross terms отсутствуют из (5); blank cross term нулевой из selfadjointness B и ортогональности psi0,psi1. Поэтому

    H(q_t)=−(1−a_n t²)log(1−a_n t²)
              −a_n t²log(t²)−t²sum r_omega log r_omega,
    Sbar_open(t)=a_n t²log(1/t²)/ell+O(t²).             (7)

Первая производная в0 равна0, вторая стремится к +infinity. Коэффициент — реальная полная first-exit вероятность того же процесса. Нельзя применять гладкую Hessian/Schur-программу к этой вакуумной точке полной ожидаемой цены. Faithful/rank-fixed ветви этим не исключены.

## 5. Строгий полный finite source discriminator

На literal Julia128 L=2 Fourier carrier берём существующую калибровочную формулу

    h=1/2, nu=3/5, sqrt(1−nu²)=4/5,
    alpha=p²/512, n=512, beta=2n alpha=2p²,
    z=2^-20, M=128, m=2n=1024.

Это диагностический слой programme family, не новый physical root или исходный fixed-g comparator. Все16 momenta и16 формы дают

    lambda_r=16nu²r,
    mult_r=16 binomial(4,r), sum mult=256,
    B_r=1−alpha lambda_r,
    Z=sum mult_r B_r^m.

У полной объявленной цены S_v8=log(CZ)/beta−M sum mult log(1−z+zB_r^m)+R сохраняется весь field-independent workspace/reference factor C. На scalar preparation R=0. Поэтому

    dS_v8/dnu=sum mult_r B_r^(m−1)lambda'_r
                 [−1/Z+M beta z/(1−z+zB_r^m)].          (8)

beta<1,Z≤256, а M beta z Z/(1−z)<32768/1048575<1. Каждое ненулевое слагаемое (8) отрицательно, поскольку lambda'_r=32nu r>0 при r>0. Следовательно dS_v8/dnu<0, тогда как dSbar_open/dnu=0 ТОЧНО.

Десятичная диагностика: dS_v8/dnu=−0.92460344604377850711877221029620660776646968749... . Знак доказан рациональной границей, не floating-point оценкой. Для первой положительной моды (7) a_n=1−(1−9p²/800)^1024=0.98784153706284287814302944650416... .

Checker восстанавливает literal ACDB CAR и все64 Julia/Walsh rows для каждого из16 momentum, затем оба порта. Это не другая двууровневая модель и не сверка одного trace. Прежние owners не перезапускаются. Никакое перекодирование внутри (1) не превращает нулевой source в (8).

## 6. Положительное соединение: исходный determinant есть вероятность

Для любого уже заданного U,P,Q=I−P и fixed 0<z<1, V=range P, d=dim V, i:V→H положим

    M0=(P+sqrt(1−z)Q)Ui,
    M1=sqrt(z)QUi.

Это полная isometry: M0*M0+M1*M1=I. Без sqrt(F) либо eigenvector oracle

    F=i*U*QUi, M0*M0=I−zF.                             (9)

Возьмём каноническую заполненную линию Lambda^d V. Её normalized Slater density не зависит от unitary базиса: вектор v1 wedge ... wedge vd меняется только фазой det R. Поднимем ВСЮ isometry в Lambda^d(H tensor C²_flag). Тогда событие E0 «ни одного flag1» имеет

    Pr(E0)=||Lambda^d M0 Omega_V||²
          =det(M0*M0)=det(I−zF).                      (10)

Это Gram determinant/Cauchy–Binet. Полная exterior-isometry имеет norm1; остальные сектора с любым числом flags1 сохраняются и имеют суммарную вероятность1−Pr(E0). Нулевые внешние eigenvalues F дают unit determinant factors; обычные регулярные multiplicities не заменяются normalized trace.

**Ресурсы:** нужны d occupied test modes/particles и induced many-body operation. Это не клон неизвестной psi и не автоматически исходные four-role CAR modes. Способность бесплатно реализовать этот растущий Fock-носитель или разместить его на reference128 не утверждается. Construction задаёт математический прибор и его размер, а не завершённое physical-native admission.

В классе all-mode survival тестов determinant вынужден single-mode правилом N_z(f)=1−zf, unitary covariance и multiplicativity при независимом ортогональном direct sum. Diagonalization только в доказательстве даёт product_i(1−zf_i). Из одной M1 эти три operational requirements здесь не выводятся; invariant scalar функции вне данного тестового класса не классифицируются.

## 7. Точная Cost−Info макроветви и все её derivatives

На реальном событии (10), для заданного его кода mu_E, исходное likelihood правило даёт

    C_E=−log mu_E/ell,
    I_E=log(Pr(E0)/mu_E)/ell,
    S_E=C_E−I_E=−log Pr(E0)/ell=J/ell.                 (11)

На одноисходном условном macro cut это также (1) с q_E=1,N_E=Pr(E0). Комплемент остаётся в полном опыте. Нормализованность полного опыта не позволяет выбросить dlog N_E. Но (11) — не h(Pr E0)/ell, средняя цена обоих исходов.

При произвольных smooth U,P,z и постоянном rank P получаем без commutativity предпосылки

    ell dS_E=Tr[(I−zF)^−1(z dF+F dz)].                 (12)

dF содержит все настоящие dU,dP. Общая frame-смена переносит весь cut и даёт trace-zero commutator; физическое движение cut не замораживается. При нелинейном поле в Hessian остаётся d²F.

При fixed z исходное closed-loop выражение теперь одновременно есть expansion реальной вероятности:

    J=sum_(k≥1)z^k Tr(F^k)/k.

Для M-term truncation истинный source-tail равен Tr[z^(M+1)F^M(I−zF)^−1 dF]. Пространственный raw-h^-2 предел из одной этой формулы не следует.

Получено математическое соответствие feedback-компонента Book-действию конкретной macrohistory, а не новая энтропия. Чтобы объявить его всей физической ценой, требуется совпадение native history/cut/programme; H,R, clock, preparation и graph-source других полей не исчезли.

## 8. Потребитель завершения

Cost−Info не «неизвестная функция»: после SAME history/readout binding формулы (1)–(3) и (6) полностью задают соответствующие источники. Не доказан другой, конкретный переход:

    Book Gamma_D и coherent algebra-valued histories
      -> фактически исполненная native программа и retained cut
      -> её raw weights/N и полный совместный source.

Простое w=q_open плюс объявление полной цены H+J+R не проходит точную проверку (8). Коллективный determinant event (9)–(12) даёт положительную реализацию одного требуемого среза, но не его бесплатный physical admission и не универсальную динамику. Нельзя считать mean entropy, branch surprisal и coarse-history action взаимозаменяемыми.

Непустое full physical refinement, независимый материальный source и ненулевой полный Lorentz Einstein coefficient не доказаны этим пакетом. Ранее найденные локальные AF-star решения сохраняются со своим исходным scope. Новые main claims или завершение ОТО не объявляются.

## 9. Проверка

Самостоятельный check_cost_info.py: 151 выполненная точная проверка; нормальный Python3.13.5/SymPy1.14.0 и python -O дают одинаковый JSON. Native row arithmetic использует целые числители/знаменатель160 и точное p²+p−1 сокращение; decimal quantities отдельно обозначены диагностикой. Все проверки — через explicit exceptions. All-size proofs находятся выше, а не выводятся из fixture counts. Старые research/root/Lean suites, repository-wide validators и full CI не запускались.
