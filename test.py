import requests
BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "note/1", data={'name': 'My First Name', 'title': 'My First Title', 'body': 'My First Body'})
print(f'Put Response: {response.json()}')
response = requests.delete(BASE + "note/1") # delete method
# not sending json serializable object
print(f'Delete Response: {response}')