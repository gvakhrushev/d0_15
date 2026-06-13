# D0 v14 — Архитектурный план интеграции и замыкания
**Роль: архитектор/планировщик. Исполнитель: Claude Code. Источник истины: `03_THEORY_MAP/theory_status_map.csv`.**

Версия плана: 1.0 · составлен на основе распакованного `D0_v14.zip` (реальная структура, не по памяти).

---

## 0. ГЛАВНЫЙ ПРИНЦИП ПЛАНА

Это **проект интеграции и замыкания**, НЕ строительство с нуля. v14 уже содержит:
- 173 claim-строки в управляющем CSV (`theory_status_map.csv`)
- граф зависимостей 316 узлов / 353 ребра (`theory_graph.{json,dot,html}`), регенерируемый из CSV
- 288 `.lean` файлов, 206 `vp_*.py` сертификатов
- бэклог Lean-перевода (`D0_LEAN_FULL_TRANSLATION_TZ_20260528/01_BACKLOG/LEAN_TRANSLATION_BACKLOG.csv`)
- уже влитый слой v15 (toral automorphism, Galois balance, quasicrystal, CKM phason)

**Работа = (A) влить недостающее из GOLDEN/v15-17 и из нашего чата → CSV-строки + Lean + cert;
(B) поднять открытые звенья по цепочке HYP→THE; (C) держать CSV как живой роудмап/статус.**

CSV — это контрольная плоскость. Каждое изменение теории = изменение строки CSV + соответствующий
артефакт (Lean-модуль и/или Python-cert), затем регенерация графа. Никаких «теоретических»
изменений без отражения в CSV. Это закон проекта.

---

## 1. КАРТА РЕПОЗИТОРИЯ (что где лежит)

```
D0_v14/
├── 00_LANGUAGE_NORMALIZATION/   # нормализация терминов (verbs/claim-levels)
├── 00_ROADMAP/                  # 3 audit-файла (Lean K-theory, operator-geometry deps, PDG integration)
├── 01_BOOKS/                    # книги (нарратив теории)
├── 03_THEORY_MAP/               # ★ КОНТРОЛЬНАЯ ПЛОСКОСТЬ
│   ├── theory_status_map.csv    # ★★★ единый источник истины, 173 строки
│   ├── theory_graph.{json,dot,html}  # генерируется из CSV
│   ├── theory_semantic_index.md
│   ├── BOOK_SECTION_MAP.md      # маппинг claim→книга→секция
│   └── D0_v15_*.md (≈45 файлов) # влитые синтез-документы v15
├── 05_CERTS/                    # 206 vp_*.py + schemas/ + outputs/ + DATA_RUNNERS/
│   ├── ported_legacy_primary/   # перенесённые сертификаты по доменам (D0-CKM-002, D0-GRAV-001…)
│   └── run_all_core_certs_results.json
├── 06_AUDIT/                    # аудиты
├── 08_PASSPORTS/                # ★ эмпирические паспорта (40+ поддиректорий)
│   ├── _MATRIX/ _RESULTS/ _DATA_MANIFESTS/ _FROZEN_*  # инфраструктура заморозки
│   ├── CKM/ DESI/ DESI_BAO/ GWOSC_LIGO/ SPARC/ PlanckCMB/ …
│   └── runners/
├── 09_LEAN_FORMALIZATION/       # ★ 288 .lean (D0.Combinatorics, D0.Dynamics, D0.Matter, D0.Topology…)
├── D0_LEAN_FULL_TRANSLATION_TZ_20260528/
│   ├── 00_TZ/ 01_BACKLOG/ 02_LEAN_ARCHITECTURE/ 03_CI/ 04_REVIEW_CHECKLISTS/
└── tools/graphify/              # CSV→граф пайплайн (graphifyy на PyPI)
```

### CSV-схема (16 колонок) — выучить наизусть, это контракт
`claim_id, book, section, type, domain, scope_guard, lean_module, lean_theorem,
lean_status, release_status, uses_bridge_assumptions, assumption_ids, python_cert,
module_exists, certs_exist, notes`

**type** ∈ {core(103), bridge(15), no-go(15), certificate(9), frontier(11), sector(4),
passport/passport_target/passport_layer(13), deprecated(2), audit(1)}

