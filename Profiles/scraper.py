import numpy as np

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Scraper:
    def __init__(self, chrome_driver_path: str) -> None:
        self.chrome_driver_path = chrome_driver_path
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-gpu")
        self.browser = None

    """-----------------------------------"""

    def create_browser(self, url=None):
        """
        :param url: The website to visit.
        :return: None
        """
        service = Service(executable_path=self.chrome_driver_path)
        self.browser = webdriver.Chrome(service=service, options=self.chrome_options)
        # Default browser route
        if url == None:
            self.browser.get(url=self.sec_annual_url)
        # External browser route
        else:
            self.browser.get(url=url)

    def clean_close(self) -> None:
        self.browser.close()
        self.browser.quit()

    """-----------------------------------"""

    def scroll_page(
        self,
        pixel_to_scroll: int = 500,
        element_to_scroll="",
        by_pixel: bool = True,
        by_element: bool = False,
    ) -> None:
        """
        :param element_to_scroll: Scroll to the specified element on the webpage.
        :returns: There is no data to return.
        """
        if by_pixel:
            self.browser.execute_script(f"window.scrollBy(0, {pixel_to_scroll})", "")

        if by_element:
            self.browser.execute_script(
                "arguments[0].scrollIntoView(true);", element_to_scroll
            )

    """-----------------------------------"""

    def get_webpage_dimensions(self):
        """
        Get the webpage width and height for the current url.
        """
        width = self.browser.execute_script("return window.outerWidth")
        height = self.browser.execute_script("return window.outerHeight")
        return width, height

    def read_data(
        self, xpath: str, wait: bool = False, _wait_time: int = 5, tag: str = ""
    ) -> str:
        """
        :param xpath: Path to the web element.
        :param wait: Boolean to determine if selenium should wait until the element is located.
        :param wait_time: Integer that represents how many seconds selenium should wait, if wait is True.
        :return: (str) Text of the element.
        """

        if wait:
            try:
                data = (
                    WebDriverWait(self.browser, _wait_time)
                    .until(EC.presence_of_element_located((By.XPATH, xpath)))
                    .text
                )
            except TimeoutException:
                print(f"[Failed Xpath] {xpath}")
                if tag != "":
                    print(f"[Tag]: {tag}")
                raise NoSuchElementException("Element not found")
        else:
            data = self.browser.find_element("xpath", xpath).text
        # Return the text of the element found.
        return data

    """-----------------------------------"""

    def click_button(
        self,
        xpath: str,
        wait: bool = False,
        _wait_time: int = 5,
        scroll: bool = False,
        tag: str = "",
    ) -> None:
        """
        :param xpath: Path to the web element.
        :param wait: Boolean to determine if selenium should wait until the element is located.
        :param wait_time: Integer that represents how many seconds selenium should wait, if wait is True.
        :return: None. Because this function clicks the button but does not return any information about the button or any related web elements.
        """

        if wait:
            try:
                element = WebDriverWait(self.browser, _wait_time).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                # If the webdriver needs to scroll before clicking the element.
                if scroll:
                    self.browser.execute_script("arguments[0].click();", element)
                element.click()
            except TimeoutException:
                print(f"[Failed Xpath] {xpath}")
                if tag != "":
                    print(f"[Tag]: {tag}")
                raise NoSuchElementException("Element not found")
        else:
            element = self.browser.find_element("xpath", xpath)
            if scroll:
                self.browser.execute_script("arguments[0].click();", element)
            element.click()

    """
    Formatting
    """

    def format_basic(self, val) -> int:
        magnitudes = ["m", "b", "t"]
        # Remove commas from string if present.
        if "," in val:
            val = val.replace(",", "")

        try:
            magnitude = val[-1]
            if magnitude in magnitudes:
                val = val[:-1]  # Remove suffix.
                if magnitude.lower() == "m":
                    multi = 1_000_000
                elif magnitude.lower() == "b":
                    multi = 1_000_000_000
                elif magnitude.lower() == "t":
                    multi = 1_000_000_000_000

                val = int(float(val) * multi)

            return val
        except IndexError:
            return np.nan

    def format_dollar(self, val) -> float:
        magnitudes = ["m", "b", "t"]
        # Remove dollar sign from string if present.
        if "$" in val:
            val = val.replace("$", "")

        # Remove commas from string if present.
        if "," in val:
            val = val.replace(",", "")

        try:
            magnitude = val[-1]

            if magnitude in magnitudes:
                val = val[:-1]  # Remove suffix.
                if magnitude.lower() == "m":
                    multi = 1_000_000
                elif magnitude.lower() == "b":
                    multi = 1_000_000_000
                elif magnitude.lower() == "t":
                    multi = 1_000_000_000_000

                val = float(val) * multi

            try:
                return int(val)
            except ValueError:
                return float(val)
        except IndexError:
            return np.nan
