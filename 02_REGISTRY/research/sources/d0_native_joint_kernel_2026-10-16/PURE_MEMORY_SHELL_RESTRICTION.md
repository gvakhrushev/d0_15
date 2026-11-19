# Pure memory: exact shell restriction и оставшийся normal operator

16 октября 2026. Consumer для того же L8/full16/reference128 v8 action,
actual native `chi=(|mask1>+|mask15>)/sqrt(2)` и исходного heat root.
Новый [exact helper](pure_memory_shell_restriction_check.py) использует
только literal owned CAR definitions и SHA-прикреплённый уже опубликованный
interval result. Никакой старый checker или 4096-matrix assembly здесь
не запускается. Цель — normal kernel/inertia всех40806 field directions
из [rank-free amplitude reduction](RANK8_AMPLITUDE_FIBRE.md), не новая
классификация рангов источника.

**Доказанный результат этого файла.** В каждом nonzero shell-transfer
секторе pure-memory поправка на полном inactive-coframe `ker T` имеет
ранг не более двух на каждую inactive leg. Для `q=(0,1,7,0)` она равна
нулю тождественно; прежняя строгая инерция `6+/2-/0` переносится точно.
Для остальных пяти shell types поправка ненулевая при всех `a>b>0`.
Это последнее утверждение само по себе не определяет инерцию суммы.

## 1. Настоящее допустимое inactive-coframe подсемейство

Из [exact rank8 source proof](RANK8_SOURCE_SUBMERSION.md) для
`q=+/-2e_i` rankT=3, а для `q=+/-e_i+/-e_j`, `i!=j`, rankT=5.
После шести представлений весь `ker T` задаётся произвольными четырьмя
coframe components каждой inactive leg `r` с `q_r=0`: соответственно
12 или8 complex dimensions. Источник и остальные link directions
не замораживаются: это полное сечение ядра установленного source map.

Для вычисления Hessian на этом сечении выбираем реальное affine
подсемейство `u_r(x)=u_r+z a_r exp(iqx)+conj(z a_r exp(iqx))`,
identity links и observer `e0`. При `q_r=0` coframe leg не меняется
вдоль собственной ножки; literal own-leg transport удовлетворён точно,
не только в первом порядке. Поэтому `D_ij=0` в этих affine coordinates.
В stationary root это тот же ограниченный Hessian, что в любом
regular native chart. Вне stationary root мы используем эту явную
affine extension; не приравниваем разные coordinate Hessians.

Положим

```text
zeta_+ = 8(exp(i*pi/4)-1)=x+i y,    zeta_-=conj(zeta_+),
lambda1=|zeta_+|^2=64(2-sqrt(2)),
v_q=8 sum_j (exp(2*pi*i*q_j/8)-1)u_j,
E=C(v_q)+iota(conj(v_q)),   E^2=Lambda I16,
Lambda=|v_q|^2,
g_sigma=Lambda+2 Re[conj(zeta_sigma)(u_r dot v_q)],
h_sigma=Im[(v_q)_0 conj(zeta_sigma)].                 (S1)
```

`g_sigma=lambda_(sigma e_r+q)-epsilon` — исходный signed Q gap.
Ни абсолютное значение, ни усечение Q здесь не вводятся. На этих
конкретных inactive shell edges gaps строго положительны по формулам
ниже. Full Z, его производные, все16 grades и reference128 неизменны.

На занятом `k=sigma e_r` только соответствующая inactive leg имеет
ненулевой первый jet. Для real component vector a:

```text
J_a=C(zeta_sigma a)+iota(conj(zeta_sigma)a)=J_a^*,
D_(k+q)=D_k+E,
X_a=D_(k+q)J_a+J_a D_k=s_a I+E J_a,
s_a=2 lambda1(u_r dot a).                              (S2)
```

Разные inactive legs не пересекаются на занятом incoming momentum,
поэтому их memory corrections образуют независимые4x4 blocks.

## 2. Почему достаточно только actual two-point CAR

При pure chi occupation numbers равны `(1,1/2,1/2,1/2)`, anomalous
two-point functions равны нулю. Это проверяется непосредственно на
всех16 occupation masks actual ACDB creator. Для
`delta ell(A)=<chi,A chi>-Tr16(A)/16` получаем

```text
delta ell(E J_b)= i h_sigma b_0,
delta ell(J_a E)=-i h_sigma a_0,
delta ell(J_a J_b)=0.                                 (S3)
```

Сначала выполняется **operator identity**, до применения состояния:

