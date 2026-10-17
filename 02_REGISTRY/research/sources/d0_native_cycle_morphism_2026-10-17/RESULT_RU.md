# D0 → физический выбор действия: точная native-петлевая алгебра, знаковое препятствие и полный source

**17 октября 2026.** Репозиторий `gvakhrushev/d0_15`. Потребитель — существующий Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334), `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`; дальнейший gate `MORPH_NATIVE_RETAINED_HISTORY_TO_V8_ACTION` → полная Cost−Info цена → полные coframe/link/observer/matter источники → нелинейная ОТО и исходный `h^-2` refinement.

**Статус: RESEARCH / EXACT FINITE THEOREMS + NARROW NO-GO.** Ни физическая селекция `H+J+R`, ни выбор clock/fugacity, ни GR не доказаны. Использованы **действительные** данные полностью записанного K(9,11,13)-процесса; дополнительно проверена универсальная конечная `P,U`-формула полного отклика. Никаких новых Fock-мод, графов, спектральных функций, mass scale, калибровок, BOOK/CLAIM или Euler-уравнений не вводится.

**Зафиксированные источники:**

- `02_REGISTRY/research/A4D_NATIVE_CYCLIC_HISTORY_PRICE_PREPARATION.md` (Git blob `92a8cf2f581c6358ba2a1dfffec7dd085196a0a7`): полный допустимый замкнутый recorded scene word, `J,C,P,U`, полный positive feedback `F`, reduced 33-label transport и точная детерминантная формула. Это **математическая реализация** declared all-walks/reading interface, а не доказательство его физического выбора.
- `02_REGISTRY/research/A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md` (Git blob `b90fe7d93489b7a3616bb0d7c8740cb975583e78`): полное пространство аддитивных стоимостей на actual scene histories; composition alone leaves edge costs free.
- `02_REGISTRY/research/A4D_GOLDEN_DETERMINANT_COMPILER.md` (Git blob `2b45f37068a72cb6ada362363ff5c3e3ac79de22`): отдельная exterior-dilation реализация детерминанта; в данном пакете она **не используется** как носитель.
- `02_REGISTRY/research/A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md`, `A4D_NATIVE_PARTITION_CORRECTED_BRANCH_INFORMATION.md`: условные pathwise Cost−Info/normalizer identities; никакой выбор полной `Info` не объявляется.
- `02_REGISTRY/research/sources/d0_native_action_selection_2026-10-16/RESULT_RU.md`: предыдущая точная семантика `P_surv,P_blank`, логарифмический source, конкурирующее rooted-repeat чтение.

## 1. Native полный recorded carrier, а не придуманная матрица

Сцена — буквально полный трёхдольный граф `K(9,11,13)`, `33` различимые метки, `359` неориентированных и `718` ориентированных рёбер. Для `i` в зонах `(9,11,13)` исходящие степени `d_i=(24,22,20)`.

Для конкретности алгоритм Hierholzer **конструирует три завершённых замкнутых слова** длины `L=1436` из целых симметричных чисел переходов

\[
N_1^{(0)}=2A_0,\quad N_1^{(+)}=2A_0+E,\quad N_1^{(-)}=2A_0-E,
\quad E_{0,9}=E_{9,0}=1,\quad E_{0,20}=E_{20,0}=-1.
\]

Каждое слово посещает все 33 метки, сохраняет **все** 1436 переходов, равенство входящих и исходящих степеней и не удаляет отказавшие/повторные маршруты. Три отдельных слова — discrete realized controls, **не** непрерывное поле в одном фиксированном carrier. Точка `t=0` и `t=±1/2` соответствуют `N_1=2(A_0+tE)`; предел рациональных частот `t=r/m`, `m` чётно, получен прежним владельцем.

Для произвольного такого word:

\[
J_{ti}=1_{w_t=i},\quad D=J^T J,\quad C=D^{-1}J^T,\quad P=JC,
\quad U=\text{сдвиг всей записанной ленты},
\]
\[
T=CUJ=D^{-1}N_1,\quad T^\dagger_D=D^{-1}T^TD,\quad
F_{\rm full}=PU^T(I-P)UP=J\,\underbrace{(I-T_D^\dagger T)}_{F_{33}}\,C.
\tag{1}
\]

При симметричной частоте `N_1=N_1^T` имеем detailed balance, `T_D^†=T`, поэтому `F_{33}=I-T²`. Jensen для стохастического `T` в стационарной положительной `D`-паре даёт `0≤F≤I`. Смена на ортонормированные labels есть similarity `\widehat T=D^{1/2}TD^{-1/2}`; внутри одной зоны `F_{ij}` остаются буквально такими же. Полный `L`-мерный feedback сохраняет все `L−33` нулевых направлений; они дают множители 1 детерминанту, но **не удаляются из полного heat trace**.

