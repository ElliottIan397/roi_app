from flask import Flask, request, jsonify
import base64
import json
from urllib.parse import quote

app = Flask(__name__)

# Full baseline from decoded scenario
BASELINE = {
    "Digitol Platform License Model Costs Incl 2CLIXZ_2.xlsx": {
        "Questionaire": {
            "C3": 1, "C7": "Yes", "D8": "EVO-X", "E19": "No", "E20": "Yes", "E21": "Yes", "E22": "Partially",
            "E23": "No", "E24": "Don't Know", "E25": "Partially", "E26": "Yes", "A19": 5, "F37": "Yes",
            "E39": "No", "E28": "Yes", "F36": "Yes", "E30": "No", "E32": "Yes", "E33": "Yes", "E34": "Yes",
            "E35": "Yes", "F41": "26-50%", "H53": "$251-$500", "F46": "Somewhat", "D48": "Occasionally",
            "D50": "Don't know", "J49": "Yes", "L50": "Email Mkting", "L51": "Probably Not", "D53": "Agree",
            "D54": "Agree", "D55": "Agree", "D56": "Agree"
        },
        "Sheet1": {
            "X1": 14, "AN40": "On", "AN46": "On", "AN43": "On", "AN41": "On", "AN45": "On",
            "A1": "Ian.Elliott@aegCapitalPartners.com"
        },
        "Incremental RS4_Plan A": {
            "C130": 0.005, "D124": 0.0015, "C127": 0.005
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

    # Deep copy baseline
    model = json.loads(json.dumps(BASELINE))
    sheets = model["Digitol Platform License Model Costs Incl 2CLIXZ_2.xlsx"]

    # Always set email and navigation
    sheets["Sheet1"]["A1"] = data["email"]
    sheets["Sheet1"]["X1"] = 14

    # Inject any submitted values into Sheet1 or Plan A if known
    for key, value in data.items():
        if key == "email":
            continue
        if key in sheets["Sheet1"]:
            sheets["Sheet1"][key] = value
        elif key in sheets["Incremental RS4_Plan A"]:
            sheets["Incremental RS4_Plan A"][key] = value
        else:
            sheets["Sheet1"][key] = value

    # Encode and return URL
    encoded = base64.b64encode(json.dumps(model, separators=(',', ':')).encode()).decode()
    full_url = "https://digitolservices.com/ecommerce-deployment-roi?s=" + quote(encoded)
    return jsonify({"url": full_url})