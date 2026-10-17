# D0 → ОТО: один полный CAR/Golden-прибор, 128×128 подготовка и вынужденная цена observer-source

**17 октября 2026.** Репозиторий `gvakhrushev/d0_15`; потребитель — существующий Draft PR #334 (`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`). Класс **RESEARCH / EXACT FINITE ONE-INSTRUMENT BORN REPRESENTATION / CONDITIONAL GOLDEN CODE SOURCE / PRECISE NATIVE ADMISSION GATE**. Это не выбор физического действия D0, не новый CORE, не полная ОТО и не доказательство исходного raw `h^{-2}`-терминала.

## 0. Что сцеплено вместо новой коллекции геометрических операторов

В существующем `A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md`, формула (5), для любой положительной метрики `G`, её единичного наблюдателя `u` и лоренцева отражения `g=2u♭⊗u♭−G` установлено точное тождество

\[
R_g=-R_G+2\underbrace{\left[(\operatorname{tr}C)^2-\operatorname{tr}(C^TC)\right]}_{Q_{\rm obs}(C)}-4\operatorname{div}_G(\theta u),
\quad C_{ij}=G(\nabla^G_{e_i}u,e_j),\quad \theta=\operatorname{tr}C.\tag{1}
\]

`C` — все девять spatial 1-jet компонент, включая антисимметрический twist. Ранее `sources/d0_same_golden_car_metric_2026-10-17/RESULT_RU.md` построил на исходном full16 CAR явные симметричные `O_ij=γ_i \widehat γ_j` с `Tr16(O_ij O_kl)/16=δ_ik δ_jl`. Предыдущий Twirl писал `Q_obs=2||Π_iso O(C)||²−||O(C)−Π_iso O(C)||²`. **Здесь вся эта комбинация впервые превращена в два исхода ОДНОГО COMPLETE конечного Born-измерения на буквальном 8×16 system first shell и исходном reference128.**

Вместо 24 отдельных измерений, отдельной 3D Fock-алгебры или «оператора, которому подан Einstein scalar» нужен только один полный Julia-блок с input `A=εO(C)` и одна когерентная selection в его реальном выходе. Для этого readout две неотрицательные probability являются строго различимыми выходами одного прибора; третий outcome хранит все blank cases. Весь источник и коэффициенты вычисляются точно, не из малого `C`.

## 1. Исходный носитель: 8×16 материальная оболочка и ВСЕ 128 reference columns

Пишем `H_s=R^8⊗Λ*R^4`, `dim H_s=128` (восемь first-shell momentum, **все** 16 exterior grades) и существующее `H_r=R^128`. В canonical maximally-entangled Schmidt frame той же условной v8 подготовки:

\[
\left|\Omega_{128}\right\rangle=\frac1{\sqrt{128}}\sum_{k=0}^{7}\sum_{a=0}^{15}|k,a\rangle_s\otimes|k,a\rangle_r,
\qquad \operatorname{Tr}_r |\Omega\rangle\langle\Omega|=I_{128}/128,
\quad\operatorname{Tr}_s|\Omega\rangle\langle\Omega|=I_{128}/128.\tag{2}
\]

Это не произвольный 16-to-128 fake purification: **обе маргинали имеют полный ранг 128**. На системе действует один и тот же исходный 16-CAR оператор в восьми momentum blocks:

\[
\mathsf O(C)=\sum_{i,j=1}^3 C_{ij}\gamma_i\widehat\gamma_j,
\qquad A_\varepsilon(C)=\varepsilon(I_8\otimes \mathsf O(C)).\tag{3}
\]

Поскольку `Tr16 O(C)²/16=||C||_F²`, `||O(C)||op≤4||C||F`. На любой компактной smooth coframe/observer chart с `||C||F≤K` фиксированное `0<ε<1/(4K)` даёт selfadjoint contraction. Это **математический chart bound**, не вывод ε из физической подготовки. В независимом диагностическом скрипте используется фиксированное ε=1/16; все общие формулы ниже выполняются для любого указанного ε.

Для одного блока k введём нормированное когерентное состояние

