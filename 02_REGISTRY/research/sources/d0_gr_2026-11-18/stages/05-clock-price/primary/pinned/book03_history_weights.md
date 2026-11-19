
### 03.3.0 Why an action exists at all: the statistical sum over histories

D0 does not postulate a Lagrangian `\mathcal L` and integrate `e^{i\int\mathcal L}`. It asks the prior question — *how do you score the statistics of all admissible histories at finite resolution without an external choice rule?* — and the action falls out as the answer. The carrier is the CORE statistical sum over histories [^b03-13]:

```math
Z_D(k):=\sum_{\gamma\in\Gamma_D(k)} w(\gamma)\,[q(\gamma)],
```

with `\Gamma_D(k)` the admissible histories at refinement level `k`, `w(\gamma)` the history weight, and `[q(\gamma)]` the memory class (topological charge/phase) in the role algebra `\mathcal A`.

**The weight is forced to be `w=\varphi^{-S}` — exponential, base `\varphi`** [^b03-14]. The form is not a postulate; three constraints close it with no freedom:

1. **Multiplicativity.** The probability of a composite history `A\to B\to C` of independent steps must factor: `w(A\to C)=w(A\to B)\,w(B\to C)`.
2. **Additivity of cost.** Code length of a composite history adds: `S_{total}=S_1+S_2`.
3. **Unique sum-to-product map.** The only function carrying a sum to a product is the exponential, `w(S)=b^{-S}`. A non-exponential weight would need an external table reconciling addition with multiplication — an exogenous catalog, ⊥M1 (DEF-0.2.2).
4. **Unique base.** The only scale number available in CORE is `\varphi` (the `p+p^2=1` fixed point, owned by BOOK_01 §01.6), so `b=\varphi`.

Hence `w(\gamma)=\varphi^{-S(\gamma)}`. The BRIDGE packaging `\varphi^{-S}=e^{-S\ln\varphi}` recovers the Boltzmann/Gibbs form, and the analytic continuation `S\to iS` recovers the quantum amplitude. Status: CORE-FORCING [^b03-15].

**Locality is a theorem, not an assumption** [^b03-16]. If a scene splits into two parts with no path between them, then `Z_{total}=Z_1\cdot Z_2`. This cluster decomposition is guaranteed by the structure of the algebra `\mathcal A` and is exactly the statement that "physics here" does not depend on "physics in another galaxy". Status: CORE-FORCING [^b03-17].

### 03.3.0a Action is assembly cost, not an imported functional

With the weight fixed, the action `S(\gamma)` of a history is forced to be its net assembly cost — resolution friction minus distinguishability gain [^b03-18]:

```math
S(\gamma):=\sum_{e\in\gamma}\operatorname{Cost}(e)\;-\;\sum_{v\in\gamma}\operatorname{Info}(v).
```

The edge sum `\sum_e\operatorname{Cost}(e)` is the resolution (UV-cutoff `\kappa`) price of traversing edges — the "friction" of the medium. The vertex sum `\sum_v\operatorname{Info}(v)` is the distinguishability gain: at each branch the history commits a choice (a bit), lowering uncertainty entropy. There is no place to insert an imported continuum Lagrangian density: the action is read off the graph history.

**No coupling constant may be multiplied in front** [^b03-19]. Standard QFT writes `\tfrac{1}{g^2}\int\dots`. In CORE this prefactor is forbidden: any `\lambda\notin\{1,\varphi^n\}` is an external Catalog of interaction strength, ⊥M1. Interaction strength must be *derived* from graph topology — as `\alpha^{-1}` is derived from the 359-channel scene count downstream — never inserted as a multiplier into the action. Status: CORE-FORCING [^b03-20].

**Least action `\delta S=0` is the Minimum Description Length tautology** [^b03-21]. Because the most probable history is the cheapest to encode in `\Sigma`, stationarity of `S` is not an additional physical postulate layered on the weight `\varphi^{-S}`; it is the same statement read at the classical limit. "Most probable" = "shortest code" = `\delta S=0` (MDL). Status: CORE-FORCING [^b03-22].

**A Feynman diagram is an equivalence class of histories, not a drawn line** [^b03-23]. A diagram is `[\gamma]_\sim` — the class of all histories sharing one topology (loop count, branch vertices, external legs). A loop is literally a closed memory cycle `P` (the light-cycle of the spectrum book); loops therefore *create* mass and charge here rather than merely correcting them, and the standard QFT divergences are the artifact of treating finite-size cycles as points (structural limit `\kappa_k`). Status: CORE-FORCING [^b03-24].
