# Заметки фикстуры проводки runner

Это измерение одного изолированного git-репозитория из `RunnerHookTests.test_cli_executes_dependents_and_keeps_unresolved_entries`. Оно не измеряет полный набор `02_REGISTRY/research/certificates` и не является сравнением скорости науки.

Команда фикстуры: `python3 tools/run_research_certs.py --repo <fixture> --ref <head> --base <base> --workers 1 --log-dir <new>`.

Первый отдельный прогон только этого теста: 7 entrypoint, 0.759 с, код 1.

Прогон внутри `python3 tools/test_research_input_closure.py` (15 tests, OK), его и берёт RESULT:

- выбрано entrypoint: 7
- время процесса CLI, включая выбор и изолированные worktree: 0.828 с
- код возврата: 1

`select_certificates` на том же `base..head` вернул `[]`: ни один путь сертификата не менялся. Менялись `shared/owner.py` (`VALUE = 1` → `VALUE = 2`) и `git mv shared/will_move.py shared/moved.py`.

| Случай | Путь | Причины | Исполнение |
|---|---|---|---|
| изменился только общий owner | `dep_a.py` (`import shared.owner`) | `changed-input` | `PASS`, stdout `dep-a 2` |
| транзитивный потребитель того же owner | `dep_b.py` (`import shared.mid`) | `changed-input` | `PASS`, stdout `dep-b 2` |
| независимый сертификат | `independent.py` | не выбран | не исполнялся |
| динамический import | `dynamic.py` (`__import__` неконстантного имени) | `unknown-dependency`, detail `dynamic-import` | `PASS` |
| ошибка разбора | `parse_error.py` (`def broken(`) | `unknown-dependency`, detail `unparsed` | `FAIL` |
| SHA pin не совпал с новым blob | `sha_pin.py`, `PINNED_SHA256['shared/owner.py']` равен hash базы | `changed-input`, `sha-mismatch` | `PASS`; байты pin-файла те же |
| pin снят переименованием | `renamed_pin.py`, `INPUTS = ['shared/will_move.py']` | `changed-input`, `deleted-input` | `PASS` |
| исполняемый сертификат меняет tracked input | `mutator.py` пишет `notes.txt` и импортирует owner | `changed-input` | `MUTATION`; patch worktree содержит `mutated` |
| зелёный job и неуспешный scientific step | объект workflow, не процесс сертификата | шаг `Replay research certificates in isolated worktrees` имеет `conclusion` `skipped` и, отдельно, `failure`, при `job conclusion=success` | `replay=false`, причина `workflow SUCCESS skipped scientific step` |

`provenance_ok=false`, `superset_of_runner=true`, `scientific_replay=false`. `historical-receipt.json` остался байт-в-байт `historical\n`. `notes.txt` исходного репозитория остался `unchanged\n`. После прогона у репозитория один worktree и пустой porcelain.

Отдельно, не эта фикстура: на живом дереве при базе, равной коммиту, `certificate_paths` выбрал 2 из 75 за 2.588 с и не исполнял их. Это `a4d_cartan_nonlinear_rigidity_check.py` и `a4d_closure_packet_integration_check.py`.
