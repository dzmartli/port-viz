from fastapi import FastAPI, WebSocket

from app.helpers import (device_connect, websocket_connect)


app = FastAPI(title='port-viz')


@ app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    """
    await websocket_connect(websocket)
    await device_connect(websocket)
