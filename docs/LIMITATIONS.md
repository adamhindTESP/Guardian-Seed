## Modeling Choice: Competing Objective Shocks

Competing optimization pressures are modeled as exponentially distributed
negative shocks, \( E_t \sim \mathrm{Exp}(1) \).

This choice reflects **bursty, asymmetric interference** commonly observed
in optimization systems, where many small competing pressures occur
frequently, and rare but large suppressive events can dominate dynamics.

The exponential distribution is intentionally conservative:
it permits heavy-tailed downside risk rather than assuming symmetric,
bounded, or Gaussian competition.

This model is not intended as a claim about real-world training dynamics,
only as a stress-test for prior persistence under unfavorable conditions.
Alternative distributions (e.g., Gaussian, bounded, Pareto) are not excluded
and may be explored in future validation gates, but are not required for
Tier-1 sensitivity and falsification analysis.
