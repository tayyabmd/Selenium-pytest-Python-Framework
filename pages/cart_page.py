"""Cart + Stripe checkout page object."""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    PAY = (By.XPATH, "//*[contains(text(),'Pay with Card')]")
    STRIPE_FRAME = (By.CSS_SELECTOR, "iframe[name='stripe_checkout_app']")
    SUCCESS = (By.XPATH, "//*[contains(text(),'PAYMENT SUCCESS')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def pay_with_card(self):
        # Stripe injects one or more "Pay with Card" nodes; click the visible one.
        self.wait.until(EC.presence_of_element_located(self.PAY))
        for el in self.driver.find_elements(*self.PAY):
            if el.is_displayed():
                el.click()
                return
        raise AssertionError("No visible 'Pay with Card' button found")

    def complete_stripe_checkout(self, card: dict):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.STRIPE_FRAME))
        self._type("email", card["email"])
        self._type("card_number", card["card"])
        self._type("cc-exp", card["expiry"])
        self._type("cc-csc", card["cvc"])
        zip_field = self.wait.until(EC.presence_of_element_located((By.ID, "billing-zip")))
        self._send_slow(zip_field, card["zip"])
        self.driver.find_element(By.ID, "submitButton").click()
        self.driver.switch_to.default_content()

    def _type(self, element_id: str, value: str):
        field = self.wait.until(EC.element_to_be_clickable((By.ID, element_id)))
        self._send_slow(field, value)

    @staticmethod
    def _send_slow(field, value: str):
        # Stripe's formatted inputs drop characters when typed too fast.
        for char in value:
            field.send_keys(char)
            time.sleep(0.08)

    def expect_success(self):
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS)) is not None
