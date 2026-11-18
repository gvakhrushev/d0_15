# B100. Независимая проверка A51 и исправление границы descriptor

**Результат: PASS в указанной области и при входных контрактах A14/A17/A48.** Воспроизведены четыре замороженных A51 science-файла, их SHA-связи, 39 малых проверок порядка, алгебра full-effect, состав A17-count и рациональные оценки. Дополнительно проверены production namespace, 34112 деревьев обратного RAW frame, весь PORT_ZERO, все 18176 деревьев SC6, образцы восьми REPORT и шаблоны native-понижения. Полные огромные REPORT и production word не исполнялись; замороженные файлы и receipt не изменялись. [Результаты и hashes](B100_A51_AUDIT_CHECK.json); [проверяющий код](audit_a51.py). `physical_C_closed=false`, `GR_closed=false`.

## 1. Что проверено независимо и что остаётся предпосылкой

Заново прочитаны `completed_marked_prefixes.py`, `COMPLETED_MARKED_PREFIX_PLAN.json`, `check_completed_marked_prefixes.py`, `COMPLETED_MARKED_PREFIX_CHECK.json` и дополнительно `COMPLETED_PREFIX_TRANSPORT_RU.md`. План содержит 12 marks: SOURCE_after_Qf, обратный RAW frame, 8 завершённых REPORT, PORT_ZERO и SC6. SOURCE_before_Qf отдельно. Три signs на 13 marks дают 39 совпадений **малой искусственной истории** с `A49.family_blocks`, включая контрольное paid padding. Это прямой буквальный replay fixtures, не 39 production-исполнений. В самом production provider использованы те же control/core/stage функции; core padding фактически вызывается `counted_pad` после окончания всей core-ветви и не переносится на внутренний frontier. Два поздних control slots, post и retention остаются в общем A49 clock.

Проверены все 5376 CODE адресов, интервалы восьми REPORT, общие SITE/port/Spin/aux/helper и DATA/private адреса; resource frame и SC6 не пересекают CODE. У восьмого REPORT те же размеры и 196 source slots, что у клонированного шаблона. Для каждого REPORT проверены первые 8 фактических деревьев; для A17 отдельно проверены его native lowering `CX,Z,CZ,X,H,CCX` на глубинах literal inverse 0–2, а также крайние шаблоны fair-bank. Все прошедшие блоки замыкают трансдьюсер и не адресуют CODE. Полностью пройденные RAW-frame-return, PORT_ZERO и SC6 завершаются `pending=0`. Это дополняет проверку A50/B98 полного affine support. Для конечной границы каждого REPORT потребляется не runtime assert, а структурная индукция B58 §1–2: отдельный REPORT составлен из замкнутых good-слов и целых распознаваемых CZ; remap сохраняет дерево, порядок и good-свойство, а конкатенация возвращает pending=0. Проверены SHA B58 и то, что A48 по-прежнему делегирует REPORT тому же `global_h1.stage_blocks` и `reversible_report_stream.report_blocks`; восьмой REPORT использует тот же локальный template с affine-сдвигом. Другой сертифицированный показатель k не меняет parity. Это обосновывает закрытие каждого REPORT на уровне принадлежащей owner индукции, без полного перебора восьми огромных последовательностей; A51 не является production replay.

## 2. Действительный смысл A17 error и цена восьмого REPORT

Здесь существенно, что A17 описывает полный retained logical/native processor, а не только success probability. По его §4 известные A14 occurrences дают hybrid bound **unitary/isometry sequence на заданных input subspaces**. Входные flags/рабочие/factory провода имеют объявленную canonical RAW-подготовку; сохраняются actual READY, failure, records, unused outcomes и output private. Разрешены произвольные SOURCE DATA/SITE columns и внешние reference/old корреляции в рамках этого fibre. На произвольный dirty factory/source-private эта проверка не распространяет оценку. `Q_pre` и `Q_pre^7` не являются полной H.1 `α_h`.

Из A15, A16 и A17 пересчитано:

    A15 (A13+A15+B31), семь REPORT       162477687666
    A17, семь REPORT                     162754649904
    один и тот же REPORT                  23250664272
    восемь REPORT                       186005314176 < 2^38.

