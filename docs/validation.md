# Model Validation

This document provides a summary of the complete model validation conducted in `notebooks/validation.ipynb`, including baseline behaviour tests, policy response tests, extreme condition tests, and sensitivity analysis.

## Baseline Behaviour Tests

Two baseline simulations were used, one theoretical check and one realistic check.

### Zero-tax Baseline

With carbon tax = 0:

- All variables remain in perfect steady state for 10 years
- Freight activity, efficiency, CI, prices, and margins remain constant
- Only cumulative stocks grow linearly (as expected)

This confirms internal equilibrium and absence of unintended drift.

### Japanese Carbon Tax Baseline

With carbon tax = 289 ¥/tCO2:

- Behaviour is almost identical to zero-tax baseline
- Slight improvements in efficiency and CI
- Small shifts in margin and activity (<1%)
- Profit increases slightly due to activity growth, while margin decreases slightly
- Cumulative profit still lower than 0-tax case

These tiny adjustments are economically realistic and consistent with an extremely small carbon tax.

## Policy Response Tests

A set of carbon-tax scenarios (2,000–20,000 ¥/tCO₂) were simulated to test behavioural validity.

### Expected Directional Responses

For higher carbon taxes, the model consistently produced:

- Increasing fuel price and freight price
- Decreasing freight demand, freight activity, emissions, profit, and margins

All signs match economic reasoning and empirical expectations.

### Viability Boundary Behaviour

Strong taxes drive margins below 2% for long enough to trigger the viability condition, while moderate taxes remain viable. This is reasonable behaviour.

## Extreme Condition Tests

Extreme parameter settings were simulated to ensure structural robustness. Four tests were conducted:

- Very High Carbon Tax
- Very Low Demand
- Very Low Fuel Price
- Very High Demand

The model behaves reasonably across wide extremes and shows no pathological behaviour.

## Sensitivity Analysis

A sensitivity analysis was performed for:

- Desired pass-through share
- Short-run elasticity
- Long-run elasticity
- Maximum efficiency improvement
- Maximum CI reduction
- Cost-pressure sensitivity

For each parameter setting, three metrics were computed:

- Max viable carbon tax
- CO2 reduction at 5000 ¥/tCO2
- Average margin at 289 ¥/tCO2

### Robustness of Viability

- Max viable tax consistently within ~3,900–9,000 ¥/tCO2
- Only major driver affecting viability: pass-through share
- All other parameters had minimal impact on viability boundary

### Robustness of CO₂ Reduction

- CO2 reduction at 5,000 ¥/tCO2 always between ~30–39%
- Direction and magnitude stable across all assumptions

### Robustness of Baseline Margins

- Average margin at 289 ¥/tCO₂ remained ~4.6% for all parameter sets
- Indicates strong baseline stability

## Validation Conclusion

Across all tests, the model demonstrates that it is valid for policy exploration.
