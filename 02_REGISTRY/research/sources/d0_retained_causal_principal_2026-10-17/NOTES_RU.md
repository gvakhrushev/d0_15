# Три причинных направления в существующей retained history

17 октября 2026. Это principal consumer уже существующего
[first-exit readout](../../A4D_RETAINED_HISTORY_CAUSAL_SOURCE.md), не новая
цена, preparation law или физически выбранный detector.

На flat positive metric G=s²I возьмём e=sO, O=I+Σθ_a R_0a+O(θ²).
Все16 CAR, восемь first-shell momenta и reference128 сохранены. Положим
X_ra=∂_rθ_a, t_a=X_0a, B_ia=X_ia (i,a=1,2,3). Для actual covector
connection M_r=-Γ_r^T линейного Lorentz metric g=s²O^TηO:

```text
M0=2Σa t_a E0a+Σa,b(Bab-Bba)Eab,
Mi=Σa[(Bia-Bai)E0a-(Bia+Bai)Ea0].                    (P1)
```

Формула получается непосредственно из полного Christoffel expression,
не из ограничения CAR. Пусть L_r=C_r Γ(M_r), J_r=L_r+L_r*. Тогда
ΣL_r=ΣJ_r=0. Столбец r матрицы M_r равен нулю. Для трёх actual characters
χ=(++--),(+-+-),(+--+) и actual labels16,8,24 имеем Jχ=Σχ_rJ_r.

```text
Qχ=Tr16 Jχ²/16,
ΣχQχ=Σi<a[2(Bia+Bai)²+4(Bia-Bai)²]
     =8Σr ||L_r||_HS²/16.                            (P2)
```

Последнее равенство доказывает точный kernel leading smooth forward jet:
∂0θ_a и три ∂aθ_a. На нём coefficient C_rΓ(M_r) равен нулю. Поэтому
leading smooth Julia/Walsh jet также нулевой: при строгом s>1 оба defect
roots положительны, а их Sylvester derivatives линейны по δP_r и δP_r*.
Это не finite-h утверждение обо всех history effects: последующие O(h²)
terms, n~h^-2 накопление и произвольные retained-history projectors здесь
не оцениваются. В raw basis одновременно преобразуются preparation и
output operator; commutator одного basis change не является сигналом.
Никакой uniform inverse из одних probability derivatives не выведен.
Для nonzero forward jet probabilities на isotropic flat preparation также
могут начинаться со второй степени; P2 — именно quadratic source.

Для spatial Fourier q и amplitude v полная диагональная union трёх
существующих событий даёт v*P(q)v, где

```text
Paa=6Σi≠a qi², Pab=-2qaqb (a≠b),
detP=32[6Σi≠j qi⁴qj²+13q1²q2²q3²].                 (P3)
```

Ранг3 при двух или трёх ненулевых spatial components; ранг2 на одной оси
(longitudinal kernel); ранг0 при q_spatial=0, независимо от q0. Это
доказательство по положительным квадратам и determinant polynomial,
не выборка рангов.

В тех же conventions EH principal density после настоящего boundary
divergence равна -2s²Σi<a(Bia-Bai)². Например q=v=(1,1,0) даёт
Qhist=8 и EH=0 (для real cosine средние вдвое меньше). Поэтому одна
transverse-cone identity не была тождеством по всем трём cone fields.
Ни одна ненулевая constant linear combination трёх диагональных Qχ не
пропорциональна полной curl²: coefficient comparison требует
wtotal=w1=w2=w3 и тем самым всех нулевых weights.

## Когерентный readout уже сохранённого регистра

Между сохранёнными label amplitudes существует проверяемый другой
bounded observable:

```text
v=(|16>+|8>+|24>)/sqrt3, Pv=|v><v|,
Jv=(J16+J8+J24)/sqrt3=4J0/sqrt3,
J0=gamma0 Γ[Σi<a(Bia-Bai)Ria],
Tr16Jv²/16=(8/3)Σi<a(Bia-Bai)².                     (P4)
```

Pv является projector, ортогональным complete blank label. Его first-exit
history event, с coefficient0 и обоими golden ports, определён как
`blank^j ⊗ Pv ⊗ I_later`. Разные j ортогональны, без reset или стирания.
Actual amplitude -2p² Mχ* A линейна по χ-output; поэтому P4 сохраняет
offdiagonal label coherences. Диагональная смесь трёх labels их теряет.

Для original faithful first shell kinetic weights coherent readout равны
(3,-1,-1,-1)/sqrt3; их mean square равен1. С actual clock coefficient
1/256 из прежнего owner principal contrast равен

```text
L_v-L_v(flat)=(1-exp(-beta/s²))/(96s²) <curl²>
            =-(1-exp(-beta/s²))/(192s⁴) I_EH_principal. (P5)
```

Равенство включает все три cone directions на principal quadratic order,
а не все10 metric rows, nonlinear EH, Newton constant или stationary
continuation. Metric/clock variation дифференцирует и coefficient P5.

В классе fixed PSD 3×3 label-coherence detectors это направление
единственно с точностью до неотрицательного множителя, если потребовать
нулевой quadratic response на всех longitudinal pair gauges. Действительно,
Bia=Bai даёт output vector (χ_i-χ_a)_χ, три таких vectors порождают
двумерную plane sum(vχ)=0. Нулевая quadratic form PSD W на каждом
vector требует Wv=0. Следовательно rangeW содержится в span(1,1,1),
то есть W=tPv, t≥0. Это математический consumer для detector selection,
не выведенный native selector и не classification всех128 outputs.

В частности коэффициент1/sqrt3 не становится native gate сам по себе.
Pv — явный observable в уже retained Hilbert space; его физическая
реализация/допуск и цена именно такого чтения должны быть предъявлены
в actual same-program interface. Никакой такой primitive здесь не добавлен.

Отдельная small noncommuting matrix проверка стыкует это с настоящими
final amplitudes обоих портов: K0,k=-2p² Mk* A, K1,k=-2ap Mk* A.
Контракция stacked amplitudes с Pv⊗I равна 4p² A*Mv Mv* A и отличается
от diagonal mixture. Это algebraic event identity, не новая аппаратная
реализация Pv и не повторный запуск прежнего32-label checker.

`check_principal.py` проверяет P1–P5 exact на pinned full16 creators,
включая все12 independent jets, hostile diagonalization control,
Fourier determinant и detector-plane spanning. Старые run() не вызваны.