\[
|\iota_k\rangle=\frac1{4\sqrt3}\sum_{a,b=0}^{15}\left(\mathsf O(I_3)\right)_{ba}|k,b\rangle_s\otimes|k,a\rangle_r,
\quad\mathsf O(I_3)=\mathsf O_{11}+\mathsf O_{22}+\mathsf O_{33},
\quad\Pi_{\rm coh}=\sum_{k=0}^{7}|\iota_k\rangle\langle\iota_k|.\tag{4}
\]

Из точных CAR trace relations получаем `<iota_k|iota_l>=δ_kl`, а `Π_coh` — проектор ранга8 на **том же** system×reference. Он сохраняется при совместной смене пространственной рамки; никакой выбранной пространственной оси в нём нет.

## 2. Одно complete Julia-измерение, три взаимоисключающих исхода

Определим `S=\sqrt{I-A_ε²}` на system и полный ортогональный 2-port gate

\[
U_\varepsilon=\begin{pmatrix} S&-A_\varepsilon\\ A_\varepsilon&S\end{pmatrix}.
\tag{5}
\]

Это **та же Julia block grammar**, что у native `J(A)=[[A,S],[S,−A]]`, а не дополнительный тип матрицы:

\[
U_\varepsilon=
\begin{pmatrix}-I&0\\0&I\end{pmatrix}
J(A_\varepsilon)
\begin{pmatrix}0&I\\-I&0\end{pmatrix}.\tag{6}
\]

Требуется физический допуск **входа** `A_ε(C)` и двух port-sign permutations; формальная Julia-реализация сама по себе его не доказывает. После (5) измеряем:

- `coh`: выходной порт 1 И `Π_coh`;
- `orth`: выходной порт 1 И `I−Π_coh`;
- `blank`: выходной порт 0, независимо от полного системы/reference;

Все projector outcomes остаются в удержанной записи, включая complement. Нет постселекции и сброса old tape. Прямые вычисления на **pure full-rank128 Schmidt state**, без полного представления `16384×16384` оператора, дают **точно**

\[
\boxed{P_{coh}=\frac{\varepsilon^2}{3}(\operatorname{tr}C)^2},\qquad
\boxed{P_{orth}=\varepsilon^2\left(\operatorname{tr}C^TC-\frac{(\operatorname{tr}C)^2}{3}\right)},\qquad
\boxed{P_{blank}=1-\varepsilon^2\operatorname{tr}C^TC}.\tag{7}
\]

Здесь `Pcoh+Porth+Pblank=1`, и все три probabilities неотрицательны. Средний квадратный trace of the original full16 CAR используется, а не произвольный eigenbasis oracle. `orth` включает все невидимые пространственные shear и twist, без исключения grade или reference.

**Новая одноносительная relative-source identity:**

\[
\boxed{2P_{coh}-P_{orth}=\varepsilon^2 Q_{obs}(C),\qquad
R_g=-R_G+\frac2{\varepsilon^2}(2P_{coh}-P_{orth})-4\operatorname{div}_G(\theta u).}\tag{8}
\]

В отличие от предыдущих «геометрических эффектов», эти два члена — **Born probabilities двух конкретных disjoint outputs одного законченного измерения**. Это ещё не тождество его полной реально выбранной `Cost−Info` цене.

### 2.1. Коэффициенты вынуждены внутри полного трёхисходного типа

Любой *field-independent* centered linear score `a Pcoh+b Porth` имеет

\[
aP_{coh}+bP_{orth}=\varepsilon^2\left[b\,||C||_F^2+\frac{a-b}{3}(\operatorname{tr}C)^2\right].\tag{9}
\]

Чтобы он совпал с `ε²[(tr C)²−||C||²]` **для всех** девяти независимых направлений, обязательно и достаточно:

\[
\boxed{b=-1,\qquad a=2.}\tag{10}
\]

Это настоящее class-internal **forcing of the relative score**, не утверждение `M1Forced` всей программы. В общей пространственной размерности d аналогичные веса `(d−1,−1)`; при d=3 именно `(2,−1)`.

Полный первый источник, в том числе moving coframe/observer/connection через настоящий `dC`, равен

\[
\boxed{d(2P_{coh}-P_{orth})
 =2\varepsilon^2\,[\theta\,\operatorname{tr}(dC)-\operatorname{tr}(C^T dC)]}\tag{11}
\]

