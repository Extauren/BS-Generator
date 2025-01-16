import os
import json
from pyairtable import Api
from pyairtable.formulas import match
from dotenv import load_dotenv

nom_complet: str = ""
sexe: str = ""

load_dotenv()

api = Api(os.environ['API_KEY'])
table = api.table(os.environ['BASE_ID'], os.environ['TABLE_TEST'])
with open("pappers.json", "r") as f:
    pappers_data: json = json.load(f)
for data in pappers_data["papper"]:
    if len(data["data"]["representants"]) > 0:
            nom_complet = data["data"]["representants"][0]["nom_complet"]
            try:
                sexe = data["data"]["representants"][0]["sexe"]
            except:
                sexe = ""
    table.create({
       'nom_entreprise': data["data"]["nom_entreprise"],
       'nom_complet': nom_complet,
       'sexe' : sexe,
       # mail
       'siren': data["siren"],
       'greffe': data["data"]["greffe"],
       'forme_juridique': data["data"]["forme_juridique"]
       # siege social deux option siege ou etablissement
    })