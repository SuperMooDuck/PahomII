# -*- coding: ansi -*-
import aiohttp
import asyncio
import re
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup


async def GetWeatherGismeteo(city:str = "bir", days:int = 1) -> str:
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

        list_time = []
        for div in base_div.find("div", {"class" : "widget-row widget-row-datetime-time"}).find_all("span"):
            list_time.append(div.string)
        list_temp = []
        for div in base_div.find("div", {"class" : "widget-row-chart widget-row-chart-temperature-air row-with-caption"}).find_all("temperature-value", value=True):
            list_temp.append(div["value"])
        list_overcast = []
        for div in base_div.find("div", {"class" : "widget-row widget-row-icon"}).find_all("div", {"class" : "row-item"}):
            list_overcast.append(div["data-tooltip"])
        list_wind = []
        for div in base_div.find("div", {"class" : "widget-row widget-row-wind row-wind-gust row-with-caption"}).find_all("speed-value", value=True):
            list_wind.append(div["value"])
        list_rain = []
        for div in base_div.find("div", {"class" : "widget-row widget-row-precipitation-bars row-with-caption"}).find_all("div", {"class" : re.compile("item-unit.*")}):
            list_rain.append(div.string)

        reply += (datetime.now() + timedelta(days = day)).strftime('%d.%m.%Y') + "\n"
        for i in range(len(list_time)):
            if (i != 2 and i != 4 and i < 6): continue
            reply += f" {list_time[i]}; {list_temp[i]}; {list_overcast[i]}; ветер {list_wind[i]} м\с; осадки {list_rain[i]} мм\n"
        reply += "\n"

    return reply
