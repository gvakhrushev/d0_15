# Полный опыт → Ward → метрическое уравнение: точное согласование и незаменимые условия вывода

16 октября 2026. `gvakhrushev/d0_15`, существующий Draft #334.
Исходный SOURCE: `d105e22ea91649047e48bb2587552e84f4547a41`.
Дополнительно потреблён `c33b2e65650533dac0d4f42b7c74d4ce72932886`.

**Результат:** доказано точное конечное координатное согласование ТОГО ЖЕ полного proper-path опыта, со всем coframe, наблюдателем, подготовкой, reference и путями; его полный первый/второй Ward; условный перенос этих тождеств при истинном устранении сохраняемых полей; конечный количественный селектор двухпроизводного метрического оператора. Это не новый action, динамика часов или отмена старого положительного causal source. Полная физическая селекция, устранение реального прибора, locality и Einstein/refinement теорема не доказаны.

## 0. Не повторять и не усиливать входы

Потреблены при исходном SHA:

- `A4D_FINITE_CAUSAL_RESPONSE_AND_CLOSURE_TEST.md`: положительный h^-2 второй отклик на longitudinal cone при фиксированном положительном приборе. Он исключает заявленное pure-EH+same-R тождество; не объявляет весь опыт калибровочно эквивалентным.
- `A4D_RAW_LINK_COTANGENT_JET.md`: настоящие пути и полные endpoint derivatives; source-coordinate inverse 1/12, не обратимость на всех grid frequencies.
- `A4D_NATIVE_CAUSAL_METRIC_SOURCE_BRIDGE.md`: factorization через G,T,measure и ту же form matter; отдельные Lorentz-cone directions.
- `sources/d0_native_action_selection_2026-10-16/RESULT_RU.md`: log полного нормированного record partition равен нулю; v8 H+J — другой signed survival/blank contrast. Ковариантность не выбирает этот контраст и его 1/j cycle semantics.
- `A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md`: только математические thermal/precision variables исключаются однозначно; они НЕ являются всем физическим наблюдателем/архивом.

Свежий owner при c33b2e65: `A4D_CONE_FULL_SHELL_FIRST_JET_NO_GO.md`. Его As=P{D0,D1}P на theta=y имеет несколько несовместимых spectral sectors. Никакое внутреннее понижение ранга в (P_Omega/8) tensor sigma не исправляет всю первую shell-строку при неизменённых field/link jets. Ниже этот результат сохраняется и отделяется от координатной свободы.

## 1. Полное семплирование — не только метрика в фиксированных координатах

Пусть L_h — тот же конечный набор labels, направленных рёбер и исходов. h, число record rounds, reference/workspace dimensions и code multiplicities остаются прежними. Рассмотрим существующее геометрическое представление labels посредством локального невырожденного отображения X: label chart → M. Это bookkeeping одного опыта, не новый постулат о физическом поле X.

Данные Phi=(e,n,Omega,C,mu,...) включают coframe 1-form, internal observer, Lorentz connection 1-form, ВСЕ16 raw exterior matter components и все reference columns, настоящую меру и прочие записанные поля. В labels используются:

    e_L=X*e,  n_L=n o X,  Omega_L=X*Omega,
    C_L=C o X (для internal компонентов), mu_L=X*mu.       (1)

Для coordinate differential forms C_L — соответствующий full exterior pullback, а не scalar substitution. Переход между этими двумя описаниями уже задаётся U_e=Lambda(e^T eta).

Ребро label-path gamma переносится по ПОЛНОМУ пути X o gamma. Его proper link — решение прежнего connection ODE вдоль этого пути. Не заменять путь прямой хордой после нелинейной замены координат.

Пусть f — любая допустимая smooth diffeomorphism, согласованная с границами. Изменим представление:

    Phi' = f*Phi,             X'=f^-1 o X.                   (2)

Тогда `(X')*(f*Phi)=X*Phi` ТОЧНО. Для связи совпадают коэффициенты ODE в каждой точке пути, поэтому совпадают ordered proper links, даже если они не коммутируют. Совпадают также inverse coframes, creator coefficients, Gram matrices и shifted true adjoints. Следовательно на том же полном конечном carrier

    D_h[Phi',X']=D_h[Phi,X],    rho_h[Phi',X']=rho_h[Phi,X]. (3)

При дополнительной внутренней смене frame равенство заменяется существующим полным isometric intertwining; в фиксированном whitened описании это unitary conjugacy. Ни один reference mode или outcome не выкинут.

Любая уже выбранная функция этих данных, в частности прежняя

    S_h=Tr(rho_m Delta_h)+log(C_h Tr K_h)/beta
                    -M Tr log((1-z)I+zK_h),                  (4)

