# -*- coding: ansi -*-
import asyncio
import logging
from alarm_module import alarm
from telebot import logger
from storage_module import storage
import bot_module

async def main():
    asyncio.create_task(alarm.WorkCycle())
    await bot_module.WorkCycle()

#logger.level = logging.DEBUG
import datetime
alarm.add_periodical_alarm(datetime.time(minute = 1), bot_module.send_to_home_chat, ["≈жеминутное напоминание, что вы все пидоры"])

asyncio.run(main())