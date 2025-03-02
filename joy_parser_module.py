import asyncio

import bs4
import aiohttp
from bs4 import BeautifulSoup
from telebot import types
from storage_module import storage

async def joy_load_posts() -> None:
    url : str = "https://joyreactor.cc/new"
    result_posts_list : list[(int, list[str], list[str])] = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            posts = BeautifulSoup(await response.text(), "html.parser" ).find_all("div", class_ = "content")

    for post in posts:
        content_list = post.find("div", class_ = "post-content")
        if not content_list: continue
        
        post_id : int = int(post.find("div", class_ = "flex gap-2 xl:gap-1").find("a")["href"].split("/")[2])
        if not store_post_id_if_new(post_id): continue

        post_tags : list[str] = []
        for tag in post.find("div", class_ = "post-tags").find_all("a"):
            post_tags.append(tag.string)

        result_content_list : list[str] = []
        for content in content_list.children:
            content_string = parse_post_content(content)
            if type(content_string) is list:
                result_content_list.extend(content_string)
            else:
                result_content_list.append(content_string)

        result_posts_list.append((post_id, post_tags, result_content_list))
    
    return result_posts_list

def parse_post_content(content_bs : bs4.ResultSet) -> str:
    if content_bs.name == "div" and not content_bs.has_attr("class"):
        content_list : list[str] = []
        for c in content_bs.children:
            content_list.append(parse_post_content(c))
        return content_list

    if (content_bs.string):
        return ('str', content_bs.string)

    img = content_bs.find("img")
    if img: return ('img', img["src"])

    video = content_bs.find("video")
    if video: return ('vid', video["data-src"].replace("webm", "mp4"))

    iframe = content_bs.find("iframe")
    if iframe: return ('iframe', iframe["src"])

    return "#UNSUPPORTED CONTENT#"

STORED_POST_LIMIT = 50

def store_post_id_if_new(post_id : int) -> bool:
    if post_id in storage.joy_old_post_ids: return False
    if len(storage.joy_old_post_ids) >= 50: storage.joy_old_post_ids.pop(0)
    storage.joy_old_post_ids.append(post_id)
    storage.save_data()
    return True