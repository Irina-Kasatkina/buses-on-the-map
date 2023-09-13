import json
from pathlib import Path
from sys import stderr

import trio
from trio_websocket import open_websocket_url


async def main():
    with open(Path('data') / '156.json', 'r', encoding='utf-8') as file_156:
        coordinates = json.loads(file_156.read())['coordinates']

    while True:
        try:
            async with open_websocket_url('ws://127.0.0.1:8080') as ws:
                for coordinate in coordinates:
                    bus = {"busId": "a156", "lat": coordinate[0], "lng": coordinate[1], "route": "156"}
                    await ws.send_message(json.dumps(bus))
                    await trio.sleep(1)
        except  OSError as ose:
            print('Connection attempt failed: %s' % ose, file=stderr)
            break


if __name__ == '__main__':
    trio.run(main)
