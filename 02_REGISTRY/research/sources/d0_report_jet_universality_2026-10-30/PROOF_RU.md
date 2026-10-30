# Не один фиксированный отчёт: общий первый отклик, зависимый масштаб и полный κ-источник

30 октября 2026. `gvakhrushev/d0_15`, существующий Draft PR #334.
Закреплённый вход: `83bf7da04a3d2558edc2fa412dbc43f19c9653cc`.

## 0. Какое требование снимается

Текущий κ-capstone требует фиксированный закон full-CAR/ten-sign/READY-and-REPORT
на всём регулярном полевом пространстве; дополнительные реализации допускаются
в faithful fibre этого же полного закона. Здесь доказано достаточное расширение:
**весь закон отчёта может меняться, включая независимые управляющие параметры,
если его базовое значение и относительный линейный отклик сохраняются, а
реальные смешанные производные высших членов равномерно контролируются.**
Положительный общий масштаб линейного отклика также не требуется фиксировать:
он поглощается обратимой картой coframe с сохранением его собственной строки.

Это source-универсальность явно указанного класса, а не утверждение, будто
замкнутость автоматически помещает все программы D0 в этот класс. Не изменяются
исходная Book03-цена, старое начальное состояние, смысл текущего gain или
материальный коэффициент λ. Действительно свободные изменения baseline или
отношения двух ведущих коэффициентов имеют ненулевые источники и сохраняются.
`unrestricted_D0_GR_closed=false`.

Метод Taylor/field-redefinition и вычисление вероятностных полиномов через
Bernstein-коэффициенты стандартны. Здесь они применены к ОДНОМ ранее доказанному
полному D0-source, включая независимые новые shape-параметры и старое матричное
прошлое. Никакой универсальной новой теоремы о renormalization/QFT не заявляется.

## 1. Потреблённые тождества и настоящий критерий изменения

Все следующие пути лежат в `02_REGISTRY/research/` на закреплённом SHA:

- `sources/d0_retained_response_concentration_2026-10-28/SOURCE_PROOF_RU.md`,
  §§1–3: прежний полином r, реальные PF-веса, один полный determinant;
- там же `GENERAL_EINSTEIN_SOURCE_RU.md`, §§1–2: обратимая материальная карта
  и ТОЧНАЯ anchored степень -2 обоих конечных moment-operands по e_x;
- там же `KAPPA_CLOSURE_RU.md`, §2: прежний exact task graph и faithful fibre;
- там же `RAW_CYLINDER_REALIZATION_RU.md`, `FULLSTEP_COMPILATION_RU.md`,
  `GROWING_CLOCK_RU.md`: реальные raw births/полные слова и тепловые бюджеты;
- `A4D_FINAL_REGULAR_SOURCE_COMPOSITION_REVIEW_2026_10_29.md`: corrected
  dense fixed-test lifts, а не сюръективность конечной сетки на всё C3;
- `A4D_INITIAL_DATA_ENERGY_TO_KAPPA_CLOSURE_2026_10_30.md`: остаётся прежним
  высокорегулярным Cauchy-потребителем; его проверки здесь не повторяются.

Входящий источник использует

    bar r_h = sum_x v_x rho_x r(eps_h f_x/rho_x,-eps_h q_x/rho_x),
    sum_x v_x rho_x=1,
    r0=r(0), rf=r_x(0)>0, rq=r_y(0)>0, lambda=-rq/rf,
    I_h=sum_x v_x(f_x+lambda q_x).

Настоящие f_x,q_x — старые moment-density operands, не положительные norm
surrogates и не остатки Einstein-уравнений. Мера и нормированная PF-плотность
не отождествляются. epsilon_h и вся регулярная область выбираются до решения.

## 2. Теорема полного совместного Taylor-источника

Пусть theta_x — действительно рассматриваемые параметры формы отчёта,
а sigma_x>0 — общий масштаб его ведущего отклика. Они могут меняться независимо
по местам и копиям. На одном общем compact chart даны положительные bounds
rho_min,sigma_min и верхние field/parameter/source bounds.

Заменим r на семейство r_theta(u), u in R2, со свойствами

    r_theta(0)=r0,
    D_u r_theta(0)=(rf,rq),                              (1)
    ||D_u² r_theta||<=H,
    ||D_theta D_u² r_theta||<=H_theta.                   (2)

