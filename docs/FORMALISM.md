# Formalism — structure, arrow, consequence

This repository is deliberately about **roles under transformations**, not three boxes that must literally exist as separate biological variables.

The v0 mechanism keeps four matrices during learning:

\[
M_t=(S_t,A_t,E_t,C_t).
\]

`E` is temporary eligibility. The frozen executable object contains `S`, `A`, and `C`.

## 1. Structure: the reversal-even part

For every observed transition `i -> j`, v0 writes reciprocal support:

\[
S_{ij}\leftarrow S_{ij}+1,\qquad
S_{ji}\leftarrow S_{ji}+1.
\]

Therefore

\[
S^T=S.
\]

If a trajectory is reversed, its undirected edge usage is unchanged:

\[
S(Rh)=S(h),
\]

where `R` reverses the history.

In v0, `S` has a more fundamental role than being another number in a score: it defines the **legal neighborhood**. An edge absent from `S` cannot be traversed by any ablation. This is why the label `A+C` in the receipt does **not** mean a system with no structure. It means the executor omits the *support magnitude* from its score while still respecting the frozen topology.

That distinction matters. Structure can be a constraint before it is a preference.

## 2. Arrow: the reversal-odd part

The same observed transition writes signed flux:

\[
A_{ij}\leftarrow A_{ij}+1,\qquad
A_{ji}\leftarrow A_{ji}-1,
\]

so

\[
A^T=-A.
\]

Under exact trajectory reversal,

\[
A(Rh)=-A(h).
\]

That is the narrow meaning of **arrow** here: the part of recorded temporal experience that changes sign under reversal. It is not a claim that every directed behavior in a learned system must live in an antisymmetric matrix.

Gate S makes this explicit. The forward history `0 -> 1 -> 2` and reverse history `2 -> 1 -> 0` produce identical `S`. `S` alone is tied at the middle state, while `S+A` recovers the experienced direction exactly.

## 3. Eligibility: what might deserve delayed credit

Each transition also updates a symmetric eligibility trace:

\[
E_{t+1}=\rho E_t + B(i,j),
\]

where `B(i,j)` marks the undirected traversed edge and v0 fixes

\[
\rho=0.8.
\]

At the start of every training episode v0 clears `E`. This is a deliberate scope boundary: the experiment tests delayed assignment **within one route episode**, not interference between eligibility traces from different episodes.

Because consequence arrives only at the terminal, earlier edges have smaller eligibility than later edges. That fact produces a useful caveat discussed below: even a symmetric consequence field can have a spatial gradient.

## 4. Consequence: outcome reassignment changes this, not S or A

At the end of an episode,

\[
C\leftarrow C + \eta r E,
\qquad \eta=1.
\]

`C` remains symmetric because `E` is symmetric.

The matched Gate A transformation is not time reversal. It is **reward reassignment**. The exact same balanced A/B transition histories are replayed, but the identity of the rewarded arm is swapped.

Under that transformation v0 requires

\[
S'=S,\qquad A'=A,\qquad C'\ne C.
\]

The frozen receipt gets zero numerical difference in `S` and `A` under reward reassignment, while the consequence matrices separate strongly.

A second control permutes the delayed outcomes in time while keeping the transition histories fixed. Correct outcome assignment gives fork accuracy `1.0`; shuffled assignment gives `0.46875` over 32 deterministic seeds.

## 5. The effective operator is routed, not S+A+C

The executable object is better written as

\[
O_t=\mathcal R(S,A,C,q_t,h_t)
\]

than as the literal matrix sum `S+A+C`.

In v0 there is no learned query `q_t` or resident state `h_t`; the minimal executor does this:

1. use `S` to define legal neighbors;
2. score legal neighbors using whichever declared components are enabled;
3. return no choice on an exact tie rather than smuggling in a deterministic preference.

A tie is scored as `0.5` in the matched binary probes: ignorance is treated as chance, not as a hidden left/right convention.

## 6. Why a symmetric C can still create directed behavior

This is an important correction to any too-neat reading of the slogan.

`C` is symmetric, yet the eligibility trace is larger near the terminal than near the start. On the rewarded arm, consequence therefore forms a monotonic edge gradient. A local chooser can follow that gradient toward reward even though `C_ij=C_ji`.

So:

> **antisymmetry is one clean carrier of temporal traversal direction, but it is not the only way an agent can behave directionally.**

A scalar or symmetric value landscape can induce an oriented policy when the agent compares neighboring values.

That is why Gate SAC tests direction on **both** arms. `S+C` follows the rewarded arm forward but points backward on the punished arm, producing interior direction accuracy `0.5`. `S+A+C` preserves forward temporal direction on both arms and gets `1.0`.

This distinction is useful beyond this toy. It separates at least two different senses of "arrow":

- **historical flux** — which way events actually tended to occur (`A`);
- **policy gradient** — which way a value field tells a chooser to move (`C` plus local comparison).

Conflating them would make the decomposition look cleaner than it is.

## 7. The three v0 transformations

The cleanest description of the experiment is as three transformation tests.

| transformation | S | A | C | question |
|---|---|---|---|---|
| reverse the same trajectory | invariant | sign flips | not used | did we preserve temporal order? |
| reassign delayed outcome | invariant | invariant | changes | did value leak into history statistics? |
| shuffle outcome times | invariant | invariant | loses task alignment | does consequence need the right eligible event? |

This is the mathematical core of the repository.

## 8. Frozen receipt

The committed `results/v0.json` reports:

- Gate S: structure reversal error `0.0`; arrow sign-flip error `0.0`; `S` direction accuracy `0.5`; `S+A` `1.0`.
- Gate A: reward reassignment changes neither `S` nor `A` (`0.0` max error); full fork accuracy `1.0`; `S+A` fork accuracy `0.5`; shuffled consequence `0.46875`.
- Gate SAC: full held-out accuracy `1.0`; `S+C` interior direction `0.5`; no illegal edge choices; frozen matrices do not change during probing.

Ablations are intentionally all reported. In particular, `A+C` numerically matches `S+A+C` in this matched world because every used edge has equal support and `S` is already enforced as a hard topology mask. v0 therefore demonstrates the **topological role** of `S`, not a benefit from adding support magnitude to the score.

## 9. What v0 has not solved

The experiment does not solve general credit assignment. Eligibility is deliberately simple, episode-local, and structurally aligned with the route. FunctionalArbors already showed how much harder the free case is: getting consequence back to a region is easier than knowing which structural change actually caused the improvement.

The experiment also does not prove that `(S,A,C)` is a unique decomposition. A richer mechanism may move information between coordinates, and different bases can make the same executable behavior look very different.

The claim earned here is smaller:

> **There exists a minimal executable setting in which reciprocal availability, reversal-odd temporal history, and delayed outcome assignment can be separated by matched transformations and recombined into a frozen mechanism.**
