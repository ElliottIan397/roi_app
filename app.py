from flask import Flask, request, jsonify
import base64
import json
from urllib.parse import quote

app = Flask(__name__)

# Baseline model with full structure
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
            "C130": 0.005, "D124": 0.0015, "C127": 0.005,
            "BB151": 0, "C252": 0, "C247": 0, "BA147": 0, "BA148": 0
        }
    }
}

@app.route("/", methods=["GET"])
def index():
    return "Digitol ROI Link Generator with Summary is online."

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    if not data or "email" not in data:
        return jsonify({"error": "Missing required 'email' field."}), 400

    model = json.loads(json.dumps(BASELINE))  # deep copy
    sheets = model["Digitol Platform License Model Costs Incl 2CLIXZ_2.xlsx"]
    sheets["Sheet1"]["A1"] = data["email"]
    sheets["Sheet1"]["X1"] = 14

    for key, value in data.items():
        if key == "email":
            continue
        if key in sheets["Sheet1"]:
            sheets["Sheet1"][key] = value
        elif key in sheets["Incremental RS4_Plan A"]:
            sheets["Incremental RS4_Plan A"][key] = value
        else:
            sheets["Sheet1"][key] = value

    # Extract KPIs
    plan = sheets["Incremental RS4_Plan A"]
    kpi_sales = plan.get("BB151", 0)
    kpi_customers = plan.get("C252", 0)
    kpi_devices = plan.get("C247", 0)
    kpi_cabinets = plan.get("BA147", 0)
    kpi_replacement = plan.get("BA148", 0)

    summary = (
        f"To achieve a 4-year ROI of ${kpi_sales:,.0f}, you will need to:\n"
        f"- Install DCA at approximately {int(kpi_customers)} customers\n"
        f"- Build a hierarchy of {int(kpi_devices)} devices\n"
        f"- Establish VMI over {int(kpi_cabinets)} supply cabinets\n"
        f"- Capture {int(kpi_replacement)}% of asset replacement opportunities."
    )

    encoded = base64.b64encode(json.dumps(model, separators=(',', ':')).encode()).decode()
    full_url = "https://digitolservices.com/ecommerce-deployment-roi?s=" + quote(encoded)

    return jsonify({"url": full_url, "summary": summary})