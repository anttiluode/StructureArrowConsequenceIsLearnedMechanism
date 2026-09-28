# Structure → Arrow → Consequence → Learned Mechanism

Design date: 2026-09-28

## Purpose

This repository asks whether a recurring pattern across the Antti Luode repo lineage can be made precise enough to survive falsification:

> A learned mechanism may require three distinct things: **structure** that makes interactions possible, an **arrow** that breaks temporal reversibility, and **consequence** that selects which directed histories persist.

The goal is not to declare a universal theory of brains, transformers, evolution, or learning. The goal is to define the smallest executable object that separates these roles, test the decomposition against matched controls, and use the older repositories as evidence and counterevidence rather than as decoration.

The repository must preserve the distinction between:

- **source-derived results** already earned in older experiments;
- **cross-repo synthesis** proposed here;
- **new v0 results** produced by this repository;
- **speculative implications** that remain explicitly unproven.

A negative v0 is a valid result.

---

## Central object

The working state is

\[
M_t=(S_t,A_t,C_t,E_t).
\]

These are not assumed to be literal biological modules.

### Structure: `S`

`S` describes reciprocal support, availability, or adjacency: which interactions/routes exist at all.

The minimal constraint is

\[
S_t^\top=S_t.
\]

`S` survives trajectory reversal. If the same undirected route is traversed in the opposite order, the reciprocal support may remain unchanged.

Interpretation examples:

- anatomical connectivity;
- a sparse graph skeleton;
- co-availability of states;
- persistent substrate on which later routing can occur.

### Arrow: `A`

`A` describes directed temporal flux/order: which way experience or activity tends to pass through available structure.

The minimal constraint is

\[
A_t^\top=-A_t.
\]

`A` changes sign under reversal. It is the part that an undirected graph Laplacian discards.

Interpretation examples:

- ordered transition bias;
- asymmetric recurrent connectivity;
- lagged skew covariance;
- phase/order relationships that distinguish `i -> j` from `j -> i`.

### Eligibility: `E`

`E` is short-lived causal candidacy: a local record of what recently participated and therefore might deserve delayed credit or blame.

A generic update is

\[
E_{t+1}=\rho E_t+\psi(x_t,x_{t+1},M_t), \qquad 0<\rho<1.
\]

`E` is deliberately separate from consequence. Recent participation is not yet proof of usefulness.

### Consequence: `C`

`C` is the slower state produced when delayed outcome is assigned through eligibility.

A generic update is

\[
C_{t+1}=\lambda C_t+\eta\,r_{t+\Delta}E_t,
\]

with controls that shuffle or erase the relationship between `r` and the eligible event.

`C` is not synonymous with scalar reward. It is the persistent trace of which locally available/directed events later proved useful or harmful under the declared task.

---

## Effective operator

The repository must not define the learned mechanism as the literal arithmetic sum `S + A + C`.

Instead, the effective operation is a routed computation

\[
O_t = \mathcal{R}(S_t,A_t,C_t,q_t,h_t),
\]

where:

- `q_t` is the current query/probe/goal;
- `h_t` is any declared fast resident state;
- `S` determines what transitions are available;
- `A` biases their direction/order;
- `C` changes which available directed transitions are selected, stabilized, or suppressed.

The frozen mechanism must be executable without replaying the training history.

This is the key boundary inherited from the older corpus: a structure that looks meaningful is not yet an algorithm. The frozen learned object must itself perform the held-out task.

---

## v0 experiment

The v0 should be a small synthetic environment, cheap enough to run on CPU in seconds to a few minutes, with no neural-network training dependency.

It contains a compact state graph with at least one ambiguity that cannot be solved from undirected structure alone and at least one delayed consequence that cannot be solved from direction alone.

A candidate concrete world is a two-choice route system with matched geometry:

```text
        u1 -> u2 -> goal A
start <
        v1 -> v2 -> goal B
```

The graph is constructed so that:

1. both arms have matched reciprocal structure;
2. experience can traverse the same edges in opposite directions;
3. delayed reward can prefer one arm without changing its geometry;
4. the final probe can require selecting a route under a fresh start/query.

The implementation may use a slightly richer graph if needed to make the controls non-degenerate, but every added state must have a declared purpose.

---

## Gates

### Gate S — structure is not direction

Train/observe matched trajectories with identical undirected edge usage but opposite temporal order.

Example pair:

```text
A -> B -> C
C -> B -> A
```

Requirements:

- `S` must be matched between the two histories within numerical tolerance;
- an `S`-only decoder/executor must not distinguish the two conditions above chance;
- `A` must reverse sign under the matched reversal;
- an `S+A` mechanism must recover the declared direction on held-out probes.

