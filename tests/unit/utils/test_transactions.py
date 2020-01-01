import pandas as pd
import pytest

from src.utils.transactions import _convert_csv_str_to_dataframe, get_transactions, InvalidTransactionsResponseError


class MockResponse:
    def __init__(self, status_code=200, result=""):
        self.status_code = status_code
        self.result = result

    def json(self):
        return {"result": self.result}


def test_convert_csv_str_to_dataframe():
    col_names = "col1,col2,col3"
    row1 = "a,b,c"
    row2 = "d,,f"
    test_str = f"{col_names}\r\n{row1}\r\n{row2}"

    actual_df = _convert_csv_str_to_dataframe(test_str)

    expected_df = pd.DataFrame([row1.split(","), row2.split(",")], columns=col_names.split(","))

    assert actual_df.equals(expected_df)


def test_get_transactions_404_response_raises_error(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse(status_code=404)

    monkeypatch.setattr("src.utils.transactions.requests.post", mock_post)

    with pytest.raises(InvalidTransactionsResponseError):
        get_transactions("abc")


def test_get_transactions_empty_result_string_raises_error(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse(result="")

    monkeypatch.setattr("src.utils.transactions.requests.post", mock_post)

    with pytest.raises(InvalidTransactionsResponseError):
        get_transactions("abc")
