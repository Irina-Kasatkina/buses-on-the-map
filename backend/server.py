import json
import logging

import trio
from trio_websocket import serve_websocket, ConnectionClosed, WebSocketRequest


buses = {}


async def get_bus_updates(request: WebSocketRequest):
    global buses
    ws = await request.accept()
    while True:
        try:
            message = await ws.get_message()
            bus_info = json.loads(message)
            logging.warning(f'get_messages(): bus_info={bus_info}')
            buses[bus_info['busId']] = bus_info
            await trio.sleep(1)
        except ConnectionClosed:
            break


async def talk_to_browser(request: WebSocketRequest):
    global buses
    ws = await request.accept()
    while True:
        try:
            response = json.dumps({
                'msgType': 'Buses',
                'buses': [buses[bus_id] for bus_id in buses],
            })
            logging.warning(f'talk_to_browser(): response={response}')
            await ws.send_message(response)
            await trio.sleep(1)
        except ConnectionClosed:
            break    


async def main():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(serve_websocket, get_bus_updates, '127.0.0.1', 8080, None)
        nursery.start_soon(serve_websocket, talk_to_browser, '127.0.0.1', 8000, None)


if __name__ == '__main__':
    trio.run(main)
