# D0 → ОТО: буквальные Golden+CNOT имеют полный вещественный active Lie-span и контролируют C²-источник фиксированной схемы

19.10.2026. **NEW EXACT ANALYTIC GATE-LIE THEOREM + INTEGER n≤7 CHECK + CONDITIONAL TRUE FIRST/SECOND SOURCE STABILITY.** Один текущий Draft PR #334. Физическое действие/правила Book03 не изменены, новый примитив не введён. Итог GR_closed=false.

**Owned входы:** [GoldenOrderInterferometer.gate](../../03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean), [GoldenCoherentMemory.fullStep](../../03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean), [native oldRIGHT admission/no-old-read](A4D_NATIVE_RETAINED_RECORD_ADMISSION.md), [original Golden LEFT / настоящие 4D адреса и ровный источник](A4D_BALANCED_NATIVE_GOLDEN_EXACT_SOURCE_SEAM_LOCAL_TO_VOLUME_MEAN_2026_10_19.md), [точная nonlinear Golden-AF ↔ star-карта](A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md), [complete CAR16 Golden-p Julia](A4D_NATIVE_GOLDEN_P_COMPLETE_CAR_CLOSED_HISTORY_SIX_PHASE_AND_PREPARATION_2026_10_19.md), [реальная неопределённость выбранной физической ActionProtocol-цены](A4D_NATIVE_DYNAMICAL_OWNERSHIP.md).

## 1. Буквальный fullStep, без нового управляемого оператора

Пусть p=φ⁻¹=(√5−1)/2, a=√p, p+p²=1. Исходный Lean владеет
\[
G_p=\begin{pmatrix}a&-p\\p&a\end{pmatrix}\in SO(2),
\qquad
\boxed{\mathrm{fullStep}_p=
\mathrm{CNOT}_{s\to fresh}\,(G_p\otimes I_{fresh})}.
\tag{1}
\]
Все 16 элементов матрицы проверены буквально. Применяя исходный CNOT повторно до архивации fresh-разряда, можно получить G⊗I в **ещё активном** carrier. Использовать уже immutable OLD RIGHT в качестве такого scratch нельзя: это нарушало бы исходный односторонний retained-record интерфейс. Полный результат далее явно предполагает, что уже разрешённые G и CNOT можно размещать на необходимых активных разрядах либо законно маршрутизировать внутри ACTIVE.

**Алгебраическая иррациональность собственного Golden-угла.** При G=exp(θY), Y=XZ=[[0,−1],[1,0]],
\[
\cos2θ=a²-p²=p-p²=\sqrt5-2.
\]
Если θ/π∈Q, то ζ=e^(2iθ) — корень единицы. Тогда t=ζ+ζ⁻¹=2√5−4 имеет все алгебраические сопряжённые в [-2,2]. Но t удовлетворяет t²+8t−4=0, а его второе сопряжённое −4−2√5<-2. Противоречие. Поэтому θ/π НЕ рационально и
\[
\boxed{\overline{\{G_p^m:m\in\mathbb N\}}=SO(2).}\tag{2}
\]
Это теорема об исходном FIXED golden числе, не новый непрерывно программируемый поворот.

## 2. Весь активный so(2ⁿ) следует только из CNOT-сопряжений

На n активных двоичных разрядах положим W_(x,z)=⊗ X^(x_i)Z^(z_i) с x,z∈F₂ⁿ. Здесь X,Z — ВЕЩЕСТВЕННЫЕ матрицы Паули. Тогда
\[
W_{x,z}^T=(-1)^{x\cdot z}W_{x,z},\quad
\operatorname{Tr}(W_{x,z}^T W_{x',z'})
=2^n\delta_{x,x'}\delta_{z,z'}.
\]
То есть все метки x⋅z=1 задают ортогональный базис вещественных антисимметричных матриц. Их ТОЧНОЕ количество
\[
\boxed{\#\{(x,z):x\cdot z=1\}=(4^n-2^n)/2
=\dim\mathfrak{so}(2^n).}\tag{3}
\]
Буквальный CNOT_(c→t) действует сопряжением
\[
x_t\leftarrow x_t\oplus x_c,\qquad
z_c\leftarrow z_c\oplus z_t.
\tag{4}
\]
CNOT + реализуемые ими SWAP порождают GL(n,2). Для произвольных x⋅z=1 существует обратимая A над F₂ с A e₁=x и A^(-T)e₁=z: первый столбец выбирается x, а прочие базисные столбцы выбираются в ker z. Значит все W_(x,z) образуются CNOT-сопряжением одного Y₁=X₁Z₁. Из плотности поворотов G в (2) получаем exp(tW_(x,z)) для ВСЕХ антисимметричных базисных направлений (3). Следовательно
\[
\boxed{
\overline{\langle G_{p,i},\mathrm{CNOT}_{c\to t}\rangle}
\supseteq SO(2^n);
}
\tag{5}
\]
для n≥3 все CNOT имеют det+1 и замыкание в точности SO(2ⁿ). Для n=2 его тождественная компонента есть SO(4), весь замкнутый набор включает det−1.

