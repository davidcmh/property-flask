from datetime import datetime

import pandas as pd
import pytest

from src.utils.charts import _compute_transaction_count_by_year, _compute_transaction_prices_by_year


@pytest.fixture(scope="module")
def transaction_df():
    cols = ["transaction_id", "year", "price_paid"]
    test_data = [
        [1, 1996, 300],
        [2, 1996, 250],
        [3, 1996, 500],
        [4, 1998, 600],
        [5, 1998, 800],
        [6, 1999, 200],
    ]
    return pd.DataFrame(test_data, columns=cols)


def test_compute_transaction_count_by_year(transaction_df):
    current_year = datetime.now().year

    actual_output = _compute_transaction_count_by_year(transaction_df)
    expected_output = {
        "label": list(range(1995, current_year + 1)),
        "data": [0, 3, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }

    assert actual_output == expected_output


def test_compute_transaction_prices_by_year(transaction_df):
    actual_output = _compute_transaction_prices_by_year(transaction_df)
    expected_output = {
        "data": [
            {"x": 1996, "y": 300},
            {"x": 1996, "y": 250},
            {"x": 1996, "y": 500},
            {"x": 1998, "y": 600},
            {"x": 1998, "y": 800},
            {"x": 1999, "y": 200},
        ]
    }

    assert actual_output == expected_output
