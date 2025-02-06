import asyncio
import telebot
from telebot import async_telebot
import re
from storage_module import storage

bot = async_telebot.AsyncTeleBot(storage.bot_key)

async def WorkCycle():
    await bot.infinity_polling(skip_pending=True)

'''
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Hi, I am EchoBot.\nJust write me something and I will repeat it!'
    await bot.reply_to(message, text)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    if message.text.lower().endswith('- gay?') :
        message.text = message.text.split('-')[0] + '- gay'
    await bot.reply_to(message, message.text)
'''

@bot.message_handler(chat_types = ["group", "supergroup", "channel"])
async def any_group_message(message : telebot.types.Message):
    print ("group message")
    text_reaction = get_text_reaction(message)
    if text_reaction:
        await bot.send_message(message.chat.id, text = text_reaction)

def get_text_reaction(message : telebot.types.Message) -> str :
    reply = ""
    for re_mask in storage.text_reactions:
        re_match = re.fullmatch(re_mask, message.text.lower())
        if not re_match: continue
        reply_template = storage.text_reactions[re_mask]

        part_start = 0
        part_index = 1
        index = 0
        for c in reply_template:
            if c == "\\" and reply_template[index + 1].isdigit():
                reply += reply_template[part_start: index] + re_match.group(part_index)
                index += 1
                part_index += 1
                part_start = index + 1
            index += 1
        if part_start < len(reply_template):
            reply += reply_template[part_start:]
    return reply