На базовой записи уменьшенный quotient по зонам равен

\[
T_{zones}=\begin{pmatrix}
0&11/24&13/24\\9/22&0&13/22\\9/20&11/20&0
\end{pmatrix},\qquad
\det(\lambda I-T_{zones})=(\lambda-1)(\lambda^2+\lambda+39/160).
\]

На ортогональном 30-мерном пространстве `T=0`, на quotient собственные числа `1,-1/2±\sqrt{10}/40`. Следовательно `F` имеет rank32, одну нулевую собственную величину и 30 единичных; `Tr F=2519/80`. Например, всю базовую детерминантную функцию можно записать без новых мод:

\[
\boxed{\det_{33}(I-zF)=(1-z)^{30}
\left(1-\frac{119}{80}z+\frac{14001}{25600}z^2\right).}
\tag{2}
\]

Это **точное следствие уже имеющегося recorded word**, не новая physical selection.

## 2. Основной контрсертификат: отрицательный цикл при положительном F

Возьмём три **различные** вершины `0,1,2` первой зоны размера 9. У них 11 общих соседей степени22 и13 общих соседей степени20. Поэтому для любых различных таких `i,j`:

\[
(T^2)_{ij}=\frac{1}{24}\left(\frac{11}{22}+\frac{13}{20}\right)=\frac{23}{480},\qquad
F_{ij}=-\frac{23}{480}.
\]

Для буквального замкнутого маршрута `0→1→2→0` коэффициент его вклада в `Tr F³` равен

\[
\boxed{w(0,1,2)=-\left(\frac{23}{480}\right)^3
=-\frac{12167}{110592000}<0.}\tag{3}
\]

Это отрицательный вес в положительном операторе `0≤F≤I`; `Tr F^n≥0` для всех `n` не означает неотрицательности каждого **матричного** пути. Знак (3) не меняется при допустимых rephasing `F_{ij}→s_i^{-1}F_{ij}s_j` (фазы сокращаются по замкнутой петле). Произвольная нелокальная смена basis могла бы устранить отрицательные entry-weight, но **изменит native label-readout**, а не будет просто rephasing этих записанных меток.

**Точное ограничение:** невозможно интерпретировать каждый отдельный закрытый **labelled** цикл как событие с вероятностью `c_γ∏F_{ij}`, `c_γ>0`, при сохранении literal matrix-element weights (3). Это не no-go для физической когерентной/знаковой амплитуды, а no-go для её молчаливой подмены положительными вероятностями. В частности, «циклы существуют в записи» **не** вынуждает их подписанную статистическую сумму.

Отрицательный контроль силён именно в третьем порядке: если заменить offdiagonal знаки на абсолютные значения в native 3×3 principal block, `Tr F` и `Tr F²` останутся равны прежним, но

\[
\operatorname{Tr}(F_{\rm abs}^3)-\operatorname{Tr}(F_{\rm native,3}^3)
=12(23/480)^3\ne0.
\tag{4}
\]

Следовательно проверки только одного возврата и второго момента пропустили бы нарушение.

## 3. Не только знак: ненулевой точный source на реализуемой frequency family

Используем ту же **действительную** симметричную частотную вариацию `A(t)=A_0+tE`. Для `|t|<1` все веса положительны, любой рациональный `t=r/m` при `m` чётно и `|r|<m` точно реализуется целым Eulerian word. На интерполированной 33-меточной паре

\[
D(t)=\operatorname{diag}(A(t)\mathbf 1),\quad T(t)=D(t)^{-1}A(t),\quad F(t)=I-T(t)^2.
\]

Выбранный цикл остаётся отрицательным при `t=±1/2`, а его **первый источник** при нуле строго отличен от нуля:

\[
\boxed{\frac{d}{dt}\,[F_{01}F_{12}F_{20}]_{t=0}
=\frac{199433}{267632640000}>0.}\tag{5}
\]

Полный reduced finite response при любой фиксированной `0<z<1` обязан включать **движущуюся плотность посещений**:

\[
\dot T=D^{-1}(E-\dot D\,T),\quad
\dot F=-(\dot T T+T\dot T),
\quad\boxed{\dot J=M z\operatorname{Tr}[(I-zF)^{-1}\dot F]}.\tag{6}
\]

Для **того же** `M=128`, `z=2^{-20}` (здесь это заданные калибровки v8, **не** их физическое получение) воспроизведено точное число

\[
\boxed{\dot J(0)=\frac{428303175104}{5676403977829946735}
\approx7.545325822066273\cdot10^{-8}\ne0.}\tag{7}
\]

