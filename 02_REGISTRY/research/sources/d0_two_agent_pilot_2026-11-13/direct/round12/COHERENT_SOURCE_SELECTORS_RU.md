# A12. Точные когерентные selectors исходного полного source processor

Потребитель — реальные `H_f/H_q` из A11 и fixed ten-sign processor H.1. Новое утверждение: выписанные полные Hermitian source operators имеют конструктивное представление как когерентная смесь **конкретных подписанных инволюций**, со всеми точными вероятностями в исходном Golden поле. Для внутренних выборов, site-dependent attenuation и всех 2048 исходных report rows сформированы целочисленные prefix tables и общий, не зависящий от поля, закона входа или coherent selector-control, шанс готовности.

Сохраняется `Lambda_h=2^1525`; coefficient не подгонялся. Вычислена готовность **selectors + их fair-resource bank**, но не полная физическая `alpha_h`. Логический Boolean/routing circuit, его H/Toffoli реализации, дополнительные ресурсы, RAW births, измерительный/когерентный интерфейс и stage/mark ledger ещё должны быть составлены. Таблица вероятностей не объявлена native gate word. `GR_closed=false`.

## 1. Полные rank-two moments без лишнего изменения нормировки

Для любых двух разных basis labels a,b пусть `X_ab=|a><b|+|b><a|`, с нулём на полном ортогональном дополнении. Пусть `T_ab` — настоящая перестановка a,b, identity на остальных; `Z_a=I-2|a><a|`. Тогда точно

```
V+=T_ab,
V-=-Z_a Z_b T_ab,
V±*=V±,  V±²=I,
X_ab=(V+ + V-)/2.                         (1)
```

Это равенство на **всех** входных колонках. На active pair обе инволюции равны swap; на complement они равны соответственно +I и -I. Так сохраняется точная norm-one нормировка X, в отличие от более грубого трёхчленного L1-разложения.

Для A11 Choi coframe leaf множитель равен `16 A=32784`, link leaf — `32 A=65568` (`A=2049`). CAR X имеет множитель1 и действует только на внутреннем site/full16 LEFT, с `I_RIGHT`. Ни spectator RIGHT, ни неизвестный oldRIGHT не адресуются. Выбранная инволюция полностью определяется известной парой labels и отдельным fair bit δ. Реальный swap можно описать обратимой формулой `x -> x xor (a xor b)` при `x in {a,b}`, identity иначе; дополнительный знак -1 применяется ровно на complement для V-. Это точная логическая спецификация, не признание многоуправляемого Boolean primitive бесплатным.

## 2. Индукция по всему tensor DAG, а не только по product-state ожиданиям

Для узла i определим положительную массу m_i:

```
constant c: m=|c|,
moment leaf: m=its exact rank-two multiplier,
add: m=sum m_child,
mul: m=product m_child.
```

Нулевые исходные branches удаляются по точному равенству. На nonzero узле строится signed-Hermitian-involution mixture с операторным средним `H_i/m_i`:

* constant возвращает `sign(c) I`;
* leaf выбирает две инволюции (1) с вероятностями1/2;
* add выбирает ребёнка с вероятностью `m_child/m_i`, identity-padding до полной пары степеней Choi/CAR;
* mul независимо выполняет выбор каждого ребёнка на его **раздельных** copy slots, затем берёт tensor product.

Все leaf/selector попытки у разных occurrences независимы, даже если DAG повторно ссылается на одну формулу. Тензорные копии группируются по типам, а их offsets — суммы соответствующих bidegrees предшествующих детей. Add использует начальные slots своего блока и identity на остатке. Поэтому умножение средних есть равенство **операторов**, действующее и на коррелированном входе, а не предположение о факторизации неизвестной физической state.

Контроль против ошибочного shared coin существенен. Для `X_01` на трёхмерном пространстве на `|2,2>` имеем `(X tensor X)=0`, но общий δ в `E[V_δ tensor V_δ]` даёт1. `verify_source_selectors.py` проверяет этот hostile case и полные involution identities. Нельзя заменить независимые internal coins одним reused random label.

На actual active `A=2049` рассчитаны все массы. Все **внутренние** add-ratios оказались рациональными; существует лишь25 различных распределений, включая dummy identity. Они покрывают весь reachable source DAG. Для final site x ещё выбирается

```
w_x=m_root/(rho_x Lambda_h),
normalized DAG с весом w_x,
+I и -I с весами (1-w_x)/2 каждый.             (2)
```

A11 majorant доказывает `0<w_x<1`. Среднее (2) равно `H_root/(rho_x Lambda_h)` на полном carrier. Тем самым один Hadamard test с этой **полной** выбранной инволюцией имеет эффекты `(I±H_x/Lambda_h)/2`. Тест и его реальная реализация должны быть включены в следующую стадию; здесь не вставляется виртуальный H gate.

## 3. Почему недвоичные знаменатели требуют retained READY

Исходный prefix lemma непосредственно работает с весами в `Z[p,1/2]`. При сохранённом `Lambda=2^1525` в site inverse-PF и нормированных DAG ratios присутствуют другие знаменатели. Нельзя объявить такие веса dyadic или бесплатно нормировать после отбрасывания неудач.

Пусть конечный palette имеет partition weights `w_(j,l)=a+b p` в `Q(p)`. Выбираем один положительный integer D, очищающий знаменатели обеих компонент **всего palette**, и `r=ceil(log2 D)`. Тогда

```
tau=D/2^r,       1/2<tau<=1,
unconditional label weights=tau*w_(j,l),
abort weight=1-tau.                           (3)
```

