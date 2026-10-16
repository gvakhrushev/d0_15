# Интеграция продолжения в существующий #334

Проверено 2026-10-16 в `gvakhrushev/d0_15`. Существующий [draft PR #334](https://github.com/gvakhrushev/d0_15/pull/334) идёт из branch `exp/a4d-joint-response-continuation-2026-10-16`; GitHub и локальный `origin` указывали на один HEAD `e9cd1b913ca8199a400aee35d35da455c27c778b`.

## Файлы и происхождение

Все 12 путей из приложенного additive patch уже были tracked в этом PR. До статусной правки основного proof `git apply --reverse --check D0_memory_rank_nonlinear_continuation_2026-10-16.patch` прошёл на дереве `e9cd1b9`; патч повторно не накладывался. Исходный приложенный Markdown в тот момент точно совпадал с tracked-файлом: SHA-256 `8ec54e4838aaa579469896eeaf369e16a24d6a6f0f67824ede6fa88f5cb9b622`, Git blob `d267ba0916c83d8972f27651950e3503f0bf9d96`. Затем в proof изменён только устаревший абзац о публикации. Старые CAR owner bytes и математический `result.json` не менялись.

## Повтор проверки

Узкий сертификат запущен на Python 3.12.13 с SymPy 1.14.0:

- обычный запуск: `PASS_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION`;
- запуск с `-O`: тот же PASS и тот же JSON;
- пять математических mutation controls отвергнуты, включая неверную seed covariance, пропуск нормировки, фиксацию пустого shell, заморозку амплитудного second jet и неверный знак resolvent.

GitHub на момент проверки не сообщил check runs для branch #334. Это локальная точная проверка указанного пакета, не CI и не новая Lean-сборка. Поле `new_GitHub_publication=false` в `VALIDATION.json` сохранено как исторический факт: локальный запуск сертификата не публиковал коммит; presence пакета проверена отдельно.

## Научная граница и следующий шаг

В PR сохранены точная трёхкомпонентная source capacity, pure-state inverse, rank-aware shell tangent, полные second-jet условия и необходимый kernel-тест от стационарной памяти. Результат не задаёт физический закон приготовления состояния. Не получены actual curved native root, физически выбранная preparation law, soundness/recovery или вывод ОТО.

Следующий короткий тест сокращён до одного точного source-neutral наблюдаемого: `W=(c0+b0)i(c0-b0)(c1+b1)i(c1-b1)`. Его trace и три source-паринга доказаны exact в расширенном checker; `W` grade-four, тогда как источники `B_r` grade 0/2. На плавающем `q=(3,3,0,0)` crossing имеем `Tr(W M_v)/16≈0.58525`, но exact kernel-вектор и точное crossing ещё не изолированы. Следующее доказательство должно интервально изолировать `t` в stationary memory fibre и оценить этот скаляр на действительном joint-kernel векторе. После этого отдельными остаются сходимость nonlinear ветви, refinement, admission и физическая идентификация Einstein.
