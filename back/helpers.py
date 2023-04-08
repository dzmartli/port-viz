"""
Helper functions
"""
import sys
import time
from typing import Union, Dict

from fastapi import WebSocket
from netmiko import ConnectHandler

from app.utils import DataHandler, Device


async def disconnect(websocket: WebSocket,
                     any_exception: Union[Exception, str]
                     ) -> None:
    """
    'Universal' exception handler

    Args:
        websocket (WebSocket): WebSocket
        any_exception (Exception | str): any exception
    """
    response_data = Device(status='disconnected')
    await websocket.send_json(response_data.dict())
    print('EXCEPTION: ', any_exception, flush=True)
    await websocket.close()
    sys.exit(1)


async def config_check(websocket: WebSocket,
                       device_conf: Dict[str, str]
                       ) -> None:
    """
    Netmiko config check

    Args:
        websocket (WebSocket): WebSocket
        device_conf (dict): netmiko connection config
    """
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
    """
    Websocket connection

    Args:
        websocket (WebSocket): WebSocket
    """
    try:
        await websocket.accept()
    except Exception as any_exception:
        await disconnect(websocket, any_exception)


async def device_connect(websocket: WebSocket) -> None:
    """
    Device connection and data collecting

    Args:
        websocket (WebSocket): WebSocket
    """
    try:
        data_handler = DataHandler()
        # Get form data
        received_data = await websocket.receive_text()
        received_form = data_handler.get_received_form(received_data)
        device_conf = data_handler.get_device_conf(received_form.ip)
        # Chech device in devices.yaml
        await config_check(websocket, device_conf)
        # Create connection
        with ConnectHandler(**device_conf) as ssh:
            ssh.enable()
            # Get version data
            version_data = ssh.send_command("sh ver")
            response_data = data_handler.get_version_response(version_data)
            await websocket.send_json(response_data.dict())
            while True:
                time.sleep(1)
                # Get port status data
                ports_data = ssh.send_command("sh ip int br")
                response_data = data_handler.get_ports_response(ports_data)
                await websocket.send_json(response_data.dict())
                # Disconnect if detach received
                received_data = await websocket.receive_text()
                received_form = data_handler.get_received_form(received_data)
                if received_form.detach:
                    ssh.disconnect()
                    await websocket.close()
                    sys.exit(1)
    except Exception as any_exception:
        await disconnect(websocket, any_exception)
