import pyeapi

with open('/home/coder/.ssh/id_rsa.pub', 'r') as sshkey:
    SSH_KEY = sshkey.readline()

with open('inventory', 'r') as inv_file:
    host = inv_file.readline().strip('\n')
    while host:
        print("*"*20)
        print("HOSTNAME:", host)
        print("*"*20)
        conn = pyeapi.connect_to(host)
        res_key = conn.api('users').set_sshkey(name='arista',
        value=SSH_KEY,
        default=False, disable=False)
        print(conn.api('users').get('arista'))
        print(res_key)
        host = inv_file.readline().strip('\n')