При владельческой `<2^-4096` норме каждого A14 macro и действительных literal inverses бюджет восьми REPORT равен `<186005314176·2^-4096`. Дополнительная ошибка G/CX replacement всей A48 core ограничена `<2^-15800`, поэтому безопасный единый budget для любого из 12 завершённых frontiers `e_D<2^-4058`. Для более ранних frontiers взять все восемь REPORT — корректная верхняя оценка, не утверждение что все уже исполнены. Это условный hybrid по сохранённым полным outputs; scalar success compression, postselection или all-dirty inputs не используются. Результат потребляет именно contracts A14/B31/A17 и A48 replacement, не заново исполняет их гигантские DAG.

## 3. Почему нет деления e_D на σt

На одной и той же задаче при `σ=2^-80`, `t=2^-1700` и одном CODE-independent фактическом processor prefix, определим source finite jet `Ĵ_B=(F̂_{B,+}-F̂_{B,-})/(2σt)` и полный исходный derivative `J_B=Φ⊗∂_j B̃(Y₀)` выбранного B̃. Если processor error на его admissible fibre ограничена `e_D`, то

    Ĵ_ν−D_ν J_B = D̂_ν(Ĵ_B−J_B) + (D̂_ν−D_ν)J_B,
    ||Ĵ_ν−D_ν J_B|| ≤ e_J,B + e_D M1,    M1=1748.

Общий fixed `D̂_ν` умножает **уже нормированную разность**, и сам derivative принадлежит тому же input fibre. Это условие существенно: две разные реализации processor для двух плеч или estimate только одной success probability не давали бы этого вывода. Ровно та же выбранная, неотброшенная factory/READY/failure выходная система присутствует в обоих плечах.

Независимая рациональная подстановка фактических замороженных A48 e_B, e_P, e_J,B и A17/A48 e_D воспроизводит значения A51:

| Объект | Проверенная оценка |
|---|---:|
| `e_D` | `<2^-4058` |
| `||F̂₀−Φ⊗D_νB̃(Y₀)||`, а также midpoint error | `<2^-62` |
| finite полный vector axis jet | `<2^-44` |
| finite jet полного joint effect `||O||≤1` | `<2^-43` |

Для последнего используется точная поляризация `Δ(F*OF)/(2σt)=F̄*OĴ+Ĵ*OF̄`. Помимо symbolic расчёта A51 отдельно проверен комплексный двумерный input и недиагональный Hermitian effect. Эта оценка охватывает любые CODE/DATA correlations и retained outcomes в данном fibre, но не нормированную на success условную статистику. Для последовательности отдельных измерений нужны отдельные нормы и её истинная композиция. Все 12 значений наследуют одни и те же исходные source- и factory-предпосылки; точные финальные norms большого слова не вычислены.

## 4. Исправление B99 с учётом RO1 и XF5–XF6

Фраза B99 об «уже зарегистрированном descriptor» была чрезмерно узкой, если понимать её как необходимость внешнего реестра или ожидания не предъявленной уникальной вакуумной матрицы. RO1 основного owner прямо ограничивает квантор: нужна одна admitted operation family с общими witnesses, а не универсальный scheduler всех D0 histories. XF5 допускает полный task descriptor как datum `T` в KAPPA6 без добавления физического program register; его шесть Book01 obligations и действительное исполнение/цена соответствующих операций остаются необходимыми. XF5 относится к конкретному reader/constructor и не доказывает автоматически, что A49 уже удовлетворяет каждому его witness.

Для A23/A49 предметное следующее действие — сформировать один непротиворечивый scoped task descriptor с **конкретным** выбранным A23 full prefix, A48/A49 границами, фактическим перечнем marks, retained outputs, допустимыми свободными полями и независимыми вариациями, canonical births, полной clock/price и соответствующими Book01/KAPPA witnesses. Где заявлена faithful-связь с уже фиксированной **другой** задачей, необходимо сопоставление именно её B, Dν, marks и условий; выбор нового полного descriptor не заменяет такое доказательство. Требование одинаковой вакуумной колонки слабее полного marked map, но отсутствие единственного расширения само по себе не блокирует scoped datum. В этом смысле §6 нового A51 proof корректно уточняет B99.

Открыты только действительно необходимые для выбранной задачи ранние/незакрытые marks, связь с физической `V_h` нормой и всеми разрешёнными направлениями, полный old/input/WORK/scene/record/Info source, Cost−Info и constraint reactions, а также физические admission/recovery/refinement. Данный аудит не превращает ни `H+J`, ни локальные finite jet bounds в полную физическую стационарность или вывод ОТО.
