# Полная ограниченная сверка Book02 §02.3b и его 30 C0-кандидатов

## Вердикт и рамки

Сверен полный исправленный текст §02.3b и все 30 source-keyed records с их
Lean-объявлениями, доказательствами и ранее сохранёнными точечными обзорами.
В данных математических определениях и условных теоремах ошибки в кванторах
не обнаружено. Рекомендую **условно принять этот конкретный разбор как полный
для исправленного раздела** после уточнения описания record 22 и явной записи
ниже о зависимости моста представленного состояния. Это рекомендация
независимой технической сверки, не решение CONTROL об acceptance, не утверждение
о глобальном C0-деноминаторе и не приёмка физической реализации.

Независимость ограничена: исполнитель участвовал в некоторых ранее записанных
точечных Book02-обзорах. Текущий проход заново проверил полный source, все
30 имён и proofs; он не является независимой проверкой авторства этих прежних
обзоров. Описанные ниже полнота и exclusions — содержательное суждение, а не
следствие проверки байтов или количества кандидатов. Существующие принятые
conditional assembly applications не заменяют отдельного решения по C0.

## Точные входы и воспроизводимость

- Исторический Book02 commit `a4d0d3919e9c2b8e9f27aeaacaafd6dcf06e6c38`,
  blob `00d7c597abb99856719b274bb86b115b17af139f`, весь файл SHA-256
  `58b6e32e99876a9077f6c55c68424819a952c471da381514e066afa65c2c7eef`;
  §02.3b `[12086,15801)`, SHA-256
  `612be4ee853d2f03469e3877a41cb16490a0cb6e5328fead13b2dbcb5346c7c8`.
- Проверенный live #402 head `a358e91e764655b16082bf7e6161a79df96a24a6`,
  active Book02 blob `77d67c6fc1c14a08e2a3475843be745c27e57637`, весь файл
  SHA-256 `152d1abf1bf01d75b9e783f3952e988f1e6595053644c2df03c18541a3729f2c`;
  тот же раздел `[12086,15810)`, SHA-256
  `beb708ff66633cd5a184268fa17febfc683a400b37c5b27ce7f9212a46bbae91`.
- Путь источника в обоих снимках:
  `01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md`.
  Первичный candidate block расположен в
  `02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md`, blob
  `72d24dd36c887cd00383e5f16cc17298581a8bd0`; JSON-блок без завершающей LF
  SHA-256 `206943122c0f0c1f4db2749b31c1f1e79ba250b506f54b3bc7945319af8991a0`.
- `03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean` blob
  `a882f38aa1caf4d619c6e1f84c73ebe97e4b127a`, SHA-256
  `c164818dc50de94afad690946d4c209309350340b5cb1586ddc9f91f74bcb203`;
  `FutureExecution.lean` blob `065a8f631e65bda8b9bc85a6ff6217de31bdd1f4`,
  `VerificationCore.lean` blob `01b02ebbe81a62464e81d5c397c101fd60fff4f9`.
  `TheoryTransfer` в имеющейся изолированной рабочей копии имеет тот же blob.
- `verify_bytes.py`, запущенный в корне настоящего Git repository, проверяет
  исходные blobs, оба SHA, ровно одну замену во всём файле, hashes разделов и
  candidate block, все границы и полный byte complement. Это read-only
  object check, не semantic proof и не аутентификация недоверенных metadata.
- `d0-book02-full-check.lean` и его log: `#check` и `#print axioms` для всех
  30 объявлений и доп. моста; `lake env lean` завершился 0 в уже существующем
  cache. Это не cold build и не проверка точности всех сохранённых type_sha256.
  Axiom footprint содержится в полном log; не сильнее `propext`,
  `Classical.choice`, `Quot.sound`. Пустое доказательство, описанное ниже,
  отдельно проверено `d0-book02-represented-emptyword.lean`, exit 0.

## Исправленная версия и полный учёт байтов

В offset `14887` историческая формулировка о необходимости coverage
(56 байтов) заменена формулировкой о достаточности (65 байтов); точные байты
обеих версий зафиксированы в `verify_bytes.py`. Других изменений во всём файле
нет. Непересекающая исходную фразу historical граница до offset 14887 остаётся
неизменной; граница от 14943 включительно сдвигается на +9. Границы внутри
изменяемой фразы не переводятся этим правилом. Так, `[14760,15284)` становится
`[14760,15293)`, а раздел заканчивается на 15810. Исторические range IDs и
результаты не являются активными bytes без указанного переноса.

Union переведённых диапазонов 30 records оставляет следующий **точный active
complement**, а не просто незамеченные пробелы:

