import requests


def fetch_iupac_from_pubchem(smiles):
    # Construct endpoint URL
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/IUPACName/JSON"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Parse nested JSON keys
        iupac_name = data["PropertyTable"]["Properties"][0]["IUPACName"]
        return iupac_name
    elif response.status_code == 404:
        return "Compound not found in database."
    else:
        return "API request failed."


# Example test
print(fetch_iupac_from_pubchem("C1=CC=CC=C1"))
# Output: 2-acetoxybenzoic acid