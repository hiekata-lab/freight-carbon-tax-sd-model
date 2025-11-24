# Equation Documentation

Documentation of all equations used in the system dynamics model, grouped by subsystem.

## Fuel Price & Operating Cost

This subsystem determines how fuel price, driven by pre-tax fuel price and carbon tax rate, affects operating cost and freight price. This structure connects carbon policy to economic impacts on operators.

### Fuel Price

- **Equation:**
  $$
  \text{Fuel Price} = \text{Pretax Fuel Price} + \text{Tax per Liter}
  $$
- **Units:** `¥/liter`
- **Description:** Market fuel price that freight operators pay.

### Tax per Liter

- **Equation:**
  $$
  \text{Tax per Liter} = \text{Carbon Tax Rate} \times \text{Carbon Content of Fuel}
  $$
- **Units:** `¥/liter`
- **Description:** Converts a carbon tax (¥/tCO2) to a fuel-tax amount per liter.

### Fuel Cost per km

- **Equation:**
  $$
  \text{Fuel Cost per km} = \frac{\text{Fuel Price}}{\text{Average Fuel Efficiency}}
  $$
- **Units:** `¥/km`
- **Description:** Fuel portion of per-km operating cost.

### Baseline Fuel Cost per km

- **Equation:**
  $$
  \text{Baseline Fuel Cost per km} = \frac{\text{Pre-Tax Fuel Price}}{\text{Baseline Fuel Efficiency}}
  $$
- **Units:** `¥/km`
- **Description:** Reference-level fuel cost before carbon tax is applied.

### Extra Fuel Cost per km

- **Equation:**
  $$
  \text{Extra Fuel Cost per km} = \text{Fuel Cost per km} - \text{Baseline Fuel Cost per km}
  $$
- **Units:** `¥/km`
- **Description:** The incremental fuel cost arising from the carbon tax. This is the cost component that operators try to pass through to customers.

### Operating Cost per km

- **Equation:**
  $$
  \text{Operating Cost per km} = \text{Non-Fuel Cost per km} + \text{Fuel Cost per km}
  $$
- **Units:** `¥/km`
- **Description:** Total per-km operating cost of freight movement.

### Baseline Operating Cost per km

- **Equation:**
  $$
  \text{Baseline Operating Cost per km} = \text{Non-Fuel Cost per km} + \text{Baseline Fuel Cost per km}
  $$
- **Units:** `¥/km`
- **Description:** Normal operating cost before carbon tax.

### Baseline Margin per km

- **Equation:**
  $$
  \text{Baseline Margin per km} = \text{Baseline Price Margin} \times \text{Baseline Operating Cost per km}
  $$
- **Units:** `¥/km`
- **Description:** The additional baseline margin per km used to construct the freight price.

### Actual Freight Price

- **Equation:**
  $$
  \text{Actual Freight Price} = \text{Baseline Freight Price} + \text{Effective Pass-Through Share} \times \text{Extra Fuel Cost per km}
  $$
- **Units:** `¥/tkm`
- **Description:** The actual freight price operators set immediately, accounting for the incremental cost increase from the tax.

### Perceived Freight Price

- **Equation:**
  $$
  \text{Perceived Freight Price} = \text{SMOOTH}(\text{Actual Freight Price}, \text{Tau}_p)
  $$
- **Units:** `¥/tkm`
- **Description:** The price customers believe they pay, adjusting gradually to actual price changes. Used to determine demand elasticities.

### Baseline Freight Price

- **Equation:**
  $$
  \text{Baseline Freight Price} = \text{Baseline Operating Cost per km} + \text{Baseline Margin per km}
  $$
- **Units:** `¥/tkm`
- **Description:** The freight price before carbon tax policy is applied. Used as the reference point for price changes and elasticity calculations.

### Effective Pass-Through Share

- **Equation:**
  $$
  \text{Effective Pass-Through Share} = \text{SMOOTH}(\text{Desired Pass-Through Share}, \text{Tau}_p)
  $$
- **Units:** `dimensionless`
- **Description:** A delayed adjustment toward the target pass-through share. This avoids instant jumps in pricing behaviour.

## Freight Demand & Activity

Models customer demand response to freight price changes through short- and long-run elasticities and delays.

### Freight Demand

- **Equation:**
  $$
  \text{Freight Demand} = \text{Underlying Freight Activity} + \text{Short-Run Price Effect on Demand} + \text{Long-Run Price Effect on Demand}
  $$
- **Units:** `tkm/month`
- **Description:** Total freight demand after incorporating short‐run and long‐run adjustments to price. Underlying Activity represents the baseline level of freight movement, while the price effects adjust demand in response to perceived freight prices.

