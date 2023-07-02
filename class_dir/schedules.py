#schedule
import asyncio
from datetime import datetime as _datetime, timedelta as _timedelta

def get_week_num():
    return (_datetime.now().date() - _datetime(2023, 2, 6).date()).days // 7 % 2

class study_hour:
    def __init__(self, subject, time_start: _datetime, time_end: _datetime, teacher, link, queue, week_index, day_index):
        self._subject = subject
        self._time_start : _datetime = time_start
        self._time_end : _datetime = time_end
        self._teacher = teacher
        self._link = link
        self._queue = queue

        self._week_index = week_index
        self._day_index = day_index

    def now_active(self):
        temp = self.till_start_end()
        return temp[0] < 0 < temp[1]

    def is_today(self):
        return _datetime.now().weekday() == self._day_index and get_week_num() == self._week_index

    def till_start_end(self):
        start = self._time_start
        end = self._time_end
        now = _datetime.now()
        return _timedelta(hours=start.hour - now.hour, minutes=start.minute - now.minute).total_seconds(), _timedelta(hours=end.hour - now.hour, minutes=end.minute - now.minute).total_seconds()

    def dict(self):
        return {
            "subject": self._subject,
            "time_start": self._time_start.strftime("%H:%M"),
            "time_end": self._time_end.strftime("%H:%M"),
            "teacher": self._teacher,
            "link": self._link,
            "queue": self._queue
        }

    def __str__(self):
        return f"{self._subject} ({self._time_start.strftime('%H:%M')} - {self._time_end.strftime('%H:%M')})\n{self._link}\n{self._teacher}"

    def __repr__(self):
        return f"{self._subject} ({self._time_start.strftime('%H:%M')} - {self._time_end.strftime('%H:%M')}) t:{self._teacher} l:{self._link} q:{self._queue}"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self._subject == other._subject and self._teacher == other._teacher and self._time_start == other._time_start and self._time_end == other._time_end
    def __lt__(self, other):
        try:
            return self._time_start < other.time_start
        except AttributeError:
            return False
    def __gt__(self, other):
        try:
            return self._time_start > other.time_start
        except AttributeError:
            return False

    @property
    def subject(self): return self._subject
    @property
    def time_start(self): return self._time_start
    @property
    def time_end(self): return self._time_end
    @property
    def teacher(self): return self._teacher
    @property
    def link(self): return self._link
    @property
    def queue(self): return self._queue
    @property
    def week_index(self): return self._week_index
    @property
    def day_index(self): return self._day_index

class dodka_hour(study_hour):
    def __init__(self, subject, time_start: _datetime, time_end: _datetime, teacher, link, queue, week_index, day_index):
        super().__init__(subject, time_start, time_end, teacher, link, queue, week_index, day_index)

        now = _datetime.now()
        adj = now + _timedelta(days=(7 * abs(week_index - get_week_num())) + (day_index - now.weekday()))
        self._expiration_date = _datetime.fromtimestamp(round(adj.timestamp() + (time_end.minute - adj.minute) * 60 + (time_end.hour - adj.hour) * 60 * 60 - adj.second))

    def dict(self):
        return {
            "subject": self._subject,
            "time_start": self._time_start.strftime("%H:%M"),
            "time_end": self._time_end.strftime("%H:%M"),
            "teacher": self._teacher,
            "link": self._link,
            "queue": self._queue,
            "week_num": self._week_index + 1,
            "day_num": self._day_index + 1,
        }

    def __bool__(self):
        return self._expiration_date > _datetime.now()

    def __str__(self):
        return f"(dod) {self._subject} ({self._time_start.strftime('%H:%M')} - {self._time_end.strftime('%H:%M')})\n{self._link}\n{self._teacher}"

    def __repr__(self):
        return f"(dod) {self._subject} ({self._time_start.strftime('%H:%M')} - {self._time_end.strftime('%H:%M')}) t:{self._teacher} l:{self._link} q:{self._queue}"

    @property
    def expiration_date(self): return self._expiration_date

