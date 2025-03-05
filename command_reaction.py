import re
from telebot import types
from bot_module import bot
from storage_module import storage

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
