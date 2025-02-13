import asyncio
import datetime
import traceback
import re

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
                    if alarm[1] == current_time and alarm[0] != current_date:
                        alarm[0] = current_date
                        await alarm[2](*alarm[3])

                for alarm in self.alarms_periodical:
                    time_since_last_trigger = (current_datetime - alarm[0]).total_seconds() // 60
                    if time_since_last_trigger >= alarm[1]:
                        alarm[0] = current_datetime
                        await alarm[2](*alarm[3])

            except Exception as e:
                e.add_note("Alarm error.")
                print(traceback.format_exc())

            finally:
                await asyncio.sleep(30)

    def load_alarms(self, storage):
        for a in storage:
            self.add_alarm(*a)

    re_time = re.compile(r"^(d|p)(\d{1,2}):(\d\d)$")
    def add_alarm(self, type_and_time : str, command, args : list = []):
        re_match = self.re_time.fullmatch(type_and_time)
        if not re_match:
            raise Exception("Alarm adding error. Incorrect time format.")

        time = datetime.time(int(re_match.group(2)), int(re_match.group(3)))

        if (re_match.group(1) == "d"):
            self.add_daily_alarm(time, command, args)
        else:
            self.add_periodical_alarm(time, command, args)

    def remove_alarm(self, type_and_time : str, command, args : list = []):
        re_match = self.re_time.fullmatch(type_and_time)
        time = datetime.time(int(re_match.group(2)), int(re_match.group(3)))
        if (re_match.group(1) == "d"):
            for a in self.alarms_daily:
                if a[1] == time and a[2] == command and a[3] == args:
                    self.alarms_daily.remove(a)
                    return
        else:
            for a in self.alarms_periodical:
                if a[1] == time and a[2] == command and a[3] == args:
                    self.alarms_periodical.remove(a)
                    return
        raise Exception("Not found alarm to remove.")

    def add_daily_alarm(self, time : datetime.time, action, args : list = []):
        last_date_triggered = datetime.datetime.now().date()
        time = datetime.time(time.hour, time.minute)
        self.alarms_daily.append([last_date_triggered, time, action, args])

    def add_periodical_alarm(self, period_in_minutes: datetime.time, action, args : list = []):
        last_time_triggered = datetime.datetime.now()
        period_in_minutes = period_in_minutes.hour * 60 + period_in_minutes.minute
        self.alarms_periodical.append([last_time_triggered, period_in_minutes, action, args])
        
alarm = Alarm()