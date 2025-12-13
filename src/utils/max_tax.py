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