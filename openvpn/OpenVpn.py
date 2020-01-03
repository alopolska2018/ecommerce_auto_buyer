import subprocess, os
#TODO fix command injection from user
class OpenVpn():
    def __init__(self, config_name):
        #Name of OpenVPN's network adapter, from the Windows Network Adapters control panel.
        self.adapter_name = 'TAP'
        #name of openvpn configuration from C:\Program Files\OpenVPN\config
        self.config_name = config_name
        # run() returns a CompletedProcess object if it was successful
        # errors in the created process are raised here too
        #we are using another script that makes our life easier
        # print('ConnectOpenVPN.exe', '/connect', '/adapter \"TAP\"', '/config "{}"'.format(self.config_name), '/verbose')

        #ConnectOpenVPN.exe /test /adapter "TAP" /verbose


    def check_connection(self):
        #0 = connected
        #1 = not connected
        cmd = 'ConnectOpenVPN.exe /test /adapter "{}" /verbose'.format(self.adapter_name)
        output = subprocess.run(cmd, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code = output.returncode
        if return_code == 0:
            return True
        else:
            return False

    def connect(self):
        # 0 = connected
        # 1 = not connected
        backup_config = os.listdir('C:\Program Files\OpenVPN\config')
        cmd = 'ConnectOpenVPN.exe /connect /adapter "{}" /config "{}"'.format(self.adapter_name, self.config_name)
        output = subprocess.run(cmd, universal_newlines=True, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        return_code = output.returncode
        if return_code == 0:
            return True
        else:
            for config in reversed(backup_config):
                self.config_name = config
                cmd = 'ConnectOpenVPN.exe /connect /adapter "{}" /config "{}"'.format(self.adapter_name,
                                                                                      self.config_name)
                output = subprocess.run(cmd, universal_newlines=True, shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                return_code = output.returncode
                if return_code == 0:
                    return True
            return False

    def disconnect(self):
        #only returns 0
        cmd = 'openvpn-gui.exe --command disconnect_all'
        output = subprocess.run(cmd, universal_newlines=True, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        return_code = output.returncode
        if return_code == 0:
            return True
        else:
            return False