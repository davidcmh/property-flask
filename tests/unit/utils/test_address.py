from src.utils.address import get_address


class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code


def test_get_address_404_response_returns_error_msg(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(404)

    monkeypatch.setattr("src.utils.address.requests.get", mock_get)

    actual_output = get_address("abc")
    expected_output = {"error_message": 'Postcode "ABC" cannot be found. Please try another postcode.'}

    assert actual_output == expected_output


def test_get_address_500_response_returns_error_msg(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(500)

    monkeypatch.setattr("src.utils.address.requests.get", mock_get)

    actual_output = get_address("abc")
    expected_output = {"error_message": "There is an error. Please try again."}

    assert actual_output == expected_output
