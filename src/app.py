import os

from flask import Flask, render_template, request, jsonify
from flask_googlemaps import GoogleMaps, Map

from src.utils import GENERIC_ERROR_MSG
from src.utils.address import get_address
from src.utils.charts import compute_charts_data
from src.utils.transactions import get_transactions, InvalidTransactionsResponseError

app = Flask(__name__)
app.config["GOOGLEMAPS_KEY"] = os.environ.get("GOOGLE_API_KEY")
GoogleMaps(app)


@app.route("/")
def index():
    default_latlng = (51.52349, -0.144435)  # latLng for 'W1W 5PN'

    google_map = Map(
        identifier="google-map",
        lat=default_latlng[0],
        lng=default_latlng[1],
        style="height:400px;width:100%;margin:0;",
        maptype_control=False,
        fullscreen_control=False,
        streetview_control=False,
    )

    return render_template("index.html", google_map=google_map)


@app.route("/postcode", methods=["POST"])
def postcode():
    """Get address and transactions data for specified postcode,
    and compute data for charts to be displayed
    """
    address = get_address(request.form.get("postcode"))
    if "error_message" in address:
        return jsonify({"success": False, "errorMessage": address["error_message"]})
    else:
        try:
            transaction_df = get_transactions(address["postcode"])
        except InvalidTransactionsResponseError:
            return jsonify({"success": False, "errorMessage": GENERIC_ERROR_MSG})
        else:
            charts_data = compute_charts_data(transaction_df)
            return jsonify(
                {
                    "success": True,
                    "address": address,
                    "transactions": transaction_df.to_dict(orient="record"),
                    "charts": charts_data,
                }
            )


if __name__ == "__main__":
    app.run(debug=True)
