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

async def set_home_chat(message : types.Message):
    if message.chat.type in ["group", "supergroup", "channel"]:
        storage.home_chat_id = message.chat.id
        storage.save_data()
        await bot.send_message(message.chat.id, text = f"Home chat set.")
    else:
        await bot.send_message(message.chat.id, text = f"Error. Chat must be group.")

async def send_to_home_chat(text : str):
    await bot.send_message(storage.home_chat_id, text = text)

command_functions_list = {"weather": weather_module.GetWeatherGismeteo,
                          "say": send_to_home_chat}

async def command_handler(message : types.Message):
    try:
        command, separator, arguments_string =  message.text[1:].partition(" ")
        if command.find("@") > -1:
            command, separator, name = command.partition("@")
            if bot.get_my_name != name: return

        args = []
        while len(arguments_string) > 0:
            nearest_space = args.find(" ")
            nearest_quote = args.find("\"")
            if nearest_space < nearest_quote:
                args.append(arguments_string[0:nearest_space])
                arguments_string = arguments_string[nearest_space+1:]



        splited_strings = message.text[1:].split(" ")
        if splited_strings[0].find("@") > -1:
            splited_strings[0] = splited_strings[0][0:splited_strings[0].find("@")]

        if splited_strings[0] == "sethomechat":
            await set_home_chat(message)
            return

        for command in command_functions_list:
            if command != splited_strings[0]: continue;
            await bot.send_message(message.chat.id, text = await command_functions_list[command](*splited_strings[1:]), parse_mode="Markdown")
    except Exception as e:
        print(traceback.format_exc())
        await bot.send_message(message.chat.id, text = f"Command error: {e}")
