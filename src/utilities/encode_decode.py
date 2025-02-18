import base64
import urllib.parse

from src.utilities import string_number_utils


def decode_base64(encoded_str):
    return base64.b64decode(encoded_str)


def test_decode_base64():
    print(
        decode_base64(
            encoded_str="CAISDwgGEMKNCBj+PyIAKgAyABoYNTNQMkt6dVVnRk9NaVp0Wnc0NW9IQS4uIgA="
        )
    )


def format_base64_after_decoded(encoded_str):
    string = str(decode_base64(encoded_str))
    is_format_done = False
    # temp1 = string.split("}", 1)[1]
    # temp2 = temp1.split('\\')[2][3:][:-1]
    while not is_format_done:
        if r"\x18" in string:
            string = string.split(r"\x18", 1)[1]
        else:
            break
    # remove last 6 chars
    string = string[:-6]
    return string


def test_format_base64_after_decoded(
    encoded_str="CAISDwgGEMKNCBj/FyIAKgAyABoYZ2JqTlZnQTEySWJLTzc3YVlENS0xUS4uIgA=",
):
    print(decode_base64(encoded_str=encoded_str))
    print(format_base64_after_decoded(encoded_str=encoded_str))


def url_decode(url) -> str:
    return urllib.parse.unquote(url)
