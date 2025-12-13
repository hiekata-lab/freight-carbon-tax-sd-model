import pandas as pd

def one_at_a_time_sensitivity_analysis(model, params, key_params, tax_levels):
    """
    Perform a one-at-a-time sensitivity analysis.
    """
    results = []
    baseline_result = model.run(params=params, return_columns=["cumulative_co2", "cumulative_profit", "viability_flag"])
    co2_base = baseline_result["cumulative_co2"].iloc[-1]
    profit_base = baseline_result["cumulative_profit"].iloc[-1]

    for param_name, param_values in key_params.items():
        for param_value in param_values:
            params[param_name] = param_value
            for tax in tax_levels:
                params["carbon_tax_rate"] = tax
                result = model.run(params=params, return_columns=["cumulative_co2", "cumulative_profit", "viability_flag"])
                co2 = result["cumulative_co2"].iloc[-1]
                profit = result["cumulative_profit"].iloc[-1]
                co2_reduction_pct = 100 * (1 - co2 / co2_base)
                profit_change_pct = 100 * (profit - profit_base) / profit_base
                results.append({
                    "param_name": param_name,
                    "param_value": param_value,
                    "tax": tax,
                    "co2_reduction_pct": co2_reduction_pct,
                    "profit_change_pct": profit_change_pct,
                    "viable": result["viability_flag"].iloc[-1]
                })
    return pd.DataFrame(results)