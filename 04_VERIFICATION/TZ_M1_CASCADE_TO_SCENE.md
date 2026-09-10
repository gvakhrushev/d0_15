# ТЗ: структурное замыкание M1-каскада до переменной сцены

## 1. Миссия

Выполнить самый ценный оставшийся фундаментальный фронт D0:
дать **непереборное**, структурное доказательство либо точный отрицательный
результат для перехода

```text
M1 / независимое повторное детектирование
  -> carried cascade of insufficiency repairs
  -> число зон переменной сцены
  -> K(9,11,13) as the selected quotient scene.
```

Рабочий umbrella-owner: `D0-CASCADE-INSUFFICIENCY-CHAIN-001`.
Точный нынешний typed seam: `D0-SCENE-COUNT-REDUCTION-001`.

Это не задача «найти ещё один аргумент, почему 3 выглядит хорошо». Цель —
либо построить отсутствующий универсальный semantic morphism, либо доказать,
что он **не следует** из нынешней M1-грамматики, и сузить фронт до одного
нового принципа/контракта. Оба исхода считаются успехом.

## 2. Зафиксированное исходное состояние

Перед работой обязательно прочитать и сохранить в отчёте точные границы:

- `D0.Foundation.SceneCountReduction` уже доказывает
  `zoneCount = 3`, **если** построены два embedding-а:
  `Fin 3 ↪ Fin zoneCount` и `Fin zoneCount ↪ Fin 3`.
- Оба текущих antecedent-а там уже являются теоремами. Поэтому функция вида
  `fun _ => ...` не «потребляет» cascade/no-extension факт и является
  vacuous route. Этот маршрут уже разоблачён
  `D0.Foundation.SceneCountRouteNoGo`.
- `D0.Foundation.CascadeCarriedAssembly` уже содержит шесть genuine floors,
  четыре interlock-а, terminal count-leg и отдельный orientation-parity floor.
  Запрещено представлять каскад как пустую prose-цепочку или повторно
  доказывать уже имеющиеся этажи.
- `D0.Foundation.ZoneCountFromRank` даёт честный верхний bound
  `rank ≤ 3 -> zoneCount ≤ 3` для complete-multipartite scene. Но rank=3
  замороженной `K(9,11,13)` нельзя переносить на переменную сцену: это круг.
- `D0.Foundation.LadderRunLength` документирует ложную закрывающую стратегию:
  остановка на 15 может быть вызвана произвольными условиями. Ни
  `InSuLattice`, ни coprimality, ни другой фильтр, специально впервые
  срабатывающий на 15, не может стать источником selection theorem без
  отдельного M1-reductio, выводящего именно этот фильтр.
- Concrete two-sided class-M1 detector seam уже закрыт:
  `D0-CONCRETE-PHYSICAL-DETECTOR-REPRESENTATION-001`. Не открывать заново
  ложную проблему singleton/class; использовать `M1ClassAdmissible` и
  concrete `Observation` как существующий исходный слой.

## 3. Непереговорные правила доказательства

### 3.1. Единственная допустимая форма selection proof

Для каждого нового forcing-шага требуется универсальная схема

```text
assume ¬X
-> derive a mandatory theta not derivable from prior D0 objects
-> prove theta affects a distinguishable outcome or law formulation
-> prove theta is not unavoidable protocol data
-> theta is an M1-forbidden external catalogue
-> contradiction.
```

Нельзя заменять этот аргумент конечным или бесконечным списком кандидатов.
Фраза «все проверенные варианты не подходят» не является доказательством.

### 3.2. Роль перебора

Допускаются только как отрицательные контроли:

- mutation/can-fail проверка сертификата;
- явный контрпример ослабленной лемме;
- вычисление уже найденного конечного инварианта;
- scout, который убивает предложенный маршрут.

Перебор не может быть ни selector-owner, ни доказательством исчерпания,
ни основанием для `CORE-FORMALIZED`.

### 3.3. Запрет зашивания результата

Новый положительный результат немедленно недействителен, если хотя бы один
из следующих объектов до доказательства содержит целевое `3`, `Fin 3`,
`9`, `11`, `13` или эквивалентное готовое разбиение как входной параметр:

- определение admissible scene/zone;
- selector score;
- semantic interpretation;
- hypothesis, уже эквивалентная `zoneCount = 3`;
- mapping из cascade floors в zones.

Исключение: эти значения допустимы только в **контролях**, конечном
следствии доказанной общей теоремы или уже существующих frozen-scene
теоремах, которые не используются для выбора переменной сцены.

### 3.4. Никакой ложной полноты

Не разрешается:

- `sorry`, `admit`, новый `axiom`, `True`-shell, содержательный `rfl`-shell;
- новый невыведенный «semantic bridge» без отдельного статуса/контракта;
- подмена переменной сцены замороженной `K(9,11,13)`;
- использование `CascadeCountInterpretation` или
  `NoExtensionCountInterpretation` с игнорируемым доказательством owner fact;
- повышение umbrella-статуса из-за одной лишь сборки Lean-модулей.

Если новый внешний принцип действительно необходим, он оформляется как
минимальный typed contract, с non-vacuous model и axiom-deletion control;
следствия получают статус `D0-X5`/`BRIDGE-ASSUMPTIONS-EXPLICIT`, а не
present-core closure.

## 4. Обязательный исследовательский маршрут

### Фаза A — adversarial scout (до нового Lean-кода)

1. Прочитать `SceneCountReduction`, `SceneCountRouteNoGo`,
   `DiscriminationRetyping`, `DiscriminationKinds`, `ZoneCountFromRank`,
   `LadderRunLength`, `CascadeCarriedAssembly`, соответствующие строки
   `CLAIM_TO_LEAN_MAP.csv`.
