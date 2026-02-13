import allure

from src.api.base_client import BaseClient


class LoginClient(BaseClient):
    @allure.step("Авторизация пользователя {email}")
    def login(self, email: str, password: str, remember_me: bool = False):
        self.logger.info(f"Авторизация: {email}")
        return self.post(
            "/login",
            data={"Email": email, "Password": password, "RememberMe": remember_me},
            allow_redirects=False
        )
