from bot_module import bot
from telebot import types
import joy_parser_module

@bot.register_command("test")
async def test(*args : list, message : types.Message):

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

                case 'iframe':
                    await bot.bot.send_message(message.chat.id, media[1])
                    return

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
            await bot.answer_to(message, f'#Media sending failed# {e}')

    
    posts = await joy_parser_module.joy_load_posts(*args)

    for post in posts:
        tags_string = ""
        for tag in post[1]:
            tags_string += tag + " | "
        tags_string = tags_string[0:-3]

        media_list : list[(str, str)] = [('str', f"[{post[0]}](https://joyreactor.cc/post/{post[0]})\n{tags_string}")]
        for content in post[2]:
            match (media_list[-1][0], content[0]):
                case ('iframe', _):
                    await bot.answer_to(message, text = media_list[-1][1])
                    media_list = [content]
                    
                case ('img'| 'vid', 'str'| 'iframe') | ('str', 'iframe'):
                    await SendMediaGroup(media_list)
                    media_list = [content]

                case _:
                    media_list.append(content)

        if len(media_list) > 0:
            await SendMediaGroup(media_list)


