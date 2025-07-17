# mmm_app_with_target.py

import streamlit as st
import pandas as pd
import plotly.express as px
from meridian_model_template import run_meridian_model

st.set_page_config(page_title="AI MMM Tool", layout="centered")
st.title("📊 AI MMM Tool (With Revenue Target)")

uploaded_file = st.file_uploader("Upload Your Campaign Data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File Uploaded Successfully")
    st.dataframe(df.head())

    expected_media_cols = [
        "TV Spend", "Print Spend", "Outdoor Spend", "Cinema Spend",
        "YouTube Spend", "FacebookAds Spend", "GoogleAds Spend",
        "Programmatic Spend", "RegionalPrint Spend", "RegionalOutdoor Spend",
        "RegionalDigital Spend", "RegionalRadio Spend", "GroundActivation Spend"
    ]

    media_cols = [col for col in expected_media_cols if col in df.columns]
    target = "revenue"

    if not media_cols:
        st.error("❌ No media spend columns found.")
    elif target not in df.columns:
        st.error("❌ 'revenue' column missing.")
    else:
        revenue_target = st.number_input("🎯 Enter Future Revenue Goal (INR)", min_value=0, step=10000)
        results = run_meridian_model(df, media_cols, target)

        st.subheader("📈 ROI Results")
        st.dataframe(results)

        if revenue_target > 0:
            total_contribution = results["normalized_contribution"].sum()
            df_budget = results.copy()
            df_budget["recommended_spend"] = df_budget["normalized_contribution"] * revenue_target

            st.subheader("📊 Budget Recommendation")
            st.dataframe(df_budget[["media_channel", "recommended_spend"]])

            st.download_button("📥 Download Budget CSV", df_budget.to_csv(index=False), "recommended_budget.csv")

        # Charts
        st.subheader("📉 ROI by Channel")
        st.plotly_chart(px.bar(results, x='media_channel', y='estimated_roi', color='media_channel'))

        st.subheader("📊 Contribution by Channel")
        st.plotly_chart(px.bar(results, x='media_channel', y='normalized_contribution', color='media_channel'))
