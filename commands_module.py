# -*- coding: ansi -*-
from alarm_module import alarm
import weather_module
from telebot import types
from bot_module import bot
from storage_module import storage
import re
import joy_parser_module

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
    #re.compile(reaction)
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
    if len(storage.text_reactions) <= number:
        await bot.answer_to(message, "Invalid reaction index.")
        return
    storage.text_reactions.pop(number)
    storage.save_data()
    await bot.answer_to(message, "Reaction removed.")
    await reaction_print(message)

@bot.register_command("test")
async def test(message : types.Message):

    async def SendMediaGroup(media_list : list[str]):
        caption : str = ''
        media_group : list[types.InputMedia] = []
        for media in media_list:
            match media[0]:
                case 'str':
                    caption = caption + media[1] + '\n'

                case 'img':
                    media_group.append(types.InputMediaPhoto(media[1]))

                case 'vid':
                    media_group.append(types.InputMediaVideo(media[1]))

        try:
            match len(media_group):
                case 0:
                    await bot.answer_to(message, caption, disable_web_page_preview = True)
                case 1:
                    match(type(media_group[0])):
                        case types.InputMediaVideo:
                            await bot.bot.send_video(message.chat.id, media_group[0].media, caption = caption, show_caption_above_media = True, parse_mode = "markdown")
                        case types.InputMediaPhoto:
                            await bot.bot.send_photo(message.chat.id, media_group[0].media, caption = caption, show_caption_above_media = True, parse_mode = "markdown")
                case _:
                    await bot.answer_to(message, caption, disable_web_page_preview = True)
                    await bot.bot.send_media_group(message.chat.id, media_group)

        except Exception as e:
            await bot.answer_to(message, '#Media sending failed#')

    
    posts = await joy_parser_module.joy_load_posts()

    for post in posts:
        tags_string = ""
        for tag in post[1]:
            tags_string += tag + " | "
        tags_string = tags_string[0:-3]

        media_list = [('str', f"[{post[0]}](https://joyreactor.cc/post/{post[0]})\n{tags_string}")]
        for content in post[2]:
            match (media_list[-1], content[0]):
                case ('iframe', _):
                    await bot.answer_to(message, text = media_list[-1][1])
                    media_list = [content]
                    
                case ('img'| 'vid', 'str'| 'iframe'):
                    await SendMediaGroup(media_list)
                    media_list = [content]

                case _:
                    media_list.append(content)

        if len(media_list) > 0:
            await SendMediaGroup(media_list)

