# Подключение принятого селектора к runner исследовательских сертификатов

Task: `WRK-A4D-RESEARCH-CLOSURE-RUNNER-WIRING`
Статус: candidate. Это проводка уже принятого правила выбора, не новая физическая посылка и не вывод ОТО.
Схема селектора не менялась: `research-input-closure/1`.
Модуль выбора: `tools/research_input_closure.py` (не переписывался).
Runner: `tools/run_research_certs.py`.
Контроли: `tools/test_research_input_closure.py`.
База ветки при открытии: `2d63cfe4ab60838315fef55f54c6cb90c6d86eff`.

## Граница, которая теперь вызывается

`run_research_certs.main` больше не отдаёт replay список из `select_certificates`. И для `--base`, и для `--all` список entrypoint берётся одной строкой:

```python
certs = __import__("research_input_closure").certificate_paths(args.repo, commit, base)
```

`select_certificates` оставлен узким diff имён `02_REGISTRY/research/certificates/**/*.py`. Его вызывает сам селектор и поднимает `RuntimeError`, если выборка уже этого diff. Неразрешённая зависимость не сужает replay: сертификат с `unknown` остаётся в списке при любой базе, даже когда diff не задевает уже названный вход.

Новый runner, кеш, диспетчер и очередь не добавлялись. Логи по-прежнему только свидетельство. Историческая квитанция не открывается на запись. Pin и исходник при `sha-mismatch` не переписываются. Ненулевой код runner по-прежнему означает, что хотя бы один исполненный статус не `PASS` (`FAIL`, `MUTATION`, `TIMEOUT`, `ERROR`, `CANCELLED`).

`.github/workflows/guards.yml` получил только запуск `python tools/test_research_input_closure.py` в шаге Fast tooling controls. Имя шага `Replay research certificates in isolated worktrees`, Draft/Ready/main, timeout, permissions, concurrency и cache не менялись.

## Что выбирается на живом дереве

Чтение коммита ветки до этой проводки, база равна тому же коммиту, только выбор, без исполнения. `certificate_paths` вернул 2 entrypoint из 75 за 2.588 с. Узкий `select_certificates` вернул пустой список.

- `a4d_cartan_nonlinear_rigidity_check.py` с коммита #200 заканчивался не-Python строкой `H=` и символом U+00B8. Из-за `unparsed` селектор выбирал его при любой базе, и runner останавливался до уже написанных контролей. Удалена только эта строка. Существующие `check(...)` после этого проходят локально; вычисленный `S0` по-прежнему ни с чем не сравнивается и новой теоремой не объявляется. На пустом diff файл больше не входит в выборку.
- `a4d_closure_packet_integration_check.py`: `unknown-dependency` и три `dynamic-import` (`path`, `read`, `sha256`), как в уже принятом описании селектора. На пустом diff он остаётся выбранным.

Полный научный набор не прогонялся. Ускорение полной науки не утверждается. На `--base` эти два неразрешённых сертификата входят в replay даже если изменённый файл не является их названным входом; относительно старого diff имён это расширяет, а не сокращает работу.

## Фикстура CLI → выбор → изолированный worker

Маленький реальный git-репозиторий, один процесс `python3 tools/run_research_certs.py --base <base> --workers 1`. Первый отдельный прогон теста: 7 entrypoint, 0.759 с, код 1. Прогон внутри полного модуля: **7 entrypoint, 0.828 с, код возврата 1**. В отчёт берётся прогон полного модуля. Подробная таблица: [FIXTURE_NOTES.md](FIXTURE_NOTES.md).

Узкий filename diff на этом диапазоне пуст. Hook исполнил оба сертификата, которые импортируют изменившийся `shared/owner.py`, и не исполнил независимый. Динамический import, синтаксически нечитаемый модуль, несовпавший SHA и переименованный pin остались в выборке. Сертификат, который пишет в отслеживаемый `notes.txt`, получил `MUTATION` внутри worktree. `historical-receipt.json` и `notes.txt` исходного репозитория не изменились. Job с заключением `success` и scientific step `skipped` либо `failure` не является replay: причина ровно `workflow SUCCESS skipped scientific step`.

## Проверки этого среза

- `python3 -m compileall -q tools`
- `python3 tools/test_research_input_closure.py`: 15 tests, OK
- `python3 tools/test_run_research_certs.py`: 11 tests, OK
- `python3 tools/test_ci_replay_reuse.py`: 17 tests, OK

Прежние отказы provenance, запрет перезаписи квитанции и проверка надмножества filename diff сохранены. Удалено только устаревшее ожидание, что runner и workflow не содержат этот селектор.

## Куда это входит у родителя

Приёмка #334 и следующих source-slice может считать, что `--base` существующего runner запускает потребителей изменённого общего входа, а не только сертификат, чей собственный путь попал в diff. Неразрешённый сертификат при этом не пропускается. Физическая посылка родителя этой проводкой не снимается.

## Оставшийся блокер

Неразрешённый `a4d_closure_packet_integration_check.py` по-прежнему входит в каждый `--base` replay. Его сужать нельзя. Хвост `S0` сертификата Картана не получил утверждения: это незаконченный фрагмент исходного файла, не новый результат.
