import asyncio
import logging
from alarm_module import alarm
from telebot import logger
from storage_module import storage


logger.level = logging.DEBUG

import bot_module

async def main():
    asyncio.create_task(alarm.WorkCycle())
    await bot_module.WorkCycle()

asyncio.run(main())