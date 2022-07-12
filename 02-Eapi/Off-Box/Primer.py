import pyeapi

INTF_DESC = 'Dummy'

node = pyeapi.connect_to('leaf1-dc1')

print(node.enable('show hostname'))

print(node.enable({'cmd': 'show cvx', 'revision': 2}))

node.config('hostname leaf1-dc1-tuned')

node.config(['interface Ethernet6', f'description {INTF_DESC}'])

try:

    result_config = node.api("interfaces").get("Ethernet6")["description"]
    assert result_config == INTF_DESC
    print(node.api("interfaces").get("Ethernet6")["description"])

except AssertionError as err:

    print("Interface description do not match expected result: ", err.args)

except:

    print("Always catch all errors even the unknown!!!")

# print(node.running_config) # Detailed running configuration with Hidden cli
# print(node.startup_config) # Normal configuration output without Hidden cli