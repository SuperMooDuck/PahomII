# -*- coding: ansi -*-
import asyncio
import logging
from alarm_module import alarm
from telebot import logger
from storage_module import storage
import bot_module

logger.level = logging.DEBUG

storage.text_reactions["^да.?$"] = "Пизда"
storage.text_reactions[r"(.+)-.*кто\?"] = r"\1 - гей"

async def main():
    asyncio.create_task(alarm.WorkCycle())
    await bot_module.WorkCycle()

asyncio.run(main())