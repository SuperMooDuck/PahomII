# -*- coding: ansi -*-
import asyncio
import logging
from alarm_module import alarm
from storage_module import storage
from bot_module import bot
import commands_module
import sys

async def main():
    log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
    log_file_handler = logging.FileHandler("TGBot.log")
    log_file_handler.setFormatter(log_formatter)
    log_stream_handler = logging.StreamHandler()
    log_stream_handler.setFormatter(log_formatter)
    logging.getLogger().addHandler(log_file_handler)
    logging.getLogger().addHandler(log_stream_handler)

    storage.load_data()
    if len(sys.argv) > 1:
        logging.warning("Inintializing bot with new token.")
        storage.bot_key = sys.argv[1]
    alarm.load_alarms(storage.alarms)
    bot.init_telebot()

    logging.warning("Bot started")
    asyncio.create_task(alarm.WorkCycle())
    await bot.WorkCycle()

asyncio.run(main())