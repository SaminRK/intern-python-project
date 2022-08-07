from time import perf_counter
from urllib.error import HTTPError

from auth import auth_manager
from env import BASE_URL
from util import NetworkRequest


def create_user(username: str, firstname: str, lastname: str, password: str):
    user_dict = {
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "password": password,
    }
    response = NetworkRequest.post(
        BASE_URL + "/api/users",
        body=user_dict,
        headers={"Content-type": "application/json"},
    )
    return response


def retry_on_stale_token(fn):
    def wrapper_fn(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            if isinstance(e, HTTPError):
                e: HTTPError
                print(e.getcode())
                if e.getcode() == 401:
                    print("Request failed due to unauthorized access. Retrying with fresh token.")
                    auth_manager.refresh_tokens()
                    return fn(*args, **kwargs)
            raise e

    return wrapper_fn


def print_execution_time(fn):
    def wrapper_fn(*args, **kwargs):
        start_time = perf_counter()
        ret = fn(*args, **kwargs)
        end_time = perf_counter()
        print(f"(Time taken {end_time - start_time} seconds)")

        return ret

    return wrapper_fn


@print_execution_time
@retry_on_stale_token
def post_tweet(text: str):
    auth_token, _, _ = auth_manager.get_auth_tokens()

    response = NetworkRequest.post(
        BASE_URL + "/api/tweets",
        body={"text": text},
        decode_json=True,
        headers={
            "Content-type": "application/json",
            "authorization": "Bearer " + auth_token,
        },
    )

    return response["code"]


@print_execution_time
@retry_on_stale_token
def get_tweets():
    auth_token, _, _ = auth_manager.get_auth_tokens()

    response = NetworkRequest.get(
        BASE_URL + "/api/tweets",
        decode_json=True,
        headers={
            "Content-type": "application/json",
            "authorization": "Bearer " + auth_token,
        },
    )

    return response["body"]
