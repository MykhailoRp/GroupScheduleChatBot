class answer_function:
    __slots__ = ["_func", "_kwargs"]

    def __init__(self, func, **kwargs):
        self._func:callable = func
        self._kwargs = kwargs

    def exe(self, **kwargs):
        return self._func(**kwargs, **self._kwargs)

    def __str__(self):
        return f"{self._func.__name__}({str(self._kwargs)})"

class pers_data:
    __slots__ = ["_last_name", "_first_name", "_fathers_name", "_group"]

    def __init__(self, prizvishche = None, imya = None, po_batkovy = None, group = None):
        self._last_name = prizvishche
        self._first_name = imya
        self._fathers_name = po_batkovy
        self._group = group

    def __str__(self):
        return f"{self._group} {self._last_name} {self._first_name} {self._fathers_name}"
    def __repr__(self):
        return f"{self._group} {self._last_name} {self._first_name} {self._fathers_name}"

    def __dict__(self):
        return self.dict()

    def dict(self):
        return {"group":self._group, "prizvishche":self._last_name, "imya":self._first_name, "po_batkovy":self._fathers_name, }

    def filled(self):
        if self._last_name is not None:
            return True
        else:
            return False

    @property
    def last_name(self): return self._last_name
    @property
    def first_name(self): return self._first_name
    @property
    def fathers_name(self): return self._fathers_name
    @property
    def group(self): return self._group


    @last_name.setter
    def last_name(self, value): self._last_name = value
    @first_name.setter
    def first_name(self, value): self._first_name = value
    @fathers_name.setter
    def fathers_name(self, value): self._fathers_name = value
    @group.setter
    def group(self, value): self._group = value

class notification_settings:
    __slots__ = ["_notif_pairs", "_queue_movement"]
    def __init__(self, notif_pairs = True, queue_movement = True, **kwargs):
        self._notif_pairs = notif_pairs
        # self.notif_morning = notif_morning
        self._queue_movement = queue_movement

    @property
    def notif_pairs(self): return self._notif_pairs
    @property
    def queue_movement(self): return self._queue_movement

    def set_setting(self, setting):
        setattr(self, "_" + setting, bool(1 - int(getattr(self, "_" + setting))))
        return getattr(self, "_" + setting)

    def options(self):
        return [[a[1:], getattr(self, a)] for a in self.__slots__]

    def dict(self):
        return {a: b for a, b in self.options()}

    def __dict__(self):
        return self.dict()

    def __repr__(self):
        return {a: getattr(self, a) for a in self.__slots__}.__repr__()

    def __str__(self):
        return "\n".join([f"{a[1:]}: {getattr(self, a)}" for a in self.__slots__])

class TELEG_USER:
    __slots__ = ['_perc_data', '_user_id', '_first_name', '_access_lvl', '_user_name', '_last_name', '_language_code', '_answer_function', '_notif_settings']

    def __init__(self, user_id: int, first_name: str, access_lvl: int = 0, user_name: str = None, last_name: str = None, language_code: str =  "en", prizvishche = None, imya = None, po_batkovy = None, group = None, personal_data: dict = None, notif_settings: dict = None):
        self._user_id: int = user_id
        self._first_name: str = first_name
        self._access_lvl: int = access_lvl
        self._user_name: str = user_name
        self._last_name: str = last_name
        self._language_code: str = language_code

        if personal_data is None:
            self._perc_data = pers_data(prizvishche, imya, po_batkovy, group)
        else:
            self._perc_data = pers_data(**personal_data)

        self._answer_function: answer_function | None = None

        if notif_settings is None:
            self._notif_settings = notification_settings()
        else:
            self._notif_settings = notification_settings(**notif_settings)

    def answer(self, **kwargs):
        temp_func = self._answer_function
        self._answer_function = None
        return temp_func.exe(**kwargs)

    def dict(self):
        return {
            "user_id": self._user_id,
            "first_name": self._first_name,
            "access_lvl": self._access_lvl,
            "user_name": self._user_name,
            "last_name": self._last_name,
            "language_code": self._language_code,

            "personal_data": self._perc_data.dict(),

            "notif_settings": self._notif_settings.dict(),
        }

    def set_from_dict(self, d:dict):
        self._user_id: int = d.get("user_id", self._user_id)
        self._first_name: str = d.get("first_name", self._first_name)
        self._access_lvl: int = d.get("access_lvl", self._access_lvl)
        self._user_name: str = d.get("user_name", self._user_name)
        self._last_name: str = d.get("last_name", self._last_name)
        self._language_code: str = d.get("language_code", self._language_code)

        if "personal_data" in d:
            self._perc_data = pers_data(**d["personal_data"])

        if "notif_settings" in d:
            self._notif_settings = notification_settings(**d["notif_settings"])

        return self

    def __dict__(self):
        return self.dict()

    def __str__(self):
        return f"{self._user_id};{self._first_name}"
    def __repr__(self):
        return f"{self._user_id};{self._first_name}"

    def __eq__(self, other):
        if isinstance(other, int):
            return self._user_id == other

        if not isinstance(other, TELEG_USER):
            return NotImplemented

        return self._user_id == other._user_id

    @property
    def user_id(self): return self._user_id
    @property
    def first_name(self): return self._first_name
    @property
    def access_lvl(self): return self._access_lvl
    @property
    def user_name(self): return self._user_name
    @property
    def last_name(self): return self._last_name
    @property
    def language_code(self): return self._language_code
    @property
    def perc_data(self): return self._perc_data
    @property
    def answer_function(self): return self._answer_function
    @property
    def notif_settings(self): return self._notif_settings


    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, str): raise WrongValueType(self._user_id, value)

        self._user_id = value
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str): raise WrongValueType(self._first_name, value)

        self._first_name = value
    @access_lvl.setter
    def access_lvl(self, value):
        if not isinstance(value, int): raise WrongValueType(self._access_lvl, value)

        self._access_lvl = value
    @user_name.setter
    def user_name(self, value):
        if not isinstance(value, str): raise WrongValueType(self._user_name, value)

        self._user_name = value
    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str): raise WrongValueType(self._last_name, value)

        self._last_name = value
    @language_code.setter
    def language_code(self, value):
        if not isinstance(value, str): raise WrongValueType(self._language_code, value)

        self._language_code = value
    @perc_data.setter
    def perc_data(self, value):
        if not isinstance(value, pers_data): raise WrongValueType(self._perc_data, value)

        self._perc_data = value
    @answer_function.setter
    def answer_function(self, value):
        if not (isinstance(value, answer_function) or value is None):
            raise WrongValueType(answer_function, value)

        self._answer_function = value
    @notif_settings.setter
    def notif_settings(self, value):
        if not isinstance(value, notification_settings): raise WrongValueType(self._notif_settings, value)

        self._notif_settings = value


class WrongValueType(ValueError):
    def __init__(self, expected, given):
        super(WrongValueType, self).__init__(f"{type(expected)} expected, but {type(given)} was given")