import urllib2, json, jsonrpclib
import cvp
from cvplibrary import Form, CVPGlobalVariables, GlobalVariableNames

# Get Devices information

mac = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_MAC)
ip = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_IP)
ztp = CVPGlobalVariables.getValue(GlobalVariableNames.ZTP_STATE) 

if ztp == 'true':
    user = CVPGlobalVariables.getValue(GlobalVariableNames.ZTP_USERNAME)
    passwd = CVPGlobalVariables.getValue(GlobalVariableNames.ZTP_PASSWORD)
else:
    user = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_USERNAME)
    passwd = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_PASSWORD)

print(dir(GlobalVariableNames))

print("*"*20+"Field ID"+"*"*20)
print(Form.getFieldById('NET_NAME').getFieldID())
print("*"*20+"Help Text"+"*"*20)
print(Form.getFieldById('NET_NAME').isMandatory())
print("*"*20+"Help Text"+"*"*20)
print(Form.getFieldById('NET_NAME').getHelpText())
print("*"*20+"Depends on"+"*"*20)
print(Form.getFieldById('NET_NAME').getDependsOn())
print("*"*20+"Type"+"*"*20)
print(Form.getFieldById('NET_NAME').getType())
print("*"*20+"Type"+"*"*20)
print(Form.getFieldById('NET_NAME').getDataValidation())

NET_NAME = Form.getFieldById('NET_NAME').getValue()
VLAN_ID = Form.getFieldById('VLAN_ID').getValue()
IPv4_ADDR = Form.getFieldById('IPv4_ADDR').getValue()
IPv4_MASK = Form.getFieldById('IPv4_MASK').getValue()

print("Network: {}".format(NET_NAME))
print("Vlan: {}".format(VLAN_ID))
print("ipv4 Address: {}".format(IPv4_ADDR))
print("ipv4 Netmask: {}".format(IPv4_MASK))

# MAC_ADDR = "00:01:02:03:04:05"

url = "https://192.168.0.4:8181/ipam/arista/mgmtbymac.php?mac={}".format(mac)
response = urllib2.urlopen(url))
hostjson = json.loads(response.read())

# Process JSON from IPAM

host = hostjson['host']
hostname = host['hostname']
ip = host['ip']
mask = host['mask']

# Generate and Print config

print("hostname {}".format(hostname))
print("!")

print("interface Management 1")
print(" ip address {}/{}".format(ip, mask))
print(" no lldp transmit")
print(" no lldp receive")
print("!")
print("ip name server vrf default 192.168.0.2")
print("ip domain-name arista.test")
print("!")
print("ip route 0.0.0.0/0 192.168.0.1")
print("!")
print("ip routing")
print("!")
print("management api http-commands")
print(" no shutdown")