### Short-Run Price Effect on Demand

- **Equation:**
  $$
  \text{Short-Run Price Effect on Demand} = \text{SMOOTH}\left(
    \text{Underlying Freight Activity} \times \left(\frac{\text{Perceived Freight Price}}{\text{Baseline Freight Price}}\right)^{\text{Elasticity SR}} - \text{Underlying Freight Activity},
    \text{Tau SR}
  \right)
  $$
- **Units:** `tkm/month`
- **Description:** Short-run (immediate) demand response to price changes. This uses the short-run price elasticity and a short adjustment delay. The smoothing prevents unrealistic instantaneous changes in demand.

### Long-Run Price Effect on Demand

- **Equation:**
  $$
  \text{Long-Run Price Effect on Demand} = \text{SMOOTH}\left(
    \text{Underlying Freight Activity} \times \left(\frac{\text{Perceived Freight Price}}{\text{Baseline Freight Price}}\right)^{\text{Elasticity LR}} - \text{Underlying Freight Activity},
    \text{Tau LR}
  \right)
  $$
- **Units:** `tkm/month`
- **Description:** Long-run demand response to price changes, using a larger elasticity and a slower adjustment. Represents structural/logistical adjustments: route changes, alternative modes, etc.

### Underlying Freight Activity (Stock)

- **Equation:**
  $$
  \text{Underlying Freight Activity} = \text{INTEG}(\text{Freight Activity Growth Rate} \times \text{Underlying Freight Activity}, \text{Baseline Demand})
  $$
- **Units:** `tkm/month`
- **Description:** Baseline structural freight movement. This represents underlying macroeconomic demand for freight independent of price effects.

### Freight Activity

- **Equation:**
  $$
  \text{Freight Activity} = \text{Freight Demand}
  $$
- **Units:** `tkm/month`
- **Description:** The actual freight activity, equal to freight demand in this model because short-run supply is highly elastic.

## Fuel Efficiency

Models how operator fuel efficiency improves as fuel costs increases with tax.

### Average Fuel Efficiency (Stock)

- **Equation:**
  $$
  \text{Average Fuel Efficiency} = \text{INTEG}(\text{Improvement} - \text{Degradation}, \text{Baseline Fuel Efficiency})
  $$
- **Units:** `km/liter`
- **Description:** The average fuel efficiency of the fleet, a stock that increases through improvement and decreases through degradation.

### Improvement (Flow)

- **Equation:**
  $$
  \text{Improvement} = \frac{\text{Efficiency Target} - \text{Average Fuel Efficiency}}{\text{Tau Eff}}
  $$
- **Units:** `km/liter/month`
- **Description:** The rate of fuel efficiency improvement, proportional to the gap between target and current efficiency, with adjustment time Tau Eff.

### Degradation (Flow)

- **Equation:**
  $$
  \text{Degradation} = \text{Average Fuel Efficiency} \times \text{Degradation Rate}
  $$
- **Units:** `km/liter/month`
- **Description:** The rate of fuel efficiency degradation, proportional to current efficiency and the degradation rate.

### Cost Pressure on Efficiency

- **Equation:**
  $$
  \text{Cost Pressure on Efficiency} = \text{Cost Pressure Sensitivity} \times \left(\frac{\text{Fuel Cost per km}}{\text{Baseline Fuel Cost per km}} - 1\right)
  $$
- **Units:** `dimensionless`
- **Description:** The pressure to improve efficiency based on increased fuel costs relative to baseline, scaled by sensitivity parameter.

### Efficiency Target

- **Equation:**
  $$
  \begin{aligned}
  \text{Efficiency Target} = \min\Bigg(&\text{Average Fuel Efficiency} \times \text{Max Efficiency}, \\
  &\text{Average Fuel Efficiency} \times \left(1 + (\text{Max Efficiency} - 1) \times \frac{\text{Cost Pressure on Efficiency}}{\text{Cost Pressure on Efficiency} + \text{Cost Pressure at Max Improvement}}\right)\Bigg)
  \end{aligned}
  $$
- **Units:** `km/liter`
- **Description:** The desired long-run fuel efficiency level.

## Carbon Intensity

This subsystem represents how carbon tax policy gradually reduces the carbon intensity (CI) of fuel through a delayed technological and supply-chain adjustment process.

### Carbon Intensity of Fuel (Stock)

- **Equation:**
  $$
  \text{Carbon Intensity of Fuel} = \text{INTEG}(\text{CI Adjustment}, \text{Baseline CI})
  $$
- **Units:** `tCO2/liter`
- **Description:** The carbon intensity of fuel, modeled as a stock that changes gradually over time. It represents the combined effects of refinery improvements, low-carbon fuel blending, and technological shifts in fuel supply.

