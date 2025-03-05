# -*- coding: ansi -*-
import asyncio
import logging
from alarm_module import alarm
from telebot import logger
from storage_module import storage
from bot_module import bot
import commands_module
import sys


async def main():
    if len(sys.argv) > 1:
        pass
    storage.load_data()
    alarm.load_alarms(storage.alarms)
    bot.init_telebot()
    asyncio.create_task(alarm.WorkCycle())
    print ("Bot started")
    await bot.WorkCycle()

#logger.level = logging.DEBUG
asyncio.run(main())