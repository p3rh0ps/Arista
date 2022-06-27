import pyeapi

with open('inventory', 'r') as inv_file:
    host = inv_file.readline().strip('\n')
    while host:
        print("*"*20)
        print("HOSTNAME:", host)
        print("*"*20)
        conn = pyeapi.connect_to(host)
        res_key = conn.api('users').set_sshkey(name='arista',
        value='ssh-rsa AAAAPLACEYOUROWNKEYHERE\
HELLLLLLOOOOOTHERECHANGEWITHYOURKEYHEREEEEEEEEEE\
HELLLLLLOOOOOTHERECHANGEWITHYOURKEYHEREEEEEEEEEE\
HELLLLLLOOOOOTHERECHANGEWITHYOURKEYHEREEEEEEEEEE\
HELLLLLLOOOOOTHERECHANGEWITHYOURKEYHEREEEEEEEEEE user@mydom',
        default=False, disable=False)
        print(conn.api('users').get('arista'))   # Take a look at the result
        # print(res_key)                         # Check if you made a change True > YES, False > NO
