# ACC102 Track 4: WRDS US Stock Financial Analyzer

## Project Overview
This is an interactive web-based financial ratio analysis tool developed for the ACC102 Track 4 assignment.
The application uses official **WRDS Compustat annual financial data** to calculate key financial metrics, generate trend visualizations, and provide automated performance analysis for selected US public stocks.

## Features
- ✅ Full English user interface
- ✅ WRDS credential display (assignment requirement)
- ✅ Customizable year range from **1990 to 2026**
- ✅ Support for custom WRDS CSV data upload
- ✅ Automatic core financial ratio calculation
  - Return on Equity (ROE)
  - Return on Assets (ROA)
  - Debt-to-Asset Ratio
  - Net Profit Margin
- ✅ Interactive data filtering
- ✅ Professional trend line & bar charts
- ✅ Automated financial performance summary & evaluation
- ✅ Built-in demo dataset for backup demonstration
- ✅ Cloud deployment on Streamlit, one-click access

## Data Source
- Primary Data: **WRDS Compustat North America Annual Fundamentals**
- Required core financial variables:
  - `tic` = Stock Ticker Symbol
  - `fyear` = Fiscal Year
  - `at` = Total Assets
  - `lt` = Total Liabilities
  - `sale` = Total Revenue / Net Sales
  - `ni` = Net Income

## How to Use
1. **Enter WRDS Account Credentials** (display only, no live cloud connection required)
2. **Set Analysis Parameters**
   - Input target stock ticker (e.g. AAPL, MSFT, NVDA)
   - Select start year (1990 - 2026)
   - Select end year (1990 - 2026)
3. **Upload Your WRDS CSV File**
   - Upload the CSV file exported from official WRDS Compustat database
4. Click **Run Full Financial Analysis**
5. View the full financial dataset, calculated ratios, interactive charts and performance summary

## Deployment & Running
This application is built with Python and Streamlit.

### Local Run
1. Install required dependencies:
```bash
pip install streamlit pandas matplotlib
