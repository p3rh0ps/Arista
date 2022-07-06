import os
import sys
import re
import pyeapi
from tabulate import tabulate


def get_ssh_infos(ssh_key: str) -> str:
    ssh_key_type = ssh_key.split(" ")[0]
    ssh_key_misc = ssh_key.split(" ")[2]
    if ssh_key_type == "ssh-rsa" and ssh_key_misc.startswith(KEY_USER+"@") and re.match(KEY_USER+"@"+KEY_HOST, ssh_key_misc):
        return ssh_key_type + " " + ssh_key_misc
    else:
        print("You don't use a key generated with the local user and local host of this system, or it is the wrong key\
            please correct by creating a new one if necessary via 'ssh-keygen -t rsa' linux cli")
        sys.exit(-1)

def ssh_key_set(operator: bool) -> str:
    print(operator)
    if operator is True:
        return "Modified"
    else:
        return "Unmodified"

with open('/home/coder/.ssh/id_rsa.pub', 'r') as sshkey:
    SSH_KEY = sshkey.readline()

USER = 'arista'
KEY_USER = os.getenv('USER')
KEY_HOST = os.getenv('HOSTNAME')
fancytab = []

try:
    with open('inventory', 'r') as inv_file:
        host = inv_file.readline().strip('\n')
        while host:
            conn = pyeapi.connect_to(host)
            key_status = "Unchanged"
            if conn.api('users').get(USER)['ssh-key'] != SSH_KEY.strip("\n"):
                res_key_op = conn.api('users').set_sshkey(name=USER,
                value=SSH_KEY,
                default=False, disable=False)
                if res_key_op is False:
                    raise AssertionError("Issue with ssh key update for host {}".format(host))
                key_status = "Updated"
            fancytab.append([host, USER, conn.api('users').get(USER)['privilege'], conn.api('users').get(USER)['role'], get_ssh_infos(conn.api('users').get(USER)['ssh-key']), key_status])
            host = inv_file.readline().strip('\n')
except FileNotFoundError as filenotf_err:
    print("File not Found: {}".format(filenotf_err.args))
except AssertionError as assert_err:
    print("Assertion Error: {}".format(assert_err.args))
    sys.exit(-1)
except KeyboardInterrupt as keyb_err:
    print("User Interrupt: {}".format(keyb_err.args))
    sys.exit(0)
except:
    print("Unknown but catched error")

print(tabulate(fancytab, headers=["Hostname", "User", "Privilege", "Role", "Ssh Type and Key", "Ssh-Key-Status"], tablefmt="grid", stralign='center', numalign='center', showindex='always'))
