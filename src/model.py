"""
Python model 'model.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import Integ, Smooth
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 120,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="month",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(name="Tax Scale", comp_type="Constant", comp_subtype="Normal")
def tax_scale():
    return 3000


@component.add(
    name="Target Carbon Intensity",
    units="tCO2/liter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "baseline_ci": 1,
        "tax_scale": 1,
        "carbon_tax_rate": 1,
        "max_reduction_ci": 1,
    },
)
def target_carbon_intensity():
    return baseline_ci() * (
        1 - max_reduction_ci() * (1 - float(np.exp(-carbon_tax_rate() / tax_scale())))
    )


@component.add(
    name="Baseline Margin",
    units="fraction",
    comp_type="Constant",
    comp_subtype="Normal",
)
def baseline_margin():
    return 0.05


@component.add(
    name="Baseline Margin per km",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"baseline_margin": 1, "baseline_operating_cost_per_km": 1},
)
def baseline_margin_per_km():
    return baseline_margin() * baseline_operating_cost_per_km()


@component.add(
    name="Actual Freight Price",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "baseline_freight_price": 1,
        "effective_passthrough_share": 1,
        "extra_fuel_cost_per_km": 1,
    },
)
def actual_freight_price():
    return (
        baseline_freight_price()
        + effective_passthrough_share() * extra_fuel_cost_per_km()
    )


@component.add(
    name="Average Fuel Efficiency",
    units="km/l",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_average_fuel_efficiency": 1},
    other_deps={
        "_integ_average_fuel_efficiency": {
            "initial": {"baseline_fuel_efficiency": 1},
            "step": {"improvement": 1, "degradation": 1},
        }
    },
)
def average_fuel_efficiency():
    return _integ_average_fuel_efficiency()


_integ_average_fuel_efficiency = Integ(
    lambda: improvement() - degradation(),
    lambda: baseline_fuel_efficiency(),
    "_integ_average_fuel_efficiency",
)


@component.add(
    name="Baseline CI", units="tCO2/liter", comp_type="Constant", comp_subtype="Normal"
)
def baseline_ci():
    return 0.00268


@component.add(
    name="Baseline Demand",
    units="tkm/month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def baseline_demand():
    return 19 * float(np.power(10, 9))


@component.add(
    name="Baseline Freight Price",
    units="¥/tkm",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"baseline_operating_cost_per_km": 1, "baseline_margin_per_km": 1},
)
def baseline_freight_price():
    return baseline_operating_cost_per_km() + baseline_margin_per_km()


@component.add(
    name="Baseline Fuel Cost per km",
    units="¥/km",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pretax_fuel_price": 1, "baseline_fuel_efficiency": 1},
)
def baseline_fuel_cost_per_km():
    return pretax_fuel_price() / baseline_fuel_efficiency()


@component.add(
    name="Baseline Fuel Efficiency",
    units="km/liter",
    comp_type="Constant",
    comp_subtype="Normal",
)
def baseline_fuel_efficiency():
    return 2.84


@component.add(
    name="Baseline Operating Cost per km",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nonfuel_cost_per_km": 1, "baseline_fuel_cost_per_km": 1},
)
def baseline_operating_cost_per_km():
    return nonfuel_cost_per_km() + baseline_fuel_cost_per_km()


@component.add(
    name="Carbon Content of Fuel",
    units="tCO2/liter",
    comp_type="Constant",
    comp_subtype="Normal",
)
def carbon_content_of_fuel():
    return 0.00268


@component.add(
    name="Carbon Intensity of Fuel",
    units="tCO2/liter",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_carbon_intensity_of_fuel": 1},
    other_deps={
        "_integ_carbon_intensity_of_fuel": {
            "initial": {"baseline_ci": 1},
            "step": {"ci_adjustment": 1},
        }
    },
)
def carbon_intensity_of_fuel():
    return _integ_carbon_intensity_of_fuel()


_integ_carbon_intensity_of_fuel = Integ(
    lambda: ci_adjustment(), lambda: baseline_ci(), "_integ_carbon_intensity_of_fuel"
)


@component.add(
    name="Carbon Tax Rate", units="¥/tCO2", comp_type="Constant", comp_subtype="Normal"
)
def carbon_tax_rate():
    return 289


@component.add(
    name="CI Adjustment",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "target_carbon_intensity": 1,
        "carbon_intensity_of_fuel": 1,
        "tau_ci": 1,
    },
)
def ci_adjustment():
    return (target_carbon_intensity() - carbon_intensity_of_fuel()) / tau_ci()


@component.add(
    name="Cost Pressure at Max Improvement",
    units="dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def cost_pressure_at_max_improvement():
    return 1


@component.add(
    name="Cost Pressure on Efficiency",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cost_pressure_sensitivity": 1,
        "fuel_cost_per_km": 1,
        "baseline_fuel_cost_per_km": 1,
    },
)
def cost_pressure_on_efficiency():
    return cost_pressure_sensitivity() * (
        fuel_cost_per_km() / baseline_fuel_cost_per_km() - 1
    )


@component.add(
    name="Cost Pressure Sensitivity",
    units="—",
    comp_type="Constant",
    comp_subtype="Normal",
)
def cost_pressure_sensitivity():
    return 0.2


@component.add(
    name="Cumulative CO2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_co2": 1},
    other_deps={"_integ_cumulative_co2": {"initial": {}, "step": {"emissions": 1}}},
)
def cumulative_co2():
    return _integ_cumulative_co2()


_integ_cumulative_co2 = Integ(lambda: emissions(), lambda: 0, "_integ_cumulative_co2")


@component.add(
    name="Cumulative Profit",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_profit": 1},
    other_deps={"_integ_cumulative_profit": {"initial": {}, "step": {"profit": 1}}},
)
def cumulative_profit():
    return _integ_cumulative_profit()


_integ_cumulative_profit = Integ(
    lambda: profit(), lambda: 0, "_integ_cumulative_profit"
)


@component.add(
    name="Degradation",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_fuel_efficiency": 1, "degradation_rate": 1},
)
def degradation():
    return average_fuel_efficiency() * degradation_rate()


@component.add(
    name="Degradation Rate",
    units="1/month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def degradation_rate():
    return 0


@component.add(
    name='"Desired Pass-Through Share"',
    units="fraction",
    comp_type="Constant",
    comp_subtype="Normal",
)
def desired_passthrough_share():
    return 0.5


@component.add(
    name="Duration Below Margin Threshold",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_duration_below_margin_threshold": 1},
    other_deps={
        "_integ_duration_below_margin_threshold": {
            "initial": {},
            "step": {"rolling_margin": 1, "margin_threshold": 1},
        }
    },
)
def duration_below_margin_threshold():
    return _integ_duration_below_margin_threshold()


_integ_duration_below_margin_threshold = Integ(
    lambda: if_then_else(rolling_margin() < margin_threshold(), lambda: 1, lambda: 0),
    lambda: 0,
    "_integ_duration_below_margin_threshold",
)


@component.add(
    name="Duration Threshold",
    units="months",
    comp_type="Constant",
    comp_subtype="Normal",
)
def duration_threshold():
    return 6


@component.add(
    name='"Effective Pass-Through Share"',
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_effective_passthrough_share": 1},
    other_deps={
        "_smooth_effective_passthrough_share": {
            "initial": {"desired_passthrough_share": 1},
            "step": {"desired_passthrough_share": 1, "tau_p": 1},
        }
    },
)
def effective_passthrough_share():
    return _smooth_effective_passthrough_share()


_smooth_effective_passthrough_share = Smooth(
    lambda: desired_passthrough_share(),
    lambda: tau_p(),
    lambda: desired_passthrough_share(),
    lambda: 1,
    "_smooth_effective_passthrough_share",
)


@component.add(
    name="Efficiency Target",
    units="km/liter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_fuel_efficiency": 2,
        "max_efficiency": 2,
        "cost_pressure_on_efficiency": 2,
        "cost_pressure_at_max_improvement": 1,
    },
)
def efficiency_target():
    return float(
        np.minimum(
            average_fuel_efficiency() * max_efficiency(),
            average_fuel_efficiency()
            * (
                1
                + (max_efficiency() - 1)
                * (
                    cost_pressure_on_efficiency()
                    / (
                        cost_pressure_on_efficiency()
                        + cost_pressure_at_max_improvement()
                    )
                )
            ),
        )
    )


@component.add(
    name="Elasticity LR",
    units="dimensionless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def elasticity_lr():
    return -0.6


@component.add(
    name="Elasticity SR",
    units="dimensionless",
    comp_type="Constant",
    comp_subtype="Normal",
)
def elasticity_sr():
    return -0.2


@component.add(
    name="Emissions",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fuel_consumption": 1, "carbon_intensity_of_fuel": 1},
)
def emissions():
    return fuel_consumption() * carbon_intensity_of_fuel()


@component.add(
    name="Extra Fuel Cost per km",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fuel_cost_per_km": 1, "baseline_fuel_cost_per_km": 1},
)
def extra_fuel_cost_per_km():
    return fuel_cost_per_km() - baseline_fuel_cost_per_km()


@component.add(
    name="Freight Activity",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"freight_demand": 1},
)
def freight_activity():
    return freight_demand()


@component.add(
    name="Freight Activity Growth Rate",
    units="1/month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def freight_activity_growth_rate():
    return 0


@component.add(
    name="Freight Demand",
    units="tkm/month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "underlying_freight_activity": 1,
        "shortrun_price_effect_on_demand": 1,
        "longrun_price_effect_on_demand": 1,
    },
)
def freight_demand():
    return (
        underlying_freight_activity()
        + shortrun_price_effect_on_demand()
        + longrun_price_effect_on_demand()
    )


@component.add(
    name="Fuel Consumption",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"freight_activity": 1, "average_fuel_efficiency": 1},
)
def fuel_consumption():
    return freight_activity() / average_fuel_efficiency()


@component.add(
    name="Fuel Cost per km",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fuel_price": 1, "average_fuel_efficiency": 1},
)
def fuel_cost_per_km():
    return fuel_price() / average_fuel_efficiency()


@component.add(
    name="Fuel Price",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pretax_fuel_price": 1, "tax_per_liter": 1},
)
def fuel_price():
    return pretax_fuel_price() + tax_per_liter()


@component.add(
    name="Improvement",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"efficiency_target": 1, "average_fuel_efficiency": 1, "tau_eff": 1},
)
def improvement():
    return (efficiency_target() - average_fuel_efficiency()) / tau_eff()


@component.add(
    name='"Long-Run Price Effect on Demand"',
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_longrun_price_effect_on_demand": 1},
    other_deps={
        "_smooth_longrun_price_effect_on_demand": {
            "initial": {
                "underlying_freight_activity": 2,
                "perceived_freight_price": 1,
                "baseline_freight_price": 1,
                "elasticity_lr": 1,
            },
            "step": {
                "underlying_freight_activity": 2,
                "perceived_freight_price": 1,
                "baseline_freight_price": 1,
                "elasticity_lr": 1,
                "tau_lr": 1,
            },
        }
    },
)
def longrun_price_effect_on_demand():
    return _smooth_longrun_price_effect_on_demand()


_smooth_longrun_price_effect_on_demand = Smooth(
    lambda: underlying_freight_activity()
    * (perceived_freight_price() / baseline_freight_price()) ** elasticity_lr()
    - underlying_freight_activity(),
    lambda: tau_lr(),
    lambda: underlying_freight_activity()
    * (perceived_freight_price() / baseline_freight_price()) ** elasticity_lr()
    - underlying_freight_activity(),
    lambda: 1,
    "_smooth_longrun_price_effect_on_demand",
)


@component.add(
    name="Margin",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"profit": 1, "revenue": 1},
)
def margin():
    return profit() / revenue()


@component.add(
    name="Margin Threshold",
    units="fraction",
    comp_type="Constant",
    comp_subtype="Normal",
)
def margin_threshold():
    return 0.02


@component.add(
    name="Max Efficiency", units="—", comp_type="Constant", comp_subtype="Normal"
)
def max_efficiency():
    return 1.25


@component.add(
    name="Max Reduction CI",
    units="fraction",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_reduction_ci():
    return 0.45


@component.add(
    name='"Non-Fuel Cost per km"',
    units="¥/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def nonfuel_cost_per_km():
    return 90


@component.add(
    name="Operating Cost per km",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nonfuel_cost_per_km": 1, "fuel_cost_per_km": 1},
)
def operating_cost_per_km():
    return nonfuel_cost_per_km() + fuel_cost_per_km()


@component.add(
    name="Operating Expenses",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"freight_activity": 1, "operating_cost_per_km": 1},
)
def operating_expenses():
    return freight_activity() * operating_cost_per_km()


@component.add(
    name="Perceived Freight Price",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_perceived_freight_price": 1},
    other_deps={
        "_smooth_perceived_freight_price": {
            "initial": {"actual_freight_price": 1},
            "step": {"actual_freight_price": 1, "tau_p": 1},
        }
    },
)
def perceived_freight_price():
    return _smooth_perceived_freight_price()


_smooth_perceived_freight_price = Smooth(
    lambda: actual_freight_price(),
    lambda: tau_p(),
    lambda: actual_freight_price(),
    lambda: 1,
    "_smooth_perceived_freight_price",
)


@component.add(
    name='"Pre-Tax Fuel Price"',
    units="¥/liter",
    comp_type="Constant",
    comp_subtype="Normal",
)
def pretax_fuel_price():
    return 108


@component.add(
    name="Profit",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"revenue": 1, "operating_expenses": 1},
)
def profit():
    return revenue() - operating_expenses()


@component.add(
    name="Revenue",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"freight_activity": 1, "perceived_freight_price": 1},
)
def revenue():
    return freight_activity() * perceived_freight_price()


@component.add(
    name="Rolling Margin",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rolling_margin": 1},
    other_deps={
        "_smooth_rolling_margin": {
            "initial": {"margin": 1},
            "step": {"margin": 1, "tau_m": 1},
        }
    },
)
def rolling_margin():
    return _smooth_rolling_margin()


_smooth_rolling_margin = Smooth(
    lambda: margin(),
    lambda: tau_m(),
    lambda: margin(),
    lambda: 1,
    "_smooth_rolling_margin",
)


@component.add(
    name='"Short-Run Price Effect on Demand"',
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_shortrun_price_effect_on_demand": 1},
    other_deps={
        "_smooth_shortrun_price_effect_on_demand": {
            "initial": {
                "underlying_freight_activity": 2,
                "perceived_freight_price": 1,
                "baseline_freight_price": 1,
                "elasticity_sr": 1,
            },
            "step": {
                "underlying_freight_activity": 2,
                "perceived_freight_price": 1,
                "baseline_freight_price": 1,
                "elasticity_sr": 1,
                "tau_sr": 1,
            },
        }
    },
)
def shortrun_price_effect_on_demand():
    return _smooth_shortrun_price_effect_on_demand()


_smooth_shortrun_price_effect_on_demand = Smooth(
    lambda: underlying_freight_activity()
    * (perceived_freight_price() / baseline_freight_price()) ** elasticity_sr()
    - underlying_freight_activity(),
    lambda: tau_sr(),
    lambda: underlying_freight_activity()
    * (perceived_freight_price() / baseline_freight_price()) ** elasticity_sr()
    - underlying_freight_activity(),
    lambda: 1,
    "_smooth_shortrun_price_effect_on_demand",
)


@component.add(
    name="Tau CI", units="months", comp_type="Constant", comp_subtype="Normal"
)
def tau_ci():
    return 120


@component.add(
    name="Tau Eff", units="dimensionless", comp_type="Constant", comp_subtype="Normal"
)
def tau_eff():
    return 36


@component.add(
    name="Tau LR", units="months", comp_type="Constant", comp_subtype="Normal"
)
def tau_lr():
    return 24


@component.add(
    name="Tau m", units="months", comp_type="Constant", comp_subtype="Normal"
)
def tau_m():
    return 12


@component.add(
    name="Tau p", units="months", comp_type="Constant", comp_subtype="Normal"
)
def tau_p():
    return 6


@component.add(
    name="Tau SR", units="months", comp_type="Constant", comp_subtype="Normal"
)
def tau_sr():
    return 3


@component.add(
    name="Tax per Liter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"carbon_tax_rate": 1, "carbon_content_of_fuel": 1},
)
def tax_per_liter():
    return carbon_tax_rate() * carbon_content_of_fuel()


@component.add(
    name="Underlying Freight Activity",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_underlying_freight_activity": 1},
    other_deps={
        "_integ_underlying_freight_activity": {
            "initial": {"baseline_demand": 1},
            "step": {
                "freight_activity_growth_rate": 1,
                "underlying_freight_activity": 1,
            },
        }
    },
)
def underlying_freight_activity():
    return _integ_underlying_freight_activity()


_integ_underlying_freight_activity = Integ(
    lambda: freight_activity_growth_rate() * underlying_freight_activity(),
    lambda: baseline_demand(),
    "_integ_underlying_freight_activity",
)


@component.add(
    name="Viability Flag",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "duration_below_margin_threshold": 1,
        "duration_threshold": 1,
        "cumulative_profit": 1,
    },
)
def viability_flag():
    return if_then_else(
        np.logical_or(
            duration_below_margin_threshold() > duration_threshold(),
            cumulative_profit() < 0,
        ),
        lambda: 0,
        lambda: 1,
    )
