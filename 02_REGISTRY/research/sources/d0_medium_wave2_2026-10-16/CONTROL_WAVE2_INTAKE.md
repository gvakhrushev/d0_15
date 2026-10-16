# N01 — CONTROL: зарегистрировать вторую волну и снять ограниченный интеграционный хвост

Repository: `gvakhrushev/d0_15`
Task: `CONTROL-PLANE`
Class: `CONTROL`
Base: `main`
Branch: `control/a4d-medium-wave2-registration-2026-10-16`
Primary artifact: `00_WORK/manifest.json`
Execution: `GitHub-first`

## Цель и первый завершённый результат
Установить девять новых WORKER briefs этого пакета в существующий `00_WORK`, не воскресить восемь завершённых поручений первой волны, сохранить #331 и один главный научный SOURCE #334. Это bounded CONTROL-поручение, не десятая независимая научная задача. После публикации/приёмки регистрации дать назначенным писателям штатные Task-ID; не ждать полного закрытия #334.

## Актуальные входы
Main: `add17919b344f0e46115619aa53d2173ecdcf219`. SOURCE #334: `74e62cdc716e10883accba9d34ccf0e21d58eb65`.
Общий вход: `02_REGISTRY/research/D0_SECOND_MEDIUM_AGENT_WAVE_2026-10-16.md`.
Прочитать actual `AGENTS.md`, `00_WORK/README.md`, manifest и live PRs. #324 merged; #310 закрыт без merge. #322 и #323 остаются отдельными intake. Восемь workers первой волны merged (#325/#326/#327/#328/#329/#330/#332/#333); только #331 moving scales сохраняет live WORKER execution на снимке. Это не вечный heartbeat.

## Регистрация без нового диспетчера
Все девять текстов уже имеют полное metadata. Пакетный `register_wave2.py` — тонкий адаптер принятого первого `register_wave.py`: переиспользует его проверку parent/claims, rollback, renderer, validators и защиту от resurrection. Старый helper не меняется. SHA исходного helper проверяется до загрузки. Здесь новая политика — только девять новых ID, их каталог и одна назначенная CONTROL-ветка; нет scheduler/cache/нового реестра.

На чистом checkout текущего main читать пакет из точного опубликованного SOURCE. При необходимости взять только этот каталог и общий вход, не весь #334. Обеспечить существующий old helper и его исходные preserved briefs из main. После проверки live ownership создать указанную CONTROL-ветку; публикация записи — отдельный малый governance PR, не science execution и не изменение frozen #322. При уже существующем перекрывающемся CONTROL-PR работать через его владельца и согласовать branch fence явно, не обходить его.

```sh
python 02_REGISTRY/research/sources/d0_medium_wave2_2026-10-16/register_wave2.py --check
python 02_REGISTRY/research/sources/d0_medium_wave2_2026-10-16/register_wave2.py --apply
```

Проверить diff: добавлены только девять строк, девять официальных briefs и generated status block; старые задачи/limits/claims/states неизменны. Обновить общий вход с настоящим registration commit и PR в этой же поставке, без нового JSON-трекера. Если main успел измениться, применить к новому main и пересчитать штатные views, не подменять их копиями из SOURCE.

Сохранить normal Draft/Ready и независимую приёмку. Не self-merge. Назначение агентов не производится скриптом. Во время отсутствия свободного CONTROL ownership возможна только read-only подготовка; не создавать третий конкурирующий управленческий поток.

## Ограниченный интеграционный хвост после регистрации
Не принимать все 1200+ research файлов как одну доказанную теорию. Совместно с владельцем #334 выбрать один точный приемочный срез для двух уже отмеченных inherited shift-irrelevance Lean lemmas и narrow source-unfolding package; разрешить их фактические module paths из diff SOURCE к main. Запустить ровно нужную formal closure и проверки неизменности входов, сохранить отдельный receipt. Если slice не готов, дать конкретный failing command/type и передать patch владельцу, не повторять старые root solves.

#322/#323 могут приниматься только по своим frozen manifests и независимым scientific review. Новая registration не изменяет их proof scopes. Общие formal_support/All-views централизовать: N03/N04 поставляют свои строки и narrow proofs, CONTROL регенерирует и принимает нужную полную closure. Никаких orphan модулей к финальной приёмке.

## Распределение
После регистрации запустить до четырёх новых WORKER при продолжающемся #331: N02, N05, N06, N10. Любой новый live WORKER сокращает этот набор. N03/N04/N08 независимы и заполняют освободившиеся слоты; native-facing часть N07 требует N05/N06, N09 получает их количественные bounds. BLOCKED и REVIEW также занимают слот. Не повышать limits (WORKER5, EXPENSIVE3, CONTROL2).

Не отправлять 9 одинаковых команд в background от имени этого текста. Каждому реальному исполнителю — отдельная назначенная ветка и exact brief. Если сервис агентов недоступен, честно выдать переносимый текст; подготовка поручений не означает запуск.

## Why delegated
Это интеграция, проверки, постановка и приёмка ограниченных результатов, которые отвлекают ведущего от физической вынужденности и nonlinear joint construction. Регистрируются существующие задачи данного пакета, а не новый программный процесс.

## GitHub execution contract
Согласовать единственного CONTROL-писателя. Draft до substantive writes, маленький governance diff, штатные валидаторы, независимая приёмка. Main не обновлять обходом PR. Результаты работников потребляются в #334 по мере готовности; их acceptance не меняет исходный exact-source/raw терминал.

## Chat handoff
Registration PR/SHA, фактическое состояние main, назначенные task IDs и свободные слоты; затем точный интеграционный verdict и оставшийся blocker. Не выдавать текстовые briefs, read-only проверки или зелёный skipped workflow за работающих агентов/доказанную ОТО.
