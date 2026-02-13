import allure
from selene import browser, have

from src.api.cart_client import Product
from src.pages.cart_page import CartPage


@allure.feature("Корзина")
@allure.story("Добавление товара")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("API", "UI", "Cart")
@allure.title("Добавление товара в корзину через API и проверка через UI")
def test_add_product_to_cart_via_api(cart_client, setup_browser):
    with allure.step("Добавить Smartphone (кол-во: 2) через API"):
        cart_client.add_to_cart(Product.SMARTPHONE, quantity=2)

    with allure.step("Открыть страницу корзины в браузере"):
        page = CartPage(base_url=browser.config.base_url)
        page.open()

    with allure.step("Проверить, что Smartphone с кол-вом 2 отображается в корзине"):
        assert "Smartphone" in page.cart_items
        assert page.cart_items["Smartphone"] == "2"

    with allure.step("Очистить корзину"):
        cart_client.remove_all_from_cart()


@allure.feature("Корзина")
@allure.story("Удаление товара")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("API", "UI", "Cart")
@allure.title("Удаление товара из корзины через API и проверка пустой корзины через UI")
def test_remove_product_from_cart_via_api(cart_client, setup_browser):
    with allure.step("Добавить и удалить Smartphone через API"):
        cart_client.add_to_cart(Product.SMARTPHONE, quantity=1)
        cart_client.remove_all_from_cart()

    with allure.step("Открыть страницу корзины в браузере"):
        browser.open("/cart")

    with allure.step("Проверить, что корзина пуста"):
        browser.element(".order-summary-content").should(
            have.text("Your Shopping Cart is empty!")
        )


@allure.feature("Корзина")
@allure.story("Добавление нескольких товаров")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("API", "UI", "Cart")
@allure.title("Добавление нескольких разных товаров в корзину через API")
def test_add_multiple_products_via_api(cart_client, setup_browser):
    with allure.step("Добавить Smartphone и 14.1-inch Laptop через API"):
        cart_client.add_to_cart(Product.SMARTPHONE, quantity=1)
        cart_client.add_to_cart(Product.LAPTOP_14, quantity=1)

    with allure.step("Открыть страницу корзины в браузере"):
        page = CartPage(base_url=browser.config.base_url)
        page.open()

    with allure.step("Проверить, что оба товара отображаются в корзине"):
        assert "Smartphone" in page.cart_items
        assert "14.1-inch Laptop" in page.cart_items

    with allure.step("Очистить корзину"):
        cart_client.remove_all_from_cart()


@allure.feature("Корзина")
@allure.story("Изменение количества")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("API", "UI", "Cart")
@allure.title("Изменение количества товара в корзине через API")
def test_update_quantity_via_api(cart_client, setup_browser):
    with allure.step("Добавить Smartphone дважды через API (1 + 2)"):
        cart_client.add_to_cart(Product.SMARTPHONE, quantity=1)
        cart_client.add_to_cart(Product.SMARTPHONE, quantity=2)

    with allure.step("Открыть страницу корзины в браузере"):
        page = CartPage(base_url=browser.config.base_url)
        page.open()

    with allure.step("Проверить, что итоговое количество Smartphone = 3"):
        assert "Smartphone" in page.cart_items
        assert page.cart_items["Smartphone"] == "3"

    with allure.step("Очистить корзину"):
        cart_client.remove_all_from_cart()


@allure.feature("Корзина")
@allure.story("Добавление товара")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("API", "UI", "Cart", "Fixture")
@allure.title("Проверка корзины с предустановленным товаром из фикстуры")
def test_cart_with_fixture_product(add_product_to_cart, setup_browser):
    with allure.step("Открыть страницу корзины (товар добавлен фикстурой)"):
        page = CartPage(base_url=browser.config.base_url)
        page.open()

    with allure.step("Проверить, что Smartphone с кол-вом 3 отображается в корзине"):
        assert "Smartphone" in page.cart_items
        assert page.cart_items["Smartphone"] == "3"
