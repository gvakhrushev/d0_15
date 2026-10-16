# Селектор потребителей по изменившимся входам сертификатов

Task: `WRK-A4D-CERTIFICATE-INPUT-CLOSURE`
Schema: `research-input-closure/1`
Модуль: `tools/research_input_closure.py`
Контроли: `tools/test_research_input_closure.py`
База ветки: `a97735a78ed0295d2e499078232d380bad26f20a` (main после слияния #324).

Это правило выбора проверок. Оно не меняет физическое действие, след, норму, входную гипотезу или ссылку и не добавляет claims. Оно не утверждает гравитационный результат.

## Правило выбора

Индекс читается только из одного коммита: `git ls-tree -r -z` и `git show <commit>:<path>`. Рабочее дерево и старые квитанции не открываются на запись.

Сертификат — каждый путь `02_REGISTRY/research/certificates/**/*.py` в дереве этого коммита. Удалённый сертификат в выборку не входит: множество entrypoint при `--all` совпадает с `run_research_certs.select_certificates`. Если при заданной базе runner возвращает путь, которого нет в этой выборке, селектор поднимает `RuntimeError` и не сужает существующую проверку.

Непосредственный вход сертификата или другого `.py` собирается статически:

- `import` и `from ... import`, включая относительный импорт и поиск рядом с импортёром. Если путь есть в дереве репозитория, он побеждает одноимённый внешний модуль.
- Корни стандартной библиотеки (встроенные модули, `sys.stdlib_module_names` при наличии, каталог stdlib и `lib-dynload`) и корни `requirements.txt` не являются входами репозитория.
- Явные списки `INPUTS`, `VALIDATION`, `PINS`, `PINNED`, `PINNED_INPUTS`, `PINNED_PATHS`.
- Карты `PINNED_SHA256`, `INPUT_SHA256`, `PINNED_COMMITS` и прочие модульные словари `*_SHA256`. Скаляр `NAME_SHA256` связывается с путём `NAME`, `NAME_RELATIVE` или `NAME_PATH`.
- Ключ-имя без слэша присоединяется к каталогу из цикла `for name in MAP` / `DIR / name` или `os.path.join`. Если каталог неоднозначен, именованная карта даёт `unresolved-pin`, а не угаданный путь.
- Загрузчики: `__import__`, `import_module`, `spec_from_file_location`, `runpy.run_path`, аргумент `filename` у `compile`, `open`, `read_text`, `read_bytes`.
- Прямые присваивания в теле функции, которые сворачиваются из модульных констант. Параметр подставляется с константных мест вызова, по цепочке вызывающих не глубже 4. Несколько параметров, каждый из которых разворачивается больше чем в одно значение, остаются неразрешёнными.
- Метка `compile`, которая не выглядит как путь (`census`, суффикс `:A0`), не является отдельным файлом. Суффикс после `:` возвращает уже найденный путь.

Транзитивное замыкание идёт только по `.py`. Цикл по уже посещённому пути пропускается. `unknown` вложенного модуля переносится с полем `via`.

Имя без слэша, которого нет в дереве и рядом с текущим файлом, считается именем временного cwd и не объявляется удалённым входом. Путь со слэшем из явного списка, pin или загрузчика, которого нет в дереве, остаётся `deleted-input`.

Сравнение путей — `git diff --name-only -z --no-renames <base> <commit>`. Сертификат выбирается, если есть хотя бы одна причина:

| Причина | Условие |
|---|---|
| `full-snapshot` | база не задана: выбирается каждый сертификат |
| `changed-entrypoint` | путь самого сертификата есть в diff |
| `changed-input` | путь любого транзитивного входа есть в diff |
| `deleted-input` | blob входа на коммите отсутствует, либо blob по `pin_commit` отсутствует |
| `sha-mismatch` | `pin_sha256` не равен SHA-256 blob, либо blob по `pin_commit` отличается |
| `unknown-dependency` | остался хотя бы один свой или транзитивный `unknown` |

`sha-mismatch` и `deleted-input` одновременно выбирают сертификат и делают `provenance_ok` ложным. Байты pin и исходников не переписываются.

Выбор и исполнение разделены. `select` ставит `ran=false` и `scientific_replay=false`. Исполнение вызывает существующий `run_research_certs.run_certificate` в новом каталоге. Повторное использование каталога и `write_exclusive` по уже существующему файлу отвергаются (`O_EXCL`). Если переданные байты исторической квитанции изменились, исполнение поднимает ошибку.

`workflow_replay` истинен только когда заключение job равно `success`, шаг `Replay research certificates in isolated worktrees` ровно один, его статус `completed` и заключение `success`. Иначе при job `success` причина ровно `workflow SUCCESS skipped scientific step`. `scientific_replay` истинен только если этот workflow-объект, когда он передан, допускает replay, исполнение действительно запускалось и каждый статус равен `PASS`. `MUTATION` не является replay. Зелёное имя workflow без выполненного шага не является replay.

## Что остаётся консервативным

Неразрешённое не пропускается: сертификат с `unknown` входит в выборку при любой базе, даже если diff не задевает уже названный вход.

- Синтаксически нечитаемый модуль даёт `unparsed`. На этом дереве так остаётся `a4d_cartan_nonlinear_rigidity_check.py`: исходник не редактировался.
- Загрузчик, аргумент которого не сворачивается в константу, даёт `dynamic-import`. Голый `exec`/`eval` тоже, кроме `exec(compile(...))` и случая, когда каждое имя в аргументе уже связано на уровне модуля.
- Импорт, который не найден в дереве и не является внешним корнем, даёт `unresolved-import`.
- Неоднозначный или несворачиваемый pin даёт `unresolved-pin`.
- Функция без единого места вызова не помечается `unknown`: мёртвый помощник не создаёт ложный вход.
- На живом дереве `a4d_closure_packet_integration_check.py` сохраняет три честных `dynamic-import`: `runpy.run_path` временной копии, чтение временного результата и вызов `sha256(SOURCE_DIR / name)` с переменной цикла. Четыре файла `INPUT_SHA256` и `COEFFICIENTS_SHA256` при этом записаны как pin и на прочитанном коммите имеют статус `match`. Временное имя `haq_coefficients.json` не объявляется удалённым входом репозитория.

На чтении дерева `cf5a3aa93d64a6de3856d7914e72e0a0fde42463` (тот же набор сертификатов, что у `a97735a`): 75 сертификатов, множество совпадает с runner, `provenance_ok` истинен, `scientific_replay` ложен, tracked porcelain не изменился. Статусы provenance: 15 `match`, 54 `unpinned`, ноль `deleted-input` и ноль `sha-mismatch`. Строки `match`:

- closure packet: `d0_a4d_closure_certificate.py` `cf87dcd06951`, `d0_a4d_closure_results.json` `8758fdd5ea96`, `a4d_slow_lift_reconstruction_check.py` `2a7ef4720ec6`, `d0_a4d_slow_lift_result.json` `ebe9a53f88fc`, `a4d_haq_coefficientwise_identity_coefficients.json` `e106d8937fad`;
- HAQ identity: `a4d_metric_null_hessian_complex_check.py` `d7707248af8a`;
- q0 germ tower: metric owner `d7707248af8a`, coefficient ledger `e106d8937fad`, physical owner `a3e02e378f35`, Gram owner `c794f7f87e35`;
- resonance checkpoint: пять json `2ea7e71d2ab0`, `f4e97cfb2458`, `a64cd8c8b3d0`, `c90d95da46f6`, `94e5a24837d3`.

Два сертификата несут `unknown-dependency`: нечитаемый Cartan и пакет closure с временными загрузчиками. Оба остаются в выборке.

## Решающие контроли

Изолированный репозиторий фикстуры, без переписывания исторических квитанций:

1. Изменён только импортируемый owner: потребитель выбран, `select_certificates` runner возвращает пусто.
2. Несовпавший `PINNED_SHA256` и несовпавший `PINNED_COMMITS`: статус `sha-mismatch`, `provenance_ok` ложен, байты файла не подменяются под pin.
3. Удалённый путь из `INPUTS`: потребитель выбран, runner пуст, статус `deleted-input`.
4. `__import__(sys.argv[1])`: при изменении постороннего `notes.txt` сертификат выбран по `unknown-dependency`. Разрешённый `import shared.owner` при том же diff не выбран.
5. Сертификат пишет в отслеживаемый `notes.txt`: статус исполнения `MUTATION`, `historical-receipt.json` неизменен, повтор каталога и запись поверх квитанции дают `FileExistsError`.
6. Job `success` с пропущенным или отсутствующим scientific step: replay ложен, причина `workflow SUCCESS skipped scientific step`. Успешный шаг и статусы `PASS` дают replay. `ran=false` и `MUTATION` не дают.

## Строка, которая не применена

`tools/run_research_certs.py` и `.github/workflows/guards.yml` не изменялись и не упоминают этот модуль. Владелец #324/M01 может в `run_research_certs.main` заменить

```python
certs = select_certificates(args.repo, commit, base)
```

на

```python
certs = __import__("research_input_closure").certificate_paths(args.repo, commit, base)
```

Запуск `python tools/run_research_certs.py` кладёт каталог `tools/` в `sys.path`, поэтому импорт резолвится без правки CI. Пока строка не стоит в runner, выбор #324 по-прежнему видит только изменённый entrypoint и пропускает изменение одного импортируемого owner. Новые фикстуры этого модуля локальны: workflow по-прежнему гоняет только `test_task_dispatch.py`, `test_run_research_certs.py` и `test_ci_replay_reuse.py`. `python -m compileall -q tools` видит синтаксис нового модуля.

## Прочитанный источник, не влитый

Pin `dfaf7c8df509d5abd83fa60a185ad530feadc9b5` читался через `git show` и на эту ветку не переносился. Оба файла отсутствуют в рабочем дереве.

`A4D_NATIVE_PREPARATION_FACTOR_SHEAR.md` сам обозначает статус: «exact cross-owner first-jet test for one corrected golden-determinant/AF-price route. It is not a native-action or GR theorem.» Это плоская factor-shear проба.

`A4D_COHERENT_COMPILATION_COST_DESCENT.md` сам обозначает статус: аналитические операторные и ссылочные утверждения, конкретное AF-построение и точные конечные проверки. Раздел 8 там назван условным гравитационным синтезом, не установленным физическим действием и не утверждением GR. Внутренний pin заметки `8d6f73012c3740d3b4113ef43ab71cb4986b9782` здесь заново не проверялся. #310, #202 и #317 не закрываются.

## Куда это входит у родителя

M01 принимает конкретный срез по списку файлов, SHA входов, команде и истинному/пропущенному/упавшему CI. Этот селектор даёт такой список для исследовательских сертификатов: изменение общего исходника без изменения entrypoint включает потребителей, а зелёное имя workflow или diff только entrypoint не считается полной проверкой зависимостей. Физическая посылка среза этим не снимается.
