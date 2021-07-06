import requests
BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "note/5", data={'name': 'My First Name', 'title': 'My First Title', 'body': 'My First Body'})
print(f'Put Response: {response.json()}')
response = requests.patch(BASE + "note/5", data={'title':'my UPDATED first title'}) # delete method
# not sending json serializable object
print(f'Patch Response: {response.json()}')