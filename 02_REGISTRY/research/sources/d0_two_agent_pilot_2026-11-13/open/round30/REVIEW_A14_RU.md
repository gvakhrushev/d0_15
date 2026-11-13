# B30. Независимая ограниченная проверка A14 native lowering

**Результат:** существенной ошибки в предъявленных A14 математике, сертификате фиксированного показателя или пооперационной подстановке в пять схем A13 не обнаружено. При stated профиле `G/CX/SourceI`, доступном port и отдельно выделенном ordinary auxiliary предъявленные X, H и CCX имеют full-column error `<=2^-4096` и точную identity на protected oldRIGHT. Временная rootlike копия повторила certificate для **заданного** `k`, exact small-word checker и lowering; три выходных JSON совпали побайтно. Candidate CF/mpmath-search не запускался и в доказательство не входит.

Это проверка конечных native **грамматик**, цен и математических ограничений. Слово с 4 111-битным repeat count не разворачивалось и физически не исполнялось. Полные source-DAG dispatch, payload, все births/marks/clock, полная target `alpha_h`, физическое `C` и GR остаются открытыми. `GR_closed=false`.

## 1. Алгебра селективного вращения и неизвестный auxiliary

Owner [native_phase/PHASE_COMPILER.md](../../../d0_native_readiness_amplification_2026-10-24/PHASE_COMPILER.md) уже доказывает parity/Walsh identity и иррациональность исходного угла. При прочих допустимых ordinary controls и target она даёт

```
product_S CX_S G_target^[(-1)^(v·S) k] CX_S
  = R_target(2^K k theta P_v).
```

Независимая целочисленная проверка `336` control/pattern комбинаций для `K=2,3,4` подтверждает Walsh-сумму: она равна `2^K` только на выбранном pattern и нулю на остальных. Старый `phase_word` API требует declared fresh blank, однако само равенство матриц работает на **всех** колонках target; A14 переносит именно это доказательство и не записывает мнимый blank в `Execution`. Допуск конкретного реального порта и графа по-прежнему необходим.

При `alpha=4k theta`, `J=[[0,-1],[1,0]]`, `Z=diag(1,-1)` A14 использует

```
X_hat=R(4k theta) Z,        H_hat=R(2k theta) Z,
CCX_hat=R_t(alpha P_11) R_aux(2 alpha P_111).
```

Порядок справа налево означает, что auxiliary-block исполняется первым. При `alpha=pi/2` он даёт `Z_t tensor I_aux` на секторе двух единичных controls, затем `J_t Z_t=X_t`. При другом control-pattern оба блока identity. Auxiliary может быть неизвестным или entangled: сравнение имеет вид `CCX tensor I_aux` на всём входном пространстве, а фактическая residual correlation не объявляется сброшенной. Для ошибок unitary blocks достаточно

```
||CCX_hat−CCX tensor I_aux|| <= e_4+e_8 <= 3 e_4,
e_j=||G^(j k)−R(target_j)||.
```

Второе неравенство следует из `||U²−V²||<=2||U−V||`; A14 непосредственно суммирует сертифицированные отдельные `e_4,e_8`. Independent sparse interpreter проверил все `1 536` колонок для реально развёрнутых native words при `k=1,2`; максимальная float-разница `<7.8e−16`. Отдельный A14 replay проверил те же малые слова **точно** в исходном алгебраическом поле и `96` применений их literal raw inverse. Полная 4 111-битная степень в этих тестах не исполнялась.

Важное уточнение inverse. `X_hat=R Z` и `H_hat=R Z` являются отражениями, но `CCX_hat` в общем случае — нет. Это верно и для фактического положительного `k`, а не только hostile `k=1`: на секторе controls `11` оператор коммутирует с `J_aux`; на двух eigen-секторах `J_aux=±i` его determinant равен `exp(±2i alpha)`. Равенство `CCX_hat²=I` потребовало бы `exp(4i alpha)=1`, то есть `(sqrt(p)+i p)^(16k)=1`, что запрещает уже owned irrational-angle theorem. [check_boolean_math.py](check_boolean_math.py) также содержит ограниченную независимую алгебраическую проверку этого известного факта через сопряжение `sqrt(p)->i/sqrt(p)`; это не новая теорема исследовательской линии. Приближённый CCX нельзя повторять вместо его true adjoint.

## 2. Независимый сертификат заданного k

`NATIVE_BOOLEAN_ANGLE.json` из локального A14 задаёт положительный `k` длиной `4111` bits. Для окончательной оценки A14 не использует float или π в исполняемом слове: `G` фиксирован, target-матрицы `R(pi/4), R(pi/2), R(pi)` используются только в certificate сравнения.

[check_angle_independent.py](check_angle_independent.py) не вызывает owner `_rotation_intervals` и не ищет k. Он заново строит рациональные dyadic enclosures для `p=(sqrt(5)−1)/2` и `sqrt(p)` целочисленными корнями на масштабе `2^16640`, затем вычисляет `(sqrt(p)+i p)^(2k)` **слева направо** с outward rounding и без обрезания к единичному кругу; две независимые interval squarings дают `4k` и `8k`. Все шесть полученных интервалов пересекают опубликованные owner интервалы и самостоятельно доказывают

