import requests

response = requests.get("https://api.github.com/users/vlad-charle/repos")
projects = response.json()

for project in projects:
    print(project["name"])