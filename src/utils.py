"""
Utility functions used across multiple notebooks.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml
from pathlib import Path
from typing import Dict, List

def calculate_max_viable_tax(model, params, tax_range=None, final_time=120):
    """
    Find the highest carbon tax where viability_flag stays 1 over the simulation period.
    Uses binary search for efficiency.
    """
    params_zero = params.copy()
    params_zero["carbon_tax_rate"] = 0
    result_zero = model.run(
        params=params_zero,
        return_columns=["viability_flag"]
    )
    if not (result_zero["viability_flag"] == 1).all():
        return 0
    
    if tax_range is None:
        tax_range = (0, 30000)  # Start with a reasonable range
    
    low, high = tax_range
    best_tax = 0
    params_mid = params.copy()

    # Binary search for max viable tax
    while high - low > 100:  # Stop when range is small enough
        mid = (low + high) // 2
        params_mid["carbon_tax_rate"] = mid
        result = model.run(
            params=params_mid,
            return_columns=["viability_flag"]
        )
        
        # Check if viability stays 1 throughout
        if (result["viability_flag"] == 1).all():
            best_tax = mid
            low = mid
        else:
            high = mid
    
    params_tax = params.copy()
    # Fine-tune in the final range
    for tax in range(int(low), int(high) + 1, 100):
        params_tax["carbon_tax_rate"] = tax
        result = model.run(
            params=params_tax,
            return_columns=["viability_flag"]
        )
        if (result["viability_flag"] == 1).all():
            best_tax = tax
        else:
            break
    
    return best_tax

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

def create_tornado_chart_on_axis(ax, df, tax_level, output_var):    
    """
    Create a tornado chart on a given axis.
    """
    # Filter data for this tax level
    tax_data = df[df['tax'] == tax_level].copy()
    
    # Calculate range (min to max) for each parameter
    tornado_data = []
    for param_name in tax_data['param_name'].unique():
        param_data = tax_data[tax_data['param_name'] == param_name][output_var]
        min_val = param_data.min()
        max_val = param_data.max()
        range_val = max_val - min_val
        
        tornado_data.append({
            'param_name': param_name,
            'min': min_val,
            'max': max_val,
            'range': abs(range_val),
            'center': (min_val + max_val) / 2
        })
    
    tornado_df = pd.DataFrame(tornado_data)
    # Sort by range (magnitude of impact)
    tornado_df = tornado_df.sort_values('range', ascending=True)
    
    y_pos = np.arange(len(tornado_df))
    
    # Plot bars from center to min and max
    for i, row in enumerate(tornado_df.itertuples()):
        # Bar from center to min (negative impact)
        if row.min < row.center:
            ax.barh(i, row.center - row.min, left=row.min, 
                   color='lightcoral', alpha=0.7)
        # Bar from center to max (positive impact)
        if row.max > row.center:
            ax.barh(i, row.max - row.center, left=row.center,
                   color='lightblue', alpha=0.7)
        # If min > center, draw full bar
        if row.min >= row.center:
            ax.barh(i, row.max - row.min, left=row.min,
                   color='lightgreen', alpha=0.7)
    
    # Add vertical line at center (baseline)
    ax.axvline(x=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    
    # Set y-axis labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tornado_df['param_name'], fontsize=8)
    ax.invert_yaxis()  # Top to bottom
    
    # Labels
    ax.set_xlabel(f'{output_var.replace("_", " ").title()}', fontsize=9)
    ax.set_title(f'Tax: {tax_level:.0f} ¥/tCO₂', fontsize=10)
    ax.grid(axis='x', alpha=0.3)
    
    return ax
