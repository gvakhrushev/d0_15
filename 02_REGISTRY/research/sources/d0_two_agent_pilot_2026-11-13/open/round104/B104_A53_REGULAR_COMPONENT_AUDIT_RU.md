# B104. Независимая проверка полевых coframe/CAR компонентов A53

**Результат: PASS в области A53.** Независимо сверены исходные 2688 координат и все 7168 coframe / 1728 CAR rows, интервальные запасы всей заявленной коробки, Golden grid на нулях/квадрантах/ties, состав coframe/CAR sectors и верхние inventory bounds с буквальными inverse. Отдельно воспроизведены выбранные полные 32- и 16-колоночные операторы из actual сертифицированных G powers. Это проверка **компонентов**, не полный новый global SOURCE, G/CX replacement, общий clock или physical Cost−Info. [Проверяющий код](audit_regular_components.py) и [receipt](B104_A53_AUDIT_CHECK.json). `physical_C_closed=false`, `GR_closed=false`.

## 1. Один field name и полное соответствие адресов

`FieldCentre` содержит 2688 независимых `Fraction` в порядке исходного B21 JSONL: 1024 coframe, 1536 proper-link, 128 matter. Ровно эта исходная последовательность сверена с `sam_index`; метки разных видов не перемешаны. Рациональный `|offset|<2^-32` и `σ=2^-80` выполняют

    2^-32+3σ < (3/8)2^-30 < min(p²,1−p²)2^-30.

Тем самым любая комбинация нового centre и всех четырёх CODE digits остаётся внутри старого **асимметричного** B21 cube. Равенство на границе, float и Boolean отвергаются. Это точные рациональные names в открытом subchart; не утверждается, что произвольное real число хранится как конечная Fraction. Перевод приближённого real input использует исходные B91 `M1=1748`, `M2=3233036`, `sqrt(2688)<52` и явно сохраняет ошибку имени и физическую norm conversion.

Из исходных B21 coordinates построен отдельный словарь `(site,role,component)→index` и сверены **все 7168 coframe templates** семи банков. В current f/q используются все четыре правильных component offsets одной роли и site; в references и исходных boundary rows новые offset не добавляются. Отдельно из PF site list и `(site,grade)→index` сверены все **1216 q + 256 y+ + 256 y−** CAR rows, исходные grades 0/15, interleaved low/high CODE wires и их patterns. Четырёхбитные шаблоны проверены полностью.

Как дополнительная диагностика, на одном поле с разными значениями во всех coordinates заново вычислены **все 7168 coframe и 1728 CAR** targets по независимой B25 численной формуле; максимальные расхождения `2.8e-17` и `2.1e-18`. Двухбитный шаг `2^-80` ниже разрешения этого float сравнения, поэтому точное связывание CODE patterns проверено отдельно; эта диагностика не заменяет интервальную гарантию.

## 2. Вся коробка, zero/ties и реальная precision

Независимый outward interval расчёт расширяет каждую из 7168 coframe rows сразу на полную величину `±(2^-32+3σ)` там, где координаты свободны. Он проверил `0<||u||<1` и каждую из трёх последовательных elimination radii `r_i≥||u||/2`, не выбирая field по случайной выборке. Для всех четырёх исходных CAR time slices независимо проверены `||ψ||²<1/15`, slack `1−p−||ψ||²>1/3`; фиксированный положительный anchor `v_1=sqrt((1+sqrt(p))/2)>9/10` гарантирует положительные знаменатели всех CAR rotations. Reference/boundary rows сохраняют прежние имена. Эти bounds обосновывают, что assertions исходных factor functions не блокируют точный ноль или допустимый центр.

