import requests
response = requests.get("https://meowfacts.herokuapp.com/?id=3")
print(response.json())
