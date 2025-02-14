from alarm_module import alarm
import weather_module
from telebot import types
from bot_module import bot
from storage_module import storage


class FakeMessage:
    def __init__(self, chat_id, user_id = None, text = None):
        self.text = text
        self.chat = self.Chat(chat_id)
        self.from_user = self.From_user(user_id)

    class Chat:
         def __init__(self, id):
            self.type = "group"
            self.id = id            

    class From_user:
        def __init__(self, id):
            self.id = id

def home_chat_message(): 
    return FakeMessage(None, storage.home_chat_id, None)

@bot.register_command("sethomechat")
async def sethomechat(message : types.Message):
    if message.chat.type in ["group", "supergroup", "channel"]:
        storage.home_chat_id = message.chat.id
        storage.save_data()
        await bot.answer_to(message, text = f"Home chat set.")
    else:
        await bot.answer_to(message, text = f"Error. Chat must be group.")

@bot.register_command("say")
async def say(text : str, message : types.Message):
    await bot.bot.send_message(storage.home_chat_id, text = text)

@bot.register_command("weather")
async def weather(city : str = "both", days : int = 1, message : types.Message = None):
    if city == "both":
        await bot.answer_to(message, await weather_module.GetWeatherGismeteo("bir", days) + "\n" + await weather_module.GetWeatherGismeteo("khab", days))
    else:
        await bot.answer_to(message, await weather_module.GetWeatherGismeteo(city, days))

@bot.register_command("alarm")
async def alarm_add(action : str, *args : list, message : types.Message):
    match action:
        case "add":
            await alarm_add(*args, message = message)
        case "remove":
            await alarm_remove(*args, message = message)
        case "print":
            await alarm_print(message)
        case _:
            raise Exception("Unknown alarm action.")

async def alarm_add(time : str, command : str, *args : list, message : types.Message):
    if command not in bot.command_functions_list:
        raise Exception("Unknown command for alarm")
    alarm.add_alarm(time, command, bot.command_functions_list[command], args)
    storage.alarms.append((time, command, args))
    storage.save_data()
    await bot.answer_to(message, "Alarm added.")
    await alarm_print(message)

async def alarm_print(message : types.Message):
    reply = "```Alarms:\n"
    i = 0
    if len(storage.alarms) == 0:
        reply += "NO ALARMS"
    else:
        for time, command, args in storage.alarms:
            reply += f"{i} - {time}; {command}; {args}\n"
            i += 1
    reply += "```"
    await bot.answer_to(message, reply)

async def alarm_remove(number : int, message : types.Message):
    if len(storage.alarms) <= number:
        await bot.answer_to(message, "Invalid alarm index.")
        return
    alarm.remove_alarm(*storage.alarms.pop(number))
    storage.save_data()
    await bot.answer_to(message, "Alarm removed.")
    await alarm_print(message)

@bot.register_command("test")
async def test(message : types.Message  = home_chat_message()):
    await alarm.test_first_daily_alarm()