import os
import requests
import pandas as pd
import Profiles.scraper
import datetime as dt
import yfinance as yf
from selenium.common.exceptions import NoSuchElementException, TimeoutException

cwd = os.getcwd()


class FilingDates(Profiles.scraper.Scraper):
    def __init__(
        self,
        ticker: str,
        alpha_vantage_key: str,
        base_export_path: str = "",
        export: bool = True,
    ) -> None:
        self.ticker = ticker.upper()
        if base_export_path == "":
            self.base_export_path = f"{cwd}\\Profiles\\FilingDates\\filing_dates.csv"
        else:
            self.base_export_path = base_export_path

        self.key = alpha_vantage_key
        self.export = export

        super().__init__("")

    """-------------------------------"""

    def get_predefined_path(self):
        return f"{cwd}\\Profiles\\FilingDates\\filing_dates.csv"

    """-------------------------------"""

    def get_fiscal_dates(self, frequency: str = "q"):
        if frequency in self.quarterly_params:
            frequency = "quarterlyEarnings"
        elif frequency in self.annual_params:
            frequency = "annualEarnings"

        # Construct the API request URL
        endpoint = "https://www.alphavantage.co/query"
        params = {"function": "EARNINGS", "symbol": self.ticker, "apikey": self.key}

        # Make the API request
        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()[frequency]
            df = pd.DataFrame(data)
            return df["fiscalDateEnding"]
        else:
            print(f"[Error] Retrieving Fiscal Dates")

    """-------------------------------"""

    def organize_quarters(self, quarters: list, fiscal_end: str):
        """
        :param quarters: Unordered list of the most recent 4 quarters.
        :param fiscal_end: The date of the 4th quarter.

        :return: list of organized quarters.
        """
        # Format the date to only get the month and day. Ex: 2020-09-30 -> 09-30
        for i in range(len(quarters)):
            split_date = quarters[i].split("-")
            split_date = f"{split_date[1]}-{split_date[2]}"
            quarters[i] = split_date

        # Format the "fiscal_end" date to match the quarters. Ex: 2020-12-31 -> 12-31
        fiscal_end = fiscal_end.split("-")
        fiscal_end = f"{fiscal_end[1]}-{fiscal_end[2]}"

        # Find the index of q4 in our list of quarters.
        q4_index = 0
        for i in range(len(quarters)):
            # If the number of days between than date1 & date2 is less than "days_threshold", the if statement will return True and break the loop.
            if self.compare_dates(
                date1=quarters[i], date2=fiscal_end, days_threshold=10
            ):
                break
            # If not, increase the q4_index. When the loop breaks the value of q4_index will be used at whatever increment it's current state is.
            else:
                q4_index += 1

        # If q4 is at the first index. [*12-31*, 03-31, 06-30, 09-30]
        if q4_index == 0:
            quarter_data = {
                "ticker": self.ticker,
                "Q1": quarters[1],
                "Q2": quarters[2],
                "Q3": quarters[3],
                "Q4": fiscal_end,
                "fiscal_end": fiscal_end,
            }
        # If q4 is at the second index. [09-30, *12-31*, 03-31, 06-30]
        elif q4_index == 1:
            quarter_data = {
                "ticker": self.ticker,
                "Q1": quarters[2],
                "Q2": quarters[3],
                "Q3": quarters[0],
                "Q4": quarters[q4_index],
                "fiscal_end": fiscal_end,
            }
        # If q4 is at the third index. [06-30, 09-30, *12-31*, 03-31]
        elif q4_index == 2:
            quarter_data = {
                "ticker": self.ticker,
                "Q1": quarters[3],
                "Q2": quarters[0],
                "Q3": quarters[1],
                "Q4": quarters[q4_index],
                "fiscal_end": fiscal_end,
            }
        # If q4 is at the third index. [03-31, 06-30, 09-30, *12-31*]
        elif q4_index == 3:
            quarter_data = {
                "ticker": self.ticker,
                "Q1": quarters[0],
                "Q2": quarters[1],
                "Q3": quarters[2],
                "Q4": quarters[q4_index],
                "fiscal_end": fiscal_end,
            }

        return quarter_data

    """-------------------------------"""

    def get_fiscal_year_end_date(self) -> str:
        """
        This function will search the SEC EDGAR database, find the most recent 10-K, and return the period of report for that 10-k.
        :return: str of the end date of the fiscal year."""

        sec_annual_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={self.ticker}&type=10-k&dateb=&owner=include&count=100&search_text="

        self.create_browser(sec_annual_url)

        # Loop vars
        running = True
        filing_index = 2
        date_index = 2

        while running:

            filing_type_xpath = (
                f"/html/body/div[4]/div[4]/table/tbody/tr[{filing_index}]/td[1]"
            )
            print(f"Filing: {filing_type_xpath}")
            date_xpath = f"/html/body/div[4]/div[4]/table/tbody/tr[{date_index}]/td[4]"
            # Extract the data.

            try:
                filing_type = self.read_data(filing_type_xpath)
                filing_date = self.read_data(date_xpath)

                if filing_type == "10-K":
                    print(f"Filing Type: {filing_type} {filing_date}")
                    documents_button_xpath = f"/html/body/div[4]/div[4]/table/tbody/tr[{filing_index}]/td[2]/a[1]"
                    self.click_button(documents_button_xpath, wait=True, _wait_time=5)
                    # NOTE: This xpath does not require an index to be incremented.
                    period_of_report_xpath = (
                        "/html/body/div[4]/div[1]/div[2]/div[2]/div[2]"
                    )
                    period_of_report = self.read_data(
                        period_of_report_xpath, wait=True, _wait_time=5
                    )
                    self.clean_close()
                    return period_of_report
                else:
                    running = False
                    self.clean_close()
                    return "N\A"
            except NoSuchElementException:
                running = False
                self.clean_close()
                return "N\A"

    """-------------------------------"""

    def get_all_data(self, frequency: str = "q"):

        csv_file = pd.read_csv(self.base_export_path)

        # Check if the ticker is in the csv file.
        ticker_data = csv_file[csv_file["ticker"] == self.ticker]

        if ticker_data.empty:
            # Get the quarterly filings for the income statement.
            fiscal_dates = self.get_fiscal_dates(frequency)
            # Get the dates of the last 4 quarters for the company.
            last_4_quarters = fiscal_dates[:4].to_list()[::-1]
            # income_statement_cols = income_statement.columns.to_list()

            # Get the fiscal year end for the company.
            fiscal_end = self.get_fiscal_year_end_date()

            if fiscal_end != "N\A":
                # Get the organized quarters.
                organized_quarters = self.organize_quarters(
                    last_4_quarters, fiscal_end=fiscal_end
                )
                organized_quarters = [organized_quarters]
                # Turn the dictionary into a list. The only element should be this dictionary.
                # Update csv dataframe with new values.
                csv_file = csv_file.from_records(organized_quarters)
                if self.export:
                    csv_file.to_csv(
                        self.base_export_path, mode="a", header=False, index=False
                    )
                ticker_data = csv_file[csv_file["ticker"] == self.ticker]
                ticker_data = ticker_data.set_index("ticker")

                return ticker_data
            else:
                print(f"Could not retrieve fiscal dates for [{self.ticker}]")
        else:
            ticker_data = ticker_data.set_index("ticker")
            return ticker_data
        # fiscal_dates = self.get_fiscal_dates(frequency)
        # last

    """-------------------------------"""

    def get_trading_years(self) -> tuple:
        try:
            # Create a Yahoo Finance Ticker object for the given symbol
            ticker = yf.Ticker(self.ticker)

            # Get historical data
            historical_data = ticker.history(period="max")

            # Extract the first trading year
            first_year = historical_data.index[0].year
            last_year = historical_data.index[-1].year
            return (first_year, last_year)
        except Exception as e:
            print(f"Error: {e}")
            return None
