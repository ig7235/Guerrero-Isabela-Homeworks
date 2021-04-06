import requests

response = requests.get(url="http://localhost:50XXX/animals")

print(response.status_code)
print(response.json())
print(response.headers)

response = requests.get(url="http://localhost:50XXX/animals/head/bunny")

print(response.status_code)
print(response.json())
print(response.headers)

response = requests.get(url="http://localhost:50XXX/animals/legs/6")

print(response.status_code)
print(response.json())
print(response.headers)
