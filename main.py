import json

from helper_functions import obtem_info_contratos_dataset, obtem_info_contratos_release

with open('04.json', 'r', encoding='utf-8') as f:
  dataset = json.load(f)

result = obtem_info_contratos_dataset(dataset)

with open('result.json', 'w', encoding='utf-8') as f:
  json.dump(result, f, indent=4)