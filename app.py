import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Financial Analysis", layout="wide")

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
    st.info("ACC102 Track 4\nInteractive US Stock Analysis Tool")

# Main Page
st.title("📊 ACC102 Track 4: US Stock Financial Analyzer")
st.subheader("Interactive Financial Ratio & Trend Analysis")

# Inputs
ticker = st.text_input("Stock Ticker (e.g. AAPL)", value="AAPL")
start_year = st.number_input("Start Year", 2020, 2024, 2020)
end_year = st.number_input("End Year", 2020, 2024, 2024)

# Run Analysis
if st.button("🚀 Run Financial Analysis"):

    # Base demo dataset
    data = {
        "Year": [2020,2021,2022,2023,2024],
        "Assets": [323888,351002,352755,352583,382054],
        "Liabilities": [258549,287912,302083,290437,309023],
        "Revenue": [274515,365817,394328,383285,391035],
        "NetIncome": [57411,94680,99803,96995,97243]
    }

    df = pd.DataFrame(data)

    # Ratio Calculation
    df["Equity"] = df["Assets"] - df["Liabilities"]
    df["ROE"] = (df["NetIncome"] / df["Equity"]).round(3)
    df["ROA"] = (df["NetIncome"] / df["Assets"]).round(3)
    df["DebtRatio"] = (df["Liabilities"] / df["Assets"]).round(3)

    # Display
    st.subheader("📄 Financial Results Table")
    st.dataframe(df, use_container_width=True)

    # Chart
    st.subheader("📈 Trend Visualization")
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(14,5))

    ax1.plot(df["Year"], df["ROE"], marker="o", label="ROE")
    ax1.plot(df["Year"], df["ROA"], marker="s", label="ROA")
    ax1.set_title("Profitability Trend")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.bar(df["Year"], df["DebtRatio"], color="orange", alpha=0.7)
    ax2.set_title("Leverage Trend")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

    # Summary
    st.subheader("📝 Analysis Summary")
    avg_roe = round(df["ROE"].mean()*100,2)
    avg_debt = round(df["DebtRatio"].mean()*100,2)

    st.write(f"Average ROE: {avg_roe}%")
    st.write(f"Average Debt Ratio: {avg_debt}%")

    if avg_roe>15:
        st.success("✅ Strong profitability")
    else:
        st.info("⚠️ Moderate profitability")

    if avg_debt<50:
        st.success("✅ Low financial risk")
    else:
        st.warning("⚠️ Higher financial risk")
