import streamlit as st
import wrds
import pandas as pd
import matplotlib.pyplot as plt

# ------------------- Side Navigation Panel -------------------
st.set_page_config(page_title="US Stock WRDS Financial Analysis", layout="wide")
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

# ------------------- Main Page Title -------------------
st.title("📊 ACC102 Track 4: WRDS US Stock Financial Analyzer")
st.subheader("Interactive Financial Ratio & Trend Analysis")

# ------------------- User Inputs -------------------
wrds_username = st.text_input("WRDS Username")
wrds_password = st.text_input("WRDS Password", type="password")

ticker = st.text_input("Stock Ticker (e.g. AAPL, MSFT, NVDA)", value="AAPL")
start_year = st.number_input("Start Year", min_value=2010, max_value=2025, value=2020)
end_year = st.number_input("End Year", min_value=2010, max_value=2025, value=2024)

# ------------------- Analysis Button -------------------
if st.button("🚀 Run Financial Analysis"):
    try:
        # Connect to WRDS Database
        db = wrds.Connection(wrds_username=wrds_username, wrds_password=wrds_password)

        # SQL Query to Retrieve Compustat Data
        sql_query = f"""
        SELECT datadate, fyear, conm, tic,
               at, lt, sale, ni, che, rect
        FROM comp.funda
        WHERE tic = '{ticker}'
        AND fyear BETWEEN {start_year} AND {end_year}
        AND indfmt = 'INDL'
        AND datafmt = 'STD'
        ORDER BY fyear ASC
        """

        df = db.raw_sql(sql_query)
        db.close()

        if df.empty:
            st.error("❌ No data found for this ticker and year range.")
        else:
            # Calculate Financial Ratios
            df['Equity'] = df['at'] - df['lt']
            df['ROE'] = df['ni'] / df['Equity']
            df['ROA'] = df['ni'] / df['at']
            df['Debt_to_Asset_Ratio'] = df['lt'] / df['at']
            df['Net_Profit_Margin'] = df['ni'] / df['sale']
            df['Revenue_Growth_Rate'] = df['sale'].pct_change()
            df['Current_Ratio'] = df['che'] / df['lt']
            df = df.round(3)

            # Display Financial Data
            st.subheader("📄 Financial Dataset & Ratio Results")
            st.dataframe(df)

            # Data Visualization
            st.subheader("📈 Financial Trend Visualization")
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

            # Profitability Trend Chart
            ax1.plot(df['fyear'], df['ROE'], marker='o', linewidth=2, label='ROE')
            ax1.plot(df['fyear'], df['ROA'], marker='s', linewidth=2, label='ROA')
            ax1.set_title("Profitability Trend (ROE & ROA)")
            ax1.set_xlabel("Year")
            ax1.legend()
            ax1.grid(alpha=0.3)

            # Leverage Trend Chart
            ax2.bar(df['fyear'], df['Debt_to_Asset_Ratio'], color='darkorange', alpha=0.7)
            ax2.set_title("Leverage Trend (Debt to Asset Ratio)")
            ax2.set_xlabel("Year")
            ax2.grid(alpha=0.3)

            plt.tight_layout()
            st.pyplot(fig)

            # Analysis Summary
            st.subheader("📝 Analysis Interpretation")
            avg_roe = df['ROE'].mean()
            avg_debt = df['Debt_to_Asset_Ratio'].mean()

            st.write(f"Average ROE: **{round(avg_roe*100, 2)}%**")
            st.write(f"Average Debt-to-Asset Ratio: **{round(avg_debt*100, 2)}%**")

            if avg_roe > 0.15:
                st.success("✅ Strong profitability.")
            elif avg_roe > 0:
                st.info("⚠️ Moderate profitability.")
            else:
                st.warning("❌ Weak or negative profitability.")

            if avg_debt < 0.5:
                st.success("✅ Low leverage & low financial risk.")
            else:
                st.warning("⚠️ Higher leverage & increased financial risk.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
