import pyeapi

node = pyeapi.connect_to('leaf1-dc1')

node.enable('show hostname')

node.enable({'cmd': 'show cvx', 'revision': 2})

node.config('hostname leaf1-dc1-tuned')

node.config(['interface Ethernet6', 'description foobar'])

try:

    result_config = node.api("interfaces").get("Ethernet6")["description"]
    assert result_config == "foobar"
    print(node.api("interfaces").get("Ethernet6")["description"])

except AssertionError as err:

    print("Interface description  do not match expected result: ", err.args)

except:

    print("Always catch all errors even the unknown!!!")

# print(node.running_config) # Detailed running configuration with Hidden cli
# print(node.startup_config) # Normal configuration output without Hidden cli
