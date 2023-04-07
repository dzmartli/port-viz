import os
import textfsm
import yaml
from typing import Union, List, Dict, Optional, Any


PortType = Dict[str, Union[str, bool]]

DeviceType = Dict[
    str,
    Dict[
        str,
        Union[
            str,
            None,
            Union[
                List[PortType],
                List[Any]
            ]
        ]
    ]
]

# Netmiko default connection conf template
netmiko_template = {
    "device_type": '',
    "host": '',
    "username": '',
    "password": '',
    "secret": '',
}


def get_template(command: str) -> str:
    file_name = command.replace(' ', '_')
    location = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))
    return f'{location}/{file_name}.template'


def convert_port_name(port_name: str) -> str:
    if 'Gigabit' in port_name:
        _, number = port_name.split('Ethernet')
        return f'GE{number}'
    elif 'Fast' in port_name:
        _, number = port_name.split('Ethernet')
        return f'FE{number}'
    else:
        _, number = port_name.split('Ethernet')
        return f'ET{number}'


def get_parsed_data(action: str, data: str) -> List[List[str]]:
    templete = get_template(action)
    with open(templete) as file:
        fsm = textfsm.TextFSM(file)
        return fsm.ParseText(data)


def get_model(parsed_data: List[List[str]]) -> Optional[str]:
    return parsed_data[0][0].split('-')[0]


def get_ports_list(parsed_data: List[List[str]]
                   ) -> Union[List[PortType], List[Any]]:
    # print(parsed_data, flush=True)
    ports: list = []
    for parsed_port in parsed_data:
        port: PortType = {}
        if 'Ethernet' in parsed_port[0]:
            port['name'] = convert_port_name(parsed_port[0])
            if parsed_port[2] == 'up':
                port['status'] = True
            else:
                port['status'] = False
            ports.append(port)
    return ports


def get_json(status: str,
             model: Optional[str],
             ports: Optional[List[PortType]]
             ) -> DeviceType:
    if ports is None:
        ports = []
    return {
        'device': {
            'status': status,
            'model': model,
            'ports': ports,
        }
    }


def get_device_conf(ip: str,
                    netmiko_template: Dict[str, str]
                    ) -> Dict[str, str]:
    location = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))
    # Set credentials
    with open(f'{location}/credentials.yaml') as credentials_yaml:
        credentials = yaml.safe_load(credentials_yaml)
        netmiko_template['username'] = credentials['username']
        netmiko_template['password'] = credentials['password']
        netmiko_template['secret'] = credentials['secret']
    # Set IP and model/os
    with open(f'{location}/devices.yaml') as devices_yaml:
        devices = yaml.safe_load(devices_yaml)
        for device in devices:
            if device['ip'] == ip:
                netmiko_template['device_type'] = device['type']
                netmiko_template['host'] = ip
                return netmiko_template
    netmiko_template['host'] = 'unknown device'
    netmiko_template['device_type'] = 'unknown model'
    return netmiko_template