Независимая проверка вычисляет (6) двумя несводимыми до ручной подгонки представлениями:

\[
\det(I-zF)=\frac{\det[(1-z)D+z A^TD^{-1}A]}{\det D},
\quad d\log\det(I-zF)=d\log\det\mathcal N-d\log\det D.
\tag{8}
\]

Они совпали точно при `z=1/8` и `2^{-20}`. **Замораживание `d(D^{-1})` отвергается** и даёт другой source. Важно: (5)–(8) — derivative **интерполяции частот полностью записанных слов**, не якобы infinitesimal Euler variation одного discrete word, не физический link/coframe source и не решение ОТО.

### Общий source при реальном движении P и U

В отдельном rational `4×4` native-feedback control положены `P²=P=P†`, `U†U=I`, `Q=I−P`, `F=PU†QUP`; выбираются **не зависящие друг от друга** интегрируемые tangents `dot P=[G,P]`, `dot U=HU` с `G†=−G`, `H†=−H`. Правильный пятичленный source:

\[
\boxed{\begin{aligned}
\dot F={}&\dot P U^\dagger QUP
+P\dot U^\dagger QUP
-PU^\dagger\dot P UP\\
&+PU^\dagger Q\dot U P
+PU^\dagger QU\dot P.
\end{aligned}}\tag{9}
\]

Для точного `z=1/8` и заранее фиксированных rational skew directions программа получает `dot J_P/M=−3303/904070`, `dot J_U/M=−10820/632849`, `dot J_total/M=−131321/6328490`; `F` и `dot F` не коммутируют. Прямое дифференцирование determinant совпадает с (9). Замораживание любого из двух физических slots меняет source. Это универсальная operator identity с допустимыми Lie/Grassmann tangents, но **их native field-to-(P,U) lift** всё ещё надо вывести.

## 4. Положительный результат: точный `logdet` из конечных циклов без внешнего Fock

Пусть **любой** конечный оператор `F` задан на уже имеющемся `r`-мерном carrier. Положим `p_j=Tr F^j`, `e_0=1` и рекуррентно

\[
ke_k=\sum_{j=1}^k(-1)^{j-1}e_{k-j}p_j,\qquad
\boxed{\det(I-zF)=\sum_{k=0}^r(-z)^ke_k.}\tag{10}
\]

Это тождества Ньютона: **не требуется** новый Hilbert/Fock space, diagonalizing oracle или заранее вычисленный determinant для определения полинома. Они требуют следы `F^j` и конечную арифметику на **исходном** carrier. Их вычислимость внутри physical cost-limited controller, допустимость соответствующих multi-cycle comparisons и **цена вычисления** остаются предметом отбора, а не выдаются бесплатно математической формулой.

Дифференцируем **все** коэффициенты (без `[F,dF]=0`):

\[
 dp_j=j\operatorname{Tr}(F^{j-1}dF),\quad
 k\,de_k=\sum_{j=1}^k(-1)^{j-1}\big(de_{k-j}p_j+e_{k-j}dp_j\big).
\tag{11}
\]

Тогда `dJ=−M dP_F(z)/P_F(z)` совпадает с (6) и прямой Jacobi formula; в checker проверено и для actual noncommuting source.

Существует также явный **конечный** signed cycle-cover expansion: если `\mathscr C` пробегает совокупности попарно непересекающихся простых ориентированных циклов на метках (включая петли), то

\[
\boxed{\det(I-zF)=\sum_{\mathscr C}(-1)^{|\mathscr C|}
 z^{\sum_{c\in\mathscr C}\ell(c)}\prod_{c\in\mathscr C}\prod_{(i\to j)\in c} F_{ij}.}
\tag{12}
\]

Её доказательство — разложение determinant по principal minors и перестановкам. Знак `(-1)^number_of_cycles` — свойство перестановок, **не** уже выбранная D0 физическая статистика истории. Формула (12) подсчитывает finite signed combinatorics, а не физическую вероятностную меру.

Для `|z|\rho(F)<1` логарифм той же функции равен

\[
-\log\det(I-zF)=\sum_{n\ge1}\frac{z^n}{n}\operatorname{Tr}F^n.
\tag{13}
\]

Развернём `Tr F^n` в **все** rooted closed walks длины n, не удаляя повторения. Циклическая группа `C_n` поворачивает метку начала. Если `\mathrm{Stab}(\gamma)` — её реальный стабилизатор, то размер orbit `n/|Stab|`, поэтому точная комбинаторная формула

\[
\boxed{\frac1n\sum_{\text{rooted }\gamma}w(\gamma)
=\sum_{[\gamma]_{cyclic}}\frac{w(\gamma)}{|\mathrm{Stab}(\gamma)|}.}\tag{14}
\]

