import allure
from selene import browser, query

from src.utils.logger import setup_logger

logger = setup_logger("CartPage")


class CartPage:
    def __init__(self, base_url: str, sign_in_cookie: dict = None):
        self.base_url = base_url
        self.sign_in_cookie = {"name": "NOPCOMMERCE.AUTH", "value": sign_in_cookie}

    @allure.step("Открыть страницу корзины")
    def open(self):
        logger.info("Открываем страницу /cart")
        browser.open("/cart")
        return self

    @property
    def cart_items(self):
        with allure.step("Получить список товаров в корзине"):
            rows = browser.all('.cart-item-row')
            cart_data = {}

            for row in rows:
                name = row.element('.product-name').get(query.text)
                quantity = row.element('.qty-input').get(query.value)
                cart_data[name] = quantity

            logger.info(f"Товары в корзине: {cart_data}")
            return cart_data
