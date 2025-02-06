# -*- coding: ansi -*-
import asyncio
import logging
from alarm_module import alarm
from telebot import logger
from storage_module import storage


logger.level = logging.DEBUG

storage.bot_key = "7659409584:AAH7Mj-Sxj1RMIqu9MaHfv8iWRb3ofSl9Kw"
storage.text_reactions["^��.?$"] = "�����"
storage.text_reactions[r"(.+)-.*���\?"] = r"\1 - ���"
storage.save_data()

import bot_module

async def main():
    asyncio.create_task(alarm.WorkCycle())
    await bot_module.WorkCycle()

asyncio.run(main())