**lean_status** ∈ {LEAN_PROVED(108), LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS(8),
PYTHON_CERTIFIED(28), OPEN(14), CERT_SCAFFOLD(4), THEOREM_TARGET(2), DEPRECATED(2)}

**release_status** (главный «уровень зрелости»): CORE-FORMALIZED(89), CERT-CLOSED(9),
NO_GO_PROVED(8), BRIDGE-ASSUMPTIONS-EXPLICIT(6), CORE_BRIDGE_SPLIT(4), EMPIRICAL-PASSPORT,
PROOF-TARGET, THEOREM-TARGET-SHARPENED, …

---

## 2. ЛЕСТНИЦА ЗРЕЛОСТИ (как «поднимать по цепочке»)

Канонический жизненный цикл claim-а (это и есть «закрытие открытых задач»):

```
HYP (идея в чате/книге, нет строки CSV)
  → CSV-строка с lean_status=OPEN, release_status=PROOF-TARGET, python_cert=(scaffold)
    → PYTHON_CERTIFIED  (vp_*.py численно/символьно проверяет, cert PASS)
      → LEAN_PROVED       (Lean-модуль доказывает, 0 sorry, CI зелёный)
        → CORE-FORMALIZED (release-статус: звено несущее, в графе как core)

Параллельные терминальные статусы (не «ниже», а «вбок»):
  NO_GO_PROVED            — доказано, что нельзя (тоже ценность!)
  BRIDGE-ASSUMPTIONS-EXPLICIT — Lean с явными ASSUMP-* (мост, не чистое ядро)
  EMPIRICAL-PASSPORT      — паспорт с замороженным манифестом (внешний тест)
  DEPRECATED              — снято (с указанием причины)
```

**Критерий повышения (жёсткий, проверяемый Claude Code):**
- OPEN→PYTHON_CERTIFIED: существует `vp_*.py`, запуск возвращает PASS, статус-флаги в выводе.
- PYTHON_CERTIFIED→LEAN_PROVED: существует `.lean` модуль, `lake build` зелёный, `grep -c sorry`=0.
- →CORE-FORMALIZED: предыдущее + claim не использует `ASSUMP-*` (иначе максимум BRIDGE-ASSUMPTIONS-EXPLICIT).
- любое→DEPRECATED: только с записью причины в `notes` и ребром в графе на замену.

**Anti-promotion firewall (из Книги 00, обязателен):** запрещено повышать статус
риторикой. Эмпирический паспорт НИКОГДА не повышается до core-теоремы. Константа,
подогнанная в паспорте, не называется выведенной. Это проверяет CI-скрипт (см. §6).

---

## 3. GAP-АНАЛИЗ: что из чата/GOLDEN/v17 ЕЩЁ НЕ В CSV

Проверено grep-ом по CSV. **Уже влито** (есть строки): toral automorphism (D0-TORAL-*),
Galois balance, quasicrystal phase-unfolding (D0-QUASI*), CKM phason holonomy,
condensed φ-vacuum cut-project, vacuum cubic (частично).

**НЕ влито — это очередь интеграции (наши результаты чата + GOLDEN §52):**

