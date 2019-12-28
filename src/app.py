import os
from urllib import parse

from flask import Flask, render_template, request, jsonify
from flask_googlemaps import GoogleMaps, Map
import requests

from .utils import get_transactions


app = Flask(__name__)
app.config["GOOGLEMAPS_KEY"] = os.environ.get("GOOGLE_API_KEY")
GoogleMaps(app)


@app.route("/")
def index():
    default_latlng = (51.52349, -0.144435)  # latLng for W1W 5PN

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
    """Get postcode info from postcodes.io"""
    input_postcode = request.form.get("postcode")
    res = requests.get(f"https://postcodes.io/postcodes/{parse.quote(input_postcode)}")

    if res.status_code != 200:
        return jsonify({"success": False})

    data = res.json()

    transaction_df = get_transactions(data["result"]["postcode"])

    return jsonify(
        {"success": True, "address": data["result"], "transactions": transaction_df.to_dict(orient="record")}
    )


if __name__ == "__main__":
    app.run(debug=True)
