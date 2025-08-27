import pandas as pd
import numpy as np

def load_data():
    """
    For MVP: generate synthetic workforce cost + revenue data.
    Later: replace with CSV upload or system connectors.
    """
    np.random.seed(42)
    months = pd.date_range("2024-08-01", periods=6, freq="MS")
    business_units = ["North America Sales", "EMEA Sales", "Customer Support"]

    rows = []
    for bu in business_units:
        base_cost = {"North America Sales": 4_800_000,
                     "EMEA Sales": 2_900_000,
                     "Customer Support": 2_500_000}[bu]
        base_rev = {"North America Sales": 12_000_000,
                    "EMEA Sales": 7_200_000,
                    "Customer Support": 3_500_000}[bu]
        for i, m in enumerate(months):
            labor_cost = base_cost * (1 + 0.01*i) + np.random.normal(0, 30_000)
            revenue = base_rev * (1 + 0.015*i) + np.random.normal(0, 100_000)
            rows.append({
                "month": m,
                "business_unit": bu,
                "labor_cost": max(0, labor_cost),
                "revenue": max(0, revenue)
            })
    df = pd.DataFrame(rows)
    return df
