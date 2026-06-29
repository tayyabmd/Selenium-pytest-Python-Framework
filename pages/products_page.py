"""Products page object: adds the cheapest product matching a keyword."""
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductsPage:
    CARD = (By.CSS_SELECTOR, ".text-center.col-4")
    ADD_BUTTON = (By.CSS_SELECTOR, ".btn-primary")
    CART = (By.XPATH, "//button[contains(.,'Cart')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def add_cheapest(self, keyword: str):
        keyword = keyword.lower()
        self.wait.until(EC.presence_of_element_located(self.CARD))
        cards = self.driver.find_elements(*self.CARD)
        cheapest, cheapest_price = None, float("inf")
        for card in cards:
            button = card.find_element(By.TAG_NAME, "button")
            onclick = (button.get_attribute("onclick") or "").lower()
            if keyword not in onclick:
                continue
            match = re.search(r",\s*(\d+)\s*\)", onclick)
            price = int(match.group(1)) if match else float("inf")
            if price < cheapest_price:
                cheapest_price, cheapest = price, button
        if cheapest is None:
            raise AssertionError(f"No product found for keyword: {keyword}")
        cheapest.click()
        time.sleep(0.8)  # let addToCart register before the next action

    def go_to_cart(self):
        self.driver.find_element(*self.CART).click()
