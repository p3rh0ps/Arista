import urllib2, json, jsonrpclib
import cvp
from cvplibrary import Form, CVPGlobalVariables, GlobalVariableNames

# Get Devices information

mac = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_MAC)
ip = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_IP)
ztp = CVPGlobalVariables.getValue(GlobalVariableNames.ZTP_STATE) 

NET_NAME = Form.getFieldById('NET_NAME').getValue()
VLAN_ID = Form.getFieldById('VLAN_ID').getValue()
IPv4_ADDR = Form.getFieldById('IPv4_ADDR').getValue()
IPv4_MASK = Form.getFieldById('IPv4_MASK').getValue()

print("Network: {}".format(NET_NAME))
print("Vlan: {}".format(VLAN_ID))
print("ipv4 Address: {}".format(IPv4_ADDR))
print("ipv4 Netmask: {}".format(IPv4_MASK))

# MAC_ADDR = "00:01:02:03:04:05"

# url = "https://192.168.0.4:8181/ipam/arista/mgmtbymac.php?mac={}".format(mac)
# response = urllib2.urlopen(url))

print(dir(GlobalVariableNames))