2. Для каждого предложенного semantic bridge построить малый контрмодельный
   тест: сохраняет ли он исходные M1/cascade premises при `zoneCount=2` или
   `zoneCount=4`? Если да, route не закрывает count.
3. Проверить, не является ли предлагаемая гипотеза логически эквивалентной
   нижнему/верхнему bound. Нужна независимая вычислимая структура, а не
   переименованное неравенство.
4. Сдать короткий verdict ровно одного типа:
   `CERT-CLOSABLE`, `NO-GO-CLOSABLE`, `PARTIAL-CLOSABLE`,
   `NOT-CLOSABLE`, `DUPLICATE-ALREADY-OWNED`.

Нельзя писать основной Lean-модуль до этого verdict.

### Фаза B — содержательное ядро

Исследовать две стороны одновременно, но не смешивать их.

#### B1. Нижняя граница: cascade semantics

Нужно получить **из данных carried cascade**, а не из уже готового count,
три попарно различимых semantic obligations/record classes и доказать, что
они не могут быть представлены одной zone без нового outcome-affecting
catalogue. Требуется:

- явный тип структурных носителей (не `Fin 3`);
- map от этого типа к зонам переменной сцены;
- доказательство injectivity через M1-reductio или invariant separation;
- контроль, где удаление ровно одной load-bearing obligation допускает
  склейку двух носителей.

Допустимый результат — доказать no-go: из текущих floors нельзя построить
такой map без нового semantic datum. В таком случае назвать минимальный
datum и доказать точный countermodel нынешней грамматики.

#### B2. Верхняя граница: no-extension semantics

Нужно вывести, что всякая admissible zone имеет один из выводимых
квадратичных/детекционных slots, без готового target cardinality. Возможные
полезные промежуточные объекты:

- variable complete-multipartite scene с собственным transport operator;
- rank/invariant, вычисляемый из variable scene независимо от количества зон;
- representation theorem от concrete class-M1 detector data к zone signature;
- universal no-extension theorem, запрещающий четвёртый primitive slot через
  `¬X -> theta -> ⊥M1`.

Если upper route использует rank, он обязан **вывести rank ≤ 3 для variable
scene**, не цитировать rank замороженной `K(9,11,13)`.

### Фаза C — интеграция обеих сторон

Положительное закрытие допустимо только при наличии обоих независимых
результатов:

```text
non-circular cascade semantics  -> zoneCount >= 3
non-circular no-extension/rank semantics -> zoneCount <= 3
therefore zoneCount = 3.
```

После этого отдельно требуется построить map от трёх зон к конкретным
размерам. Нельзя объявлять, что `zoneCount=3` само по себе выводит
`(9,11,13)`: для размеров должен быть назван отдельный уже существующий или
новый owner (например, capacity/orientation/homology route) и проверена его
независимость от count route.

## 5. Ожидаемые артефакты

Имена можно скорректировать только при отсутствии коллизии, но разделение
обязанностей сохранить.

1. Scout memo в `04_VERIFICATION/` с verdict и перечислением убитых маршрутов.
2. Один или несколько Lean-модулей в `09_LEAN_FORMALIZATION/D0/Foundation/`,
   например:
   - `M1CascadeSceneSemantics.lean` — только если B1 имеет честный owner;
   - `M1NoExtensionSceneSemantics.lean` — только если B2 имеет честный owner;
   - `M1CascadeSceneNoGo.lean` — предпочтителен, если scout находит
     countermodel вместо закрытия.
3. Детерминированный certificate `05_CERTS/vp_m1_cascade_scene_*.py`.
   Первая строка: `STRUCTURE_FIXED_BEFORE_NUMBER:`.
4. Минимальный source-patch соответствующей секции Book 01; не редактировать
   собранный `BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md` напрямую.
5. Одна обновлённая строка существующего claim ID либо новый ID, только если
   Phase A доказала, что это не duplicate.
6. Отчёт по шаблону `VERIFIED_CLOSURE_PROTOCOL.md`, включая remaining exact
   blocker даже при положительном частичном результате.

## 6. Acceptance criteria

### Положительный исход

Можно менять статус `D0-SCENE-COUNT-REDUCTION-001` или umbrella только если:

- новая теорема не принимает `zoneCount=3`, `Fin 3` или эквивалентный bound
  как semantic premise;
- оба bounds имеют независимые, наблюдаемо-нагруженные источники;
- mutation controls ломают каждый bound по отдельности;
- `D0.All` строится без `sorry`/новых аксиом;
- registry, cert, source-book и все gates зелёные.

### Отрицательный исход

Сильный и желательный результат, если доказано одно из следующего:

- текущий M1/cascade язык допускает модель с 2 или 4 зонами;
- любой candidate morphism факторизуется через уже имеющийся count bound;
- proposed structural invariant не различает четвёртый slot;
- для перехода требуется точно названный новый outcome-affecting primitive.

Тогда закрыть **маршрут** как `NO-GO`, не umbrella, и оставить один
конструктивный следующий owner.

## 7. Обязательная проверка перед сдачей

Выполнить как минимум:

```bash
python tools/validate_csv.py
python tools/d0_logic_chain.py
python tools/d0_value_model.py
python tools/d0_score.py --strict
python tools/check_cert_can_fail.py
python 05_CERTS/run_all_v15_closure_certs.py
cd 09_LEAN_FORMALIZATION && lake build D0.All
python 09_LEAN_FORMALIZATION/tools/check_no_sorry_in_core.py
```

Финальный ответ исполнителя должен быть кратким и содержать только:
commit, модули, cert, статус claims, результат scout, список реально
замкнутых/убитых маршрутов, green-gate и один точный remaining blocker.
