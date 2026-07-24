import asyncio
from websockets.asyncio.server import serve

from server import Server

server = Server()

server.room_manager.create("Python", "Aryel", True, "123")
server.room_manager.create("JavaScript", "Aryel", True)

async def main():
    async with serve(server.handler, "0.0.0.0", 8000):
        print("Servidor iniciado.")
        await asyncio.Future()

asyncio.run(main())