| Active bytes | Диспозиция |
| --- | --- |
| `[12086,12729)` | Заголовок, навигация, заявленная связь с Book01 §01.1.8, ссылка на owner и accepted conditional application. Это provenance и вход уже представленного `TheoryVerification E`, а не безусловное доказательство E. Строгая сверка самой Book01 остаётся отдельной; данный фрагмент не добавляет ещё одну независимую теорему. |
| `[13109,13110)`, `[13646,13647)`, `[14273,14274)`, `[14759,14760)` | По одной LF; структурные разделители, не математические атомы. |
| `[15293,15810)` | Финальный separator и физический application boundary: actual admitted operations, полное действие/источник, часы, refinement, книги 03/07. Это реальные незакрытые требования к применению; их нельзя исключать из глобального физического обязательства и нельзя засчитывать как доказанные этой Lean-теоремой. Как source scope в этой section не являются новой доказанной Lean теоремой. |

Семантика диапазонов records пересекается намеренно: несколько утверждений
подтверждаются одним абзацем; число 30 не является числом дизъюнктных текстов
и не является общим знаменателем всех книг/реестра/негативных результатов.

## Поэлементная сверка 30 records

Номера — порядок pinned JSON. Везде `F,G` — заданные полные абстрактные
`FutureExecution`, `I` — **заданный** `Interpretation F G`; физическая
полнота его действий/тестов из этого не следует.

1. `Interpretation`: определение задаёт state/actionWord/test/outcome maps,
   injective outcomeMap и все pointwise primitive step/observe equations.
   Это предпосылки интерфейса; stateMap не обязана быть инъективной.
2. `compile`: рекурсивная конкатенация слов для каждого source action,
   включая пустое слово; соответствует source finite-word construction.
3. `run_commutes`: ∀ finite w и source s; доказывается индукцией из primitive
   step, не является дополнительным полем структуры.
4. `profile_commutes`: ∀ s,w,t на mapped test; справа outcomeMap исходного
   результата. Это не все дополнительные тесты G.
5. `compile_append`: ∀ source words u,v сохраняется конкатенация.
6. `comp`: для двух заданных интерпретаций строит композицию всех карт и
   доказывает её primitive fields; intermediate action компилируется в слово.
7. `comp_compile`: ∀ w последовательное и составное кодирование совпадают;
   не утверждает равенство физических длин, длительностей или цен.
8. `commonExecution`: State = G.State, Action/Test = F.Action/F.Test,
   outcome = G.Outcome; step/read задаются только картами I.
9. `common_profile_eq_iff`: ∀ исходные s,t; обе стороны о полных конечных
   профилях **common** контекстов. Reflection использует outcome_injective.
10. `EmpiricalImage`: подтип образа futureMap, а не все native states/classes.
11. `imageEquiv`: биекция F.FutureClass с этим образом; `Equiv.ofBijective`
    использует доказанную injectivity, а не raw-state injectivity/полноту G.
12. `imageStep`: для каждого a и q:image даёт опять image, используя
    futureMap_step; это закрытость, не отдельная предпосылка.
13. `imageEquiv_step`: ∀ a,q действует указанная интертвинерная диаграмма.
14. `verifiedStateImageEquiv`: дополнительно требует конкретный
    `E : TheoryVerification F.futureEmpiricalTheory`; через `E.represents`
    даёт эквивалентность E.protocol.State и image. Ни E, ни I не построены
    для произвольного физического процесса.
15. `verifiedRun_image`: ∀ w,s при тех же I,E отображает уже представленное
    выполнение в quotient class фактического G.run(compiled w, stateMap s).
    Это равенство классов, не сырых состояний или отдельных промежуточных ходов.
16. `translate`: source FutureClass-предикат переводится обратным imageEquiv.
17. `transfer_theorem`: source proof ∀q, H q→P q требуется как вход;
    на каждом q:image перевод H остаётся гипотезой, а не исчезает.
18. `transfer_from_premises`: произвольный index type; требуются source proof
    и каждый translated A i q. Пустое семейство допустимо; proof не создаётся.
19. `translate_conjunction`: точное ↔ при любых P,Q и q:image.
20. `translate_negation`: точное ↔ при любых P и q:image.
21. `translate_forall`: точное ↔ для произвольного индексного типа и q:image;
    этой теоремой не строится внешняя синтаксическая proof system.