Это вывод `1/n` **как группоидного веса** при условии **допуска самого циклического quotient**. Нельзя заменить правую сторону суммой «по одному за каждую orbit»: у повторений нетривиальный stabilizer, например одно и то же self-loop, повторённое `n` раз, имеет `|Stab|=n`.

Checker проверяет exact рациональные значения `n=1,…,6` (в том числе периодические слова), конечный signed cycle-cover, Ньютона с первой вариацией, и trace-log series. В принципе (10)–(14) решают **алгебраическую** задачу «как получить весь детерминант из native возвратных слов без нового Fock». Они **не** решают физическую задачу «почему процесс оценивается именно этим signed cycle groupoid с соответствующей ценой».

## 5. Точная следующая стрелка физического forcing

Центральная задача уточняется до **одного** source-typed morphism:

\[
\text{native admitted retained }(P,U,\mathrm{archive},\rho,\mathrm{clock})
\stackrel{?}{\longrightarrow}
\text{signed unrooted cycle valuation}/\mathrm{Aut}
\stackrel{?}{\longrightarrow}
-128\log\det(I-z PU^\dagger QUP).
\tag{15}
\]

Нужно закрыть не математическое `det` (его конечный алгоритм уже предъявлен), а следующий **физический закон реализации**, не подменяя его новой аксиомой:

1. **Знак/когерентность:** разрешённые records должны порождать именно signed products, включая (3), а не positive probabilities или абсолютные веса. Если нужен fermionic antisymmetrizer, надо построить его **на прежних** native carriers и доказать его реальную цену.
2. **Корень/период:** надо доказать, что quotient по циклическому началу **не стирает будущие различения сохранённого clock/archive**, иначе (14) лишь математическая группоидная нормировка, не физический M1 quotient. Current price может быть инвариантен при одновременной смене начала и представления, но full future tests требуют отдельного доказательства.
3. **Связь 33-scene с v8:** этот пример уже является declared native K(9,11,13) record, но его `F_{33}` **не** отождествлён с `F_{v8}=I-(I-\alpha\Delta)^m` на `4096×16` thermal carrier. Нужна настоящая primitive-to-operator/readout map, а не перенос символа `F`.
4. **Полная цена и variation:** вывести `Cost−Info` данного **одного** процесса и его ensemble normalization, reference128, controller, matter, clock/fugacity, а затем полный (9) с coframe/link/observer/state variations; весь `H+J+R`, не только `J`.
5. **GR:** самостоятельное действие-источник сравнить с полным Lorentz Einstein stress на admissible tangent и провести исходный `h^{-2}` refinement. Нельзя объявить (7) физическим stress исходной A4D.

**Ключевая развилка:** либо native примитивы гарантируют signed-cycle groupoid с полной сохранённой историей, что превращает (10)–(14) в выбранное физическое `J` (после доказательства source/cost), либо такого права нет — тогда нынешнее `-logdet` остаётся **условной** ценой, а M1 не закрывает её подбор.

## 6. Проверка и воспроизведение

В пакете `check_native_cycle_morphism.py`:

- настоящий `K(9,11,13)`, три Eulerian word по1436 шагов и 33 меткам, все directed counts, `D,P,T,F` по предыдущему owner, без L×L dense matrices;
- точный quotient spectrum, rank32, знак цикла (3), phase rephasing control, первая source формула (5);
- два независимых full33 deterministic способа `dJ` при `z=1/8` и оригинальном `z=2^{-20}`, с отклонением при frozen visit density;
- отдельное одновременное движение *оба* `P` и `U` с noncommuting `dF`, оба ненулевых first sources и Jacobi check;
- signed permutation cycle cover, настоящий cyclic-stabilizer `1/n` по всем rooted words на native трехметочном principal block до длины6, отличимое нарушение sign erasure в третьем моменте, первые source jets тождеств Ньютона.

Заявлены 77 проверочных условий с точной рациональной/символьной арифметикой; `python` и `python -O` дают побайтно одинаковый `RESULT.json`. Ни 1436-мерный полный оператор не строится плотным способом, ни чужие дорогие tests/Lean/roots не перезапускаются. Численная оценка здесь лишь печать точной рациональной дроби. Для проверки выполненных input identities и самого текста приложения требуется обычный code review; этот пакет не выдаёт доказательство admission за machine-certified core theorem.

**Потребитель:** `LAW_SELECT_V8_PROGRAM_AND_PRICE` внутри Draft #334, далее его полная цена/variation, **не** немедленное принятие ОТО. Оставить Draft / `IN_PROGRESS`; не трогать `main`, BOOK, CLAIM, README, очередь, чужих исполнителей и их научные receipts.
