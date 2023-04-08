import os
import textfsm
import yaml

from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from typing import Union, List, Dict, Optional, Any


Port_Type = Dict[str, Union[str, bool]]

Device_Type = Dict[
    str,
    Dict[
        str,
        Union[
            str,
            None,
            Union[
                List[Port_Type],
                List[Any]
            ]
        ]
    ]
]


#@dataclass
class Port(BaseModel):
    name: str
    status: bool


#@dataclass
class Device(BaseModel):
    status: str
    model: str = 'not defined'
    ports: List[Port] = []


class DataHandler:

    location = os.environ['LOCATION']
    netmiko_template = {
        "device_type": '',
        "host": '',
        "username": '',
        "password": '',
        "secret": '',
    }

    def __init__(self) -> None:
        self.credentials = self._set_credentials()
        self.devices = self._set_devices()

    @classmethod
    def _set_credentials(cls) -> Dict[str, str]:
        with open(f'{cls.location}/credentials.yaml') as credentials_yaml:
            return yaml.safe_load(credentials_yaml)

    @classmethod
    def _set_devices(cls) -> Dict[str, str]:
        with open(f'{cls.location}/devices.yaml') as devices_yaml:
            return yaml.safe_load(devices_yaml)

    def _get_template(self, command: str) -> str:
        file_name = command.replace(' ', '_')
        return f'{self.location}/{file_name}.template'

    def _convert_port_name(self, port_name: str) -> str:
        if 'Gigabit' in port_name:
            _, number = port_name.split('Ethernet')
            return f'GE{number}'
        elif 'Fast' in port_name:
            _, number = port_name.split('Ethernet')
            return f'FE{number}'
        else:
            _, number = port_name.split('Ethernet')
            return f'ET{number}'

    def get_parsed_data(self, action: str, data: str) -> List[List[str]]:
        templete = self._get_template(action)
        with open(templete) as file:
            fsm = textfsm.TextFSM(file)
            return fsm.ParseText(data)

    def get_port_status_list(self,
                             parsed_data: List[List[str]]
                             ) -> Union[List[Port_Type], List[Any]]:
        ports: list = []
        for parsed_port in parsed_data:
            if 'Ethernet' in parsed_port[0]:
                name = self._convert_port_name(parsed_port[0])
                if parsed_port[2] == 'up':
                    status = True
                else:
                    status = False
                port = Port(name=name, status=status)
                ports.append(port)
        return ports

    def get_device_conf(self, ip: str) -> Dict[str, str]:
        self.netmiko_template['username'] = self.credentials.get('username')
        self.netmiko_template['password'] = self.credentials.get('password')
        self.netmiko_template['secret'] = self.credentials.get('secret')
        # Set IP and model/os
        for device in self.devices:
            if device.get('ip') == ip:
                self.netmiko_template['device_type'] = device.get('type')
                self.netmiko_template['host'] = ip
                return self.netmiko_template
        self.netmiko_template['host'] = 'unknown device'
        self.netmiko_template['device_type'] = 'unknown model'
        return self.netmiko_template

    @staticmethod
    def get_device_model(parsed_data: List[List[str]]) -> Optional[str]:
        return parsed_data[0][0].split('-')[0]
