import json as _json

config_file = open("configuration.json", "r")
config_json = _json.load(config_file)
config_file.close()

bot_token = config_json["bot_token"]
bot_name = config_json["bot_name"]

this_group = config_json["this_group"]

alt_groups = config_json["alt_groups"]

notice_before_pair =  10 * 60
morning_schedule_notice = 40

class ACCESS_LEVELS:
    BANNED = -1
    UNVERIFIED = 0
    OTHER_STUDENT = 1
    GROUP_STUDENT = 2
    ADMIN = 3

    DEFAULT = 0


queue_order = {
    ACCESS_LEVELS.GROUP_STUDENT: 1,  #also 0 for priority
    ACCESS_LEVELS.ADMIN: 1,  #also 0 for priority
    ACCESS_LEVELS.OTHER_STUDENT: 2,
}

queue_depth_notif = 3

queue_one_pos = True

queue_notify_chats = config_json['queue_notify_chats']