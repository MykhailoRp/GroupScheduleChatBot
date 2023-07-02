import pickle
import json
import os

import utils

import class_dir.queues as _queues
import class_dir.schedules as _schedules
import class_dir.user_classes as _user_classes

class DATA_BASE:
    def __init__(self):
        self._queue = _queues.QUEUE(3)
        self._known_users = {}

        with open(r"class_dir/loaddata/rozklad.json", "r", encoding="utf-8") as s:
            self._schedule = _schedules.SCHEDULE_MANAGER(json.loads(s.read()))

        with open("class_dir/loaddata/group.json", "r", encoding="utf-8") as s:
            self._group = json.loads(s.read())

    def load(self, load_file):
        def key_inter(key: str):
            if key.isdigit(): return int(key)
            return key

        def gooverer(a):
            if isinstance(a, dict): return {key_inter(key): gooverer(a[key]) for key in a}
            if isinstance(a, list): return [gooverer(b) for b in a]
            return a

        if "_known_users" in load_file:
            with open("savedata/user_data.json", "r", encoding="utf-8") as s:
                json_user_data = json.loads(s.read())
                json_user_data = gooverer(json_user_data)

                for j_u_id in json_user_data:
                    if j_u_id in load_file["_known_users"]:
                        u: _user_classes.TELEG_USER = load_file["_known_users"][j_u_id]

                        u.set_from_dict(json_user_data[j_u_id])
                    else:
                        load_file["_known_users"][j_u_id] = _user_classes.TELEG_USER(**json_user_data[j_u_id])

        with open("savedata/group_save.json", "r", encoding="utf-8") as s:
            group = json.loads(s.read())

            load_file["_group"] = gooverer(group)

        try:
            temp_group = load_file.pop("_group")
        except KeyError:
            temp_group = {}

        self.__dict__ = self.__dict__ | load_file

        self._group = self.__dict__.get("_group", {}) | temp_group

    def save(self):
        with open("savedata/save-file", "wb") as f:
            print(self.__dict__)
            temp_dict = self.__dict__.copy()
            temp_dict.pop("_queue")
            pickle.dump(temp_dict, f)

        with open("savedata/group_save.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self._group, indent=4, ensure_ascii=False))

        with open("savedata/user_data.json", "w", encoding="utf-8") as f:
            m_dump_dict = {}
            for user_id in self._known_users:
                t_user: _user_classes.TELEG_USER = self._known_users[user_id]
                m_dump_dict[user_id] = t_user.dict()

            f.write(json.dumps(utils.vals(m_dump_dict), indent=4, ensure_ascii=False))


    @property
    def queue(self): return self._queue
    @property
    def known_users(self): return self._known_users
    @property
    def schedule(self): return self._schedule
    @property
    def group(self): return self._group