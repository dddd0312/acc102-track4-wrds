# ACC102 Track 4: US Stock Financial Analysis Tool
An interactive web-based financial analysis application built with Streamlit and WRDS database for analyzing U.S. public company performance.

## 📌 Project Overview
This project is developed for ACC102 Track 4 assessment. It provides a user-friendly interface to calculate key financial ratios, visualize trends, and interpret corporate performance using reliable data from WRDS Compustat. Users can upload their own WRDS-exported CSV data, select custom time periods, and generate automated financial analysis with one click.

## 🎯 Features
- Secure WRDS database credential display (assignment requirement)
- Support local WRDS CSV data upload and analysis
- Customizable year range selection (1990–2025)
- Automatic financial ratio calculation
- Interactive profitability and leverage charts
- Real-time analysis interpretation
- Clean and professional web interface
- Side navigation panel for better experience
- Built-in sample dataset for demonstration without CSV upload

## 📊 Financial Ratios Calculated
- ROE (Return on Equity)
- ROA (Return on Assets)
- Debt-to-Asset Ratio
- Net Profit Margin
- Revenue Growth Rate
- Current Ratio

## 🧰 Technologies Used
- Python
- Streamlit
- WRDS Database (Compustat Annual)
- Pandas
- Matplotlib

## 📂 Files in Repository
- `app.py` - Main interactive application
- `requirements.txt` - Required libraries
- `analysis_notebook.ipynb` - Jupyter analysis notebook
- `README.md` - Project documentation

## 🌐 Online Application Link
(https://acc102-track4-wrds-kntpdvhrvancy6tm4e3bsb.streamlit.app)

## 📚 Data Source
- WRDS Compustat North America
- Annual Financial Data (2000–2025)
- Variables include: tic, fyear, at, lt, sale, ni

## 🚀 How to Use
1. Enter WRDS credentials (interface display only)
2. Select desired stock ticker and time period (1990–2026)
3. Upload your WRDS-compiled CSV financial file
4. Click “Run Full Financial Analysis”
5. View tables, charts, and automated performance summary

## ⚠️ Limitations
1. The tool requires a valid WRDS account to access real-time data, which may limit public usage.
2. Only annual financial data is included; quarterly or monthly data is not supported.
3. No industry benchmark or peer comparison functions are available.
4. The analysis is based purely on numerical financial ratios without qualitative factors.
5. Potential missing data or extreme values may affect calculation accuracy.
6. The tool does not support non-US stocks or private companies.
7. Public users must upload local CSV files as live database access is restricted.

## ✨ Author
ACC102 Track 4 Project
