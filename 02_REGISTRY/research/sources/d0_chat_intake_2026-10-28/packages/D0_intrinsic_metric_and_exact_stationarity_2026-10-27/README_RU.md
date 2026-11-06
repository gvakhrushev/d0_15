# Продолжение доказательства D0 / 27 октября 2026

- `SYNTHESIS_RU.md` — содержание и граница доказанного на русском.
- `PROOF.md` — полные формулировки и доказательства, входные источники.
- `check_intrinsic_metric_heat_recovery.py` — самодостаточная проверка.
- `result.json`, `result_optimized.json` — реально полученные результаты.
- `previous_check_replay.json` — повторный запуск предыдущей проверки.
- `MANIFEST.json` — контрольные суммы файлов.

Запуск:

```bash
python -m pip install -r requirements.txt
python check_intrinsic_metric_heat_recovery.py
python -O check_intrinsic_metric_heat_recovery.py
```

Использованы Python 3.13.5, SymPy 1.14.0, mpmath 1.3.0.
В JSON отмечена фактическая версия среды; при другой версии Python это
поле может отличаться без изменения математического результата.

Пакет не объявляет безусловное закрытие ОТО. Он не содержит скрытого
подтверждения native-компиляции, выбора полной цены, общего сеточного
обратного оператора, Lean, CI или мерджа. В GitHub в этом проходе запись
не выполнялась. Исходная версия ветки подтверждена подключённым GitHub:
`c7708742bea04684ffd6aed16774cfdf1b94b129`.
