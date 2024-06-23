import requests
import pandas as pd


class SecScraper:
    def __init__(self, folder_path: str) -> None:
        self.folder_path = folder_path
        self.cik_file = f"{self.folder_path}\\cik_data.csv"

    def get_cik(self, ticker: str):
        df = pd.read_csv(self.cik_file, sep="|")

        try:
            cik = df.loc[df["Ticker"] == ticker.upper(), "CIK"].iloc[0]
            cik = str(cik).zfill(
                10
            )  # Add leading zero prefix. The total string length should *ONLY EVER* be 10 characters long.
            return cik
        except IndexError:  # If ticker is not found.
            return None

    def get_filing_history(self, ticker: str):
        cik = self.get_cik(ticker)
        query = f"https://data.sec.gov/submissions/CIK{cik}.json"
        print(f"Query: {query}")
        response = requests.get(query)
        print(f"Response: {response.status_code}")


if __name__ == "__main__":
    ticker = "AAPL"
    folder_path = "D:\\FinancialData\\FinancialData\\EquityData\\CIK"
    s = SecScraper(folder_path)
    cik = s.get_filing_history(ticker)
