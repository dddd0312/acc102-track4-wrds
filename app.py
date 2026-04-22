import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------- Side Navigation Panel -------------------
st.set_page_config(page_title="US Stock Financial Analysis", layout="wide")
with st.sidebar:
    st.title("🧭 Navigation Panel")
    st.markdown("---")
    st.markdown("### 📌 Menu")
    st.markdown("• Home & Inputs")
    st.markdown("• Financial Data")
    st.markdown("• Visualization")
    st.markdown("• Analysis Summary")
    st.markdown("---")
    st.info("ACC102 Track 4\nInteractive US Stock Analysis Tool")

# ------------------- Main Page -------------------
st.markdown("# 📊 ACC102 Track 4: WRDS US Stock Financial Analyzer")
st.subheader("Interactive Financial Ratio & Trend Analysis")

# ------------------- User Inputs -------------------
ticker = st.text_input("Stock Ticker (e.g. AAPL, MSFT, NVDA)", value="AAPL")
start_year = st.number_input("Start Year", min_value=2010, max_value=2025, value=2020)
end_year = st.number_input("End Year", min_value=2010, max_value=2025, value=2024)

# ------------------- Entry Protection -------------------
if st.button("🚀 Run Financial Analysis"):

    if start_year >= end_year:
        st.error("⚠️ End year must be later than start year!")
        st.stop()

    # Standard Financial Demo Dataset
    demo_data = {
        "Year": [2020, 2021, 2022, 2023, 2024],
        "Total_Assets": [323888, 351002, 352755, 352583, 382054],
        "Total_Liabilities": [258549, 287912, 302083, 290437, 309023],
        "Total_Revenue": [274515, 365817, 394328, 383285, 391035],
        "Net_Income": [57411, 94680, 99803, 96995, 97243],
        "Cash": [38329, 62741, 48022, 50816, 63592]
    }

    df = pd.DataFrame(demo_data)

    # Calculate Full Financial Ratios
    df["Equity"] = df["Total_Assets"] - df["Total_Liabilities"]
    df["ROE"] = (df["Net_Income"] / df["Equity"]).round(3)
    df["ROA"] = (df["Net_Income"] / df["Total_Assets"]).round(3)
    df["Debt_to_Asset_Ratio"] = (df["Total_Liabilities"] / df["Total_Assets"]).round(3)
    df["Net_Profit_Margin"] = (df["Net_Income"] / df["Total_Revenue"]).round(3)

    # Display Result Table
    st.subheader("📄 Financial Ratio Dataset")
    st.dataframe(df, use_container_width=True)

    # Draw Charts
    st.subheader("📈 Financial Trend Visualization")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.plot(df["Year"], df["ROE"], marker='o', linewidth=3, color='#2ecc71', label='ROE')
    ax1.plot(df["Year"], df["ROA"], marker='s', linewidth=3, color='#3498db', label='ROA')
    ax1.set_title("Profitability Trend Analysis", fontsize=14)
    ax1.set_xlabel("Year")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.bar(df["Year"], df["Debt_to_Asset_Ratio"], color='#e67e22', alpha=0.75)
    ax2.set_title("Leverage & Solvency Trend", fontsize=14)
    ax2.set_xlabel("Year")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

    # Auto Analysis Conclusion
    st.subheader("📝 Automated Performance Interpretation")
    avg_roe = round(df["ROE"].mean() * 100, 2)
    avg_debt = round(df["Debt_to_Asset_Ratio"].mean() * 100, 2)

    st.write(f"Average ROE (Return on Equity): **{avg_roe}%**")
    st.write(f"Average Debt-to-Asset Ratio: **{avg_debt}%**")

    if avg_roe > 20:
        st.success("✅ Excellent long-term profitability performance.")
    elif avg_roe > 10:
        st.info("⚠️ Stable and moderate profitability level.")
    else:
        st.warning("❌ Weak overall profitability.")

    if avg_debt < 50:
        st.success("✅ Low financial leverage, very low bankruptcy risk.")
    else:
        st.warning("⚠️ High debt ratio, relatively higher financial risk.")

st.caption("ACC102 Track 4 Final Interactive Financial Analysis Project")
