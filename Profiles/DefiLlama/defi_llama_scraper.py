import os
import requests

# Date & Time
import time
import datetime as dt
import numpy as np
import pandas as pd
import lxml.html

# Selenium
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import Profiles.scraper

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
}


class DefiLlama(Profiles.scraper.Scraper):
    def __init__(
        self,
        chrome_driver_path: str,
        base_export_path: str,
        export: bool = False,
        overwrite_if_exists: bool = False,
    ) -> None:
        self.export = export
        self.overwrite_if_exists = overwrite_if_exists
        self.scroll_interval = 17
        self.pixel_count = 100
        self.sleep_time = 5
        self.base_export_path = f"{base_export_path}\\DefiLlama"
        os.makedirs(self.base_export_path, exist_ok=True)
        super().__init__(chrome_driver_path)

    def scrape_chains(self):
        url = "https://defillama.com/chains"

        date = dt.datetime.now().date()
        date_str = date.strftime("%Y-%m-%d")
        file_name = f"chains_{date_str}.csv"
        folder = "Chains"
        path = f"{self.base_export_path}\\{folder}\\{file_name}"
        scrape_new = False
        try:
            # If file exists, it will be read.
            df = pd.read_csv(path)

            if self.overwrite_if_exists:
                scrape_new = True
            else:
                return df

        except FileNotFoundError:
            os.makedirs(f"{self.base_export_path}\\{folder}", exist_ok=True)
            scrape_new = True

        if scrape_new:
            table_config = {
                "name": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[1]/span/a",
                    "format": None,
                },
                "protocols": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[2]",
                    "format": None,
                },
                "active_address": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[3]",
                    "format": lambda x: self.format_basic(x),
                },
                "tvl": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[7]",
                    "format": lambda x: self.format_dollar(x),
                },
                "24h_volume": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[10]",
                    "format": lambda x: self.format_dollar(x),
                },
                "24h_fees": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[11]",
                    "format": lambda x: self.format_dollar(x),
                },
                "mcap/tvl": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[2]/div[4]/div[2]/div[{}]/div[12]",
                    "format": lambda x: self.format_dollar(x),
                },
            }

            # df = self.scrape_table(url, table_config)
            df = self.scrape_table(url, table_config)
            if self.export:
                self.export_to_csv(df, path)
            return df

    """
    =========================
    Scraping Categories
    =========================
    """

    def scrape_dexes(self):
        url = "https://defillama.com/protocols/Dexes"

        date = dt.datetime.now().date()
        date_str = date.strftime("%Y-%m-%d")
        file_name = f"dexes_{date_str}.csv"
        folder = "Dexes"
        path = f"{self.base_export_path}\\{folder}\\{file_name}"
        scrape_new = False
        try:
            # If file exists, it will be read.
            df = pd.read_csv(path)
            if self.overwrite_if_exists:
                scrape_new = True
            else:
                return df

        except FileNotFoundError:
            os.makedirs(f"{self.base_export_path}\\{folder}", exist_ok=True)
            scrape_new = True

        if scrape_new:

            table_config = {
                "name": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[2]/span/span/a",
                    "format": None,
                },
                "tvl": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[6]",
                    "format": lambda x: self.format_dollar(x),
                },
                "fees_7d": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[7]",
                    "format": lambda x: self.format_dollar(x),
                },
                "revenue_7d": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[8]",
                    "format": lambda x: self.format_dollar(x),
                },
                "volume_7d": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[9]",
                    "format": lambda x: self.format_dollar(x),
                },
                "mcap_tvl": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[10]",
                    "format": lambda x: self.format_dollar(x),
                },
                "fees_24h": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[11]",
                    "format": lambda x: self.format_dollar(x),
                },
                "fees_30d": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[12]",
                    "format": lambda x: self.format_dollar(x),
                },
                "revenue_24h": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[13]",
                    "format": lambda x: self.format_dollar(x),
                },
                "volume_24h": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[14]",
                    "format": lambda x: self.format_dollar(x),
                },
            }

            df = self.scrape_table(url, table_config)
            if self.export:
                self.export_to_csv(df, path)
            return df

    def scrape_oracles(self):
        url = "https://defillama.com/oracles"

        date = dt.datetime.now().date()
        date_str = date.strftime("%Y-%m-%d")
        file_name = f"oracles_{date_str}.csv"
        folder = "Oracles"
        path = f"{self.base_export_path}\\{folder}\\{file_name}"
        scrape_new = False
        try:
            # If file exists, it will be read.
            df = pd.read_csv(path)

            if self.overwrite_if_exists:
                scrape_new = True
            else:
                return df

        except FileNotFoundError:
            os.makedirs(f"{self.base_export_path}\\{folder}", exist_ok=True)
            scrape_new = True

        if scrape_new:
            table_config = {
                "name": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[4]/div[2]/div[{}]/div[1]/span/a",
                    "format": None,
                },
                "protocols_secured": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[4]/div[2]/div[{}]/div[3]",
                    "format": lambda x: self.format_dollar(x),
                },
                "tvs": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[4]/div[2]/div[{}]/div[4]",
                    "format": lambda x: self.format_dollar(x),
                },
            }

            df = self.scrape_table(url, table_config)
            if self.export:
                self.export_to_csv(df, path)
            return df

    def scrape_rwa(self):
        url = "https://defillama.com/protocols/RWA"

        date = dt.datetime.now().date()
        date_str = date.strftime("%Y-%m-%d")
        file_name = f"rwa_{date_str}.csv"
        folder = "RWA"
        path = f"{self.base_export_path}\\{folder}\\{file_name}"
        scrape_new = False
        try:
            # If file exists, it will be read.
            df = pd.read_csv(path)

            if self.overwrite_if_exists:
                scrape_new = True
            else:
                return df

        except FileNotFoundError:
            os.makedirs(f"{self.base_export_path}\\{folder}", exist_ok=True)
            scrape_new = True

        if scrape_new:
            table_config = {
                "name": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[2]/span/span/a",
                    "format": None,
                },
                "tvl": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[6]/span/span",
                    "format": lambda x: self.format_dollar(x),
                },
                "fees_7d": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[7]",
                    "format": lambda x: self.format_dollar(x),
                },
                "revenue_7d": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[8]",
                    "format": lambda x: self.format_dollar(x),
                },
                "volume_7d": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[9]",
                    "format": lambda x: self.format_dollar(x),
                },
                "mcap_tvl": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[10]",
                    "format": lambda x: self.format_dollar(x),
                },
                "fees_24h": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[11]",
                    "format": lambda x: self.format_dollar(x),
                },
                "fees_30d": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[12]",
                    "format": lambda x: self.format_dollar(x),
                },
                "revenue_24h": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[13]",
                    "format": lambda x: self.format_dollar(x),
                },
                "volume_24h": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[14]",
                    "format": lambda x: self.format_dollar(x),
                },
            }
            df = self.scrape_table(url, table_config)
            if self.export:
                self.export_to_csv(df, path)
            return df

    def scrape_treasuries(self):
        url = "https://defillama.com/treasuries"

        date = dt.datetime.now().date()
        date_str = date.strftime("%Y-%m-%d")
        file_name = f"treasuries_{date_str}.csv"
        folder = "Treasuries"
        path = f"{self.base_export_path}\\{folder}\\{file_name}"
        scrape_new = False
        try:
            # If file exists, it will be read.
            df = pd.read_csv(path)
            if self.overwrite_if_exists:
                scrape_new = True
            else:
                return df

        except FileNotFoundError:
            scrape_new = True

        if scrape_new:
            table_config = {
                "name": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[2]/div[2]/div[1]/div[{}]/span/a",
                    "format": None,
                },
                "stablecoins": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[2]/div[2]/div[{}]/div[3]",
                    "format": lambda x: self.format_dollar(x),
                },
                "major_coins": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[2]/div[2]/div[{}]/div[4]",
                    "format": lambda x: self.format_dollar(x),
                },
                "own_tokens": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[8]",
                    "format": lambda x: self.format_dollar(x),
                },
                "others": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[9]",
                    "format": lambda x: self.format_dollar(x),
                },
                "total_excluding_own_tokens": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[10]",
                    "format": lambda x: self.format_dollar(x),
                },
                "total": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[11]",
                    "format": lambda x: self.format_dollar(x),
                },
                "mcap": {
                    "value": "/html/body/div[1]/div[1]/div/main/div[3]/div[3]/div[2]/div[{}]/div[12]",
                    "format": lambda x: self.format_dollar(x),
                },
            }
            df = self.scrape_table(url, table_config)
            if self.export:
                self.export_to_csv(df, path)
            return df

    """
    =========================
    Scraping
    =========================
    """

    def scrape_table(self, url, config: dict):
        self.create_browser(url)
        table = []
        index = 1
        pixel_count = self.pixel_count
        self.scroll_page(1100)
        time.sleep(self.sleep_time)
        scraping = True
        while scraping:
            try:
                if index % self.scroll_interval == 0:
                    pass
                    growth = 0.03
                    pixel_count = pixel_count + (pixel_count * growth)
                    self.scroll_page(self.pixel_count)
                    print("--------------------------------------------------------")
                    time.sleep(self.sleep_time)
                row_data = {}
                for k in config.keys():
                    item = config[k]
                    xpath = item["value"].format(index)
                    val = self.read_data(xpath, wait=True)
                    if item["format"] != None:
                        val = item["format"](val)
                    row_data[k] = val

                table.append(row_data)
                index += 1
            except TimeoutException:
                self.clean_close()
                scraping = False
            except NoSuchElementException:
                self.clean_close()
                scraping = False

        df = pd.DataFrame(table)
        try:
            df = df.set_index("name")
        except KeyError:
            pass
        return df

    def export_to_csv(self, df: pd.DataFrame, path: str):
        try:
            df = pd.read_csv(path)
            if self.overwrite_if_exists:
                df.to_csv(path)
            else:
                print(f"[CSV Exist] {path}. Data was not overwritten. ")
        except FileNotFoundError:
            df.to_csv(path)
