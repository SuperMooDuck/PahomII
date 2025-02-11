import asyncio
from telebot import types
from telebot import async_telebot
import re
from storage_module import storage
import weather_module
import traceback

bot = async_telebot.AsyncTeleBot(storage.bot_key)

async def WorkCycle():
    await bot.infinity_polling(skip_pending=True)

@bot.message_handler(func=lambda message: True)
async def any_message_handler(message : types.Message):
    if message.text.startswith("/"): 
        await command_handler(message)
    else:
        await text_reaction_handler(message)

@bot.inline_handler(lambda query: True)
async def inline_handler(query: types.InlineQuery):
    print("Inline handler")
    a = types.InlineQueryResultArticle('1', 'Вилкой в глаз.', types.InputTextMessageContent('Вилкой в глаз.'))
    b = types.InlineQueryResultArticle('2', 'В жопу раз.', types.InputTextMessageContent('В жопу раз.'))
    await bot.answer_inline_query(query.id,results = [a, b])


async def text_reaction_handler(message : types.Message) -> str :
    for re_mask in storage.text_reactions:
        re_match = re.fullmatch(re_mask, message.text.lower())
        if not re_match: continue
        await bot.send_message(message.chat.id, text = re_match.expand(storage.text_reactions[re_mask]))
        return

command_functions_list = {"weather": weather_module.GetWeatherGismeteo}

async def command_handler(message : types.Message):
    try:
        splited_strings = message.text[1:].split(" ")
        if splited_strings[0].find("@") > -1:
            splited_strings[0] = splited_strings[0][0:splited_strings[0].find("@")]

        for command in command_functions_list:
            if command != splited_strings[0]: continue;
            await bot.send_message(message.chat.id, text = await command_functions_list[command](*splited_strings[1:]), parse_mode="Markdown")
    except Exception as e:
        print(traceback.format_exc())
        await bot.send_message(message.chat.id, text = f"Command error: {e}")