[Exact integer replay](sources/d0_native_golden_gate_span_2026-10-19/check_literal_golden_cnot_so_generators.mjs) проходит n=1..7 с последовательностью полных рангов 1,6,28,120,496,2016,8128; отдельно проверяет взаимную ортогональность всех 496 real skew-Pauli направлений n=5 и исходную 4×4 матрицу fullStep. Логическое доказательство иррациональности — (2), а не численная оценка угла.

## 3. Следствие для САМОГО исходного полного CAR16 Golden-p Julia

Пусть на исходном реальном 16-мерном exterior CAR действует настоящая ограниченная proper-Lorentz матрица Λ(L), где C=p Λ(L) является strict contraction ||C||<1 на ранее owned chart. COMPLETE вещественный Julia-дилататор
\[
J_C=
\begin{pmatrix}
C&(I-CC^T)^{1/2}\\
(I-C^TC)^{1/2}&-C^T
\end{pmatrix}
\in O(32).
\tag{6}
\]
Путь t↦J_(tC), 0≤t≤1, непрерывен. При t=0 это swap двух 16-мерных блоков с det=(-1)^16=1. Поэтому
\[
\boxed{J_C\in SO(32).}\tag{7}
\]
По (5) на ровно ПЯТИ active qubit-разрядах вся COMPLETE CAR16+fresh-flag Julia-схема может быть **поточечно аппроксимирована** конечным словом только исходных Golden+CNOT (с любой заданной operator-norm точностью), если их active-размещение действительно допускается.

Для любого КОНЕЧНОГО множества уже существующих ACTIVE Golden LEFT адресов q, блоковый оператор
\[
U_{\rm live}=\sum_{q\in Q}|q\rangle\langle q|_{\rm live}\otimes J_{C_q}
+\sum_{q\notin Q}|q\rangle\langle q|\otimes I_{32}
\tag{8}
\]
также является элементом SO(2^(k+5)) после заполнения k активных адресных бит. Следовательно он тоже аппроксимируется одним FIXED finite native G/CNOT-word на всем конечном диапазоне q; это не отдельный gate oracle для каждого q. Все GOOD/BAD дополнения остались. Тензор I_oldRIGHT/ref128 исключает запрещённое old→active чтение.

**Точный scope:** (5)–(8) решают математическую алгебраическую полноту ORIGINAL ALPHABET для ACTIVE real orthogonal controllers, а НЕ literal admission его расстановок, кодирование неизвестного физического поля, native-selected Cost−Info, длину/стоимость compilation, физическое K-node matter/clock, или существование exact конечного word для любого вещественного Julia target.

## 4. Стабильность ПЕРВОГО и ВТОРОГО источника при одном фиксированном слове

