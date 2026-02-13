from enum import Enum

import allure
from bs4 import BeautifulSoup

from src.api.base_client import BaseClient


class Product(Enum):
    SMARTPHONE = 43
    LAPTOP_14 = 31
    VIRTUAL_GIFT_CARD_25 = 2


class CartClient(BaseClient):
    @allure.step("Добавить товар {product} в корзину (кол-во: {quantity})")
    def add_to_cart(self, product: Product, quantity: int):
        self.logger.info(f"Добавляем товар {product.name} (id={product.value}), кол-во: {quantity}")
        self.post(
            endpoint=f"/addproducttocart/catalog/{product.value}/1/{quantity}"
        )

    @allure.step("Удалить все товары из корзины")
    def remove_all_from_cart(self):
        cart_endpoint = "/cart"

        cart_response = self.get(cart_endpoint)

        soup = BeautifulSoup(cart_response.text, 'html.parser')
        remove_checkboxes = soup.find_all("input", {"name": "removefromcart"})

        if remove_checkboxes:
            self.logger.info(f"Найдено товаров в корзине: {len(remove_checkboxes)}, удаляем все")
            payload = [
                ("removefromcart", cb.get("value")) for cb in remove_checkboxes
            ]
            payload.append(("updatecart", "Update shopping cart"))
            self.post(cart_endpoint, data=payload)
        else:
            self.logger.info("Корзина уже пуста")
