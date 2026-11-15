# A46: независимый полный current bank с сохранением исходного SC6

**Результат.** К конечной конструкции A30 добавлены отдельные 180 Choi
подготовок с `bank=f`, 16 CAR с `bank=q`, собственные DATA/RIGHT, source-private,
processor/fair/READY/sigma и один полный A17 REPORT. Он использует настоящее
совместное `(u,U,ψ)` и сохраняет весь когерентный остаток. Исходный SC6 читает
ровно семь прежних REPORT. Дополнительные рождения и все операции прямого
и обратного хода включены в новую цену/clock. Это конечная математическая
спецификация и проверка её структуры; огромное production слово не исполнено.

Закрывается конкретный недостаток A45: там f-Choi/q-CAR повторно использовались
семью REPORT, поэтому не составляли независимый восьмой сохранённый банк.
Здесь банк действительно отделён. Полный исходный набор Dν-карт/first jets,
same-task FN admission, исходный old cut и физический Cost−Info этим не доказаны.
`physical_C_closed=false`, `GR_closed=false`.

## 1. Размещение и рождение

Старый logical `aux=2` остаётся physical `1`. Старый A29 compiler helper имеет
logical адрес `10407050784`, physical `10407050781`; это другой регистр.
Fresh logical interval начинается с `10407050785`, сразу после helper.
Его ширина равна

    (1486716794−8) + 180·24 + 16·3 = 1486721154.

Для fresh адресов `physical(q)=q−3`; первый fresh physical адрес —
`10407050782`. Общее число early RAW births — **11893771936**. Старое
отображение, SAM, общий external SITE, SC6 selectors, port, aux и helper
сохранены. Ни один дополнительный физический нулевой вход не постулируется:
каждый fresh вход рождается в исходном RAW v, а ZERO/FAIR/sigma готовятся
оплаченными прежними процедурами.

Fresh REPORT получает собственный непрерывный virtual private interval.
Локальные SOURCE buffers и все processor wires переводятся одним сдвигом;
shared SITE/port/spin/aux/old witness переводятся прежними правилами.
Choi DATA сохраняет порядок output[0:5], input[5:10], address[10:22]; CAR
сохраняет grade[0:4], internal SITE[4:12] и все семь RIGHT wires. Вызовы
SOURCE идут через реальные `f` Choi и `q` CAR providers, без новой таблицы
целевых состояний. Все 4368 source-private остаются в полном пространстве.

## 2. Буквальная последовательность

Прямой A′ выполняет:

1. Один прежний SITE; семь прежних SIGMA/SOURCE; fresh SIGMA/SOURCE.
2. RAW frame и его literal inverse на всех **34112** DATA/RIGHT wires.
3. Семь прежних REPORT, затем fresh REPORT.
4. Прежние PORT_ZERO и SC6 с прежними 23 logical адресами.

Далее идут central Z и буквальный старый inverse всего A′. После этого
**всё слово** переводится одним A29 compiler в G/CX, с прежним helper и
прежним сертифицированным k. Поэтому native обратная часть не называется
точным inverse уже переведённой прямой части. Внутренние literal depths,
включая depth=2 у обратного RAW frame, сохранены.

Qf стоит после общего прямого RAW frame; Qb — после inverse соответствующего
обратного frame. Средняя часть между ними адресует только WORK. Метки
допустимы только при закрытом SourceI transducer state. Полные завершённые
REPORT имеют явные tags; автоматический перенос всех исходных внутренних
Dν/α-меток не заявляется.

## 3. Сохранение и исходный семиотчётный источник

Старые REPORT не адресуют fresh DATA, RIGHT, processor или source-private.
Следовательно их действительное унитарное исполнение сохраняет reduced
state fresh arena+SAM: это действие на дополнении. Полная совместная карта
с shared SITE при этом сохраняется как карта, а не заменяется частичным
следом. Нельзя утверждать, что состояние SITE вместе с fresh банком вообще
не меняется: SITE участвует в старых REPORT.

На уровне идеальных закрытых логических макросов fresh REPORT D действует
только на fresh arena и shared SITE, тождественно на port/aux/Spin. Обозначим
через C прежние PORT_ZERO/SC6, через R семь старых REPORT, через B полный
source prefix. Поскольку C и Z не адресуют SITE/fresh,

    A′ = C D R B,
    A′† Z A′ = B† R† D† C† Z C D R B = B† R† C† Z C R B.

Коммутативность используется для **идеального логического** D на всех
колонках. Реальный old-profile D и переведённый G/CX D используют shared
port/aux/helper; для них оплачивается ошибка, точная коммутативность не нужна.
Не предполагается и all-dirty-column коммутативность SOURCE preparations.

Canonical-input hybrid содержит нормированную fresh source ветвь для каждого
SAM b и сохраняет весь branch-dependent remainder R_b. После отмены D
семиотчётный оператор не адресует fresh arena; на диагональной SAM-компрессии
её norm²=1. Поэтому идеальный скаляр остаётся

    M⁰_b = c_ref − 2g I_τ(Y_b).

