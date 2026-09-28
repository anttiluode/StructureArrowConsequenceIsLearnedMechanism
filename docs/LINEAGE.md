# Lineage — what the older repositories earned, and what this repo borrows

This document is not a list of inspirations. It is an evidence boundary. Each older project is separated into **earned**, **used here**, and **not claimed**.

## GeometricNeuron / GeometricNeuronAndSapolskysFractal

**Earned.** The geometric-neuron line repeatedly separated a reciprocal/symmetric object from a directional/skew object. The later fractal demo made that distinction visible in development: local reciprocal attraction grew a bush with chirality wandering around zero, while a small consistent local skew accumulated into a reproducible global handedness.

**Used here.** The algebraic split `S^T=S`, `A^T=-A`, and the insistence that passive geometry is not automatically a temporal arrow.

**Not claimed.** Chirality is not learning, the growth demo is not evidence for literal neuronal morphogenesis, and this repo does not establish a biological fractal scaling law.

## Rytmi / TATWATASW

**Earned.** In Rytmi R1, the measured chain was plateau-written asymmetric field -> rhythmic inhibition -> emergent phase precession -> STDP -> ordered replay. Scrambling spike order inside each theta cycle preserved spikes and cells but destroyed ordered replay. G0 then showed one cue could launch long replay and that rhythmic dead time suppressed spurious second waves under noise.

**Used here.** Temporal order deserves its own causal coordinate. Activity amount and membership can stay similar while order changes what is written.

**Not claimed.** The `A` matrix here is not hippocampal phase precession, STDP, theta, or a biological sequence circuit.

## FunctionalArbors

**Earned.** The strongest positive stage showed a free branching arbor using local grow/prune operations, pulse eligibility, and soma consequence to discover task-useful geometric delays. Later stages then exposed the hard part: explicit return transport of consequence could work while free credit assignment remained null, and even exact "these cells were just born" tags were too coarse.

**Used here.** Eligibility and consequence must be distinct. "Recently active" or "recently changed" is only a candidate cause until delayed outcome selects it.

**Not claimed.** v0 does not solve the causal-credit problem that FunctionalArbors hit. It resets eligibility each route episode and uses a tiny controlled world.

## FlyBench — from dumbflies to the clicker neuron

**Earned.** The original dumbflies audit showed why behavior prediction is not mechanism discovery: a flexible observer reached nearly perfect speed prediction mostly from inertia while the actual visual story was wrong. The resonator flies then made tuning causally affect place preference. In the clicker-neuron stage, local resonant participation plus an eligibility trace and delayed clicks changed which flies/synapses survived and budded; different teaching histories left visibly different substrates under the same later test. The local online mechanism did not beat a globally optimized fixed resonator bank on raw accuracy.

**Used here.** A concrete example of delayed consequence selecting among locally active candidates, and a reminder to keep predictive score separate from causal explanation.

**Not claimed.** The fork world is not a fly, colony, neuron, or model of dopamine.

## DevelopmentalSpectralNeuron

**Earned.** The frozen v0 was negative. Alternating versus blocked developmental histories produced less structural/probe variation than random seed; blind history readback was chance; low spectral modes did not beat geometry-matched nulls. An earlier positive receipt was invalidated after code review found implementation shortcuts/bugs.

**Used here.** History does not automatically become useful anatomy. A graph can grow and still erase the temporal distinction we hoped it would preserve.

**Not claimed.** The negative result does not prove development cannot store temporal order. It kills one particular local resonator/resource/stigmergy implementation.

## OperatorTime

**Earned.** Fixed substrate parameters can yield different effective operators when resident history differs. In matched synthetic gates, the same current probe and same event multiset produced different operator responses when order/history differed; serial artifacts constrained a trajectory through operator space rather than specifying a fixed operator by themselves.

**Used here.** The learned object should ultimately be judged by **what operation is available now**, not merely by whether a state variable stores history.

**Not claimed.** SAC v0 has no transformer, self model, semantic text, or rich resident-state operator factory.

## ResonantCortex2

**Earned.** Search trajectories contained locally compressible structure and some cross-solver geometry, but the frozen compressed/routed machine did not execute the held-out algorithms. The failure moved the bottleneck from "find a regular trace" to **composition and routing**.

**Used here.** A graph, mode bank, or compressed trace is not an algorithm until the frozen object itself executes.

**Not claimed.** SAC v0 does not solve general algorithm distillation. Its world is deliberately constructed so the relevant roles are identifiable.

## NeuralAlgorithmDecoding

**Earned.** On controlled organisms, distributed learned computation could sometimes be reduced to smaller executable causal descriptions. A GRU addition model yielded an exact two-state carry transducer under intervention tests; later gates also preserved `NOT_IDENTIFIABLE` when hidden causes were deliberately aliased.

**Used here.** There is a natural inverse problem: after experience compiles a mechanism, can an outside observer recover the smallest faithful causal abstraction under interventions?

**Not claimed.** v0 does not run that inverse decoder. It supplies a tiny forward organism with an answer key that could be used for such a test later.

## The recurring line

Across these repositories, a more careful common sentence is visible:

```text
variation / available structure
        ->
ordered local events
        ->
short-lived eligibility
        ->
delayed consequence
        ->
persistent change
        ->
a different operator is available next time
```

Different repositories instantiate different arrows in that diagram, and several fail precisely because one arrow is missing.

The synthesis in this repository is therefore not "all the old projects were secretly SAC." It is:

> **SAC is a compact set of questions to ask of them. What interactions existed? What part of history was reversal-sensitive? What later outcome selected among those histories? What executable operation remained afterward?**
