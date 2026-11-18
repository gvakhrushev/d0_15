# A13 + B27: вход в настоящий native профиль для рабочих регистров

В B27 рассмотрены реальные пары basis labels из A11/B25. Выбранная signed involution уже задаётся исполнимым `X/CX/CCX/Z/CZ` gate list: один invariant membership flag, controlled pair swap и знак на complement, с чистой обратной очисткой. Все 72 192 leaf occurrences покрываются 20 480 различными Choi и512 CAR парами. Внутренний CAR site, RIGHT и внешний PF SITE не отождествляются. Dynamic coherent lookup этих пар из source-DAG/SITE ещё предстоит скомпилировать.

Root воспроизвёл B27 в отдельном дереве с исходным `native_execution.py`: три scripts, шесть восстановленных файлов совпали побайтно. Проверены logical words на всех малых inputs, реальных pair endpoints/complement/padding и суперпозициях; exact native phase/inverse identities — на полном 16-dimensional q/port/Spin space. См. [ROOT_REVIEW_B27.json](ROOT_REVIEW_B27.json).

## 1. Точная операция на неизвестном окружении

В настоящем `G_CX_SOURCE_I` Spin четырёхмерен, `L_i²=-I4`, а `SourceI=diag(I4,L_i)`. Поэтому два последовательных SourceI — точно `Z_port⊗I_Spin`, без предположения о состоянии Spin. Для обычного q и доступного объявленного port:

```
SWAP(q,port); SourceI²; G(port); SourceI²; SWAP(q,port)
     = G_q^-1 tensor I_port tensor I_Spin.
```

Каждый SWAP — три настоящих CX. Итого **11 primitive calls**, включая 6 CX, 4 SourceI и1 G. По дороге port/Spin могут меняться и коррелировать с q; identity утверждается на границе всего macro. На всех промежуточных событиях остаются реальные gates и их цена/отметки. Полное равенство, а не только marginal, позволяет последовательно применять macro к разным q с одним и тем же неизвестным port/Spin.

Для настоящего fresh RAW `v=(sqrt(p),p)` имеем `G^-1 v=|0>`. Тем самым появляется конкретный путь к чистому рабочему регистру. Он требует доступного port/CX маршрута, действительных births v, неприкосновенности oldRIGHT и оплаты всей последовательности. Восстановление уже очищенного q из0 обратно вv, если оно нужно полному графу, является отдельным платным G.

## 2. Подстановка в действительные A13 адреса

`build_native_zero_preparations.py` выпустил **буквальные списки native gates** для всех выходных и рабочих wires трёх selector circuits. Исходные palette/Golden/fair wires остаются произвольными. Вне логической схемы выделены отдельные port, два Spin wires и защищённый oldRIGHT witness. Карта logical→native задана явно; little-endian значение логического регистра не перепутано с MSB-first tensor numbering native checker.

| Decoder | Fresh v targets для output/work | Настоящих gates | CX / SourceI / G |
|---|---:|---:|---|
| internal |1389|15279|8334 /5556 /1389|
| top |1595|17545|9570 /6380 /1595|
| report |118|1298|708 /472 /118|

`NATIVE_ZERO_PREPARATIONS.json` содержит все 34 122 calls и их адреса; исходный native checker подтвердил синтаксический domain каждого word. All-column equality следует композиционно из проверенного B27 macro с различными q; огромные полные матрицы не строились. Требуется1389,1595 или118 реальных births соответственно, но **их physical stage/birth/clock ledger ещё не выдан**. Это три отдельные component preparations, а не полный расписанный report.

Важная деталь owning API: `Execution.blank_wires` означает ввод **computational zero** через `input_isometry`, а не исходного RAW v. Поэтому в выпущенных Execution это поле пусто. Checker проверяет gate word на произвольных полных входах; условие о настоящих v и вывод нулевого scratch записаны отдельно. Подстановка v в поле, которое уже означает0, ошибочно обошла бы требуемую подготовку. Число births не прибавляется к API `expanded_stages`: тот считает только gates. Полная физическая временная шкала должна включить их отдельно по своему owner.

## 3. Сохранённый остаток

Подстановка снимает абстрактную неопределённость операции, которая даёт нулевой scratch при stated port/birth interface. Она не реализует остальные `X/CCX/H` логические gates, не готовит fair bank, не выбирает source-DAG node/copy offsets и не маршрутизирует неизвестный квантовый payload. `CZ` теперь реализована отдельной [exact native конструкцией](NATIVE_CONTROLLED_PHASE_RU.md), без отобранного READY-сектора. Logical first-success в A13 работает только с вычисленными метками. Полная readiness, retained history/marks, readers/seal и original clock остаются невычисленными.

Физическое Cost−Info `C` не отождествлялось с этим gate count или decoded probability. Полное native-source→Book03 сопоставление, затем dynamics/refinement остаются частью цели ОТО. `GR_closed=false`.
