# B60. Исходные source marks на общем RAW checkpoint

**Результат:** A30 задаёт новый оплаченный порядок, в котором все семь исходных source banks подготовлены до первого REPORT, затем на их DATA выполнен явный `B_R`; на общей контрольной точке исходные ограниченные coframe/link/CAR moment operators имеют конкретные физические адреса и униформную оценку ошибки. Это утверждение о canonical fresh-WORK fibre и подготовленных source marks, а не полное all-dirty-column T2, физическое измерение, доказанный reader или равенство старой и новой цены.

## 1. Какие исходные операторы и состояния нужны

Оригинальный ten-sign owner, формулы (8), (9), (13), использует Choi state

\[
|\Omega_b\rangle=(32\cdot2049)^{-1/2}\sum_{a,i,j}(J_{b,a})_{ji}|a,i,j\rangle
\]

и anchor `r=(0,0,0)`. Для реально выбираемого `t=(a,i,j) != r` исходный ограниченный оператор

\[
H_t=32784(|r\rangle\langle t|+|t\rangle\langle r|)
\]

имеет норму 32784 и извлекает элемент `J_a[j,i]`. Coframe mark — его вакуум/grade-one entry; исходный link `U` требует `2H_t`, нормой 65568. Inverse-link, Cayley, coframe e и иные конечные chart-координаты восстанавливаются прежним regular decoder и его собственными нормами; нельзя заменять их просто переименованием (u). A11 periodic catalogue задаёт точные адреса и shifts.

Для материала оригинальные `A=0,15` на полном CAR carrier и без PF-множителя имеют

\[
\Psi_{z,A}=\frac{128}{\sqrt p}
 (|z,1\rangle\langle z,A|+|z,A\rangle\langle z,1|)\otimes I_{RIGHT},
 \qquad \|\Psi_{z,A}\|=128/\sqrt p<256.
\]

Все 16 grades, внутренний site и свежий RIGHT128 сохраняются; это не неизвестный oldRIGHT. Внешний общий SITE — отдельный регистр с прежними PF `|x><x|` и весом `N_x/10946`; его projector не входит в `B_R`. Для меняющейся плотности H.5 требует также настоящие PF marks и их действительную вариацию. Знаки/READY/report — отдельные исходные labels/effects, не маскируемые моментами.

A27/B54 доказывают на указанном product checkpoint оригинальные prepared-state моменты: f-bank имеет `(u_b,U_b,0)`, q-bank — `(u_b,I,Psi_b)`, с одной и той же coframe `u_b`; f даёт link, q — материал. Choi отражения дают нужный `O_b` на заявленном clean-private fibre; CAR готовит исходный vacuum/Fourier и `O_m O_m*^T` с `I_RIGHT`. Из этого получаются соответствующие исходные source-state/isometry marks, не тождество полного native target на произвольных dirty helpers. B54 отдельно связал все 72 192 leaf-индекса на банк и 1372 source slots с оригинальными моментами.

Для **UNSPLIT** исходного current-bank `(u_b,U_b,Psi_b)` H.5 прямо требует отдельный полный bank, если такая mark действительно нужна. Состояния split f и q не объявляются этой одной исходной квантовой копией. Он в A30 не добавлен.

## 2. Время и перенесённый RAW frame

В исходном A25 REPORT f находится на macro-index 594, а первый SOURCE q — на 1190. Потому исходные отдельные source completion точки сами не дают одновременную необработанную пару f/q. В A30 сначала идут SITE и все 7 наборов `SIGMA+196 SOURCE`, затем полный frame `B_R` и общий source checkpoint, после чего платный `B_R†`, семь REPORT и comparator. Все 1372 SOURCE и реальный порядок семи REPORT проверены по [самому schedule](audit_a30_checkpoint.py), [результат](A30_COMMON_CHECKPOINT_INDEPENDENT.json).

Перестановка оправдана **на идеальном canonical сравнении**: следующий source использует только свои свежие DATA/private и SAM как неизменяемый control; REPORT другого bank обращается к своей arena/source, с общим SITE и SAM только как controls. На требуемом свежем fibre ideal source и ideal report возвращают общий aux/port как identity. Поэтому операции переставляются для любого SAM/old input, включая когерентное и запутанное. Это не утверждение точной коммутативности приближённых native слов, которые могут временно использовать и запутывать общий helper/port. Новый гибрид получает свою prefix-ошибку; история, clock и цена пересчитываются.

Owner §7eh.C.2/H.3 требует `B_R U B_R†` и `B_R O B_R†` на ресурсах, исключая SAM, внешний SITE, labels и другие невходящие факторы. A25 source outputs до bridge находятся в computational frame. Использовать закодированный mark `B_R O B_R†` на таком невращённом output нельзя: точный одно-битный контроль из [проверки](audit_h3_marks_reordering.py) даёт несовпадение `2p²`. A30 действительно платит `B_R=G^⊗29848` **после** всей source подготовки, и оригинальные `B_R O B_R†` определены на общей точке; его реальный обратный bridge стоит native gates и находится перед REPORT. Неявного изменения basis нет.

