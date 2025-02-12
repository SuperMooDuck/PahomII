import weather_module
from telebot import types
from bot_module import bot
from bot_module import register_command
from bot_module import answer_to
from storage_module import storage

class FMessage:
	def __init__(self, user_id, chat_id, text):
		self.text = text
		self.chat = self.Chat(chat_id)
		self.from_user = self.From_user(user_id)

	class Chat:
		def __init__(self, id):
			self.id = id

	class From_user:
		def __init__(self, id):
			self.id = id

home_chat_message = FMessage(None, storage.home_chat_id, None)

@register_command("sethomechat")
async def set_home_chat(message : types.Message):
    if message.chat.type in ["group", "supergroup", "channel"]:
        storage.home_chat_id = message.chat.id
        storage.save_data()
        await bot.send_message(message.chat.id, text = f"Home chat set.")
    else:
        await bot.send_message(message.chat.id, text = f"Error. Chat must be group.")

@register_command("say")
async def send_to_home_chat(message : types.Message, text : str):
    await bot.send_message(storage.home_chat_id, text = text)

@register_command("weather")
async def weather(message : types.Message, city : str = "both", days : int = 1):
    if city == "both":
        await answer_to(message, await weather_module.GetWeatherGismeteo("bir", days) + "\n" + await weather_module.GetWeatherGismeteo("khab", days))
    else:
        await answer_to(message, await weather_module.GetWeatherGismeteo(city, days))