Failure interpretation:

- if `S` alone solves the task, the task is not isolating direction;
- if `A` does not reverse under trajectory reversal, the arrow construction is invalid;
- if `S+A` cannot execute direction, skew statistics are descriptive but not operational.

### Gate A — direction is not value

Hold the directed experience fixed while changing which route receives delayed consequence.

Requirements:

- `S` and `A` remain matched across reward assignments;
- an `S+A` executor cannot know which route should persist/be selected;
- `C` differs when reward assignment differs;
- shuffled consequence destroys the effect;
- an `S+A+C` mechanism selects the rewarded route on a fresh probe.

Failure interpretation:

- if `A` alone predicts the rewarded route, the task leaks value into direction;
- if shuffled consequence performs equally well, `C` is not carrying causal assignment;
- if consequence changes behavior only during training but leaves no frozen usable mechanism, the persistence claim fails.

### Gate SAC — the frozen mechanism executes

Train only from local transitions plus delayed outcome. Freeze `S`, `A`, and `C`. Remove training-time reward/teacher signals. Present fresh starts/queries.

Predeclared baselines:

- `S only`;
- `A only` where mathematically meaningful;
- `C only` where mathematically meaningful;
- `S+A`;
- `S+C`;
- `A+C`;
- full `S+A+C`;
- full model with consequence shuffled in time;
- optional direct transition-count baseline if it is not algebraically identical to one of the above.

The full model earns support only if it beats the matched ablations for the intended reason and continues to do so after freezing.

The gate should report behavioral success and direct diagnostics of the internal decomposition. A high task score without the claimed internal separations is not a pass.

---

## Metrics

Minimum committed receipt:

- structural match under reversal;
- skew sign flip under reversal;
- route/action accuracy for Gate S;
- `S`/`A` invariance across reward reassignment;
- `C` separation across reward reassignment;
- consequence-shuffle control;
- frozen held-out execution accuracy;
- ablation table;
- seed count and confidence/dispersion summary;
- exact parameter/config hash or committed config block.

The v0 should prefer transparent effect sizes and paired differences over elaborate significance machinery. If inferential statistics are used, the test and seed count must be declared before the final receipt.

---

## Lineage: what older repositories actually contribute

This repository must include a separate `docs/LINEAGE.md` after implementation. It should distinguish inherited evidence from present inference.

### GeometricNeuron / GeometricNeuronAndSapolskysFractal

Inherited point:

- reciprocal structure and directed skew are not the same object;
- a small systematic local asymmetry can be magnified through repeated growth into a coherent global arrow.

Use here:

- motivates the `S` / `A` split;
- warns against reading direction out of passive geometry alone.

Do not claim:

- that the fractal demo proves biological development uses this decomposition;
- that the growth pattern is a mathematical fractal scaling result;
- that chirality itself is learning.

### Rytmi / TATWATASW

Inherited point:

- within-cycle temporal order is causal in the model;
- phase-shuffling can preserve activity while destroying replay order;
- asymmetric temporal fields plus rhythmic inhibition and STDP can write directional sequence structure.

Use here:

- motivates treating arrow/order as its own computational variable rather than as generic activation strength.

### FunctionalArbors

Inherited point:

- free structural variation can become task-useful when local eligibility is paired with later soma consequence;
- later versions show that transporting reward is easier than assigning it correctly;
- even exact recent structural-event tags can be too coarse for causal credit.

Use here:

- motivates explicit separation of `E` from `C`;
- prevents the repo from pretending that any delayed reward automatically solves structural credit assignment.

### FlyBench clicker neuron

Inherited point:

- local temporal filters plus an eligibility trace and sparse delayed teacher clicks can visibly change which substrate elements survive/grow;
- same later test can read different learned substrate after different click histories;
- the system does not beat a globally optimized fixed resonator bank on raw accuracy, so the claim is about local online credit/readable structure rather than SOTA prediction.

Use here:

- concrete example of consequence selecting among already directed/active local components.

### DevelopmentalSpectralNeuron

Inherited point:

- local resonator/resource/stigmergic growth did **not** make alternating versus blocked temporal developmental order reliably readable from final anatomy;
- seed variation exceeded history effect in the frozen v0;
- low modes did not beat geometry-matched nulls;
- earlier positive result was invalidated by implementation bugs.

Use here:

- negative control for the tempting claim that history automatically becomes useful structure;
- motivates asking what signed/credited variable survives development.

### OperatorTime

Inherited point:

