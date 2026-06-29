"""Products page object: adds the cheapest product matching a keyword."""
import re
from selenium.webdriver.common.by import By


class ProductsPage:
    CARD = (By.CSS_SELECTOR, ".text-center.col-4")
    CART = (By.XPATH, "//button[contains(.,'Cart')]")

    def __init__(self, driver):
        self.driver = driver

    def add_cheapest(self, keyword: str):
        keyword = keyword.lower()
        cards = self.driver.find_elements(*self.CARD)
        cheapest, cheapest_price = None, float("inf")
        for card in cards:
            name = card.find_element(By.CSS_SELECTOR, "p.font-weight-bold").text.lower()
            if keyword not in name:
                continue
            price_text = next(p.text for p in card.find_elements(By.TAG_NAME, "p") if "Rs." in p.text)
            price = int(re.sub(r"\D", "", price_text))
            if price < cheapest_price:
                cheapest_price, cheapest = price, card
        if cheapest is None:
            raise AssertionError(f"No product found for keyword: {keyword}")
        cheapest.find_element(By.TAG_NAME, "button").click()

    def go_to_cart(self):
        self.driver.find_element(*self.CART).click()
