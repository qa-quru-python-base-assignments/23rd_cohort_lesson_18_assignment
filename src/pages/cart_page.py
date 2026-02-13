from selene import browser, query


class CartPage:
    def __init__(self, base_url: str, sign_in_cookie: dict = None):
        self.base_url = base_url
        self.sign_in_cookie = {"name": "NOPCOMMERCE.AUTH", "value": sign_in_cookie}

    def open(self):
        browser.open("/cart")
        return self

    @property
    def cart_items(self):
        rows = browser.all('.cart-item-row')
        cart_data = {}

        for row in rows:
            name = row.element('.product-name').get(query.text)
            quantity = row.element('.qty-input').get(query.value)

            cart_data[name] = quantity

        return cart_data
