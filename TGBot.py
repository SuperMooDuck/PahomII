# -*- coding: ansi -*-
import asyncio

from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot('')


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Hi, I am EchoBot.\nJust write me something and I will repeat it!'
    await bot.reply_to(message, text)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    if message.text.lower().endswith('- êòî?') :
        message.text = message.text.split('-')[0] + '- ãåé'
    await bot.reply_to(message, message.text)


from telebot import logger
import logging

logger.level = logging.DEBUG

asyncio.run(bot.polling())
