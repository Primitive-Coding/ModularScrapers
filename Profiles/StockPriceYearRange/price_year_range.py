# Date & time imports
import time
import datetime as dt

import os

cwd = os.getcwd()
# Webscraping
import requests

# Yahoo Finance imports
import yfinance as yf

import pandas as pd

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Profiles.scraper


class StockPriceYearRange(Profiles.scraper.Scraper):
    def __init__(self, ticker: str, base_export_path: str = "") -> None:
        self.ticker = ticker.upper()
        super().__init__("")

    """-------------------------------"""

    """-------------------------------"""

    def get_quarter_price_data(
        self, fiscal_periods: pd.Series, trading_years: tuple
    ) -> dict:
        quarterly_data = {}
        for year in range(trading_years[0], trading_years[1] + 1):
            q1_date = fiscal_periods.Q1.values[0]
            q2_date = fiscal_periods.Q2.values[0]
            q3_date = fiscal_periods.Q3.values[0]
            q4_date = fiscal_periods.Q4.values[0]

            print(f"Q1: {q1_date}")

            # Logic to determine the start date for Q1.
            if self.if_date_greater(
                target_date=q1_date, compare_date=q4_date
            ):  # Determine if Q1 is greater than Q4. If it is, then the company has an "offset" fiscal year.
                # Get the start date for Q1, by calculating 1 day after the end of Q4.
                q1_start_date = f"{year-1}-{self.add_days_to_date(target_date=q4_date, days_to_add=1)}"
                q1_end_date = f"{year-1}-{q1_date}"
            # Company with a normal fiscal year.
            else:
                q1_start_date = f"{year}-01-01"
                q1_end_date = f"{year}-{q1_date}"
            # Logic to determine the start date for Q2.
            if self.if_date_greater(
                target_date=q2_date, compare_date=q4_date
            ):  # Determine if Q2 is greater than Q4.
                # Get the start date for Q2, by calculating 1 day after the end of Q1.
                q2_start_date = f"{year-1}-{self.add_days_to_date(target_date=q1_date, days_to_add=1)}"
                q2_end_date = f"{year-1}-{q2_date}"
            else:
                q2_start_date = f"{year}-{self.add_days_to_date(target_date=q1_date, days_to_add=1)}"
                q2_end_date = f"{year}-{q2_date}"
            # Logic to determine the start date for Q3 & Q4.
            if self.if_date_greater(target_date=q3_date, compare_date=q4_date):
                # Get the start date for Q3, by calculating 1 day after the end of Q2.
                q3_start_date = f"{year-1}-{self.add_days_to_date(target_date=q2_date, days_to_add=1)}"
                q3_end_date = f"{year-1}-{q3_date}"

                q4_start_date = f"{year-1}-{self.add_days_to_date(target_date=q3_date, days_to_add=1)}"
                q4_end_date = f"{year}-{q4_date}"

            else:
                q3_start_date = f"{year}-{self.add_days_to_date(target_date=q2_date, days_to_add=1)}"
                q3_end_date = f"{year}-{q3_date}"

                # Q4 dates
                q4_start_date = f"{year}-{self.add_days_to_date(target_date=q3_date, days_to_add=1)}"
                q4_end_date = f"{year}-{q4_date}"

                # Get the data from each quarter.
            q1_data = self.get_quarter_data(
                quarter_start=q1_start_date, quarter_end=q1_end_date
            )
            q2_data = self.get_quarter_data(
                quarter_start=q2_start_date, quarter_end=q2_end_date
            )
            q3_data = self.get_quarter_data(
                quarter_start=q3_start_date, quarter_end=q3_end_date
            )
            q4_data = self.get_quarter_data(
                quarter_start=q4_start_date, quarter_end=q4_end_date
            )

            # Store price data in dictionary.
            quarterly_data[f"{year}"] = {
                "Q1": {"start": q1_start_date, "end": q1_end_date, "data": q1_data},
                "Q2": {"start": q2_start_date, "end": q2_end_date, "data": q2_data},
                "Q3": {"start": q3_start_date, "end": q3_end_date, "data": q3_data},
                "Q4": {"start": q4_start_date, "end": q4_end_date, "data": q4_data},
            }

        return quarterly_data

    """-------------------------------"""

    def get_quarter_data(self, quarter_start: str, quarter_end: str) -> dict:
        """
        :param quarter_start: A string that is the date of the quarter_start (Start of the quarter).
        :param quarter_end: A string that is the date of the quarter_end (End of the quarter).
        :return: Dictionary holding the high, low, average of the prices within the timeframe of the quarter.
        """

        quarter_data = {}

        # Split the dates into independent variables.
        start_year, start_month, start_day = quarter_start.split("-")
        end_year, end_month, end_day = quarter_end.split("-")

        # Turn all of the date elements into integers.
        start_year, start_month, start_day = (
            int(start_year),
            int(start_month),
            int(start_day),
        )
        end_year, end_month, end_day = int(end_year), int(end_month), int(end_day)

        # Create start and end dates for the first quarter of the year
        start_date = dt.datetime(start_year, start_month, start_day)
        end_date = dt.datetime(end_year, end_month, end_day)

        # Fetch the stock data for the specified ticker symbol and date range
        stock_data = yf.download(self.ticker, start=start_date, end=end_date)

        # Extract the 'High' and 'Low' columns from the stock data
        quarter_data["High"] = float(round(stock_data["High"].max(), 2))
        quarter_data["Low"] = float(round(stock_data["Low"].min(), 2))
        try:
            quarter_data["Average"] = float(round(stock_data["Adj Close"].mean(), 2))
        except ValueError:
            quarter_data["Average"] = "N\A"
        return quarter_data

    """-------------------------------"""

    def get_annual_price_data(self, fiscal_start_end: dict, year: int):
        """
        :param fiscal_start_end: Dictionary that contains the fiscal year start in the key "fiscal_start", and the fiscal year end in the key "fiscal_end".
        :return: Dictionary holding the high, low, average of the prices within the timeframe of the annual fiscal year.
        """
        annual_data = {}
        finalized_data = {}

        # If the fiscal start is greater than the fiscal end (only in terms of months, and day. ) Ex: 11-31 > 1-31 or 6-30 < 7-31
        if self.if_date_greater(
            target_date=fiscal_start_end["fiscal_start"],
            compare_date=fiscal_start_end["fiscal_end"],
        ):

            fiscal_start = f"{year-1}-{fiscal_start_end['fiscal_start']}"
            fiscal_end = f"{year}-{fiscal_start_end['fiscal_end']}"
            # Fetch the stock data.
            stock_data = yf.download(self.ticker, start=fiscal_start, end=fiscal_end)

            # Extract the "High" and "Low" columns from the stock data.
            annual_data["High"] = round(stock_data["High"].max(), 2)
            annual_data["Low"] = round(stock_data["Low"].min(), 2)

            try:
                annual_data["Average"] = round(stock_data["Adj Close"].mean(), 2)
            except ValueError:
                annual_data["Average"] = "N\A"
        else:
            fiscal_start = f"{year}-{fiscal_start_end['fiscal_start']}"
            fiscal_end = f"{year}-{fiscal_start_end['fiscal_end']}"
            # Fetch the stock data.
            stock_data = yf.download(self.ticker, start=fiscal_start, end=fiscal_end)

            # Extract the "High" and "Low" columns from the stock data.
            annual_data["High"] = round(stock_data["High"].max(), 2)
            annual_data["Low"] = round(stock_data["Low"].min(), 2)

            try:
                annual_data["Average"] = round(stock_data["Adj Close"].mean(), 2)
            except ValueError:
                annual_data["Average"] = "N\A"

        finalized_data = {"start": fiscal_start, "end": fiscal_end, "data": annual_data}

        return finalized_data

    def get_all_data(self, trading_years: list, fiscal_periods: pd.Series):
        pass
