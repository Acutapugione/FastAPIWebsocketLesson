import asyncio
import websockets


async def main():
    async with websockets.connect("ws://localhost:8001/mama_mila_dupu") as ws:
        await ws.send("Hello, server!", text=True)
        message = await ws.recv()
        print(f"Received: {message}")


asyncio.run(main())
