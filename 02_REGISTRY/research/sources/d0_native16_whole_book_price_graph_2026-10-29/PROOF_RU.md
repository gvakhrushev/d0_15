# Native16: один терминальный record-copy и буквальная полная цена Book

## Точный owner-срез

В существующем Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334)
добавлен §7dt на commit
[`22b4e3f430ddb7d8dd7af6e734f5e63225edd056`](https://github.com/gvakhrushev/d0_15/blob/22b4e3f430ddb7d8dd7af6e734f5e63225edd056/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md).
Мемо pinned как blob `1e81dd0151eea362fedacc008293bcf4f0c7d806`, SHA-256
`2a1bb4ea2cd694605d09293921bed76f8b9fe5fd237d1aa18a6979c989f292bf`;
обновлённый brief — blob `6f34289104bb71b593e53c6440d827e3182a249f`, SHA-256
`8d8cbc92c2d797d2417c0d254886245ecceff58bc1b72b853d04111329250b0f`.
Дословные срезы §7dt и brief сохранены рядом.
Owner memo pin: path `02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md` commit `22b4e3f430ddb7d8dd7af6e734f5e63225edd056` blob `1e81dd0151eea362fedacc008293bcf4f0c7d806`; §7dt proves one terminal record layer, independent preparation and the literal full Book price with 93 exact checks.
Owner task pin: path `00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md` commit `22b4e3f430ddb7d8dd7af6e734f5e63225edd056` blob `6f34289104bb71b593e53c6440d827e3182a249f`; the 29 October checkpoint names one terminal record layer, full price and `GR_closed=false`.

§7dt берёт буквальную цену Book03.25 `H+J` и меняет compiler с
`C;W;C` на одну реальную терминальную копию `W;C`, `C=product_a CX(a,r(a))`.
Для одного заранее фиксированного множества использованных processing blanks
`A` каждому `a` соответствует уже initialized и untouched reserve `r(a)`;
новых blank, reset, free inverse или нового primitive нет. Это пока
фиксированный математический execution graph, не physical admission.

На каждом complete original word, включая все подготовки, readers,
failed branches и inverse calls внутри `W`, checker устанавливает
`K_post=K_W`, `E_0=K_W* K_W`, и нулевой return complement. Результат
переживает независимо изменённые подготовки внутри `W`; он не требует
отражения полного слова или двух копий. Для произвольной альтернативы полного
слова сохраняется точная разность
`Q_gap=logdet(aI+zeta E)-logdet(aI+zeta K*K)`, причём
`0<=Q_gap<=zeta/a Tr(Delta)`. Полная цена остаётся исходной `H_N+J`
с этим исходным положительным gap и настоящим clock `H_N`.

Конкретное конечное сравнение оставляет одинаковым начальный изометрический
образ и все первоначальные провода: 34-call вариант с инвентарём
`22 CX + 2 G + 10 SourceI` имеет ту же изометрию на входе, что прежний
37-call вариант; при разрешённой задаче без фиксированной длительности
реальная полная цена 37-call выше примерно на `0.11068705792869126234`.
Две 52-call подготовки дают одинаковый inventory `34 CX + 4 G + 14
SourceI`, но одна реально меняет retained report и снижает полную цену
примерно на `7.2042261899642878e-6`; эта вариация не удалена и не названа
нулевым источником. Реальная copy-reversal ошибка сохраняет gap `Delta`
и соответствующий `Q_gap`.

В checker встроены 93 exact checks по всем 512 active columns над
`QQ(sqrt(p))`, всем input coherences, всем 34 occurrence suffixes,
record effects и полной цене. Owner receipt SHA-256
`b4e52e9d777135388051c2e5908e99a3110816b256be7d5769315a985dffbfe3`;
checker SHA-256
`0b240fde3cef3e433f598a81e68fb6f32995ce77ae736652f7dd43f6ce28e359`.
Точный код, receipt, минимальные замороженные 7ds/7do fixtures, ordinary,
`-O` и повторный replay сохранены в intake. `replay_manifest.json` фиксирует
версии среды и побайтное совпадение всех запусков с published receipt.

## Поправка и оставшиеся предпосылки

Для буквальной математической цены Book03.25 отдельный Shannon,
von Neumann или fitted Info-терм не требуется: это не дополнительное
слагаемое заданного `H+J`. Другая физическая оценка, если она будет
предложена, требует собственного отображения. Это уточняет прежнюю слишком
широкую формулировку §7ds, не изменяя его операторных тождеств.

Результат поддерживает конкретную карту из действительных native words в
complete price graph. Он не доказывает, что физический D0 допускает этот
reserve layout или эти изменения задачи/начала, не определяет полный
физический `X_N`, не выбирает автономно задачу или record и не выводит
общий минимум либо конечное стационарное слово. Более широкому field
compiler ещё нужны настоящий reserve map, ширина, новый clock и refinement.
Complete physical `Cost-Info`, независимые clock/boundary уравнения,
Lean/CI, physical selection и GR closure остаются открыты. `GR_closed=false`.
