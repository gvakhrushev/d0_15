# Полная constrained amplitude inertia из точной Q-конгруэнции

16 октября 2026. Аналитический consumer того же faithful L8/reference128
v8 root; исходный action, Delta и normalization не меняются. Intake на
checkout `190eec3d50e5af92f5fe193dc3cf7382778b3747` использует сохранённые
результаты complete field inverse и
[LOCAL_CRITICAL_LOCUS_CONSUMER.md](LOCAL_CRITICAL_LOCUS_CONSUMER.md).
Большая full-amplitude matrix не строится и не диагонализуется.

## 1. Результат и точная область счёта

Для исходных65536 real field coordinates и normalized complex
`Psi:H_ref128 -> H_workspace65536` полный **constrained** Hessian на
касательной к `||Psi||_HS=1` имеет real inertia

```text
positive =16,779,967,
negative =     5,589,
zero     =    57,195,
total    =16,842,751.                              (A1)
```

Здесь сохранены все exterior grades, все128 reference columns и все
Q-amplitude variations, включая отрицательный mass sector. Это Hessian
на normalized domain; отдельная epsilon multiplier row и вещественная
radial amplitude direction в (A1) не добавляются. Reference unitaries,
включая общий phase, **входят** в zero count. Отдельно хранимые affine
shifts остаются вне этой области.

Входная complete reduced density/field inertia равна
`(39615 positive,1493 negative,40811 zero)`. Это прочитано из
`FIELD_INVERSE_RESULTS.json`, где все483 field-only representatives
строго проверены, а validation фиксирует byte-identical normal/optimized
scientific JSON. Здесь этот расчёт не запускается повторно.

## 2. Нормированные amplitude coordinates и reference zeros

Работаем в полном whitened Hilbert space владельца. Полное observer
whitening — гладкая замена координат paired Hilbert bundle, поэтому
constrained inertia исходной задачи сохраняется; его field derivatives
не удаляются из mixed blocks. Пусть P — occupied rank128 projector,
Q=I−P. Около исходной full-rank preparation P Psi обратима на reference.
Единственные локальные normalized coordinates имеют вид

```text
Psi=[sqrt(1−||Y||_HS^2) sqrt(sigma)+Y] V,
sigma>0 on P, Tr_P sigma=1,
QY=Y,  Y:P H -> Q H,  V:H_ref -> P H unitary.       (A2)
```

Это polar decomposition P Psi: V — его unitary factor, sigma — его
положительная density, нормированная собственной trace, а
`Y=Q Psi V*`. Поэтому (A2) не замораживает никаких matrix components.
Точная цена не зависит от правого V. U(128) имеет16384 real dimensions,
действует свободно при полном column rank и даёт16384 zero directions,
отдельных от reduced density/field kernel40811.

Нормировка в (A2) включена до дифференцирования. В исходном root Y=0,
`Delta_* P=epsilon_* P`, `Q Delta_* P=0`, так что чистый Q-блок
второго дифференциала равен

```text
d^2 S[dot Y,dot Y]
   =2 Tr(dot Y* (Delta_Q−epsilon_*) dot Y),
H_Q=2(Delta_Q−epsilon_*) tensor I_ref128.           (A3)
```

В (A3) dot Y — именно raw Q-amplitude tangent в HS norm. Для graph
coordinates `QJ` появляется дополнительная положительная congruence
через `sqrt(sigma_*)`; это не изменение mass eigenvalues в выбранной
raw-amplitude норме и не дополнительный множитель128 в (A3).

## 3. Исключённая Q-форма точно даёт Phi

Из exact Schur reduction владельца берём E,J,G и тождество
`dE=J* dDelta J−d epsilon G`. Для фиксированных x,sigma уравнение
`Tr sigma E(x,epsilon)=0` определяет epsilon_hat, поскольку его
epsilon derivative есть `−Tr sigma G<0`. Обозначим
`N_sigma=Tr sigma G`. Тогда

```text
Psi_hat=J sqrt(sigma/N_sigma) V,
Y_hat=QJ sqrt(sigma/N_sigma),
Phi(x,sigma)=F_price(Delta(x))+epsilon_hat(x,sigma). (A4)
```

