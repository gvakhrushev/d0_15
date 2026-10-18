# D0 → ОТО: два физических типа источника одной Book03-цены и точная граница универсальной связи

**18 октября 2026. Владелец:** ограниченный source-consumer существующего Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334), задача `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. **Статус:** точная конечная алгебра и условная C²-редукция источника / физическое D0→ОТО ОТКРЫТО. Новое действие, новая цена, независимая материя, Newton-калибровка и физический селектор НЕ вводятся. Ни claim, ни BOOK, ни Lean не повышаются.

**Прямые входы:** [полная AF×scene цена §§6.18–6.22](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md), [Book03 owner §03.3.2](../../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md), [прямой finite feedback source §§5–8](sources/d0_af_full_feedback_first_source_2026-10-17/RESULT_RU.md), [текущая стратегическая композиция §7.9](A4D_STRATEGIC_SYNTHESIS_FOUNDATIONS_TO_GR_2026_10_17.md), [исходный whole-retained Julia128](A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md) и [полный Ward](A4D_FULL_EXPERIMENT_WARD_AND_METRIC_DESCENT.md). Результаты потребляются на ОДНОМ объявленном AF×scene return carrier, а не путём склеивания разных цен по имени.

## 1. Один настоящий оператор, а не две придуманные энергии

У владельца двухтактовой цены при `0<z<1`, старых блоках `j`, multiplicities `D_j`, `K=Σ_j D_j dim old_j=F_(2N+9)`, и reference factor `nu`:

```
J(E,B) = -nu K Tr_s log Q(B)
         -nu Σ_j D_j Tr_(old_j⊗scene) log R_j(E_j,B),
Q(B)=I-zB,
R_j=(1-z)I+z[I-4E_j(I-E_j)]⊗(I-B).
```

`B` — полное *уже принадлежащее* scene-feedback на retained528 cut. Реальные нулевые feedback-моды (264) и positive-моды (184,36,44), их полный scene complement, actual AF regular right multiplicity и всё `reference128` сохраняются. Скалярный `J` — **компонент** исходного stack, не весь `Cost-Info` и не новое состояние matter.

Положим `p=phi^-1`, `e0=p²`, `L=4p³=4e0(1-e0)=4(1-2e0)`, `a=1-L=p^6`. В фиксированной исходной сцене `B0`, `0<=B0<=I` обозначим

```
Q0=I-z B0,   R0=(1-z)I+za(I-B0),
C0=Tr_s[(I-B0)R0^-1] > 0,
W0=Q0^-1 + a R0^-1 > 0.                                 (1)
```

Здесь `C0` — **операторный геометрический source-coefficient** на `e0`, не дополнительно выбранная константа Ньютона. Он ненулевой из-за действительных неединичных eigenmodes сцены.

## 2. Новая основная теорема: совместная геометрия + scene source из ОДНОГО J

Пусть `c>0` стремится к0, `E_j(c,y)=e0 I+c F_j(y)` и `B(c,y)=B0+c M(y)` — действительно предоставленные гладкие operator germs на исходных old×scene Hilbert spaces. `F_j` — настоящие AF geometric/star insertions, `M=M^*` — возможная самостоятельная *scene-response direction*, НЕ заранее назначенный материальный тензор. Требуются положительные contractions для всех малых c, один и тот же return cut, а на compact chart поля `y` — uniform operator C³ bounds `F_j,M`, включая physical preparation, observer и clock там, где они являются genuine arguments. Вся исходная работа/return leakage остаётся в `J`, новые исходы не отбрасываются.

Тогда НА ОДНОЙ И ТОЙ ЖЕ конечной цене

```
J(c,y)-J(0)=nu K c z[
    L C0 * barF(y) + Tr_s(W0 M(y)) ]+ O_C²(nu K c²),
barF=(1/K) Σ_j D_j Tr_(old_j) F_j .                     (2)
```

После **математической** нормировки одним field-independent коэффициентом `a_ref=nu K c z L C0>0` имеем

```
A_c(y)=[J(c,y)-J(0)]/a_ref
    = barF(y) + (1/(L C0))Tr_s(W0 M(y))
              + O_C²(c).                               (3)
```

Не только значения, но **все первые и вторые полевые источники** в общем C³ chart сходятся. Константа ошибки не зависит от `K` и reference multiplicity `nu`, если normalised old-trace jets и scene operator bounds равномерны; число scene coordinates=528 фиксировано. Это не утверждает automatic source control после spatial reconstruction или при реальном `h^{-2}` #216. Нормировка (3) не переопределяет физические часы, Newton constant или полную action: она только сравнивает источники.

**Доказательство.** `lambda(E)=4E(I-E)`; при `E=e0I` верны `lambda(e0)=lambda'(e0)=L`. Первый джет `R_j` равен `-zc[L F_j⊗(I-B0)+a I⊗M]`, а первый джет `Q` равен `-zcM`. Для positive matrices `D Tr log A=Tr A^-1 DA` даже при `[M,B0] !=0`; при `c=0` тензорный resolvent разделяется. Это немедленно даёт (2). Floor `Q,R >= (1-z)I` и uniform bounded C³ source jets дают (3) с `O_C²(c)` через многомерный интегральный Taylor remainder. Полные zero feedback modes НЕ создают `q log q` singularity. Не требуется ни независимая Shannon-mean программа, ни постулированный stress.