сохраняется ТОЧНО при (2). Её event probabilities, numerator/normalizer и все конечные композиции этих же array-операций и чтений сохраняются той же подстановкой. Field-dependent calibration, если она действительно является функцией тех же transported данных, тоже переносится; произвольное coordinate-dependent правило может нарушить (3) и должно иметь свой отдельно записанный источник. Число раундов m дискретно и здесь не дифференцируется.

**Область:** (3) — coordinate naturality уже имеющегося geometric realization. Не доказано, что X есть независимо исполняемая native переменная, что engine разрешает физически передвигать detector, или что это равенство выбирает Cost−Info. Формально параметризовать можно и негравитационную теорию. Это не доказательство background independence или ОТО из одного нового имени переменной.

## 2. Полный Ward при конечном h и корректная вторая производная

Для потока f_t с generator xi:

    dS_h[ L_xi Phi, -xi o X ]=0.                            (5)

В (5) содержатся все coframe/link/observer/preparation/measure вариации. Это конечное слабое тождество; оно не выводится дифференцированием лишь скалярной сходимости S_h и не отождествляет атомарные grid covectors с непрерывными плотностями.

Пусть R_xi(z) — полная скорость (2) на координатном C2-chart всех соответствующих данных. Тогда вдоль потока

    Hess S_h[R_xi,R_xi] + dS_h[(dR_xi)R_xi]=0.               (6)

Только в полной stationary point получаем из производной (5)

    Hess S_h R_xi=0.                                        (7)

Нельзя использовать (7) на arbitrary background с ненулевыми другими Euler rows. Даже для ровно инвариантной функции Hess по кривой вращения вне критической точки компенсируется её ускорением; это включено в exact control.

Если существуют continuum Euler densities с достаточной регулярностью, (5) даёт обычное Noether identity. Например для covariant metric g, scalar clocks Y=X^-1, scalar matter phi и one-form a:

    -2 nabla_mu E_g^mu_nu
      + E_A partial_nu Y^A + E_phi partial_nu phi
      + E_a^mu(nabla_nu a_mu-nabla_mu a_nu)
      - a_nu nabla_mu E_a^mu + остальные полные tensor rows =0. (8)

E определены по δS=∫dV_g[E_g^{mu nu}δg_mu nu+E_AδY^A+...]. Для прочих форм и independent connection «остальные» означает действительный adjoint соответствующей Lie-variation, не permission удалить их. Универсальная точная запись (5) сохраняет их полностью и не требует скаляризовать связь.

При выполнении всех остальных собственных equations (8) даёт metric Bianchi identity. При fixed unsolved detector/clock это заключение неверно. Проверка на scalar-gradient action даёт точное `-2 div E_g+E_Y dY=0`; без E_Y оно не выполняется. Пример иллюстрирует Ward, не добавляет scalar-clock action к D0.

## 3. Что на самом деле менялось в предыдущем longitudinal test

Возьмём именно прежний flat background и первую скорость:

    g0=s² eta, G0=s² I, a0=s dt, Y0=x,
    phi=cos Q(x1+x2),
    dot a=s phi(dx1+dx2),
    dot g=2(dot a a0^T+a0 dot a^T), dot G=0, dot Y=0.        (9)

При xi^0=2 sin Q(x1+x2)/Q, xi^i=0 имеем `dot g=L_xi g0`.
НО полное перетаскивание (2) требует

    L_xi a0=2s phi(dx1+dx2),
    L_xi G0 !=0,     L_xi Y0=xi.                           (10)

Следовательно `dot a-L_xi a0=-s phi(dx1+dx2)`, а clocks вообще не переносились. Это не скрытая gauge trajectory всего опыта.

Это различие можно зарегистрировать без выбора ненатуральной координатной компоненты. Введём физически относительный clock Gram

    B^{AB}=g^{mu nu}(partial_mu Y^A)(partial_nu Y^B).         (11)

При совместном pullback он меняется как scalar reading и имеет нулевую первую вариацию на постоянном B0. На прежней fixed-clock curve

    dot B^{01}=dot B^{02}=2phi/s² !=0.                      (12)

Поэтому прежний положительный `lim h^-2(H+J)''` остаётся реальным response ТОГО fixed-detector опыта. Его нельзя ни объявить чистой Einstein-частью, ни обнулить ссылкой на coordinate gauge. Нынешний результат не исправляет числа, signs или proof scope прежнего owner; он вычисляет отличия между двумя полными физическими вопросами.

Это также не вводит новый «observer stress» по формуле S−EH. Любое такое разложение требует отдельно определённого собственного retained price и его полного вариационного закона.

## 4. Свежая shell-несовместимость не устраняется сменой координат

