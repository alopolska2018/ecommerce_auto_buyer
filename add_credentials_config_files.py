import os

config_list = os.listdir('C:\Program Files\OpenVPN\config')

for item in config_list:
    with open('C:\Program Files\OpenVPN\config\{}'.format(item), 'a') as f:
        f.write('auth-user-pass login.conf\n')
