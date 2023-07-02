import configurator as _cfg
from class_dir import data_base as _data_base, user_classes as _user_classes
from aiogram import types as _types

def get_user_profile_from_message(message: _types.Message, data_base: _data_base.DATA_BASE) -> _user_classes.TELEG_USER:

    if message.from_user.id in data_base.known_users:
        return data_base.known_users[message.from_user.id]

    #generate new user data
    data_base.known_users[message.from_user.id] = _user_classes.TELEG_USER(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        access_lvl=_cfg.ACCESS_LEVELS.DEFAULT,
        user_name=message.from_user.username,
        last_name=message.from_user.last_name,
        language_code=message.from_user.language_code
    )

    return data_base.known_users[message.from_user.id]