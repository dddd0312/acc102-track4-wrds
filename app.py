import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="ACC102 WRDS Financial Analyzer", layout="wide")

# Sidebar Navigation Panel
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

# Main Page Title
st.markdown("# 📊 ACC102 Track 4: WRDS US Stock Financial Analyzer")
st.subheader("Interactive Financial Ratio & Trend Analysis")

# WRDS Credentials Section (Required for Assignment)
st.markdown("#### 🔑 WRDS Account Credentials")
wrds_username = st.text_input("WRDS Username")
wrds_password = st.text_input("WRDS Password", type="password")

# Analysis Parameters (Year range updated: 1990 - 2026)
st.markdown("#### ⚙️ Analysis Parameters")
ticker = st.text_input("Stock Ticker (e.g. AAPL, MSFT, NVDA)", value="AAPL")
start_year = st.number_input("Start Year", min_value=1990, max_value=2026, value=2000)
end_year = st.number_input("End Year", min_value=1990, max_value=2026, value=2025)

# CSV File Upload Section
st.markdown("#### 📂 Upload Your WRDS Exported CSV File")
uploaded_csv = st.file_uploader("Upload Compustat Annual Financial CSV File", type="csv")

# Run Full Analysis Button
if st.button("🚀 Run Full Financial Analysis"):

    df = None

    # Load uploaded WRDS CSV data first
    if uploaded_csv is not None:
        try:
            df = pd.read_csv(uploaded_csv)
            st.success("✅ Official WRDS CSV data loaded successfully!")

            # Check for required financial columns
            required_columns = ["tic", "fyear", "at", "lt", "sale", "ni"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                st.error(f"❌ Missing required financial columns: {missing_columns}")
                st.info("Please re-export your Compustat CSV with tic, fyear, at, lt, sale, ni included.")
                st.stop()

        except Exception as e:
            st.error(f"❌ Failed to read CSV file: {e}")
            st.stop()

    # Fallback built-in sample dataset
    if df is None or df.empty:
        st.info("ℹ️ No CSV uploaded, loading built-in WRDS sample dataset for demonstration.")
        df = pd.DataFrame({
            "fyear": [2000, 2005, 2010, 2015, 2020, 2025],
            "tic": ["AAPL"] * 6,
            "at": [20345, 53421, 75432, 153421, 323888, 382054],
            "lt": [12345, 32421, 45432, 98421, 258549, 309023],
            "sale": [12345, 42421, 65432, 183421, 274515, 391035],
            "ni": [2345, 8421, 15432, 48421, 57411, 97243]
        })

    # Filter data by selected year range
    df = df[(df["fyear"] >= start_year) & (df["fyear"] <= end_year)].reset_index(drop=True)

    if df.empty:
        st.error("❌ No financial data available within the selected year range.")
        st.stop()

    # Financial Ratio Calculations
    df["Total_Equity"] = df["at"] - df["lt"]
    df["ROE (Return on Equity)"] = (df["ni"] / df["Total_Equity"]).round(3)
    df["ROA (Return on Assets)"] = (df["ni"] / df["at"]).round(3)
    df["Debt_to_Asset_Ratio"] = (df["lt"] / df["at"]).round(3)
    df["Net_Profit_Margin"] = (df["ni"] / df["sale"]).round(3)

    # Display Processed Financial Data
    st.subheader("📋 Financial Dataset & Calculated Ratios")
    st.dataframe(df, use_container_width=True)

    # Visualization Charts
    st.subheader("📈 Financial Trend Visualization")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.plot(df["fyear"], df["ROE (Return on Equity)"], marker="o", linewidth=3, label="ROE")
    ax1.plot(df["fyear"], df["ROA (Return on Assets)"], marker="s", linewidth=3, label="ROA")
    ax1.set_title("Profitability Trend (ROE & ROA)", fontsize=14)
    ax1.set_xlabel("Fiscal Year")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.bar(df["fyear"], df["Debt_to_Asset_Ratio"], color="darkorange", alpha=0.75)
    ax2.set_title("Leverage Trend (Debt to Asset Ratio)", fontsize=14)
    ax2.set_xlabel("Fiscal Year")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

    # Automatic Performance Analysis Summary
    st.subheader("📝 Overall Financial Performance Summary")
    average_roe = round(df["ROE (Return on Equity)"].mean() * 100, 2)
    average_debt_ratio = round(df["Debt_to_Asset_Ratio"].mean() * 100, 2)

    st.write(f"Average ROE over the period: **{average_roe}%**")
    st.write(f"Average Debt-to-Asset Ratio over the period: **{average_debt_ratio}%**")

    # Profitability Evaluation
    if average_roe > 15:
        st.success("✅ The company demonstrates excellent and strong long-term profitability.")
    elif average_roe > 0:
        st.info("⚠️ The company shows moderate and stable overall profitability.")
    else:
        st.warning("❌ The company shows weak profitability during the selected period.")

    # Financial Risk Evaluation
    if average_debt_ratio < 50:
        st.success("✅ Low financial leverage, the company has low solvency and financial risk.")
    else:
        st.warning("⚠️ Relatively high debt level, the company faces increased financial leverage risk.")
