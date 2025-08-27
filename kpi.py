import numpy as np

def compute_kpis(df):
    df["labor_cost_%_of_rev"] = np.where(df["revenue"] > 0,
                                         df["labor_cost"] * 100 / df["revenue"], np.nan)
    return df
