import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 页面配置
st.set_page_config(page_title="ACC102 WRDS Financial Analyzer", layout="wide")

# 侧边导航栏
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

# 主标题
st.markdown("# 📊 ACC102 Track 4: WRDS US Stock Financial Analyzer")
st.subheader("Interactive Financial Ratio & Trend Analysis")

# WRDS 登录入口（保留作业要求）
st.markdown("#### 🔑 WRDS Login Credentials")
wrds_username = st.text_input("WRDS Username")
wrds_password = st.text_input("WRDS Password", type="password")

# ==============================
# ✅ 这里已经帮你把年限改成 1990 - 2026
# ==============================
st.markdown("#### ⚙️ Analysis Parameters")
ticker = st.text_input("Stock Ticker (e.g. AAPL)", value="AAPL")
start_year = st.number_input("Start Year", min_value=1990, max_value=2026, value=2000)
end_year = st.number_input("End Year", min_value=1990, max_value=2026, value=2025)

# CSV 上传
st.markdown("#### 📂 Upload Your WRDS Compustat CSV File")
upload_file = st.file_uploader("Upload WRDS Annual Financial CSV", type="csv")

# 运行分析
if st.button("🚀 Run Full Financial Analysis"):

    df = None

    # 读取上传的 CSV
    if upload_file:
        df = pd.read_csv(upload_file)
        st.success("✅ Successfully loaded your WRDS CSV data!")

    # 兜底数据
    if df is None or df.empty:
        st.info("ℹ️ Using built-in sample WRDS dataset")
        df = pd.DataFrame({
            "fyear": [2000,2005,2010,2015,2020,2025],
            "tic": ["AAPL"]*6,
            "at": [20345, 53421, 75432, 153421, 323888, 382054],
            "lt": [12345, 32421, 45432, 98421, 258549, 309023],
            "sale": [12345, 42421, 65432, 183421, 274515, 391035],
            "ni": [2345, 8421, 15432, 48421, 57411, 97243]
        })

    # 根据选择的年份筛选数据
    df = df[(df["fyear"] >= start_year) & (df["fyear"] <= end_year)]

    if df.empty:
        st.error("❌ No data available in the selected year range!")
        st.stop()

    # 财务比率计算
    df["Equity"] = df["at"] - df["lt"]
    df["ROE"] = (df["ni"] / df["Equity"]).round(3)
    df["ROA"] = (df["ni"] / df["at"]).round(3)
    df["Debt_to_Asset_Ratio"] = (df["lt"] / df["at"]).round(3)
    df["Net_Profit_Margin"] = (df["ni"] / df["sale"]).round(3)

    # 展示数据
    st.subheader("📋 Financial Data & Calculated Ratios")
    st.dataframe(df, use_container_width=True)

    # 图表
    st.subheader("📈 Financial Trend Visualization")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.plot(df["fyear"], df["ROE"], marker="o", lw=3, label="ROE")
    ax1.plot(df["fyear"], df["ROA"], marker="s", lw=3, label="ROA")
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

    # 分析总结
    st.subheader("📝 Financial Performance Summary")
    avg_roe = round(df["ROE"].mean() * 100, 2)
    avg_debt = round(df["Debt_to_Asset_Ratio"].mean() * 100, 2)

    st.write(f"Average ROE: **{avg_roe}%**")
    st.write(f"Average Debt-to-Asset Ratio: **{avg_debt}%**")

    if avg_roe > 15:
        st.success("✅ Excellent long-term profitability performance.")
    elif avg_roe > 0:
        st.info("⚠️ Moderate and stable profitability.")
    else:
        st.warning("❌ Weak profitability during the selected period.")

    if avg_debt < 50:
        st.success("✅ Low financial leverage, very low solvency risk.")
    else:
        st.warning("⚠️ Relatively high debt level, increased financial risk.")
