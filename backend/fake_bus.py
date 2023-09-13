import json
import os
from pathlib import Path
from sys import stderr

import trio
from trio_websocket import open_websocket_url


def load_routes(directory_path='routes'):
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf8') as file:
                yield json.load(file)


async def run_bus(url, bus_id, route):
    while True:
        try:
            async with open_websocket_url(url) as ws:
                for coordinate in route['coordinates']:
                    bus = {'busId': bus_id, 'lat': coordinate[0], 'lng': coordinate[1], 'route': bus_id}
                    await ws.send_message(json.dumps(bus))
                    await trio.sleep(1)
        except  OSError as ose:
            print('Connection attempt failed: %s' % ose, file=stderr)
            break


async def main():
    url = 'ws://127.0.0.1:8080'
    async with trio.open_nursery() as nursery:
        for route in load_routes():
            nursery.start_soon(run_bus, url, route['name'], route)


if __name__ == '__main__':
    trio.run(main)
