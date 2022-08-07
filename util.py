import json
from http.client import HTTPResponse
from typing import Optional
from urllib.request import Request, urlopen


class NetworkRequest:
    @staticmethod
    def __request__(url: str, method: str, headers={}, data: Optional[dict] = None, decode_json=False) -> dict:
        if data is not None:
            data = json.dumps(data).encode("utf-8")
        req = Request(url=url, method=method, data=data)
        for key, value in headers.items():
            req.add_header(key, value)

        result = {}
        with urlopen(req) as res:
            res: HTTPResponse
            body = res.read().decode("utf-8")
            if decode_json:
                result["body"] = json.loads(body)
            else:
                result["body"] = body
            result["code"] = res.status

        return result

    @staticmethod
    def get(url, headers={}, decode_json=False) -> dict:
        return NetworkRequest.__request__(url=url, method="GET", headers=headers, decode_json=decode_json)

    @staticmethod
    def post(url, headers={}, body: Optional[dict] = None, decode_json=False) -> dict:
        return NetworkRequest.__request__(url=url, method="POST", headers=headers, data=body, decode_json=decode_json)

    @staticmethod
    def put(url, headers={}, body: Optional[dict] = None, decode_json=False) -> dict:
        return NetworkRequest.__request__(url=url, method="PUT", headers=headers, data=body, decode_json=decode_json)

    @staticmethod
    def delete(url, headers={}, body: Optional[dict] = None, decode_json=False) -> dict:
        return NetworkRequest.__request__(url=url, method="DELETE", headers=headers, data=body, decode_json=decode_json)
