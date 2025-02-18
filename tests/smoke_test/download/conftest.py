import pytest

from src.utilities import file_utils


@pytest.fixture()
def remove_installer_downloaded():
    file_utils.delete_installer_downloaded()
    yield
    file_utils.delete_installer_downloaded()
