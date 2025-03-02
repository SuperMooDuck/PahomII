# -*- coding: ansi -*-
import asyncio
import logging
from alarm_module import alarm
from telebot import logger
from storage_module import storage
from bot_module import bot
import commands_module


async def main():
    load_alarms()
    bot.init_telebot()
    asyncio.create_task(alarm.WorkCycle())
    print ("Bot started")
    await bot.WorkCycle()

def load_alarms():
    for type_and_time, command_name, args in storage.alarms:
        alarm.add_alarm(type_and_time, command_name, bot.command_functions_list[command_name], args)

#logger.level = logging.DEBUG
asyncio.run(main())