Это не позволяет стирать fresh branch overlaps при внутренних Q-вставках:
Q смешивает SAM labels и обычно не коммутирует с fresh подготовкой.
Их новая оценка приводится отдельно ниже.

## 4. Полная стоимость и ошибка

К A30 profile добавлены fresh SOURCE+SIGMA+REPORT и literal inverse этих
операций; четыре fresh RAW frame дают на каждый из 4264 wires

    (G_port,G_other,CX,SourceI) = (3,1,18,24).

Полный CZ census — **1203136**. Повторная компиляция даёт длину core с
bit_length **11647**. Точные целые counts и rational bounds находятся в
`INDEPENDENT_CURRENT_BANK_PLAN.json` и вычисляются без разворачивания repeats.

При тех же uniform upstream сертификатах:

    новый source-prefix error < 2^-3232;
    full all-column G/CX replacement e_W < 2^-3244;
    canonical compressed error e_B < 2^-3231;
    2/3 < M_b ≤ 1.

Последняя верхняя граница — сжатие действительного unitary; вещественность и
SAM-control-only дают действительную диагональную M. Ошибка одного fresh
REPORT берётся из 1/7 A17 seven-report macro census; семь REPORT структурно
одинаковы. B90 дополнительно проверяет более грубую оценку с полным семикратным
бюджетом для fresh REPORT.

## 5. Новый фиксированный выход и цена

Из **новой actual M** конечным алгебраическим рецептом A41 строится новое U*;
его native approximation Uhat фиксируется во всех endpoints новой семьи.
Старый A30/A45 Uhat не переиспользуется по предположению близости. Положительность
M обеспечивает исходный рецепт нормирования и устранения Householder-знаков.
Grid и верхние counts A41 зависят только от m=2688, поэтому остаются прежними.
Python production provider по-прежнему не реализован; assembler явно отвергает
передачу этих верхних counts как якобы вычисленных точных counts слова.

Пересчитаны early births, новый core, два Q slots, post/probe padding и late
retention: `Nbase.bit_length=25457`, **K=137444**. Это равенство K следует из
нового расчёта; цена не объявляется равной старой. Clock dimension:

    2^11893771936 · (Lbase−2+3·2^137444) − 1.

Нормирование всех новых строк использует собственный gain

    Γ_new = 4 z p^K c_ref gs / (1−z+z p^K c0_new²).

A42 estimates применяются с новой M, новым фиксированным Uhat и новым Nbase:
incoming finite row error `<2^-75`, corrected covector error `<2^-70`,
outgoing full finite dual bound `<2^-75`. Исходное heat/spectator допущение
и граница old-cut admission остаются такими же, как у A42/A43.

## 6. Внутренние Q: пересчёт, а не перенос endpoint ошибки

На одном coframe ребре меняются **540** Choi копий; link — **360**;
matter — **32** CAR. Для j=2:

    Λ²_ideal ≤ 540·(3s/32)²,
    sqrt(540)·3/32 < 35/16,
    Λ_actual < (35/16)s+2·2^-3232 < (9/4)s.

Поэтому собственная A43 j2 оценка, с тем же идеальным семиотчётным M⁰ и
проверенными новыми e_B/e_W, остаётся `<2^-77` аналитически и `<2^-75` для
finite full H+J contrast. Конкретная нормированная Qb строка `>2^-45`; Qf
имеет противоположный знак. Равенство двух price-swapped endpoints следует
из WORK-only середины и полного stage gauge на той же новой paid family;
оно не отождествляет все исходные intermediate marks/FN fibres.

Для любых двух полных SAM labels product-source bound теперь равен

    δ²_ideal ≤ [540·256·(3/16)² + 360·256·(81/16)²
                 + 32·(11/10)²]s² < (1539s)²,
    δ_actual < 1540s,  τ/(gs)<85.

Повторное применение отражённой kernel identity A44 даёт

    ||d_Qb − (1/2)d_reduced_Pf|| ≤
      (3/4)[85(2δ²+2e_W)+e_W/(gs)] + e_U/(gs) < 2^-31.

Это операторная dual-оценка всех real-SAM skew направлений для аналитического
feedback; все такие направления не объявляются физически допустимыми.
Старое глобальное `<2^-32` не переносится. Для Qf знак обратный.

## 7. Проверка и оставшаяся обязанность

Root checker проверяет всю affine address injection на virtual interval,
все 196 fresh source bindings, неизменность старых банков/SC6, фактические
SOURCE templates, четыре literal depths, прежний helper, отказ от незакрытой
SourceI-метки, пять полностью развёрнутых малых paid histories, clock dimensions,
новый error budget и production guard. Малые истории проверяют assembler;
они не выдаются за исполнение огромной физической модели.

Следующий содержательный шаг — привязать к этой независимой арене конкретные
исходные Dν-карты и обязательные метки, с их полным остатком и first-source
переносом. Наличие восьмой арены само по себе не доказывает compulsory
Cost−Info selection, все исходные independent preparation equations или
refinement к ОТО. Новые коэффициенты действия, Info или selector не введены.
