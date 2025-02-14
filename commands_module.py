# -*- coding: ansi -*-
from alarm_module import alarm
import weather_module
from telebot import types
from bot_module import bot
from storage_module import storage
import re

@bot.register_command("start")
async def start(message : types.Message):
    await bot.answer_to(message, text = "Рыба - карась, игра - началась.")

@bot.register_command("help")
async def start(message : types.Message):
    await bot.answer_to(message, text = "За помощью - обращайтесь к психиатору.")

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

@bot.register_command("reaction")
async def reaction(action : str, *args : list, message : types.Message):
    match action:
        case "print":
            await reaction_print(*args, message = message)
        case "add":
            await reaction_add(*args, message = message)
        case "remove":
            await reaction_remove(*args, message = message)
        case _:
            raise Exception("Unknown reaction action")

async def reaction_add(mask : str, reaction : str, message : types.Message):
    re.compile(mask)
    re.compile(reaction)
    storage.text_reactions.append((mask, reaction))
    storage.save_data()
    await bot.answer_to(message, "Reaction added.")
    await reaction_print(message)

async def reaction_print(message : types.Message):
    reply = "```\nText reactions:\n"
    i = 0
    for mask, reaction in storage.text_reactions:
        reply += f"{i} : {mask} - {reaction}\n"
        i += 1
    reply += "```"
    await bot.answer_to(message, reply)

async def reaction_remove(number : int, message : types.Message):
    if len(storage.alarms) <= number:
        await bot.answer_to(message, "Invalid reaction index.")
        return
    storage.text_reactions.pop(number)
    storage.save_data()
    await bot.answer_to(message, "Reaction removed.")
    await reaction_print(message)

@bot.register_command("test")
async def test(message : types.Message):
    await alarm.test_first_daily_alarm()