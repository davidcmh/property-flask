from urllib import parse

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/postcode", methods=["POST"])
def postcode():
    """Get postcode info from postcodes.io"""
    input_postcode = request.form.get("postcode")
    res = requests.get(f"https://postcodes.io/postcodes/{parse.quote(input_postcode)}")

    if res.status_code != 200:
        return jsonify({"success": False})

    data = res.json()
    return jsonify({"success": True, "result": data["result"]})


if __name__ == "__main__":
    app.run(debug=True)
