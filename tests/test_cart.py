import allure
from selene import browser, have

from src.api.cart_client import Product
from src.pages.cart_page import CartPage


@allure.title("Добавление товара в корзину через API и проверка через UI")
def test_add_product_to_cart_via_api(cart_client, setup_browser):
    # Arrange
    cart_client.add_to_cart(Product.SMARTPHONE, quantity=2)

    # Act
    page = CartPage(base_url=browser.config.base_url)
    page.open()

    # Assert
    assert "Smartphone" in page.cart_items
    assert page.cart_items["Smartphone"] == "2"

    # Cleanup
    cart_client.remove_all_from_cart()


@allure.title("Удаление товара из корзины через API и проверка пустой корзины через UI")
def test_remove_product_from_cart_via_api(cart_client, setup_browser):
    # Arrange — добавляем и удаляем товар через API
    cart_client.add_to_cart(Product.SMARTPHONE, quantity=1)
    cart_client.remove_all_from_cart()

    # Act
    browser.open("/cart")

    # Assert — корзина пуста
    browser.element(".order-summary-content").should(
        have.text("Your Shopping Cart is empty!")
    )


@allure.title("Добавление нескольких разных товаров в корзину через API")
def test_add_multiple_products_via_api(cart_client, setup_browser):
    # Arrange
    cart_client.add_to_cart(Product.SMARTPHONE, quantity=1)
    cart_client.add_to_cart(Product.LAPTOP_14, quantity=1)

    # Act
    page = CartPage(base_url=browser.config.base_url)
    page.open()

    # Assert
    assert "Smartphone" in page.cart_items
    assert "14.1-inch Laptop" in page.cart_items

    # Cleanup
    cart_client.remove_all_from_cart()


@allure.title("Изменение количества товара в корзине через API")
def test_update_quantity_via_api(cart_client, setup_browser):
    # Arrange — добавляем товар дважды через API (количество суммируется)
    cart_client.add_to_cart(Product.SMARTPHONE, quantity=1)
    cart_client.add_to_cart(Product.SMARTPHONE, quantity=2)

    # Act
    page = CartPage(base_url=browser.config.base_url)
    page.open()

    # Assert — итоговое количество = 3
    assert "Smartphone" in page.cart_items
    assert page.cart_items["Smartphone"] == "3"

    # Cleanup
    cart_client.remove_all_from_cart()


@allure.title("Проверка корзины с предустановленным товаром из фикстуры")
def test_cart_with_fixture_product(add_product_to_cart, setup_browser):
    # Act — фикстура add_product_to_cart уже добавила 3 Smartphone
    page = CartPage(base_url=browser.config.base_url)
    page.open()

    # Assert
    assert "Smartphone" in page.cart_items
    assert page.cart_items["Smartphone"] == "3"