22. `translate_future_observation`: утверждение точнее сформулировать так:
    `translate (fun p => F.quotientProfile p w t = o) q ↔
    I.commonExecution.quotientProfile q.val w t = I.outcomeMap o`.
    Сейчас слово `equals` в поле statement JSON неоднозначно: это ↔ двух
    **предложений**, а не равенство translated predicate и outcome. Обратное
    направление использует injective outcomeMap. Исправить prose без изменения
    Lean statement/hypotheses; не заменять common test на произвольный G test.
23. `NativeContextCoverage`: ∀ native word/test выбирает ЕДИНЫЙ source
    context и readout, корректные для ∀ represented s. Readout не зависит
    от s. Witness задан, не выведен из primitive commutation.
24. `native_profile_eq_iff`: при C и ∀ source s,t, эквивалентность полного
    G-профиля их образов и F-профиля. C достаточно; его конкретная форма
    не является необходимой для истинности equivalence.
25. `visibleBitSystem`: Bool×Bool, Unit action/test, identity action, чтение
    только первой координаты; конечный абстрактный source.
26. `extraBitTestSystem`: тот же state/action, Bool test выбирает первую или
    вторую координату; добавочный test — абстрактный, не физический факт.
27. `visibleBitInterpretation`: id state/outcome, одношаговое слово `[()]`,
    test false; все primitive equations действительно выполняются.
28. `visibleBit_same_all_source_futures`: (false,false)/(false,true)
    имеют равные F.profile для всех source words и test.
29. `extraBit_different_native_futures`: native test true после пустого
    слова различает те же состояния, следовательно G.profile различны.
30. `extra_native_test_prevents_coverage`: для этой конкретной I нет даже
    `Nonempty (NativeContextCoverage I)`. Не доказывает, что никакой другой
    witness/физическая система не может иметь coverage.

## Диспозиция represented-state моста

`Interpretation.verifiedStateImageEquiv_representedState` отсутствует среди
30 records, хотя используется доказательством `verifiedRun_image` и объясняет
фразу о том же представленном состоянии. Он должен быть явно назван
обязательной source-to-Lean связью, а не оставлен подразумеваемым. Тем не менее
он **не нуждается во втором счёте математической единицы**: следствие record 15
при `w=[]` восстанавливает это равенство после `Subtype.ext`. Это проверено
Lean-файлом `d0-book02-represented-emptyword.lean`; в нём не используется сам
мост как гипотеза, используется опубликованная теорема `verifiedRun_image`.
Решение о политике атомизации остаётся за владельцем C0.

Направление proof dependency важно: существующее доказательство универсальной
record 15 фактически использует named bridge; независимое обратное выведение
лишь показывает логическое покрытие конечного частного случая, а не делает
этот bridge лишним в compiled proof. Равным образом пустые compilation lemmas,
`futureMap`, `futureMap_injective`, `native_profile_reflects`, assertionFaithful
и отдельный XOR-control следует сохранять как proof inputs/controls со своими
условиями, без автоматического прибавления отдельных source assertions.
XOR-control доказывает только ненужность данного single-context witness для
равенства полных профилей; extra-bit доказывает лишь неприменимость witness
в другом конкретном примере.

## Открытые границы

Actual representation F,G,I,E, набор тестов и покрытие ещё требуют своего
физического построения. Прикладной consumer
`lean-operational-transfer-to-theory-transfer` сохраняет свои входы; это не
принятие C0-classification. Далее `gr_operational_realization` требует actual
preparation, full Cost−Info/source, clock/work и refinement. Никакая из этих
проверок не закрывает физическую GR или `GR_closed`. Кроме того, исторические
Book01 §01.1.6 и §01.1.8, другие разделы десяти книг и вне-книжные research,
registry, certificates и negative controls не могут быть исключены из общего
обязательства только потому, что этот один раздел полностью рассмотрен.

## Machine-readable proposed corrections

The historical candidate block remains authoritative for its own snapshot;
this explicitly versioned review supplements it without accepting C0.

```json
{
  "schema": "book02-023b-reviewed-corrections/1",
  "corrections": {
    "Interpretation.translate_future_observation": {
      "historical_statement": "Translation of a source quotient observation equals the actual common quotient readout with I.outcomeMap o.",
      "statement": "Translation of the proposition F.quotientProfile p w t = o at q is logically equivalent to I.commonExecution.quotientProfile q.val w t = I.outcomeMap o."
    },
    "Interpretation.verifiedRun_image": {
      "proof_dependency": "D0.Foundation.TheoryTransfer.Interpretation.verifiedStateImageEquiv_representedState",
      "role": "Existing proof dependency and the empty-word consequence of this candidate; not an independently counted source assertion.",
      "control": "d0-book02-represented-emptyword.lean"
    }
  }
}
```