при field-independent ε. Для moving ε дополнительный член `2εdε Qobs` обязателен. Полная scalar Lorentz source follows from differentiating (8), including `dR_G`, `d\sqrt{|g|}`, `d(\operatorname{div})` and `dC`; при retained boundary её flux не стирается без условий.

Если одновременно менять материальную/reference подготовку, сам `Πcoh`, метрику скалярного произведения либо controller, возникают их реальные `dρ` и `dΠ` источники. (11) имеет именно **совместную рамку**, в которой эти purely representational terms сокращаются; замораживание половины этих данных — другая физическая задача.

## 3. Буквальный Golden code 0/10 поставляет относительные целые веса — при явном маршрутизаторе исходов

Существующий D0 prefix code `F=0` имеет длину1, `R=10` имеет длину2. На **полном prefix-free cut**, где F останавливается, а R даёт ещё один ход, листья:

\[
\boxed{F=0\;(C=1),\quad RF=100\;(C=3),\quad RR=1010\;(C=4).}\tag{12}
\]

Их золотая эталонная масса **точно нормирована**:

\[
\mu=(p,p^3,p^4),\qquad p+p^3+p^4=1,\quad p=\varphi^{-1}.\tag{13}
\]

Сопоставим complete readouts `(coh,blank,orth)` именно с `(F,RF,RR)`. Тогда при фактических вероятностях (7) и **без произвольных весов исходов**:

\[
\boxed{\mathbb E_q C-3=P_{orth}-2P_{coh}=-\varepsilon^2 Q_{obs}.}\tag{14}
\]

Число 3 — действительная длина **пустого** слова RF, поэтому это centered code price, не добавленный полевой counterterm. В данной branch-grammar `(1,3,4)` фиксированы; равенство (14) действует для любой нормированной `(qcoh,qblank,qorth)`. Равно как (10), это **точная возможность** реализовать наблюдательский вклад через существующий двухбуквенный код без новых физических констант.

Но нужное сопоставление исходов **НЕ следует** только из `p+p²=1`. У исходного неконтролируемого Golden splitter шансы трёх листьев равны (13), а не (7). Чтобы (7) попадали в те же literal `F/R` histories, original programme должен реально исполнять state-dependent branching, coherent old-reference cut, conditional stopping и полную стоимость его контроллера. Этот *outcome-labelled morphism* — теперь один точный admission target.

### 3.1. Отрицательный контроль против слишком лёгкого «M1 выберет этот маршрут»

Даже буквальное совпадение кодовых коэффициентов НЕ доказывает оптимальность выбранного назначения листьев. Когда `ε=h/16→0`, `Pblank≈1`, а `Pcoh,Porth=O(h²)`. Если разрешено **слепо переназначать** code words по максимальной частоте, более дешёвое назначение отправляет **blank** в короткий `F` длины1, а `coh` в `RF` длины3. Оно снижает ожидаемую стоимость **строго на**

\[
oxed{2(P_{blank}-P_{coh})>0}	ag{14a}
\]

для малых `h`. Поэтому ни одна из формул (12)–(14) не даёт reductio, что M1 или простой Huffman/MDL автоматически выбирают нужный физический router. Нужна *вынужденная operational identity*: какие исходы именно **прямой ход**, **возврат**, **сохранённое сравнение**, и почему их перекодировка физически меняет или не меняет сам опыт. Если исходы можно бесплатно переставлять, нужная цена не минимальна. Это выполненный hostile control физической селекции, а не повод стереть положительное вероятностное тождество (8).

### 3.2. Cost−Info нельзя заменить одним centered Code

Строгий отрицательный контроль на **этом же** трёхисходном приборе. Если сделать дополнительное SAME-history физическое отождествление `w_i=q_i`, `Info_i=log_φ(q_i/μ_i)` при `μ_i=p^{C_i}`, то

\[
\mathbb E_q(C-Info)=H_\varphi(q), \tag{15}
\]

а **не** `(E_q C−3)`. Для `C(t)=tC_*`, где обе выходные интенсивности ненулевые, обозначим `a=Pcoh(1)>0`, `b=Porth(1)>0`. Тогда `q(t)=(a t²,1−(a+b)t²,b t²)` и

