import json
import pyeapi

node = pyeapi.connect_to('leaf1-dc1')

vlans = node.api('vlans')

print(vlans.getall())

vlans.create(2222)
vlans.set_name(100, 'foo')
vlans.set_name(2222, 'bar')

vlan_pydata = vlans.getall()
for vlan, vlan_data in vlan_pydata.items():
    print("*vlan-id*",vlan)
    print("****Name****",vlan_data['name'])
    print("****State****",vlan_data['state'])
    print("****Trunk Groups****",vlan_data['trunk_groups'])
