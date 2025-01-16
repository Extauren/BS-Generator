import requests
import json

data: list = []
item: json = {}

with open("pappers.json", "a") as save:
    with open("rcs_list.txt", "r") as f:
        for line in f:
            res = requests.get(url)
            if res.status_code == 200 or res.status_code == 206:
                item = {'siren': line.replace(" ", "")[:-1], 'data': res.json()}
                data.append(item)
    json.dump(data, save, ensure_ascii=False, indent=4)