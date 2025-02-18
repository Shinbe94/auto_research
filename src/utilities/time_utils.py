from datetime import datetime, timedelta
from src.utilities import string_number_utils


def get_time():
    from datetime import datetime

    return ((str(datetime.now())).split(" ")[1]).split(".")[0]


def test_get_time():
    print(get_time())


def get_hour():
    from datetime import datetime

    return (((str(datetime.now())).split(" ")[1]).split(".")[0]).split(":")[0]


def test_get_hour():
    print(get_hour())


def get_minute():
    from datetime import datetime

    return (((str(datetime.now())).split(" ")[1]).split(".")[0]).split(":")[1]


def test_get_minute():
    print(get_minute())


def get_second():
    from datetime import datetime

    return (((str(datetime.now())).split(" ")[1]).split(".")[0]).split(":")[2]


def get_milli_second():
    from datetime import datetime

    return (str(datetime.now())).split(".")[1]


def n_minutes_after_current(n):
    now = datetime.now()
    now_plus_n = now + timedelta(minutes=n)
    return now_plus_n


def test_n_minutes_after_current():
    print(n_minutes_after_current(1))
    print("abc" + str(n_minutes_after_current(1))[11:16])
    print(str(n_minutes_after_current(1))[11:16])
