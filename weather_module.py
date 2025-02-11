# -*- coding: ansi -*-
import aiohttp
import asyncio
import re
import emoji
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup


async def GetWeatherGismeteo(city:str = "both", days:int = 1) -> str:
    if type(days) is str:
        days = int(days)

    base_url = "https://www.gismeteo.ru/"
    match city:
        case "bir": 
            city = "Биробиджан"
            base_url += "weather-birobidzhan-4860/"
        case "khab": 
            city = "Хабаровск"
            base_url += "weather-khabarovsk-4862/"
        case "both":
            return await GetWeatherGismeteo("bir", days) + "\n" + await GetWeatherGismeteo("khab", days)
        case _: 
            raise Exception("Unknown city for Gismeteo weather")
    
    reply = f"Погода от Gismeteo.ru для города {city}\n"

    for day in range(days):
        
        url = base_url
        if day > 1:
            url += f"{day+1}-day/"
        elif day > 0:
            url += f"tomorrow/"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                base_div = BeautifulSoup(await response.text(), "html.parser" ).find("div", {"class" : "widget-body"})

        reply += "```"

        list_time = []
        for div in base_div.find("div", {"class" : "widget-row widget-row-datetime-time"}).find_all("span"):
            list_time.append(div.string)

        list_wind = []
        for div in base_div.find("div", {"class" : "widget-row widget-row-wind row-wind-gust row-with-caption"}).find_all("speed-value", value=True):
            list_wind.append(div["value"])

        list_rain = []
        for div in base_div.find("div", {"class" : "widget-row widget-row-precipitation-bars row-with-caption"}).find_all("div", {"class" : re.compile("item-unit.*")}):
            list_rain.append(div.string)

        list_temp = []
        for div in base_div.find("div", {"class" : "widget-row-chart widget-row-chart-temperature-air row-with-caption"}).find_all("temperature-value", value=True):
            list_temp.append(f"+{div["value"]}" if int(div["value"]) > 0 else div["value"])

        list_overcast = []
        for div in base_div.find("div", {"class" : "widget-row widget-row-icon"}).find_all("div", {"class" : "row-item"}):
            value = div["data-tooltip"].lower()
            emoji_text = ""
            if value.find("ясно") > -1:
                emoji_text = ":sun:"
            elif value.find("гроза") > -1:
                emoji_text = ":cloud_with_lightning_and_rain:"
            else:
                sun =  0 if value.find("пасмурно") > -1 else 1
                rain =  1 if value.find("дождь") > -1 or value.find("снег") > -1 else 0
                match (sun, rain):
                    case (1, 0): emoji_text = ":sun_behind_cloud:"
                    case (0, 1): emoji_text = ":cloud_with_rain:"
                    case (1, 1): emoji_text = ":sun_behind_rain_cloud:"
                    case (0, 0): emoji_text = ":cloud:"
            list_overcast.append(emoji_text)

        reply += (datetime.now() + timedelta(days = day)).strftime('%d.%m.%Y') + "\n"
        for i in range(len(list_time)):
            if (i != 2 and i != 4 and i < 6): continue
            reply += (f"{emoji.emojize(list_overcast[i])} {list_time[i].rjust(5)}; "
                      f"{emoji.emojize(":thermometer:")}{list_temp[i].rjust(3)}; "
                      f"{emoji.emojize(":tornado:")}{list_wind[i].rjust(2)} м\с; "
                      f"{emoji.emojize(":droplet:")}{list_rain[i].rjust(2)} мм\n")
        reply += "```\n"

    return reply
