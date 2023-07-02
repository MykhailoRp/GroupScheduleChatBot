import json
import os

while True:
    try:

        bot_token = input("Bot token: ")
        chat_ids = input("Chat ids (format: 'chat_id, chat_id, chat_id, ...'): ").split(", ")
        alt_groups = input("Alternative group names (format: 'group_1, group_2, group_3, ...'): ").split(", ")
        this_group = input("This group name: ")
        bot_name = input("Bot name: ")

        if len(chat_ids) == 0 or len(alt_groups) == 0:
            raise IndexError

        with open("configuration.json", "w", encoding="utf-8") as out_file:
            json.dump({

                "alt_groups": alt_groups,
                "this_group": this_group,

                "bot_token": bot_token,
                "bot_name": bot_name,

                "queue_notify_chats": chat_ids,

            }, out_file, indent=4, ensure_ascii=False)

    except FileNotFoundError:
        print("!FAILED TO FIND FILE!")
    except IndexError:
        print("!WRONG FORMAT!")
    finally:
        print("Created group.json file")
        break

try:
   os.makedirs("class_dir/loaddata")
except FileExistsError:
   pass

try:
   os.makedirs("savedata")
except FileExistsError:
   pass

while True:
    try:

        group_file = input("File with name info of all students (format: 'name info' per line): ")

        with open(group_file, "r", encoding="utf-8") as in_file:
            lines = [a.replace("\n", "") for a in in_file.readlines()]
            with open("class_dir/loaddata/group.json", "w", encoding="utf-8") as out_file:
                json.dump({a:False for a in lines}, out_file, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        print("!FAILED TO FIND FILE!")
        continue
    except IndexError:
        print("!WRONG FORMAT!")
        continue
    finally:
        print("Created group.json file")
        break

while True:
    try:

        schedule_f = input("File with schedule (format: 'week_num|day_num|time_start|time_end|name|teacher|link|queue(0/1)' per line): ")

        with open(schedule_f, "r", encoding="utf-8") as in_file:
            lines = [a.replace("\n", "").split("|") for a in in_file.readlines()]

            end_dict = {}

            for a in lines:
                end_dict[a[0]] = end_dict.get(a[0], {}) | {a[1]: end_dict.get(a[0], {}).get(a[1], {}) | {a[2]: {"end": a[3], "name": a[4], "teacher": a[5], "link": a[6], "queue": bool(a[7])}}}

            with open("class_dir/loaddata/rozklad.json", "w", encoding="utf-8") as out_file:
                json.dump(end_dict, out_file, indent=4, ensure_ascii=False)

    except FileNotFoundError:
        print("!FAILED TO FIND FILE!")
        continue
    except IndexError:
        print("!WRONG FORMAT!")
        continue
    finally:
        print("Created rozklad.json file")
        break

if input("Start bot? y/n --> ") in ["Y", "y"]: import start