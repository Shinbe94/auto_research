from dataclasses import dataclass

import requests


@dataclass
class Response:
    status_code: int
    text: str
    as_dict: object
    headers: dict


class APIRequest:
    def get(self, url, headers) -> Response:
        response = requests.get(url, headers=headers)
        return self.__get_responses(response)

    def get_with_parameters(self, url, headers, parameters) -> Response:
        response = requests.get(url, params=parameters, headers=headers)
        return self.__get_responses(response)

    def post(self, url, payload, headers) -> Response:
        response = requests.post(url, data=payload, headers=headers)
        return self.__get_responses(response)

    def delete(self, url) -> Response:
        response = requests.delete(url)
        return self.__get_responses(response)

    @staticmethod
    def __get_responses(response: Response) -> Response:
        status_code = response.status_code
        text = response.text
        try:
            as_dict = response.json()
        except Exception:
            as_dict = {}
        headers = response.headers
        return Response(status_code, text, as_dict, headers)
