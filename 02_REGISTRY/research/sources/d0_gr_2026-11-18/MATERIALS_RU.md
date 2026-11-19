# Семь исследовательских выпусков D0 за 18 ноября 2026 года

Каждый местный научный файл хранится один раз под читаемым именем. Первичные материалы, дословно доступные в закреплённой версии репозитория, открываются по ссылкам ниже. Предметные результаты и их допущения даны в записках выпусков.

| Выпуск | Основная записка | PDF | Файлов в исходном ZIP |
|---|---|---|---:|
| `00-projective` | [Исходная проективная жёсткость](stages/00-projective/proof_en.txt) | [PDF](stages/00-projective/D0_Projective_Einstein_Rigidity_2026-11-18.pdf) | 13 |
| `01-synthesis` | [Совместная жёсткость и обратная связь](stages/01-synthesis/SYNTHESIS_RU.md) | [PDF](stages/01-synthesis/D0_GR_Synthesis_2026-11-18.pdf) | 10 |
| `02-physical-transfer` | [Физический перенос и детектор](stages/02-physical-transfer/TRANSFER_RU.md) | [PDF](stages/02-physical-transfer/D0_GR_Physical_Transfer_2026-11-18.pdf) | 46 |
| `03-full-source` | [Восстановленная цена и исходный источник](stages/03-full-source/SYNTHESIS_RU.md) | [PDF](stages/03-full-source/D0_GR_Restored_Price_2026-11-18.pdf) | 50 |
| `04-absolute-calibration` | [Абсолютная калибровка и два часа](stages/04-absolute-calibration/SYNTHESIS_RU.md) | [PDF](stages/04-absolute-calibration/D0_GR_Two_Clocks_2026-11-18.pdf) | 75 |
| `05-clock-price` | [Цена часов и конечные записи](stages/05-clock-price/SYNTHESIS_RU.md) | [PDF](stages/05-clock-price/D0_GR_Clock_Price_2026-11-18.pdf) | 61 |
| `06-same-history` | [Одна и та же история и память](stages/06-same-history/SYNTHESIS_RU.md) | [PDF](stages/06-same-history/D0_GR_Same_History_2026-11-18.pdf) | 44 |

Выпуск абсолютной калибровки включает также записку о полной записи. [PDF](stages/04-absolute-calibration/D0_GR_Full_Record_2026-11-18.pdf)

## Как восстановить отдельный выпуск

Команды запускаются из каталога этого реестра в клоне Git с объектами закреплённой ревизии. Нужны Python 3.8 или новее, стандартная библиотека и Git. Номер ревизии и точные смещения каждого опубликованного фрагмента записаны в манифесте. В ином каталоге добавьте опцию `--repo КАТАЛОГ_КЛОНА` перед названием команды.

~~~sh
python3 materialize.py list
python3 materialize.py list 05-clock-price
python3 materialize.py extract 05-clock-price restored-clock
python3 materialize.py zip 05-clock-price restored-clock.zip
python3 materialize.py verify
~~~

Каталог назначения или ZIP должны быть новыми. При распаковке возвращаются исходные имена, файлы и вложенные архивы. Для получения исходного потока ZIP воспроизводятся исходные даты, внешний атрибут записей, порядок и уровень Deflate. Проверка сравнивает SHA-256 и обнаруживает несовместимый компрессор. Побайтовый результат проверен с zlib 1.2.12.

Публичный выпуск абсолютной калибровки использует `python3` вместо частного абсолютного пути в одном поле исторического отчёта. Обновлён соответствующий SHA-256 в описи. Все научные данные, версии библиотек и результаты исходных проверок сохранены. Остальные шесть ZIP имеют исходные SHA-256. Для полного побайтового воспроизведения всех семи владелец исходного отчёта может локально указать старый ZIP калибровки или исходный `diagnostics/TESTS.json`.

~~~sh
python3 materialize.py --historical-calibration ORIGINAL_CALIBRATION.zip verify
~~~

Две независимые распаковки проверили по 299 записей. В историческом режиме совпали все пути, байты и полные потоки семи ZIP. В открытом режиме совпали все пути и 297 исходных файлов. Два изменённых файла относятся к замене одного приватного поля и его контрольной сумме. Описи обоих режимов прошли проверку. [Полный журнал](REPLAY.json) · [Состав и хеши выпусков](manifest.json)

