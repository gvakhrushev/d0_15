# B112. Точная сетка и CODE-only plane для precision 32768

**Результат.** Для существующих `paid_padding.old.plane_blocks` и `plane_upper` из A42 получены строгая положительная Golden G-сетка, новый π/8 power и оба signed Cayley endpoint powers при `t=2^-6000`, `m=5376`. Все степени находятся в `1≤k≤q`, `bit_length(q)=32773`. Равномерная all-column ошибка одной полной plane не превосходит

    μ=(2^5375+40·5376)·2^-32768 <2^-27392.                  (1)

Это precision input для следующего paid family/clock, а не новая family, полный compiler для произвольного skew или физическое исполнение гигантского word. Старые A54 SOURCE, actual B105 post и отдельный старый post-probe не изменены. `physical_C_closed=false`, `GR_closed=false`.

[Публичный модуль](plane_grid_32768.py), [строгий grid certificate](GRID_32768_CERTIFICATE.json), [генератор](certify_grid_32768.py), [проверка и inventory](B112_PLANE_PRECISION_CHECK.json). Проверка использует существующую B80 целочисленную арифметику и локальную зависимость `gmpy2==2.3.2`; она не обращается к float для доказательства сетки.

## 1. Реальная грамматика и контракт подключения

`direct/round49/paid_padding.py` связывает `old` с `direct/round42/fixed_post_paid_family.py`. Его `plane_blocks(a,b,k,sam,macros)` использует только CODE wires: affine X/CX, затем A41 `star_blocks`, затем обратный по порядку affine список. X каждого раза заново реализуется тем же native π/8 шаблоном; его фактический word не объявляется своим буквальным обратным. Ни один helper не заимствован из WORK.

Для следующего владельца доступен API:

```python
uniform_grid()                         # (pn, q, certificate)
Macros().ks['pi8']                     # новый положительный power
Macros().x(q, helper)                  # ровно A38 plane X/Z/pi8 grammar
plane_power(sign, m=5376, step_bits=6000)  # 1 <= k <= q
```

`Macros` намеренно предоставляет только методы, используемые A42 plane; прежний A38 `Macros` требует certificate с error_bits=20000 и не подходит для нового precision. Шаблоны `power`, `pi8`, `z`, `x` напрямую используют существующие методы A38 с **новым** k8. Например компактный DAG `x` имеет ровно `20 k8` G и 2 CX на двух CODE wires. Остальные A38 angle macros для этой plane грамматики не используются.

## 2. Certified uniform positive-power grid

Повторён B80 метод с `S=2^67584`: через целочисленный `isqrt`, направленное округление, шесть half-angle шагов и знакопеременный atan построены внешние интервалы `θ=atan(sqrt(p))` и `π=16atan(1/5)−4atan(1/239)`. Для γ=`θ/(2π)` взят рациональный CF кандидат середины интервала; сам CF является лишь поиском. Затем на всех целых данных проверено

    gcd(pn,q)=1,    E=max(|q·γ_lo−pn·S|, |q·γ_hi−pn·S|),
    qE<S,           16·2^32768<q,       bit_length(q)=32773.

Следовательно `|γ−pn/q|<1/q²` для полного интервала. Перестановка `k·pn mod q` при `1≤k≤q` и ошибка orbit `<1/q` дают для вычислимой цели с узким outward interval операторную ошибку строго `<16/q<2^-32768`. Остаток 0 отображается в положительное `k=q`; отрицательные G-повторы не вводятся.

Для π/8 его turn равен `1/16`; выбран ближайший `j/q` и `k8≡j·pn⁻¹ mod q`. Целочисленно проверены `|16j−q|≤8`, `1≤k8≤q`, modular congruence и общий grid bound. Это отдельный сертификат **нового** π/8, а не использование старого power с ошибкой `2^-20000`.

## 3. Два Cayley endpoints и all-column error

Для знака s целевой двухплоскостной Cayley угол равен `2 atan(s·2^-6001)`. A41 Walsh star применяет один и тот же малый G-power в `L=2^(m−1)` parity terms, поэтому требуемый turn отдельного power:

    τ_s=s·atan(2^-6001)/(π·2^5375).

`plane_power` вычисляет его двусторонний dyadic interval той же B80 atan/pi арифметикой, округляет midpoint к одной из q клеток и применяет modular inverse. Проверено для обоих s: интервал и клетка дают погрешность не более `3/(4q)`, orbit добавляет строго `<1/q`, следовательно каждый физический малый SO(2) target имеет error `<2^-32768`. Проверки также подтверждают разные signed powers и `k_++k_-=q`. Изменения native exponent возникают только в этой новой plane family; выбор степеней и его вычислительные ресурсы не объявляются бесплатными физическими стадиями.

Для всех CODE columns и любых `a<b`, A41 Walsh identity даёт точную identity вне выбранной plane и `L` фактических G-повторов одного выбранного power. Телескопическая all-column оценка star не больше `L·2^-32768`. В affine части на каждом из не более m X перед star и тех же m X после неё π/8 macro имеет 4+12+4=20 приближённых малых поворотов; обе стороны дают `40m·2^-32768`. Все CX точны. Так получается (1), включая случай разных actual forward/reverse приближений. Это сравнительная **operator** error на всей CODE Hilbert space и tensor identity на WORK, не только ошибка подготовленной χ.

## 4. Реальная стоимость и проверка

Для любого `a<b`, `L=2^5375`, выбранного endpoint `k≤q`, числа 1 в a не более 5376, а Hamming distance не более 5376. Существующий `plane_upper` непосредственно даёт componentwise upper

    G  ≤ L·q + 40·5376·k8,
    CX ≤ 5375·L + 2·5375 + 4·5376.

Точные hex-целые сохранены в receipt: `G_upper.bit_length=38148`, `CX_upper.bit_length=5388`. Это upper на неподполненное plane word. Новый владелец должен использовать фактический `counted_pad`, общий control length и новый `Nbase/K`; старая цена или старый `K` не переносятся. Uniform upper действителен для обоих signed endpoints и всех пар basis labels.

`check_plane_precision.py` побайтно воспроизводит целый grid certificate, проверяет оба signed interval/cell bounds и реальные компактные макросы. Независимая небольшая all-column диагностика исполняет **148** полных A42 plane words и **2144** columns при `m=3,4`, сверяет знак, поддержку и точный inventory; surrogate G=R(π/8) в этой диагностике не выдаётся за Golden production gate или общее доказательство. Production-sized Walsh маски, повторы и полный path sum не раскрыты.

Остаются построение новой четырёхслотовой finite request family, равное оплачиваемое padding всех её labels, пересчёт clock/heat/readback и проверка полного plane-derived dual. Таблица конечных plane rows не доказывает сама по себе uniform finite comparison для произвольного совместно скомпилированного skew. Physical `V_h`, исходный marked transport и Cost−Info/GR по-прежнему открыты.
