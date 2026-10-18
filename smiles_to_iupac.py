import requests
from urllib.parse import quote


def fetch_iupac_from_pubchem(smiles):
    # 1. Safely encode special characters like #, /, \, etc., for URL usage
    encoded_smiles = quote(smiles, safe='')

    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{encoded_smiles}/property/IUPACName/JSON"

    try:
        # Add a timeout so your app doesn't freeze if the API lags
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            iupac_name = data["PropertyTable"]["Properties"][0]["IUPACName"]
            return iupac_name

        elif response.status_code == 404:
            return "Compound not found in the PubChem database."
        else:
            return f"API error: Received status code {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Network error occurred: {e}"


# Example test with a triple bond (Acetylene / Ethyne: C#C)
print(fetch_iupac_from_pubchem("C#C"))