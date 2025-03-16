import asyncio
import websockets
import json

clients = set()  # قائمة بجميع اللاعبين المتصلين

async def handler(websocket, path):
    clients.add(websocket)
    print(f"🔵 لاعب متصل! عدد اللاعبين الآن: {len(clients)}")

    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"📩 رسالة من لاعب: {data}")

            # بث الرسالة إلى جميع اللاعبين
            for client in clients:
                if client != websocket:
                    await client.send(json.dumps(data))

    except websockets.exceptions.ConnectionClosed:
        print("🔴 لاعب غادر!")
    finally:
        clients.remove(websocket)

async def start_server():
    server = await websockets.serve(handler, "0.0.0.0", 8080)
    print("🚀 السيرفر يعمل على المنفذ 8080")
    await server.wait_closed()

asyncio.run(start_server())
