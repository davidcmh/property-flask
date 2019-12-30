from datetime import datetime

EARLIEST_DATA_YEAR = 1995
CURRENT_YEAR = datetime.now().year


def _compute_transaction_count_by_year(transaction_df):
    df = transaction_df.copy()
    df["year"] = transaction_df.transaction_date.str[:4]

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


def compute_charts_data(transaction_df):
    charts_data = {"transactionCountByYear": _compute_transaction_count_by_year(transaction_df)}
    return charts_data
