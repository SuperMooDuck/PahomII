from telebot import types
from telebot import async_telebot
import re
from storage_module import storage
import logging
from typing import Callable

class Bot:

    class FakeMessage:

        class Chat:
             def __init__(self, id):
                self.type = "group"
                self.id = id            

        class From_user:
            def __init__(self, id):
                self.id = id

        def __init__(self, chat_id : int, user_id : int = None, text : str = None):
            self.text = text
            self.chat = self.Chat(chat_id)
            self.from_user = self.From_user(user_id)

    command_functions_list : dict[str, Callable]
    re_arguments : re.Pattern
    bot : async_telebot.AsyncTeleBot

    def __init__(self):
        self.command_functions_list = {}
        self.re_arguments = re.compile(r'"[^"]+"|[^\s"]+')

    def init_telebot(self):
        self.bot = async_telebot.AsyncTeleBot(storage.bot_key)
        self.bot.register_message_handler(self.any_message_handler, func=lambda message: True)
        self.bot.register_inline_handler(self.inline_handler,  func=lambda message: True)

    async def WorkCycle(self):
        await self.bot.infinity_polling(skip_pending=True)

    async def answer_to(self, message : types.Message, text : str, **kwargs):
        await self.bot.send_message(message.chat.id, text, parse_mode = "markdown", **kwargs) 

    async def any_message_handler(self, message : types.Message):
        if message.text.startswith("/"): 
            await self.command_handler(message)
        else:
            await self.text_reaction_handler(message)

    async def text_reaction_handler(self, message : types.Message) -> str :
        for re_mask, reaction in storage.text_reactions:
            re_match = re.fullmatch(re_mask, message.text.lower())
            if not re_match: continue
            await self.answer_to(message, text = re_match.expand(reaction))
            return

    async def command_handler(self, message : types.Message):
        try:
            command, separator, arguments_string =  message.text[1:].partition(" ")
            if command.find("@") > -1:
                command, separator, name = command.partition("@")
                actual_name = (await bot.bot.get_me()).username
                if actual_name != name: return

            args : list[str] = []
            for arg in self.re_arguments.findall(arguments_string):
                if arg.startswith('"'):
                    args.append(arg[1:-1])
                elif arg.isdecimal():
                    args.append(int(arg))
                else:
                    args.append(arg)

            if command in self.command_functions_list:
                await self.command_functions_list[command](*args, message = message)

        except Exception as e:
            logging.exception("Command error. ")
            await self.bot.send_message(message.chat.id, text = f"Command error: {type(e).__name__}. {e}")

    def register_command(self, command_name : str):
        def decorator(command_function):
            async def decorated_function(*args, message : types.Message = None):
                if message == None:
                    message = self.FakeMessage(storage.home_chat_id)
                await command_function(*args, message = message)
            self.command_functions_list[command_name] = decorated_function
            return decorated_function
        return decorator

    async def inline_handler(self, query: types.InlineQuery):
        print("Inline handler")
        a = types.InlineQueryResultArticle('1', 'Вилкой в глаз.', types.InputTextMessageContent('Вилкой в глаз.'))
        b = types.InlineQueryResultArticle('2', 'В жопу раз.', types.InputTextMessageContent('В жопу раз.'))
        await self.bot.answer_inline_query(query.id,results = [a, b])        

bot = Bot()