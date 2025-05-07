from flask import Flask, request, jsonify
import base64
import json
from urllib.parse import quote

app = Flask(__name__)

# Static baseline (update this with actual full baseline values if needed)
BASELINE = {
    "Digitol Platform License Model Costs Incl 2CLIXZ_2.xlsx": {
        "Sheet1": {
            # A1 will be replaced with email
        },
        "Incremental RS4_Plan A": {
            # Placeholder; user-supplied values can go here if specified
        }
    }
}

@app.route("/", methods=["GET"])
def index():
    return "Digitol ROI Link Generator is online."

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    if not data or "email" not in data:
        return jsonify({"error": "Missing required 'email' field."}), 400

    # Deep copy of the baseline to avoid mutation
    model = json.loads(json.dumps(BASELINE))

    sheet1 = model["Digitol Platform License Model Costs Incl 2CLIXZ_2.xlsx"]["Sheet1"]
    plan_a = model["Digitol Platform License Model Costs Incl 2CLIXZ_2.xlsx"]["Incremental RS4_Plan A"]

    # Required: insert email and X1 to skip to ROI page
    sheet1["A1"] = data["email"]
    sheet1["X1"] = 14

    # Insert all other user-defined inputs into Sheet1 by default
    for key, value in data.items():
        if key == "email":
            continue
        # Default all input keys to Sheet1 (you can customize per key if needed)
        sheet1[key] = value

    # Encode and return the URL
    encoded = base64.b64encode(json.dumps(model, separators=(',', ':')).encode()).decode()
    full_url = "https://digitolservices.com/ecommerce-deployment-roi?s=" + quote(encoded)
    return jsonify({"url": full_url})