| Новый claim_id (предлагаемый) | Содержание | Источник | Целевой статус |
|---|---|---|---|
| D0-ICOSIAN-E8-CARRIER-001 | Q₈⊂2T⊂2I, икозианное кольцо (норма a+b√5↦a+b) = E₈ (Морделл); 120 единиц на 2-й оболочке | чат итер.7 + Conway-Sloane | LEAN_PROVED (точная арифм. ℤ[√5], уже есть код) |
| D0-ICOSIAN-LEECH-BRIDGE-001 | E₈→Λ₂₄ икозианная конструкция (R.Wilson) | чат итер.7 + SPLAG гл.8 | BRIDGE (внешняя теорема, cite) |
| D0-XI5-TORUS-DEFECT-001 | ξ₅=φ⁵−11=φ⁻⁵, дефект адреса тора; Tr T⁵=−11 | чат итер.10, GOLDEN §52 | LEAN_PROVED (cert `vp_xi5_torus_defect.py` готов, PASS) |
| D0-VACUUM-CUBIC-WINDOW-001 | λ³=359λ+2574 (e₁=0,e₂=−359,e₃=2·1287); конкурент S_DE-квадратике | чат итер.1 | PYTHON_CERTIFIED→LEAN |
| D0-Q8-DEDEKIND-MINIMALITY-001 | Ω₈≅Q₈ вынуждено гамильтоновостью (Дедекинд 1897); [Q₈,Q₈]=Z=Φ={±1} | чат итер.5 | LEAN_PROVED (перебор групп ≤8 + cite) |
| D0-WINDOW44-GROUP-SPECTRUM-001 | (ℤ/44)*≅ℤ₂×ℤ₂×ℤ₅; характеристич. подгруппы {1,4,5,20}; 20=4×5 | чат итер.4 | LEAN_PROVED (конечная группа) |
| D0-MSD20-CABIBBO-001 | m_s/m_d=20=φ_E(44) (LEM-зазор алиасинг) → sinθ_C=1/(2√5) через GST | чат итер.4 | core(LEM) + BRIDGE(GST) |
| D0-CKM-WOLFENSTEIN-QUAD-001 | A=7δ₀, ρ̄=1/2π, η̄=3δ₀; γ=arctan(3π/φ³)=65.80°; J,β,α out-of-sample | чат итер.2 | PYTHON_CERTIFIED (HYP-пакет, фальсификатор) |
| D0-PMNS-DELTA0-FAMILY-001 | sin²θ₁₂=1/3−2δ₀², sin²θ₁₃=1/4φ⁵, sin²θ₂₃=1/2+δ₀/2, Δm²ratio=δ₀/4 | чат итер.3 | PYTHON_CERTIFIED (бьёт GRA/GRB, см. отчёт) |
| D0-MIXING-HIERARCHY-INVERSION-001 | ранг3-невырожд (кварки малое смеш.) vs ядро30-вырожд (лептоны большое) | чат итер.3 | LEAN_PROVED (линал графа) |
| D0-KERNEL-ZONE-SPLIT-001 | ядро 30=8⊕10⊕12 (зонная подструктура архива) | чат итер.3 | LEAN_PROVED (вычислено) |
| D0-DIM-LADDER-COMPACT-001 | Q(D)=φ^(D−4); δ-каскад δ₋ₙ=δ₀ⁿ⁺¹; квант=1 при D=4 | чат итер.6, док.Вахрушева | LEAN_PROVED |
| D0-VIETA-GALOIS-ABCD-001 | ABCD=данные Галуа ℚ(√5); A,B инвариантны, C,D сопряж.пара | чат итер.6 | LEAN_PROVED (проверено) |
| D0-TIME-2D-PISOT-001 | слой времени=T² вынужден квадратичной Пизо-минимальностью; разбиение гладкое ⟺ Пизо | чат доп. | core(THE) + cite Adler-Weiss |
| D0-SIGNATURE-31-SPLIT-001 | (3,1) раздельно: 3=rank(adj), 1=модулярный поток; стрела=Пизо-сжатие ψ | чат доп. | frontier→core |
| D0-IF-KS-ENTROPY-001 | I_f=log φ = h_KS(T) торального автоморфизма (владелец GW-цели) | чат итер.8 | core→passport-владелец |
| D0-ZETA8-REGISTRY-001 | семь воплощений одного ℤ₂ (Галуа/Люка/Q₈-центр/спинор/ориентация/detT/удвоение) | чат, сводно | core (мета-теорема связности) |

**Семь воплощений ℤ₂ — отдельный приоритет**: это не claim, а *структурная нить*,
связывающая ≥7 существующих claim-ов. В графе оформить как узел-концентратор с рёбрами
`same_Z2_incarnation` ко всем семи. Делает связность видимой.

---

## 4. ВНЕШНИЕ ЯКОРЯ И ПАСПОРТНЫЕ ЦЕЛИ (из глубокого исследования)

Влить в `08_PASSPORTS/` как новые манифесты-цели (НЕ как core):

| Паспорт | Содержание | Статус-цель | Файл-якорь |
|---|---|---|---|
| E8_QUANTUM_CRITICAL | CoNb₂O₆: m₂/m₁=φ в E₈-спектре (Coldea 2010, Science 327) | EXTERNAL-ANCHOR | новый |
| H0_EVOLVING_W | H₀(z)-тренд ↔ эволюц. w из Rₙ=φⁿ−1; DESI DR2 w₀>−1,wₐ<0 | EMPIRICAL-PASSPORT | расширить DESI/ |
| NUFIT_PMNS | sin²θ₁₂=0.3055 vs NuFIT 6.0; победа над GRA(0.276)/GRB(0.345) | EMPIRICAL-PASSPORT | новый |
| LIGO_IF_LOGPHI | I_f=log φ=h_KS, полоса 35–85 Гц (уже есть GWOSC_LIGO/) | THEOREM-TARGET | расширить |

