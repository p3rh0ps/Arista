from EapiClientLib import EapiClient

switch = EapiClient( disableAaa=True, privLevel=15 )
response = switch.runCmds( 1, ['show version'] )
print("The switch's system MAC addess is {}".format(response['result'][0]['systemMacAddress']))