\[
\boxed{H_\varphi(q(t))
 =\frac{2(a+b)}{\log\varphi}\,t²\log\frac1{|t|}+O(t²),\qquad
E C-3=-\varepsilon² t²Q_{obs}(C_*).}\tag{16}
\]

Первая функциональная зависимость не имеет конечной второй вариации в `t=0`, вторая имеет строго конечный, допускающий оба знака Hessian. Следовательно **literal normalized classical branch surprisal Info не может автоматически выбирать нужную Lorentz source** на этой семье. Нужен другой уже внутренне выводимый архивный Info/cut или настоящая ненормированная стоимость, которая компенсирует всю нетривиальную source, а не присвоенное вручную вычитание.

## 4. Конкретный исходный h/16 и сильный twisted контроль

В `A4D_RETAINED_HISTORY_CAUSAL_SOURCE.md` native Julia blank coefficient уже имеет вид `A=hD_h/16`, и retained single-label probability имела характерный множитель `1/256`. **Математическая** специализация той же амплитудной нормировки к наблюдательскому билейнеру `D_obs=O(C)` использует `ε_h=h/16`. Тогда точно на любом конечном h, пока `h||O(C)||<16`,

\[
\boxed{h^{-2}(2P_{coh}-P_{orth})=\frac1{256}Q_{obs}(C),\qquad
h^{-2}d(2P_{coh}-P_{orth})=\frac1{256}dQ_{obs}.}\tag{17}
\]

Это точное совпадение **структурной нормы выходов** с прежним Julia-`1/256` owner, а не доказательство, что его конкретные 32 label/CAR words уже реализуют `D_obs`. Clock variations с `dh≠0` к (17) не подходят без полной chain rule. Прямое h²-чтение ещё не доказывает original h^-2 unweighted raw sum: в 4D суммирование по `h^-4` узлам добавляет **четыре степени**. Например, если ошибки 10 metric first-source rows оценены поузлово `O(h^8)` в одной исходной chart, то normalized raw `h^-2 Σ_x` error `O(h²)`; такого uniform estimate для данного proposed readout ещё нет.

На действительной геометрической twisted-field семье из предыдущего владельца `G=I`, `u=(cos kx,0,sin kx,0)` получаем в подвижной spatial frame `C_12=k`, все остальные C_ij=0 и

\[
Q_{obs}=-k²,\quad Pcoh=0,\quad Porth=\varepsilon² k²,
\quad 2Pcoh-Porth=-\varepsilon²k²,\quad R_g=-2k²,\quad \partial_kR_g=-4k.\tag{18}
\]

При диагностическом ε=1/16 и k=1 ортогональный event имеет настоящую вероятность `1/256`; blank вероятность `255/256`. Никакой отдельно введённой четырёхмерной кривизны в этом witness нет. Для generic C скрипт проверяет точную source on a noncommuting 16-CAR field jet, а не только diagonal/twist.

## 5. Физическая граница: нужен один действительный старый-reference coherent cut

Проверка на принадлежность **уже ограниченному native one-way class** из `A4D_NATIVE_FEASIBLE_GAIN_AND_ACTION_SOURCE.md`.

Сама projection `Πcoh` **не** invariant under translation of a low old-reference bit: на каждом reference16 блоке `|iota_k>∝vec(T)`, где `T=O(I3)` — обратимая 16×16 матрица. Если old-bit flip S≠±I оставлял его rank-one line invariant, то `vec(T S^T)=λ vec(T)` влекло бы `S^T=λ I` — противоречие. Поэтому

\[
\boxed{[\Pi_{coh},I_s\otimes S_{\rm old}]\ne0.}\tag{19}
\]

Любой old-record-blind single-port projective effect вида `F_active⊗I_old` commutes with every old translation. Если one-way U commutes with them, то его сопряжённый effect тоже commutes. Следовательно (19) **исключает реализацию именно данного coherent sub-event как label-blind одноходового порта с одним таким старым pointer/cut**. Это scoped obstruction, а не глобальная теорема невозможности: outcome-labelled полные POVM, последовательные возвраты, реальные старые-reference readdressing operations могут лежать за пределами restricted class. Там требуется собственный физический admission и вся цена.

Четыре оставшиеся стрелки, без нового action:**

