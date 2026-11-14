# B37. Конечный native `U_star` для фиксированного CAR half-vector

## Результат

Построен конечный, адресованный `G/CX/SourceI` DAG [CAR_USTAR_NATIVE.json](CAR_USTAR_NATIVE.json) и его буквальный оплаченный raw inverse. Он приближает конкретный `SO(16)` target на **всех** grade, port и Spin columns с операторной ошибкой `≤2^-4096`; независимая целочисленная оценка даёт даже `<2^-4142`. На входном grade `|1>` он готовит

```
u_star = (|1> + sqrt(p)|1> + p|14>)/sqrt(2(1+sqrt(p))).
```

Нет private clean wires, произвольного rotation oracle, измерения или postselection. Доступный отдельный native port и два Spin wires могут содержать произвольное состояние; после complete macro они восстанавливаются, включая произвольную запутанность. SAM, SITE, CAR RIGHT, unknown oldRIGHT и прочие spectators не входят в этот word. Это закрывает **фиксированный `U_star` parent B35**, но не готовит весь CAR/source bank, не выдаёт births/marks/clock или физический `C`; `GR_closed=false`.

## 1. Целевой угол и настоящий word

Пусть `p²+p=1`, `cos(theta)=sqrt(p)`, `sin(theta)=p`. Тогда

```
u_star = cos(theta/2)|1> + sin(theta/2)|14>.
```

Grade wires нумеруются **младший бит первым**. Перестановка `C` — три физических CX:

```
CX(grade0,grade1); CX(grade0,grade2); CX(grade0,grade3).
C|1>=|15>,  C|14>=|14>.
```

Пусть `P_111` контролирует `grade1,grade2,grade3=111`. Выбран положительный целый `k`, точная длина которого 4 142 bits. В хронологическом порядке исполняются `C`, owned Walsh/parity word

```
R = exp[ J_(grade0) · 8k theta · P_111 ],
```

и `C†` (эти три CX в обратном порядке). Он совпадает с identity вне grades `1,14`; в активной паре реализует `R(8k theta)` в порядке трансформированных `|14>,|15>`. Поскольку `8k theta` сертифицированно близок к `−theta/2` modulo `2π`, образ `|1>` близок к `u_star` с тем же all-column bound. `C† R C` — настоящий конечный native target word, а не обозначение внешней матрицы.

[build_car_ustar.py](build_car_ustar.py) использует численный continued-fraction поиск **только как proposal**. Сертификат в JSON вычисляет целочисленные outward интервалы для точных `cos(8k theta), sin(8k theta)` и target half-angle roots на 16 640 binary digits. Фактические (G^n) задаются точным `p`, а вычисление сертификата не пользуется float/π. Отдельный [verify_car_ustar_interval.py](verify_car_ustar_interval.py) заново выполняет независимую outward арифметику с другой точностью 12 800 bits и без unit-clamping; он доказывает суммарную ошибку sin/cos `<2^-4142`. Норма разности двух real rotation blocks не больше этой суммы; потому bound распространяется на все grade/port/Spin columns и любую внешнюю запутанность.

## 2. Конкретный schedule и его платный обратный проход

Для каждого отрицательного Walsh power используется принадлежащая A14 оптимизированная реализация `G_target^-k` через один общий маршрут `SWAP; Z_port G_port^k Z_port; SWAP`. Это точный блок на всех columns, но его промежуточные marks и цена относятся **этому новому порядку**. Никакие ранее зарегистрированные этапы не отождествляются. Для выбранного DAG:

| Операция | `G_port` | `G_other` | CX | SourceI |
|---|---:|---:|---:|---:|
| Forward | `4k` | `4k` | `54` | `16` |
| Literal raw inverse | `8k` | `0` | `24k+54` | `32k+48` |

Forward содержит `8k+70` реальных primitive calls, обратный word — `64k+102`; числа `k` сохранены **точно**, не через float. В inverse каждый actual G/SourceI/CX обращается по правилам владельца в буквальном обратном порядке; никаких бесплатных сокращений внутри отмеченной истории не заявлено. Старое побуквенное построение каждого из `4k` отрицательных G имело бы другие forward counts (`24k+30` CX и `16k` SourceI) и не является данным schedule.

