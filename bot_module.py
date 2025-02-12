from telebot import types
from telebot import async_telebot
import re
from storage_module import storage
import traceback

bot = async_telebot.AsyncTeleBot(storage.bot_key)

async def WorkCycle():
    await bot.infinity_polling(skip_pending=True)

async def answer_to(message : types.Message, text : str):
    await bot.send_message(message.chat.id, text, parse_mode = "markdown" )

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

command_functions_list = {}

re_arguments = re.compile(r'"[^"]+"|[^\s"]+')
async def command_handler(message : types.Message):
    try:
        command, separator, arguments_string =  message.text[1:].partition(" ")
        if command.find("@") > -1:
            command, separator, name = command.partition("@")
            actual_name = (await bot.get_me()).username
            if actual_name != name: return

        args = []
        for arg in re_arguments.findall(arguments_string):
            if arg.startswith('"'):
                args.append(arg[1:-1])
            elif arg.isdecimal():
                args.append(int(arg))
            else:
                args.append(arg)

        if command_functions_list[command]:
            await command_functions_list[command](message, *args)

    except Exception as e:
        print(traceback.format_exc())
        await bot.send_message(message.chat.id, text = f"Command error: {e}")

def register_command(command_name : str):
    def decorator(command_function):
        command_functions_list[command_name] = command_function
    return decorator