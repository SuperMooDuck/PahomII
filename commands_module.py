# -*- coding: ansi -*-
from telebot import types
from bot_module import bot
from storage_module import storage
import weather_module

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
