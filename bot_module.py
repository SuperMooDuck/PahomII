import asyncio
import telebot
from telebot import async_telebot
import re
from storage_module import storage
import weather_module

bot = async_telebot.AsyncTeleBot(storage.bot_key)

async def WorkCycle():
    await bot.infinity_polling(skip_pending=True)

@bot.message_handler(func=lambda message: True)
async def any_message_handler(message : telebot.types.Message):
    if message.text.startswith("/"): 
        await command_handler(message)
        return
    await text_reaction_handler(message)

@bot.inline_handler(lambda query: True)
async def inline_handler(query: telebot.types.InlineQuery):
    print("Inline handler")
    a = telebot.types.InlineQueryResultArticle('1', 'Вилкой в глаз.', telebot.types.InputTextMessageContent('Вилкой в глаз.'))
    b = telebot.types.InlineQueryResultArticle('2', 'В жопу раз.', telebot.types.InputTextMessageContent('В жопу раз.'))
    await bot.answer_inline_query(query.id,results = [a, b])


async def text_reaction_handler(message : telebot.types.Message) -> str :
    for re_mask in storage.text_reactions:
        re_match = re.fullmatch(re_mask, message.text.lower())
        if not re_match: continue
        await bot.send_message(message.chat.id, text = re_match.expand(storage.text_reactions[re_mask]))
        return

async def command_handler(message : telebot.types.Message):
    if not message.text.startswith("/"): return
    try:
        splited_strings = message.text[1:].split(" ")
        reply = None
        match splited_strings[0]:
            case "weather":
                if len(splited_strings) == 1: reply = await weather_module.GetWeatherGismeteo()
                else: reply = await weather_module.GetWeatherGismeteo(*splited_strings[1:])
        if reply:
            await bot.send_message(message.chat.id, text = reply)
    except:
        await bot.send_message(message.chat.id, text = "Command error")