[CAR_USTAR_EXACT_CHECK.json](CAR_USTAR_EXACT_CHECK.json) на точной арифметике `Z[a]`, `a=sqrt(p)`, `a⁴+a²−1=0`, исполняет **все** 256 grade⊗port⊗Spin⊗oldRIGHT columns для `k=1` и `k=2`, затем каждый действительный literal inverse: всего 512+512 полных проверок, с настоящим `L_i=diag(J,−J)`. Для огромного сертифицированного k проверены сама DAG grammar, схема, exact адреса, oldRIGHT exclusion, counts и буквальная структура inverse; раскрывать и исполнять `~2^4145` native calls не заявляется. [CAR_USTAR_REPLAY.json](CAR_USTAR_REPLAY.json) повторяет построение в изоляции и получает byte-identical JSON.

## 3. Интерфейс для A18: произвольная пара и дополнительные controls

`build_car_ustar.pair_word(k, a_label, b_label, grade, port, spin, extra_controls, extra_pattern, protected)` выдаёт конечный native DAG и точную metadata для двух **разных** grades `a,b∈[0,15]`. Он строит обратимую CX-перестановку по `a XOR b`: младший отличающийся bit — pivot, остальные отличающиеся bits устраняются CX из pivot. После неё два grades отличаются одним pivot bit и задают одну общую маску остальных трёх bits. Дополнительные SAM/site controls присоединяются как read-only controls с указанным fixed pattern.

Для `L=len(extra_controls)` число controls `K=3+L`, а фактический угол равен **`2^K k theta`**, а не всегда `8k theta`. Если `t` — pivot bit преобразованного `a`, то

```
U|a> = cos(phi)|a> + (-1)^t sin(phi)|b>,  phi=2^K k theta.
```

Все другие grade/extra-control patterns являются identity на полных columns. В `protected` вызывающий код обязан передать RIGHT/oldRIGHT и иные факторы, которые нельзя даже использовать как control; функция запрещает их пересечение с grade/controls/port/Spin. Само read-only SAM/site control не доказывает допустимость конкретного marked graph. `pair_word(…,1,14)` без дополнительных controls точно воспроизводит B37 DAG.

Для выбора другого угла `propose_target(bits,K,target_turn_fn)` выполняет **недоверенный численный proposal**. Затем `certify_target(k,K,cos_interval,sin_interval,bits,precision)` целочисленно проверяет его against actual native power. Переданные интервалы заданы целыми endpoints с общим знаменателем `2^precision`; **их принадлежность действительному target должен отдельно доказать вызывающий код**. Успех generic emitter на произвольном будущём target не заявляется без этой проверки.

Для планирования, если `n=2^K`, `h=popcount(a XOR b)−1`, а `v=n/2` при ненулевом полном predicate pattern и `v=0` при нулевом, данный optimized forward имеет

```
G_port=v k,  G_other=(n−v)k,
CX=K n+6v+2h,  SourceI=4v.
```

Literal raw reverse нужно считать из **реально выпущенного** word; для этих агрегатов `G_port'=G_port+G_other`, `CX'=CX+6 G_other`, `SourceI'=3 SourceI+4(G_port+G_other)`. Это число вызовов, не их допуск или физическая цена.

[PAIR_INTERFACE_CHECK.json](PAIR_INTERFACE_CHECK.json) проверяет exact k=1 native semantics для всех 240 упорядоченных разных grade pairs, 3 840 grade columns, 2 048 дополнительных control/flag cases и ещё 2 048 cases с произвольными port/Spin/oldRIGHT. Проверено отсутствие targets на extra controls, exact identity вне predicate, отказ при protected-control alias и два малых generic angle certificate, включая target zero. Это проверка интерфейса, а не сертификат q/y± targets A18.

## 4. Применение и оставшиеся обязательства

В B35 `U_star` требовался для отражения `R_(u_star)` материального map. На заявленном входном подпространстве его uniform error теперь не больше `2^-4096`, без private-clean U workspace; принадлежащий B35 anchor-reflection compiler и отдельная подготовка соответствующих дополнительных predicate zeros всё равно оплачиваются. Для 112 возможных CAR copies даже консервативный вклад `4·112·2^-4096 <2^-4087` относится только к этому fixed U и не включает остальные стадии.

SAM/site-controlled `U_m` для q и y±, Choi U, исходный vacuum/Fourier и SITE, реальные source copies, весь H.1 comparator/READY, birth admission и marks/clock остаются отдельными задачами. Никакие величины Info, полная alpha или GR этой локальной конструкцией не определены.