1. Доказать **сам native matrix-input** `h O(C)/16` из физически разрешённых coframe/observer/connection history words, включая field/source jets, а не только то, что CAR-алгебра содержит эти девять матриц.
2. Доказать допустимую **coherent reference outcome** (4) на полном128, не молчаливый old-bit projector и не scalar oracle.
3. Доказать реальный **router** `(coh,blank,orth)↔(F,RF,RR)` и complete code / Info / all failures/controller overhead, с действительной физической source, не просто eq.(14).
4. Совместить с уже owned Golden `R_G` geometric reading и actual matter source в **одном** full action, затем построить exact joint-critical nonflat refinement and prove original ten-slot raw `h^{-2}` comparison. Matching source значения на одной twisted chart недостаточно.

Ни одна из этих стрелок не может заменяться догадкой «раз значения совпали, M1 автоматически выбрал программу». Но после (7), (12) и (14) **не требуется больше искать произвольный tensor/score/coefficients**: следующий решающий proof находится ровно на outcome-labelled physical admission/cost interface существующих Golden/CAR операций.

## 6. Сильная положительная сцепка: весь observer-source входит в ОДИН существующий центральный AF-ценообразователь

Предыдущий §3 доказал возможность относительного `Cost` на трёх исходах, но §3.2 установил реальное препятствие: если сначала измерить `(coh,blank,orth)`, а потом применить **отдельно ко всем трём** нелинейный Shannon/KL score, появится лишний логарифмический источник. Применяем исходную стратегию `A4D_CENTRAL_RECORD_VARIATIONAL_EQUIVALENCE.md`: **когерентное объединение полных амплитуд ДО одной terminal AF price**, а не сумма независимо оценённых исходов. Следующий результат — точный конечный операторный компилятор этого конкретного `Q_obs`, а не внешний oracle его значения.

### 6.1. Сам Golden alphabet даёт три РАВНОВЕСНЫХ управляющих истории

Берём **исходный cut accumulated cost ≥3**, то есть минимальные префиксы, достигшие стоимости 3. В неизменной грамматике F=0 стоимости1 и R=10 стоимости2 его полный prefix-free набор:

| История | Literal bit word | Стоимость | Golden масса | Действие на полном выходе |
|---|---|---:|---:|---|
| `FFF` | `000` | 3 | `p³` | `−W_coh` |
| `FR` | `010` | 3 | `p³` | `−W_coh` |
| `RF` | `100` | 3 | `p³` | `+W_orth` |
| `FFR` | `0010` | 4 | `p⁴` | `I` |
| `RR` | `1010` | 4 | `p⁴` | `I` |

**Проверено точно:** `3p³+2p⁴=1`; эти пять слов покрывают все исходы cut, включая две pending/remainder истории. Более того, literal **стоимость собственно управляющего Golden слова**, пока контроллер не меняет ярлык его истории, имеет точное ожидание

\[
\boxed{\mathbb E_\mu C_{\rm control}=3(3p^3)+4(2p^4)=7-6p,\qquad d_X \mathbb E_\mu C_{\rm control}=0.}\tag{22a}
\]

Значит, фиксированная плата именно за **эти пять исходных кодовых слов** не создаёт скрытого observer-source. Это НЕ доказательство бесплатного условного исполнения `−Wc,+Wo`, хранения новых controller flags, подготовки reference128 или их поле-зависимого decoder/completion; такие издержки могут давать дополнительный настоящий источник и должны быть сохранены.
 Их исходная coherent state имеет коэффициенты `p^(3/2),p^(3/2),p^(3/2),p²,p²`, без подготовленного fair `1/√3` и без дополнительного значения вероятности. Два выбранных `−` — те же математические центральные знаки, которые D0 имеет в `Q₈`; физический допуск их conditional placement нужно отдельно доказать.

Пусть на **готовой полной wavefunction** после первого Julia-прибора §2 определены два оператора:

\[
E_c=|1\rangle\langle1|_{port}\otimes\Pi_{coh},\qquad
E_o=|1\rangle\langle1|_{port}\otimes(I-\Pi_{coh}),
\]
\[
\boxed{W_c=I-2E_c,\quad W_o=I-2E_o.}\tag{22}
\]

