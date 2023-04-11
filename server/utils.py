"""
Utils and classes
"""
import json
import os
import textfsm
import yaml

from typing import List, Dict, Optional

from pydantic import BaseModel


class Port(BaseModel):
    """
    Single port status
    """
    name: str
    status: bool


class Device(BaseModel):
    """
    Device status response
    """
    status: str
    model: str = 'not defined'
    ports: List[Port] = []


class ReceivedForm(BaseModel):
    """
    Received form
    """
    ip: str
    detach: bool


class NetmikoTemplate(BaseModel):
    """
    Default netmiko template
    """
    device_type: Optional[str] = ''
    host: Optional[str] = ''
    username: Optional[str] = ''
    password: Optional[str] = ''
    secret: Optional[str] = ''


class DataHandler:
    """
    Data handling class
    """

    location = os.environ['LOCATION']
    version_command = 'sh ver'
    port_status_command = 'sh ip int br'

    def __init__(self) -> None:
        self.model = 'not defined'
        self.credentials = self._set_credentials()
        self.devices = self._set_devices()

    @classmethod
    def _set_credentials(cls) -> Dict[str, str]:
        """
        Setter for user/pass data

        Returns:
            (dict): user/pass data
        """
        with open(f'{cls.location}/params/credentials.yaml') as credentials_yaml:
            return yaml.safe_load(credentials_yaml)

    @classmethod
    def _set_devices(cls) -> List[Dict[str, str]]:
        """
        Setter for ip/os data

        Returns:
            (dict): ip/os data
        """
        with open(f'{cls.location}/params/devices.yaml') as devices_yaml:
            return yaml.safe_load(devices_yaml)

    def _get_template(self, command: str) -> str:
        """
        Get textfsm template based on command

        Args:
            command (str): terminal command for device

        Returns:
            (str): template name
        """
        file_name = command.replace(' ', '_')
        return f'{self.location}/templates/{file_name}.template'

    def _convert_port_name(self, port_name: str) -> str:
        """
        Port name shortener

        Args:
            port_name (str): full port name

        Returns:
            (str): sort port name
        """
        if 'Gigabit' in port_name:
            _, number = port_name.split('Ethernet')
            return f'GE{number}'
        elif 'Fast' in port_name:
            _, number = port_name.split('Ethernet')
            return f'FE{number}'
        else:
            _, number = port_name.split('Ethernet')
            return f'ET{number}'

    def _get_parsed_data(self, command: str, data: str) -> List[List[str]]:
        """
        Get textfsm parsed data

        Args:
            action (str): terminal command for device
            data (str): raw data from netmiko

        Returns:
            (list): data parsed by textfsm
        """
        templete = self._get_template(command)
        with open(templete) as file:
            fsm = textfsm.TextFSM(file)
            return fsm.ParseText(data)

    def _get_port_status_list(self,
                              parsed_data: List[List[str]]
                              ) -> List[Port]:
        """
        Get ports status list

        Args:
            parsed_data (list): data parsed by textfsm ('sh ip int br')

        Returns:
            (list): list of port status pydantic objects
        """
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

    def _get_device_model(self, parsed_data: List[List[str]]) -> str:
        """
        Get device model

        Args:
            parsed_data (list): data parsed by textfsm ('sh ver')

        Returns:
            (str): device model
        """
        return parsed_data[0][0].split('-')[0]

    def get_device_conf(self, ip: str) -> Dict[str, str]:
        """
        Get device configuration dict for netmiko ConnectHandler

        Args:
            ip (str): device IP address

        Returns:
            (dict): netmiko template
        """
        username = self.credentials.get('username')
        password = self.credentials.get('password')
        secret = self.credentials.get('secret')
        # Set IP and model/os
        for device in self.devices:
            if device.get('ip') == ip:
                device_type = device.get('type')
                return NetmikoTemplate(device_type=device_type,
                                       host=ip,
                                       username=username,
                                       password=password,
                                       secret=secret).dict()
        return NetmikoTemplate(device_type='unknown model',
                               host='unknown device',
                               username=username,
                               password=password,
                               secret=secret).dict()

    def get_version_response(self, version_data: str) -> Device:
        """
        Get data for 'sh ver' response

        Args:
            version_data (str): raw data from netmiko ('sh ver')

        Returns:
            (Device): Device pydantic object with model info
        """
        parsed_model = self._get_parsed_data(self.version_command,
                                             version_data)
        self.model = self._get_device_model(parsed_model)
        return Device(status='connecting', model=self.model)

    def get_ports_response(self, ports_data: str) -> Device:
        """
        Get data for 'sh ip int br' response

        Args:
            ports_data (str): raw data from netmiko ('sh ip int br')

        Returns:
            (Device): Device pydantic object with model info and ports data
        """
        parsed_ports = self._get_parsed_data(self.port_status_command,
                                             ports_data)
        ports = self._get_port_status_list(parsed_ports)
        return Device(status='connected', model=self.model, ports=ports)

    def get_received_form(self, received_data: str) -> ReceivedForm:
        """
        Get received form data

        Args:
            received_data (str): received form data

        Returns:
            (ReceivedForm): ReceivedForm pydantic object
                with ip and detach info
        """
        ip = json.loads(received_data).get('ip')
        detach = json.loads(received_data).get('detach')
        return ReceivedForm(ip=ip, detach=detach)
