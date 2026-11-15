# B98: независимый аудит четырёх строк A50

**Результат: PASS в области A49/B97.** Для выбранной typed SOURCE, canonical RAW fibre, born-product CODE, пустого `H₀=C`, фиксированного actual post и одного оплаченного Book `H+J` clock проверены четыре независимые finite price строки на каждой из 2688 MG2-осей. A50 не предполагает симметричность actual cross-kernel, точную обратимость двух скомпилированных control words или нулевую Q-строку. Огромный production word не исполнялся. Original `Dν`/marks, произвольный old carrier, физическая Cost−Info binding и refinement остаются открыты; `physical_C_closed=false`, `GR_closed=false`.

## 1. Новый split и all-insertion error

В действительном порядке A49 первые 1568 SOURCE slots, один SITE и восемь SIGMA заканчиваются первым RAW resource frame; это первый Q-cut. Затем идут обратный RAW frame, восемь REPORT, PORT_ZERO и прежний SC6; центральный знак и literal reverse образуют middle до второго cut. Последняя часть — возврат source. В exact SourceI-profile, до G/CX replacement,

    W₀=B₀† S₀ B₀,     S₀=D₀† Z D₀=S₀†.

Фактический compiled split `W=C S B` сохраняется без подстановки `C=B†` или `S=S†`. Проверены affine диапазоны всех восьми REPORT, 34112 resource wires, SC6, shared SITE/port/Spin/aux и старый compiler helper: ни один не пересекает 5376 CODE wires. Вместе с B96 CODE-target grammar это означает, что actual middle S не адресует CODE даже как control, и `[S,Y]=0` точно для CODE-only Y. CODE-control-only одного целого W само по себе этого вывода не дало бы.

[audit_split_and_transducer.py](audit_split_and_transducer.py) проверяет исходные два cut tags, принимает только закрытую SourceI-пару и демонстрирует отказ при незакрытой паре. Опираясь на A29/B82 all-column macro replacement, каждое полное SourceI² использует не более 16 единиц error на 2 прежних SourceI, а closed CZ — не более 32 единиц на не менее 5 SourceI. Поэтому `8·W.SourceI` является верхним числом units `2^-20000`. Вставка любого одного contraction `||Y||≤1` на закрытом cut не увеличивает норм оставшихся unitary множителей, и прежнее телескопирование даёт

    ||Φ(Y)−Φ₀(Y)|| ≤ e_W ||Y||,   e_W<2^-15800.

Это отдельное **all-insertion** сравнение к exact SourceI-profile, а не вывод из конечного endpoint error и не SOURCE-to-ideal target error. Оно требует inherited all-column A29 macro theorem и закрытых cuts; никаких других marks автоматически не переносит.

## 2. Dimension-free kernel без симметричного actual L

Обозначим `u_b=B₀,b ω` с полным SOURCE/private/fresh remainder. Все labels лежат в исходном chart, `||Y_b−Y_c||<156σ`; B91 `M1≤1748`, обе prefix ошибки и `σ=2^-80` дают

    δ₀=sup_(b,c)||u_b−u_c|| <2^-61.

Это полный prepared-state bound, не partial trace или скаляризация fresh source. Для `V e_b=e_b⊗u_b`, `J e_b=e_b⊗u_ref`, `Δ=V−J`, и любого skew Y, точная A44 algebra записывается

    Φ₀(Y)−(D Y+Y D)/2
      =Δ†(Y⊗S₀)Δ−(A Y+Y A)/2,
    D=Φ₀(I),  A=Δ†(I⊗S₀)Δ.

Линейные по Δ части сокращаются из `S₀=S₀†`; норма остатка не более `2δ₀²||Y||`, независимо от числа CODE labels. К actual insertion добавляются skew error не более `2e_W` и symmetric error не более `e_W`. Actual matrix `L_cb=⟨ω,C_c S B_bω⟩` в общем случае nonsymmetric; её симметрия нигде не предполагается.

[check_kernel_and_pb.py](check_kernel_and_pb.py) независимо проверяет равенство для всех трёх символических skew-направлений CODE размерности 3 и сохраняет отдельную symmetric часть намеренно nonsymmetric actual kernel. [check_nonsymmetric_and_clock.py](check_nonsymmetric_and_clock.py) дополнительно предъявляет пару split с одинаковым конечным endpoint, но различным insertion kernel: endpoint equality не заменяет установленную выше all-insertion bound. Оба примера — точные рациональные fixtures, не вычисление giant kernel.

