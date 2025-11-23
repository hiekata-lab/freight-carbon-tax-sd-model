# Parameter Documentation

Documentation of all parameters used in the system dynamics model, grouped by subsystem.

## Carbon Intensity

Describes how the carbon intensity (CI) of fuel responds to carbon pricing and decarbonisation limits.

### Baseline CI

- **Value:** `0.00268`
- **Units:** `tCO2/liter`
- **Description:**  Initial carbon intensity of diesel fuel based on UNEP guidelines [[1]](#ref1).

### Max Reduction CI

- **Value:** `0.45`
- **Units:** `fraction`
- **Description:**  Maximum feasible fractional reduction in CI over 10 years under strong policy, calibrated to match EU heavy-duty vehicle CO2 standards [[2]](#ref2).

### Carbon Tax at Full CI Reduction

- **Value:** `40000`
- **Units:** `¥/tCO2`
- **Description:** Carbon tax level required to activate the maximum CI reduction potential, calibrated from observed findings of studies [[3]](#ref3) [[4]](#ref4).

### Tau CI

- **Value:** `120`
- **Units:** `months`
- **Description:** Time constant for slow CI adjustment due to fuel supply and infrastructure changes.

## Fuel Efficiency

Controls how average fuel efficiency evolves due to cost pressure, operational improvements, and saturation limits.

### Baseline Fuel Efficiency

- **Value:** `2.84`
- **Units:** `km/liter`
- **Description:** Initial average fuel efficiency of the freight vehicle fleet, based on average fuel efficiency for heavy-duty trucks in Japan [[5]](#ref5).

### Max Efficiency

- **Value:** `1.25`
- **Units:** `multiplier`
- **Description:** Maximum allowable proportional improvement in fuel efficiency, calibrated from findings of fuel efficiency in heavy-duty vehicles study [[6]](#ref6).

### Cost Pressure Sensitivity

- **Value:** `0.2`
- **Units:** `dimensionless`
- **Description:** Scales how strongly changes in fuel cost create pressure for efficiency improvements, calibrated to be conservative.

### Cost Pressure at Max Improvement

- **Value:** `1`
- **Units:** `dimensionless`
- **Description:** Cost pressure level at which efficiency improvement approaches its maximum rate, calibrated to be conservative.

### Degradation Rate

- **Value:** `0`
- **Units:** `1/month`
- **Description:** Rate at which vehicles lose efficiency in the absence of improvements. The model doesn't consider any degradation of fuel efficiency in the current version.

### Tau Eff

- **Value:** `36`
- **Units:** `months`
- **Description:** Delay time for efficiency to adjust toward its target, calibrated so that most of the efficiency response to a cost signal emerges over a few years.

## Pricing

Controls fuelprice, freight rates, and rate adjustment dynamics.

### Desired Pass-Through Share

- **Value:** `0.5`
- **Units:** `fraction`
- **Description:** Intended share of additional fuel cost operators aim to pass through to customers, calibrated from IEA data on average pass-through of international oil price increases [[7]](#ref7).

### Tau p

- **Value:** `6`
- **Units:** `months`
- **Description:** Delay in adjustment of freight prices and pass-through behaviour, calibrated to represent contract durations an internalisation of new price levels times.

### Pre-Tax Fuel Price

- **Value:** `108`
- **Units:** `¥/liter`
- **Description:** Base fuel price excluding carbon taxation, calibrated from data on total fuel price, VAT and tax per liter [[8]](#ref8).

### Non-Fuel Cost per km

- **Value:** `90`
- **Units:** `¥/km`
- **Description:** Operating cost per kilometre excluding fuel, calibrated from findings on fuel share of operating cost in the Japanese trucking industry [[9]](#ref9).

## Freight Demand

Captures how shippers adjust demand in response to freight prices in the short and long run.

### Baseline Demand

- **Value:** `19000000000`
- **Units:** `tkm/month`
- **Description:** Estimated monthly tonne-kilometres transported in Japan, calibrated from the OECD's quarterly data on total road freight transport in Japan [[10]](#ref10).

### Elasticity SR

- **Value:** `-0.2`
- **Units:** `dimensionless`
- **Description:** Short-run price elasticity of freight demand, calibrated from literature on Price sensitivity of road freight transport [[11]](#ref11).

### Elasticity LR

- **Value:** `-0.6`
- **Units:** `dimensionless`
- **Description:** Long-run price elasticity of freight demand, calibrated from literature on Price sensitivity of road freight transport [[11]](#ref11).

### Tau SR

- **Value:** `3`
- **Units:** `months`
- **Description:** Adjustment time for short-run demand response, calibrated to match a quarterly planning horizon.

### Tau LR

- **Value:** `24`
- **Units:** `months`
- **Description:** Adjustment time for long-run demand response, calibrated so that structural adjustments to higher freight prices take several years to materialise.

### Freight Activity Growth Rate

- **Value:** `0`
- **Units:** `1/month`
- **Description:** Baseline growth in economic activity, set to zero in the current version.

## Financial Viability

Determines whether freight operators remain financially sustainable under different tax scenarios.

### Margin Threshold

- **Value:** `0.02`
- **Units:** `fraction`
- **Description:** Minimum profit margin required to be considered financially viable, calibrated to match the lower bound of ranges on trucking company profitability [[12]](#ref12).

### Duration Threshold

- **Value:** `6`
- **Units:** `months`
- **Description:** Maximum period allowable below the margin threshold before viability is lost.

### Tau m

- **Value:** `12`
- **Units:** `months`
- **Description:** Smoothing time for rolling financial margin evaluation, calibrated to represent an annual perspective on financial performance.

## Exogenous Policy Inputs

Scenario parameters that drive policy experiments.

### Carbon Tax Rate

- **Value:** `user-defined`
- **Units:** `¥/tCO2`
- **Description:** Carbon tax applied to fuel based on its carbon content.

## References

<a name="ref1"></a>[1] Charles Thomas, Tessa Tennant
and Jon Rolls. (2012). The GHG Indicator: UNEP Guidelines for Calculating Greenhouse Gas Emissions for Businesses and NonCommercial Organisations. [Link](https://www.uncclearn.org/wp-content/uploads/library/unep12.pdf)

<a name="ref2"></a>[2] Council of the EU. (2024). Heavy-duty vehicles: Council signs off on stricter CO2 emission standards. [Link](https://www.consilium.europa.eu/en/press/press-releases/2024/05/13/heavy-duty-vehicles-council-signs-off-on-stricter-co2-emission-standards/)

<a name="ref3"></a>[3] Kojima, S., et al. 2018. Choki teitanso bijon jitsugen ni muketa gurin zeisei kaikaku teian: Bakkukyasutingu ni motozuku seisaku hyoka no tekiyo (Proposal for Green Tax Reform to Realize a Long-term Low-Carbon Vision: Application of a Policy-Assessment Method Based on Backcasting). Kankyo Keizai Seisaku Kenkyu 11-2: 82-86. Accessed October 7, 2022. [Link](https://www.jstage.jst.go.jp/article/reeps/11/2/11_82/_pdf)

<a name="ref4"></a>[4] Suk, S.H., et al. 2022. "Carbon Market Linkage of China, Japan, and Korea and Its Decarbonization Impact on Economy and Environment: E3ME Application Case Study." Materials presented to the 11th Congress of the Asian Association of Environmental and Resource Economics, Ho Chi Minh City, August 12, 2022.

<a name="ref5"></a>[5] TransportPolicy.net. Heavy-Duty: Fuel Economy. [Link](https://www.transportpolicy.net/standard/japan-heavy-duty-fuel-economy/)

<a name="ref6"></a>[6] Delgado, Oscar & Rodriguez, Felipe & Muncrief, Rachel. (2017). Fuel efficiency technology in European heavy-duty vehicles: Baseline and potential for the 2020–2030 timeframe. Accessed November 23, 2025. [Link](https://www.researchgate.net/publication/318642247_Fuel_efficiency_technology_in_European_heavy-duty_vehicles_Baseline_and_potential_for_the_2020-2030_timeframe)

<a name="ref7"></a>[7] International Energy Agency (IEA). Proportion of transport fuel price increases passed through to consumers by region, Dec 2020 - Apr 2022. [Link](https://www.iea.org/data-and-statistics/charts/proportion-of-transport-fuel-price-increases-passed-through-to-consumers-by-region-dec-2020-apr-2022)

<a name="ref8"></a>[8] Ministry of the Environment, Japan. Automobile Tax System. [Link](https://www.env.go.jp/en/policy/tax/auto/ch8.html)

<a name="ref9"></a>[10] Han, Y., Kawasaki, T., & Hanaoka, S. (2022). The Benefits of Truck Platooning with an Increasing Market Penetration: A Case Study in Japan. Sustainability, 14(15), 9351. [Link](https://doi.org/10.3390/su14159351)

<a name="ref10"></a>[11] OECD. (2024). Total Road Freight Transport in Japan. Data accessed via CEIC database. [Link](https://www.ceicdata.com/en/japan/freight-transport-by-mode-of-transport-oecd-member-quarterly/jp-total-road-freight-transport-total)

<a name="ref11"></a>[12] De Jong, G., et al. Transport & Environment. (2010). Price Sensitivity of Road Freight Transport - Significance for Climate Policy. [Link](https://www.transportenvironment.org/uploads/files/2010_07_price_sensitivity_road_freight_significance_ce.pdf)

<a name="ref12"></a>[13] PCS Soft. (2025). Trucking Company Profit Margin: How to Boost Profitability. [Link](https://pcssoft.com/blog/trucking-company-profit-margin/)
