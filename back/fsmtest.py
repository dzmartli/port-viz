import textfsm
import os
from dataclasses import dataclass
from typing import Union, List, Dict, Optional, Any


a = """Interface              IP-Address      OK? Method Status                Protocol
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

b = """Cisco IOS Software, vios_l2 Software (vios_l2-ADVENTERPRISEK9-M), Version 15.0(TTC_20140605)FLO_DSGS7, EARLY DEPLOYMENT DEVELOPMENT BUILD, synced to  V152_3_0_88_PI4
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2014 by Cisco Systems, Inc.
Compiled Thu 05-Jun-14 05:35 by jsfeng

*** IOSv: UNSUPPORTED DEMO VERSION ONLY ***

ROM: Bootstrap program is IOSv

vIOS-L2-01 uptime is 2 hours, 22 minutes
System returned to ROM by reload
System image file is "flash0:/vios_l2-adventerprisek9-m"
Last reload reason: Unknown reason



This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

Cisco IOSv () processor (revision 1.0) with 312577K/209920K bytes of memory.
Processor board ID 
1 Virtual Ethernet interface
16 Gigabit Ethernet interfaces
DRAM configuration is 72 bits wide with parity disabled.
256K bytes of non-volatile configuration memory.
2097144K bytes of ATA System CompactFlash 0 (Read/Write)
0K bytes of ATA CompactFlash 1 (Read/Write)
0K bytes of ATA CompactFlash 2 (Read/Write)
0K bytes of ATA CompactFlash 3 (Read/Write)

Configuration register is 0x0"""


def get_template(model, action):
    location = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))
    return f'{location}/{model}-{action}.template'


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


# model = 'vios_l2'
# action = 'shipintbr'
#
# with open(get_template(model, action)) as f:
#    fsm = textfsm.TextFSM(f)
#    result = fsm.ParseText(a)
#
#
# ports = []
# for arr in result:
#    port = {}
#    if 'Ethernet' in arr[0]:
#        port['name'] = convert_port_name(arr[0])
#        if arr[2] == 'up':
#            port['status'] = True
#        else:
#            port['status'] = False
#        ports.append(port)
#
# print(ports)
#
# action = 'shver'
#
# with open(get_template(model, action)) as f:
#    fsm = textfsm.TextFSM(f)
#    result = fsm.ParseText(b)
#
# print(result[0][0].split('-')[0])
#
#
def get_parsed_data(model, action, data):
    templete = get_template(model, action)
    with open(templete) as file:
        fsm = textfsm.TextFSM(file)
        return fsm.ParseText(data)


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


@dataclass
class Port:
    name: str
    status: bool


@dataclass
class Device:
    status: str
    model: Optional[str]
    ports: List[Optional[Port]]


c = Port('GE0/0', True)
ports = [c]
d = Device('connected', 'some', ports)

print(c)
print(d)