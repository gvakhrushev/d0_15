# Cold-start refresh PR #402 — `42132ba5`

## Результат

Полный cold-start выполнен на чистом snapshot PR #402
`42132ba53d306d0ce1104d21435661545807add0`. Поиск нашёл все обязательные
источники в **49 из 50** cases при окне 18 кандидатов; benchmark с regression
содержит 51 проверку. Change-impact regression прошёл.

Два прежних пропуска устранены без изменения source scope и требований к
пинам:

- `native-stationary-recording-seed-whole-word-source`: **4/4** источника;
  memo и checker найдены по одному запросу, pinned owner-файлы имеют ожидаемые
  commit/blob.
- `native16-whole-book-price-graph`: **12/12** источников; replay checker и
  его manifest находятся тем же запросом.

## Оставшаяся граница

Единственный неполный case — `pr334-native-kappa-owner-delta`: workspace search
не нашёл **68 из 69** требуемых путей. Это содержимое закреплено за owner
snapshot PR #334 `e94e518c43b748e6c4fff1d4db364a6265bbf44d`; отдельный тест
`test_pr334_e94_owner_manifest_pins_all_68_changed_paths` прошёл и сверил для
всех 68 файлов Git blob, число байт и SHA-256. Этот тест подтверждает точность
Git-пинов, а не полнотекстовую discoverability owner-ветки из рабочего дерева
PR #402.

## Воспроизводимость и статус

Полный stdout runner — 25,119,434 байта, SHA-256
`e4997ab46e9e5e9ac60baae25ef88005a94de9998dccd8e83e0f2c8a53feecba`.
Компактная сводка, сохранённая рядом, — 2,559,915 байт, SHA-256
`4bcd52d6710cd96ff72239879a60c5a62b0a7a6e8ef185f136ea6152a8c93cc4`.
Команда, хэши runner/search-engine/fixtures и агрегаты перечислены в
[`replay_manifest.json`](replay_manifest.json); полные статусы поиска и exact
source receipts сохранены в [`cold_start_summary.json`](cold_start_summary.json).

Это обновление меняет только формулировки двух cold-start запросов. Lean
источники не менялись и новой Lean-теоремы здесь нет; прежний точный `D0.All`
receipt сохраняет свою область применения. Научный статус не повышен:
`GR_closed=false`.
