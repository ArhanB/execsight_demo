import pandas as pd
from sklearn.linear_model import LinearRegression

def train_model(df):
    """Train a simple linear regression model for labor cost % of revenue."""
    df_model = df.copy()
    df_model["month_num"] = (df_model["month"] - df_model["month"].min()).dt.days // 30

    agg_df = df_model.groupby("month_num").agg({
        "labor_cost": "sum",
        "revenue": "sum"
    }).reset_index()
    agg_df["ratio"] = agg_df["labor_cost"] / agg_df["revenue"]

    X = agg_df[["month_num"]].values
    y = agg_df["ratio"].values
    model = LinearRegression().fit(X, y)
    return model, df_model

def predict_ratio(model, df_model, future_date):
    """Predict ratio for a given date."""
    month_num = (pd.to_datetime(future_date) - df_model["month"].min()).days // 30
    pred_ratio = model.predict([[month_num]])[0]
    return pred_ratio
