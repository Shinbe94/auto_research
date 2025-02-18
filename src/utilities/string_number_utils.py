import uuid


def find_text_between_2_string(text, first, last):
    try:
        start = text.index(first) + len(first)
        end = text.index(last, start)
        return text[start:end]
    except ValueError:
        return ""


def substring_after(string, delimiter):
    return string.partition(delimiter)[2]


def substring_before_char(string, char):
    sub_string = ""
    for s in string:
        if s is not char:
            sub_string = sub_string + s
        else:
            break
    return sub_string


def test_split():
    print("102.1.1.0".split(".", 1)[0])


def substring_before_string(string, string_delimiter):
    return string.split(string_delimiter, 1)[1]


def get_string_between_2_str(string, first_str, second_str):
    sub_first = string.split(first_str, 1)[1]
    sub_second = sub_first.split(second_str, 1)[0]
    return sub_second


def test_get_string_between_2_str():
    print(
        get_string_between_2_str(
            "/uninstall?hl=vi&crversion=76.0.3809.132&os=10.0.17763",
            "crversion=",
            "&os",
        )
    )
    print(
        get_string_between_2_str(
            "108.0.5359.128_from_108.0.5359.100_coccocsetup.exe",
            "from_",
            "_coccocsetup.exe",
        )
    )


def test_substring_before_string():
    print(
        substring_before_string(
            "/uninstall?hl=vi&crversion=76.0.3809.132&os=10.0.17763", "crversion="
        )
    )


def test_sub():
    print(substring_after("00:11/00:12", "/"))
    print(substring_after("0:04 of 1:57", "of "))
    print(substring_before_char("mp2/mp4/Medium/480p", "/"))


def format_timing_duration(media_length):
    # Format to fit with HH:MM:SS
    if len(media_length) == 4:
        media_length = "00:0" + media_length
    elif len(media_length) == 5:
        media_length = "00:" + media_length
    elif len(media_length) == 7:
        media_length = "0" + media_length
    return media_length


def generate_array_uuid(array_length):
    array = []
    for i in range(array_length):
        array.append(str(uuid.uuid4()))
    return array


def test_generate_array_uuid():
    print(generate_array_uuid(600))
