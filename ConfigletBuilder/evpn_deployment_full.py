import yaml
from cvplibrary import RestClient, CVPGlobalVariables,GlobalVariableNames
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
# Do not check certificates while using RESTful API Session

switch = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)
# Retrieve switch labels information

for item in switch:
    key, value = item.split(':')
    if key == 'hostname':
        hostname = value
# Iterate through the list and catch hostname of the switch

CVP_IP = '192.168.0.5'
# Cloud Vision Portal IP

cvp_api_url = 'https://{}/cvpservice/'.format(CVP_IP)
configlet_underlay_datafile = 'underlay.yml'

cvp_full_url = cvp_api_url+'configlet/getConfigletByName.do?name='+configlet_underlay_datafile
rest_method = 'GET'

rest_client = RestClient(cvp_full_url, rest_method)
# RESTful API Construct

if rest_client.connect():
    raw_data = rest_client.getResponse()

underlay_raw_data = yaml.safe_load(raw_data)
underlay = yaml.safe_load(underlay_raw_data['config'])

#
# Global EVPN Variables
#

MTU = underlay['global']['MTU']
# Global MTU for Fabric Ethernet interface
 
PREFIX_LIST = """
ip prefix-list LOOPBACK
    seq 10 permit 192.168.101.0/24 eq 32
    seq 20 permit 192.168.102.0/24 eq 32
    seq 30 permit 192.168.201.0/24 eq 32
    seq 40 permit 192.168.202.0/24 eq 32
route-map LOOPBACK permit 10
  match ip address prefix-list LOOPBACK
"""
# Prefix-list to redistribute loopbacks IP Range

PEER_RANGE = """
peer-filter LEAF-AS-RANGE
 10 match as-range 65000-65535 result accept
"""
# Match all Private AS used by the MP-BGP EVPN Fabric

#
# End Global EVPN Variables
#

#
# Below CVP ConfigletBuilder function often never return values
# As their purpose is to create configuration via print function
#

#
# Function to generate Fabric and Loopback interfaces configuration
#

def gen_int(device):
    for iface in underlay[device]['interfaces']:
      print("interface {}".format(iface))
      ip = underlay[device]['interfaces'][iface]['ipv4']
      mask = underlay[device]['interfaces'][iface]['mask']
      print("  ip address {}/{}".format(ip, mask))
      if 'thernet' in iface:
        print("  mtu {}".format(MTU))
        print("  no switchport")

#
# Function to generate Leafs Fabric configuration
#

def gen_leaf(device):
    ASN = underlay[device]['BGP']['ASN']
    LOOPBACK0 = underlay[device]['interfaces']['loopback0']['ipv4']
    DC_list = hostname.split("-")
    DC = DC_list[1]
    DC_ASN = underlay['global'][DC]['spine_ASN']
    activate = """
    address-family evpn
      neighbor EVPN activate
     
    address-family ipv4
      neighbor Underlay activate
      neighbor LEAF_Peer activate
      redistribute connected route-map LOOPBACK
    """
    
    print("ip virtual-router mac-address 001c.7300.0099")
    print(PREFIX_LIST)
    
    print("router bgp {}".format(ASN))
    print("  router-id {}".format(LOOPBACK0))
    print("  no bgp default ipv4-unicast")
    print("  maximum-paths 3")
    print("  distance bgp 20 200 200") 
    print("  neighbor Underlay peer group")
    print("  neighbor Underlay remote-as {}".format(DC_ASN))
    print("  neighbor Underlay send-community")
    print("  neighbor Underlay maximum-routes 12000")
    for neighbor in underlay[hostname]['BGP']['spine-peers']:
      print("  neighbor {} peer group Underlay".format(neighbor))
    
    print("  neighbor LEAF_Peer peer group")
    print("  neighbor LEAF_Peer remote-as {}".format(ASN))
    print("  neighbor LEAF_Peer next-hop-self")
    print("  neighbor LEAF_Peer maximum-routes 12000")
    if underlay[hostname]['MLAG'] == 'Odd':
      print("  neighbor 192.168.255.2 peer group LEAF_Peer")
    if underlay[hostname]['MLAG'] == 'Even':
      print("  neighbor 192.168.255.1 peer group LEAF_Peer")

    print("  neighbor EVPN peer group")
    print("  neighbor EVPN remote-as {}".format(DC_ASN))
    print("  neighbor EVPN update-source Loopback0")
    print("  neighbor EVPN ebgp-multihop 3")
    print("  neighbor EVPN send-community")
    print("  neighbor EVPN maximum-routes 0")
    for neighbor in underlay['global'][DC]['spine_peers']:
      print("  neighbor {} peer group EVPN".format(neighbor))
    print(activate)

#
# Function to generate Spines Fabric configuration
#

def gen_spine_bgp(device):
    ASN = underlay[hostname]['BGP']['ASN']
    LOOPBACK0 = underlay[hostname]['interfaces']['loopback0']['ipv4']
    P2P_RANGE = "192.168.103.0/24"
    EVPN_RANGE = "192.168.101.0/24"
    
    print(PREFIX_LIST)
    print(PEER_RANGE)
    print("router bgp {}".format(ASN))
    print("  router-id {}".format(LOOPBACK0))
    print("  no bgp default ipv4-unicast")
    print("  maximum-paths 3")
    print("  distance bgp 20 200 200")
    print("  bgp listen range {} peer-group LEAF_Underlay peer-filter LEAF-AS-RANGE".format(P2P_RANGE))
    print("  neighbor LEAF_Underlay peer group")
    print("  neighbor LEAF_Underlay send-community")
    print("  neighbor LEAF_Underlay maximum-routes 12000") 
    print("  neighbor EVPN peer group") 
    print("  bgp listen range {} peer-group EVPN peer-filter LEAF-AS-RANGE".format(EVPN_RANGE))
    print("  neighbor EVPN update-source Loopback0")
    print("  neighbor EVPN ebgp-multihop 3")
    print("  neighbor EVPN send-community extended")
    print("  neighbor EVPN maximum-routes 0")
    print("  address-family evpn")
    print("    neighbor EVPN activate")
    print("  address-family ipv4")
    print("    neighbor LEAF_Underlay activate")
    print("    redistribute connected route-map LOOPBACK")

#
# Generate MP-BGP EVPN configuration Spines + Leaves
#

gen_int(hostname)

if 'leaf' in hostname:
  gen_leaf(hostname)
if 'spine' in hostname:
  gen_spine_bgp(hostname)