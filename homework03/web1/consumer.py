import requests

response = requests.get(url="http://localhost:5011/animals")

print(response.status_code)
print(response.json())
print(response.headers)


response = requests.get(url="http://localhost:5011/animals/head/bunny")

print(response.status_code)
print(response.json())
print(response.headers)


response = requests.get(url="http://localhost:5011/animals/legs/6")

print(response.status_code)
print(response.json())
print(response.headers)
