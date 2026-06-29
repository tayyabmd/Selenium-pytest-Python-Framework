from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage

TEST_CARD = {
    "email": "example@gmail.com",
    "card": "4242424242424242",
    "expiry": "1234",
    "cvc": "123",
    "zip": "12345",
}


def test_buy_and_checkout(driver):
    home = HomePage(driver)
    products = ProductsPage(driver)
    cart = CartPage(driver)

    home.open()
    dept = home.choose_department()

    if dept == "moisturizer":
        products.add_cheapest("aloe")
        products.add_cheapest("almond")
    else:
        products.add_cheapest("spf-50")
        products.add_cheapest("spf-30")

    products.go_to_cart()
    cart.pay_with_card()
    cart.complete_stripe_checkout(TEST_CARD)
    assert cart.expect_success()
