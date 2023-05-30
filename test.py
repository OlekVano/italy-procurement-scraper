import json
from datetime import datetime

with open('01.json', 'r', encoding='utf-8') as f:
  dataset = json.load(f)

def obtem_objeto_contrato(release):
  return release['tender']['description']

def obtem_tipo_procedimento(release):
  return release['tender']['procurementMethodDetails']

def obtem_tipo_contrato(release):
  return release['tender']['mainProcurementCategory']



def obtem_info_release(release):
  output = {
    'objeto_contrato': None,
    'tipo_procedimento': None,
    'tipo_contrato': None,
    'cpvs': [],
    'entidade_adjucante': None,
    'entidades_adjucatarias': [],
    'preco_contratual': None,
    'data_publicacao': None,
    'data_celebracao_contrato': [],
    'prazo_execucao': None,
    'local_execucao': None,
    'fundamentacao': None,
    'data_fecho_contrato': None
  }

  output['objeto_contrato'] = release['tender']['description']
  output['tipo_procedimento'] = release['tender']['procurementMethodDetails']
  output['tipo_contrato'] = release['tender']['mainProcurementCategory']

  for award in release['awards']:
    for item in award['items']:
      output['cpvs'].append(f"{item['classification']['id']} {item['classification']['description']}")
    for supplier in award['suppliers']:
      output['entidades_adjucatarias'].append(f"{supplier['name']} ({supplier['id']})")

  output['entidade_adjucante'] = f"{release['buyer']['name']} ({release['buyer']['id']})"

  output['preco_contratual'] = f"{release['tender']['lots'][0]['value']['amount']} {release['tender']['lots'][0]['value']['currency']}"

  output['data_publicacao'] = release['date'][:10]

  output['data_celebracao_contrato'] = release['contracts'][0]['dateSigned'][:10]

  output['data_fecho_contrato'] = release['contracts'][0]['period']['endDate'][:10]
  

  # calcular prazo de execucao
  formato_data = '%Y-%m-%d'
  data_celebracao = datetime.strptime(output['data_celebracao_contrato'], formato_data)
  data_final = datetime.strptime(output['data_fecho_contrato'], formato_data)
  diferenca = data_final - data_celebracao
  output['prazo_execucao'] = f"{diferenca.days} dias"

  endereco_buyer = release['parties'][0]['address']
  output['local_execucao'] = f"{endereco_buyer['countryName']}, {endereco_buyer['locality']}"

  return output

release = dataset['releases'][0]
print(json.dumps(release, indent=4))
print(json.dumps(map_release(release), indent=4))