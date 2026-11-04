# Обновление compiled inventory C0 — 4 ноября 2026

После нового Lean-модуля и его публичного импорта собран inventory шести владельцев трёх C0-срезов на чистом `254890361d19795096bc6a741f6f6f03b160ae0e`. Сборщик использует `D0.All` и имеющийся кэш, проверяя источники до и после извлечения. Получены 482 декларации; их содержание совпадает с предыдущим inventory. SHA-256 `declarations.json`: `8f811ecad4a34d479ef773a5eb6583de7bbc471f00038408d05af3770dfba2c2`; digest Lean-источников `d5809e0d4ad3bf094571fbcbbaa566a7e94b84fcf3963b2f6ec7bee7cc51baa9`. Семантическое принятие C0 не оценено; `GR_closed=false`.

Команда:

```sh
python3 tools/lean_declaration_inventory.py --module D0.Foundation.FutureExecution --module D0.Foundation.VerificationCore --module D0.Foundation.UncoupledCenterRawWitness --module D0.Foundation.FutureShortlexAdapter --module D0.Foundation.VerifiabilityNecessity --module D0.Foundation.TheoryTransfer --output /tmp/d0-c0-three-slices-inventory-254890361.json
```
