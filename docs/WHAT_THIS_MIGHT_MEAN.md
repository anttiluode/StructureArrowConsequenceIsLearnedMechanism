# What this might mean

This file is intentionally more speculative than the executable result. Nothing here should be read back into `results/v0.json` as an earned claim.

## 1. The deeper object may be an equivalence relation, not a component diagram

The first temptation is to draw three boxes:

```text
Structure -> Arrow -> Consequence
```

That is probably too engineering-shaped.

A more interesting reading is that experience progressively destroys equivalences that existed before the history occurred.

Before order matters, a route and its reverse may be treated as the same undirected object:

\[
h \sim Rh.
\]

Writing an arrow breaks that equivalence because

\[
A(Rh)=-A(h).
\]

Before consequence matters, two equally experienced routes may be behaviorally equivalent. Reassign the delayed outcome and only the consequence coordinate is allowed to change. The system now distinguishes histories that had identical structure and temporal counts but different consequences.

So learning can sometimes be viewed as:

> **the progressive refinement of which histories the future system treats as equivalent.**

That is a less box-like statement than "three modules make learning."

## 2. History becoming mechanism

A history is gone in the ordinary sense: the events no longer exist. Yet something about it can remain as a constraint on future transformations.

The sequence is:

\[
\text{transient events}
\rightarrow
\text{persistent residue}
\rightarrow
\text{changed future operator}.
\]

This is the common shape behind several otherwise different projects:

- a dendritic/arbor geometry left by development;
- asymmetric recurrent weights left by ordered spikes;
- a fly population whose resonant composition was selected by outcomes;
- a resident state that changes the effective operator without changing long-term parameters;
- a trained network whose distributed dynamics can later be decoded into a smaller program.

The important word is **compiled**. Experience is not merely remembered as a recording. It changes what transformations are cheap, legal, likely, or even available later.

## 3. Geometry, circulation, and value

There is a useful mathematical analogy here, as long as it stays an analogy.

`S` resembles a topology/conductance: where can influence pass?

`A` resembles a circulation or nonequilibrium current: which direction did flow preferentially take?

`C` resembles an outcome-shaped potential or edge value: which local possibilities became attractive or repulsive after consequence?

This makes the learned mechanism look less like a static lookup table and more like **computation on structured matter**:

```text
where movement is possible
× how history circulates through it
× which regions/outcomes matter
```

Graph theory has much richer decompositions of flow—gradient, curl/cycle, harmonic components, directed Laplacians, Hodge theory. SAC v0 is not any one of those theories. But those tools may be the right mathematical language for the next step because they explicitly separate topology, potential-like gradients, and circulation.

A particularly important lesson from v0 is that a symmetric value field can still induce directional behavior. The antisymmetric `A` is therefore not "all direction." It is **time-reversal-odd historical flux**. A value gradient is a different source of an arrow in behavior.

That correction may matter a lot.

## 4. Why the DevelopmentalSpectralNeuron failure now looks informative

The failed developmental spectral experiment tried to let temporal history become graph anatomy and then read computation from the Laplacian.

But an undirected Laplacian is, by construction, mostly a statement about reciprocal geometry. Two opposite traversals can share the same skeleton and the same undirected spectral coordinates.

That does not mean spectral structure is useless. It means the pipeline

```text
history -> graph -> undirected Laplacian -> algorithm
```

can erase precisely the variable that carries order.

A richer developmental compiler may need to preserve at least two things:

```text
reciprocal support / geometry
+
directed flux / order
```

and then some form of consequence must decide which of those directed possibilities are worth stabilizing.

The old fractal/skew repo had already given the warning in a different form: passive structure can magnify what is there, but if the signed local bias is absent there may be no reliable global arrow to magnify.

## 5. The flies are interesting because they make compilation visible

The fly line has been running for years because it gives a strange advantage: the agents are simple enough that global computation can emerge from populations of local rules without pretending each agent understands the result.

A fly does not know the algorithm the colony may implement.

A growth cone does not know the final arbor.

A synapse does not know the sequence replayed by the circuit.

A token does not know the transformer computation in which it participates.

