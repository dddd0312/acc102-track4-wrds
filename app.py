import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 页面基础配置
st.set_page_config(page_title="ACC102 WRDS Financial Analyzer", layout="wide")

# 左侧导航栏
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

# 主页面标题
st.markdown("# 📊 ACC102 Track 4: US Stock Financial Analyzer")
st.subheader("Interactive Financial Ratio & Trend Analysis")

# ✅ 恢复WRDS登录入口（作业必填项）
st.subheader("🔑 WRDS Database Login")
wrds_username = st.text_input("WRDS Username")
wrds_password = st.text_input("WRDS Password", type="password")

# 基础参数输入
st.subheader("⚙️ Analysis Settings")
ticker = st.text_input("Stock Ticker (e.g. AAPL, MSFT, NVDA)", value="AAPL")
start_year = st.number_input("Start Year", min_value=2010, max_value=2030, value=2020)
end_year = st.number_input("End Year", min_value=2010, max_value=2030, value=2024)

# ✅ 新增CSV上传入口（用你本地下载的WRDS CSV）
st.subheader("📂 Or Upload Local WRDS CSV File")
uploaded_wrds_csv = st.file_uploader("Upload WRDS exported CSV", type="csv")


# 运行分析按钮
if st.button("🚀 Run Financial Analysis"):

    # 基础输入校验保护
    if start_year >= end_year:
        st.error("⚠️ End Year must be later than Start Year!")
        st.stop()

    df = None

    # 1. 优先方式：本地WRDS账号直连获取数据
    if wrds_username.strip() and wrds_password.strip():
        try:
            import wrds
            db = wrds.Connection(wrds_username=wrds_username, wrds_password=wrds_password)

            query = f"""
            SELECT fyear, tic, at, lt, sale, ni
            FROM comp.funda
            WHERE tic = '{ticker.upper()}'
            AND fyear BETWEEN {start_year} AND {end_year}
            AND indfmt = 'INDL'
            AND datafmt = 'STD'
            ORDER BY fyear ASC
            """
            df = db.raw_sql(query)
            db.close()

            if not df.empty:
                st.success("✅ Successfully loaded real-time data from WRDS database!")

        except Exception:
            st.warning("⚠️ Cloud WRDS connection failed, will use backup data source.")
            df = None


    # 2. 备选方式：读取你上传的WRDS导出CSV
    if df is None and uploaded_wrds_csv is not None:
        df = pd.read_csv(uploaded_wrds_csv)
        st.success("✅ Successfully loaded your uploaded WRDS CSV file!")


    # 3. 兜底演示数据（保证页面绝对不会崩溃）
    if df is None or df.empty:
        st.info("ℹ️ Using built-in AAPL WRDS sample data for demonstration.")
        df = pd.DataFrame({
            "fyear": [2020,2021,2022,2023,2024],
            "tic":["AAPL"]*5,
            "at":[323888,351002,352755,352583,382054],
            "lt":[258549,287912,302083,290437,309023],
            "sale":[274515,365817,394328,383285,391035],
            "ni":[57411,94680,99803,96995,97243]
        })


    # 统一财务比率计算
    df["Equity"] = df["at"] - df["lt"]
    df["ROE"] = (df["ni"] / df["Equity"]).round(3)
    df["ROA"] = (df["ni"] / df["at"]).round(3)
    df["Debt_to_Asset_Ratio"] = (df["lt"] / df["at"]).round(3)
    df["Net_Profit_Margin"] = (df["ni"] / df["sale"]).round(3)


    # 展示完整数据表
    st.subheader("📄 Financial Dataset & Calculated Ratios")
    st.dataframe(df, use_container_width=True)


    # 可视化图表
    st.subheader("📈 Financial Trend Visualization")
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(15,6))

    ax1.plot(df["fyear"], df["ROE"], marker="o", linewidth=3, label="ROE")
    ax1.plot(df["fyear"], df["ROA"], marker="s", linewidth=3, label="ROA")
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


    # 自动英文分析总结
    st.subheader("📝 Performance Analysis Summary")
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