Это две самосопряжённые **унитарные инволюции**, без новой переменной матричной функции: `W²=I` и все остальные исходы остаются в состоянии. Пусть `|Ψ_C〉=U_ε(C)(|0〉port⊗|Ω_128〉)`. Тогда

\[
\langle\Psi_C|W_c|\Psi_C\rangle=1-2P_{coh},
\qquad\langle\Psi_C|W_o|\Psi_C\rangle=1-2P_{orth}.\tag{23}
\]

Контроллер из таблицы — **одна полная block-diagonal ортогональная операция на пяти исходных Golden-history секторах**; ни один из них не выбрасывается. Обозначим `|χ〉` нормированную пятисловную золотую seed из таблицы и `|α_C〉=|χ〉⊗|Ψ_C〉`, `|β_C〉=U_control|α_C〉`. Оба состояния нормированы на одном полном носителе. Прямое вычисление, а НЕ ввод desired scalar как control:

\[
\begin{aligned}
h(C):=\operatorname{Re}\langle\alpha_C|\beta_C\rangle
 &=p^3[-2\langle W_c\rangle+\langle W_o\rangle]+2p^4\\
 &=1-4p^3+2p^3(2P_{coh}-P_{orth})\\
 &\boxed{=1-4p^3+2p^3\varepsilon^2 Q_{obs}(C).}
\end{aligned}\tag{24}
\]

**Ресурсное уточнение.** Нормировка `1/√3` в записанном в (4) векторе **не требует нового иррационального угла в самой матрице измерения**. На каждом reference16-блоке `v=vec(O(I_3))` имеет целочисленные CAR-координаты и `v^Tv=48`, поэтому

\[
\boxed{\Pi_{coh}^{(k)}=vv^T/48,\qquad W_c^{(k)}=I-vv^T/24.}\tag{23a}
\]

Это точная **рациональная Householder reflection** (`W_c²=I`) на прежней аппаратной Hilbert space. Математически не нужен отдельный unitary-compiler с `√3` в угле смешения. Но деление на24 и возможность **адресовать такую старую reference projection** ещё не доказаны исходной ring/gate грамматикой D0: rational matrix existence НЕ является native implementation.

**Нетривиальное отличие от предыдущей попытки:** геометрическая комбинация (24) кодируется **как один когерентный overlap двух полностью нормированных записей**, а не сначала распознаётся как probability и подаётся в новый прибор как scalar input. Блоки `−W_c,−W_c,+W_o,I,I` — настоящие матрицы на уже существующей системе × reference128 × retained labels, независимые от заранее вычисленного `Q_obs`. Вся field dependence поступает через `O(C)` первого Julia-блока §2. Не используются новые Fock-виды, плакеттный source-oracle или вещественный регулируемый score.

**Оговорка:** доступность `E_c`, `E_o`, conditional Q₈ sign, исходной coherent пятисловной superposition и controller source внутри реально допущенного D0 двигателя НЕ доказана. Это физически решающая, теперь одна и точная primitive-admission/price задача.

### 6.2. Передача в уже существующую terminal AF-price без нового лагагранжиана

В `A4D_CENTRAL_RECORD_VARIATIONAL_EQUIVALENCE.md` §4 исходный Golden interference, затем восемь прямых букв, задают для **любого** настоящего real overlap `h∈[-1,1]` единственный central effect

\[
z=p^2+2p^{12}h.\tag{25}
\]

Подстановка именно **вычисленного полного** (24), без scalar oracle и без нового свободного `λ`, даёт

\[
\boxed{z(C)=p^2+2p^{12}(1-4p^3)+4p^{15}\varepsilon^2Q_{obs}(C),}\tag{26}
\]
\[
\boxed{dz[V]=4p^{15}\varepsilon^2\,dQ_{obs}[V]}.\tag{27}
\]

При `C=0`: `h_*=1−4p³≈0.05572809`, `z_*≈0.38231215` — **строго внутри** прежнего проверенного окна `[3/8,25/64]`. На любой bounded compact observer chart и достаточно малом фиксированном ε окно сохраняется, так что старый owner даёт `2/5<a_n(z,σ)<5/2` для **любого** ранга нормированной AF-подготовки `σ`. Следовательно для неизменной физической программы старой terminal AF-price, *если её реальная полная стоимость допускает данный upstream control без дополнительного source*, 