Действительно, `PJ=P`, `G=P+J*QJ`, поэтому
`1−||Y_hat||_HS^2=1/N_sigma`; (A4) принадлежит ровно карте (A2).
Имеем `Q(Delta−epsilon_hat)Psi_hat=0`, а P-residual равен
`E sqrt(sigma/N_sigma) V`. При вариации Y с фиксированными sigma,V
P-компонента dot Psi пропорциональна sqrt(sigma)V, и её contraction с
этим residual равна нулю из `Tr sigma E=0`. Значит Y_hat — настоящий
critical point по **всем** normalized Q-amplitude coordinates.

Q-блок (A3) обратим. Обычный IFT потому делает Y_hat единственным
близким Q-critical solution при фиксированных x,sigma,V. Его значение
действия точно равно Phi: `Tr Psi_hat* Delta Psi_hat=epsilon_hat`,
поскольку normalization равна1 и `Tr sigma E=0`. Следовательно
Schur complement полного constrained Hessian по Q равен

```text
Hess Phi  direct_sum  0_(dim U128).                (A5)
```

В частности, (A5) содержит все field/Q mixed terms, движущийся G,
полный global Z response и исходную second jet карту. Они не
отбрасываются при сложении inertias. Для symmetric block matrix
`[[A,B],[B^T,C]]`, A=H_Q, точная triangular congruence даёт
`A direct_sum (C−B^T A^{-1}B)`. По Sylvester

```text
Inertia(H_full_constrained)
 =Inertia(H_Q)+Inertia(Hess Phi)+(0,0,16384).       (A6)
```

Речь об indefinite stationary elimination, не о minimization по Y.
Существование отрицательного Q mass этому доказательству не мешает.

## 4. Интервальный intake знаков Q mass

Выполнен один маленький read-only scalar intake: загружена только
`full_symbol_interval_weights.spectral_intervals(repo)`. Ни её `run()`,
ни old checks, ни full matrices не вызывались. Immutable owner SHA256:

```text
0d8651dae3b6b7ba2049a1c71ac47895e536f9ccc5f85bf9978c133c75ccfc18
```

Его119 exact feature groups покрывают все4096 momenta. Для каждого
не-shell feature знак строго отделённого resolvent interval совпадает
со знаком `lambda−epsilon_*`. Его знаменатель вычислен с exact feature
subtraction до interval arithmetic. Поэтому отрицательные mass modes
не предполагаются заранее. На **всём** исходном d/o rectangle radius
`1e-12` существенные поля фактического JSON stdout intake равны:

```json
{
  "below_modes": 1,
  "shell_modes": 8,
  "above_modes": 4087,
  "below_features": [[[0,0],[0,0]]],
  "minimum_absolute_Q_gap_lower": "2.1727398353670858171131866782514588191052668743172128475971637398695",
  "H_Q_inverse_norm_upper": "0.23012419244180915603270387320526416160869314329422386281607996217203",
  "Q_positive_real": 16740352,
  "Q_negative_real": 4096
}
```

Нижняя gap-граница и верхняя inverse-граница экспортированы из точных
binary interval endpoints с направленным decimal rounding. В частности
`||H_Q^{-1}||op <0.230124192441809157 <4` в raw-amplitude HS norm.
Это существенно сильнее необходимой для IFT обратимости. Отрицателен
ровно ground mode: это результат подсчёта всех119 groups, а не
предпосылка, выводимая только из одного известного negative resolvent.

Каждый momentum имеет16 workspace components,128 reference columns и
две real coordinates на complex amplitude. Таким образом

```text
dim_R Qamp =2*(65536−128)*128 =16,744,448,
positive_Q =2*4087*16*128      =16,740,352,
negative_Q =2*1*16*128         =     4,096.         (A7)
```

В thermal/feedback данных owner сохранены ground contribution и
`Z in [49.33703024859027025358...,49.33703025259505430705...]`.
В matter mass используется исходный Delta, не log heat generator.

## 5. Сложение и проверка размеров

Из (A6)–(A7)