Нормы (2) — действительные bilinear/parameter operator norms на той же
области, а не вывод из близости значений. Семейство C2 по u и C1 по theta
с этими смешанными производными. theta может иметь любую конечную размерность;
число параметров входит через её объявленную норму. Требуются настоящие bounds,
а не uniformity, объявленная по названию. Ни Einstein=0, ни геометрическая
кривизна решения не входят в (1)–(2).

Положим w_x=(f_x,-q_x), a_x=sigma_x w_x и

    bar r_h = sum_x v_x rho_x r_(theta_x)(eps_h a_x/rho_x),
    I_h^sigma=sum_x v_x sigma_x(f_x+lambda q_x).          (3)

Для совместной вариации поля, sigma,rho,theta, с sum v dotrho=0:

    |D bar r_h - eps_h rf D I_h^sigma|
    <=eps_h² sum_x (v_x/rho_x) [
       H |a_x| |D a_x|
       +(H/2)|a_x|² |D rho_x|/rho_x
       +(H_theta/2)|a_x|² ||D theta_x|| ].               (4)

Ни одна новая shape-строка в(4) не отброшена.

**Доказательство.** Определим R_theta(u)=r_theta(u)-r0-(rf,rq).u.
Из (1)–(2) и интегральной формы Taylor:

    |D_u R_theta(u)|<=H|u|,
    |R_theta(u)-D_uR_theta(u).u|<=H|u|²/2,
    ||D_theta R_theta(u)||<=H_theta |u|²/2.

Последнее использует D_theta r_theta(0)=D_theta D_u r_theta(0)=0.
Дифференцирование rho r_theta(eps a/rho) даёт три remainder terms:

    eps D_uR_theta(u).D a
    +(R_theta-D_uR_theta.u)D rho
    +rho D_thetaR_theta(u).D theta.

Постоянная r0 сокращается по нормировке PF; линейная часть даёт именно
 eps rf D I_h^sigma. Подстановка u=eps a/rho доказывает(4). QED.

В фиксированной реальной совместной норме и при равномерных bounds:

    ||D bar r_h/(eps_h rf)-D I_h^sigma|| <= C eps_h.      (5)

C включает 1/rf и все настоящие карты field->moment. Он не назначается
равным1 и не считается uniform для необоснованных raw-осцилляций.

При конечных native comparisons (4) интегрируется вдоль объявленного target
comparison; погрешность действительно скомпилированных концов добавляется
с прежним делением на |t|Gamma. Производная дискретного компилятора не нужна.

### Допустимое ослабление точной калибровки

Если на уровне h вместо(1) имеются e0_h(theta) в baseline и линейная
ошибка e1_h(theta), то в полном source дополнительно остаются

    O(||D_theta e0_h||/(eps_h rf))
    +O((||e1_h||+||D_theta e1_h||)/rf),                   (6)

с настоящими полевыми/PF bound-факторами. Поэтому достаточно соответствующих
исчезающих budget, но малой ошибки только значения недостаточно.
Field-independent baseline, одинаковый для всех theta в данной comparison,
не создаёт собственного derivative; его абсолютная цена не вычитается.
При site-dependent baseline реальные PF-строки также надо добавить.

## 3. Масштаб первого отклика является зависимым, а не новым уравнением

Это применение уже доказанной anchored homogeneity, а не предположение о
scale invariance полного Book03-действия. На каждом конечном x:

    f_x(t e_x,U)=t^-2 f_x(e_x,U),
    q_x(t e_x,Psi)=t^-2 q_x(e_x,Psi).

При положительном sigma определим

    e_tilde,x=e_x/sqrt(sigma_x),
    omega_tilde=omega, Psi_tilde=Psi.                    (7)

Тогда ТОЧНО, до smooth limit:

    I_h^sigma(e,omega,Psi)=I_h(e_tilde,omega,Psi).         (8)

Более того аргументы отчёта в(3) равны исходным аргументам, вычисленным на
 e_tilde, поэтому для фиксированного theta и заданного target map изменение
sigma является такой же конечной репараметризацией всего reporter, не только
линейной цены. Если дополнительные physical costs зависят отдельно от sigma,
они этим равенством не покрываются.

