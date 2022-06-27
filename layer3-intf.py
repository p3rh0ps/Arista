import pyeapi

connect = pyeapi.connect_to("leaf1")
connect.api("ipinterfaces").create('Ethernet1')
result = connect.api("ipinterfaces").set_address('Ethernet1','10.1.1.1/24')

if result == True:
    print("Completed!")
if result == False:
    print("Error!")
