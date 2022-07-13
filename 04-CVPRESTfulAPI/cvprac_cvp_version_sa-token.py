from cvprac.cvp_client import CvpClient
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

token = open('./SAOne.token', 'r')
clnt = CvpClient()
clnt.connect(nodes=['192.168.0.5'], username='',password='',api_token=token.readlines()[0])
print(clnt.api.get_cvp_info())
token.close()
# Expected output {'version': '2021.3.0'}