На обеих actual B93 grids K=15 и K=24 отдельно сформированы и 7168-битным complex-ball возведением перепроверены **26** настоящих Golden powers: все четыре осевых quadrants, по восемь рациональных точек круга и точная tie `|cos|=|sin|=1/sqrt(2)`. Для `controlled_X` отдельно проверены реальные power π/2 и его удвоенная phase π: суммарная ошибка `<3·2^-3460`. Сетка и предыдущий короткий сертификат дают общий all-angle результат; 26 checks являются независимой выборкой, а не перечислением всех real полей. Selector выбирает компонент с нижней границей `>3/5`, затем достаточно узкий интервал; ни exact-zero, ни точное сравнение с границей округления не требуется. Строгий положительный margin существует на единичной окружности, поэтому удвоение precision завершается при сохранении исходных interval contracts.

## 3. Оператор, затраты и literal inverse

Для одного coframe sector A53 всегда выводит 24 Fock rotations, один base rotation и controlled X. При `δ=2^-3460` имеем `24δ+δ+3δ=28δ<2^-3455`. CAR half-vector использует три сохраняемые rotations и даёт `<3δ<2^-3458`. Контроли address/CODE и, где применимо, SITE остаются read-only: выбранные targets и перестановки CX затрагивают только допустимые внутренние Julia/grade/aux wires; protected RIGHT и oldRIGHT не используются как targets. На прочих sectors SourceI-profile Walsh реализует точную identity. Поэтому error по coherent суперпозиции непересекающихся адресов и CODE patterns — **максимум**, не сумма ошибок всех sectors; каждый sector при этом реально входит в стоимость.

Выполнена независимая численная диагностика actual macro-chronology: G powers вычислены отдельно complex balls, затем агрегированные условные rotation/permutation матрицы составлены для f/q/reference coframe на **всех 32 Julia columns и обоих aux состояниях**, и для q/y+/y− CAR на **всех 16 columns выбранного трёхплоскостного continuation**. Максимальное расхождение с B25 Julia или полным заявленным CAR continuation `<1.2e-16`. Эта проверка выявляет ошибки адреса, ориентации и порядка; она не разворачивает нативные `2^K` masks и не заменяет строгий error proof.

Независимая целочисленная формула `pair_counts` проверена при всех возможных widths K, обоих типах patterns, максимальном `k=q` и максимальных перестановках. Действительная phase controlled X может иметь K=25 и использует doubled multiplier; она включена в тот же coframe upper. Для 120 actual coframe/CAR sector × inverse-depth случаев, в том числе внутренних уже обращённых units, заново подсчитаны forward/обратные counters и проверено доминирование. Линейный положительный `raw_inverse_counts` сохраняет componentwise upper при каждом дополнительном literal inverse; inverse-of-inverse не сокращается бесплатно. Независимо восстановлены размеры и forward/inverse upper всех банков:

    coframe f/q: 256·4^4+768 = 66304 sectors каждый;
    coframe reference: 1024 sectors каждый;
    CAR q: 64·16+192 = 1216;  CAR y±: 256 каждый.

Сохранённые в A53 componentwise upper — именно верхние границы, не вычисленные точные цены gigantic unpadded слов. В них не включены новый B103 proper-link SELECT, полная SOURCE композиция, SourceI replacement или новый post/growing clock.

## 4. Следующее применение

A53 корректно задаёт параметризованные coframe и CAR компоненты без отсылки к Einstein predicate. B103 добавляет отдельный original proper-link Julia32 provider; они должны быть связаны на одной `FieldCentre` и одном действительном A53 SOURCE расписании. После этого отдельно нужны полный hybrid/source error с actual canonical private, combined actual inventory и оплаченный G/CX/clock, fixed-family post и все required marked prefixes. B103 показал сохранение старого `<2^-3423` только при сохранении остальных A48 component error contracts; оно не является автоматической проверкой новой интеграции.

Physical fine instrument/suffix, все допустимые independent source rows и исходный V_h/right-lift, same-execution physical Cost−Info и GR refinement остаются открыты. Ни этот audit, ни конечная точность компонентов не объявляют физическую стационарность.