class study_day:
    def __init__(self, day_dict, name, day_index, week_index):
        self._hours: [study_hour] = [study_hour(day_dict[a]["name"], _datetime.strptime(a, "%H:%M"), _datetime.strptime(day_dict[a]["end"], "%H:%M"), day_dict[a]["teacher"], day_dict[a]["link"], day_dict[a]["queue"], day_index, week_index) for a in day_dict]
        self._name = name
        self._day_index = day_index
        self._week_index = week_index

    def now_active(self):
        for hour in self._hours:
            if hour.now_active(): return hour

        return None

    def next_active(self):
        for i, hour in enumerate(self._hours):
            if hour.till_start_end()[0] >= 0:
                return hour

            if isinstance(hour, dodka_hour):
                if not hour:
                    self._hours.pop(i)

        return None

    def add_dodka(self, subject, time_start, time_end, teacher, link, queue, week_num, day_num):
        return self._hours[self.put_sorted(dodka_hour(subject, time_start, time_end, teacher, link, queue, week_num, day_num))]

    def find(self, hour_to_find: dodka_hour | study_hour):
        for i, h in enumerate(self._hours):
            if h == hour_to_find: return i

        return -1

    def put_sorted(self, element):
        for i, e in enumerate(self._hours):
            if element < e:
                self._hours.insert(i, element)
                return i
        else:
            self._hours.append(element)
            return len(self._hours) - 1

        return -1

    def dict(self):
        return {
            a:b.dict() for a, b in enumerate(self._hours)
        }

    def __bool__(self):
        return len(self._hours) > 0

    def __getitem__(self, item):
        return self._hours[item]

    def __setitem__(self, key, value):
        self._hours[key] = value

    def __str__(self):
        return f"{self._name}\n" + "\n".join([" - " + a.__repr__() for a in self._hours])
    def __repr__(self):
        return f"{self._name}: " + ", ".join([a.__repr__() for a in self._hours])

    @property
    def hours(self):
        return self._hours

    @property
    def name(self):
        return self._name

    @property
    def day_index(self):
        return self._day_index

    @property
    def week_index(self):
        return self._week_index


week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

class study_week:
    def __init__(self, week_dict, week_index):
        self._days = [study_day(week_dict[a], week[int(a)], int(a), week_index) for a in week_dict]
        self._week_index = week_index

    def now_active(self):
        return self._days[_datetime.now().weekday()]

    def next_active(self):
        if _datetime.now().weekday()+1 >= len(self._days): return None

        return self._days[_datetime.now().weekday() + 1]

    def add_dodka(self, subject, time_start, time_end, teacher, link, queue, week_num, day_num):
        return self._days[day_num].add_dodka(subject, time_start, time_end, teacher, link, queue, week_num, day_num)

    def dict(self):
        return {
            a:b.dict() for a,b in enumerate(self._days)
        }

    def __getitem__(self, item):
        return self._days[item]

    def __str__(self):
        return f"{self._week_index}\n" + "\n".join([str(a) for a in self._days])

    def __repr__(self):
        return f"{self._week_index}: " + " | ".join([a.__repr__() for a in self._days])

    @property
    def days(self):
        return self._days

    @property
    def week_index(self):
        return self._week_index


class SCHEDULE:
    def __init__(self, schedule_dict):
        self._schedule = [study_week(schedule_dict[a], int(a)) for a in schedule_dict]

    def now_active(self):
        return self._schedule[get_week_num()]

    def next_active(self):
        return self._schedule[get_week_num() % len(self._schedule)]

    def add_dodka(self, subject, time_start, time_end, teacher, link, queue, week_num, day_num):
        return self._schedule[week_num].add_dodka(subject, time_start, time_end, teacher, link, queue, week_num, day_num)

    def del_dodka(self, week_index, day_index, hour_index):
        return self._schedule[week_index].days[day_index].hours.pop(hour_index)

    def dict(self):
        return {
            a:b.dict() for a, b in enumerate(self._schedule)
        }

    def __getitem__(self, item):
        return self._schedule[item]

    def __str__(self):
        return f"Schedule\n" + "\n".join([str(a) for a in self._schedule])

    def __repr__(self):
        return f"Schedule: " + " | ".join([a.__repr__() for a in self._schedule])

    @property
    def schedule(self):
        return self._schedule



