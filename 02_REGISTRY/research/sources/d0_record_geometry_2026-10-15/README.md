# Последнее исследование D0: полный текст для нового ИИ

15 октября 2026 года. Публикация в существующем [PR #323](https://github.com/gvakhrushev/d0_15/pull/323), ветка `control/d0-strategy-handoff-2026-10-15`.

Этот каталог сохраняет весь текст переданного исследования и большой задачи. Для чтения не нужны ZIP, base64, распаковщик или прежний чат. Это исследовательское приложение к существующему маршруту: [#310](https://github.com/gvakhrushev/d0_15/pull/310) ведёт научную работу, [#324](https://github.com/gvakhrushev/d0_15/pull/324) — единственный рабочий процесс. Здесь нет новой очереди, зарегистрированной задачи или второго писателя #310.

## Порядок чтения

1. Прочитать этот файл и [закреплённые входы](SOURCE_PINS.json). Сначала учесть изменения #310 после написания brief, перечисленные ниже.
2. Прочитать **[новый синтез с доказательствами](original/SYNTHESIS_RU.md)** полностью.
3. Прочитать **[большую задачу для дорогого ИИ](original/EXPENSIVE_AI_BRIEF_RU.md)** полностью. Её label `NATIVE-RECORD-2JET-SOURCE-GR` не является новым task ID.
4. Прочитать [предыдущий синтез двух материалов](original/inputs/D0_two_syntheses_to_GR_2026-10-15.md), [резонансный синтез](original/inputs/D0_resonant_synthesis_to_GR_2026-10-15.md) и [аудит](original/inputs/D0_deep_audit_2026-10-15%281%29.md).
5. Использовать [полный указатель каждого исходного пути](TEXT_INDEX.md) для доказательств, программ, исходных отчётов, патчей и контрольных результатов. Два HTML-материала доступны также как [текст об отображении поля в прибор](html_text/D0_otobrazhenie_pole_pribor.md) и [текст о башне и пределе](html_text/D0_sintez_bashnya_phi_predel.md).

Ключевой вопрос задачи: вывести **одну собственную непустую refining-family D0**, её полную цену и реальные вариации, затем доказать источник-полноту и количественный перенос всех требуемых метрических уравнений. Данный U(4) germ ранга 10 — кинематический вход. Он не устанавливает physical admission, общий native action или вывод ОТО.

## Какие файлы перенесены

| Файл прошлого чата | Читаемая копия |
|---|---|
| `/mnt/data/D0_expensive_AI_native_record_to_GR_task_2026-10-15.md` | [EXPENSIVE_AI_BRIEF_RU.md](original/EXPENSIVE_AI_BRIEF_RU.md), совпадает с отдельным файлом из Downloads побайтно |
| `/mnt/data/D0_record_geometry_new_synthesis_2026-10-15.md` | [SYNTHESIS_RU.md](original/SYNTHESIS_RU.md), документ с этим назначением внутри переданного ZIP; отдельный файл на этом компьютере не обнаружен |
| `/mnt/data/D0_source_faithful_record_and_expensive_task_2026-10-15.zip` | Весь текст открыт в `original/` и `expanded/`; [TEXT_MANIFEST.json](TEXT_MANIFEST.json) связывает каждый член со своей копией |
| Ранее сохранённый 21-файловый capsule #323 | Текст также открыт; последние 21 строки [указателя](TEXT_INDEX.md) связывают его с копиями |

Архив найден в Downloads; его SHA-256 — `ee53b2fad8e687b3a26f4f9cc00a283b27ece643dbfe7552354be794e1e424e8`. Оригинал и дубликат `(1).zip` совпадают. Исходники сохранены без редакторской правки.

Внешний ZIP и все вложенные ZIP содержат **150 текстовых вхождений / 77 уникальных содержимых**. Вместе с прежним capsule #323 опубликовано **78 уникальных исходных текстов**. Повторы адресуются одной копией с неизменными байтами. Десять вхождений пяти бинарных XZ-частей декодируются в 25 файлов, каждый из которых уже есть среди открытых копий. Прямое сравнение с оригинальным ZIP проверяет и этот факт. Все 20 файлов `new_additions.patch` и 25 файлов `additions.patch` также имеют полные открытые копии; патчи сохранены отдельно как исходный текст.

`original/MANIFEST.json`, `original/VALIDATION.json`, старые README и отчёты отражают **момент создания** пакета. Их прежние `remote_publication: false`, sandbox-ссылки и пути архивов намеренно не переписаны. Нынешние проверки и статус находятся в [publication validation](PUBLICATION_VALIDATION.json) и [свежем replay](validation/new_packet.json).

## Что уже сделано в #310 и не требует повторного исследования

Исходный brief читался на `fe2fc53fb9479aba6c8c99c8294d25b444f7a27a`. При публикации проверен более новый SOURCE **`5a68275e06b76177e54a9f909a723f7d7a9949e7`**. Его два следующих коммита важны для устранения дублирования:

| Существующий результат | Как использовать |
|---|---|
| [Полный prepared-source и joint continuation](https://github.com/gvakhrushev/d0_15/blob/5a68275e06b76177e54a9f909a723f7d7a9949e7/02_REGISTRY/research/A4D_NATIVE_RECORD_SOURCE_JOINT_CONTINUATION.md) | Готовые forward/reverse pullback, нормализатор, правильные state tangents, критерий source descent, совместимость 24+10. Применять к тому же native-процессу. |
| [Башня, trace и тепловой источник](https://github.com/gvakhrushev/d0_15/blob/5a68275e06b76177e54a9f909a723f7d7a9949e7/02_REGISTRY/research/A4D_TOWER_TRACE_HEAT_SOURCE_SYNTHESIS.md) | Точная ширина `1/(F_(N+1) F_(N+2))`, условный бюджет ошибки источника и сохраняющийся тепловой дефект уже записаны в SOURCE. |
| [Доказательство совместного теплового предела](https://github.com/gvakhrushev/d0_15/blob/5a68275e06b76177e54a9f909a723f7d7a9949e7/02_REGISTRY/research/sources/d0_tower_heat_synthesis_2026-10-15/HEAT_JOINT_LIMIT_PROOF.md) | Предел `beta=c/L` даёт `15/(32c^2)>0`. При `c=1` он перекрывает результат `15/32` нового пакета; повтор не является новым прорывом. |
| [Archive occupation source](https://github.com/gvakhrushev/d0_15/blob/5a68275e06b76177e54a9f909a723f7d7a9949e7/02_REGISTRY/research/A4D_NATIVE_ARCHIVE_OCCUPATION_SOURCE.md) | Уже вычислены собственная A9 occupation, полный источник и сохраняющийся источник для `N>=9` с явным Jones lift. Physical map и полный Cost−Info binding остаются открытыми. |

Кинематический second-jet пример этого пакета не опровергает условный first-jet calculus владельца. Следующий содержательный шаг — **native реализация и полное вариационное отождествление**, сохранение архива и материи, нелинейная совместимость и равномерный перенос. Не поручать новому ИИ заново выводить известные pullback, Fibonacci width, heat limit или occupation source как главный результат.

Перед научным исполнением заново разрешить живые SHA и единственного писателя #310 через действующий маршрут #324. Этот снимок ничего не запускает и не освобождает WIP. #202/#317 и frozen checkpoint #322 сохраняют свои области и статусы.

## Воспроизводимые проверки без скачивания архивов

Python 3.11+; зависимости нового пакета указаны в [requirements_replay.txt](requirements_replay.txt). Команды выполняются из корня репозитория.

```sh
python 02_REGISTRY/research/sources/d0_record_geometry_2026-10-15/verify_publication.py
python 02_REGISTRY/research/sources/d0_record_geometry_2026-10-15/replay.py
```

Первая команда проверяет все 78 открытых исходных текстов и соответствие прежнему capsule. Необязательный `--original-zip /absolute/path/to/original.zip` дополнительно сравнивает все 150 вхождений, вложенные контейнеры и декодированные данные с локальным оригиналом; для обычного чтения и replay этот ZIP не нужен.

Вторая команда повторяет новые проверки: exact second-jet, ранг десять, отрицательные контроли, default/`-O`, три испорченные программы, точный рациональный коэффициент и floating heat diagnostic. Она сравнивает результат с исходным, ничего не записывает в исходники и печатает JSON. Численная таблица не заменяет аналитического доказательства предела.

Исторические точные тождества и конечный резонансный cubic result также можно воспроизвести из текста:

```sh
python 02_REGISTRY/research/sources/d0_record_geometry_2026-10-15/replay_historical.py --output /tmp/d0-historical-fresh
python 02_REGISTRY/research/sources/d0_record_geometry_2026-10-15/replay_historical.py --optimized --output /tmp/d0-historical-fresh-optimized
```

Выходной каталог должен быть новым или пустым. [Адаптер](replay_historical_text.py) проверяет SHA исходников, меняет во временной копии только загрузку ZIP/XZ-зависимостей и поле provenance. Полное математическое тело остаётся побайтно тем же; оно сравнивается с прежними JSON. Протокол и результаты лежат в [validation/historical](validation/historical/adapter_receipt.json) и [validation/historical_optimized](validation/historical_optimized/adapter_receipt.json).

Полный старый interval/full4d replay, Lean build и весь научный CI #310 здесь не заявляются. [Контекстный interval patch](expanded/PRESERVED_INPUT_full4d_exact_sheet/repo/02_REGISTRY/research/sources/d0_full_four_dimensional_sheet_2026-10-15/UPSTREAM_INTERVAL_REPAIR.patch) — только правка конструктора; полный upstream `intervals.py` читается по закреплённой ссылке в [SOURCE_PINS.json](SOURCE_PINS.json). В старом cold-start ответе ссылка на `D0_deep_audit_2026-10-15.zip` ведёт на внешний пакет, **не входящий в переданный ZIP**; она не является зависимостью двух replay выше. Соответствующий текст аудита включён и связан в указателе.

Архивные `IMPORT_INTO_310.py`, `REPLAY_OFFLINE.py`, инструкции применения патчей и старые предложения задач сохранены как источник. Публикационные проверки их не запускают. Они не являются действующей командой новому ИИ.

## Граница результата

Публикация подтверждает сохранность и воспроизводимость указанных конечных проверок. Она не принимает научный материал в CORE, не доказывает physical admission или единый native action, не закрывает родительскую задачу, не выводит причинность/ОТО и не сливает PR. Границы исходного brief и всех прежних результатов сохранены.
