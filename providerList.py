import requests
import json

data = requests.Session().get("https://apis.justwatch.com/content/providers/locale/en_US").json()

out = {}
for ele in data:
    if "flatrate" in ele["monetization_types"]:
        out[ele["id"]] = ele["clear_name"]

open("out.txt","w").write(json.dumps(out, indent="  ", sort_keys=True))
