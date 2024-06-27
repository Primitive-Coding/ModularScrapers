# Modular Scrapers

Collection of modular scrapers.
Each section below pertains to a folder within "Profiles"

---

### 13F

1. Navigate to the repository:
   ```
   cd 13F
   ```
2. Install pandas or requirements.txt
   ```
   pip install -r requirements.txt
   ```

```
python analyze_13f.py path/to/xml/file.xml [-n TOP_POSITIONS]
```

Replace `path/to/xml/file.xml` with the path to your 13F XML file.

Optional arguments:

- `-n TOP_POSITIONS` or `--top-positions TOP_POSITIONS`: Specify the number of top positions to display (default is 20).

Example:
`python analyze_13f.py filings/13f_filing.xml -n 10`

---

### Commodities

- Get information related to commodities.

---

### DefiLlama

- Take a snapshot of current market.
- Get Chain rankings by Total Value Locked (TVL).
- Get Oracle rankings by Total Value Secured (TVS).
- Get Treasury rankings by treasury composition.

---

### EarningsEstimates

- Get historical EPS, and predicted EPS by analysts.

---

### Equities

- Get annual or quarterly financial statements from Alpha Vantage.
- _Note_ Requires API key.

---

### Filing Dates

- Get the filing dates of the company.

---

### Macroeconomic

- Get the most recent macroeconomic data including:
  - Consumer Price Index (CPI)
  - Fed Funds Rate
  - 10Y - 2Y Treasury Yield Spread

---

### SEC

- Get information related to a company.

---

### StockPriceYearRange

- Get the stock prices within a specific period of a financial report.
