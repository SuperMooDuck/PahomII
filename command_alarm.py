from bot_module import bot
from alarm_module import alarm
from storage_module import storage
from telebot import types

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