```text
positive =16,740,352+39,615 =16,779,967,
negative =     4,096+ 1,493 =     5,589,
zero     =    40,811+16,384 =    57,195.

normalized original domain:
65536+[2*65536*128−1] =16,842,751,

same domain in Schur/polar coordinates:
81919+16384+16744448  =16,842,751.                 (A8)
```

Нулевое пространство совпадает с tangent полной normalized-amplitude
critical family:40811 reduced directions и16384 reference unitaries.
Это совместимо с exact local Morse–Bott reconstruction; Q-block новых
zero directions не добавляет. Для bordered multiplier convention к
(A1) добавилась бы одна positive и одна negative direction; это другая
матрица, не Hessian на normalized tangent, который указан здесь.

## 6. Intake provenance и границы

Потреблённые неизменённые source/result bytes:

| Файл | SHA256 |
| --- | --- |
| `FIELD_INVERSE_RESULTS.json` | `f35590e4d1e15cfd597b6458398d9d68b0c1bd035fa8f6697edde6cb4c573604` |
| `FIELD_INVERSE_VALIDATION.json` | `370fc120176d59b0255c094bba08bb1915266202af45ef0ccb4fcfa35da0b663` |
| `LOCAL_CRITICAL_LOCUS_CONSUMER.md` | `80b399ebbc49c5b82045f57b152e64d6fb858fa883955d93e1476ccfee51b0b5` |
| `full_symbol_interval_weights.py` | `0d8651dae3b6b7ba2049a1c71ac47895e536f9ccc5f85bf9978c133c75ccfc18` |
| `../d0_native_field_transport_2026-10-16/stored_rotational_wave.py` | `2b12f26d814a57cc99084e904deeac69a8f64a8d9a0eb9ee765e8104ef50bc37` |
| `../d0_record_generated_heat_v8_2026-10-14/receipt.json` | `da44c7393b1164ce4babcab2ea13707958364d273d2c3fa1d86d514a9ac83ae9` |

Эта таблица фиксирует именно прочитанный Git snapshot190eec3d, а не
требует равенства текущим расширенным документам. Последующее изменение
только integer composition inverse-bound и annotations локального
consumer не меняет ни483 interval orbit records, ни inertia (40)/(A1).
Полный текущий input manifest находится в FIELD_INVERSE_VALIDATION.json.

Эквивалентное воспроизводимое scalar-intake тело команды из корня
репозитория, печатающее только counts и две границы:

```python
import hashlib, importlib.util
from pathlib import Path
p = Path('02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/full_symbol_interval_weights.py')
expected = '0d8651dae3b6b7ba2049a1c71ac47895e536f9ccc5f85bf9978c133c75ccfc18'
if hashlib.sha256(p.read_bytes()).hexdigest() != expected:
    raise ArithmeticError('scalar owner pin')
spec = importlib.util.spec_from_file_location('amplitude_scalar_owner', p)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)
a = w.spectral_intervals(Path.cwd())
counts = {'below': 0, 'shell': 0, 'above': 0}
for f, row in a['feature_data'].items():
    if f == a['shell_feature']:
        counts['shell'] += row['count']
    else:
        lo, hi = w.bounds(row['resolvent'])
        if hi < 0:
            counts['below'] += row['count']
        elif lo > 0:
            counts['above'] += row['count']
        else:
            raise ArithmeticError('unclassified Q feature')
if sum(counts.values()) != 4096 or counts['shell'] != 8:
    raise ArithmeticError('incomplete mode count')
print(counts)
gap = a['minimum_complement_shell_gap_lower']
print(w._decimal(gap, w.ROUND_FLOOR))
print(w._decimal(1/(2*gap), w.ROUND_CEILING))
```

Это finite L8 full-rank constrained-v8 inertia и точная local critical
reconstruction. Она не является refinement-uniform inverse, оценкой
всего physical action, primitive/preparation admission или выводом ОТО.
Rank8 boundary, иной reference/carrier, affine shifts, исходный g_tau и
fixed-source h^{-2} raw,l1 terminal остаются в прежней области владельцев.
Ни source, ни ожидаемые scientific outputs для этого intake не менялись.
