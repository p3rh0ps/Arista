import requests
import json
from pprint import pprint

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CVP_HOST = "*********"
CVP_USER = "*********"
CVP_PASS = "*********"

url = f"https://{CVP_HOST}"
headers = { 'Content-Type': 'application/json' }
loginURL = "/web/login/authenticate.do"
authenticateData = json.dumps({'userId' : CVP_USER, 'password' : CVP_PASS})

auth_response = requests.post(url+loginURL,data=authenticateData,headers=headers,verify=False)
assert auth_response.ok

cookies = auth_response.cookies
output = auth_response.json()

print("User Name: {}".format(output['username']), end="\n-*-*-*-*-*-*-\n")
print("First Name: {}".format(output['user']['firstName']), end="\n-*-*-*-*-*-*-\n")
print("Last Name: {} ".format(output['user']['lastName']), end="\n-*-*-*-*-*-*-\n")
print("User Permissions: {}".format(output['permissionList']), end="\n-*-*-*-*-*-*-\n")
print("Cookie Jar: {}".format(cookies), end="\n-*-*-*-*-*-*-\n")

full_invent = {'inventory': 'false'}

url = f"https://{CVP_HOST}/cvpservice/inventory/devices"
invent_response = requests.get(url, cookies=cookies, headers=headers, verify=False, params=full_invent)

pprint(invent_response.json(), indent=4)
