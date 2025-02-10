import asyncio
import logging
from alarm_module import alarm
from telebot import logger
from storage_module import storage
import bot_module

async def main():
    asyncio.create_task(alarm.WorkCycle())
    await bot_module.WorkCycle()

logger.level = logging.DEBUG
asyncio.run(main())