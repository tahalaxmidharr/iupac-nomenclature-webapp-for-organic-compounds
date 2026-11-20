from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import quote

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-iupac", methods=["POST"])

@app.route("/get-iupac", methods=["POST"])
def get_iupac():
    data = request.get_json(silent=True) or {}
    smiles = data.get("smiles", "").strip()

    if not smiles:
        return jsonify({"error": "No molecular structure detected."}), 400

    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
        "compound/smiles/property/IUPACName/JSON"
    )

    try:
        # Send SMILES as form data instead of embedding it in the URL.
        response = requests.post(
            url,
            data={"smiles": smiles},
            timeout=15
        )

        if not response.ok:
            try:
                details = response.json()
            except ValueError:
                details = response.text[:300]

            return jsonify({
                "error": "PubChem could not process this structure.",
                "details": details,
                "smiles": smiles
            }), 502

        pubchem_data = response.json()

        # Check every level instead of assuming IUPACName exists.
        properties = (
            pubchem_data.get("PropertyTable", {})
            .get("Properties", [])
        )

        if not properties or not properties[0].get("IUPACName"):
            return jsonify({
                "error": "PubChem returned no IUPAC name for this structure.",
                "smiles": smiles,
                "pubchem_response": pubchem_data
            }), 502

        iupac_name = properties[0]["IUPACName"]

        return jsonify({
            "iupac_name": iupac_name,
            "smiles": smiles
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Could not connect to PubChem.",
            "details": str(e)
        }), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
