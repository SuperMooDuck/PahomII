

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

@bot.message_handler(chat_types = ["group", "supergroup", "channel"])
async def any_group_message(message : telebot.types.Message):
    text_reaction = get_text_reaction(message)
    if text_reaction:
        bot.send_message(message.chat.id, text = text_reaction)

def get_text_reaction(message : telebot.types.Message) -> str :
    reply = None
    for re_mask in storage_object.text_reactions.keys:
        re_match = re.fullmatch(re_mask, message.text.lower())
        if not re_match: continue
        reply_template = storage_object.text_reactions[re_mask]

        part_start = 0
        part_index = 1
        index = 0
        for c in reply_template:
            if c == "\\" and reply_template[index + 1].is_digit():
                reply += reply_template[part_start: index] + re_match.group[part_index]
                index += 1
                part_index += 1
                part_start = index + 1
            index += 1
        if part_start < len(reply_template):
            reply += reply_template[part_start:]
    return reply