import os
import json
from pyairtable import Api
from pyairtable.formulas import match
from dotenv import load_dotenv

nom_complet: str = ""
sexe: str = ""
structure: str = ""
count: int = 0

load_dotenv()

api = Api(os.environ['API_KEY'])
table = api.table(os.environ['BASE_ID'], os.environ['TABLE_TEST'])
with open("pappers.json", "r") as f:
    pappers_data: json = json.load(f)
for data in pappers_data["papper"]:
    structure = data["data"]["nom_entreprise"]
    airtable = table.first(formula=match({"Structure": structure}))
    if airtable is not None:
        count += 1
        if len(data["data"]["representants"]) > 0:
                nom_complet = data["data"]["representants"][0]["nom_complet"]
                try:
                    sexe = data["data"]["representants"][0]["sexe"]
                except:
                    sexe = ""
        table.update(airtable['id'], {
            'nom_complet': nom_complet,
            'sexe' : sexe,
            'RCS': data["siren"],
            'Ville RCS': data["data"]["greffe"],
            'forme_juridique': data["data"]["forme_juridique"],
            'Siège social': data["data"]["siege"]["adresse_ligne_1"]
        })
print(count)