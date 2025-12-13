"""
Tax adjustment rule comparison utilities.

This module provides functions to compare adaptive tax trajectories against
static taxes at the time-averaged level.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Dict, Optional
from pysd.py_backend.output import ModelOutput


def compare_adaptive_tax_vs_static(
    model,
    base_params: Dict,
    tax_adjustment_func: Callable,
    return_columns: Optional[list] = None,
    final_time: int = 120,
    initial_tax: Optional[float] = None,
    **adjustment_kwargs
) -> Dict:
    """
    Compare an adaptive tax trajectory against a static tax at the time-averaged level.
    
    Parameters:
    -----------
    model : PySD model
        The loaded PySD model
    base_params : dict
        Base parameters for the model
    tax_adjustment_func : callable
        Function that determines the tax rate at each time step.
        Signature: tax_adjustment_func(t, current_tax, model_state, **kwargs) -> float
        where:
            t: current time step (0 to final_time-1)
            current_tax: current carbon tax rate
            model_state: dict with current model state (for rules 3 & 4)
            **kwargs: additional parameters for the adjustment rule
        Returns: new tax rate for next time step
    return_columns : list, optional
        Columns to return from model runs. Defaults to cumulative metrics.
    final_time : int
        Simulation length in months (default: 120)
    initial_tax : float, optional
        Starting tax rate. If None, uses base_params["carbon_tax_rate"]
    **adjustment_kwargs
        Additional keyword arguments passed to tax_adjustment_func
    
    Returns:
    --------
    dict with comparison results
    """
    if return_columns is None:
        return_columns = [
            "cumulative_co2",
            "cumulative_profit",
            "viability_flag"
        ]
    
    if initial_tax is None:
        initial_tax = base_params["carbon_tax_rate"]
    
    # Set up stepper for adaptive trajectory
    output = ModelOutput()
    model.set_stepper(
        output,
        step_vars=["carbon_tax_rate"],
        final_time=final_time,
    )
    
    # Run adaptive trajectory
    tax_rate_current = initial_tax
    tax_trajectory = []
    model_state = {}  # For rules that need model state (margin, emissions, etc.)
    
    for t in range(final_time):
        # Store current tax
        tax_trajectory.append(tax_rate_current)
        
        # Step the model with current tax
        model.step(1, {"carbon_tax_rate": tax_rate_current})
        
        # Get current model state by accessing variables directly
        # This allows the adjustment function to access current margin, emissions, etc.
        try:
            # Access model variables directly using component system
            model_state = {
                'time': t,
                'cumulative_co2': model.components.cumulative_co2(),
                'cumulative_profit': model.components.cumulative_profit(),
                'rolling_margin': model.components.rolling_margin(),
            }
        except (AttributeError, KeyError):
            # If direct access fails, provide empty state
            # Rules 1 & 2 don't need model state anyway
            model_state = {
                'time': t,
                'cumulative_co2': None,
                'cumulative_profit': None,
                'rolling_margin': None,
            }
        
        # Calculate next tax rate using the adjustment function
        tax_rate_current = tax_adjustment_func(
            t, 
            tax_rate_current, 
            model_state,
            **adjustment_kwargs
        )
    
    # Collect adaptive trajectory results (only after all steps are done)
    adaptive_results = output.collect(model)
    
    # Extract final values
    co2_adaptive = adaptive_results["Cumulative CO2"].iloc[-1]
    profit_adaptive = adaptive_results["Cumulative Profit"].iloc[-1]
    viability_adaptive = adaptive_results["Viability Flag"].iloc[-1]
    
    # Calculate time-averaged tax
    time_avg_tax = np.mean(tax_trajectory)
    
    # Run static tax at time-averaged level
    params_static = base_params.copy()
    params_static["carbon_tax_rate"] = time_avg_tax
    static_results = model.run(params=params_static, return_columns=return_columns)
    
    co2_static = static_results["cumulative_co2"].iloc[-1]
    profit_static = static_results["cumulative_profit"].iloc[-1]
    viability_static = static_results["viability_flag"].iloc[-1]
    
    # Calculate differences
    co2_diff = co2_adaptive - co2_static  # Negative means adaptive is better (lower CO2)
    profit_diff = profit_adaptive - profit_static  # Positive means adaptive is better (higher profit)
    
    # Pareto checks
    pareto_better = (co2_adaptive < co2_static) and (profit_adaptive > profit_static)
    pareto_worse = (co2_adaptive > co2_static) and (profit_adaptive < profit_static)
    
    # Create comparison DataFrame
    comparison_df = pd.DataFrame({
        "Metric": ["Cumulative CO2", "Cumulative Profit", "Viability", "Time-Averaged Tax"],
        "Adaptive": [
            co2_adaptive,
            profit_adaptive,
            viability_adaptive,
            time_avg_tax
        ],
        "Static": [
            co2_static,
            profit_static,
            viability_static,
            time_avg_tax
        ]
    })
    comparison_df["Absolute Difference"] = comparison_df["Adaptive"] - comparison_df["Static"]
    comparison_df["Relative Difference (%)"] = 100 * (
        comparison_df["Absolute Difference"] / comparison_df["Static"]
    )
    
    return {
        "tax_trajectory": tax_trajectory,
        "time_avg_tax": time_avg_tax,
        "adaptive_results": adaptive_results,
        "static_results": static_results,
        "co2_adaptive": co2_adaptive,
        "profit_adaptive": profit_adaptive,
        "viability_adaptive": viability_adaptive,
        "co2_static": co2_static,
        "profit_static": profit_static,
        "viability_static": viability_static,
        "co2_diff": co2_diff,
        "profit_diff": profit_diff,
        "co2_diff_pct": 100 * co2_diff / co2_static if co2_static != 0 else 0,
        "profit_diff_pct": 100 * profit_diff / profit_static if profit_static != 0 else 0,
        "pareto_better": pareto_better,
        "pareto_worse": pareto_worse,
        "comparison_df": comparison_df,
    }


# Example tax adjustment functions for the 4 rules:

def step_increase_rule(t: int, current_tax: float, model_state: Dict, 
                       step_size: float, max_tax: float, **kwargs) -> float:
    """
    Rule 1: Simple annual step increase.
    τ_{t+12} = min(τ_t + δ_step, τ_max)
    
    Parameters:
    -----------
    step_size : float
        Annual step increase (applied monthly, so divide by 12)
    max_tax : float
        Maximum tax cap
    """
    monthly_step = step_size / 12  # Convert annual to monthly
    return np.minimum(current_tax + monthly_step, max_tax)


def percentage_growth_rule(t: int, current_tax: float, model_state: Dict,
                           annual_growth_rate: float, **kwargs) -> float:
    """
    Rule 2: Percentage growth rule.
    τ_{t+12} = τ_t(1 + g)
    
    Parameters:
    -----------
    annual_growth_rate : float
        Annual growth rate (e.g., 0.1 for 10% per year)
    """
    monthly_growth = (1 + annual_growth_rate) ** (1/12)  # Convert annual to monthly
    return current_tax * monthly_growth


def margin_based_rule(t: int, current_tax: float, model_state: Dict,
                      target_margin: float, margin_band: float,
                      tax_increase: float, tax_decrease: float,
                      **kwargs) -> float:
    """
    Rule 3: Profit/margin-based rule.
    Raises tax when margin is high, lowers when margin is low.
    
    Note: This rule adjusts annually (every 12 months), not monthly.
    
    Parameters:
    -----------
    target_margin : float
        Target margin level (m*)
    margin_band : float
        Bandwidth around target margin
    tax_increase : float
        Tax increase when margin > target + band (applied annually)
    tax_decrease : float
        Tax decrease when margin < target - band (applied annually)
    """
    rolling_margin = model_state.get('rolling_margin')
    if rolling_margin is None:
        return current_tax  # Can't adjust without margin info
    
    # Only adjust annually (every 12 months)
    if t % 12 == 0 and t > 0:
        if rolling_margin > target_margin + margin_band:
            return current_tax + tax_increase
        elif rolling_margin < target_margin - margin_band:
            return max(0, current_tax - tax_decrease)  # Don't go negative
        else:
            return current_tax
    else:
        return current_tax


def emission_path_rule(t: int, current_tax: float, model_state: Dict,
                       target_emissions_func: Callable, emission_band: float,
                       tax_increase: float, tax_decrease: float,
                       **kwargs) -> float:
    """
    Rule 4: Emission-path-based rule.
    Adjusts tax based on deviation from target emission path.
    
    Note: This rule adjusts annually (every 12 months), not monthly.
    
    Parameters:
    -----------
    target_emissions_func : callable
        Function that returns target cumulative emissions at time t
        Signature: target_emissions_func(t) -> float
    emission_band : float
        Bandwidth around target emissions
    tax_increase : float
        Tax increase when emissions > target + band (applied annually)
    tax_decrease : float
        Tax decrease when emissions < target - band (applied annually)
    """
    cumulative_co2 = model_state.get('cumulative_co2')
    if cumulative_co2 is None:
        return current_tax  # Can't adjust without emission info
    
    # Only adjust annually (every 12 months)
    if t % 12 == 0 and t > 0:
        target_emissions = target_emissions_func(t)
        current_emissions = cumulative_co2
        
        if current_emissions > target_emissions + emission_band:
            return current_tax + tax_increase
        elif current_emissions < target_emissions - emission_band:
            return max(0, current_tax - tax_decrease)  # Don't go negative
        else:
            return current_tax
    else:
        return current_tax


def plot_comparison(result: Dict, rule_name: str = "Adaptive Tax", 
                    save_path: Optional[str] = None, figsize: tuple = (12, 10)) -> None:
    """
    Create a comprehensive comparison plot showing adaptive vs static tax trajectories.
    
    Parameters:
    -----------
    result : dict
        Result dictionary from compare_adaptive_tax_vs_static()
    rule_name : str
        Name of the tax adjustment rule (for title)
    save_path : str, optional
        Path to save the figure. If None, figure is not saved.
    figsize : tuple
        Figure size (width, height) in inches
    
    Returns:
    --------
    None (displays plot)
    """
    adaptive_results = result["adaptive_results"]
    static_results = result["static_results"]
    tax_trajectory = result["tax_trajectory"]
    time_avg_tax = result["time_avg_tax"]
    
    # Create figure with 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # 1. Cumulative CO2 trajectories
    axes[0, 0].plot(
        adaptive_results.index, 
        adaptive_results["Cumulative CO2"], 
        label="Adaptive", 
        linewidth=2
    )
    axes[0, 0].plot(
        static_results.index, 
        static_results["cumulative_co2"], 
        label="Static", 
        linewidth=2, 
        linestyle="--"
    )
    axes[0, 0].set_xlabel("Time (months)")
    axes[0, 0].set_ylabel("Cumulative CO₂")
    axes[0, 0].set_title("Cumulative CO₂ Comparison")
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)
    
    # 2. Cumulative Profit trajectories
    axes[0, 1].plot(
        adaptive_results.index, 
        adaptive_results["Cumulative Profit"], 
        label="Adaptive", 
        linewidth=2
    )
    axes[0, 1].plot(
        static_results.index, 
        static_results["cumulative_profit"], 
        label="Static", 
        linewidth=2, 
        linestyle="--"
    )
    axes[0, 1].set_xlabel("Time (months)")
    axes[0, 1].set_ylabel("Cumulative Profit")
    axes[0, 1].set_title("Cumulative Profit Comparison")
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    
    # 3. Tax rate over time
    axes[1, 0].plot(
        range(len(tax_trajectory)), 
        tax_trajectory, 
        label="Adaptive", 
        linewidth=2
    )
    axes[1, 0].axhline(
        time_avg_tax, 
        label="Static (Time-Averaged)", 
        linewidth=2, 
        linestyle="--", 
        color='orange'
    )
    axes[1, 0].set_xlabel("Time (months)")
    axes[1, 0].set_ylabel("Carbon Tax Rate (¥/tCO₂)")
    axes[1, 0].set_title("Tax Rate Comparison")
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3)
    
    # 4. CO2 difference over time
    co2_diff = adaptive_results["Cumulative CO2"].values - static_results["cumulative_co2"].values
    axes[1, 1].plot(
        static_results.index, 
        co2_diff, 
        linewidth=2, 
        color='red'
    )
    axes[1, 1].axhline(0, linestyle="--", color='gray', alpha=0.5)
    axes[1, 1].set_xlabel("Time (months)")
    axes[1, 1].set_ylabel("CO₂ Difference (Adaptive - Static)")
    axes[1, 1].set_title("CO₂ Difference Over Time")
    axes[1, 1].grid(alpha=0.3)
    
    # Add overall title
    fig.suptitle(f"{rule_name} vs Static Tax Comparison", fontsize=14, y=1.02)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()