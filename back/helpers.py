import json
import sys
import time
from typing import Union, Dict

from fastapi import WebSocket
from netmiko import ConnectHandler


from app.utils import (netmiko_template,
                       get_json,
                       get_model,
                       get_device_conf,
                       get_parsed_data,
                       get_ports_list)


async def disconnect(websocket: WebSocket,
                     any_exception: Union[Exception, str]
                     ) -> None:
    send_data = get_json('disconnected', model=None, ports=None)
    await websocket.send_json(send_data)
    print('EXCEPTION: ', any_exception, flush=True)
    await websocket.close()
    sys.exit(1)


async def config_check(websocket: WebSocket, device: Dict[str, str]) -> None:
    if device['host'] == 'unknown device':
        send_data = get_json('unknown device', model=None, ports=None)
        await websocket.send_json(send_data)
        await disconnect(websocket, any_exception='unknown device')
        sys.exit(1)
    if device['device_type'] != 'cisco_ios':
        send_data = get_json('unknown model', model=None, ports=None)
        await websocket.send_json(send_data)
        await disconnect(websocket, any_exception='unknown model')
        sys.exit(1)


async def websocket_connect(websocket: WebSocket) -> None:
    try:
        await websocket.accept()
    except Exception as any_exception:
        await disconnect(websocket, any_exception)


async def device_connect(websocket: WebSocket) -> None:
    try:
        data = await websocket.receive_text()
        device = get_device_conf(json.loads(data)['ip'], netmiko_template)
        await config_check(websocket, device)
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            version_data = ssh.send_command("sh ver")
            parsed_model = get_parsed_data('sh ver', version_data)
            model = get_model(parsed_model)
            send_data = get_json('connecting', model=model, ports=None)
            await websocket.send_json(send_data)
            while True:
                time.sleep(1)
                ports_data = ssh.send_command("sh ip int br")
                parsed_ports = get_parsed_data("sh ip int br", ports_data)
                ports = get_ports_list(parsed_ports)
                send_data = get_json('connected', model=model, ports=ports)
                await websocket.send_json(send_data)
                data = await websocket.receive_text()
                if json.loads(data)['detach']:
                    ssh.disconnect()
                    await websocket.close()
                    sys.exit(1)
    except Exception as any_exception:
        await disconnect(websocket, any_exception)
