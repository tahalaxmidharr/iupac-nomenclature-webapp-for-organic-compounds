from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import quote

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-iupac", methods=["POST"])
def get_iupac():
    data = request.get_json()
    smiles = data.get("smiles", "").strip()

    if not smiles:
        return jsonify({"error": "No molecular structure detected."}), 400

    # Safely encode the SMILES string for web transmission
    encoded_smiles = quote(smiles, safe='')
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{encoded_smiles}/property/IUPACName/JSON"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            pubchem_data = response.json()
            iupac_name = pubchem_data["PropertyTable"]["Properties"][0]["IUPACName"]
            return jsonify({"iupac_name": iupac_name, "smiles": smiles})

        elif response.status_code == 404:
            return jsonify({"error": "Compound not found in the PubChem database."}), 404
        else:
            return jsonify({"error": f"API error (Status code: {response.status_code})"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)