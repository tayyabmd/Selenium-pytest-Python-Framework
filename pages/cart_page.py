"""Cart + Stripe checkout page object."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    PAY = (By.XPATH, "//button[contains(.,'Pay with Card')]")
    STRIPE_FRAME = (By.CSS_SELECTOR, "iframe[name='stripe_checkout_app']")
    SUCCESS = (By.XPATH, "//*[contains(text(),'PAYMENT SUCCESS')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def pay_with_card(self):
        self.driver.find_element(*self.PAY).click()

    def complete_stripe_checkout(self, card: dict):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.STRIPE_FRAME))
        self.driver.find_element(By.ID, "email").send_keys(card["email"])
        self.driver.find_element(By.ID, "card_number").send_keys(card["card"])
        self.driver.find_element(By.ID, "cc-exp").send_keys(card["expiry"])
        self.driver.find_element(By.ID, "cc-csc").send_keys(card["cvc"])
        self.driver.find_element(By.ID, "billing-zip").send_keys(card["zip"])
        self.driver.find_element(By.XPATH, "//button[contains(.,'Pay')]").click()
        self.driver.switch_to.default_content()

    def expect_success(self):
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS)) is not None