Проверены все ресурсы: 1260 Choi по 22 wires и 112 CAR по 19 wires (внутренний SITE8 + grade4 + свежий RIGHT7), всего **29 848 разных**; ни один не является внешним SITE, SAM, report label, private helper, port или old factor. Независимый пересчёт показывает, что мост с его настоящими inverse depths в полном W добавляет на один такой wire `4G+18CX+24SourceI` до A29, затем `(4+192k)G+42CX` и 24 rotation-power blocks после преобразования. [Проверка моста](audit_raw_bridge.py), [результат](RAW_RESOURCE_BRIDGE_CHECK.json). После платного `B_R†` REPORT снова работает в computational frame; transport более поздних или внутренних исходных marks требует отдельной явной карты.

## 3. Регистры, нормы и произвольные входные legs

Реестр A30 использует настоящую A11 `PERIODIC_SOURCE_BINDING`: 256 SITE × 282 шаблона. Для f Choi выбран фактический slot 392, для q Choi — 1340, для q CAR — 1342. Независимая проверка сравнила исходный каталог с B25 и перебрала **139 264** Choi descriptors на f/q и **2 560** CAR descriptors на q: физические little-endian wires, rank-two векторы `G^⊗|r/t>`, исходные коэффициенты и I_RIGHT совпали; extra PF не вставлен. Также проверены все 1372 source completion и общий RAW checkpoint. [Код](audit_a30_mark_registry.py), [результат](A30_MARK_REGISTRY_INDEPENDENT.json).

Пусть `V` — идеальная подготовка до указанного checkpoint, `Vhat` — фактическая на том же canonical WORK-вложении, `||Vhat−V||<=eta_prefix` равномерно на всей свободной `SAM⊗old⊗reference` области. Тогда для любого фиксированного ограниченного checkpoint-оператора `O` и независимых начальных preparation legs `F,B` на этих свободных факторах

\[
\|F^*(\widehat V^*O\widehat V-V^*OV)B\|
 \le2\eta_{prefix}\,\|F\|\,\|B\|\,\|O\|.
\]

Это операторное неравенство сохраняет произвольные комплексные когерентности и запутанность SAM/old, без выбора одного `b`. Его применение предполагает ту же canonical fresh-WORK подготовку; оно не разрешает отдельной входной ноге менять свежий WORK. Два слова могут совпадать на одном подготовленном столбце и отличаться на грязных: точный [fixture](check_canonical_uniform_legs.py) одновременно проверяет эту границу и комплексный запутанный SAM/old пример.

A30 вычисляет `eta_prefix=eta_SITE+eta_Choi+eta_CAR+epsilon_before` через реальные компоненты и фактический prefix replacement count. Точная рациональная проверка даёт `2eta_prefix<2^-3231` на единицу нормы. Поэтому **для каждого именованного mark**, а не как цена всего decoder:

```
u:   <2^-3215       U:   <2^-3214       Psi: <2^-3223
```

`65568>2^16`, поэтому для link использована строгая консервативная степень `2^17`. Для составного `O_f tensor O_q` используется его настоящая произведённая норма; несколько marks/reader errors учитываются отдельно. Ранний mark, действующий только на уже готовую DATA и диагонально на SAM/общий SITE, коммутирует с последующими source-only операциями; mark с недиагональным SAM или общим aux/port так переносить нельзя. На **общей** точке произвольный ограниченный O допускается в приведённой оценке, но его физический reader ещё не построен.

## 4. Что остаётся для H.3/H.5 и исходного источника

H.2/T2 задаёт полный `A_b,t` и исходный `O_t` на каждом требуемом marked frontier, с purifiers, complements и межветвевой когерентностью. H.3 требует соответствующие prefix errors и реальные readers/transport; один общий checkpoint не доказывает внутренние odd-CZ или после-REPORT marks и не доказывает all-column approximation writer на произвольном ранее занятом bank.

H.5 использует f/q moments **совместно** с одной coframe и настоящими PF marks при изменяющейся плотности. Эти source-операнды теперь описаны одновременно на A30 checkpoint, но это не утверждение, что все некоммутирующие rank-two marks имеют одно общее projective measurement. Для физического readout нужны реально допускаемые тесты, их work и цена. Нелинейный средний decoder из §7ar388 требует актуальной полной Jacobian, chart constants, условия invertibility и Neumann correction, включая `eta_mark/s`; соответствующие вычисленные bounds здесь не выданы. Численная малость individual mark errors сама не доказывает полный physical right lift или нулевые независимые source rows.

После checkpoints остаются реальные clock/heat на всех modes, исходный cut, old-prefix/mark/price-reading и конечные сравнения с настоящим `Gamma_s`, `E_tau`, independent programme/input reactions и общая Book03 source map. Никакая прежняя история/цена не отождествлена, `physical_C_closed=false`, `GR_closed=false`.