```
e_2 <= 2^-4096,     e_4 <= 2^-4096,
e_4 + e_8 <= 2^-4096.
```

`1/sqrt(2)` для H зажат соседними dyadic integer-root endpoints. Поскольку `||R(c,s)−R(c0,s0)|| <= |c−c0|+|s−s0|`, конечные целочисленные сравнения дают истинный full-column operator bound. Результат и hashes — [INDEPENDENT_ANGLE_CHECK.json](INDEPENDENT_ANGLE_CHECK.json). Изолированный replay дополнительно вызвал owner `certify` с уже данным k и побайтно подтвердил весь исходный certificate; поиск candidate не проверялся и не требуется для soundness предъявленного k.

## 3. Реальные forward и literal raw inverse

A14 строит новый график для отрицательной степени:

```
G_q^-k = SWAP(q,port); SourceI²; G_port^k; SourceI²; SWAP(q,port).
```

Это **новый** forward word длиной `k+10` для `q!=port`, а не ретроактивная скидка на уже исполненный letterwise inverse и не перенос его marked/clock истории. Для обратного хода A14 обращает в обратном порядке каждый фактический primitive: CX сам себе inverse, SourceI заменяется тремя SourceI, а каждый отдельный G — owned 5/11-call inverse с реальными маршрутизациями. [check_lowering_independent.py](check_lowering_independent.py) заново построил обратные DAG деревья из forward leaves и пересчитал их exact inventories без раскрытия 4 111-битных repeats:

| Macro | Forward calls | Literal raw inverse calls |
|---|---:|---:|
| H | `2k+8` | `22k+12` |
| X | `4k+8` | `44k+12` |
| CCX | `12k+92` | `96k+140` |

Для CCX forward точный inventory `12k G + 68 CX + 24 SourceI`. Reverse A14 является настоящим adjoint **реализованного** forward word, а не повторным приблизительным CCX и не другим, заново оптимизированным negative-power графиком. Каждый физический вызов в обе стороны и каждый промежуточный mark/clock подлежат оплате.

## 4. Пять схем A13 и error interface B29

Независимо сверены A13 hashes, exact logical counts, wire maps и формулы substituted forward/reverse inventories для трёх decoder и обеих cap7 first-success схем. На уровне шаблонов каждый `SourceI` использует один заявленный port и два Spin wires, каждый ordinary control не является target ни G, ни CX, а protected oldRIGHT не адресуется. В сочетании с B28, где все `52 444 771` логических decoder gates были просмотрены на read-only inputs, это подтверждает stated typewise wiring claim при действительной аллокации указанных раздельных `port/Spin/aux/oldRIGHT` ролей. Port и Spin возвращаются точно на границе каждого macro; внутри него они могут меняться. Наличие этих границ не удостоверяет самостоятельно любую промежуточную original mark.

Для одного fixed logical circuit с `N_X,N_H,N_CCX` приблизительными replacements и exact CX все extended-column inputs, включая произвольный общий auxiliary, дают telescoping estimate

```
||U_native−U_logical tensor I_aux||
  <= (N_X+N_H+N_CCX) 2^-4096.
```

Случайная корреляция auxiliary, оставшаяся после одной approximate CCX, не сбрасывается: следующий all-column estimate применим к полученному joint state, и ошибки складываются. Отдельное изолированное воспроизведение дополнительного A14 checker проверило `350` actual macro bindings (первые части трёх decoders и оба полных first-success streams), а не притворилось разворачиванием всех астрономических native calls.

Для семи известных A13 report частей (без остальных отсутствующих операторов) `N_X+N_CCX=92 263 351 768<2^37`, поэтому их вклад `<2^-4059`. Он меньше требуемых в B29 условных per-gate примеров даже после conservative lift. Это не ограничивает **всю** `eta_A`: надо прибавить фактические H tests, source preparations, dynamic DAG/copy offsets, quantum payload routes, доступ порта, auxiliary/scratch births, отдельно требуемые prefix/readers и при наличии дополнительные forward/inverse occurrences. Target `alpha_h>=1/2`, Hessian `L`, нормы/Neumann correction маркированного decoder и физический `C` B30 не доказывает.

## 5. Воспроизведение и provenance

[ISOLATED_REPLAY.json](ISOLATED_REPLAY.json) документирует rootlike копию A13/A14 вместе с owning `native_execution.py` и `native_phase.py`: заданный k в owner interval cert, `check_native_boolean.py` и `lower_native_selectors.py`; три reconstructed outputs побайтно идентичны исходным. [ISOLATED_LOWERING_REPLAY.json](ISOLATED_LOWERING_REPLAY.json) отдельно фиксирует позднее дополнительное `check_native_lowering.py` и его output. Ни один direct файл не изменён.

Из open-checkout:

```
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round30/check_angle_independent.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round30/check_boolean_math.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round30/check_lowering_independent.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round30/replay_a14_isolated.py
python3 -B -W error 02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round30/replay_native_lowering.py
```

Hash inputs и outputs собраны в [RECEIPT.json](RECEIPT.json). Повтор не публикует работу и не доказывает закрытие исходной GR-задачи.