Пусть `Delta_h=Delta0+h A1+o(h)` и P — настоящее eigenshell Delta0 с eigenvalue eps0. При любом гладком isometric изменении представления, записанном на фиксированном Hilbert space как `U_h=I+h K+o(h)`, K*=-K,

    A1' = A1 + [K,Delta0],
    P A1' P = P A1 P.                                    (13)

Следовательно спектр As и условие `(As-eps1 P)C0=0` инвариантны. Движение первого amplitude corrector включает K C0, но не меняет projected compatibility. Смена наблюдательного Gram, действительно переносящая тот же inner product, после whitening имеет ровно этот вид. Нефизическое similarity с забытым adjoint не разрешается.

При c33b2e65 уже доказано, что у fixed theta=y full shell нет собственного подпространства с поддержкой на всех четырёх осях. (13) означает: никакой coordinate repair не исправит это ограничение. Нужен настоящий first field/link source, дающий некоммутаторный вклад P deltaA1 P, либо другая реально допустимая preparation/shell. Теорема не разрешает выбирать этот вклад рукой для отмены As.

Таким образом новые Ward-тождества не являются обходом нового no-go. Они отделяют бессодержательное изменение записи от физического изменения совместной задачи.

## 5. Когда из полного источника действительно получается метрический

Пусть z теперь обозначает настоящие retained fields, а не fugacity в (4). Для избежания смешения ниже пишем r. Рассмотрим ТОТ ЖЕ full action S(g,r) на действительном совместном chart. Допустим доказано существование local smooth решения

    δ_r S(g,r_*(g))=0,
    r_*(f*g)=f*r_*(g)                                     (14)

с той же preparation/history и физическими граничными условиями. Тогда без введения нового слагаемого определена reduced price

    Gamma[g]=S(g,r_*(g)),
    dGamma=d_gS|_(r_*).                                  (15)

Она diffeomorphism covariant. Если B=S_gr и D=S_rr обратимы на честно определённом сохраняемом complement, то

    H_eff=S_gg-B D^-1 B*,                                (16)
    H_eff(L_xi g)=0                                      (17)

на полном стационарном фоне. Доказательство: full Ward даёт
`S_gg G+B R=0`, `B*G+D R=0`; исключение R даёт (17).

Это не подгонка B D^-1 B* к нужному source. Все блоки должны быть производными одного S. При сингулярном D сначала требуется

    P_ker(D) B* v=0.                                    (18)

Псевдообратная не отменяет (18), нулевые shell/reference блоки не обращаются, а физические rank-birth направления не считаются gauge по названию.

Условия (14) для полного D0-прибора НЕ доказаны нынешним результатом. Прежние единственные thermal/precision auxiliaries удовлетворяют своей математической max-задаче, но не заменяют observer, reference128 и исходную matter. Фиксированные clocks нельзя минимизировать как будто их уравнения уже были частью исходной программы.

### Количественный, пригодный для потребителя остаток

Если full Ward-block residuals на конкретной скорости равны

    r_g=S_gg G+B R,    r_r=B*G+D R,

то ТОЧНО

    H_eff G=r_g-B D^-1 r_r.                              (19)

Отсюда `||H_eff G||<=||r_g||+||B D^-1|| ||r_r||` в совместимых нормах. Полный raw h^-2 перенос требует явных norm conversions и uniform bounds; scalar smallness или fixed-cut inverse этого не дают. Никакой старый raw comparator (19) не подменяет.

## 6. Вынужденность формы Einstein после descent: конечные тождества, не каталог теорий

Теперь явно условный selector. Пусть после (14) и необходимого контролируемого предела leading metric response на flat vacuum:

1. локален, имеет ровно две производные;
2. Lorentz-equivariant, без независимого observer/clock/connection tensor в его коэффициентах;
3. является Hessian скалярного variational action;
4. удовлетворяет полному metric Ward/Bianchi.

Из invariant contractions общего symmetric h остаются пять tensor structures:

    E_mu nu = a Box h_mu nu
      + b(partial_mu partial^rho h_rho nu + partial_nu partial^rho h_rho mu)
      + c partial_mu partial_nu tr(h)
      + d eta_mu nu partial^rho partial^sigma h_rho sigma
      + e eta_mu nu Box tr(h).                            (20)

Здесь пять коэффициентов — конечный базис одного указанного representation class, не перебор физических действий. Selfadjointness полного packed pairing даёт c=d. Divergence identity даёт

    a+b=0, b+d=0, c+e=0.

Решение однозначно до масштаба:

    (a,b,c,d,e)=c0(1,-1,1,1,-1).                         (21)

