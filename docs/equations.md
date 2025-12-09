# Equation Documentation

Documentation of all equations used in the system dynamics model, grouped by subsystem.

## Fuel Price & Operating Cost

This subsystem determines how fuel price, driven by pre-tax fuel price and carbon tax rate, affects operating cost and freight price. This structure connects carbon policy to economic impacts on operators.

### Fuel Price

- **Equation:** Fuel Price = Pretax Fuel Price + Tax per Liter
- **Units:** `¥/liter`
- **Description:** Market fuel price that freight operators pay.

### Tax per Liter

- **Equation:** Tax per Liter = Carbon Tax Rate * Carbon Content of Fuel
- **Units:** `¥/liter`
- **Description:** Converts a carbon tax (¥/tCO2) to a fuel-tax amount per liter.

### Fuel Cost per km

- **Equation:** Fuel Cost per km = (Fuel Price) / (Average Fuel Efficiency)
- **Units:** `¥/km`
- **Description:** Fuel portion of per-km operating cost.

### Baseline Fuel Cost per km

- **Equation:** Baseline Fuel Cost per km = (Pre-Tax Fuel Price) / (Baseline Fuel Efficiency)
- **Units:** `¥/km`
- **Description:** Reference-level fuel cost before carbon tax is applied.

### Extra Fuel Cost per km

- **Equation:** Extra Fuel Cost per km = Fuel Cost per km - Baseline Fuel Cost per km
- **Units:** `¥/km`
- **Description:** The incremental fuel cost arising from the carbon tax. This is the cost component that operators try to pass through to customers.

### Operating Cost per km

- **Equation:** Operating Cost per km = Non-Fuel Cost per km + Fuel Cost per km
- **Units:** `¥/km`
- **Description:** Total per-km operating cost of freight movement.

### Baseline Operating Cost per km

- **Equation:** Baseline Operating Cost per km = Non-Fuel Cost per km + Baseline Fuel Cost per km
- **Units:** `¥/km`
- **Description:** Normal operating cost before carbon tax.

### Baseline Margin per km

- **Equation:** Baseline Margin per km = Baseline Price Margin * Baseline Operating Cost per km
- **Units:** `¥/km`
- **Description:** The additional baseline margin per km used to construct the freight price.

### Actual Freight Price

- **Equation:** Actual Freight Price = Baseline Freight Price + Effective Pass-Through Share * Extra Fuel Cost per km
- **Units:** `¥/tkm`
- **Description:** The actual freight price operators set immediately, accounting for the incremental cost increase from the tax.

### Perceived Freight Price

- **Equation:** Perceived Freight Price = SMOOTH(Actual Freight Price, Tau_p)
- **Units:** `¥/tkm`
- **Description:** The price customers believe they pay, adjusting gradually to actual price changes. Used to determine demand elasticities.

### Baseline Freight Price

- **Equation:** Baseline Freight Price = Baseline Operating Cost per km + Baseline Margin per km
- **Units:** `¥/tkm`
- **Description:** The freight price before carbon tax policy is applied. Used as the reference point for price changes and elasticity calculations.

### Effective Pass-Through Share

- **Equation:** Effective Pass-Through Share = SMOOTH(Desired Pass-Through Share, Tau_p)
- **Units:** `dimensionless`
- **Description:** A delayed adjustment toward the target pass-through share. This avoids instant jumps in pricing behaviour.

## Freight Demand & Activity

Models customer demand response to freight price changes through short- and long-run elasticities and delays.

### Freight Demand

- **Equation:** Freight Demand = Underlying Freight Activity + Short-Run Price Effect on Demand + Long-Run Price Effect on Demand
- **Units:** `tkm/month`
- **Description:** Total freight demand after incorporating short‐run and long‐run adjustments to price. Underlying Activity represents the baseline level of freight movement, while the price effects adjust demand in response to perceived freight prices.

### Short-Run Price Effect on Demand

- **Equation:** Short-Run Price Effect on Demand = SMOOTH(Underlying Freight Activity * (Perceived Freight Price / Baseline Freight Price) ^ Elasticity SR - Underlying Freight Activity, Tau SR)
- **Units:** `tkm/month`
- **Description:** Short-run (immediate) demand response to price changes. This uses the short-run price elasticity and a short adjustment delay. The smoothing prevents unrealistic instantaneous changes in demand.

### Long-Run Price Effect on Demand

- **Equation:** Long-Run Price Effect on Demand = SMOOTH(Underlying Freight Activity * (Perceived Freight Price / Baseline Freight Price) ^ Elasticity LR - Underlying Freight Activity, Tau LR)
- **Units:** `tkm/month`
- **Description:** Long-run demand response to price changes, using a larger elasticity and a slower adjustment. Represents structural/logistical adjustments: route changes, alternative modes, etc.

### Underlying Freight Activity (Stock)

- **Equation:** Underlying Freight Activity = INTEG(Freight Activity Growth Rate * Underlying Freight Activity, Baseline Demand)
- **Units:** `tkm/month`
- **Description:** Baseline structural freight movement. This represents underlying macroeconomic demand for freight independent of price effects.

### Freight Activity

- **Equation:** Freight Activity = Freight Demand
- **Units:** `tkm/month`
- **Description:** The actual freight activity, equal to freight demand in this model because short-run supply is highly elastic.

## Fuel Efficiency

Models how operator fuel efficiency improves as fuel costs increases with tax.

### Average Fuel Efficiency (Stock)

