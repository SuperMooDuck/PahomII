# -*- coding: ansi -*-
import asyncio
import logging
from alarm_module import alarm
from telebot import logger
from storage_module import storage
import bot_module
import commands_module

async def main():
    asyncio.create_task(alarm.WorkCycle())
    print ("Bot started")
    await bot_module.WorkCycle()

#logger.level = logging.DEBUG
import datetime

asyncio.run(main())