Полный differential map:

    delta e_tilde=sigma^-1/2
                    [delta e-(e/(2sigma))delta sigma].   (9)

Он имеет bounded правый lift delta e=sqrt(sigma)delta e_tilde, delta sigma=0
на каждом объявленном положительном регулярном collar. При требовании C3
норм сохраняются реальные C3 bounds sigma и её обратного корня.
Полный ведущий covector удовлетворяет тождеству

    2sigma E_sigma+<e,E_e>=0.                            (10)

Таким образом свободная вариация sigma ПРИ ФИКСИРОВАННОМ e не зануляется
по названию: она в точности является прежним coframe-направлением. Когда
все coframe-строки выполнены, её строка выполнена автоматически. В kernel
(9) происходит реальная compensating вариация, а не удаление объёмной моды.

Собственная материальная метрика получается из того же усиленного символа:

    K_mat=sigma m g^-1,
    e_hat,sigma=sqrt(m sigma/E)e,
    g_hat,sigma=(m sigma/E)g.                            (11)

Это ровно прежняя density-involution карта, применённая к e_tilde.
Независимая omega варьируется ДО исключения. Подставлять формулу conformal
Levi-Civita связи до вариации и удалять производные sigma нельзя.

Общий случай r_theta'(0)=s(theta)(rf,rq), s>0 сводится сюда без новой
независимой переменной: взять sigma=s(theta), а
hat r_theta(v)=r_theta(v/s(theta)). Нужны фактические uniform bounds (2)
после этого преобразования. sigma — вычисленный коэффициент исходного
семейства, а не дополнительно постулированный материальный scalar.

## 4. Один полный determinant сохраняет все новые независимые строки

Для каждой текущей копии j возьмём полный READY corner

    c_j=1-2a_h bar r_(h,j),  c_j>=c_*>0,

при настоящем фиксированном a_h. Как у владельца, всё прошлое остаётся
A=C_<*C_<>=0, Tr A>0, eta=p^K, s=product_j c_j²,
D=(1-z)I+z eta s A. Вся цена остаётся B=H-Tr log D.
Положим

    L=sum_j 1/c_j, w_j=(1/c_j)/L,
    Gamma=4a_h eps_h rf z eta s Tr(D^-1 A)L>0.

Прямое дифференцирование даёт без предположений о коммутировании A,DA:

    DJ/Gamma = F_old
              +sum_j w_j Dbar r_(h,j)/(eps_h rf),
    F_old=-Tr(D^-1 DA)/[4a_h eps_h rf L Tr(D^-1 A)].      (12)

На max-норме независимых нынешних полей/амплитуд/shape/PF параметров(5) даёт

    ||DJ/Gamma-F_old-sum_j w_j D I_(h,j)^sigma||
           <=eps_h sum_j w_j C_j.                      (13)

Uniform C_j<=C даёт C eps_h, независимо от числа копий. Это НЕ1/M-удаление
ненулевого источника: для одинакового ненулевого полевого ковектора E сумма
w_j||E|| равна||E||. Все shape-строки ограничены (4) до повторения.

Полный source budget имеет вид

    ||DB/Gamma - sum_j w_j pi_sigma,j* E_ES||
       <= E_old + E_geometry + C eps_h
          + E_native_contrasts + E_full_heat.           (14)

Все старые слагаемые имеют прежние доказанные owners и настоящий gain.
Нормированный trace/архивная матрица не заменяют физическое состояние.

Точное тепло совпадает для фиксированной полной отражённой factorization
на прежнем однородном fixed-clock носителе; с записанным tensor-прошлым
сигнатура каждого нового отражения также сохраняет спектр полного endpoint.
Но для реальных raw-growing histories с новыми рождениями это не объявляется
автоматическим тождеством. Там используется ПРЕЖНИЙ growing-clock budget
с фактической новой длиной, всеми birth details, harmonic modes и ресурсами.

К порядку выбора ресурса владельца добавляется лишь действительный новый
конечный postprocessor: сначала chart/bounds/epsilon/M/t, затем точности,
все полные target-слова и их вычисленная длина, после этого retention K
и цена/read precision. Больше стадий оплачиваются; они не маскируются
старым clock. General native admission этого нового кода из M1 не выводится.

