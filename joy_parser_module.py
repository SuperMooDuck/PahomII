import asyncio
import aiohttp
from bs4 import BeautifulSoup
from telebot import types

async def joy_load_posts() -> None:
    url = "https://joyreactor.cc/new"
    posts_list = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            posts = BeautifulSoup(await response.text(), "html.parser" ).find_all("div", class_ = "content")

    for post in posts:
        
        post_id = int(post.find("div", class_ = "flex gap-2 xl:gap-1").find("a")["href"].split("/")[2])
        #print (post_id)

        post_tags = []
        for tag in post.find("div", class_ = "post-tags").find_all("a"):
            post_tags.append(tag.string)
        #print (post_tags)

        content_list = []
        for content in post.find("div", class_ = "post-content").children:
            
            if (content.string):
                content_list.append(content.string) #print (content.string)
                continue

            if not content.has_attr("class"):
                iframe = content.find("iframe")
                if iframe: content_list.append(iframe["src"])#print(iframe["src"])
                else:             print("shit")
                continue

            match (content["class"][0]):
                case "image" | "single":
                    content_list.append(types.InputMediaPhoto(content.find("img")["src"]))#print (content.find("img")["src"])
                    continue
                case "ant-spin-nested-loading":
                    content_list.append(types.InputMediaVideo(content.find("video")["data-src"].replace("webm", "mp4")))#print (content.find("video")["data-src"].replace("webm", "mp4"))
                    continue
            
            print("shit")

        print ("************************************")