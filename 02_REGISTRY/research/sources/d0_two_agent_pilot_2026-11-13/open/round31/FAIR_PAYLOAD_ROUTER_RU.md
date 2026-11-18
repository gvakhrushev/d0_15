# B31. Когерентная маршрутизация первого успешного fair payload

**Результат:** построен конечный cap-28 bank из исходных parity-kernel attempts и фиксированного логического router. Он выполняет **все 28 попыток**, сохраняет каждую failure/success ветвь, её `B,C` и отдельную one-hot метку первого успеха; выбранный quantum payload переносится в подготовленный output управляемым SWAP, а временные survival-биты очищаются. На идеальном успешном checkpoint полный output точно факторизуется как `|+>_out tensor retained_environment`, включая когерентную суперпозицию всех success patterns и произвольный внешний `D/oldRIGHT`.

Предъявлены исполнимый [логический gate list](LOGICAL_FAIR_ROUTER.json), реальные native слова подготовки и исходных 28 kernels, а также конечный [native router DAG с literal raw inverse](NATIVE_FAIR_BANK.json), использующий проверенные A14 approximants. Для одной готовой реализации ideal success вероятность

```
q_28=1−(1−2p³)^28 = 0.999999982993369353898666736181... .
```

При A14 error `<=2^-4096` каждый физический router отличается от идеального на всех входных колонках не более `59·2^-4096`; exact factorization/one-hot относятся к идеальному target, для приближённого результата ниже даны отдельные оценки. Не заявляются полный `alpha_h`, готовый source dispatcher, полный birth/mark/clock ledger, физическое `C` или GR. `GR_closed=false`.

## 1. Потреблённый owned kernel и все его ветви

Исходный paid parity source из `PAID_CODE_AND_MOMENT_WRITER.md` §2 и §7c171 owner действует на **трёх computational-zero** wires, chronological order:

```
G(A); G(B); CX(A,C); CX(B,C); CX(A,B).
```

`p=(sqrt(5)−1)/2`, `a=sqrt(p)`. Его исходное полное состояние на `|000>` вычислено точно в owning Golden field, без отбора failure:

```
p |000> + p² |100> + a p |011> + a p |111>
 = (p|0>+p²|1>)_A |0>_B|0>_C
   + sqrt(2p³) |+>_A |1>_B|1>_C.                  (1)
```

Следовательно `C=1` — success с `s_F=2p³`, `B=1` — его **сохраняемый** известный byproduct, и payload уже ровно `|+>=(|0>+|1>)/sqrt2` с одинаковыми знаками. Дополнительного correction ни для одной successful ветви этого конкретного kernel нет. При `C=0` сохраняется вся ненормированная failure state из (1); её probability `p²+p⁴=1−2p³=3−4p`. Все восемь full-input колонок конкретного native `2G+3CX` word проверены; у нас нет права подменить неопределённый вход на `|000>` без реальной подготовки.

Для каждой из 28 attempts заново создаются отдельные `A_i,B_i,C_i`; все kernel calls выполняются независимо от более ранних flags. Банк должен иметь достаточное разрешённое fresh-WORK пространство и исходный `SourceI` port/Spin, без воздействия на защищённый oldRIGHT. Из-за этой фиксированной схемы значения остальных попыток не отбрасываются после первого success.

## 2. Реальный квантовый output и точный логический gate list

В [fair_router.py](fair_router.py) `K=28` выдаёт 143 logical wires:

* 84 wires трёхполосных attempts;
* один output и один XOR-ready;
* 29 очищаемых `survive` и 28 сохраняемых `chosen` one-hot records.

На входе output, ready, survive, chosen подготовлены в computational zero для требуемого fair-resource checkpoint; сам gate list определён на произвольном input output/ready и на произвольных attempt payloads при clean survive/chosen. Вычисляется

```
survive_0=1,
chosen_i=survive_i AND C_i,
survive_(i+1)=survive_i XOR chosen_i = survive_i AND (NOT C_i).
```

Затем `ready xor=1−survive_28`. Если success есть, ровно один `chosen_i=1` соответствует первому `C_i=1`. Для каждого i выполняется настоящий logical Fredkin, разложенный как

