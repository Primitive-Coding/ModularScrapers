from Profiles.Macroeconomic.macro_scraper import MacroScraper
from Profiles.Commodities.commodities_scraper import CommoditiesScraper
from Profiles.Equities.equities_scraper import EquityScraper
from Profiles.DefiLlama.defi_llama_scraper import DefiLlama

import os

from dotenv import load_dotenv

load_dotenv()

alpha = os.getenv("alpha_vantage_key")


CHROME_DRIVER_PATH = "D:\\ChromeDriver\\chromedriver.exe"
EXPORT_PATH = "Test"


if __name__ == "__main__":
    d = DefiLlama(CHROME_DRIVER_PATH, EXPORT_PATH, export=True)
    d.scrape_chains()
