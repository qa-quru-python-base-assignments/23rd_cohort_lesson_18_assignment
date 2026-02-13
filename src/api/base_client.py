import allure
import requests

from src.utils.allure_attach import attach_request_response
from src.utils.logger import setup_logger


class BaseClient:
    def __init__(self, base_url: str, cookies: dict = None):
        self.base_url = base_url
        self.session = requests.Session()
        self.cookies = cookies

        self.logger = setup_logger(self.__class__.__name__)

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"

        with allure.step(f"API {method} {endpoint}"):
            self.logger.info(f"Request: {method} {url}")

            try:
                response = self.session.request(method, url, cookies=self.cookies, **kwargs)
                self.logger.info(f"Response: {response.status_code}")

                attach_request_response(
                    method=method,
                    endpoint=endpoint,
                    response=response,
                )

                return response
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}")
                raise

    def get(self, endpoint: str, params: dict = None, **kwargs):
        return self._request('GET', endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: dict = None, json: dict = None, **kwargs):
        return self._request('POST', endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint: str, json: dict = None, **kwargs):
        return self._request('PUT', endpoint, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)
