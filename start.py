import bot


def load_no_file():
    print("FAILED TO FIND OR LOAD SAFE FILE")

    try:
        with open("savedata/user_data.json", "r", encoding="utf-8") as _: pass
        with open("savedata/group_save.json", "r", encoding="utf-8") as _: pass

        if input("Use load without save file? (Using only json *some data might be lost*) y/n --> ") in ["Y", "y"]:
            bot.DB.load({"_known_users": {}})
    except FileNotFoundError:
        pass

if input("Use saved data? y/n --> ") in ["Y", "y"]:
    try:
        with open("savedata/save-file", "rb") as f:
            load_file: dict = bot.pickle.load(f)

        bot.DB.load(load_file)
    except FileNotFoundError:
        load_no_file()
    except AttributeError:
        load_no_file()

bot.executor.start_polling(bot.dp, skip_updates=True, on_shutdown=bot.custom_shutdown, on_startup=bot.custom_startup)