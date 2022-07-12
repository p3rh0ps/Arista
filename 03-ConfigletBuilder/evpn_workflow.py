from cvplibrary import Form
from cvplibrary import GlobalVariables, GlobalVariableNames, Device

ip = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_IP)
user = "******"
passwd = "*******"

VRF = "Tenant1"
VLAN_ID = Form.getFieldById('VLAN_ID').getValue()
VNI = int(VLAN_ID) + 1000
anycast_addr = Form.getFieldById('anycast_addr').getValue()
netname = Form.getFieldById('netname').getValue()
password = Form.getFieldById('password').getValue()

def Conf_Vlandb(VLAN_ID):
    # Vlan creation
    print("")
    print("vlan {}".format(VLAN_ID))

def Conf_Svi(VLAN_ID, anycast_addr, VRF, netname):
    # Create SVI
    print("int vlan ".format(VLAN_ID))
    print(" description {}".format(netname))
    print(" vrf {}".format(VRF))
    print(" ip addr virtual {}/24".format(anycast_addr))
    print(" no autostate")

def Conf_Vti(VLAN_ID, VNI):
    # Associate VNI to VXLAN inside Virtual Tunnel Interface
    print("")
    print("int vxlan 1")
    print(" vxlan vlan {} vni {}".format(VLAN_ID, VNI))
    print("")

def get_bgpasn():
    # Retrieve BGP ASN from the switch to perform BGP configuration
    ss = Device(ip,user,passwd)
    show_ip_bgp_summary = ss.runCmds(["enable", {"cmd": "show ip bgp summary"}])[1]
    ASN = show_ip_bgp_summary['response']['vrfs']['default']['asn']
    return ASN

def Conf_Bgpevpn(VLAN_ID, VNI):
    # BGP EVPN configuration statement supplement
    ASN = get_bgpasn()
    print("")
    print("router BGP {}".format(ASN))
    print(" vlan {}".format(VLAN_ID))
    print("  rd auto")
    print("  route-target both {}:{}".format(VNI, VNI))
    print("  redistribute learned")
    print("")

Conf_Vlandb(VLAN_ID)
Conf_Vti(VLAN_ID, VNI)
Conf_Svi(VLAN_ID, anycast_addr, VRF, netname)
Conf_Bgpevpn(VLAN_ID)