from urllib import parse

from flask import Flask, render_template, request
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
    return res.text


if __name__ == "__main__":
    app.run(debug=True)
