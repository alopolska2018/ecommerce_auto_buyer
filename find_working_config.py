from openvpn.OpenVpn import OpenVpn
import os

def find_working_configs(config_name):
    vpn = OpenVpn(config_name)
    already_connected = vpn.check_connection()
    timeout = 0
    while already_connected == True:
        vpn.disconnect()
        already_connected = vpn.check_connection()
        timeout += 10
        if timeout == 10:
            while already_connected == True:
                print('Script can not disconnect from vpn automatically, please do it manually')
                input('Type y if you disconnected manually: ')
                already_connected = vpn.check_connection()
    connected = vpn.connect()
    if connected == True:
        with open('working_configs', 'a') as f:
            f.writelines(config_name)
    else:
        with open('not working configs', 'a') as f:
            f.writelines(config_name)
config_list = os.listdir('C:\Program Files\OpenVPN\config')
for name in config_list:
    find_working_configs(name)


