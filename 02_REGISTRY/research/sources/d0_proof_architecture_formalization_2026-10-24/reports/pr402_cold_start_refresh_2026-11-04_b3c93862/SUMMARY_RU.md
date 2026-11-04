# Cold-start refresh PR #402 — `b3c93862`

## Результат

Полный runner завершился с кодом 0 на чистом снимке PR #402
`b3c9386221fa7c382ff98479f447e61d70b4c68a`. В окне 18 поиск нашёл все обязательные источники в **49 из 50** сценариев;
benchmark содержит **51** контроль, включая regression изменения источника против посторонней прозы.

## Kappa owner delta

- **17/17** query-specific locator файлов найдены.
- В strict direct-content поиске найдено **23/67** доступных owner-текстов; ещё **44/67**
  загружены по exact Git pin, но не содержат достаточно совпавших терминов данного запроса.
- Отдельная exact-pin regression сверяет все **68** изменённых путей PR #334 по
  `commit:path` Git blob, числу байт и SHA-256; oversized memo остаётся pin-only.

Поэтому этот case остаётся неполным: точность и наличие пинов не объявлены полнотекстовой
discoverability. Никакой порог поиска или scope источников не ослаблялся.

## Lean-интеграция

Узкая сборка `D0.Analysis.MovingProjectorBookPriceDensityBridge` прошла **3279 Lake jobs**
на Lean 4.30.0. Для `D0.All` wrapper распознал уже имеющийся успешный final receipt с
точно теми же source, dependency и environment SHA-256; он сообщил `SKIP`, а не запускал
ещё одну неизменённую полную сборку. Квитанция сохранена в
[`lean_build_receipt.json`](lean_build_receipt.json).

## Provenance и границы

Полный stdout runner: 25,393,708 байт, SHA-256
`0be645fd64d35d304a565e17d73adcbf36b3b077f127db9287ab583c09c4c8f2`; оставлен локально вне Git. Компактная воспроизводимая сводка: 2,825,869 байт,
SHA-256 `2f392ff91a0f1ebd583f368bdf01885dafd7e989a80861894a70589e6f0e35c8`. Полные receipts сценариев и привязка к source snapshot находятся
в [`cold_start_summary.json`](cold_start_summary.json); команды, входные хэши и пределы проверки —
в [`replay_manifest.json`](replay_manifest.json). Компактор проверяет целостность и snapshot
входного stdout, но сам runner не перезапускает.

Lean-результат формализует конечную матричную цену и её moving-projector источник.
Он не выбирает физическую цену или admitted execution. `GR_closed=false`; статус PR #334
не изменён.
