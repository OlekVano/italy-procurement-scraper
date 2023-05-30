import json

from helper_functions import obtem_info_contratos_release

with open('dataset.json', 'r', encoding='utf-8') as f:
  dataset = json.load(f)

releases = dataset['releases']

def main():
  for i in range(len(releases)):
    try:
      info_release = obtem_info_contratos_release(releases[i])
      print(json.dumps(info_release, indent=4))
    except:
      print(i)
      with open(f'release{i}.json', 'w') as f:
        json.dump(releases[i], f, indent=4)
      return
    
main()