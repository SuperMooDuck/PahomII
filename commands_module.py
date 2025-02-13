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
async def sethomechat(message : types.Message = home_chat_message):
    if message.chat.type in ["group", "supergroup", "channel"]:
        storage.home_chat_id = message.chat.id
        storage.save_data()
        await bot_module.bot.send_message(message.chat.id, text = f"Home chat set.")
    else:
        await bot_module.bot.send_message(message.chat.id, text = f"Error. Chat must be group.")

@bot_module.register_command("say")
async def say(text : str, message : types.Message = home_chat_message):
    await bot_module.bot.send_message(storage.home_chat_id, text = text)

@bot_module.register_command("weather")
async def weather(city : str = "both", days : int = 1, message : types.Message  = home_chat_message):
    if city == "both":
        await bot_module.answer_to(message, await weather_module.GetWeatherGismeteo("bir", days) + "\n" + await weather_module.GetWeatherGismeteo("khab", days))
    else:
        await bot_module.answer_to(message, await weather_module.GetWeatherGismeteo(city, days))

@bot_module.register_command("alarmadd")
async def alarm_add(time : str, command : str, *args : list, message : types.Message  = home_chat_message):
    if command not in bot_module.command_functions_list:
        raise Exception("Unknown command for alarm")

    alarm.add_alarm(time, bot_module.command_functions_list[command], args)
    storage.alarms.append((time, bot_module.command_functions_list[command], args))
    storage.save_data()
    await bot_module.answer_to(message, "Alarm added.")
    await alarm_print(message)

@bot_module.register_command("alarmprint")
async def alarm_print(message : types.Message  = home_chat_message):
    reply = "```Alarms:\n"
    i = 0
    if len(storage.alarms) == 0:
        reply += "NO ALARMS"
    else:
        for time, command, args in storage.alarms:
            reply += f"{i} - {time}; {command.__name__}; {args}\n"
            i += 1
    reply += "```"
    await bot_module.answer_to(message, reply)

@bot_module.register_command("alarmremove")
async def alarm_remove(number : int, message : types.Message  = home_chat_message):
    if len(storage.alarms) <= number:
        await bot_module.answer_to(message, "Invalid alarm index.")
        return
    alarm.remove_alarm(*storage.alarms.pop(number))
    storage.save_data()
    await bot_module.answer_to(message, "Alarm removed.")
    await alarm_print(message)
