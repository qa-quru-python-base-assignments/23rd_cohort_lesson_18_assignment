from enum import Enum

from bs4 import BeautifulSoup

from src.api.base_client import BaseClient


class Product(Enum):
    SMARTPHONE = 43
    LAPTOP_14 = 31
    VIRTUAL_GIFT_CARD_25 = 2


class CartClient(BaseClient):
    def add_to_cart(self, product: Product, quantity: int):
        self.post(
            endpoint=f"/addproducttocart/catalog/{product.value}/1/{quantity}"
        )

    def remove_all_from_cart(self):
        cart_endpoint = "/cart"

        cart_response = self.get(cart_endpoint)

        soup = BeautifulSoup(cart_response.text, 'html.parser')
        remove_checkboxes = soup.find_all("input", {"name": "removefromcart"})

        if remove_checkboxes:
            payload = [
                ("removefromcart", cb.get("value")) for cb in remove_checkboxes
            ]
            payload.append(("updatecart", "Update shopping cart"))
            self.post(cart_endpoint, data=payload)
