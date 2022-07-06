from cvplibrary import Device

ip = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_IP)
user = "arista"
passwd = "arista1"

def Vlan_db(VLAN_ID):
    # Vlan creation
    print("")
    print("vlan {}".format(VLAN_ID))

def SVI(VLAN_ID, anycast_addr, VRF, netname):
    # Create SVI
    print("int vlan ".format(VLAN_ID))
    print(" description {}".format(netname))
    print(" vrf {}".format(VRF))
    print(" ip addr virtual {}/24".format(anycast_addr))
    print(" no autostate")

def VTI(VLAN_ID, VNI):
    # Associate VNI to VXLAN inside Virtual Tunnel Interface
    print("")
    print("int vxlan 1")
    print(" vxlan vlan {} vni {}".format(VLAN_ID, VNI))
    print("")

def BGP_EVPN(VLAN_ID, VNI):
    # BGP EVPN configuration statement supplement
    print("")
    print("router BGP {}".format(ASN
    print(" vlan {}".format(VLAN_ID))
    print("  rd auto")
    print("  route-target both {}:{}".format(VNI, VNI))
    print("  redistribute learned")
    print("")

