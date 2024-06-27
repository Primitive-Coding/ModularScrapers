# Operating system imports
import os


# Pandas imports
import pandas as pd

import yfinance as yf


import Profiles.scraper

commodities = {
    "BZ=F": {
        "name_key": "Brent Crude Oil",
        "class_key": "Oil",
        "category_key": "Fossil Fuels",
    },
    "CC=F": {
        "name_key": "Cocoa",
        "class_key": "Cocoa",
        "category_key": "Agriculture",
    },
    "KC=F": {
        "name_key": "Coffee",
        "class_key": "Coffee",
        "category_key": "Agriculture",
    },
    "HG=F": {
        "name_key": "Copper",
        "class_key": "Copper",
        "category_key": "Basic Materials",
    },
    "ZC=F": {
        "name_key": "Corn Futures",
        "class_key": "Corn",
        "category_key": "Agriculture",
    },
    "CT=F": {
        "name_key": "Cotton",
        "class_key": "Cotton",
        "category_key": "Agriculture",
    },
    "CL=F": {
        "name_key": "Crude Oil",
        "class_key": "Oil",
        "category_key": "Fossil Fuels",
    },
    "GC=F": {
        "name_key": "Gold",
        "class_key": "Gold",
        "category_key": "Basic Materials",
    },
    "HO=F": {
        "name_key": "Heating Oil",
        "class_key": "Heating Oil",
        "category_key": "Fossil Fuels",
    },
    "KE=F": {
        "name_key": "KC HRW Wheat",
        "class_key": "Wheat",
        "category_key": "Agriculture",
    },
    "HE=F": {
        "name_key": "Lean Hogs",
        "class_key": "Hogs",
        "category_key": "Agriculture",
    },
    "LE=F": {
        "name_key": "Live Cattle",
        "class_key": "Cattle",
        "category_key": "Agriculture",
    },
    "B0=F": {
        "name_key": "Mont Belvieu LDH Propane",
        "class_key": "Propane",
        "category_key": "Fossil Fuels",
    },
    "NG=F": {
        "name_key": "Natural Gas",
        "class_key": "Natural Gas",
        "category_key": "Fossil Fuels",
    },
    "ZO=F": {
        "name_key": "Oat Futures",
        "class_key": "Oats",
        "category_key": "Agriculture",
    },
    "OJ=F": {
        "name_key": "Orange Juice",
        "class_key": "Orange Juice",
        "category_key": "Agriculture",
    },
    "PA=F": {
        "name_key": "Palladium",
        "class_key": "Palladium",
        "category_key": "Basic Materials",
    },
    "PL=F": {
        "name_key": "Platinum",
        "class_key": "Platinum",
        "category_key": "Basic Materials",
    },
    "LBS=F": {
        "name_key": "Random Length Lumber",
        "class_key": "Lumber",
        "category_key": "Basic Materials",
    },
    "ZR=F": {
        "name_key": "Rough Rice",
        "class_key": "Rice",
        "category_key": "Agriculture",
    },
    "SI=F": {
        "name_key": "Silver",
        "class_key": "Silver",
        "category_key": "Basic Materials",
    },
    "ZL=F": {
        "name_key": "Soybean Oil",
        "class_key": "Soybean Oil",
        "category_key": "Agriculture",
    },
    "ZS=F": {
        "name_key": "Soybeans",
        "class_key": "Soybeans",
        "category_key": "Agriculture",
    },
    "SB=F": {
        "name_key": "Sugar #11",
        "class_key": "Sugar",
        "category_key": "Agriculture",
    },
    "HRC=F": {
        "name_key": "U.S. Midwest Domestic Hot-Rolled Coil Steel",
        "class_key": "Steel",
        "category_key": "Basic Materials",
    },
}


class CommoditiesScraper(Profiles.scraper.Scraper):
    def __init__(
        self,
        chrome_driver_path: str,
        base_export_path: str,
    ):
        self.browser = None
        self.commodities_data_folder_path = f"{base_export_path}\\CommoditiesData"
        os.makedirs(self.commodities_data_folder_path, exist_ok=True)
        super().__init__(chrome_driver_path)

    """-----------------------------------"""
    """-----------------------------------"""
    """-----------------------------------"""

    def reorder_data(self):
        path = f"{self.commodities_data_folder_path}\\commodity_info.csv"
        df = pd.read_csv(path)
        new_order = ["ticker", "name", "info", "tag"]
        reordered_df = df[new_order]
        reordered_df = reordered_df.rename(
            columns={"info": "classification", "tag": "category"}
        )
        reordered_df.to_csv(path, index=False)

    """-----------------------------------"""

    def get_data(self) -> pd.DataFrame:
        df = pd.DataFrame(commodities)
        return df

    """-----------------------------------"""

    def get_price(self, ticker: str):
        price = yf.download(ticker.upper())
        return price

    """-----------------------------------"""

    def export_data(self, path_to_export: str = ""):
        df = pd.DataFrame(commodities).T
        if path_to_export == "":
            df.to_csv(f"{self.commodities_data_folder_path}\\commodity_info.csv")
        else:
            df.to_csv(path_to_export)

    """-----------------------------------"""
    """-----------------------------------"""