```text
X_a^*X_b=s_a s_b I+s_a E J_b+s_b J_a E+Lambda J_a J_b. (S4)
```

Таким образом потенциальный degree-four term исчезает по `E^2=Lambda I`.
Нельзя подставлять one-particle approximation или объявлять chi Gaussian:
здесь это не требуется. Из (S3)–(S4)

```text
delta ell(X_a^*X_b)
 =2 i lambda1 h_sigma[(u_r dot a)b_0-(u_r dot b)a_0].   (S5)
```

Incoming Gram содержит обратный порядок индексов. Conjugation фаз
меняет знак h, transposition меняет знак квадратной скобки; incoming
вклад равен outgoing вкладу. С учётом shell mass `1/8` и знака Schur
получаем **оба вклада**, а не половину:

```text
H_chi-H_trace = direct_sum_(inactive r) Delta H_r,
Delta H_r = -i lambda1/2 (sum_(sigma=+,-) h_sigma/g_sigma)
                         (u_r e0^T-e0 u_r^T).          (S6)
```

Raw affine Y в обоих preparations равен
`lambda1/2 sum_r conj(a_r) dot b_r`: anticommutator J_a,J_b скалярен.
В этом подсемействе (S6) — вся поправка; price Hessian с полным global
normalizer сокращается в разности. Для theta/stabilizer directions
всего native chart такое утверждение неверно: их actual D2 curvature
сохраняется в [full-Y interface](PURE_MEMORY_FIELD_HESSIAN_INTERFACE.md).

Если `w_r=u_r-(u_r)_0 e0`, `U_r=[e0,w_r]` и
`gamma_r=lambda1/2 sum h_sigma/g_sigma`, то

```text
Delta H_r=U_r [[0,i gamma_r],[-i gamma_r,0]] U_r^*,
K_r=u_r e0^T-e0 u_r^T,
K_r^3=-|w_r|^2 K_r.                                  (S7)
```

Это точная rank<=2 factorization. При `gamma_r!=0,w_r!=0` ранг равен2,
а инерция **самой поправки** равна `(1,1,2)`; это не инерция H_chi.

## 3. Шесть типов и один закрытый перенос инерции

На прежнем heat background `U=F eta`, `F=(a-b)I+b11^T`,

```text
d=a^2+3b^2, o=2b(a+b), d-o=(a-b)^2>0,
tau_0=a, tau_1=tau_2=tau_3=b,
G=2 lambda1(d-o)+8 x^2 o>0.                            (S8)
```

Прямое сложение двух shell weights даёт:

```text
q=2e_i:
 g_+=128(d+o), g_-=128[(d-o)+(2-sqrt(2))o],
 sum h/g=-128 tau_i lambda1(d+2o)/(g_+ g_-).

q=e_i+e_j:
 g_+=2 lambda1(d+3o), g_-=G,
 sum h/g=2xy(tau_i+tau_j)/G.

q=e_i-e_j:
 g_+=g_-=G,
 sum h/g=2xy(tau_i-tau_j)/G.                           (S9)
```

Все denominators в (S9) положительны при `a>b>0`, а `xy<0`.
Значит первые пять строк таблицы имеют ненулевую поправку на каждой
inactive leg; последняя имеет нулевую поправку при всех таких a,b.
Это не проверка на одном rational fixture и не fitted source.

| Тип / representative q | Inactive legs | Complex dim | Число real Fourier frequencies | Real dim | Rank поправки / leg |
|---|---|---:|---:|---:|---:|
| time axis 2000 | 1,2,3 |12|2|24|2|
| spatial axis 0200 |0,2,3|12|6|72|2|
| same time-spatial 1100 |2,3|8|6|48|2|
| same spatial-spatial 0110 |0,3|8|6|48|2|
| opposite time-spatial 1700 |2,3|8|6|48|2|
| opposite spatial-spatial 0170 |0,3|8|6|48|0|

Для q0170 имеем точное равенство pure и trace restricted Hessians.
Прежний [interval result](OPPOSITE_SHELL_TRANSFER_RESULTS.json), SHA256
`ea994fef6edc38f4b01a98eed7379841f6a603dfbb02b641382bfa853f64db75`,
уже содержит full-trace restricted S4 congruence q1700 -> q0170 и
строгую `6+/2-/0` на всём owned root box radius1e-12.
Distance upper bound `9.46751770254899e-5<1`. Из текущего
[normal/-O receipt](OPPOSITE_SHELL_TRANSFER_VALIDATION.json) читаются
scientific equality и identities этого exact result и всех scientific
source files, уже закреплённых внутри immutable result. Whole validation
не hard-pinned: его prose-owner fingerprint может обновляться при
интеграции документа, не меняя scientific inputs. Result и scientific
source bytes проверяются, расчёт не повторяется.
Здесь S4 используется только внутри уже доказанной full-trace
restriction. Pure-memory S4 symmetry не утверждается.

