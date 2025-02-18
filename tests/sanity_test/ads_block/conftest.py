import pytest, requests


@pytest.fixture()
def get_safe_browsing_data() -> str:
    try:
        r = requests.get(f"https://safe-browsing-api.coccoc.com/api/v2/get_unsafe_urls")
    except Exception as e:
        raise e
    else:
        data = r.json()
        return len(data["domains"]) + len(data["urls"])  # Return version
