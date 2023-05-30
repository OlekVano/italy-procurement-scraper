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

  award = obtem_award_por_id(release, contrato['id'])

  if 'suppliers' in award:
    for supplier in award['suppliers']:
      entidades_adjudicatarias.append(f"{supplier['name']} ({supplier['id']})")
  else:
    for party in release['parties']:
      if 'supplier' in party['roles']:
        entidades_adjudicatarias.append(party)

  return entidades_adjudicatarias

def obtem_cpvs(contrato):
  cpvs = []

  for item in contrato['items']:
    cpvs.append(f"{item['classification']['id']} {item['classification']['description']}")

  return cpvs

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

def obtem_data_celebracao(release, contrato):
  if 'dateSigned' in contrato:
    return contrato['dateSigned'][:10]
  if 'period' in contrato and 'startDate' in contrato['period']:
    return contrato['period']['startDate'][:10]
  if 'amendments' in contrato:
    return contrato['amendments'][-1]['date'][:10]
  
  return None

def obtem_data_fecho(contrato):
  return contrato['period']['endDate'][:10]

def obtem_prazo_execucao(release, contrato):
  data_assinatura = obtem_data_celebracao(release, contrato)

  if data_assinatura == None:
    return None

  data_assinatura = datetime.strptime(data_assinatura, FORMATO_DATAS)
  data_final = datetime.strptime(obtem_data_fecho(contrato), FORMATO_DATAS)
  diferenca = data_final - data_assinatura

  return f'{diferenca.days} dias'

def obtem_comprador_por_id(release, id):
  for party in release['parties']:
    if 'buyer' in party['roles']:
      return party

def obtem_local_execucao(release):
  comprador = obtem_comprador_por_id(release, release['buyer']['id'])

  if comprador == None:
    return None

  endereco_comprador = comprador['address']

  partes_local = []

  if 'countryName' in endereco_comprador:
    partes_local.append(comprador['address']['countryName'])
  if 'locality' in endereco_comprador:
    partes_local.append(comprador['address']['locality'])

  return ', '.join(partes_local)

def obtem_info_contrato(release, contrato):
  info = {
    'objeto_contrato': obtem_objeto_contrato(release),
    'tipo_procedimento': obtem_tipo_procedimento(release),
    'tipo_contrato': obtem_tipo_contrato(release),
    'cpvs': obtem_cpvs(contrato),
    'entidades_adjudicantes': [obtem_entidade_adjudicante(release)],
    'entidades_adjudicatarias': obtem_entidades_adjudicatarias(release, contrato),
    'preco_contratual': obtem_preco_contratual(contrato),
    'data_publicacao': obtem_data_publicacao(release),
    'data_celebracao': obtem_data_celebracao(release, contrato),
    'prazo_execucao': obtem_prazo_execucao(release, contrato),
    'local_execucao': obtem_local_execucao(release),
    'fundamentacao': 'NOT IMPLEMENTED',
    'data_fecho_contrato': obtem_data_fecho(contrato)
  }

  return info

def obtem_info_contratos_release(release):
  contratos = []

  if 'contracts' in release:
    for contrato in release['contracts']:
      contratos.append(obtem_info_contrato(release, contrato))
      
  return contratos