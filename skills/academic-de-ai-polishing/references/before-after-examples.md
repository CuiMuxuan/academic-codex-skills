# Before / After Examples

Use these examples to calibrate what "lower AIGC trace" rewriting should look like in academic prose. The goal is not to imitate the exact wording below. The goal is to preserve meaning while changing cadence, logic delivery, and authorial stance.

Each example includes:

- a high-risk original
- a stronger revision
- the main reason the original sounded templated
- what the revision changed without changing the claim

## Example 1: Connector Stacking

### Before

`Moreover, humid conditions significantly affect adsorption performance. Furthermore, water molecules compete for adsorption sites. Therefore, the removal efficiency of hydrophobic pollutants may decline substantially.`

### After

`Under humid operation, adsorption capacity often narrows for a more specific reason than the percentage data first suggest: water occupies accessible sites and leaves less usable pore volume for hydrophobic odorants, so apparent polishing capacity can fall quickly once competitive uptake becomes dominant.`

### Why the original felt AI-shaped

- stacked connectors carried the logic instead of the content
- each sentence was short, even, and declarative
- the paragraph summarized rather than explained

### What changed

- the transition became causal rather than signposted
- mechanism replaced generic summary
- sentence rhythm became less uniform

## Example 2: Mirror-Balanced Contrast

### Before

`Biological treatment is cost-effective and environmentally friendly, but its stability remains a major challenge under fluctuating operating conditions.`

### After

`Biological treatment remains attractive because its operating burden can be lower than that of chemical or thermal routes once the system is established. That advantage becomes less decisive when inlet composition swings rapidly, since the same wet biofilm that supports efficient bulk removal also makes the process vulnerable to transient overloading, acidification, and maldistribution.`

### Why the original felt AI-shaped

- built from the familiar "X is good, but Y is challenging" template
- no mechanism connected the benefit and the limitation
- "major challenge" was generic filler

### What changed

- the trade-off was unpacked rather than balanced symmetrically
- the limitation was tied to failure routes
- the prose sounds more evaluative and less formulaic

## Example 3: Over-Scripted Review Critique

### Before

`Existing technology-by-technology reviews provide useful information. However, they cannot adequately guide process selection under real humid multicomponent conditions.`

### After

`Technology-by-technology reviews remain useful for orientation, but they are much less reliable once the design question shifts from unit description to route selection under humid multicomponent service. At that point, the decisive issue is no longer what each unit can do in isolation, but which burden it can absorb without destabilizing the rest of the train.`

### Why the original felt AI-shaped

- classic "existing studies are useful, however..." frame
- the critique was correct but too neatly staged
- the practical deficiency was abstract

### What changed

- the criticism now emerges from a concrete design consequence
- the paragraph sounds more like an engineering judgment than a template

## Example 4: Checklist Logic

### Before

`The first issue is water competition. The second issue is multicomponent interference. The third issue is load fluctuation.`

### After

`Three constraints repeatedly narrow the usable operating window under humid multicomponent service. Water competition is often the first to appear because it reshapes transfer or site access before removal collapses visibly. Mixed-pollutant interference then redistributes removal burdens across the train, while load fluctuation determines whether those burdens remain transient or accumulate into chronic instability.`

### Why the original felt AI-shaped

- it reads like outline expansion
- each sentence has identical construction
- no hierarchy or interaction is expressed

### What changed

- the list became an argument about how constraints unfold
- repetition was reduced without losing the three-part structure

## Example 5: Generic Future-Work Boilerplate

### Before

`More studies are needed to evaluate long-term performance and standardize reporting methods in future research.`

### After

`What the field lacks is not another short-duration removal study, but longer real-gas validation with a minimum reporting set that makes cross-study comparison possible: residence time, loading history, humidity, pressure drop, pH or conductivity when relevant, by-product profile, and stability after disturbance or regeneration.`

### Why the original felt AI-shaped

- classic future-work boilerplate
- "more studies are needed" says little about what is actually missing

