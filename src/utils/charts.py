from datetime import datetime

EARLIEST_DATA_YEAR = 1995
CURRENT_YEAR = datetime.now().year


def _compute_transaction_count_by_year(transaction_df):
    df = transaction_df.copy()

    aggregated_df = df.groupby("year").count().transaction_id.reset_index()
    aggregated_df["transaction_count"] = aggregated_df.transaction_id
    transaction_count_by_year = {}

    for year, count in zip(aggregated_df.year, aggregated_df.transaction_count):
        try:
            year = int(year)
        except ValueError:
            continue
        transaction_count_by_year[year] = count

    output = {"label": [], "data": []}
    for year in range(EARLIEST_DATA_YEAR, CURRENT_YEAR + 1):
        output["label"].append(year)
        output["data"].append(transaction_count_by_year.get(year, 0))

    return output


def _compute_transaction_prices_by_year(transaction_df):
    df = transaction_df.copy()

    output = {"data": []}
    for year, price in zip(df.year, df.price_paid):
        try:
            year = int(year)
            output["data"].append({"x": year, "y": price})
        except ValueError:
            continue

    return output


def compute_charts_data(transaction_df):
    """Compute data required for different charts, in the format expected by Chart.js"""
    transaction_df["year"] = transaction_df.transaction_date.str[:4]
    charts_data = {
        "transactionCountByYear": _compute_transaction_count_by_year(transaction_df),
        "transactionPricesByYear": _compute_transaction_prices_by_year(transaction_df),
    }
    return charts_data
