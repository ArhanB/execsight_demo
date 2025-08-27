import streamlit as st
import pandas as pd
from predictor import train_model, predict_ratio

def dashboard(df):
    st.title("📊 ExecSight Dashboard Sample")
    st.markdown("**Labor Cost % of Revenue Monitoring**")

    # Overall KPI
    latest_month = df["month"].max()
    latest_df = df[df["month"] == latest_month]
    overall_cost = latest_df["labor_cost"].sum()
    overall_rev = latest_df["revenue"].sum()
    overall_ratio = overall_cost / overall_rev

    st.metric(label=f"Overall Labor Cost % of Revenue ({latest_month.strftime('%b %Y')})",
              value=f"{overall_ratio:.1%}")

    if overall_ratio > 0.50:
        st.error(f"⚠️ ALERT: Overall labor cost is {overall_ratio:.1%} of revenue — above 50% threshold!")

    # BU Breakdown
    st.subheader("Business Unit Breakdown")
    bu_table = latest_df[["business_unit","labor_cost","revenue","labor_cost_%_of_rev"]] \
                 .round(2).set_index("business_unit")
    st.dataframe(bu_table)

    for bu, row in bu_table.iterrows():
        if row["labor_cost_%_of_rev"] > 60:
            st.warning(f"⚠️ {bu}: Labor cost is {row['labor_cost_%_of_rev']:.1f}% of revenue (above 60% threshold).")

    # Trend Charts
    st.subheader("Trend Over Time")
    bu_choice = st.selectbox("Choose Business Unit", df["business_unit"].unique())
    bu_df = df[df["business_unit"] == bu_choice]
    st.markdown("**Graph showing Labor Cost and Revenue Over Time**")
    st.line_chart(bu_df.set_index("month")[["labor_cost", "revenue"]])
    st.markdown("**Graph showing Labor Cost % of Revenue Over Time**")
    st.line_chart(bu_df.set_index("month")[["labor_cost_%_of_rev"]])

    # Prediction Section
    st.subheader("🔮 Predict Labor Cost % of Revenue")
    model, df_model = train_model(df)
    future_date = st.date_input("Select a future date to predict")

    if future_date:
        pred_ratio = predict_ratio(model, df_model, future_date)
        if pred_ratio > 0.50:
            st.error(f"⚠️ Predicted labor cost is {pred_ratio:.1%} of revenue for {future_date.strftime('%b %Y')} — above 50% threshold!")
        else:
            st.success(f"Predicted labor cost is {pred_ratio:.1%} of revenue for {future_date.strftime('%b %Y')}")
