import os
import yaml


def get_device_conf(ip):
    device_conf = {
        "device_type": '',
        "host": '',
        "username": '',
        "password": '',
        "secret": '',
    }
    location = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))
    with open(f'{location}/credentials.yaml') as credentials_yaml:
        credentials = yaml.safe_load(credentials_yaml)
        device_conf['username'] = credentials['username']
        device_conf['password'] = credentials['password']
        device_conf['secret'] = credentials['secret']
    with open(f'{location}/devices.yaml') as devices_yaml:
        devices = yaml.safe_load(devices_yaml)
        for device in devices:
            if device['ip'] == ip:
                device_conf['device_type'] = device['type']
                device_conf['host'] = ip
                return device_conf
    device_conf['host'] = 'unknown device'
    device_conf['device_type'] = 'unknown model'
    return device_conf


if __name__ == "__main__":
    print(get_device_conf('192.168.200.1'))