**Реальный потребитель:** если `barF` является уже принадлежащим Palatini/star-limit, а настоящий native `M(g,omega,psi)` существует, то его действительный candidate matter/spin metric source — не остаток `G_{mu nu}`, а прямая вариация исходного оператора:

```
D_y A_0[V] = D_y barF[V] +
              (1/(L C0)) Tr_s(W0 D_y M[V]).             (4)
```

При `V=delta g` это даёт metric stress, а при `V=delta omega,delta psi` — connection/spin и собственные matter equations. Их лоренцева covariance, независимая физическая допустимость, Ward-сохранение, локальность, source scales и истинная joint stationary sequence ЕЩЁ НЕ доказаны. Если `M` не зависит от prepared matter, то (4) не даёт независимой материи, как бы красиво ни выглядел коэффициент.

## 3. Универсальная гравитационная связь: точная проверка и неожиданная развязка

Геометрический coefficient при действительно moving `B`:

```
g'_B(e0)=zL C(B),
C(B)=Tr_s[(I-B)((1-z)I+za(I-B))^-1].
```

Его ПОЛНАЯ производная по любой, в том числе некоммутирующей, `dot B`:

```
D_B C[dot B]=-(1-z) Tr_s[R(B)^-2 dot B].              (5)
```

Значит при произвольных конечных не-изоспектральных возбуждениях B эффективный гравитационный коэффициент GENERICALLY меняется — такое семейство скорее scalar-tensor, чем постоянная Newton coupling. Простая изоспектральная вариация `dot B=[X,B]` зануляет (5), но также зануляет ПОЛНЫЙ trace-log scene source; она не поставляет самостоятельную материю.

**Положительный слабый предел:** если ИЗ ТОГО ЖЕ ФИЗИЧЕСКОГО ИСПОЛНЕНИЯ следует `B=B0+cM` с bounded M и `c→0`, то (5) даёт `C(B)=C0+O(c)` АВТОМАТИЧЕСКИ: в source limit гравитационная связь становится постоянной без отдельного isocoupling constraint. Сохраняется нетривиальный независимый `Tr(W0 M)` из (3). Его относительный коэффициент уже фиксирован текущим feedback оператором, не fitted. Это настоящая структурная возможность одной Book-компоненты, не вывод того, что D0 реализует требуемый `M`.

## 4. Даже конечный t имеет НЕпустые constant-coupling directions с ненулевым native scene response

Покажем аналитически, что tensor feedback НЕ принуждает материальную сцену изменять Newton coefficient. На собственных положительных feedback каналах `b_1,b_2∈(0,1)` кратностей `m_1,m_2` положим

```
Q_i=1-z b_i, R_i=(1-z)+za(1-b_i),
dot b_1=R_1²/m_1, dot b_2=-R_2²/m_2.                 (6)
```

Из (5) `D C=0` ТОЧНО. Но полный source (13ax) на `e0`:

```
D_B J/(nu K z)=Tr_s[(Q^-1+aR^-1)dot B]
               = H(b_1)-H(b_2),
H(b)=R(b)²/Q(b)+aR(b).                                (7)
```

`R(b)=aQ(b)+L(1-z)`; значит

```
H(b_1)-H(b_2)=(Q_1-Q_2)*
 [2a² - L²(1-z)²/(Q_1Q_2)].                            (8)
```

Для **демонстрационного** golden `z=p²`, `1-z=p`, `a=p^6`, `L=4p³`; `L²(1-z)²-2a²=2p^8(8-p^4)>0`. Все `Q_i∈(0,1]`, так что bracket в (8) строго отрицателен для ЛЮБЫХ `b_1!=b_2`. В собственном 528-cut действительно имеются два различных внутренних канала `b_1=L` (184), `b_2=L3=1-(130p-81)²` (36), оба в (0,1). Численно `D C=0`, но `D_B J/(nu K z)≈0.09642053726>0`.

Поскольку `∂ C/∂ b_2=-m_2(1-z)/R_2²!=0`, implicit function theorem дает реальную локальную **нелинейную** кривую `C(B(t))=C(B0)` точно, и `D J(t)/dt!=0`. Значит constant gravitational coefficient и independent *scene-current* алгебраически совместимы даже при фиксированном t. Это НЕ создание физического matter stress из произвольного spectral-controller: только необходимый operator-level source-space witness.

Общий positive feedback-contraction `0<=B<=I` математически реализуется на уже существующих scene retained528+complement22448 координатах без увеличения Hilbert width: каждому eigenvector retained cut достаточно одного ортогонального внешнего партнёра и реального 2×2 вращения с `sin² θ=b`. Полная рабочая операция унитарна и сохраняет leakage. Но actual D0 nine-word допускает лишь СВОЙ B: произвольные такие вращения НЕ объявляются нативными gates, field-dependent programme или физическими переменными. Kinematic realizability `!=` operational selection.

