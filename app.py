import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="ACC102 Track 4: Financial Analyzer", layout="wide")

# Sidebar Navigation
with st.sidebar:
    st.title("🧭 Navigation Panel")
    st.markdown("---")
    st.markdown("### 📌 Menu")
    st.markdown("• Home & Inputs")
    st.markdown("• Financial Data")
    st.markdown("• Visualization")
    st.markdown("• Analysis Summary")
    st.markdown("---")
    st.info("ACC102 Track 4\nUS Stock Financial Analysis Tool")

# Main Title
st.markdown("# 📊 ACC102 Track 4: US Stock Financial Analyzer")
st.subheader("Interactive Financial Ratio & Trend Analysis (Built-in WRDS Data)")

# Year Selection (1990 - 2026)
st.markdown("#### ⚙️ Analysis Parameters")
start_year = st.number_input("Start Year", min_value=1990, max_value=2026, value=2000)
end_year = st.number_input("End Year", min_value=1990, max_value=2026, value=2025)

# Run Button
if st.button("🚀 Run Full Financial Analysis"):

    # AUTO LOAD CSV FROM YOUR REPOSITORY
    try:
        df = pd.read_csv("aapl.csv")
        st.success("✅ Built-in WRDS dataset loaded successfully!")
    except Exception as e:
        st.error(f"❌ Error loading CSV file: {e}")
        st.stop()

    # Validate required columns
    required = ["tic", "fyear", "at", "lt", "sale", "ni"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        st.error(f"❌ Missing columns: {missing}")
        st.stop()

    # Filter by year range
    df = df[(df["fyear"] >= start_year) & (df["fyear"] <= end_year)].copy()

    if df.empty:
        st.error("❌ No data available in selected year range.")
        st.stop()

    # Calculate financial ratios
    df["Total_Equity"] = df["at"] - df["lt"]
    df["ROE"] = (df["ni"] / df["Total_Equity"]).round(3)
    df["ROA"] = (df["ni"] / df["at"]).round(3)
    df["Debt_to_Asset"] = (df["lt"] / df["at"]).round(3)
    df["Net_Profit_Margin"] = (df["ni"] / df["sale"]).round(3)

    # Show Data Table
    st.subheader("📋 Financial Dataset & Calculated Ratios")
    st.dataframe(df, use_container_width=True)

    # Charts
    st.subheader("📈 Financial Trend Visualization")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.plot(df["fyear"], df["ROE"], marker="o", linewidth=3, label="ROE")
    ax1.plot(df["fyear"], df["ROA"], marker="s", linewidth=3, label="ROA")
    ax1.set_title("Profitability Trend (ROE & ROA)", fontsize=14)
    ax1.set_xlabel("Fiscal Year")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.bar(df["fyear"], df["Debt_to_Asset"], color="darkorange", alpha=0.75)
    ax2.set_title("Leverage Trend (Debt-to-Asset Ratio)", fontsize=14)
    ax2.set_xlabel("Fiscal Year")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

    # Summary
    st.subheader("📝 Financial Performance Summary")
    avg_roe = round(df["ROE"].mean() * 100, 2)
    avg_debt = round(df["Debt_to_Asset"].mean() * 100, 2)

    st.write(f"Average ROE: **{avg_roe}%**")
    st.write(f"Average Debt-to-Asset Ratio: **{avg_debt}%**")

    if avg_roe > 15:
        st.success("✅ Excellent long-term profitability.")
    elif avg_roe > 0:
        st.info("⚠️ Moderate and stable profitability.")
    else:
        st.warning("❌ Weak profitability over the period.")

    if avg_debt < 50:
        st.success("✅ Low financial leverage and low financial risk.")
    else:
        st.warning("⚠️ High debt level, increased financial risk.")