## Материалы, переиспользованные из Git

Всего 263 различных содержательных файла. В деревьях выпусков размещено 235 уникальных копий. Пять файлов и 23 точных фрагмента (240 952 байта) восстанавливаются из существующих объектов. Шесть вложений трёх ранее выпущенных ZIP восстанавливаются из тех же рецептов.

| Первое историческое имя | Вид привязки | Опубликованный источник |
|---|---|---|
| 00-projective / `check_projective_rigidity.py` | фрагмент, 4652 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L191310) |
| 00-projective / `doob_actual_mark.json` | фрагмент, 494 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L193712) |
| 00-projective / `doob_actual_mark.py` | фрагмент, 1423 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L193673) |
| 00-projective / `projective_rigidity_controls.json` | фрагмент, 750 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L191433) |
| 02-physical-transfer / `physical_transfer/primary/native_execution.py` | файл целиком | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py) |
| 04-absolute-calibration / `primary/A67/RawZone.lean` | файл целиком | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/03_FORMALIZATION/D0/Integration/V15/RawZone.lean) |
| 04-absolute-calibration / `primary/B121/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md` | файл целиком | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md) |
| 04-absolute-calibration / `primary/check_complete_143484_stage_clock_cost_selector.mjs` | файл целиком | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/sources/d0_native_two_three_clock_2026-10-20/check_complete_143484_stage_clock_cost_selector.mjs) |
| 04-absolute-calibration / `primary/checkpoint/check_actual_stopped_cost.py` | фрагмент, 5249 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L191635) |
| 04-absolute-calibration / `primary/checkpoint/check_direct_cq_source.py` | фрагмент, 4336 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L191812) |
| 04-absolute-calibration / `primary/checkpoint/check_full128_cq_coframe_residual.py` | фрагмент, 6113 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L191464) |
| 04-absolute-calibration / `primary/checkpoint/check_uniform_book_source.py` | файл целиком | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py) |
| 04-absolute-calibration / `primary/checkpoint/checkpoint_manifest.json` | фрагмент, 1684 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L191276) |
| 04-absolute-calibration / `primary/checkpoint/expected_actual_stopped_cost.json` | фрагмент, 1648 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L191766) |
| 04-absolute-calibration / `primary/checkpoint/expected_direct_cq_source.json` | фрагмент, 7958 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L191908) |
| 04-absolute-calibration / `primary/checkpoint/expected_full128_cq_coframe_residual.json` | фрагмент, 968 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L191609) |
| 04-absolute-calibration / `primary/current_7ga_gb.md` | фрагмент, 94774 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L190221) |
| 05-clock-price / `primary/pinned/7fh_A_literal_NT3.md` | фрагмент, 2188 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L137272) |
| 05-clock-price / `primary/pinned/7fm_A_writer.md` | фрагмент, 2053 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L142391) |
| 05-clock-price / `primary/pinned/7fq_cd13.md` | фрагмент, 4501 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L151810) |
| 05-clock-price / `primary/pinned/7fu_gr_criterion.md` | фрагмент, 7915 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L156244) |
| 05-clock-price / `primary/pinned/7fx_f0.md` | фрагмент, 3507 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L157768) |
| 05-clock-price / `primary/pinned/7gc_retained_reference.md` | фрагмент, 10624 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L192160) |
| 05-clock-price / `primary/pinned/7gd_port_law.md` | фрагмент, 11709 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L192429) |
| 05-clock-price / `primary/pinned/7ge_coherent_normalization.md` | фрагмент, 5307 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L192630) |
| 05-clock-price / `primary/pinned/7gf_composition_replay.md` | фрагмент, 51265 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L192695) |
| 05-clock-price / `proofs/continuum/frozen/check_actual_ledger_row.py` | фрагмент, 6422 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L192911) |
| 05-clock-price / `proofs/continuum/frozen/expected_actual_ledger_row.json` | фрагмент, 5412 байт | [Git](https://github.com/gvakhrushev/d0_15/blob/15f5b786ed912a0e91d660e337bf60a7c15c7cfa/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#L193048) |
