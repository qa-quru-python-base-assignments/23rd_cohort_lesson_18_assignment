import os

import pytest
from dotenv import load_dotenv
from selene import browser

from src.api.cart_client import CartClient, Product
from src.api.login_client import LoginClient

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


@pytest.fixture()
def signed_in_user_cookie():
    email, password = os.getenv("EMAIL"), os.getenv("PASSWORD")

    response = LoginClient(BASE_URL).login(email, password)

    return {
        "NOPCOMMERCE.AUTH": response.cookies["NOPCOMMERCE.AUTH"]
    }


@pytest.fixture()
def cart_client(signed_in_user_cookie):
    return CartClient(BASE_URL, cookies=signed_in_user_cookie)


@pytest.fixture()
def setup_browser(signed_in_user_cookie):
    browser.config.base_url = BASE_URL
    browser.open("/")

    cookie_value = signed_in_user_cookie["NOPCOMMERCE.AUTH"]
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie_value})

    browser.driver.refresh()

    yield

    browser.quit()


@pytest.fixture()
def add_product_to_cart(cart_client):
    cart_client.add_to_cart(Product.SMARTPHONE, quantity=3)
    yield
    cart_client.remove_all_from_cart()
