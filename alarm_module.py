import asyncio
import datetime
import traceback
import re
from typing import Callable
from bot_module import bot

class Alarm:

    class Alarm_Config:
        type_letter : str
        trigger_time : datetime.time
        command_name : str
        command_function : Callable
        args : list
        last_time_triggered : datetime.datetime

        def __init__(self, type_letter : str, trigger_time : datetime.time, command_name : str, command_function : Callable, args : list, last_time_triggered : datetime.datetime):
            self.type_letter= type_letter
            if self.type_letter != "d" and self.type_letter != "p":
                raise Exception(f"Unknown type letter for alarm: {self.type_letter}")
            self.trigger_time = trigger_time
            self.command_name = command_name
            self.command_function = command_function
            self.args = args
            self.last_time_triggered = last_time_triggered

        def ready_to_trigger(self, time_now: datetime.datetime) -> bool:
            if self.type_letter == "d" and (time_now.time().replace(second = 0, microsecond = 0) != self.trigger_time or time_now.date() == self.last_time_triggered.date()):
                return False
            elif self.type_letter == "p" and (time_now - self.last_time_triggered).total_seconds() // 60 < self.trigger_time.hour * 60 + self.trigger_time.minute:
                return False
            return True

        async def trigger(self):
            self.last_time_triggered = datetime.datetime.now()
            await self.command_function(*self.args)

    alarms_list : list[Alarm_Config]

    def __init__(self):
        self.alarms_list = []

    async def WorkCycle(self):
        while True:
            try:
                current_datetime = datetime.datetime.now()

                for alarm in self.alarms_list:
                    if alarm.ready_to_trigger(current_datetime):
                        await alarm.trigger()

            except Exception as e:
                e.add_note("Alarm error.")
                print(traceback.format_exc())

            finally:
                await asyncio.sleep(30)

    re_time = re.compile(r"^(d|p)(\d{1,2}):(\d\d)$")
    def add_alarm(self, type_and_time : str, command_name : str, command_function : Callable, args : list = []):
        re_match = self.re_time.fullmatch(type_and_time)
        if not re_match:
            raise Exception("Alarm adding error. Incorrect alarm format.")

        time = datetime.time(int(re_match.group(2)), int(re_match.group(3)))
        last_time_trigerred = datetime.datetime.now()
        if (re_match.group(1) == "d"):
            last_time_trigerred -= datetime.timedelta(days = 1)

        self.alarms_list.append(self.Alarm_Config(re_match.group(1), time, command_name, command_function, args, last_time_trigerred))

    def remove_alarm(self, type_and_time : str, command_name : str, args : list = []):
        re_match = self.re_time.fullmatch(type_and_time)
        time = datetime.time(int(re_match.group(2)), int(re_match.group(3)))
        for alarm in self.alarms_list:
            if alarm.type_letter == re_match.group(1) and alarm.trigger_time == time and alarm.command_name == command_name and alarm.args == args:
                self.alarms_list.remove(alarm)
                return
        raise Exception("Not found alarm to remove.")

    def load_alarms(self, alarms : list[tuple[str, str, list]]):
        for type_and_time, command_name, args in alarms:
            alarm.add_alarm(type_and_time, command_name, bot.command_functions_list[command_name], args)

    async def test_first_daily_alarm(self):
        alarm = self.alarms_list[0]
        await alarm.trigger()
        
alarm = Alarm()