- **Equation:** Average Fuel Efficiency = INTEG(Improvement - Degradation, Baseline Fuel Efficiency)
- **Units:** `km/liter`
- **Description:** The average fuel efficiency of the fleet, a stock that increases through improvement and decreases through degradation.

### Improvement (Flow)

- **Equation:** Improvement = (Efficiency Target - Average Fuel Efficiency) / (Tau Eff)
- **Units:** `km/liter/month`
- **Description:** The rate of fuel efficiency improvement, proportional to the gap between target and current efficiency, with adjustment time Tau Eff.

### Degradation (Flow)

- **Equation:** Degradation = Average Fuel Efficiency * Degradation Rate
- **Units:** `km/liter/month`
- **Description:** The rate of fuel efficiency degradation, proportional to current efficiency and the degradation rate.

### Cost Pressure on Efficiency

- **Equation:** Cost Pressure on Efficiency = Cost Pressure Sensitivity * ((Fuel Cost per km) / (Baseline Fuel Cost per km) - 1)
- **Units:** `dimensionless`
- **Description:** The pressure to improve efficiency based on increased fuel costs relative to baseline, scaled by sensitivity parameter.

### Efficiency Target

- **Equation:** Efficiency Target = MIN(Average Fuel Efficiency * Max Efficiency, Average Fuel Efficiency * (1 + (Max Efficiency - 1) * Cost Pressure on Efficiency / (Cost Pressure on Efficiency + Cost Pressure at Max Improvement)))
- **Units:** `km/liter`
- **Description:** The desired long-run fuel efficiency level.

## Carbon Intensity

This subsystem represents how carbon tax policy gradually reduces the carbon intensity (CI) of fuel through a delayed technological and supply-chain adjustment process.

### Carbon Intensity of Fuel (Stock)

- **Equation:** Carbon Intensity of Fuel = INTEG(CI Adjustment, Baseline CI)
- **Units:** `tCO2/liter`
- **Description:** The carbon intensity of fuel, modeled as a stock that changes gradually over time. It represents the combined effects of refinery improvements, low-carbon fuel blending, and technological shifts in fuel supply.

### CI Adjustment (Flow)

- **Equation:** CI Adjustment = (Target Carbon Intensity - Carbon Intensity of Fuel) / (Tau CI)
- **Units:** `tCO2/liter/month`
- **Description:** The rate at which carbon intensity transitions toward its target level.
The adjustment is smoother and slower than policy changes, reflecting real-world behaviour in fuel production.

### <span style="color:yellow">MODIFIED: Target Carbon Intensity</span>

- **Equation:** Target Carbon Intensity = Baseline CI * (1 - Max Reduction CI * (1 - EXP(- Carbon Tax Rate)))
- **Units:** `tCO2/liter`
- **Description:** *TODO*

## Emissions & Consumption

This subsystem converts freight activity and fuel efficiency into fuel consumption and greenhouse gas emissions.

### Fuel Consumption

- **Equation:** Fuel Consumption = (Freight Activity) / (Average Fuel Efficiency)
- **Units:** `liter/month`
- **Description:** Total monthly fuel use. Higher freight activity increases consumption, while improvements in average fuel efficiency reduce it.

### Emissions

- **Equation:** Emissions = Fuel Consumption * Carbon Intensity of Fuel
- **Units:** `tCO2/month`
- **Description:** Monthly CO2 emissions from heavy-duty vehicle operations. Emissions depend on how much fuel is used and how carbon-intensive the fuel is.

### Cumulative Emissions

- **Equation:** Cumulative CO2 = INTEG(Emissions, 0)
- **Units:** `tCO2`
- **Description:** The total emissions over the simulation horizon, integrated from zero.

## Profit & Viability

This subsystem represents the economic performance of freight operators and determines whether they remain financially viable under different carbon tax levels.

### Revenue

- **Equation:** Revenue = Freight Activity * Perceived Freight Price
- **Units:** `¥/month`
- **Description:** Total monthly revenue received by operators.

### Operating Expenses

- **Equation:** Operating Expenses = Freight Activity * Operating Cost per km
- **Units:** `¥/month`
- **Description:** Total operating costs for performing freight activity.

### Profit

- **Equation:** Profit = Revenue - Operating Expenses
- **Units:** `¥/month`
- **Description:** Monthly profit earned by freight operators.

### Margin

- **Equation:** Margin = (Profit) / (Revenue)
- **Units:** `dimensionless`
- **Description:** Profit margin expressed as a share of revenue.

### Rolling Margin

- **Equation:** Rolling Margin = SMOOTH(Margin, Tau_m)
- **Units:** `dimensionless`
- **Description:** A smoothed version of the margin, representing a moving-average perception of profitability and reflecting how operators perceive their own financial condition with delay, rather than reacting instantly to monthly fluctuations.

### Duration Below Margin Threshold (Stock)

- **Equation:** Duration Below Margin Threshold = INTEG( IF THEN ELSE(Rolling Margin < Margin Threshold, 1, 0), 0 )
- **Units:** `months`
- **Description:** Accumulates the number of months during which profitability has been below the acceptable threshold.

### Cumulative Profit

- **Equation:** Cumulative Profit = INTEG(Profit, 0)
- **Units:** `¥`
- **Description:** The accumulated profit across the simulation period.

### Viability Flag

- **Equation:** Viability Flag = IF THEN ELSE( (Duration Below Margin Threshold > Duration Threshold) OR (Cumulative Profit < 0), 0, 1 )
- **Units:** `dimensionless`
- **Description:** A binary flag indicating system viability (1 = viable, 0 = not viable). The system is not viable if margin has been below threshold for too long or if cumulative profit is negative.