```
CX(A_i,out); CCX(chosen_i,out,A_i); CX(A_i,out).
```

На выбранной ветви он **обменивает** `A_i` с output; исходное значение output остаётся в сокете `A_i`, а остальные attempts нетронуты. При отсутствии success output сохраняется. После всех 28 controlled swaps, в обратном порядке `survive_(i+1) xor=chosen_i xor survive_i`, затем `survive_0 xor=1`; все 29 survival-битов чисты, а готовый one-hot `chosen` и все `B,C` остаются. `C_i` после kernel не становится target; ни внешний `D`, ни oldRIGHT не участвуют.

Counts одного cap-28 router точно `X=3`, `CX=169`, `CCX=56`, всего **228 logical gates**. Формула для произвольного cap K: `X=3`, `CX=6K+1`, `CCX=2K`, итого `8K+4`. Входной output не сбрасывается и не измеряется. Альтернатива `CX(A_i,out)` для `|+>_A|0>_out` давала бы Bell state с output marginal `I/2`; hostile-control проверяет, что это не независимый `|+>`.

## 3. Почему success-factorization истинна когерентно

Пусть `s=(C_0,...,C_27)` — **не измеряемые** flag wires после 28 disjoint preparations, а `i(s)` — первая единица. На каждом selected site `C_i=1` у исходного kernel имеется точная factorization `sqrt(2p³)|+>_{A_i}|1>_{B_i}`. Унитарный first-success router действует диагонально по оставленным `C` и для каждой строки `s!=0` переносит этот `|+>` в заранее нулевой output. Следовательно на произвольной внешней очищенной истории `|psi>_D`:

```
Pi_(ready=1) U_ideal ( |v>_fresh^tensor143 tensor |psi>_D )
  = |+>_out tensor |E_success(psi)>_all_retained,
||E_success(psi)||² = q_28 ||psi||².                    (2)
```

В `E_success` остаются все source C/B, все невостребованные payloads, selected прежний socket `|0>`, точный one-hot выбранного attempt, а также все прежние дополнительные факторы. Сумма по разным `s` остаётся когерентной; ни failure, ни branch label не трассируется и не заменяется одним сообщением. Ортогональность разных сохранённых `C` и независимая исходная подготовка kernels дают `q_28=1−(1−2p³)^28`. На `ready=0` output остаётся в `|0>`, все попытки неуспешны и records сохранены. (2) относится к **одному конкретному checkpoint**; после того как потребитель допустимо взаимодействует с output, он может его запутать с другими системами.

[check_fair_router.py](check_fair_router.py) проверил все `18 720` data/control входных колонок малых `K=1..4`, все `8 190` success patterns для `K=1..12`, 2 055 характерных/random patterns `K=28`, и точное покомпонентное попарное равенство коэффициентов `p^u a^v` успешного когерентного состояния для всех `K=1..6` (`5 334` компонент). Это дополняет указанное индукционное доказательство для всех `2^28` patterns; они не перечислялись по отдельности.

## 4. Фактическая native рамка, обратный word и цена

Все 143 логические wires требуются как реальные fresh RAW births `v=(sqrt(p),p)`. Для каждого отдельного q зафиксирован B27/A13 exact full-column native word `G_q^-1` через тот же доступный port:

```
SWAP(q,port); SourceI²; G(port); SourceI²; SWAP(q,port),
```

то есть `6 CX + 4 SourceI + 1 G = 11` gates; он преобразует настоящую свежую `v` в `|0>`, а произвольные entangled port/Spin возвращает точно на своей границе. В `Execution` оставлено `blank_wires=()`: этот API означал бы уже computational zero, а не RAW birth. Затем раскрыты именно 28 буквальных kernels (56 G, 84 CX). [NATIVE_FAIR_BANK.json](NATIVE_FAIR_BANK.json) содержит прямой список всех `1 713` таких native gates и его буквальный paid inverse из `3 989` calls; в счёт gates **не** включены 143 рождения, и physical birth/clock ledger ещё должен быть включён по владельцу.

A14-контролируемые X/CCX подставлены в все 228 операций router с общим ordinary arbitrary auxiliary, отдельными port и двумя Spin wires, защищённым oldRIGHT. Пусть `k` — зафиксированный A14 4 111-bit integer. Действительные DAG inventories:

