import os
import math
import json
from babel.dates import format_datetime
from datetime import datetime
from num2words import num2words
import numpy as np
from pyairtable import Api

class Data:
    __api = None
    __structure: str = None
    __siege_social: str = None
    __legal_email: str = None
    __legal_lastname: str = None
    __legal_firstname: str = None
    __legal_type: str = None
    __rcs: str = None
    __city: str = None
    __forme_social: str = None
    __postal_code: str = None
    __montant_investi: str = None
    __montant_investi_letter: str = None
    __price_letter: str = None
    __tribunal_name: str = None
    __montant_souscription: str = None
    __montant_souscription_letter: str = None
    __action_seed: int = None
    __action_name: str = None
    __iban_img = None
    __action_price: str = None
    __iban: str = None
    __siege_social_addr: str = None
    __part_sociales: str = None
    __part_sociales_letter: str = None
    __frais_entre: str = None
    __frais_entre_letter: str = None
    __iban_techmind: str = None
    __date: str = None
    __gender: str = None
    __entries_fee_pourcentage: str = None
    __target_name: str = None
    __target_addr: str = None
    __target_rcs: str = None
    __status_date: str = None
    __bsa_air: str = "False"
    __montant_total: str = None
    __total_letter: str = None
    __bank_name: str = None

    def __init__(self, structure: str, bsa_air: bool) -> None:
        self.__api = Api(os.environ['API_KEY'])
        self.__get_airtable_data(structure)
        self.__get_target_data()
        self.__get_pappers_data()
        self.__calc_action_seed()
        self.__frais_entre = self.__set_entries_fee()
        self.__montant_souscription = self.__calc_montant_souscription()
        self.__action_seed = self.__convert_price_to_fr(str(self.__action_seed))
        self.__montant_souscription_letter = self.__convert_price_in_letter(self.__montant_souscription)
        self.__price_letter = self.__convert_price_in_letter(self.__montant_investi)
        self.__part_sociales = self.__calc_part_sociale()
        self.__part_sociales_letter = self.__convert_price_in_letter(self.__part_sociales)
        self.__frais_entre_letter = self.__convert_price_in_letter(self.__frais_entre)
        self.__montant_investi_letter = self.__convert_price_in_letter(self.__montant_investi)
        self.__total_letter = self.__convert_price_in_letter(self.__montant_total)
        self.__set_date()
        self.__set_gender_in_letter()
        if bsa_air:
            self.__bsa_air = True

    def __convert_price_to_fr(self, price: str) -> str:
        price_fr: str = price.replace(".", ",")
        price_list: list = price_fr.split(',')
        price_list_len: int = len(price_list[0])
        price_space_nb: int = (int(math.trunc(price_list_len) / 3))
        fst_price_list: list = list(price_list[0])

        for i in range(price_space_nb):
            if (price_list_len - ((i + 1) * 3)) != 0:
                fst_price_list.insert((price_list_len - ((i + 1) * 3)), " ")
        if len(price_list) == 2:
            return (''.join(map(str,fst_price_list)) + ',' + price_list[1])
        return (''.join(map(str,fst_price_list)))
        # fix: too many decimal number

    def __convert_price_in_letter(self, price: str) -> str:
        price_list: list = []
        price_letter_list: list = []
        price_fr: str = ""

        price = price.replace(" ", "").replace("€", "")
        price_list = price.split(',')
        for price in price_list:
            price_letter_list.append(num2words(price, lang='fr'))
        price_fr = price_letter_list[0] + " euros"
        if len(price_list) == 2:
            if price_letter_list[1] != "zéro":
                price_fr += " et " + price_letter_list[1] + " centimes"
        return price_fr

    def __calc_part_sociale(self) -> str:
        montant_souscription_nb: float = float(self.__montant_souscription.replace(",", ".").replace(" ", ""))
        self.__part_social: str = str(int(montant_souscription_nb * 100))

        return self.__convert_price_to_fr(self.__part_social)

    def __set_gender_in_letter(self) -> None:
        if self.__gender == "Male":
            self.__gender = "Monsieur"
        else:
            self._gender = "Madame"

    def __set_entries_fee(self) -> str:
        pourcentage_float: float = int(self.__entries_fee_pourcentage[0]) / 100
        montant_investi_int = float(self.__montant_investi.replace(",", ".").replace(" ", ""))
        self.__entries_fee: str = "{:.2f}".format(montant_investi_int * pourcentage_float)

        return self.__convert_price_to_fr(self.__entries_fee)

    def __calc_action_seed(self) -> None:
        montant_nb: float = float(self.__montant_investi.replace(",", ".").replace(" ", ""))
        action_price_nb: float = float(self.__action_price.replace(",", ".").replace(" ", ""))
        
        self.__action_seed = int(np.ceil(montant_nb / action_price_nb))

    def __calc_montant_souscription(self) -> float:
        action_price_nb = float(self.__action_price.replace(" ", "").replace(",", "."))
        montant: str = "{:.2f}".format(self.__action_seed * action_price_nb)

        return self.__convert_price_to_fr(montant)

    def __get_target_data(self) -> None:
        table = self.__api.table(os.environ['BASE_ID'], os.environ['TABLE_TARGET'])
        records = table.all()
        for record in records:
            if record['fields'] != {}:
                self.__target_name = record['fields']['Nom de la société cible']
                self.__target_addr = record['fields']['Adresse de la société cible']
                self.__target_rcs = record['fields']['RCS de la société cible']
                self.__status_date = record['fields']['Date des statuts']
                self.__montant_total = record['fields']['Montant total investi']
                self.__action_name = record['fields']['Nom action']
                self.__action_price = record['fields']['Prix par action'][:-1]
                self.__iban = record['fields']['IBAN SPV']
                self.__iban_techmind = record['fields']['IBAN Frais']
                self.__bank_name = record['fields']['Nom de la banque']
                return
        print("Error: cannot get target data from airtable")
        exit()

    def __get_airtable_data(self, structure: str) -> None:
        get_data: bool = False
        table = self.__api.table(os.environ['BASE_ID'], os.environ['TABLE_NAME'])
        records = table.all()

        self.__structure = structure
        for record in records:
            if record != {} and record['fields'] != {}:
                try:
                    if structure == record['fields']['Structure']:
                        self.__siege_social = record['fields']['Siège social']
                        self.__legal_firstname = record['fields']['Prénom']
                        self.__legal_lastname = record['fields']['Nom']
                        self.__legal_email = record['fields']['Mail']
                        self.__legal_type = record['fields']["L'investissement est-il réalisé à titre personnel ou via une holding ?"]
                        self.__rcs = record['fields']['RCS']
                        self.__city = record['fields']['Ville']
                        try:
                            self.__forme_social = record['fields']['Forme juridique']
                        except:
                            self.__forme_social = None
                        self.__postal_code = record['fields']['Code postal']
                        self.__montant_investi = record['fields']['Montant investi'][:-1]
                        self.__gender = record['fields']['M/F']
                        self.__entries_fee_pourcentage = record['fields']['Frais']
                        self.__iban_img = record['fields']['Image IBAN SPV']
                        self.__iban_img = self.__iban_img[0]["url"]
                        get_data = True
                        break
                except Exception as e:
                    print(e)
        if not get_data:
            print("Error: get data from airtable failed")
            exit()

    def __get_pappers_data(self) -> None:
        pappers_data: json = None

        with open("pappers.json", "r") as f:
            pappers_data = json.load(f)
        for data in pappers_data["papper"]:
            if data["siren"] == self.__rcs.replace(" ", ""):
                self.__tribunal_name = data["data"]["greffe"] #to vérify
                self.__siege_social_addr = data["data"]["siege"]["adresse_ligne_1"] # addr ligne 2 ?
                return
        print("Error: cannot get data from pappers")
        exit()

    def __set_date(self) -> None:
        self.__date = format_datetime(datetime.now(), "dd MMMM yyyy", locale='fr_FR')