This is not evidence that these systems are equivalent. It is a recurring design principle:

> **global computation can be manufactured by repeated local selection without a local element containing the global explanation.**

The scientific burden then shifts to the update rule. What local variable preserves the relevant sign? What marks causal participation? What delayed event selects it? What remains after the fast activity disappears?

That is exactly where the negative repositories become useful. They tell us which apparently plausible local variables were *not* enough.

## 6. Nested time scales

One possible broad interpretation is that SAC-like questions can be asked at several nested time scales:

- **evolution:** what substrate and learning rules exist at all?
- **development:** what physical routes/modes become available?
- **learning/plasticity:** what directed histories and consequences modify persistent parameters?
- **working/resident state:** what transient residue changes the operator available right now?
- **culture/artifacts:** what serial structures perturb another learner later?

These are not the same mechanisms. "Consequence" means radically different things at these levels: reproductive success is not dopamine, dopamine is not a supervised label, and gradient descent is not a trophic signal.

The possible unification is only at the level of a question:

> **How does past interaction restrict the family of operations available to the future?**

OperatorTime is the fast end of that question. Developmental morphology is a slow end. SAC supplies one vocabulary for asking what was preserved between them.

## 7. Transformer connection — narrower than "brains are transformers"

Transformers are useful here because they cleanly separate at least two time scales.

During inference, learned projection matrices can stay fixed while context and KV state change query-conditioned routing. The effective attention operator is therefore context-dependent even without weight updates.

Across training, outcome/loss changes the slower parameters.

That gives a structural analogy:

```text
slow substrate/parameters
+
resident history/context
+
query-conditioned directed routing
+
training consequence on a slower clock
```

But attention is not this repo's antisymmetric `A`; attention matrices are generally neither symmetric nor skew-symmetric. Gradient descent is not this repo's local eligibility rule. The analogy is about **nested operator time**, not one-to-one biological parts.

The potentially useful engineering question is more specific:

> Can a frozen large model be given a persistent sparse memory that separately tracks availability, directed transition history, and consequence, so that repeated experience compiles into a small executable routing substrate rather than only more prompt/KV tokens?

AdaptiveObserverCache, TransformerToX, Rytmi, and the history-compiler discussions approach pieces of that question from different sides.

## 8. Algorithm distillation, corrected

The naive version was:

```text
successful trajectories
-> skeletonize them
-> graph Laplacian
-> algorithm
```

ResonantCortex2 and DevelopmentalSpectralNeuron both warn against that jump.

A more credible target is:

```text
experience
-> persistent topology/support
-> directed transition statistics
-> consequence-linked eligibility
-> query/goal-dependent routing
-> frozen executable surrogate
```

Only the last line earns the word **algorithm**.

NeuralAlgorithmDecoding then suggests the inverse direction:

```text
frozen learned mechanism
-> interventions / counterfactuals
-> smallest faithful executable abstraction
```

Put together, there is a forward-and-inverse research program:

1. **compile** experience into a mechanism;
2. **decompile** the mechanism back into a causal program;
3. compare the recovered program to the answer key;
4. attack both sides with interventions.

The flies are unusually useful here because we can own both the organism and the answer key.

## 9. What would make this more profound rather than merely neat

The current v0 is a constructed separation test. The roles are designed so the transformations are identifiable. That is useful calibration, not discovery.

The next profound step would be to remove the labels and ask whether the decomposition can be **found** from behavior and interventions:

- observe a black box with unknown persistent state;
- reverse selected trajectories;
- reassign outcomes while holding transitions fixed;
- perturb candidate edges/states;
- infer which recovered coordinates are reversal-even, reversal-odd, and consequence-sensitive;
- compile the smallest model that predicts held-out interventions.

That would connect FlyBench directly to NeuralAlgorithmDecoding: not "we built S, A, C," but "an outside scientist recovered the transformation classes that the hidden mechanism actually uses."

And if the hidden organism does **not** admit the SAC decomposition, the right answer should be `NOT_IDENTIFIABLE` or a different decomposition—not force the world into our three letters.

That is probably the real escape from the box.