## 5. Soundness/recovery теперь для класса разных report laws

Пусть выполнены старые geometric/decoder/raw-clock/native-budget условия,
(1)–(2), положительные регулярные sigma/PF bounds и реальные lift maps.
Предельный источник(14) есть полная pullback Einstein–two-scalar система
для метрики(11), с прежним lambda=-rq/rf.

Для каждого фиксированного плотного гладкого теста поля правый lift (9)
сохраняет его в source: delta sigma=delta theta=0. Поэтому нулевой полный
κ-source влечёт все42 геометрических уравнения. При геометрическом решении
обратные field-name lifts и (4),(14) дают norm recovery, включая независимые
shape-строки. Никакая конечная сетка не объявляется сюръективной на весь C3;
используется исправленный fixed-test density аргумент родителя.

Свободные compensated sigma-направления являются ядром ведущей карты;
нескомпенсированные — входят в coframe-источник по(9)–(10). Ведущий coupling
не меняется. Следовательно это расширение существующего κ-source результата,
а не доказательство другой системы с новым уравнением amplitude.

Разные laws r_theta не обязаны быть all-input faithful исходному r при конечном
h. Их исходные probability records и абсолютные цены могут различаться.
Теорема отождествляет только ПРЕДЕЛ полных нормированных источников на
заявленной регулярной области. Arbitrary fine-record observables, quantum
channel equality и универсальное физическое X_N этим не отождествляются.

## 6. Конкретное изменённое правило реализуется конечной таблицей

Чтобы (1) не было пустым условием, берём существующий составной
READY-and-REPORT Bernoulli effect P=a_h r(u), а его reference значение
P_*=a_h r0 вычисляем из того же нулевого operand и исходного кода.
Для -1<=theta<=1 определим

    Q_theta(P)=P+theta P(1-P)(P-P_*)².                   (15)

Точно:

    Q_theta(P_*)=P_*, Q'_theta(P_*)=1,
    ∂theta Q_theta(P_*)=∂theta Q'_theta(P_*)=0.

Но Q_theta в общем случае не равно P. Например во внешнем structural
контроле P=.21,P_*=.19 получены .20993364,.21,.21006636 дляtheta=-1,0,1.
Эти различия реально сохранены, не названы gauge.

Разложение Bernstein степени4 имеет коэффициенты

    beta0=0,
    beta1=1/4+theta P_*²/4,
    beta2=1/2-theta P_*(1-P_*)/3,
    beta3=3/4+theta(1-P_*)²/4,
    beta4=1.                                           (16)

При P_* in[0,1],theta in[-1,1] все beta_k in[0,1]:
 beta1 in[0,1/2], beta2 in[5/12,7/12], beta3 in[1/2,1].
Поэтому выполняются четыре исходных trials, сохраняется число k успехов,
а условный финальный report имеет вероятность beta_k. Тогда

    sum_k binom(4,k) beta_k P^k(1-P)^(4-k)=Q_theta(P).

Неизвестное квантовое состояние не клонируется. Если каждый исходный
report имеет полный scalar effect P I на защищённом DATA, совместные
вероятности последовательных fresh-report instruments действительно
Bernoulli: trace каждого выбранного branch умножается на P или1-P для
любого оставшегося, включая entangled, DATA-state. Либо используются
реальные отдельно порождённые текущие банки прежнего конструктора.

Полный target есть сохранённые trial-регистры и controlled output rotation,
весь32-колоночный preparation A, затем отражённый wrapper A* Z A. Копии
результатов и их обратные стадии остаются в carrier. После raw-born
conjugation G^tensor5 получается настоящий input v^tensor5, а не новый
примитивный blank. Code проверяет полные матрицы, но НЕ печатает новое
G/CX/SourceI слово: применение прежнего full-column compiler и его
finite-error budget является аналитической композицией, не новым запуском.

Нормированный shape-family r_theta(u)=Q_theta(a_h r(u))/a_h удовлетворяет
(1) точно. На реальном компактном reference a_h in(1/3,7/20), r0>0 его
положительные controlled probabilities имеют требуемые genuine margins;
крайние beta0,4 постоянны. При r<=1/4 и P_*=a_h r0<=7/80:

    Q_theta(P) <=(7/80)[1+(7/80)^2]=45143/512000,
    c_new>=210857/256000>4/5.                            (17)

