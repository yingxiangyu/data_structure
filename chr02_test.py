import asyncio
import websockets


async def hello(websocket, path):
    name = await websocket.revc()
    print(f"< {name}")
    greeting = f"hello {name}"
    await websocket.send(greeting)
    print(f"> {greeting}")


start_server = websockets.serve(hello, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
