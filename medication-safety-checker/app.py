from flask import Flask, jsonify, render_template, request
from itertools import combinations
from pathlib import Path
import json

app = Flask(__name__)

DATA_FILE = Path(__file__).parent / "data" / "interactions.json"

def load_interactions():
    """Load illustrative demo rules. These are not clinical decision support data."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({"status": "healthy", "service": "medication-safety-checker"}), 200

@app.post("/api/check")
def check_interactions():
    payload = request.get_json(silent=True) or {}
    medicines = payload.get("medicines", [])

    if not isinstance(medicines, list):
        return jsonify({"error": "'medicines' must be a list."}), 400

    cleaned = []
    seen = set()
    for item in medicines:
        if not isinstance(item, str):
            continue
        name = item.strip()
        key = name.casefold()
        if name and key not in seen:
            cleaned.append(name)
            seen.add(key)

    if len(cleaned) < 2:
        return jsonify({
            "error": "Enter at least two medicine names to check.",
            "interactions": [],
            "medicines": cleaned
        }), 400

    rules = load_interactions()
    lookup = {}
    for rule in rules:
        a, b = sorted([rule["medicine_a"].casefold(), rule["medicine_b"].casefold()])
        lookup[(a, b)] = rule

    results = []
    for first, second in combinations(cleaned, 2):
        pair = tuple(sorted([first.casefold(), second.casefold()]))
        rule = lookup.get(pair)
        if rule:
            results.append({
                "medicine_a": first,
                "medicine_b": second,
                "severity": rule["severity"],
                "description": rule["description"],
                "demo_only": True
            })

    return jsonify({
        "medicines": cleaned,
        "checked_pairs": len(list(combinations(cleaned, 2))),
        "interactions_found": len(results),
        "interactions": results,
        "notice": "This is an educational software demonstration using illustrative sample rules. It is not validated medical information and must not be used to make treatment decisions."
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
