import asyncio
import datetime
import traceback
from storage_module import storage
import commands_module

class Alarm:

    def __init__(self):
        self.alarms_daily = []
        self.alarms_periodical = []

    async def WorkCycle(self):
        while True:
            try:
                current_datetime = datetime.datetime.now()
                current_time = datetime.time(current_datetime.hour, current_datetime.minute)
                current_date = current_datetime.date()
                        
                for alarm in self.alarms_daily:
                    if alarm[0] == current_time and alarm[1] != current_date:
                        alarm[1] = current_date
                        await alarm[2](commands_module.home_chat_message, *alarm[3])

                for alarm in self.alarms_periodical:
                    time_since_last_trigger = (current_datetime - alarm[0]).total_seconds() // 60
                    if time_since_last_trigger >= alarm[1]:
                        alarm[0] = current_datetime
                        await alarm[2](commands_module.home_chat_message, *alarm[3])

            except Exception as e:
                print(traceback.format_exc())
                await commands_module.send_to_home_chat(f"Alarm error: {e}")

            finally:
                await asyncio.sleep(30)

    def add_daily_alarm(self, time : datetime.time, action, args : list = []):
        last_date_triggered = datetime.datetime.now().date
        time = datetime.time(time.hour, time.minute)
        self.alarms_daily.append([time, last_date_triggered, action, args])

    def add_periodical_alarm(self, period_in_minutes: datetime.time, action, args : list = []):
        last_time_triggered = datetime.datetime.now()
        period_in_minutes = period_in_minutes.hour * 60 + period_in_minutes.minute
        self.alarms_periodical.append([last_time_triggered, period_in_minutes, action, args])
        

alarm = Alarm()