# A Slope Is Not a Guarantee

A chart has a line through four points. The analyst writes that the investment goes up 1.4% whenever the market rises. The sentence discards the intercept, residuals, units and sampling conditions. Reconstruct the fitted relationship before treating it as a rule.

## Build the line from small numbers

Use this wholly invented four-period example. Each row pairs an asset and the same period's benchmark. Both returns are expressed in percentage points, not dollars. No transaction costs or forecasts are implied.

| Period | Benchmark x | Asset y |
| --- | ---: | ---: |
| A | −4 | −5 |
| B | −2 | −1 |
| C | 2 | 3 |
| D | 4 | 7 |

An ordinary least-squares line with intercept minimizes the sum of squared **vertical** residuals in this specification. Compute mean x = 0 and mean y = 1. Cross products of the centered values sum to 56, and the sum of squared centered benchmark values is 40. Dividing gives a slope of 1.4; its intercept is mean y minus slope times mean x, or 1. In this specified regression the dimensionless slope earns the informal label “beta” with respect to that benchmark and sample. The fitted value in the same return units is `1 + 1.4x`.

At x = −2, the fitted y is −1.8. The observed value is −1.0, so observed minus fitted is +0.8. The other residuals in chronological order are −0.4, −0.8 and +0.4. Check the four residuals sum to zero to rounding; that follows from fitting a free intercept here. A fit through a different set of observations can produce a different slope.

## Draw a boundary around the inference

A one percentage-point difference in x changes the line's fitted y by 1.4 percentage points. It does not guarantee observed y changes by that amount, does not attribute cause, and does not prove the line is useful beyond the observed range. If benchmark returns were all equal, the slope's denominator would be zero. Changing benchmarks or choosing a favorable window after seeing results also changes what this estimate means. A four-point toy line is for reconstruction, not investment advice.

**Teardown.** “At x = 0 the asset is promised 1%, and there is no chance of losing.” That is a fitted point in a small sample, not a payoff guarantee. Distinguish a prediction input, a fitted value, and a contract.

**Transfer.** Append a fifth row x = 0, y = −4. Recalculate both means, slope and intercept. Explain how an observation at the old x mean can change the intercept without changing this example's slope. Do not use that property to assume all new observations are harmless.

[Contents](../README.md)
