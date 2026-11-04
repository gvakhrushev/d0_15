# Compiled inventory после дифференциала Фреше — 4 ноября 2026

На чистом `ef0c2561b9aceb6fa17f73451d08973b3ee82dbf` извлечены шесть C0-владельцев из `D0.All` с существующим кэшем. Все 482 декларации по содержанию совпадают с предыдущим inventory; proof details собраны. SHA-256 `declarations.json`: `0b343b9ef9248708f328522c439b1d5f2f6b45b50a5f72e4d7800132f1bf0567`; digest Lean-источников `8160cbb6faccf39f5cf87252a2be17d9439c30bdf880cfe35c9f102a57779f34`. Семантическое принятие C0 не оценивалось; `GR_closed=false`.

```sh
python3 tools/lean_declaration_inventory.py --module D0.Foundation.FutureExecution --module D0.Foundation.VerificationCore --module D0.Foundation.UncoupledCenterRawWitness --module D0.Foundation.FutureShortlexAdapter --module D0.Foundation.VerifiabilityNecessity --module D0.Foundation.TheoryTransfer --output /tmp/d0-c0-three-slices-inventory-ef0c2561b.json
```
