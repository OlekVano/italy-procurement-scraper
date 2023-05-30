import requests

BASE_URL = 'https://api.anticorruzione.it/opendata/ocds/api/v1/1.0.0'

print('Version')
r = requests.get(f'{BASE_URL}/version')
print(r.status_code) # 200
print(r.content) #

print('something that shouldnt work')
r = requests.get(f'{BASE_URL}/something/that/shouldnt/work')
print(r.status_code) # code 404
print(r.content) # html page saying not found

print('stats')
r = requests.get(f'{BASE_URL}/stats')
print(r.status_code) # 200 OK
print(r.content) # Failure in connecting to Dremio: cdjd.com.dremio.exec.rpc.ConnectionFailedException: CONNECTION....

print('all active tenders')
r = requests.get(f'{BASE_URL}/tender/id/count/active')
print(r.status_code) # 200 OK
print(r.content) # Failure in connecting to Dremio: cdjd.com.dremio.exec.rpc.ConnectionFailedException: CONNECTION....

print('all tenders')
r = requests.get(f'{BASE_URL}/tender/id/count/all')
print(r.status_code) # 200 OK
print(r.content) # Failure in connecting to Dremio: cdjd.com.dremio.exec.rpc.ConnectionFailedException: CONNECTION....