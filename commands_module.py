from alarm_module import alarm
import weather_module
from telebot import types
import bot_module
from storage_module import storage


class FakeMessage:
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

home_chat_message = FakeMessage(None, storage.home_chat_id, None)

@bot_module.register_command("sethomechat")
async def set_home_chat(message : types.Message):
    if message.chat.type in ["group", "supergroup", "channel"]:
        storage.home_chat_id = message.chat.id
        storage.save_data()
        await bot_module.bot.send_message(message.chat.id, text = f"Home chat set.")
    else:
        await bot_module.bot.send_message(message.chat.id, text = f"Error. Chat must be group.")

@bot_module.register_command("say")
async def send_to_home_chat(message : types.Message, text : str):
    await bot_module.bot.send_message(storage.home_chat_id, text = text)

@bot_module.register_command("weather")
async def weather(message : types.Message, city : str = "both", days : int = 1):
    if city == "both":
        await bot_module.answer_to(message, await weather_module.GetWeatherGismeteo("bir", days) + "\n" + await weather_module.GetWeatherGismeteo("khab", days))
    else:
        await bot_module.answer_to(message, await weather_module.GetWeatherGismeteo(city, days))

@bot_module.register_command("alarmadd")
async def alarm_add(message : types.Message, time : str, command : str, args : list):
    alarm.add_alarm(time, bot_module.command_functions_list[command], args)