Используется этот реальный новый cold bound, а не прежний33/40, который
буквально может не сохраниться. Существующие full-source/retention proofs
нуждаются в положительном bound; их constants пересчитываются на4/5.

Переход от математического target к конечным raw словам сохраняет
ошибки полного составного эффекта. Требование δ/(epsilon_h |t|)->0
с реальными coefficients не отменено. Наличие биномиальной таблицы
не означает допуск её физических операций во всех X_N.

## 7. Что действительно не должно исчезнуть

Три отрицательных контроля ограничивают вывод:

1. Независимая добавка theta к r0 имеет normalized source1/(epsilon rf).
   Её нельзя удалить как «постоянную» при вариации самого theta.
2. Изменение отношения rq/rf создаёт leading delta lambda*q. Оно не
   поглощается общей положительной coframe-шкалой и меняет материальную
   константу. Эта строка остаётся O(1).
3. Даже exact first-jet matching и uniform D_u² недостаточны без mixed
   derivative bound: R_h(u,theta)=u² sin(theta/epsilon_h²) имеет нулевые
   value/first jet приu=0 и bounded u-Hessian, но приu=epsilon,theta=0
   (∂theta R_h)/epsilon=1/epsilon. Его нельзя объявить irrelevant.

В текущем двухоперандном маршруте остаток задачи выбора тем самым
сокращён с целой функции отчёта до reference-baseline, ведущего отношения
двух откликов, действительной регулярности и native-domain обязательств.
Общая closure/M1 всё ещё не доказывает эти условия автоматически; критерий
необходимой физической селекции не объявлен решённым. Это не исключает
другие способы контролировать оставшиеся направления.

## 8. Исполненная проверка

Самодостаточный `check_report_jet.py`: 141 checks, ordinary/-O/repeat JSON
побайтно идентичны, stderr пуст. Это количество проверок реализации,
не141 новых математических теорем. Выполнены:

- exact Bernstein identity и value/first/mixed jets;
- полный32-колоночный reporter с raw-born input и полный128-мерный
  old+current operator, не нормальное прошлое и обе clock-степени(1024 modes);
- exact rational совместная Taylor-оценка с independently varying PF,sigma,theta;
- исходный full-CAR positive-y polynomial, настоящий r_f,lambda и полный
  matrix logdet на100 decimal digits. Gain от2.2055e-32 до4.3076e-35;
- независимые shape-строки НЕ нулевые при finite epsilon, но их dual norm
  уменьшается с9.92249e-16 приepsilon1/16 до1.90575e-18 приepsilon1/8192;
- все42 pointwise Palatini directions плюс новая amplitude-строка,
  exact redefinition and Ward identity; источник в точке не равен нулю;
- три отрицательных контроля §7 и отсутствие1/M недилюции.

Погрешность матричного determinant равенства<=1.91e-21;
42-coordinate chain error1.33e-15; amplitude Ward error4.86e-17.
Большая сетка, native postprocessor emission, общий PDE, Lean, repository CI
и независимая научная приёмка не запускались. Parent heavy checks не повторены.

## 9. Стандартные методы и граница новизны

Nacu–Peres, *Fast simulation of new coins from old*, arXiv:math/0309222,
и Holtz–Nazarov–Peres, *New coins from old, smoothly*, arXiv:0808.1936 —
первичные источники стандартного Bernstein/Bernoulli-factory подхода.
Здесь(15)–(17) полностью выведены; не заявляется изобретение этого метода.

Criado–Perez-Victoria, *Field redefinitions in effective theories at higher
orders*, arXiv:1811.09413 — стандартный контекст обратимых замен полей.
Настоящее(7)–(11) — точное классическое следствие уже owned степени -2,
не утверждение равенства квантовых теорий или всех finite record instruments.

Вклад пакета — единая явная подстановка (4),(8),(12) в полный прошлый
D0-source theorem и непустой класс изменённых report laws с собственными
независимыми строками. Старый строгий finite root/physical_X_N контракт
не переименован и accepted claims/main не повышены.
