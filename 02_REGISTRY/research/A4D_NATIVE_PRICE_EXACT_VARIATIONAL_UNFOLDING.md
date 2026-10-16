# Полная существующая цена: точное вариационное развёртывание, все источники и конечный тест невязки

16 октября 2026. Продолжение SOURCE #334; исторический вход #310. Вход: `4cf20e47da327666302370ee42579b29048d2ca0`.

**Область:** та же цена v8 `H+J_program+R` и тот же bounded stored-adjoint класс, для которого первичный владелец уже доказал полное operator/program intertwining. Ни нового выбранного Q, ни добавленной AF-терминальной цены, ни замены определения тепла здесь нет. Ниже замкнута расширенная вариационная система этого конечного сектора; **выбор его программы основаниями D0, весь физический Cost−Info, Einstein-предел и исходный raw-owner terminal этим не закрываются**.

## 0. Место в общей цепочке

Потребляются, а не повторяются:

1. [Основания без перебора каталогов](https://github.com/gvakhrushev/d0_15/blob/4cf20e47da327666302370ee42579b29048d2ca0/02_REGISTRY/research/A4D_FOUNDATION_FORCING_NOT_CATALOGUE_SEARCH.md): исходный процесс и его геометрическое представление должны согласовываться по порождающим операциям, подготовке и чтению. Функциональный кортеж не выбирает произвольное программируемое действие.
2. [Полный источник и перенос](https://github.com/gvakhrushev/d0_15/blob/4cf20e47da327666302370ee42579b29048d2ca0/02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md), §§0.1,0.3: один и тот же selfadjoint stored Dirac, все16 exterior components, настоящий observer-whitening, полный прибор v8 и все его source jets. Не следует снова объявлять этот ограниченный operator map неизвестным.
3. [Исходный v8](https://github.com/gvakhrushev/d0_15/blob/4cf20e47da327666302370ee42579b29048d2ca0/02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md): фиксированная цена, калибровки, полный workspace/reference, certified homogeneous root. Старый root search не повторяется.
4. [Совместный adjoint-source](https://github.com/gvakhrushev/d0_15/blob/4cf20e47da327666302370ee42579b29048d2ca0/02_REGISTRY/research/A4D_NATIVE_JOINT_ADJOINT_SOURCE.md) и [constrained source](https://github.com/gvakhrushev/d0_15/blob/4cf20e47da327666302370ee42579b29048d2ca0/02_REGISTRY/research/A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md): допустимые joint curves и их полный pullback, а не независимые ambient variations.

Цель нового результата: сохранить полное действие вместо перехода к отдельному curvature readout, явно решить его статистические вспомогательные уравнения, доказать точную эквивалентность первых/вторых вариаций и дать проверяемую оценку ошибки источника. Вспомогательные переменные не требуют нового физического постулата о приготовлении Gibbs-состояния.

## 1. Неизменённая цена и носители

Работаем сначала в фиксированном whitened Hilbert space H размерности d. Для actual stored-adjoint данных это пространство получается существующим полным exterior isometry; невырожденность и smoothness этого отображения остаются его гипотезами.

Пусть D=D*, Delta=D², alpha>0, m=2n, beta=m alpha,

    B=I-alpha Delta,   b0 I<=B<=I,   b0>0,
    K=B^m,   F=I-K,
    A=I-zF=(1-z)I+zK,   0<=z<1.

У старого v8 b0=p³, multiplicity M=128 и C=128 workspaceDim. Здесь C>0 и M>0 оставлены явно; они НЕ перенормируют trace на H и не удаляют состояния. Тепловой generator есть

    Lambda=-(1/alpha)log B,  K=exp(-beta Lambda),

а matter использует Delta, не Lambda. При физической нормированной амплитуде Psi на H tensor H_ref положим rho_m=Tr_ref |Psi><Psi|/||Psi||². Полная цена:

    S=Tr(rho_m Delta)+(1/beta)log(C Tr K)-M Tr log A.        (1)

Слагаемое C кодирует неизменённые workspace/reference multiplicities первичного вывода. Множитель M принадлежит полному feedback. Ни counting trace, ни PF trace, ни geometric volume не отождествляются.

## 2. Точная совместная вариационная реализация

Вводим две **математические вспомогательные переменные**, не новые физические поля материи:

- sigma>=0, Tr sigma=1 на том же полном H;
- X>0 на H, без нормировки trace.

Пусть H_vN(sigma)=-Tr sigma log sigma, с 0log0=0. Зададим

    L(x;sigma,X)=R(x)+log C/beta
             +[H_vN(sigma)+Tr(sigma log K)]/beta
             +M[d+log det X-Tr(XA)],                     (2)

где x включает все прежние геометрические, link, observer и matter данные. Это не новая выбранная цена: сейчас доказывается её точная эквивалентность (1).

**Теорема 1.** При каждом допустимом x

    S(x)=max_(sigma>=0,Tr sigma=1; X>0) L(x;sigma,X),
    sigma_*=K/Z, Z=Tr K,   X_*=A^-1.                    (3)

Максимум единственен в этих вспомогательных переменных. Более того, для любой пробной пары

    S-L = D(sigma||sigma_*)/beta
          +M[Tr Y-log det Y-d],
    Y=A^(1/2) X A^(1/2).                                (4)

Оба слагаемых неотрицательны и одновременно нулевые ровно при (3).

**Доказательство.** log sigma_*=log K-log Z I. Подстановка в определение относительной энтропии даёт первое равенство разности. Для второй части det Y=det A det X, Tr Y=Tr XA. Применение y-log y-1>=0 к положительным eigenvalues Y даёт знак и единственность. Никакого предположения [sigma,K]=0 или [X,A]=0 нет. Эти коммутирования выполняются у найденного максимума, а не задаются всем пробам. Нулевая Delta-мода даёт K=1 и A=1 и остаётся в Z. □

Использованная Gibbs/logdet duality — стандартная математика. Новое применение относится к полной неизменённой цене и всем её вариациям на текущем D0-интерфейсе, не к мировой новизне вариационной формулы.

### Важное различие с физическим минимумом подготовки

sigma здесь — переменная вариационного представления уже данного log trace; X — переменная представления уже данного logdet. Они не отождествляются с rho_m, AF sigma или дополнительно приготовленным устройством. Максимизация в (3) вычисляет ту же исходную функцию. Она НЕ утверждает, что физический engine термализуется, достигает максимума энтропии или минимизирует только терминальный record-price.

Для обычных stationary equations используем **интерьер** sigma>0, X>0. Их условия дают log sigma+beta Lambda=constant I и X^-1=A, то есть (3). Если вместо этого параметризовать sigma=CC*/Tr(CC*) и включить нулевые ranks как гладкие амплитуды, можно создать граничные критические ветви. Мы не объявляем их новыми корнями исходной задачи. Максимум (3) остаётся faithful, поскольку B>0. Все прежние rank branches физической Psi сохраняются без изменений.

## 3. Эквивалентность всех стационарных уравнений

В интерьере auxiliary domains:

    d_(x,sigma,X) L=0
       <=> d_x S=0, sigma=sigma_*(x), X=X_*(x).        (5)

Доказательство не требует, чтобы dS=0 было минимумом. Вспомогательные уравнения однозначно фиксируют (3), а envelope rule на их trace/positivity domains даёт dS=partial_x L. Обратно любой исходный root имеет единственный auxiliary lift. Это биекция стационарных множеств для того же x и тех же допустимых curves.

Для сингулярного native constraint set равенство первых источников читается вдоль действительных допустимых C1-кривых. Линеаризованные formal tangent solutions не объявляются интегрируемыми. Утверждения о Hessian ниже требуют соответствующего C2-манifold chart либо отдельной допустимой C2-кривой.

При fixed alpha,m,z,C,M получается **один полный оператор источника**:

    W=rho_m - B^(m-1)/Z + M beta z B^(m-1) A^-1,
    dS=Tr(W dDelta)+Tr(Delta d rho_m),                 (6)

или, без ложного [rho_m,D]=0,

    dS=Tr[(D W+W D)dD]+Tr(Delta d rho_m).

Формула следует из полного некоммутирующего polynomial derivative

    dK=-alpha sum_(j=0)^(m-1) B^j (dDelta) B^(m-1-j)

и цикличности trace. Коммутируют spectral functions B,A, но не произвольные dDelta и rho_m. Член heat содержит B^(m-1)/Z, **не** K/Z: finite generator Lambda отличается от Delta.

Matter variation на полной сфере H tensor H_ref по-прежнему даёт

    (Delta tensor I)Psi=epsilon Psi, epsilon=R.

Никакого collapse полной reference/Schmidt-структуры к pure16 здесь нет. Геометрические уравнения — существующий constrained pullback (6) через actual native map. Если этот map не допускает независимую metric variation, (6) не делает её допустимой. Источник не выбирается как требуемый Einstein tensor.

### Полевые калибровки и движущаяся нормировка

(3)–(5) остаются тождествами, когда alpha,beta,z,C,M зависят от полей и сохраняют указанную область; использовать тогда нужно полную производную

    dS=dR+(dlog C)/beta+Tr(dK)/(beta Z)
        -log(CZ) dbeta/beta²
        -Tr(log A)dM -M Tr(X_* dA),                  (7)
    dA=-(I-K)dz+z dK.

При fixed integer m и moving alpha в dK входит dB=-alpha dDelta-Delta dalpha. Если beta=m alpha, её производная также входит в (7). Изменение discrete n/размерности носителя не является гладким полевым derivative. В обычном v8 root используются его исходные fixed calibrations; их физическая вынужденность не доказывается (3).

## 4. Вторая вариация: исчезают две вспомогательные проблемы обращения

На вспомогательном максимуме Hessian по sigma и X имеет два независимых отрицательных блока. В пространстве Hermitian trace-zero H для sigma:

    -L_sigma,sigma[H,H]=(1/beta)Tr[H Dlog_(sigma_*)[H]]
                          >= ||H||_HS²/beta.        (8)

Поскольку lambda_max(sigma_*)<=1, каждое logarithmic divided difference не меньше1. Вырожденность Delta не мешает: повторным eigenvalues соответствует производная1/lambda. После настоящей trace-zero compression

    ||(-L_sigma,sigma)_T^-1||_(HS->HS)<=beta.

Для Hermitian Y во втором блоке:

    -L_X,X[Y,Y]=M Tr[A Y A Y]
                    >=M(1-z)² ||Y||_HS²,
    ||(-L_X,X)^-1||<=1/[M(1-z)²].                    (9)

Эти две границы не содержат dimension(H) и не требуют gap между разными eigenvalues D. Они не дают uniform bounds для всего physical Hessian, для beta(h), или для смешанных field-to-operator maps. Малые eigenvalues sigma_* ухудшают прямую entropy-Hessian, но не указанную верхнюю границу её обратной.

Профили изменяются по

    d sigma_*=(dK)/Z-K(dZ)/Z²,
    d X_*=-X_*(dA)X_*;                              (10)

первая формула сохраняет normalizer и все off-diagonal coherences. Также

    Dlog_(sigma_*)[d sigma_*]+beta dLambda
                   =-dlog Z I

при fixed beta. Нельзя заморозить ни одну из этих производных при переходе ко второму источнику.

Обозначим y=(sigma,X), H_y=L_yy. Для исходной полной цены точно

    Hess(S)=L_xx-L_xy H_y^-1 L_yx.                  (11)

На любой совместной critical point extended Hessian конгруэнтна diag(Hess(S),H_y). Kernel и исходные negative directions не теряются. Добавляется ровно `2d²-1` отрицательных вспомогательных направлений; это свойство представления max, не новые физические неустойчивости. Никакой positivity полной gravitational action из (8),(9) не следует.

Вдоль действительной кривой вспомогательные Schur-вклады равны

    Corr_H=Tr[sigma_*' Dlog_(sigma_*)[sigma_*']]/beta,
    Corr_J=M Tr[A X_*' A X_*'].

Они неотрицательны. Полная вторая производная — frozen-auxiliary second derivative плюс эти два **вычисленных** вклада, а не назначенный positive remainder. Это напрямую потребляет уже имеющиеся all-field/source jets.

## 5. Цена ошибки прямо ограничивает ошибку физического источника

Пусть пробные sigma,X удовлетворяют области (2), а

    eps_H=D(sigma||sigma_*)/beta,
    eps_J=M[Tr Y-log detY-d],    Y=A^(1/2)XA^(1/2).

При eps_H,eps_J>=0 и `q>=max(1,||Y||op)` для любой фиксированной native вариации v:

    |dS[v]-partial_x L[v]|
       <=sqrt(2 beta eps_H)||dLambda[v]||op
        +q sqrt(2 M eps_J)
           ||A^-1/2 dA[v] A^-1/2||HS.              (12)

Первая часть — quantum Pinsker `D>=||sigma-sigma_*||_1²/2`; вторая следует из f(y)=y-log y-1 и f''>=1/q² на отрезках между1 и eigenvalues Y. Затем применяется trace Cauchy–Schwarz. Условие на q проверяется на тех же actual matrices. При operator norms, переходе к local raw sums и растущем H сохраняются соответствующие norm factors: HS-bound не объявляется независимым от размера для всех field perturbations.

На fixed-alpha domain из §1 дополнительно

    ||dLambda||op<=||dDelta||op/b0,
    ||A^-1/2 dA A^-1/2||HS
       <=z beta ||dDelta||HS/(1-z).                (13)

Следовательно это исполнимый **source residual criterion**, а не сравнение одного значения действия. Перед применением к исходной h^-2 raw,l1 норме нужен действительный spatial reconstruction; его не заменяет (13).

## 6. Эти вспомогательные чтения уже принадлежат полной программе

sigma_* не нужно объявлять дополнительно физически приготовленным Gibbs-state. Его любое чтение на том же полном H вычисляется из исходной survival-программы:

    Tr(sigma_* O)=Tr(K O)/Tr K.

Векторы/матрицы сравниваются как взвешенные фактические survival results, с сохранённым знаменателем, а не как безусловная postselected preparation. Все failure outcomes остаются в полном процессе. Если реально готовить условное состояние, ресурс и archive protocol этого нового приготовления требуют отдельного учёта.

Возвратный профиль есть resolvent самой исходной F:

    X_*=(I-zF)^-1=sum_(j=0)^infinity z^j F^j.

Это не каталог разных моделей: все члены являются степенями одного исходного положительного return-оператора, с фиксированным z. Не утверждается F^j=U^j: физическое исполнение степени с её проектированиями и обратными операциями требует соответствующего admitted circuit, если нужен именно новый лабораторный опыт, а не вычисление прежнего resolvent. Для `X_k=sum_(j=0)^k z^j F^j` точно

    X_*-X_k=z^(k+1)F^(k+1)X_*,
    ||X_*-X_k||op<=z^(k+1)/(1-z).                 (14)

Все modes F сохраняются; усечение касается длины истории и имеет доказанный хвост. При fixed z source error feedback от такой замены не больше

    M z^(k+2)||dF||_1/(1-z)
       <=M beta z^(k+2)||dDelta||_1/(1-z).         (15)

Finite history readout всё ещё оценивает probability expectations с конечной статистической точностью; (14) не превращает эксперимент в exact-real oracle. Правило выбора k должно быть связано с необходимой precision исходного теста.

## 7. Совместимость с исходным M1/primitive intertwining

Последний primary SOURCE §0.3 уже доказывает `V_a I=I U_a` для каждого primitive **объявленной v8 программы** и соответствие всей цены на bounded stored-adjoint family. Теперешние профили — функции этих же перенесённых operators: K, logK, A^-1. Они поэтому переносятся тем же I без нового выбора spectral eigenbasis.

При изменении observer I все его производные сохраняются. В фиксированном whitened frame представительные commutators в rho_m,Delta и их products сокращаются в trace. (4) и (11) — тождества одной scalar function; их перенос на native representation не оставляет отдельного необоснованного entropy source. Но это не создаёт native primitive permission или dynamics там, где primary owner доказывает лишь условное operator representation.

Доказательство от противного здесь закончено для конкретного нужного утверждения: если та же заданная S имеет другую interior auxiliary critical pair, она должна удовлетворять `log sigma+beta Lambda=constant I` и `X^-1=A`. Первое плюс trace1 фиксирует sigma_*, второе фиксирует X_*. Противоречие. Не потребовалось перечислять альтернативные тепловые подготовки или резольвенты.

Не следует расширять этот вывод до «M1 уже выбрал саму S». Functional tuple обеспечивает воспроизводимое чтение. Общий исходный price/primitive law и его геометрический Einstein предел требуют своих владельцев. Эта заметка не превращает необходимую структуру проверки в достаточное уравнение гравитации.

## 8. Что действительно доведено до конца и что осталось физическим

Внутри одного неизменённого full v8-price получены: exact variational identity; единственный полный auxiliary profile; биекция всех stationary points на реальном x-domain; все первые источники; полный Schur-second source и kernel correspondence; две явные dimension-free auxiliary inverse bounds; цена ошибки как source bound; конечный контролируемый history readout. Это одна замкнутая математическая конструкция, а не пять независимых выбранных моделей.

Главное применение к дальнейшему выводу: heat/feedback preparation и их скрытые derivatives больше не должны становиться отдельными postulates или подбираться для компенсации геометрии. Они определены одной исходной ценой. При решении полной нелинейной системы можно исключить sigma,X строго, сохранив только трудный physical coframe/link/matter блок; нельзя исключить прежний реальный shell/observer residual как будто он тоже auxiliary.

Существующий certified homogeneous root v8 автоматически имеет единственный lift (3) и остаётся stationary point той же области; повторного решения root для этой перепараметризации не нужно. Это обеспечивает непустоту применения на уже установленном native-sector, а не только на тестовой матрице. Неплоский native root этим не построен.

**Не решено здесь:** выбор всей этой программы/цены и её historical costs из D0-core; физический допуск полного prepared matter/reference и scales; identification положительной record curvature с Lorentz geometry; nonflat full native critical family; uniform spatial/AF refinement и исходный exact-source/raw-owner terminal. Последний computed curved-wave obstruction primary SOURCE сохраняется: (5) переносит его, не обходит.

Для последнего GR-заявления нужно на этом же поле доказать действительное равенство геометрического source с Einstein source и отдельно вывести оставшийся физический stress. Определить stress как остаток до желаемого G нельзя. Ни (4), ни наличие ролей detector/history не доказывают это равенство сами. Поэтому **полная ОТО не объявлена закрытой**.

## 9. Реплей и математический контекст

`check_unfolding.py` выполняет exact SymPy расчёт: один zero Dirac mode; opposite-sign Dirac и повторные Delta eigenvalues; complex noncommuting first/second jets; полный нормированный two-reference matter; все15 trace-zero Hermitian density и16 precision directions; некоммутирующий entropy-gap и logdet-gap; полную second-response/Schur identity; историю resolvent и observer commutators. Размер4 — конечный проверочный fixture общей теоремы, не замена full16 native carrier. Проверки не исполняют старые suites и не доказывают primitive admission.

Обычный и оптимизированный Python дают одинаковый JSON. Четыре изменённых вычисления отвергаются математически: замороженный normalizer, неверный inverse derivative, удалённый thermal Schur-вклад, замена теплового generator на Delta в source.

Стандартный контекст: Reible–Hartmann–Delle Site, *Two-sided Bogoliubov inequality to estimate finite size effects in quantum molecular simulations*, Letters in Mathematical Physics 112,97 (2022), DOI 10.1007/s11005-022-01586-3 (Gibbs variational principle/relative entropy); Boyd–Vandenberghe, *Convex Optimization* (logdet concavity/conjugacy). Эти теоремы используются как математика и не вносят новых физических предпосылок. Все нужные finite identities доказаны выше; внешние статьи не заменяют native owner.
