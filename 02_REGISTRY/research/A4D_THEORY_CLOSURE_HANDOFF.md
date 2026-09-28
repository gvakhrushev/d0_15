# Расширенное ТЗ: завершить теоретический мост A4D → designated Einstein

**Назначение:** единое теоретическое поручение по оставшемуся мосту выбранного naked-star действия A4D к нелинейному метрическому отклику Эйнштейна. Это документ передачи работы, а не новый доказанный результат или новая зарегистрированная задача.

**Репозиторий:** `gvakhrushev/d0_15`, https://github.com/gvakhrushev/d0_15.
**Язык:** русский, формулы и точные определения.
**Режим:** доказательства в облаке; большие вычисления и окончательное воспроизведение сертификатов локально.
**Исходная интеграция:** PR [#317](https://github.com/gvakhrushev/d0_15/pull/317), ветка `exp/a4d-resonance-divisor-stratification`, проверенные исходные данные на `72047a0a59a9f9269d9e6f153cbc587bb6899d25`; baseline `main` для этих данных — `e80a3b1ccf615fb4f70bf5900181592604928497`. Эти результаты находятся в ветке PR, а не объявлены слитыми в `main`.
**Владелец отклика:** существующий Draft PR [#310](https://github.com/gvakhrushev/d0_15/pull/310), ветка `exp/a4d-joint-response-resolvent`, известный входной head `fc0d7aea8a58fef628e96a0aff3cf506755db43f`. Перед записью результата сверить свежий head; не дублировать этот PR.
**Граница:** выбранный A4D star-action → designated Einstein. Полное завершение остальных ветвей D0, отдельного full-affine носителя #202, Lean и публичных физических claims не входит в это поручение.

## 1. Цель и критерий завершения

Завершить математическую цепочку

\[
\text{резонансная геометрия и совместимость}
\longrightarrow
\text{точный стационарный лист на меняющемся фоне}
\longrightarrow
\text{контроль метрического отклика всех допустимых модулей}
\longrightarrow
\text{равномерный нелинейный предел и геометрическая реконструкция}.
\]

Сначала сформулировать точное конечное утверждение с кванторами; затем довести до конца все его действительно необходимые леммы. Полная факторизация, локальная нормальная форма, один обнулённый луч или один полюс — промежуточные результаты. Они не являются завершением поручения.

Положительный результат обязан включать:

1. Непустой, содержательно заданный класс фиксированных гладких невырожденных метрик и точных стационарных связей, допускающий ненулевую макроскопическую кривизну. Класс и условия листа заданы независимо от желаемого ответа. Для общего response-decoupling terminal он включает owned grid-scale nongauge микроструктуру #232 в заявленном chart; ограничение одной заранее выбранной гладкой связью не доказывает этот terminal. Если существующие данные действительно исключают часть микроструктуры, это исключение нужно вывести, а не добавить по определению.
2. Существование точной связи для полного конечного connection Euler, а не только формального ряда, IR-параметрикса или конечного набора коэффициентов.
3. Оценку метрического отклика в явно указанной топологии с константами, равномерными по измельчению и числу взаимодействующих мод. Физические модuli либо дают тот же предел, либо их вклад ограничен доказанной оценкой.
4. Нелинейный предел реконструированного отклика `-G/2` для этого класса, с правильной нормировкой десяти Gram-слотов, устранением зависимости от вспомогательного фрейма и заявленным остатком.
5. Решение вопроса универсальности: какие другие точные листы допускает исходная теория, изменяют ли они физический отклик, и нужны ли дополнительные условия выбора. Условие выбора, не выведенное из исходных данных, должно оставаться явной дополнительной гипотезой.

Отрицательный результат обязан дать точный контрпример или доказательство невозможности конкретно сформулированного моста, показать, какие из более слабых designated-утверждений он оставляет в силе, и завершить их анализ. Один блокированный луч не опровергает все листы; отсутствие доказанной оценки не является no-go. Если часть цепочки остаётся открытой, конечный статус — PARTIAL/OPEN, а не «теория завершена».

## 2. Правильные объекты сравнения

Пусть `Q_h` — действительное конечное семплирование одной фиксированной гладкой Lorentz-метрики `g`, `K_h^sm` — гладкая приближённая ветвь #216, а `K_h` — точная связь на заявленном листе. `E_Q` — геометрический частный metric Euler выбранного действия, `E_K` — полный connection Euler. Зафиксировать разделение group link / dressed link / dimensionless logarithm; один символ `K` не должен незаметно менять тип.

Определить tensor reconstruction `R_h` в конвенции владельца и положить

\[
\mathcal E_h(g,K)=R_h\!\left[h^{-2}E_Q(Q_h,K)\right],
\qquad
\mathcal D_h(g,K)=\mathcal E_h(g,K)-\mathcal E_h(g,K_h^{\rm sm}).
\]

Необходимы два разных перехода:

\[
\mathcal D_h\longrightarrow0,
\qquad
\mathcal E_h(g,K_h^{\rm sm})\longrightarrow-\tfrac12G[g].
\]

Их сумма даёт требуемый предел для точной ветви. Формула `h^-2 ΔE_Q → -G/2` для разности с гладким comparator неверно смешивает эти две цели.

Первая страница итогового доказательства фиксирует: конечные carrier и boundary conditions; число фаз и реальные conjugate pairs; десять слотов `(00,01,02,03,11,12,13,22,23,33)`; поднятие индексов и фактор 2 на off-diagonal outputs; источник и comparator; норму, тестовые функции и реконструкцию; класс гладкости; компактные границы невырожденности; область link-log chart; зависимость всех констант. Uniformity для одного фиксированного `g` и uniformity по bounded классу метрик — разные утверждения.

Для операторного утверждения на тестовой метрике решается `E_K=0`; метрический source equation не подставляется в качестве доказательства отклика. Для утверждения о joint-critical sourced sequences отдельно задать исходный vacuum/matter contract и проверить обе конечные Euler-системы. Нельзя определить источник задним числом как полученный `E_Q`. Два решения с одинаковым заранее заданным metric source дают нулевую разность подстановкой: это контроль, а не homogenization theorem относительно #216 comparator.

## 3. Уже имеющиеся входы и их точная область

Читайте указанные владельческие файлы, а не старые сводки или числа из переписки. Вычисления ниже не повторять без необходимой проверки конвенции.

| Вход | Что установлено | Чего он не даёт |
|---|---|---|
| #201/#270 и direct Schur–Einstein cross-check | Низкочастотный плоский символ `K_Schur=-K_G^(1)/2`, нормировка десяти metric coordinates; `det A(1)=256` | Полный nonlinear continuum theorem |
| #208 и #216 | Нелинейный Lorentz quotient; IR-gap; гладкий approximate solve с `E_K=O(h^∞)`; Fourier/alias tails и суммированный IR remainder | Существование точного листа и uniform coupled normal rescue |
| #223/#226 | Normal-center locality и finite-stencil sensitivity, raw exponent 0, normalized loss 2 в своих chart/norm hypotheses | Контроль всех grid-scale модулей или Young measures |
| #232/#275, `A4D_Y_SLOW_JOINT_CONTINUATION.md` | Явная all-order joint-stationary Y-семья; response gap точно 0 на её заявленном, макроскопически плоском профиле | Искривлённый макрофон, весь `N0`, общий #240 limit |
| #314, `A4D_ORTH3_NONFLAT_T3H_RESPONSE.md` | В полном 96-row COS-джете с #260 log-correction и #241 solder источник `t³h` имеет ненулевой Fredholm pairing 1; range correction отсутствует | On-shell metric residue; доказательство невозможности иных detuned/multimode продолжений |
| #315, diagonal Smith owner | На диагонали `det A=(z²+1)^12/(16z^12)`, rank 16 при `i`, положительные Smith exponents `(1,1,1,1,2,2,2,2)` | Многопараметрический Smith form или глобальный полюс порядка 2 во всех направлениях |
| #317 на pinned head | Exact Hodge identities, 671-term determinant ledger, арифметическая факторизация над `Q(i)` и `Q`; generic arithmetic rank 23; exact complex rank-23 witness; physical even-rank/positivity | Absolute irreducibility над `C`, все intersection strata, stationary response |

В константном Hodge-базисе `T` имеем

\[
T^{-1}AT=\begin{pmatrix}0&M\\\sigma(M)&0\end{pmatrix},
\quad M(Z^{-1})=M(Z)^T,
\quad \sigma:i\mapsto-i\text{ при фиксированных }z.
\]

`rank A=rank M+rank σ(M)` на комплексном торе. На физическом торе `|z_r|=1` дополнительно `σ(M)=M†`, поэтому `rank A=2 rank M` и `det A=|det M|²`. Комплексный rank 23 и физическая even-rank теорема совместимы. Норма determinant не является квадратом рационального polynomial; физический resonance находится на пересечении двух coefficient-conjugate zero sets.

Новый direct SD/ASD replay восстанавливает тот же `A` и сверяет все 576 entries с owner table. Он подтверждает комплексный rank-23 свидетель: на `(u,1,-1,2)` имеем `det M=f(u)/(128u³)`; любой корень `f` прост и отделён от корней coefficient-conjugate `f`, откуда `rank M=11`, `rank σ(M)=12`, `rank A=23`. Следовательно, вывод «rank M и rank σ(M) совпадают при каждом фиксированном complex Z, потому что сопряжены их миноры» неверен: сопряжение коэффициентов не сопрягает одновременно точку `Z`.

Вторая поправка касается диагонали: точный рациональный результат `det M(i+w)=-w⁶(w+2i)⁶/[4(w+i)⁶]`. Полином `-1024 w⁶(w+i)⁶(w+2i)⁶` есть определитель матрицы `2(w+i)M`, так как общий знаменатель умножен на все 12 строк; забытый множитель `(2(w+i))¹²` меняет `det M`. Реплей проверяет это равенство явно.

Нулевой `E_Q(Q,I)` для всех `Q` не означает нулевой mixed derivative `D_K E_Q(Q,I)`: в #226 есть точный ненулевой sensitivity witness. Любое заявление об обнулении характерного mixed block должно сначала согласовать literal action, transpose, сопряжение и coordinate maps. F7/F9 и germ `q0=ddᵀ` не считать доказанным Ward-классом или метрически мёртвым во всех каналах по конечным samples.

## 4. Единая программа доказательства

### D. Геометрия опасных резонансов

Использовать уже найденную структуру `M` (12×12, четыре роли, 3×3 skew role blocks), а не пересчитывать большой determinant. Закончить absolute factor boundary и higher-codimension rank geometry там, где они действительно входят в доказательство отклика: regular pieces, intersections, дальнейшие rank drops, реальные unit-torus points. Для полного terminal #317 требуется полное constructible покрытие complex torus согласно его зарегистрированному brief.

Вывести содержательные kernel/cokernel координаты и локальные reduced normal forms, в частности около `(i,i,i,i)` с четырьмя независимыми character detunings. Отличить контакт выбранной diagonal curve от transversal degeneracy. Не вводить многопараметрический «Smith form» без соответствующего локального кольца и доказательства.

Для полного Einstein-моста допускается обойти несущественную комплексную классификацию, если доказано, почему вся оставшаяся область не влияет на выбранный физический класс и равномерную оценку. Тогда не объявлять закрытым отдельный full-classification terminal #317. Не заставлять конечный физический вывод ждать ненужного полного Gröbner census.

### R. Стационарное продолжение и реальный метрический отклик

Провести range/kernel reduction **полной** конечной connection equation на медленном фоне после genuine Lorentz quotient. Сохранять tangent equations, cokernel compatibility и все coupling между conjugate phases и различными модами. Явно вычислить/вывести сокращённое уравнение для физических резонансных amplitudes; `N0` и Orth3 — разные носители.

Для Orth3 сначала использовать уже доказанное препятствие на exact resonance. Проверить, устраняется ли оно admissible detuning, lower-order log corrections или взаимодействием мод в полном reduced equation. Detuning на физическом торе задавать через реальные фазы `z_r=exp(iθ_r)`; радиальный путь `i(1+δ)` сам по себе комплексный аналитический probe, а не реальная конечная последовательность. Exact detuned characters на периодическом carrier должны быть допустимыми lattice characters или сопровождаться иной явно заданной boundary realization.

При существующем продолжении рассчитать `E_Q` на реально решённой ветви с нужными nonlinear connection corrections и second-order metric terms. Формула вида `QᵀA^-1F` годится только как доказанная производная согласованной reduced системы, с указанными фоном и степенями; она не заменяет весь nonlinear response. Principal part/residue именовать только после задания пути/дивизора, normalization, source и on-shell correction. При отсутствии продолжения доказать его область невозможности и перейти к оставшимся допустимым модам.

Существенно: `EK=0` не требует uniqueness связи для Einstein-предела. Возможна общая метрическая response class для разных nongauge sheets. Сначала доказать или опровергнуть именно эту response equivalence.

### U. Refinement-uniform normal rescue или response decoupling

Закрыть недостающий динамический переход #216/#240/#310. Дать существование хотя бы одного exact sheet над genuinely curved smooth backgrounds и оценку всех sheet/moduli, включённых в заявленный класс. Стандартный достаточный путь:

\[
d_\perp(K_h,\mathcal Z_h^{\rm sm})
\le C h^{-p}\|r_h\|^\beta,
\qquad r_h=E_K(Q_h,K_h^{\rm sm})=O(h^\infty),\quad \beta>0,
\]

с постоянными `C,p,β`, не деградирующими при увеличении lattice size, переходе между rank strata, взаимодействии мод и изменении фона в заявленной компактной области. `Z_h^sm` содержит только реально допустимые smooth-fiber moduli; нельзя включить произвольные curved roots по определению. Если нормальное расстояние не контролируется из-за физических модулей, доказать непосредственно response estimate, достаточный для `D_h→0`, с контролем их действительных nonlinear moments/commutators.

Разрешён альтернативный подход через response quotient, compensated compactness или Young measures, если доказаны именно используемые moment constraints из finite Euler и passage через nonlinear metric variation. Weak convergence и bounded energy сами по себе не заменяют этого шага.

Обязательные hostile inference controls: isolated zero не гарантирует solvability; конечномерный Łojasiewicz exponent при каждом `L` не гарантирует uniform exponent; constant-background normal isolation не исключает slow-background bifurcation вроде `v³-hv`; гладкие Fourier tails не контролируют новые resonant couplings автоматически. Это тесты аргумента, а не контрпримеры к самому star action.

Не делить доказательство на «посчитали несколько коэффициентов — поэтому все порядки». Нужны реальная оценка остатка, convergence или иной полный nonlinear argument. Любая amplitude threshold должна выводиться из actual reduced equations и metric readout; эвристические `t=o(h^(1/3))` и экстраполяция одного джета не являются теоремой.

### S. Статус выбранного листа и необходимость selector

Определить, что именно в исходной постановке выбирает designated class: уже заданная sampling realization, фиксированные boundary/source data, допустимый continuation, либо другое реально имеющееся условие. Отличать математическое ограничение класса теоремы от эндогенного dynamical selector.

Если все допустимые физические модuli response-equivalent, connection selector может оказаться ненужным — доказать это. Если существуют разные response classes, доказать наличие/отсутствие отбора исходными finite equations и данными. Предъявить самостоятельное недостающее условие только как необходимую дополнительную гипотезу; не менять action и не выдавать spectral cutoff из proof parametrix за физическое правило.

Одиночный flat Y-контроль показывает multiplicity связи, но не разные curved-background Einstein responses. Отрицательный universality verdict должен опираться на actual nonflat stationary/sourced sequence в исходной конвенции, а не на off-shell 40-vector. Для no-go зарегистрированного joint-response brief нужны именно его source/comparator hypotheses и genuine joint-critical witness.

### E. Собрать конечную геометрическую теорему

После U/R применить уже owned low-momentum coefficient и normal-coordinate locality, суммировать все nonlinear orders и остатки, затем доказать covariance/reconstruction и frame erasure в указанном классе. Само наличие Lorentz gauge invariance не заменяет local-Diff naturality continuum response.

Итоговая оценка должна иметь буквальный вид, например

\[
\sup_{K_h\in\mathcal C_h(g)}
\|\mathcal E_h(g,K_h)+\tfrac12G[g]\|_{\mathcal T}
\le C_g h^\gamma+\varepsilon_h,
\qquad \gamma>0,\quad \varepsilon_h\to0,
\]

или иной явно доказанный mode of convergence. Привести exact определение `C_h(g)` и `T`, область существования и все hypotheses; не обещать uniform sup по неограниченному семейству метрик. Если заявлена только локальная pointwise/J²-теорема, отдельно установить, что требуется для её глобального/weak варианта.

Полевая sourced equation получается после отдельного fixed matter/source contract. Нормировку Newton constant, физическое время и все новые matter assumptions не выводить из одного коэффициента `-1/2`.

## 5. Распределение работы: облачная теория и локальные сертификаты

Приоритет дорогой модели — уменьшить сложность последней задачи и написать полный аргумент: invariant/kernel reduction, normal forms, existence mechanism, uniform estimates, response equivalence, geometric reconstruction. В облаке разрешены малые exact spot-checks. Большие 12×12/24×24 determinants, Gröbner/minor decompositions, многопараметрические jets по всем колонкам, character census и большие Lean builds выполняются локально.

Каждый необходимый локальный check выдаётся как отдельный буквальный контракт:

- literal input matrix/polynomial/ideal или точная конструкция из pinned source;
- поле/кольцо, localization, ordering, quotient и source convention;
- конечный exact algorithm и размер задачи;
- равенство, witness, rank/minor или estimate, который требуется проверить;
- доказанная связь этого выхода с теоремой и влияние противоположного исхода;
- какие conclusions остаются CONDITIONAL до успешного replay.

Не требовать от локального исполнителя «найти всю теорию». Не подменять proof условием «если остаток равен нулю», где этот остаток и есть основной вопрос. Если точная проверка ещё не выполнена, отметить это честно, а саму теоретическую часть довести до минимального finite certificate без скрытых исследовательских шагов.

## 6. Порядок чтения и сохранение результата

Сначала прочитать лишь:

1. `02_REGISTRY/research/A4D_RESONANCE_DIVISOR_STRATIFICATION.md`, `certificates/a4d_hodge_structural_review_results.json` и `certificates/a4d_sd_asd_reduction_results.json` **в ветке #317**; ledger и sparse entries открывать по необходимости. Уточнённый результат: комплексная rank-23 точка точна; удвоение ранга доказано только на unit torus; диагональная формула для `det M` rational, а напечатанный полином относится к матрице после очистки знаменателя.
2. `02_REGISTRY/research/MEMO_A4D_J2_SMOOTH_RESONANCE_CLOSURE.md`, особенно §§0, 7–8: здесь сформулирован actual coupled-rescue blocker.
3. `02_REGISTRY/research/A4D_ORTH3_NONFLAT_T3H_RESPONSE.md` и §§8–11 `A4D_Y_SLOW_JOINT_CONTINUATION.md`: obstruction против exact existence control.
4. `00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md`: source/comparator и terminal #240/#310.
5. `A4D_J2_METRIC_RESPONSE_SENSITIVITY.md`, `A4D_J2_NORMAL_COORDINATE_LOCALITY.md`, `A4D_SCHUR_EINSTEIN_DIRECT_IDENTIFICATION.md` и `ATORUS_TYPED_RESPONSE_RECONSTRUCTION.md` только в частях, которые использует доказательство.

Читать дополнительные owners только по явной зависимости. Ранние FUGU-пакеты и withdrawn response `Res≈110.85` не являются источником доказательства. Не начинать с 256-point scan или повторения Hodge factorization.

Доказательства D сохраняются в существующем owner #317; response/uniformity — в существующем owner #310. Это связанные разделы одной теоретической работы, а не разрешение создать новые child tasks/PR. Не менять чужой live head без проверки свежего состояния и явного назначения ветки. При работе без Git write access выдать готовые документы/патчи с точными repository paths и pinned входами для локальной интеграции.

## 7. Сдача: завершённая цепочка, а не один пункт

Итоговый документ должен содержать:

1. Главную теорему или exact no-go с полными кванторами, метриками, sheet/source class и топологией.
2. Dependency graph D→R/U→S/E, полный новый proof и ссылки на точно использованные существующие lemmas. Для каждой зависимости — PROVED / finite-certified / CONDITIONAL / OPEN.
3. Отдельные вердикты: existence точного designated sheet; универсальность по nongauge moduli; response-decoupling; nonlinear Einstein limit; нужен ли дополнительный selector.
4. Доказательство охвата опасных modes/strata и uniformity, включая genuinely curved backgrounds. Отдельно статус полного algebraic terminal #317, если физический proof его обошёл.
5. Минимальный список literal local certificates и готовые inputs; конечная оценка остатка; hostile controls против неверного шага.
6. Все реальные остаточные условия. Не ограничивать их искусственно «одним-двумя» и не скрывать missing assumption в определении класса.

**Правило продолжения:** после доказанной локальной леммы сразу переходить к следующей зависимости главной теоремы. Исчерпание времени/бюджета допускает сохранённый частичный результат, но не меняет критерий завершения. Цель поручения — окончательно решить теоретический мост в заявленной области и определить предел его универсальности.
