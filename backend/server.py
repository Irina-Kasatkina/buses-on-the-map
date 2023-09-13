import json
from pathlib import Path

import trio
from trio_websocket import serve_websocket, ConnectionClosed

async def echo_server(request):
    ws = await request.accept()
    with open(Path('data') / '156.json', 'r', encoding='utf-8') as file_156:
        coordinates = json.loads(file_156.read())['coordinates']

    while True:
        try:
            for coordinate in coordinates:
                buses = {
                    "msgType": "Buses",
                      "buses": [
                          {"busId": "a156", "lat": coordinate[0], "lng": coordinate[1], "route": "156"},
                      ]
                }
                await ws.send_message(json.dumps(buses))
                await trio.sleep(1)
        except ConnectionClosed:
            break

async def main():
    await serve_websocket(echo_server, '127.0.0.1', 8000, ssl_context=None)

trio.run(main)
