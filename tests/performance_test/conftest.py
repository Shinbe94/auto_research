import pytest
from datetime import datetime

from src.utilities import file_utils


@pytest.fixture(autouse=True, scope="module")
def zip_all_results_file():
    file_utils.remove_files_re(
        directory=str(file_utils.get_project_root())
        + r"\tests\performance_test\test_result",
        filename_re="results",
    )
    yield
    file_utils.zip_all_file_with_no_path_added(
        filename=rf'WIN_PERFORMANCE_RESULTS_{datetime.now().strftime("%Y-%m-%d %H_%M_%S.zip")}',
        dir_path=str(file_utils.get_project_root())
        + r"\tests\performance_test\test_result",
    )
