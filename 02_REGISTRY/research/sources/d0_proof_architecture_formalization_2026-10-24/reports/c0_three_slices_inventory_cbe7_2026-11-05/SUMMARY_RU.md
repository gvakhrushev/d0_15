# Compiled inventory после композиции амплитуды — 5 ноября 2026

На чистом `cbe7de75dbc92273db10dfaabf7e3d31fdf9f204` извлечены шесть C0-владельцев из `D0.All` с существующим кэшем. Все 482 декларации по содержанию совпадают с предыдущим inventory; proof details собраны. SHA-256 `declarations.json`: `56268d2c32e779c79c1f4eab072c17e09c720ed33367fc4b3759a07e1e9db49c`; digest Lean-источников `55b3182ae142d1cef14648a1213368b604ba0a7f19e4ab74d6968000fc5613b0`. Семантическое принятие C0 не оценивалось; `GR_closed=false`.

```sh
python3 tools/lean_declaration_inventory.py --module D0.Foundation.FutureExecution --module D0.Foundation.VerificationCore --module D0.Foundation.UncoupledCenterRawWitness --module D0.Foundation.FutureShortlexAdapter --module D0.Foundation.VerifiabilityNecessity --module D0.Foundation.TheoryTransfer --output /tmp/d0-c0-three-slices-inventory-cbe7de75d.json
```