\[
\boxed{d_C A_{AF}(C,\sigma)
 =4p^{15}\varepsilon^2 a_n(z(C),\sigma)\,dQ_{obs}[C],\qquad a_n>0,}\tag{28}
\]

при фиксированной `σ`, а после настоящей stationary preparation elimination тот же reduced envelope имеет эту геометрическую производную. `a_n` — **один общий положительный множитель на ВСЕ девять observer rows**, не девять подобранных coupling и не только second Taylor coefficient. Именно это делает нелинейный source гладким и устраняет логарифмический `t²log|t|` из §3.2: log-терминал получает центральное **внутреннее** значение `z_* > 0` и зависит от C только через уже сложенный invariant `Q_obs(C)`.

Дальнейшая уже известная геометрическая композиция требует включить **в тот же центральный overlap до AF price** операторные источники `−R_G`, `2Q_obs` и полную native matter/measure contribution. Суммировать отдельные AF цены `A(R_G)+A(Q_obs)` НЕЛЬЗЯ: тогда на разных строках появятся разные множители `a_n`. Теорема (28) закрывает математический observer-block input/variation к существующей central programme, но не утверждает, что full physical Cost−Info всей новой последовательности **равно** старому terminal AF score. Controller preparation, coherent cut, code/Info и history reference должны быть выведены из исходных primitive laws.

### 6.3. Почему это действительно сокращает физическую задачу

Раньше требовалось физически *выбрать* нефизическую скалярную комбинацию `Q_obs` между двумя вероятностями, затем *снова* управлять другим прибором её вычисленным значением. (24)–(28) устраняют эту двойную селекцию. Не нужен отдельный `√3`-угол score-Julia (сама coherent projection имеет рациональную матрицу `vvᵀ/48`, но её native preparation/cut всё ещё открыт), ни detector, которому подан скаляр Lorentz curvature, ни постселектированные средние: **три равномассовые исходные Golden histories, две настоящие отражающие матрицы и один terminal AF flag**.

Физическая точка сужена: доказать, что **именно этот** conditioned complete-record controller принадлежит реально допустимому D0 процессу, а его **полная оплаченная цена** после реальной подготовки/сравнения имеет источник (28) без пропущенного field-dependent overhead. Если да, для observer-блока существующая AF теорема сразу передаёт необходимые Euler zero sets и reduced Hessian без дополнительных локальных тепловых приближений. Если нет — найден конкретный отсутствующий native morphism, а не «неясный выбор Einstein-тензора».

## 7. Воспроизведение и границы проверки

`check_observer_born.py` дополнительно проверяет рациональную Householder projection (23a) без √3 в её матричных entries. Он строит исходные CAR creation/annihilation 16×16, проверяет каждый из девяти операторов `γ_i hatγ_j` и все их trace-пары; считает три outcomes из чистого 128×128 Schmidt state на original 8×16 momentum/form shell и полного reference128, а не из подменённой 16/128 модели; проверяет source на некоммутирующих джетах, unique `(2,-1)`, code lengths `(1,3,4)`, exact two-stage `p+p³+p⁴=1`, нормировку `h/16`, label-blind translation obstruction и Shannon hostile control. Проверки также включают точную пятисловную Golden-history coherent aggregation (24), controller reflections, native central `z` из (25), его полную first source и проверку положительного AF-window. Проверки включают чистый 128-Schmidt и diagnostic mixture с full-rank reference marginal как независимые две подготовки. Одновременно строится нетривиальный32×32 original Julia и constant-port readdressing. Всё это **контроли алгебраических теорем**, а не native gate selection proof.

Запуск из repo root:

```sh
python3 02_REGISTRY/research/sources/d0_observer_born_three_event_2026-10-17/check_observer_born.py
python3 -O 02_REGISTRY/research/sources/d0_observer_born_three_event_2026-10-17/check_observer_born.py
```

Числовые fixtures и точные матрицы самостоятельны; старый Lean, дорогой L8 roots, main CI, original raw refinement не перепроверялись. GitHub PR #334 остаётся `Draft / IN_PROGRESS`.