Пусть W и U — однажды зафиксированные на всём рассматриваемом поле y вещественные ортогональные матрицы, ||W−U||_op≤ε, E — фиксированный original complete-record эффект с ||E||≤1, а ρ(y) — РЕАЛЬНО ДОПУЩЕННАЯ C² движущаяся ACTIVE плотность состояния. Тогда
\[
p_U(y)=\mathrm{Tr}[\rho(y)U^T E U],\qquad
p_W(y)=\mathrm{Tr}[\rho(y)W^T E W].
\]
Треугольник и trace duality дают
\[
\|U^TEU-W^TEW\|_{\rm op}\le2\epsilon\|E\|_{\rm op},
\]
и в частности
\[
\boxed{\begin{aligned}
|p_W-p_U|&\le2\epsilon,\\
|Dp_W[V]-Dp_U[V]|&\le2\epsilon\|D\rho[V]\|_1,\\
|D^2p_W[V,Z]-D^2p_U[V,Z]|&\le2\epsilon\|D^2\rho[V,Z]\|_1.
\end{aligned}}\tag{9}
\]
Значит совпадение одних конечных вероятностей НЕ нужно заменять заведомо ложным «у аппаратуры нет производной»: у одного field-INDEPENDENT compiled word с настоящей движущейся подготовкой контролируются и все C¹/C² источники через (9). [Independent analytic Golden-source replay](sources/d0_native_golden_gate_span_2026-10-19/check_fixed_word_source_stability.mjs) использует только степени настоящего исходного Golden gate и 21 входной аналитический контроль: фиксированный 22031-Golden-power word достигает ошибки оператора 5.9671×10⁻⁵, а ошибки вероятности/первой и второй производных удовлетворяют (9) с явными запасами. Этот тест — математический sanity-check, НЕ реальная D0-подготовка или whole Book физическая цена.

**Серьёзное ограничение:** конечные слова образуют СЧЁТНОЕ множество вещественных матриц. Любой непрерывный map из связной открытой вещественной field-chart в набор ТОЧНЫХ матриц конечных G/CNOT-слов постоянен: непостоянный связный образ через разделяющий линейный функционал дал бы несчётный интервал внутри счётного множества. Поэтому сам по себе y-dependent выбор РАЗНЫХ конечных слов НЕ даёт точный непрерывный Euler source. Правильный route: ONE fixed word + ACTUAL smooth field-dependent native active input ρ(y) + правильно оплаченная подготовка. Это запрещает подмену подготовки бесплатным полевым oracle.

Если на каждом из O(h^-4) свободных site исходного raw #216 source error от gate approximation ≤2ε_h M_h, M_h=sup||Dρ_h||₁, то original h^-2 raw l1-норма этого канала ≤C ε_h M_h h^-6. Поэтому
\[
\boxed{\epsilon_h M_h=o(h^6)}
\tag{10}
\]
достаточно для ТОЛЬКО этого raw-контроля. Плотность gate-set обеспечивает математическое существование сколь угодно малой ε_h для фиксированного h, но НЕ uniform word-length/work bound, admissible native smooth input, controlled joint roots или весь raw #216.

## 5. Стратегический one-cut consumer — НЕ новое действие

Самый короткий реальный эксперимент продолжения теперь должен происходить на ОДНОМ исходном Golden LEFT активном Role-cell, а не на дополнительном 33-scene→Role адресном proxy:

1. Доказать literal G0 placement оригинальных Golden/CNOT на LIVE ACTIVE bits для CAR16+fresh и чтение собственного full16 coframe/link field-input; OLD RIGHT/ref128 должны остаться неизменными.
2. Для ОДНОГО fixed compiled programme установить реально admissible, C² moving active ρ(e,U,Ψ,prep,clock), все сохранившиеся GOOD/BAD/full128/source и оплату gates/CNOT/controller/work. Сравнить полный FIRST и SECOND источник при точности (9), не заменяя истинный Cost−Info условным Shannon или одним detector-odds.
3. Установить обязательную выбранную полный H+J+R/Book цену именно ЭТОГО исполнения и сравнить на ВСЕХ независимых 16+24+CAR+prep+clock tangent с уже имеющимися Golden-AF ↔ Palatini и balanced J₂/physical volume owners. Силы дополнительных History/Book 32 future +327 odd +326 even не исчезают по умолчанию.
4. Затем consume собственные exact curved roots, Ward, physical refinement, independently owned matter, без GR/claim promotion раньше доказательства.

**Результат:** отсутствие исходного универсального gate alphabet больше НЕ оправдывает новый свободный O(N) примитив; эта возможность снята математически. Но физический источник не определяется одной лишь плотностью схем и остаётся открытым до same-run Cost−Info/field-preparation binding. GR_closed=false.

## Status/repro

- [Golden+CNOT exact integer Lie orbit](sources/d0_native_golden_gate_span_2026-10-19/check_literal_golden_cnot_so_generators.mjs) — literal fullStep, cyclotomic irrationality certificate, all ranks, real n=5 496-generator orthogonality.
- [Fixed-word C² source stability](sources/d0_native_golden_gate_span_2026-10-19/check_fixed_word_source_stability.mjs) — real Golden powers, exact operator/trace derivative inequality control for smooth input.
