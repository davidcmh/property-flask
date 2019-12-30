import copy
from io import StringIO

import requests
import pandas as pd


form_data_template = {
    "output": "csv",
    "url": "/landregistry/query",
    "q": """
        prefix lrppi: <http://landregistry.data.gov.uk/def/ppi/>
        prefix lrcommon: <http://landregistry.data.gov.uk/def/common/>

        SELECT *
        WHERE
        {{
          ?transaction_record a lrppi:TransactionRecord;
                            lrppi:propertyAddress ?address.
          ?address lrcommon:postcode ?postcode.
          VALUES ?postcode {{ "{postcode}" }}

          OPTIONAL {{?address lrcommon:county ?county}}
          OPTIONAL {{?address lrcommon:paon ?paon}}
          OPTIONAL {{?address lrcommon:saon ?saon}}
          OPTIONAL {{?address lrcommon:street ?street}}
          OPTIONAL {{?address lrcommon:town ?town}}
          OPTIONAL {{?transaction_record lrppi:hasTransaction ?has_transaction}}
          OPTIONAL {{?transaction_record lrppi:estateType ?estate_type}}
          OPTIONAL {{?transaction_record lrppi:propertyType ?property_type}}
          OPTIONAL {{?transaction_record lrppi:recordStatus ?record_status}}
          OPTIONAL {{?transaction_record lrppi:transactionCategory ?transaction_category}}
          OPTIONAL {{?transaction_record lrppi:pricePaid ?price_paid}}
          OPTIONAL {{?transaction_record lrppi:transactionDate ?transaction_date}}
          OPTIONAL {{?transaction_record lrppi:transactionId ?transaction_id}}
        }}
    """,
}


def _convert_csv_str_to_dataframe(csv_str):
    f = StringIO(csv_str)
    df = pd.read_csv(f)
    return df


def get_transactions(postcode):
    """Get transaction data from Land Registry API and return data as dataframe"""
    form_data = copy.deepcopy(form_data_template)
    form_data["q"] = form_data["q"].format(postcode=postcode)
    r = requests.post("http://landregistry.data.gov.uk/app/root/qonsole/query", data=form_data)
    if r.status_code != 200:
        raise Exception("Failed to execute transaction API.")

    result = r.json().get("result")
    if result is None:
        raise Exception("No result was returned from transaction API.")

    df = _convert_csv_str_to_dataframe(result).sort_values("transaction_date", ascending=False)

    return df
