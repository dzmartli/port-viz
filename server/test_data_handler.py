"""
Some unit testing

All tests are coupled with configuration (see docker compose)
Test device IP address: 192.168.200.5
"""
import pytest

from utils import DataHandler, Device, Port, ReceivedForm


@pytest.fixture
def data_handler():
    return DataHandler()


@pytest.fixture
def ip():
    return '192.168.200.5'


@pytest.fixture
def version_data():
    return """Cisco IOS Software, test_model Software (test_model-ADVENTERPRISEK9-M), Version 15.0(TTC_20140605)FLO_DSGS7, EARLY DEPLOYMENT DEVELOPMENT BUILD, synced to  V152_3_0_88_PI4"""


@pytest.fixture
def model():
    return 'test_model'


@pytest.fixture
def ports_data():
    return """Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     unassigned      YES unset  up                    up      
GigabitEthernet0/1     unassigned      YES unset  down                  down    
GigabitEthernet0/2     unassigned      YES unset  down                  down    
GigabitEthernet0/3     unassigned      YES unset  down                  down    
GigabitEthernet1/0     unassigned      YES unset  down                  down    
GigabitEthernet1/1     unassigned      YES unset  down                  down    
GigabitEthernet1/2     unassigned      YES unset  down                  down    
GigabitEthernet1/3     unassigned      YES unset  down                  down    
GigabitEthernet2/0     unassigned      YES unset  down                  down    
GigabitEthernet2/1     unassigned      YES unset  down                  down    
GigabitEthernet2/2     unassigned      YES unset  down                  down    
GigabitEthernet2/3     unassigned      YES unset  down                  down    
GigabitEthernet3/0     unassigned      YES unset  down                  down    
GigabitEthernet3/1     unassigned      YES unset  down                  down    
GigabitEthernet3/2     unassigned      YES unset  down                  down    
GigabitEthernet3/3     unassigned      YES unset  down                  down    
Vlan1                  192.168.200.5   YES NVRAM  up                    up"""


@pytest.fixture
def ports():
    return [
        Port(name='GE0/0', status=True),
        Port(name='GE0/1', status=False),
        Port(name='GE0/2', status=False),
        Port(name='GE0/3', status=False),
        Port(name='GE1/0', status=False),
        Port(name='GE1/1', status=False),
        Port(name='GE1/2', status=False),
        Port(name='GE1/3', status=False),
        Port(name='GE2/0', status=False),
        Port(name='GE2/1', status=False),
        Port(name='GE2/2', status=False),
        Port(name='GE2/3', status=False),
        Port(name='GE3/0', status=False),
        Port(name='GE3/1', status=False),
        Port(name='GE3/2', status=False),
        Port(name='GE3/3', status=False)
    ]

@pytest.fixture
def received_data():
    return '{"ip":"192.168.200.5","detach":false}'


@pytest.fixture
def sh_ver_template():
    return '/code/app/sh_ver.template'


@pytest.fixture
def sh_ip_int_br_template():
    return '/code/app/sh_ip_int_br.template'


@pytest.fixture
def sh_ver_parsed_data():
    return [['test_model-ADVENTERPRISEK9-M', '15.0(TTC_20140605)FLO_DSGS7', '']]


@pytest.fixture
def sh_ip_int_br_parsed_data():
    return [
        ['GigabitEthernet0/0', 'unassigned', 'up', 'up'],
        ['GigabitEthernet0/1', 'unassigned', 'down', 'down'],
        ['GigabitEthernet0/2', 'unassigned', 'down', 'down'],
        ['GigabitEthernet0/3', 'unassigned', 'down', 'down'],
        ['GigabitEthernet1/0', 'unassigned', 'down', 'down'],
        ['GigabitEthernet1/1', 'unassigned', 'down', 'down'],
        ['GigabitEthernet1/2', 'unassigned', 'down', 'down'],
        ['GigabitEthernet1/3', 'unassigned', 'down', 'down'],
        ['GigabitEthernet2/0', 'unassigned', 'down', 'down'],
        ['GigabitEthernet2/1', 'unassigned', 'down', 'down'],
        ['GigabitEthernet2/2', 'unassigned', 'down', 'down'],
        ['GigabitEthernet2/3', 'unassigned', 'down', 'down'],
        ['GigabitEthernet3/0', 'unassigned', 'down', 'down'],
        ['GigabitEthernet3/1', 'unassigned', 'down', 'down'],
        ['GigabitEthernet3/2', 'unassigned', 'down', 'down'],
        ['GigabitEthernet3/3', 'unassigned', 'down', 'down'],
        ['Vlan1', '192.168.200.5', 'up', 'up']
    ]


def test_get_device_conf(ip, data_handler):
    assert data_handler.get_device_conf(ip) == {
        "device_type": "cisco_ios",
        "host": "192.168.200.5",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    assert data_handler.get_device_conf('192.168.200.7') == {
        "device_type": "some_os",
        "host": "192.168.200.7",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }


def test_get_version_response(version_data, model, data_handler):
    assert data_handler \
        .get_version_response(version_data) == Device(status='connecting',
                                                      model=model)


def test_get_ports_response(ports_data, ports, data_handler):
    assert data_handler \
        .get_ports_response(ports_data) == Device(status='connected',
                                                  model='not defined',
                                                  ports=ports)


def test_get_received_form(ip, received_data, data_handler):
    assert data_handler \
        .get_received_form(received_data) == ReceivedForm(ip=ip, detach=False)


def test__set_credentials(data_handler):
    # Check credentials yaml
    credentials = data_handler._set_credentials()
    credentials_list = []
    for key in credentials.keys():
        credentials_list.append(key)
    assert credentials_list == ['username', 'password', 'secret']


def test__set_devices(data_handler):
    # Check devices yaml
    devices = data_handler._set_devices()
    for device in devices:
        device_params_list = []
        for key in device.keys():
            device_params_list.append(key)
        assert device_params_list == ['ip', 'type']


def test__get_template(sh_ver_template, sh_ip_int_br_template, data_handler):
    assert data_handler._get_template('sh ver') == sh_ver_template
    assert data_handler._get_template('sh ip int br') == sh_ip_int_br_template


def test__convert_port_name(data_handler):
    # Cases for different pot types
    assert data_handler._convert_port_name('GigabitEthernet0/1') == 'GE0/1'
    assert data_handler._convert_port_name('FastEthernet0/2') == 'FE0/2'
    assert data_handler._convert_port_name('Ethernet0/3') == 'ET0/3'


def test__get_parsed_data(version_data,
                          ports_data,
                          sh_ver_parsed_data,
                          sh_ip_int_br_parsed_data,
                          data_handler):
    # Show version command
    assert data_handler \
        ._get_parsed_data('sh ver', version_data) == sh_ver_parsed_data
    # Show ip interface brief command
    assert data_handler \
        ._get_parsed_data('sh ip int br',
                          ports_data) == sh_ip_int_br_parsed_data


def test__get_port_status_list(sh_ip_int_br_parsed_data, ports, data_handler):
    assert data_handler \
        ._get_port_status_list(sh_ip_int_br_parsed_data) == ports


def test__get_device_model(sh_ver_parsed_data, model, data_handler):
    assert data_handler._get_device_model(sh_ver_parsed_data) == model
