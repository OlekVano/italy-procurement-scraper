import json
from datetime import datetime

FORMATO_DATAS = '%Y-%m-%d'

def obtem_objeto_contrato(release):
  return release['tender']['description']

def obtem_tipo_procedimento(release):
  return release['tender']['procurementMethodDetails']

def obtem_tipo_contrato(release):
  return release['tender']['mainProcurementCategory']

def obtem_entidade_adjudicante(release):
  return f"{release['buyer']['name']} ({release['buyer']['id']})"

def obtem_award_por_id(release, id):
  for award in release['awards']:
    if (award['id'] == id):
      return award

def obtem_entidades_adjudicatarias(release, contrato):
  entidades_adjudicatarias = []
  
  award = obtem_award_por_id(contrato['id'])

  for supplier in award['suppliers']:
    entidades_adjudicatarias.append(f"{supplier['name']} ({supplier['id']})")

  return entidades_adjudicatarias

def obtem_cpvs(contrato):
  cpvs = []

  for item in contrato['items']:
    cpvs.append(f"{item['classification']['id']} {item['classification']['description']}")

def obtem_preco_contratual(contrato):
  moedas = {}
  for item in contrato['items']:
    try:
      moedas[item['unit']['value']['currency']] += item['unit']['value']['amount']
    except:
      moedas[item['unit']['value']['currency']] = item['unit']['value']['amount']
  
  output = ''

  for moeda, quantidade in moedas.items():
    if output != '':
      output += '; '
    output += f"{quantidade} {moeda}"

  return output

def obtem_data_publicacao(release):
  return release['date'][:10]

def obtem_data_celebracao(contrato):
  return contrato['dateSigned']
  
def obtem_prazo_execucao(contrato):
  data_assinatura = datetime.strptime(contrato['dateSigned'], FORMATO_DATAS)
  data_final = datetime.strptime(contrato['period']['endDate'], FORMATO_DATAS)

  diferenca = data_final - data_assinatura

  return f'{diferenca.days} dias'

def obtem_comprador_por_id(release, id):
  for party in release['parties']:
    if 'buyer' in party['roles']:
      return party

def obtem_local_execucao(release):
  comprador = obtem_comprador_por_id(release, release['buyer'['id']])
  endereco_comprador = comprador['address']

  partes_local = []
  chaves_endereco = endereco_comprador.keys()

  if 'countryName' in chaves_endereco:
    partes_local.append(comprador['address']['countryName'])
  if 'locality' in chaves_endereco:
    partes_local.append(comprador['address']['locality'])

  return ', '.join(partes_local)

def obtem_data_fecho(contrato):
  return contrato['period']['endDate'][:10]

def obtem_info_contrato(release, contrato):
  info = {
    'objeto_contrato': obtem_objeto_contrato(release),
    'tipo_procedimento': obtem_tipo_procedimento(release),
    'tipo_contrato': obtem_tipo_contrato(release),
    'cpvs': obtem_cpvs(contrato),
    'entidade_adjudicante': obtem_entidade_adjudicante(release),
    'entidade_adjudicataria': obtem_entidades_adjudicatarias(release, contrato),
    'preco_contratual': obtem_preco_contratual,
    'data_publicacao': obtem_data_publicacao(release),
    'data_celebracao': obtem_data_celebracao(release),
    'prazo_execucao': obtem_prazo_execucao(contrato),
    'local_execucao': obtem_local_execucao(),
    'fundamentacao': 'NOT IMPLEMENTED',
    'data_fecho_contrato': obtem_data_fecho(contrato)
  }

  return info

def obtem_info_contratos_release(release):
  contratos = []

  for contrato in release['contracts']:
    contratos.append(obtem_info_contrato(release, contrato))
  
  return contratos