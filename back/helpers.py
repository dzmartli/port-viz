import json
import sys
import time
from typing import Union, Dict

from fastapi import WebSocket
from netmiko import ConnectHandler


from app.utils import DataHandler, Device


async def disconnect(websocket: WebSocket,
                     any_exception: Union[Exception, str]
                     ) -> None:
    response_data = Device(status='disconnected')
    await websocket.send_json(response_data.dict())
    print('EXCEPTION: ', any_exception, flush=True)
    await websocket.close()
    sys.exit(1)


async def config_check(websocket: WebSocket,
                       device_conf: Dict[str, str]
                       ) -> None:
    if device_conf.get('host') == 'unknown device':
        response_data = Device(status='unknown device')
        await websocket.send_json(response_data.dict())
        await disconnect(websocket, any_exception='unknown device')
        sys.exit(1)
    if device_conf.get('device_type') != 'cisco_ios':
        response_data = Device(status='unknown model')
        await websocket.send_json(response_data.dict())
        await disconnect(websocket, any_exception='unknown model')
        sys.exit(1)


async def websocket_connect(websocket: WebSocket) -> None:
    try:
        await websocket.accept()
    except Exception as any_exception:
        await disconnect(websocket, any_exception)


async def device_connect(websocket: WebSocket) -> None:
    try:
        # Get form data
        data = await websocket.receive_text()
        data_helper = DataHandler()
        device_conf = data_helper.get_device_conf(json.loads(data).get('ip'))
        # Chech device in devices.yaml
        await config_check(websocket, device_conf)
        # Create connection
        with ConnectHandler(**device_conf) as ssh:
            ssh.enable()
            # Get version data
            version_data = ssh.send_command("sh ver")
            parsed_model = data_helper.get_parsed_data('sh ver', version_data)
            model = DataHandler.get_device_model(parsed_model)
            response_data = Device(status='connecting', model=model)
            await websocket.send_json(response_data.dict())
            while True:
                time.sleep(1)
                # Get port status data
                ports_data = ssh.send_command("sh ip int br")
                parsed_ports = data_helper.get_parsed_data("sh ip int br",
                                                           ports_data)
                ports = data_helper.get_port_status_list(parsed_ports)
                response_data = Device(status='connected',
                                       model=model,
                                       ports=ports)
                await websocket.send_json(response_data.dict())
                # Disconnect if detach received
                data = await websocket.receive_text()
                if json.loads(data).get('detach'):
                    ssh.disconnect()
                    await websocket.close()
                    sys.exit(1)
    except Exception as any_exception:
        await disconnect(websocket, any_exception)