class SCHEDULE_MANAGER(SCHEDULE):
    def __init__(self, schedule_dict):
        super().__init__(schedule_dict)

        self._next_pair = None

        self._updated_day = False
        self._day_active = False
        self._waiting = False

    def get_pair(self, week_i, day_i, hour_i):
        return self._schedule[week_i].days[day_i].hours[hour_i]

    def add_dodka(self, subject, time_start, time_end, teacher, link, queue, week_num, day_num):
        dodka_temp = super(SCHEDULE_MANAGER, self).add_dodka(subject, time_start, time_end, teacher, link, queue, week_num, day_num)

        if dodka_temp.is_today():
            if not self._day_active:
                self._updated_day = True

        return dodka_temp

    def del_dodka(self, week_index, day_index, hour_index):

        dodka_temp: dodka_hour = self._schedule[week_index].days[day_index].hours[hour_index]

        if not isinstance(dodka_temp, dodka_hour):
            raise HourNotDodka()

        if dodka_temp.now_active() or self._next_pair == dodka_temp:
            raise CantDeleteActive()

        return super(SCHEDULE_MANAGER, self).del_dodka(week_index, day_index, hour_index)

    async def wait_for_time(self, s):
        self._waiting = True
        await asyncio.sleep(s)
        self._waiting = False


    async def manage(
            self,
            logger_,

            NextNotifFunc,
            NotifAboutCurrentPairFunc,
            NotifAboutCurrentPairEndFunc,

            QueueCollectStartFunc,
            QueueStartFunc,

            clear_dynamic_messages,

            notice_before_pair = 60,
    ):

        test_now = self.now_active().now_active().now_active()
        if test_now is not None:
            if test_now.queue:
                await QueueCollectStartFunc()
                await QueueStartFunc()

        while True:
            logger_.info(f"New day, soon pair notice")

            this_week = self.now_active()
            this_day = this_week.now_active()

            del this_week

            async def day_func(_this_day):
                self._day_active = True

                self._next_pair = _this_day.next_active()

                while self._next_pair is not None:
                    temp = self._next_pair.till_start_end()[0] - notice_before_pair
                    logger_.info(f"Waiting {temp} to notify for next pair soon ({notice_before_pair} sec)")

                    await asyncio.sleep(temp)

                    await NextNotifFunc(self._next_pair)

                    if self._next_pair._queue:
                        await QueueCollectStartFunc()

                    temp = self._next_pair.till_start_end()[0]
                    logger_.info(f"Waiting {temp} to notify for next pair soon (0 sec)")

                    await asyncio.sleep(temp)

                    await NotifAboutCurrentPairFunc(self._next_pair)

                    if self._next_pair._queue:
                        await QueueStartFunc()

                    temp = self._next_pair.till_start_end()[1]
                    logger_.info(f"Waiting {temp} for the end of pair")

                    await asyncio.sleep(temp)

                    await clear_dynamic_messages()

                    self._next_pair = _this_day.next_active()

                    await NotifAboutCurrentPairEndFunc(self._next_pair)

                self._day_active = False

                time_now = _datetime.now()
                temp = _timedelta(hours=23 - time_now.hour, minutes=60 - time_now.minute).total_seconds() + 100
                logger_.info(f"Day ended, waiting {temp} to notify for new day")

                self._waiting = True
                waiting_task = asyncio.create_task(self.wait_for_time(temp))

                while self._waiting:
                    if self._updated_day:
                        self._updated_day = False
                        self._next_pair = _this_day.next_active()
                        if self._next_pair is not None:
                            waiting_task.cancel()
                            return await day_func(_this_day)

                    await asyncio.sleep(1)

            await day_func(this_day)




class DodkaExceptions(Exception): pass

class HourNotDodka(DodkaExceptions):
    def __init__(self):
        super().__init__("Tried to delete regular pair")

class CantDeleteActive(DodkaExceptions):
    def __init__(self):
        super().__init__("Can`t delete active or next pairs")