**Снять/разграничить (риски из исследования):**
- g−2: закрыт решёточным HVP (WP25) — пометить DEPRECATED как «цель новой физики».
- W-масса CDF II: конфликт CMS/ATLAS — не использовать.
- стерильное ν (LSND/MiniBooNE эВ): исключено KATRIN+MicroBooNE 2025 — **явно разграничить**
  с 30-мерным архивом D0 (новая строка-disclaimer D0-ARCHIVE-NOT-STERILE-NU-001, type=no-go/clarification).
- S₈: почти закрыт (KiDS Legacy ушёл к Planck) — снять как твёрдую цель; добавить
  внутренний фальсификатор H₀↑/S₈ как passport-проверку.

---

## 5. ФАЗЫ РАБОТ (для Claude Code, по порядку)

### ФАЗА 0 — Инфраструктура и фриз базы (0.5 дня)
- [ ] T0.1 Зафиксировать v14 как ветку `base-v14` (git init если нет, тег).
- [ ] T0.2 Установить graphify (`pip install graphifyy`), проверить регенерацию графа из CSV.
- [ ] T0.3 Написать `tools/validate_csv.py`: проверяет схему (16 колонок), валидность enum-значений,
      что для каждого LEAN_PROVED существует файл `lean_module`, для каждого PYTHON_CERTIFIED —
      файл `python_cert`. Падает на рассинхроне. **Это страж целостности.**
- [ ] T0.4 Написать `tools/check_firewall.py`: запрещает release_status=CORE-FORMALIZED при
      непустом assumption_ids; запрещает passport→core повышение между ревизиями (diff CSV).
- [ ] T0.5 Завести `00_ROADMAP/INTEGRATION_LOG.md` — журнал интеграции (что влито, откуда, дата).

### ФАЗА 1 — Интеграция «дешёвых» THE из чата (готовые доказательства) (2–3 дня)
Приоритет: то, где Lean-доказательство конечно и почти готово (перебор/линал/арифметика ℤ[√5]).
Для каждого — создать CSV-строку, перенести cert из наших скриптов, написать Lean-модуль.
- [ ] T1.1 D0-XI5-TORUS-DEFECT-001 (cert `vp_xi5_torus_defect.py` уже есть и PASS → Lean: ℤ[φ] арифметика).
- [ ] T1.2 D0-WINDOW44-GROUP-SPECTRUM-001 ((ℤ/44)*, конечная группа → Lean Decidable).
- [ ] T1.3 D0-Q8-DEDEKIND-MINIMALITY-001 (перебор групп ≤8 + тройное тождество).
- [ ] T1.4 D0-KERNEL-ZONE-SPLIT-001 + D0-MIXING-HIERARCHY-INVERSION-001 (линал K(9,11,13), уже считается).
- [ ] T1.5 D0-VIETA-GALOIS-ABCD-001 + D0-DIM-LADDER-COMPACT-001 (тождества φ, проверено).
- [ ] T1.6 D0-ICOSIAN-E8-CARRIER-001 (точная арифметика ℤ[√5], код из итер.7 → Lean Gram/Морделл).
- [ ] T1.7 Регенерировать граф, прогнать validate_csv + check_firewall.

### ФАЗА 2 — Семь воплощений ℤ₂ как мета-слой связности (1–2 дня)
- [ ] T2.1 D0-ZETA8-REGISTRY-001: строка-концентратор.
- [ ] T2.2 Расширить graphify-вход рёбрами `same_Z2_incarnation` (7 рёбер к существующим claim).
- [ ] T2.3 Lean: единый файл `D0.Synthesis.Z2Registry` с теоремами тождества всех семи ℤ₂
      (Галуа-сопряжение = чётность Люка = центр Q₈ = … ), где это формализуемо.
- [ ] T2.4 Документ `01_BOOKS/SYNTHESIS_Z2_SPINE.md` — нарратив нити (из нашего чата).

