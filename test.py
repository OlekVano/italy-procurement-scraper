import json

from helper_functions import obtem_info_contratos_release

with open('release4.json', 'r', encoding='utf-8') as f:
  release = json.load(f)

info_release = obtem_info_contratos_release(release)
print(json.dumps(info_release, indent=4))