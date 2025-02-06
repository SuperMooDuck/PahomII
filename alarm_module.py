import asyncio

class Alarm:
    async def WorkCycle(self):
        while True:
            print("Alarm")
            await asyncio.sleep(30)

alarm = Alarm()