Для `μ=c_ref−2gIτ(Y₀)`, `τ=||M−μI||`, B65/B96 дают `τ/(gσ)<2^-41`. С `e_U<2^-9247`, `gσ>2^-3208` и реальными A48 errors A44 bound воспроизводится независимо:

    |d_Qb,analytic−½d_Pf,reduced|
      ≤(3/4)[(τ/(gσ))(2δ₀²+2e_W)+e_W/(gσ)] + e_U/(gσ)
      <2^-160.

Для каждого Qf/Qb применяется своя допустимая вариация; оценка не утверждает нуль ни одной из них. Полные finite endpoints дополнительно учитывают A47 control error, finite-J Taylor и полный clock heat; тогда `|FD_Qb/Γ−½ FD_Pf/Γ|<2^-159` на соответствующей MG2 оси.

## 3. Q-swap и точная область равенства цены

В A49 `Q_f+` исполняет `P̂_−` в первом слоте, а `Q_b−` — **тот же самый фактический** `P̂_−` во втором. Пустой слот имеет тот же оплаченный размер; источник, обе верхние/нижние ветви, fixed post, общий layout и последний retention G одинаковы. Поскольку S CODE-disjoint, этот конкретный word коммутирует с S и полные endpoints совпадают. Для `Q_f−`/`Q_b+` аналогично используется один и тот же `P̂_+`. Не требуется, чтобы `P̂_−` было обратным `P̂_+`.

Обозначая prefix unitaries двух равнодлинных историй `A_j,A'_j`, layerwise `V_j=A'_j A_j†` равен I до и после переставляемого square сегмента. Это даёт сопряжение полного T и P растущего clock, включая все birth-complements, затем feedback и всей тепловой матрицы. Поэтому **полная оплаченная** `H+J(Q_f+)` равна `H+J(Q_b−)` и наоборот; finite Qf/Qb contrasts противоположны. Эта цена — Book reader A49, не доказанная физическая Cost−Info.

Наш независимый точный fixture повторяет conjugacy обоих полных growing clocks, feedback и heat для **двух не являющихся взаимными inverse** слов и произвольного nonsymmetric controlled return. При этом фиксированный промежуточный CODE mark имеет разные pulled-back maps. Поэтому exact price swap не доказывает original `Dν`, equality маркированных историй или same-FN admission. Цена и marks имеют разные интерфейсы.

## 4. Pb перед постом и рациональные бюджеты

Для `r=||Mχ||`, `ξ=Mχ/r`, `U*ξ=χ` и реального skew X исходный `P_b†` расположен **до** фиксированного U*. Его аналитическая целевая строка

    c'_Pb=−r ξᵀ X ξ=0.

Это не повод перемещать control после post без замены генератора: в 3D `[U*,X]` вообще ненулевой. Exact fixture проверяет правильную ориентацию, нулевой target derivative, ненулевой arbitrary-post negative control и различие before/after направлений. Actual Uhat и независимо построенные control endpoints имеют отдельно учтённые ненулевые ошибки; A50 не заявляет exact price stationarity.

[audit_price_bounds.py](audit_price_bounds.py) считывает raw B97/A47/A48/A49 receipts и независимо от A50 `bounds()` воспроизводит полные рациональные значения и signs:

    |FD_Pf/Γ| <2^-108,
    |FD_Qf/Γ|, |FD_Qb/Γ| <2^-108,
    |FD_Pb/Γ| <2^-189,
    ||(FD_Pf,FD_Qf,FD_Qb,FD_Pb)/Γ||₂ <2^-102.

Последняя граница вычислена точным суммированием квадратов 4×2688 реальных рациональных envelopes. Её нельзя вывести одной только грубой оценкой трёх наборов `<2^-108`. В неё включены B97 third-order scalar/product and actual post weight, finite-J Taylor, обе реальные control approximations и R11 heat на общем paid clock.

Для **произвольного** real CODE skew A50 отдельно получает только аналитические dual bounds `Pf<2^-40`, `Qf/Qb<2^-41`, `Pb<2^-6039`. Это другие оценки: finite all-skew dual и original physical `V_h`/all-controls norm не доказаны выбранными 2688 MG2 finite rows. Закреплённые значения, включая это ограничение, проверены в [INDEPENDENT_ROW_BOUNDS_CHECK.json](INDEPENDENT_ROW_BOUNDS_CHECK.json).

## 5. Что остаётся исходной задачей

Нужно связать фактические source/frontier maps `Dν B` и их first jets с полным original marked descriptor на том же retained remainder, отдельно разрешить используемое A23 vacuum extension и все native births/marks, установить допустимость четырёх slot directions и исходный `V_h` right lift. Нужны также реальные old/input/WORK/scene/record/READY/Info строки и физический Cost−Info ledger/refinement. Ни малость четырёх заданных строк, ни exact Q-swap цен, ни математическая конечность огромного word не решают этих вопросов. Нет заявления о физической стационарности или выводе ОТО.
