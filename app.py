from flask import Flask, request, jsonify
import base64
import json
from urllib.parse import quote

app = Flask(__name__)

# Baseline payload structure (can be expanded as needed)
BASELINE = {
    "Digitol Platform License Model Costs Incl 2CLIXZ_2.xlsx": {
        "Sheet1": {},
        "Incremental RS4_Plan A": {}
    }
}

@app.route("/", methods=["GET"])
def index():
    return "Digitol ROI Link Generator is running."

@app.route("/generate", methods=["POST"])
def generate_link():
    data = request.json
    if not data or "email" not in data:
        return jsonify({"error": "Missing required 'email' field."}), 400

    # Start with a copy of the baseline
    result = json.loads(json.dumps(BASELINE))  # deep copy

    # Always set Sheet1!X1 = 14 to jump to the ROI page
    sheet1 = result["Digitol Platform License Model Costs Incl 2CLIXZ_2.xlsx"]["Sheet1"]
    sheet1["X1"] = 14

    # Insert email into Sheet1!A1
    sheet1["A1"] = data["email"]

    # Apply additional user-provided cell values (excluding 'email')
    for key, value in data.items():
        if key == "email":
            continue
        sheet1[key] = value

    # Encode to base64 and generate the link
    encoded = base64.b64encode(json.dumps(result, separators=(',', ':')).encode()).decode()
    full_url = "https://digitolservices.com/ecommerce-deployment-roi?s=" + quote(encoded)
    return jsonify({"url": full_url})