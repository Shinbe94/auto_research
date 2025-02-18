import pytest

from src.utilities import os_utils, file_utils


@pytest.fixture(autouse=True)
def clean_all_crash_dump():
    """
    To clean all crash dump before and after test
    Returns:
    """
    folder = rf"C:\Users\{os_utils.get_username()}\AppData\Local\CocCoc\Browser\User Data\Crashpad\reports"
    file_utils.remove_all_crash_dump(directory=folder)
    yield
    file_utils.remove_all_crash_dump(directory=folder)
