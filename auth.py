from env import BASE_URL
from util import NetworkRequest


class AuthManager:
    def __init__(self) -> None:
        self._username = None
        self._password = None
        self._access_token = None
        self._refresh_token = None
        self._token_type = None

    def set_username_password(self, username: str, password: str) -> None:
        self._username = username
        self._password = password

    def _get_auth_tokens(self) -> None:
        if self._username is None or self._password is None:
            raise ValueError("username and/or password is not provided to AuthManager")

        response = NetworkRequest.post(
            BASE_URL + "/api/auth",
            body={"username": self._username, "password": self._password},
            headers={"Content-type": "application/json"},
            decode_json=True,
        )
        body = response["body"]
        self._access_token = body["access_token"]
        self._refresh_token = body["refresh_token"]
        self._token_type = body["token_type"]

    def get_auth_tokens(self) -> tuple[str, str, str]:
        if self._access_token is None:
            self._get_auth_tokens()

        return self._access_token, self._refresh_token, self._token_type

    def refresh_tokens(self) -> None:
        if self._refresh_token is None:
            self.get_auth_tokens()
            return

        response = NetworkRequest.post(
            BASE_URL + "/api/auth/token",
            body={"refresh_token": self._refresh_token},
            headers={"Content-type": "application/json"},
            decode_json=True,
        )
        body = response["body"]
        self._access_token = body["access_token"]
        self._refresh_token = body["refresh_token"]
        self._token_type = body["token_type"]


auth_manager = AuthManager()
