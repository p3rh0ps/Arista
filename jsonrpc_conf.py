import requests

url = "https://leaf1/command-api"

commands = open("eth1.json", "r")

r = requests.post(url, auth=('user','passwd'), data=commands, verify=False) 

print(r.text)