Итак, шесть spatial-opposite frequencies дают real inertia `36+/12-/0`.
Вместе с прежними семью строго положительными q0 Gram directions
закрыты55 normal directions с инерцией `43+/12-/0`. Остальные40751
на этом шаге остаются отдельным consumer, без вывода из малого ранга.

При желании пять оставшихся shell restrictions можно проверять ещё
меньшими матрицами. Если `H0` — прежний invertible trace restriction,
`Delta=U C U^*`, m — число inactive legs, то `C` имеет inertia(m,m).
Для `Ksmall=C^{-1}+U^*H0^{-1}U`, размером6 или4,

```text
p(H_chi)=p(H0)+n(Ksmall)-m,
n(H_chi)=n(H0)+p(Ksmall)-m,
z(H_chi)=z(Ksmall).                                  (S10)
```

Это Sylvester congruence одного bordered matrix. Строгую инерцию
Ksmall ещё нужно доказать, если этот путь выбран; (S10) не заменяет её.

## 4. Допустимые симметрии и real counting

Time coordinate pure chi выделена. Spatial S3 сохраняет heat Gram и
конъюгирует admitted SO3 links в SO3. При нечётной spatial permutation
top component chi меняет знак, а mask1 component сохраняется.
CAR parity `(-1)^N` возвращает прежнюю chi с точностью до общего знака.
Parity коммутирует со всеми even operators, в частности Delta, X, Y,
source probes и Schur products; это точное восстановление состояния,
а не предположение о пространственной изотропии pure source.
Поэтому spatial S3 и global q->-q достаточно для сокращения проверок.
Time-spatial permutation из full-trace S4 на pure source не переносится.

`H_-q=conj(H_q)` по reality. Один nonselfconjugate complex block с
инерцией(p,n,z) даёт real +/-q pair с инерцией(2p,2n,2z).
Для selfconjugate q, все компоненты которых0/4, используется real
polarization и нет множителя2. Все15 nonzero selfconjugate frequencies
лежат вне Omega-Omega; spatial S3 разбивает их на семь типов.

Существующее полное native mean slice имеет complex dimension
`17-2s(q)`, s — число active legs. Чисто комбинаторно, без новой
4096-frequency census,

```text
sum_(q!=0) (17-2s(q))=40943,
nonzero shell raw quotient =8*15+24*13=432,
outside Omega-Omega =40943-432=40511 real directions,
shell kerT quotient =8*12+24*8=288 real directions,
V8 dimension =40511+288+7=40806.                       (S11)
```

Числа в (S11) уже учитывают real Fourier pairing. Перенос инерции
trace Hessian на весь V8 из одного лишь совпадения `ker T` запрещён:
(S6) даёт явную ненулевую поправку, а full chart также имеет D2 curvature.

## 5. Named consumer: normal inverse и full-amplitude inertia

Пусть новый строгий consumer устанавливает на всём V8 real inertia
`(p,n,z)`, `p+n+z=40806`. Rank151 regular amplitude source map и
точная57195-dimensional flat amplitude family берутся из
[rank-free proof](RANK8_AMPLITUDE_FIBRE.md). Congruence с151 source
hyperbolic pairs даёт raw shell-amplitude/field inertia

```text
(p+151, n+151, 57195+z),  total dimension98303.         (S12)
```

Из [amplitude consumer](AMPLITUDE_INERTIA_CONSUMER.md) unchanged Q block
имеет real inertia `(16740352,4096,0)`: все below/above-shell signs
проверены прежними scalar enclosures. Это не предположение, что
resolvent положителен. На исходной normalized full-amplitude domain

```text
(p+16740503, n+4247, 57195+z),
total dimension16842751.                              (S13)
```

Reference, rank-birth и source-fibre zeros уже входят в57195; повторно
добавлять16384 reference zeros нельзя. Если z=0, normal IFT/Morse--Bott
из rank-free proof исключает дополнительные близкие critical branches
около pure seed, кроме точно построенной flat family. Если z>0,
существование новых nonlinear branches из этого не следует.

Этот consumer сохраняет исходные g_tau, matter, reference, stored
transport и action. Physical preparation/admission, continuum limit,
новая микроскопическая word law или вывод ОТО здесь не доказаны.