### ФАЗА 3 — Космология/время: подведение владельцев под паспортные цели (3–4 дня)
- [ ] T3.1 D0-TIME-2D-PISOT-001 + D0-SIGNATURE-31-SPLIT-001 (фича 2D, раздельный 3+1).
- [ ] T3.2 D0-IF-KS-ENTROPY-001: связать I_f=log φ с h_KS(T) — поднять GW-цель из «голого числа»
      до «владелец-теорема + паспорт».
- [ ] T3.3 D0-VACUUM-CUBIC-WINDOW-001 vs существующая S_DE-квадратика: оформить как **развилку**
      (две конкурирующие core-формы окна), cert сравнения, паспорт-различитель против DESI DR3.
- [ ] T3.4 Паспорт H0_EVOLVING_W: манифест, негативные контроли, фальсификатор H₀↑/S₈.
- [ ] T3.5 Разграничение D0-ARCHIVE-NOT-STERILE-NU-001 (no-go/clarification).

### ФАЗА 4 — Флейвор: CKM/PMNS пакеты + цепь Кабиббо (3–5 дней)
- [ ] T4.1 D0-MSD20-CABIBBO-001: core(LEM-зазор алиасинг) + BRIDGE(GST). **Формализовать LEM-зазор**
      (алиасинг класса-5) — это третий мягкий сустав, цель фазы.
- [ ] T4.2 D0-CKM-WOLFENSTEIN-QUAD-001: cert с E-учётом + out-of-sample (J,γ,β,α). Статус PYTHON_CERTIFIED,
      release=THEOREM-TARGET-SHARPENED (фальсификатор γ=65.80° на ±1°).
- [ ] T4.3 D0-PMNS-DELTA0-FAMILY-001: cert + паспорт NUFIT_PMNS с явным сравнением GRA/GRB.
- [ ] T4.4 Паспорт E8_QUANTUM_CRITICAL (Coldea) как EXTERNAL-ANCHOR для икозианной ветви.

### ФАЗА 5 — Закрытие открытого Lean-бэклога и frontier (континуально, параллельно)
- [ ] T5.1 Разобрать `LEAN_TRANSLATION_BACKLOG.csv`: 14 OPEN + 4 CERT_SCAFFOLD статусов.
- [ ] T5.2 CVFT frontier (D0-CVFT-F1..F8): оценить, какие реально доказуемы, какие → BRIDGE/DEPRECATED.
- [ ] T5.3 GW passport targets (D0-GRAV-WAVE-002/004/008/010, D0-LIGO-003/004): довести до
      замороженных манифестов или честно пометить THEOREM-TARGET.

### ФАЗА 6 — Гигиена и публикационная нарезка (континуально)
- [ ] T6.1 Снять deprecated/риски (g−2, W-масса) с записью причин.
- [ ] T6.2 Сверить книги (01_BOOKS) с CSV — нарратив не должен противоречить статусам.
- [ ] T6.3 Подготовить 4 публикационных блока (см. §7) как срезы CSV по доменам.

---

## 6. CLAUDE CODE: РАБОЧИЙ ЦИКЛ И ИНСТРУМЕНТЫ

**Каждая задача Tx.y исполняется одним циклом:**
```
1. Прочитать целевую CSV-строку (или создать черновик).
2. Реализовать артефакт:
   - Python cert → 05_CERTS/vp_<claim>.py (должен печатать PASS/флаги, exit 0).
   - Lean модуль → 09_LEAN_FORMALIZATION/D0/<Domain>/<Name>.lean (0 sorry).
3. Обновить CSV-строку (lean_status, release_status, *_exists, python_cert, notes).
4. Прогнать tools/validate_csv.py  → должен пройти.
5. Прогнать tools/check_firewall.py → должен пройти.
6. Регенерировать граф (graphify) → закоммитить json/dot/html.
7. Дописать INTEGRATION_LOG.md.
```

**Три скрипта-стража, которые Claude Code пишет в Фазе 0 (это каркас контроля качества):**
- `validate_csv.py` — синхрон CSV↔файлы↔enum.
- `check_firewall.py` — anti-promotion + assumption-discipline (diff между ревизиями CSV).
- `regen_graph.sh` — обёртка graphify + проверка, что счётчики узлов/рёбер не упали случайно.