Это linearized Einstein operator с convention-dependent общим множителем. Его все10 строк annihilate `h=L_xi eta`. Коэффициент c0, его знак и физические единицы этим не определены. Нулевой c0 допустим алгебраически; для gravity нужно независимо доказать c0!=0.

**Устойчивый вариант.** Обозначим R_5 матрицу четырёх перечисленных линейных условий, включая c-d. Для k=(1,-1,1,1,-1)

    I-R_5^T(R_5 R_5^T)^-1 R_5 = k k^T/5,
    ||R_5^T(R_5 R_5^T)^-1||_F²=4.                       (22)

Значит distance до Einstein-line не больше `2||R_5 coefficients||_2`. Это конкретный coefficient-error consumer, не ошибка полных Euler на произвольной сетке.

### Нелинейный конечный вывод при тех же дополнительных физических свойствах

Если reduced local action density естественна и зависит только от метрики, с total derivative order не выше2, то в normal coordinates единственная нетривиальная invariant contraction второго jet — scalar R; first derivatives исчезают в точке. Parity-odd contraction curvature с epsilon равна0 по algebraic Bianchi. С точностью до границы:

    Gamma_local = integral (lambda+c R_g) dV_g,
    δGamma_local = integral [(lambda/2)g^{mu nu}-c G^{mu nu}] δg_mu nu dV_g. (23)

При отдельно выведенном actual matter action его Euler сохраняется и даёт Einstein equation с соответствующими c,lambda. Это узкий вывод формы natural two-derivative action; более общая nonlinear uniqueness также известна в математике гравитации. Ни minimal tuple, ни отсутствие внешнего каталога сами по себе не установили locality/derivative-order hypotheses (20)/(23).

Контроль: `(Box eta_mu nu-partial_mu partial_nu)(Box tr h-partial partial h)` divergence-free и variational, но имеет четыре производные. При retained vector/clock tensors существуют другие двухпроизводные структуры. При fixed positive beta спектральная цена может быть nonlocal, что уже видно на собственном flat-modulus control. Эти возможности не исключаются одним Ward и не удаляются новым именем «reduced».

## 7. Что эта сборка меняет в работе на закрытие

Теперь раздельные требования сведены к одной проверяемой композиции:

    полные native данные и их transported representation
    → exact finite Ward
    → actual retained equations и их допустимое исключение/независимое чтение
    → local metric-only response с необходимым контролем порядка
    → Einstein operator и nonlinear EH form.

Первое тождество и условные импликации следующих стрелок здесь доказаны. Сам actual physical selector и две средние физические предпосылки не заполнены: не предъявлены ни r_*(g) для полного declared detector, ни доказанный local two-derivative предел с ненулевым c. Новый output не обещает, что несколько успешных finite checks автоматически их дадут.

Практический consumer #334: при формировании next mixed field/link/preparation corrections использовать все rows, полный true-adjoint path source и invariance (13), затем проверять (19), а не объявлять metric block единственной Hessian. Для action-selector требуется actual native ensemble law из последнего RESULT_RU: изменение координат не выбирает survival/blank signs, `1/j`, uniform heat preparation или clock law. Не вводить r-penalty, операторную subtraction или EH-counterterm ради принуждения (21).

Это не смена конечной цели. Это способ перестать выдавать nonzero response fixed detector за автоматически неправильную гравитацию или, наоборот, за готовый Einstein-source. Старый положительный h² контраст остаётся; теперь точно известно, где он расположен в полном пространстве вариаций и какие уравнения нужны для его физического разделения.

## 8. Проверка и внешняя математика

Соседний `check_relational_ward.py` содержит exact SymPy controls: нелинейный coordinate shear с opposite embedding; изменяющиеся coframe/observer/measure; noncommuting path-generator pullback и первые/вторые jets; полный16 CAR operator fixture; actual reference columns без выбора одной колонки; old cone clock strain; full/partial Hessian distinction и singular-block counterexample; Noether с настоящим scalar clock Euler; exact invariant five-coefficient selector; projected shell spectrum. Общие теоремы не выводятся из числа контролей.

Основные результаты являются конкретным применением известных naturality/Noether/Schur идей, а не заявлением, что этот общий аппарат впервые найден D0. Первичные внешние источники: Iyer–Wald, arXiv:gr-qc/9403028 (Noether identities diffeomorphism-invariant theories); Varadarajan, Phys.Rev.D75,044018 (2007), DOI10.1103/PhysRevD.75.044018 (параметризация теории сама по себе не делает её GR). Они не вносят физические аксиомы в D0. Условный two-derivative вывод (20)–(23) дан непосредственно выше.

Новых Lean declarations, независимой научной приёмки, существования curved joint roots, физической генерации полей часов и full GR closure здесь нет. Старые proofs/receipts/claims не изменяются.
