import class_dir.user_classes as _user_classes
from aiogram import types as _types

class QUEUE:
    def __init__(self, priority_lvls = 2):
        self._queue = []
        [self._queue.append([].copy()) for _ in range(priority_lvls)]

        self._current: _user_classes.TELEG_USER | None = None
        self._started = False

        self._i = 0

        self._update_msgs: [_types.Message] = []

    def start(self):
        self._started = True
        return self.next()

    def __bool__(self): return self._started

    def current(self) -> _user_classes.TELEG_USER | None: return self._current

    def get_update_msg(self) -> list: return self._update_msgs

    def next(self):
        if not self._started:
            raise QueueIsNotStarted()

        for i, a in enumerate(self._queue):
            if len(a) > 0:
                self._current = a.pop(0)
                break
        else: self._current = None

        return self._current

    def add(self, priority, user):
        self._queue[priority].append(user)

        pos = 0

        i = 0

        while i <= priority:
            pos += len(self._queue[i])
            i += 1

        return pos - 1

    def remove(self, item: _user_classes.TELEG_USER):
        for i, a in enumerate(self._queue):

            for j, b in enumerate(a):
                if b == item:
                    a.pop(j)
                    return j

        return None

    def clear(self):
        [self._queue[i].clear() for i in range(len(self._queue))]
        self._current = None
        self._started = False
        self._update_msgs.clear()
        return True

    def index(self, item):
        for i, a in enumerate(self):
            if a == item: return i

        else: return None

    def _list(self) -> list:
        res_list = []

        for a in self._queue:
            res_list.extend(a)

        return res_list

    def __getitem__(self, item) -> _user_classes.TELEG_USER:
        return self._list()[item]

    def __len__(self):
        return len(self._list())

    def __iter__(self):
        return self

    def __next__(self):
        if self._i >= len(self):
            self._i = 0
            raise StopIteration

        self._i += 1

        return self[self._i-1]

    def __contains__(self, item):

        if item == self._current: return True

        for a in self._list():
            if a == item: return True
        return False


        # return item in self._list() or (item == self.current)

    def __str__(self):
        order = {i:a for i, a in enumerate(self._queue)}
        return f"QUEUE {len(self)} {order}"
    def __repr__(self):
        order = {i: a for i, a in enumerate(self._queue)}
        return f"QUEUE {len(self)} {order}"

    def prettify(self, queue_labels: list):
        s = f'<b>Черга для наступної пари</b>\n\n<b>Зараз відповідає:\n'

        if self._current is None: s += "ніхто (хто ж це???)"
        else: s += f'<a href="tg://user?id={self._current.user_id}">{self._current.perc_data}</a>'

        s += '</b>\n\n<i>Далі:</i>\n\n'

        for i, a in enumerate(self._queue):
            if len(a) == 0:
                continue

            s += str(queue_labels[i]) + "\n"

            for j, u in enumerate(a):
                s += f'{j+1}. <a href="tg://user?id={u.user_id}">{u.perc_data.__str__()}</a>\n'

            if i < len(self)-1: s += "\n\n"

        return s



class QueueExceptions(Exception): pass

class QueueIsNotStarted(QueueExceptions):
    def __init__(self):
        super().__init__("Queue is not started")