**Definition of Done для claim-а** (Claude Code проверяет механически):
☑ строка в CSV с валидными enum ☑ артефакт(ы) существуют и зелёные ☑ для CORE-FORMALIZED
нет ASSUMP-* ☑ граф регенерирован ☑ запись в INTEGRATION_LOG ☑ нет нарушений firewall.

---

## 7. КРИТЕРИИ УСПЕХА ПРОЕКТА (измеримые)

**Метрики из CSV (отслеживать в каждом релизе):**
- N(CORE-FORMALIZED) — растёт; цель этапа 1: +12 (наши THE-результаты).
- N(OPEN)+N(CERT_SCAFFOLD) — падает к нулю по управляемым звеньям.
- N(claim с пустым артефактом при не-OPEN статусе) = 0 (валидатор гарантирует).
- N(нарушений firewall) = 0 всегда.
- Покрытие: доля claim с И Lean И cert (сейчас ≈ часть; цель — все core).

**Качественные ворота:**
1. Цепь Кабиббо закрыта до «2 THE + 1 GST-мост» (LEM-зазор алиасинга формализован).
2. Три мягких сустава закрыты или явно помечены (списки ролей, чётность+2, алиасинг).
3. Семь воплощений ℤ₂ видны в графе как явная нить.
4. Каждая паспортная цель имеет фальсификатор (γ=65.80°, Σm_ν, H₀↑/S₈, I_f-полоса).
5. Все риски-2026 (g−2, W, стерильное ν, S₈) обработаны записью, не молчанием.

**Анти-цель (чего НЕ делать):**
- Не объявлять «Immutable/Grand Singularity» (нарушение собственного §00.4/05.5; именно
  это сломало v17 — в v14 НЕ переносить).
- Не повышать паспорт до core. Не называть подогнанную константу выведенной.
- Не строить заново то, что в CSV уже CORE-FORMALIZED.

---

## 8. ПЕРЕДАЧА В CLAUDE CODE (стартовый промпт-ядро)

> Контекст: репозиторий D0_v14. Источник истины — `03_THEORY_MAP/theory_status_map.csv`
> (схема и enum в `D0_v14_ARCHITECT_PLAN.md` §1). Граф регенерируется из CSV через graphify.
> Твоя работа — исполнять задачи Tx.y из §5 плана по рабочему циклу §6, соблюдая лестницу
> зрелости §2 и firewall (запрет повышения статуса риторикой, запрет passport→core).
> Definition of Done — §6. Начни с Фазы 0 (T0.1–T0.5): напиши трёх стражей и зафиксируй базу.
> Каждую интеграцию бери из таблицы §3 (новые claim_id) и §4 (паспорта); тексты доказательств
> и cert-скрипты — из приложенного отчёта `D0_CKM_INTERFACE_ITERATION_REPORT.md` и
> `vp_xi5_torus_defect.py`. После каждого claim — validate_csv + check_firewall + regen_graph.

**Приложить в Claude Code вместе с репозиторием:**
- этот план (`D0_v14_ARCHITECT_PLAN.md`)
- `D0_CKM_INTERFACE_ITERATION_REPORT.md` (10 итераций, все доказательства+скрипты)
- `D0_RESEARCH_ADDENDUM_cosmology_sterile_2D.md` (паспортные цели + риски)
- артефакт исследования (топ-10 находок, носители)
- `vp_xi5_torus_defect.py` (готовый эталон cert-формата)

---

## 9. РИСК-РЕЕСТР ПРОЕКТА (инженерный, не теоретический)

| Риск | Митигация |
|---|---|
| CSV и файлы рассинхронятся | validate_csv.py в Фазе 0, прогон после каждой задачи |
| Тихое повышение статуса | check_firewall.py на diff CSV |
| Lean не собирается (mathlib версия) | зафиксировать toolchain в lakefile; CI из D0_LEAN_*/03_CI |
| Перенос v17-овершутов | белый список §3; всё вне списка — только после ручной ратификации архитектором |
| Граф «распух» дубликатами | regen_graph.sh проверяет дельту счётчиков; дедуп по claim_id |
| Потеря истории решений | INTEGRATION_LOG.md обязателен в DoD |

---

*Конец плана v1.0. Следующий шаг архитектора: по запросу — детализировать любую фазу до
уровня отдельных Lean-сигнатур и cert-спеков, либо сгенерировать стартовые файлы стражей
(validate_csv.py / check_firewall.py / regen_graph.sh) для Фазы 0.*
