"""Home page object: reads temperature and routes to a department."""
from selenium.webdriver.common.by import By


class HomePage:
    URL = "https://weathershopper.pythonanywhere.com/"
    TEMPERATURE = (By.ID, "temperature")
    BUY_MOISTURIZERS = (By.XPATH, "//button[contains(.,'Buy moisturizers')]")
    BUY_SUNSCREENS = (By.XPATH, "//button[contains(.,'Buy sunscreens')]")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def temperature(self) -> int:
        text = self.driver.find_element(*self.TEMPERATURE).text
        return int("".join(c for c in text if c.isdigit() or c == "-"))

    def choose_department(self) -> str:
        if self.temperature() < 19:
            self.driver.find_element(*self.BUY_MOISTURIZERS).click()
            return "moisturizer"
        self.driver.find_element(*self.BUY_SUNSCREENS).click()
        return "sunscreen"
