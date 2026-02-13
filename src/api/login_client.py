from src.api.base_client import BaseClient


class LoginClient(BaseClient):
    def login(self, email: str, password: str, remember_me: bool = False):
        return self.post(
            "/login",
            data={"Email": email, "Password": password, "RememberMe": remember_me},
            allow_redirects=False
        )