```
                    G             CX                 SourceI        total
router forward      684k          3995               1350           684k+5345
router raw inverse  684k          2088k+3995         2736k+4050     5508k+8045
bank forward        684k+199      4937               1922           684k+7058
bank raw inverse    684k+199      2088k+5273         2736k+6562     5508k+12034
```

Строки включают буквальные native gates, но не включают 143 birth stages, аллокацию/права на port, Spin и auxiliary, последующего потребителя, seal и полную физическую временную шкалу. Математический inverse списывает каждый исходный primitive, в частности (G^{-1}) и SourceI^-1, и допускается только там, где реальные flags/work ещё живы и не стали защищённой immutable записью; он не обращает сами рождения. Неоплаченного reset или повторного использования approximate CCX как собственного обратного нет.

[check_native_bank_structure.py](check_native_bank_structure.py) независимо сверил все `1 713` prefix и `3 989` обратных gate calls, восстановил literal raw inverse всего router DAG, пересчитал symbolic counts и просмотрел `6 020` syntactic leaves; `C_i,B_i` после kernel не являются targets, oldRIGHT ни разу не адресован. Huge DAG по k не раскрывался. В дополнение [check_small_native_router.py](check_small_native_router.py) выполнил small `k=1`, `K=1,2` native routers и буквальные inverses на 32 произвольных колонках, включая dirty auxiliary, port, Spin и scratch; это float diagnostic, не huge-word execution.

## 5. Readiness только fair-компонента и ошибка реальной подстановки

[certify_fair_readiness.py](certify_fair_readiness.py) точно использует `1−2p³=3−4p<53/100`. На идеальном checkpoint `q_28>1/2`. Если A12 `M=10 248 262` fair ресурсов на report порождены **отдельными копиями** этого фиксированного bank, с сохранением всех READY records до их совместного predicate, то

```
alpha_fair,ideal = q_28^M > 3/4.
```

Это lower bound только для fair-bank части; размещение/права и другие READY components ещё не объединены. Подстановка A14 даёт для одного полного bank на всех входных/aux columns

```
eta_bank <= (3+56) 2^-4096 = 59·2^-4096 < 2^-4090,
|Pr_hat(ready)−q_28| <= 2 eta_bank.
```

Для любого внешнего input, включая purification и auxiliary, нормированное фактическое состояние на `ready=1` находится на trace distance не более `2 eta_bank/sqrt(q_28)` от **некоторого конкретного идеального** `|+><+|_out tensor rho_E`; поэтому приблизительная схема не выдаётся за exact unentangled output. Реальный `chosen`, survival и ready могут содержать настолько малый остаток; он не удаляется вручную.

При последовательной подстановке `M` таких bank DAG на disjoint RAW births с общим arbitrary auxiliary весь all-column error `<=59 M·2^-4096<2^-4066` на report; для семи таких report `<2^-4064`. Их реализация и общий graph должны быть предъявлены отдельно, а совпадающая exact alpha для approximate word не предполагается. На случае, где все `M` banks сначала подготовлены и их READY flags сохранены до общего projector, результат даёт соответствующую uniform lower bound `Pr_hat(all fair ready) > 3/4−2^-4065`; он не включает остальные selector/processor READY flags. Эти расчёты нельзя умножить на новый независимый factor после включения тех же A12 fair banks второй раз.

## 6. Проверка, воспроизведение и остаток

```
OPENBLAS_NUM_THREADS=1 python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round31/check_fair_router.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round31/build_native_fair_bank.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round31/check_native_bank_structure.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round31/certify_fair_readiness.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round31/check_small_native_router.py
```

Все скрипты пишут только в `open/round31`; входные A14/A12 и owner остаются read-only. [RECEIPT.json](RECEIPT.json) закрепляет все inputs/outputs. Остаются полные physical RAW births и ограничения порта, реальное размещение многочисленных bank copies, source-DAG dispatch и потребитель output, полная единая готовность, marked prefix/readers/seal и действительная цена/clock. Затем требуется отдельная связь с физическим Cost−Info и геометрическим источником; GR здесь не закрыта.
