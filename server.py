import asyncio
import websockets

# قائمة الغرف (كل غرفة تحتوي على 6 لاعبين كحد أقصى)
rooms = {}

async def handler(websocket, path):
    try:
        print("🔵 لاعب متصل!")
        
        # استقبال أول رسالة من اللاعب
        message = await websocket.recv()
        print(f"📩 استلمت: {message}")

        if message == "join":
            # البحث عن غرفة غير ممتلئة
            joined_room = None
            for room_id, players in rooms.items():
                if len(players) < 6:
                    joined_room = room_id
                    players.append(websocket)
                    break

            # إذا لم تكن هناك غرفة متاحة، أنشئ غرفة جديدة
            if joined_room is None:
                joined_room = len(rooms) + 1
                rooms[joined_room] = [websocket]

            await websocket.send(f"room:{joined_room}")
            print(f"✅ لاعب انضم إلى الغرفة {joined_room}")

            # التحقق إذا امتلأت الغرفة والبدء
            if len(rooms[joined_room]) == 6:
                await start_race(joined_room)

        # الاستماع للرسائل القادمة من العميل
        async for message in websocket:
            print(f"📨 رسالة من اللاعب: {message}")

    except websockets.exceptions.ConnectionClosed:
        print("🔴 لاعب قطع الاتصال!")
    
async def start_race(room_id):
    """بدء السباق عندما تكتمل الغرفة"""
    print(f"🏁 بدء السباق في الغرفة {room_id}!")
    for player in rooms[room_id]:
        await player.send("start_race")

# تشغيل السيرفر على المنفذ 8080
start_server = websockets.serve(handler, "0.0.0.0", 8080)

print("🚀 سيرفر Godot WebSocket يعمل على المنفذ 8080...")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