### CI Adjustment (Flow)

- **Equation:**
  $$
  \text{CI Adjustment} = \frac{\text{Target Carbon Intensity} - \text{Carbon Intensity of Fuel}}{\text{Tau CI}}
  $$
- **Units:** `tCO2/liter/month`
- **Description:** The rate at which carbon intensity transitions toward its target level.
The adjustment is smoother and slower than policy changes, reflecting real-world behaviour in fuel production.

### Target Carbon Intensity

- **Equation:**
  $$
  \text{Target Carbon Intensity} = \text{Baseline CI} \times \left(1 - \text{Max Reduction CI} \times \min\left(1, \frac{\text{Carbon Tax Rate}}{\text{Carbon Tax at Full CI Reduction}}\right)\right)
  $$
- **Units:** `tCO2/liter`
- **Description:** The policy-determined desired carbon intensity. It decreases linearly with carbon tax rate until reaching its maximum feasible reduction fraction, representing the incentive for refineries and the energy sector to adopt lower-carbon fuel pathways.

## Emissions & Consumption

This subsystem converts freight activity and fuel efficiency into fuel consumption and greenhouse gas emissions.

### Fuel Consumption

- **Equation:**
  $$
  \text{Fuel Consumption} = \frac{\text{Freight Activity}}{\text{Average Fuel Efficiency}}
  $$
- **Units:** `liter/month`
- **Description:** Total monthly fuel use. Higher freight activity increases consumption, while improvements in average fuel efficiency reduce it.

### Emissions

- **Equation:**
  $$
  \text{Emissions} = \text{Fuel Consumption} \times \text{Carbon Intensity of Fuel}
  $$
- **Units:** `tCO2/month`
- **Description:** Monthly CO2 emissions from heavy-duty vehicle operations. Emissions depend on how much fuel is used and how carbon-intensive the fuel is.

### Cumulative Emissions

- **Equation:**
  $$
  \text{Cumulative CO2} = \text{INTEG}(\text{Emissions}, 0)
  $$
- **Units:** `tCO2`
- **Description:** The total emissions over the simulation horizon, integrated from zero.

## Profit & Viability

This subsystem represents the economic performance of freight operators and determines whether they remain financially viable under different carbon tax levels.

### Revenue

- **Equation:**
  $$
  \text{Revenue} = \text{Freight Activity} \times \text{Perceived Freight Price}
  $$
- **Units:** `¥/month`
- **Description:** Total monthly revenue received by operators.

### Operating Expenses

- **Equation:**
  $$
  \text{Operating Expenses} = \text{Freight Activity} \times \text{Operating Cost per km}
  $$
- **Units:** `¥/month`
- **Description:** Total operating costs for performing freight activity.

### Profit

- **Equation:**
  $$
  \text{Profit} = \text{Revenue} - \text{Operating Expenses}
  $$
- **Units:** `¥/month`
- **Description:** Monthly profit earned by freight operators.

### Margin

- **Equation:**
  $$
  \text{Margin} = \frac{\text{Profit}}{\text{Revenue}}
  $$
- **Units:** `dimensionless`
- **Description:** Profit margin expressed as a share of revenue.

### Rolling Margin

- **Equation:**
  $$
  \text{Rolling Margin} = \text{SMOOTH}(\text{Margin}, \text{Tau}_m)
  $$
- **Units:** `dimensionless`
- **Description:** A smoothed version of the margin, representing a moving-average perception of profitability and reflecting how operators perceive their own financial condition with delay, rather than reacting instantly to monthly fluctuations.

### Duration Below Margin Threshold (Stock)

- **Equation:**
  $$
  \text{Duration Below Margin Threshold} = \text{INTEG}\left(
    \text{IF THEN ELSE}(\text{Rolling Margin} < \text{Margin Threshold}, 1, 0),
    0
  \right)
  $$
- **Units:** `months`
- **Description:** Accumulates the number of months during which profitability has been below the acceptable threshold.

### Cumulative Profit

- **Equation:**
  $$
  \text{Cumulative Profit} = \text{INTEG}(\text{Profit}, 0)
  $$
- **Units:** `¥`
- **Description:** The accumulated profit across the simulation period.

### Viability Flag

- **Equation:**
  $$
  \text{Viability Flag} = \text{IF THEN ELSE}\left(
    (\text{Duration Below Margin Threshold} > \text{Duration Threshold}) \text{ OR } (\text{Cumulative Profit} < 0),
    0,
    1
  \right)
  $$
- **Units:** `dimensionless`
- **Description:** A binary flag indicating system viability (1 = viable, 0 = not viable). The system is not viable if margin has been below threshold for too long or if cumulative profit is negative.
