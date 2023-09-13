import json
from pathlib import Path

import trio
from trio_websocket import serve_websocket, ConnectionClosed


async def get_messages(request):
    ws = await request.accept()
    while True:
        try:
            message = await ws.get_message()
            print(message)
            await trio.sleep(1)
        except ConnectionClosed:
            break


async def main():
    await serve_websocket(get_messages, '127.0.0.1', 8080, ssl_context=None)


if __name__ == '__main__':
    trio.run(main)