Они принадлежат `Z[p,1/2]`. Все labels и abort сохраняются. Общий τ один для каждого j, в том числе coherent j; управляющий register остаётся явным, поэтому полный READY effect на нём равен `tau I`, а не только одинаковым диагональным числам после его измерения.

Умножаем пары integer coefficients `D w` на phi до неотрицательности: `(A,B)->(A+B,A)`. Для общего n получаем

```
tau w = (A p^n + B p^(n+1))/2^r,
sum_l A_l=2^r F_(n+1),  sum_l B_l=2^r F_n,     (4)
```

включая abort. Приготовляются **все** n Golden и r fair coins. Первая Golden prefix с суммарным exponent>=n определяет тип n или n+1 и свой lexicographic rank; unused suffix тоже приготовлен и сохранён. Вместе с fair-string rank это один целый индекс соответствующей capacity. Сохранённые cumulative thresholds назначают label. Reversible rank/threshold scratch должен быть uncomputed либо явно сохранён как часть target map; нельзя измерять промежуточный label и подменять когерентную смесь классическим entropy term.

## 4. Действительно вычисленные tables

`compile_source_selectors.py` использует только точную арифметику `Q(p)`; sign определяется сравнением рациональных квадратов для `(2a-b)+b sqrt(5)`. Original report polynomial (degree2×8,27 monomials) развёрнут из прежней формулы r, включая sigma±1 и исходные z=2^-20,epsilon=1/64. У всех2048 beta и1-beta проверена строгая положительность и исходный ненулевой high coefficient.

| Palette | Распределений | Fair bits r / attempt | Golden coins n / attempt | READY |
|---|---:|---:|---:|---|
| internal DAG, включая dummy |25|1374|0|общий tau_internal из файла|
| source root/type × SITE |512|1580|1|общий tau_top из файла|
| original sigma ×10-sign mask |2048|94|6|1 при готовых ресурсах|

Файлы `INTERNAL_SELECTOR_PALETTE.json`, `TOP_SOURCE_SELECTOR_PALETTE.json`, `TEN_SIGN_REPORT_PALETTE.json` содержат каждую точную weight pair, все целочисленные counts и capacities. Postprocessor labels — REPORT1/REPORT0; никаких отдельно неослабленных B или ell oracle не используется.

Независимый verifier не импортирует поле compiler-класса: он заново восстанавливает веса из integer counts, проверяет все boundaries интервалов rank-decoder, перебирает все raw Golden words для встречающихся n=0,1,6 и суммирует unused suffix exactly. Получено **39 941** checks; это не исполнение Boolean/native circuits на r-bit пространстве.

## 5. Фиксированное расписание и ненулевая readiness именно этой части

Depth-first interpreter для одного источника посещает node i, на add выбирает одного child, на mul проходит всех children с copy offsets. Максимум visits считается индуктивно `1+max child` / `1+sum child`, включая constants/leaves. Для `2 f +8 q` это **1054 slots**. В неиспользуемом слоте действует dummy palette; prefix preparation и его READY checks всё равно оплачиваются. Каждая visited leaf получает отдельный fair δ; используется отдельный fixed padded leaf pool. Branch-dependent раннего остановa или пропуска расходов не предполагается.

Чтобы не оставлять exponentially small случайную готовность лишь из-за неудач prefix, для каждого slot берём фиксированные cap7 для internal и cap7 для top. **Все** попытки выполняются, даже после первого успеха. Coherent first-success routing выбирает правильный label; каждый исходный label, READY, suffix и прочая работа сохраняется. Если все попытки неуспешны, остается явный abort. Никакого conditioning-away failure в полной программе нет.

Для одного report это **10 248 262 fair qubits** и **76 Golden qubits** для этих selectors. Сюда не включены ещё не составленные H/Toffoli/routing circuits и их отдельные ресурсы. Original plus-resource bank имеет per-attempt probability `s_F=2p^3`, с сохраняемым known-one byproduct. Выбран cap28; полный исчисленный selector-plus-bank требует **286 951 336 попыток**. Каждая попытка имеет собственные настоящие рождения, G/CNOT, чтения/когерентные flags, маршрутизацию и clock; эти числа не являются полным gate ledger.

Именно этот компонент имеет точную готовность

```
alpha_component = [1-(1-2p^3)^28]^10248262
  *[1-(1-tau_internal)^7]^1054
  *[1-(1-tau_top)^7]^10 >= 1/2.                (5)
```

Неравенство проверено рационально: `1-2p^3<53/100`, суммы failure bounds для internal и top <=1/8 каждая, для fair bank <=1/4. Доказательство включает все попытки и фиксированные padded slots. Это огромный конечный свидетель, а не эффективная практическая реализация.

**Полная alpha_h не равна (5) по уже имеющимся данным.** Требуются настоящие Boolean evaluation/threshold/first-success/routing/Hadamard-test operations, их H/Toffoli resource bank и полный native admission/clock. Исходные exact H/Toffoli factories применимы на своём measurement/feedforward интерфейсе; перенос их полного dilation/marks в H.1 G/CX/SourceI profile нельзя считать выполненным просто наличием тех же marginals. Возможная all-column approximation должна иметь свой действительный error budget. Здесь не присваивается новая общая alpha и не выводится новый физический Info.

## 6. Следующая подстановка

B25 строит полный seven-bank target на том же A2049 и source bindings; A12 даёт точную source-sign selection specification для его данных. Следующий конструктор должен выпустить fixed Boolean/native schedule, source/test flags и настоящий READY predicate, сохранив canonical birth framing и все marked prefix outputs. После этого можно вычислить **полную** alpha, связать действительный NPS и A10 recovery, а затем полную физическую Cost−Info/Book source. Полная ОТО остаётся открытой.