## 5. Строгие негативные контроли: откуда материя НЕ возникнет

1. В действительном fixed nine-word autonomous-scene owner `B0` задан оператором и **не зависит от состояния подготовки**. Если все изменения подготовленного CAR16 matter меняют только `rho`, но не `B`, то `D_rho J=0` тождественно: один этот state-independent feedback determinant НЕ создаст независимый state-dependent stress. Это НЕ запрет других уже принадлежащих state-dependent Book-компонент (Rayleigh, полная история, код) или настоящего backreaction `B(m)` в иной admissible программе.
2. Изоспектральное `M=[X,B0]` даёт `Tr(W0M)=0`. «Matter» в виде только смены scene basis/source frame фактически не создает никакого native scalar action/source. Нужен собственный nonisospectral, non-gauge operator jet, локально связанный с raw CAR16 и всеми его счетчиками.
3. `J` ОДНО не имеет внутренней scene-критичности по свободным положительным spectral `dot B>=0`: `D_B J=nu K z Tr[W0 dot B]>0` при `dot B!=0`, ибо `W0>0`. Материальная stationary dynamics требует реально дополнительных `S_rest` / actual constraint equations. Внутренняя сцена fixed gate может не допускать эти вариации — это не no-go для всех joint roots.
4. Нельзя объявлять `J_total=J_AF+J_v8` без исходного composite contract: trace-log serial/tensor composition неаддитивен. Даже при действительно аддитивном stack `J_v8` honestly scales `m_N=F_(2N+15)`, а `m_N/K→φ^6`: growing AF memory не подавляет его источник автоматически.

**Дополнительный source-scale gate:** если independently derived normalized matter/Rayleigh response имеет order-one stress, а `a_ref=nu K c z L C0`, ненулевое конечное relative coupling потребует `nu K c=Theta(1)` при bounded fixed z/B0, если ничто иное не нормирует/не масштабирует native material response. Это СЛЕДСТВИЕ ПРЕДПОЛОЖЕННЫХ размеров двух истинных источников, НЕ физический вывод `t(h)` и НЕ разрешение переписать размерную калибровку. Наличие v8 feedback source `O(m_N)` одновременно требует genuine cancellation, source-neutrality или `O(c)` per-spectator scaling перед таким совместным пределом. Нельзя просто отбросить J_v8 или назвать его материей по остаточному принципу.

## 6. Прямой путь к финальной ОТО и действительно один decisive native test

**Главный проверяемый missing arrow** — вычислить `M=D_c B|_(c=0)` НЕ из выбранного continuum stress, а из **одного фактического native joint** AF×Julia/scene full-return word, где raw CAR16, observer, Lorentz links, retained controller, preparation, all128 labels и Book03 stack принадлежат ТОМУ ЖЕ исполнению. Проверить:

- `M` зависит от independently varied raw matter `psi`, а не только от геометрии/конъюгации/априорно фиксированного scene B0;
- полная SAME программа действительно имеет нормированные `B0+cM` и `E0+cF` с контролируемыми `C²` first-source jets, включая whole-work/full128 leakage;
- истинные scene/matter Euler rows и full coordinate/embedding Ward заставляют `D_psi A_0=0` и divergence-free metric source из `Tr(W0M)`;
- на уже принадлежащем local Palatini coframe metric и nine volume-preserving Kerr–Schild directions истинный joint source converges к `R_(kk)-κT_(kk)`, с independent matter source вычисленным по (4), НЕ как `G-κT` residual;
- при spatial recovery и single fixed action scale вклад полного `S_rest` либо действительно включён в этот source, либо доказан controlled. Тогда девять нулевых equations + metric/matter Ward + Bianchi дают ALL10 `G+Λg=κT`, с Λ constant без подбора volume subtraction.

Если fixed scene `B` вообще не имеет такого material jet, честный ответ немедленный: путь THROUGH THIS Book03 component к independently sourced matter закрыт, и следующий native consumer — реально state-dependent Rayleigh/coherent/complete-record price с теми же φ/gauge/clock нормами. Это изменение маршрута, не новый каталог коэффициентов.

**Принципиальная граница:** (2)–(8) и source/witness являются точными доказательствами о принадлежащем feedback component и объявленном composite carrier; сама физическая admission/forcing, nonzero matter-map `M`, pure/scene stationary branch, source-controlled nonlinear joint limit и исходный raw all-ten/#216 терминал остаются OPEN. Даже positive spectral witness НЕ означает, что проект D0 уже вывел ОТО.

## 7. Проверки

[Targeted checker](certificates/a4d_single_native_feedback_sourced_einstein_bridge_check.py) проверяет golden identities, полный actual scene528 spectrum, independent geometric/scene source at weak scaling versus exact nonlinear logdet, same-source coefficient, positive/negative and isocoupling hostile controls. Аналитические доказательства §2–§5 верны для всего конечного carrier и noncommuting operator variations. Статус checks относится к математическому исследованию, не к физическому native admission, полному Lean или всей original dynamic.
