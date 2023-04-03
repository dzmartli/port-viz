from fastapi import FastAPI, WebSocket, Request
import time

# Create application
app = FastAPI(title='port-viz')


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    #print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            # Wait for any message from the client
            # Send message to the client
            first = {
                'device': {
                    'status': 'disconnected',
                    'model': "ios",
                    'ports': [
                        {
                            'name': "GE0/0",
                            'status': True
                        },
                        {
                            'name': "GE0/1",
                            'status': True
                        },
                        {
                            'name': "GE0/2",
                            'status': True
                        },
                        {
                            'name': "GE0/3",
                            'status': True
                        },
                        {
                            'name': "GE1/0",
                            'status': True
                        },
                        {
                            'name': "GE1/1",
                            'status': True
                        },
                        {
                            'name': "GE1/2",
                            'status': True
                        },
                        {
                            'name': "GE1/3",
                            'status': True
                        },
                        {
                            'name': "GE2/0",
                            'status': True
                        },
                        {
                            'name': "GE2/1",
                            'status': True
                        },
                        {
                            'name': "GE2/2",
                            'status': True
                        },
                        {
                            'name': "GE2/3",
                            'status': True
                        },
                        {
                            'name': "GE3/0",
                            'status': True
                        },
                        {
                            'name': "GE3/1",
                            'status': True
                        },
                        {
                            'name': "GE3/2",
                            'status': True
                        },
                        {
                            'name': "GE3/3",
                            'status': True
                        },
                    ]
                }
            }
            second = {
                'device': {
                    'status': 'connected',
                    'model': "ios",
                    'ports': [
                        {
                            'name': "GE0/0",
                            'status': True
                        },
                        {
                            'name': "GE0/1",
                            'status': True
                        },
                        {
                            'name': "GE0/2",
                            'status': True
                        },
                        {
                            'name': "GE0/3",
                            'status': True
                        },
                        {
                            'name': "GE1/0",
                            'status': True
                        },
                        {
                            'name': "GE1/1",
                            'status': True
                        },
                        {
                            'name': "GE1/2",
                            'status': True
                        },
                        {
                            'name': "GE1/3",
                            'status': True
                        },
                        {
                            'name': "GE2/0",
                            'status': True
                        },
                        {
                            'name': "GE2/1",
                            'status': True
                        },
                        {
                            'name': "GE2/2",
                            'status': True
                        },
                        {
                            'name': "GE2/3",
                            'status': False
                        },
                        {
                            'name': "GE3/0",
                            'status': True
                        },
                        {
                            'name': "GE3/1",
                            'status': True
                        },
                        {
                            'name': "GE3/2",
                            'status': False
                        },
                        {
                            'name': "GE3/3",
                            'status': True
                        },
                    ]
                }
            }
            third = {
                'device': {
                    'status': 'connecting',
                    'model': "some",
                    'ports': [
                        {
                            'name': "GE0/0",
                            'status': True
                        },
                        {
                            'name': "GE0/1",
                            'status': True
                        },
                        {
                            'name': "GE0/2",
                            'status': True
                        },
                        {
                            'name': "GE0/3",
                            'status': True
                        },
                        {
                            'name': "GE1/0",
                            'status': True
                        },
                        {
                            'name': "GE1/1",
                            'status': True
                        },
                        {
                            'name': "GE1/2",
                            'status': True
                        },
                        {
                            'name': "GE1/3",
                            'status': True
                        },
                        {
                            'name': "GE2/0",
                            'status': True
                        },
                        {
                            'name': "GE2/1",
                            'status': True
                        },
                        {
                            'name': "GE2/2",
                            'status': True
                        },
                        {
                            'name': "GE2/3",
                            'status': True
                        },
                        {
                            'name': "GE3/0",
                            'status': True
                        },
                        {
                            'name': "GE3/1",
                            'status': True
                        },
                        {
                            'name': "GE3/2",
                            'status': True
                        },
                        {
                            'name': "GE3/3",
                            'status': True
                        },
                    ]
                }
            }
            #first = {'status': 'ON'}
            #second = {'status': 'OFF'}
            await websocket.send_json(first)
            #print("Sending")
            time.sleep(3)
            await websocket.send_json(second)
            time.sleep(3)
            # print(data)
            await websocket.send_json(third)
            time.sleep(3)
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')