- fixed substrate parameters can still produce different effective operators when resident history differs;
- history order can matter even when the current probe and event multiset are matched.

Use here:

- motivates defining the learned object by the operation available now, not only by stored state.

### ResonantCortex2

Inherited point:

- successful/search trajectories can contain compressible local structure while autonomous compiled execution still fails;
- composition/routing is a harder boundary than local fit.

Use here:

- requires Gate SAC to test the frozen executable mechanism rather than celebrate a graph, mode bank, or compression score.

### NeuralAlgorithmDecoding

Inherited point:

- a distributed learned process can sometimes be reduced to a smaller faithful executable causal abstraction under explicit intervention families;
- identifiability must be allowed to fail.

Use here:

- motivates the inverse question: after SAC learns a mechanism, can an outside observer recover the compact `(S,A,C)` causal abstraction?

This inverse decoder is **not** required for v0. It is a natural v1 only if v0 earns the forward mechanism.

---

## Deeper hypothesis, explicitly not a v0 claim

The most interesting cross-repo inference is that learning may sometimes be described as **history progressively breaking symmetries in a persistent substrate**.

One possible hierarchy is:

1. **Structure:** some interactions become possible at all.
2. **Arrow:** repeated temporal order breaks reversal symmetry.
3. **Consequence:** delayed outcomes break equivalence among directed histories by stabilizing some and suppressing others.
4. **Operator:** the future system now has a different set of actions/transformations available.

This can be written schematically as

\[
\text{experience}
\to
\text{available structure}
\to
\text{directed history}
\to
\text{credited persistence}
\to
\text{effective operator}.
\]

The repo may discuss evolution, development, synaptic learning, resident state, cultural transmission, and machine learning as possible nested timescales of this broad pattern, but must label that as analogy/hypothesis unless directly tested.

The phrase "symmetry breaking" must remain mathematically tied to an explicit transformation whenever used:

- reversal invariance for `S`;
- sign reversal for `A`;
- reward reassignment / outcome permutation for `C`.

Do not use it as a poetic synonym for "things changed."

---

## Transformer connection

The repository may make a limited computational analogy:

- transformer attention is a query-conditioned directed routing operator available transiently at inference;
- learned parameters are slower substrate;
- KV/resident context changes future routing without changing the original projection matrices;
- training consequences alter the slower substrate across episodes.

This does **not** imply that transformer attention maps directly to biological `A`, that gradient descent is the same mechanism as local delayed credit, or that brains are transformers.

A future experiment could ask whether a persistent sparse `(S,A,C)` memory can complement a frozen transformer by retaining causal route structure across episodes. That is out of v0 scope.

---

## Repository shape after implementation

```text
README.md
experiment.py
sac/
  world.py
  mechanism.py
  metrics.py
  config.py
tests/
  test_symmetry.py
  test_credit.py
  test_freeze.py
results/
  v0.json
docs/
  FORMALISM.md
  LINEAGE.md
  WHAT_THIS_MIGHT_MEAN.md
  superpowers/specs/2026-09-28-structure-arrow-consequence-design.md
```

If implementation remains genuinely tiny, `sac/` may be collapsed into fewer files, but tests and conceptual boundaries must stay separate.

---

## Engineering constraints

- Python + NumPy only unless a dependency earns its place.
- CPU-only.
- Deterministic seeds.
- No expensive hyperparameter search.
- No tuning each ablation independently.
- No plotting required for gate validity.
- Frozen final configuration must be committed before interpreting the final receipt.
- Tests must include algebraic invariants (`S^T=S`, `A^T=-A`) and causal boundary tests, not only smoke tests.
- A failed gate remains in the repository.

---

## Success criteria

v0 is worth keeping if it accomplishes one of two outcomes.

### Positive

It demonstrates, under matched controls, that:

1. reciprocal structure cannot recover temporal direction;
2. directed history cannot by itself recover later value assignment;
3. delayed consequence through eligibility changes a persistent mechanism;
4. the frozen full mechanism executes a held-out task better than the ablations for the declared causal reason.

### Negative but informative

It shows that one of these distinctions collapses in the minimal system, or that the full decomposition adds no executable power over a simpler baseline.

Either result narrows the synthesis.

---

## Explicit non-goals

v0 does not attempt to prove:

- a universal learning law;
- a literal neuronal model;
- a theory of consciousness;
- that evolution, development, synaptic plasticity, and transformer training are the same process;
- that spectral graph modes are thoughts;
- that a Laplacian is an algorithm;
- that local credit assignment is solved in general;
- that the decomposition is unique.

The repository should prefer a small killed claim over a broad unfalsifiable one.
