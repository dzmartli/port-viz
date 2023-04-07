from pprint import pprint
import time
import textfsm
import os
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


def get_template(command):
    file_name = command.replace(' ', '_')
    location = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))
    return f'{location}/{file_name}.template'


def convert_port_name(port_name):
    if 'Gigabit' in port_name:
        _, number = port_name.split('Ethernet')
        return f'GE{number}'
    elif 'Fast' in port_name:
        _, number = port_name.split('Ethernet')
        return f'FE{number}'
    else:
        _, number = port_name.split('Ethernet')
        return f'ET{number}'


def get_parsed_data(action, data):
    templete = get_template(action)
    with open(templete) as file:
        fsm = textfsm.TextFSM(file)
        return fsm.ParseText(data)


def get_model(parsed_data):
    return parsed_data[0][0].split('-')[0]


def get_ports_list(parsed_data):
    ports = []
    for parsed_port in parsed_data:
        port = {}
        if 'Ethernet' in parsed_port[0]:
            port['name'] = convert_port_name(parsed_port[0])
            if parsed_port[2] == 'up':
                port['status'] = True
            else:
                port['status'] = False
            ports.append(port)
    return ports


def get_json(status, model, ports):
    if not ports:
        ports = []
    return {
        'device': {
            'status': status,
            'model': model,
            'ports': ports,
        }
    }


def send_show_command(device):
    # print(get_json('connecting', model=None, ports=None))
    # print()
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            version_data = ssh.send_command("sh ver")
            parsed_model = get_parsed_data('sh ver', version_data)
            model = get_model(parsed_model)
            # print(get_json('connected', model, ports=None))
            # print()
            try:
                while True:
                    time.sleep(5)
                    ports_data = ssh.send_command("sh ip int br")
                    print(type(ports_data))
                    parsed_ports = get_parsed_data("sh ip int br",  ports_data)
                    ports = get_ports_list(parsed_ports)
                    # print(get_json('connected', model, ports))
                    # print()
            except (NetmikoTimeoutException) as error:
                print(error)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


if __name__ == "__main__":
    device = {
        "device_type": "cisco_ios",
        "host": "192.168.200.5",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    result = send_show_command(device)
    pprint(result, width=120)
