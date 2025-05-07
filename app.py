from flask import Flask, request, jsonify
import base64
import json
from urllib.parse import quote

app = Flask(__name__)

# Baseline payload structure (you can replace this with your actual decoded baseline)
BASELINE = {
    "Digitol Platform License Model Costs Incl 2CLIXZ_2.xlsx": {
        "Sheet1": {},
        "Incremental RS4_Plan A": {}
    }
}

@app.route("/", methods=["GET"])
def index():
    return "Digitol Link Generator is running!"

@app.route("/generate", methods=["POST"])
def generate_link():
    data = request.json
    if not data or "email" not in data:
        return jsonify({"error": "Missing email field"}), 400

    # Copy baseline and inject user data
    updated = json.loads(json.dumps(BASELINE))  # deep copy
    updated["Digitol Platform License Model Costs Incl 2CLIXZ_2.xlsx"]["Sheet1"]["A1"] = data["email"]

    for k, v in data.items():
        if k == "email":
            continue
        # Assume all input fields are Sheet1 cells by default
        updated["Digitol Platform License Model Costs Incl 2CLIXZ_2.xlsx"]["Sheet1"][k] = v

    # Encode and build URL
    encoded = base64.b64encode(json.dumps(updated, separators=(',', ':')).encode()).decode()
    full_url = "https://digitolservices.com/ecommerce-deployment-roi?s=" + quote(encoded)
    return jsonify({"url": full_url})