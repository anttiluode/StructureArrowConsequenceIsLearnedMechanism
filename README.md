# Structure → Arrow → Consequence → Learned Mechanism

A tiny executable falsifier for a pattern that kept reappearing across the repo genealogy:

> **What interactions exist? Which part of history changes sign when time is reversed? Which delayed outcomes select among those histories? What operation is left available afterward?**

This repository does **not** claim those are three universal modules of learning. The useful formulation turned out to be about transformation classes, not boxes.

## Frozen v0 result

All three predeclared gates pass in the minimal forked-world experiment.

| test | result |
|---|---:|
| reverse history: `S` max difference | **0.0** |
| reverse history: `A + A_reverse` max error | **0.0** |
| direction from `S` only | **0.50** |
| direction from `S+A` | **1.00** |
| reward reassignment: `S` max difference | **0.0** |
| reward reassignment: `A` max difference | **0.0** |
| rewarded fork, full `S+A+C` | **1.00** |
| rewarded fork, `S+A` | **0.50** |
| shuffled delayed consequence, fork | **0.46875** |
| full held-out probes | **1.00** |
| `S+C` interior direction | **0.50** |
| illegal edge choices | **0** |
| frozen-state mutation during probes | **none detected** |

Committed receipt: [`results/v0.json`](results/v0.json).

The important ablation table is:

| enabled score terms* | fork value | interior direction | all held-out probes |
|---|---:|---:|---:|
| `S` | 0.50 | 0.50 | 0.50 |
| `A` | 0.50 | 1.00 | 0.90 |
| `C` | 1.00 | 0.50 | 0.60 |
| `S+A` | 0.50 | 1.00 | 0.90 |
| `S+C` | 1.00 | 0.50 | 0.60 |
| `A+C` | 1.00 | 1.00 | 1.00 |
| `S+A+C` | **1.00** | **1.00** | **1.00** |

\* `S` always supplies the hard legal-edge mask. `A+C` therefore means "omit support magnitude from the score," **not** "remove topology." In this matched world all used edges have equal support, so `A+C` and `S+A+C` are numerically identical. That is a limitation, not something to hide.

## The minimal mechanism

For an observed transition `i -> j`:

### Structure — reversal-even support

```text
S[i,j] += 1
S[j,i] += 1
```

so

\[
S^T=S.
\]

`S` says which routes exist. Reverse a trajectory and its reciprocal support is unchanged.

### Arrow — reversal-odd temporal flux

```text
A[i,j] += 1
A[j,i] -= 1
```

so

\[
A^T=-A,
\qquad A(Rh)=-A(h).
\]

`A` is specifically the part of temporal history that flips sign under reversal.

### Eligibility and consequence

Within an episode:

\[
E_{t+1}=0.8E_t+B(i,j).
\]

At the terminal:

\[
C\leftarrow C+rE.
\]

The reward is `+1` on the designated arm and `-1` on the other. Reassign the reward while replaying exactly the same balanced transitions and `S`/`A` remain unchanged; only `C` changes.

The frozen executor then asks which legal transition is supported by the declared combination of history and consequence. It never receives reward during probing.

## The three gates

### Gate S — structure is not temporal direction

Matched histories:

```text
0 -> 1 -> 2
2 -> 1 -> 0
```

They have identical `S`. At node 1, `S` alone is tied (`0.50`); `S+A` identifies the experienced direction (`1.00`).

### Gate A — direction is not value

Both arms are traversed equally often in the same directions. Only the delayed outcome assignment changes.

```text
same S
same A
different C
```

`S+A` therefore cannot know which equally experienced arm is valuable (`0.50` at the fork). Correctly assigned consequence gives `1.00`. Shuffle those terminal outcomes in time and fork accuracy falls to `0.46875` across the frozen 32 seeds.

### Gate SAC — freeze it and make it run

After training, `S`, `A`, and `C` are frozen. The teacher/reward is removed.

The held-out probes ask two different things:

1. at the fork, choose the arm whose past consequence was positive;
2. from interior states on **both** arms, continue in the experienced forward direction.

