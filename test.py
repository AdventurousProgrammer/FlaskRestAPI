import requests
BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "note/5", data={'name': 'My First Name', 'title': 'My First Title', 'body': 'My First Body'})
print(f'Put Response: {response}')
response = requests.get(BASE + "note/6") # delete method
# not sending json serializable object
print(f'Get Response: {response.json()}')