### What changed

- the research gap became specific
- reporting variables were named directly
- the sentence now carries judgment about field priorities

## Example 6: Safe Summary Without Stake

### Before

`Taken together, these studies provide valuable insights into the treatment of odorous gases under humid conditions.`

### After

`Taken together, these studies do not support a single best technology claim. What they do show, more convincingly, is that humid odorous-gas control succeeds only when each unit is assigned a burden consistent with its actual operating window rather than its headline removal efficiency.`

### Why the original felt AI-shaped

- broad synthesis with no stake
- "valuable insights" is low-information academic filler

### What changed

- the revision states what the evidence does and does not justify
- the synthesis becomes selective, not ceremonial

## Example 7: Abstract-Level Over-Smoothing

### Before

`This review systematically summarizes recent advances in the treatment of humid multicomponent odorous gases and provides important guidance for future process design.`

### After

`This review examines humid multicomponent odor control as a process-allocation problem rather than a catalogue of isolated technologies, with emphasis on how pollutant properties, humidity penalties, and failure routes determine whether a unit is credible as front-end capture, bulk removal, or trace polishing.`

### Why the original felt AI-shaped

- abstract jargon with no distinguishing claim
- "systematically summarizes" and "important guidance" are both generic

### What changed

- the review angle is stated explicitly
- the sentence now has a sharper organizing claim

## Example 8: Hybrid-Route Template

### Before

`Hybrid route I combines scrubbing with biological treatment. Hybrid route II combines biological treatment with adsorption. Hybrid route III combines adsorption with thermal oxidation.`

### After

`These hybrid routes differ less in how many units they contain than in where they place the control burden. Scrubbing followed by biological polishing is most defensible when soluble inlet shocks would otherwise destabilize the downstream biology. Biological treatment plus adsorption makes sense when bulk removal is already stable and the remaining problem is low-threshold residual odor. Adsorption coupled to thermal oxidation belongs to a different class again, because its credibility depends on whether concentration and regeneration can be achieved without shifting the penalty into energy demand or secondary handling.`

### Why the original felt AI-shaped

- route-by-route labeling with identical sentence frames
- no trade-off logic
- reads like generated taxonomy

### What changed

- the route list was recast as burden allocation logic
- each route is distinguished by a different engineering rationale

## Example 9: Headline-Metric Inflation

### Before

`High removal efficiency indicates that the system has excellent treatment performance under humid conditions.`

### After

`High removal efficiency is only a partial indicator under humid operation. Unless it is read alongside loading history, runtime stability, pressure drop, liquid chemistry, or breakthrough behavior, the same percentage can describe either a genuinely robust system or a narrow operating window that has not yet been stressed.`

### Why the original felt AI-shaped

- overconfident interpretation of a generic metric
- no hidden qualifier

### What changed

- the revision inserts measurement discipline
- performance is judged in context rather than by a single number

## Example 10: Introduction Confidence That Feels Too Perfect

### Before

`The challenge of odorous gas control has become increasingly significant in modern industry, and this review provides a timely and comprehensive response to that need.`

### After

`Odorous-gas control in humid industrial settings is not difficult to justify as an environmental priority; the harder problem is that the available treatment literature still offers limited help when an engineer must decide how to distribute control burdens across a real multicomponent train. That gap, rather than novelty for its own sake, is what motivates the present review.`

### Why the original felt AI-shaped

- polished but generic importance claim
- "timely and comprehensive" is promotional

### What changed

- the motivation is reframed as a concrete unmet decision need
- the prose sounds more grounded and less sales-like

## How To Generalize These Examples

When using these examples in real work:

- keep the claim, but change the delivery mechanism
- replace symmetry with hierarchy, mechanism, or trade-off
- replace ceremonial summary with selective judgment
- let one sentence do explanatory work, not just connective work
- prefer local rewrites over full redrafting unless the whole paragraph is structurally unsalvageable