Full SAC scores `1.00`. `S+A` has direction but not value. `S+C` has value but fails half the interior-direction probes.

## An important correction: C can also make an arrow in behavior

`C` is symmetric, but delayed reward arrives after a sequence of decaying eligibility traces. On the rewarded arm, later edges therefore have larger positive `C` than earlier edges. A local chooser can climb that gradient toward reward.

So this repo does **not** say "all direction lives in antisymmetry."

It says:

- `A` is a clean carrier of **time-reversal-odd historical flux**;
- a symmetric value field can independently induce a **policy direction** through local comparison.

That distinction is one of the more useful things that fell out of building the falsifier. See [`docs/FORMALISM.md`](docs/FORMALISM.md).

## Why this repo exists in the genealogy

The idea did not begin here.

- **GeometricNeuron / GeometricNeuronAndSapolskysFractal:** reciprocal geometry and skew/direction were already separate; a tiny consistent local skew could be magnified into a global arrow.
- **Rytmi / TATWATASW:** scramble within-cycle temporal order while preserving spikes and replay order collapses; time/order is causal.
- **FunctionalArbors:** local structural variation becomes useful only when eligibility meets later soma consequence; later versions show that *correct* causal assignment is much harder than transporting reward.
- **FlyBench:** the original flies demonstrated how prediction can hide mechanism; the clicker neuron then made sparse delayed teaching visibly reshape a local resonant substrate.
- **DevelopmentalSpectralNeuron:** negative result—temporal developmental order did not automatically become readable anatomy or useful spectral modes.
- **OperatorTime:** the operation available now can depend on resident history even with fixed substrate parameters.
- **ResonantCortex2:** compressible successful trajectories were not enough; frozen composition/routing failed, so a pretty structure is not yet an algorithm.
- **NeuralAlgorithmDecoding:** in controlled cases, a distributed learned process can be interrogated back into a smaller executable causal abstraction—and can correctly return `NOT_IDENTIFIABLE` when the hidden cause is aliased.

The detailed evidence boundary is in [`docs/LINEAGE.md`](docs/LINEAGE.md).

## The deeper hypothesis

The more interesting formulation is not "learning has three boxes." It is:

> **Learning can sometimes be described as history progressively refining which pasts the future system treats as equivalent.**

Reciprocal structure is invariant to reversal. Temporal flux is not. Outcome reassignment then separates histories that had the same structure and direction statistics but different consequences. The residue of those broken equivalences is an executable constraint on the future.

Schematically:

```text
transient experience
    -> what interactions remain possible
    -> what temporal asymmetries remain
    -> what outcomes stabilize/suppress them
    -> what operator is available next time
```

That may be a useful question across development, learning, resident state, artificial agents, and algorithm distillation without claiming those processes use the same biological mechanism.

See [`docs/WHAT_THIS_MIGHT_MEAN.md`](docs/WHAT_THIS_MIGHT_MEAN.md) for the speculative version, including the graph-flow / transformer / algorithm-distillation connections and where the analogy should stop.

## Run it

Requires Python 3.11+ and NumPy. Tests use pytest.

```bash
python -m pytest -q
python experiment.py --output results/v0.json
python experiment.py --check-receipt results/v0.json
```

The final command regenerates the entire deterministic 32-seed experiment and fails if one byte of the committed receipt changes.

## What this does not establish

It does not establish:

- a universal law of learning;
- a literal neuronal mechanism;
- general structural credit assignment;
- that `S/A/C` is a unique basis;
- that an undirected Laplacian plus a skew matrix is sufficient for intelligence;
- that evolution, dendritic development, dopamine, gradient descent, and teacher clicks are the same kind of consequence;
- that transformers implement this decomposition;
- that this toy has discovered an algorithm rather than validating a deliberately constructed separation.

The next worthwhile test is harder and less box-like: **hide the decomposition, expose only behavior/interventions, and ask an outside observer to recover the reversal-even, reversal-odd, and consequence-sensitive coordinates—or say that this decomposition is not identifiable.**

That would make this repo meet FlyBench and NeuralAlgorithmDecoding from opposite directions.
