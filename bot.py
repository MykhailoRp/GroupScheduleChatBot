from datetime import datetime
import logging

import asyncio

import pickle

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import aiogram.utils.exceptions as AIO_Exceptions

import functions as funcs
from class_dir import data_base, schedules, string_time_class, user_classes
import configurator as conf
from lang import ua, emoji

logging.basicConfig(
    handlers=[logging.FileHandler('main_log.log', 'w', 'utf-8')],
    level = logging.INFO,
    format = u'%(asctime)s | %(levelname)-8s | %(name)-10s | %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
)

logger_ = logging.getLogger("logger")
logger_.setLevel(logging.INFO)
logger_handler = logging.StreamHandler()
logger_handler.setLevel(logging.INFO)
logger_formatter = logging.Formatter(u'| %(asctime)s | %(levelname)-8s | %(message)s', datefmt='%H:%M:%S')
logger_handler.setFormatter(logger_formatter)
logger_.addHandler(logger_handler)

bot = Bot(token=conf.bot_token, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)

DB = data_base.DATA_BASE()

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


#button shortcuts
def start_butts():
    butts = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=3,
        keyboard=[
            [types.KeyboardButton(ua.show_full_roz_for_today_but + " " + emoji.show_full_roz_for_today_but), types.KeyboardButton(ua.show_full_roz_for_tomorrow_but + " " + emoji.show_full_roz_for_tomorrow_but), types.KeyboardButton(ua.show_full_roz_but + " " + emoji.show_full_roz_but)],
            # [types.KeyboardButton(ua.moodle_but + " " + emoji.moodle_status)],
            [types.KeyboardButton(ua.settings_but + " " + emoji.settings)],
        ]
    )
    return butts

def cancel_but():
    butts = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=3,
        keyboard=[
            [types.KeyboardButton(ua.but_cancel + " " + emoji.cancel)]
        ]
    )
    return butts

def view_q_but(user_data: user_classes.TELEG_USER):
    butts = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(ua.queue_show_but, callback_data="/show_queue")],
            [queue_but_gen(user_data)]
        ]
    )
    return butts

def queue_but_gen(user_data):
    return types.InlineKeyboardButton(ua.queue_leave_but + " " + emoji.leave_queue, callback_data="/leave_queue") if user_data in DB.queue else types.InlineKeyboardButton(ua.queue_join_but + " " + emoji.join_queue, callback_data="/join_queue")
#end button shortcuts


#command function

async def me(message: types.Message, user_data: user_classes.TELEG_USER):
    return await bot.send_message(message.from_user.id, f"{user_data.perc_data.group}, {user_data.perc_data.first_name}, {user_data.perc_data.last_name}, {user_data.perc_data.fathers_name}, {user_data.first_name}", reply_markup=start_butts())

async def starter(message: types.Message, user_data: user_classes.TELEG_USER):

    if message.get_args() == "join_queue": return await queue_join(message, user_data)

    return await bot.send_message(message.from_user.id, ua.starter, reply_markup=start_butts())

async def admins_comms(message: types.Message, user_data: user_classes.TELEG_USER):
    return await bot.send_message(message.from_user.id, "\n".join(list(admin_comms.keys())))

async def cancel(message: types.Message, user_data: user_classes.TELEG_USER):
    user_data.answer_function = None

    return await bot.send_message(message.from_user.id, ua.canceled, reply_markup=start_butts())


#auth
async def auth_start(message: types.Message, user_data: user_classes.TELEG_USER):
    join_queue = message.get_args() == "join_queue"
    butts = types.InlineKeyboardMarkup(row_width=1,
        inline_keyboard=[
            [types.InlineKeyboardButton(text=ua.IP24_group_but, callback_data="/auth_main {}".format(join_queue))],
            [types.InlineKeyboardButton(text=ua.alt_group_but, callback_data="/auth_alt {}".format(join_queue))],
        ]
    )

    return await bot.send_message(message.from_user.id, ua.starter+"\n\n"+ua.authorize_start, reply_markup=butts)

async def auth_main(message: types.Message, user_data: user_classes.TELEG_USER, join_queue = False):
    if not join_queue: join_queue = message.get_args() == "True"
    butts = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=ua.alt_group_but, callback_data=f"/auth_alt {join_queue}")]
        ]
    )

    await bot.send_message(message.from_user.id, ua.authorize_IP24, reply_markup=butts)

    user_data.answer_function = user_classes.answer_function(auth_main_end, join_queue = join_queue)

async def auth_main_end(message: types.Message, user_data: user_classes.TELEG_USER, join_queue = False):
    PIB = message.text.split(" ", maxsplit=3)

    if len(PIB) < 3:
        if len(PIB) == 0:
            await bot.send_message(message.from_user.id, "EMPTY MESSAGE")
        if len(PIB) == 1:
            await bot.send_message(message.from_user.id, ua.alt_auth_no_IB)
        if len(PIB) == 2:
            await bot.send_message(message.from_user.id, ua.alt_auth_no_B)

        return await auth_main(message, user_data, join_queue)

    if not DB.group.get(" ".join(PIB), True):
        user_data.access_lvl = conf.ACCESS_LEVELS.GROUP_STUDENT

        user_data.perc_data.group = "ІП-24"

        user_data.perc_data.last_name = PIB[0]
        user_data.perc_data.first_name = PIB[1]
        user_data.perc_data.fathers_name = PIB[2]

        DB.group[" ".join(PIB)] = True

        await bot.send_message(message.from_user.id, ua.IP24_auth_ready.format(" ".join(PIB)), reply_markup=start_butts())

        if join_queue:
            await queue_join(message, user_data)

        return True
    else:
        await bot.send_message(message.from_user.id, ua.IP24_auth_failed.format(" ".join(PIB)), reply_markup=start_butts())
        await auth_main(message, user_data, join_queue)
        return

async def auth_alt_PIB(message: types.Message, user_data: user_classes.TELEG_USER, join_queue = False):
    if not join_queue: join_queue = message.get_args() == "True"
    butts = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=ua.IP24_group_but, callback_data=f"/auth_main {join_queue}")],
        ]
    )

    await bot.send_message(message.from_user.id, ua.alt_auth_PIB, reply_markup=butts)
    user_data.answer_function = user_classes.answer_function(auth_alt_catch_PIB, join_queue = join_queue)
    return

async def auth_alt_catch_PIB(message: types.Message, user_data: user_classes.TELEG_USER, join_queue = False):
    PIB = message.text.split(" ", maxsplit=3)

    if len(PIB) < 3:
        if len(PIB) == 0:
            await bot.send_message(message.from_user.id, "EMPTY MESSAGE")
        if len(PIB) == 1:
            await bot.send_message(message.from_user.id, ua.alt_auth_no_IB)
        if len(PIB) == 2:
            await bot.send_message(message.from_user.id, ua.alt_auth_no_B)

        return await auth_alt_PIB(message, user_data, join_queue)

    user_data.perc_data.last_name = PIB[0]
    user_data.perc_data.first_name = PIB[1]
    user_data.perc_data.fathers_name = PIB[2]

    return await auth_alt_GROUP(message, user_data, join_queue)

async def auth_alt_GROUP(message: types.Message, user_data: user_classes.TELEG_USER, join_queue = False):

    group_buts = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    [group_buts.add(a) for a in conf.alt_groups]

    await bot.send_message(message.from_user.id, ua.alt_auth_group, reply_markup=group_buts)
    user_data.answer_function = user_classes.answer_function(auth_alt_end, join_queue = join_queue)
    return

async def auth_alt_end(message: types.Message, user_data: user_classes.TELEG_USER, join_queue = False):
    user_data.perc_data.group = message.text
    user_data.access_lvl = conf.ACCESS_LEVELS.OTHER_STUDENT
    await bot.send_message(message.from_user.id, ua.alt_auth_ready.format(user_data.perc_data), reply_markup=start_butts())

    if join_queue: await queue_join(message, user_data)

    return True
#end auth

#settings

def generate_option_buttons_for_user(user_data: user_classes.TELEG_USER):
    buttons = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(ua.notif_options[opt] + f"   " + (emoji.option_on if val else emoji.option_off), callback_data=f"/set_setting {opt}")] for opt, val in user_data.notif_settings.options()
        ]
    )

    return buttons

async def notifications_menu(message: types.Message, user_data: user_classes.TELEG_USER):
    await bot.send_message(message.from_user.id, ua.options_menu, reply_markup=generate_option_buttons_for_user(user_data))

async def set_setting(message: types.Message, user_data: user_classes.TELEG_USER):
    setting = message.get_args()

    user_data.notif_settings.set_setting(setting)

    await message.edit_reply_markup(generate_option_buttons_for_user(user_data))
#end settings

#queues

async def get_message_join_q_buttons():
    buttons = types.InlineKeyboardMarkup(row_width=1,
        inline_keyboard=[
            [types.InlineKeyboardButton(ua.queue_fast_but, callback_data="/join_queue 0")],
            [types.InlineKeyboardButton(ua.queue_slow_but, callback_data="/join_queue 1")],
            [types.InlineKeyboardButton(ua.queue_invite_but, switch_inline_query=ua.queue_invite.format("https://t.me/{bot_name}?start=join_queue".format(bot_name=(await bot.get_me()).username)))],
        ]
    )

    return buttons

async def update_dynamic_msg():
    for message in DB.queue.get_update_msg():
        try:
            await message.edit_text(DB.queue.prettify(ua.queue_labels), reply_markup=await get_message_join_q_buttons())
        except AIO_Exceptions: pass

async def clear_dynamic_messages():
    for message in DB.queue.get_update_msg():
        try:
            await message.unpin()
        except AIO_Exceptions: pass


async def Notify_Queue_Change(change_pos_after: int = 0):
    await update_dynamic_msg()

    pos = change_pos_after

    async def func(user, place):
        if place == 0:
            await bot.send_message(user.user_id, ua.queue_you_are_next_no_skip)  # , reply_markup=im_now_buts)
        else:
            if user.notif_settings.queue_movement:
                await bot.send_message(user.user_id, ua.queue_you_are_now_num.format(place + 1))

    while pos < len(DB.queue) and pos <= conf.queue_depth_notif:
        asyncio.create_task(func(DB.queue[pos], pos))
        pos += 1


async def Queue_Collecting_Start(*args, **kwargs):
    DB.queue.clear()

    for chat_id in conf.queue_notify_chats:
        try:
            await bot.send_message(chat_id, ua.queue_collection_start)
            DB.queue.get_update_msg().append(await bot.send_message(chat_id, DB.queue.prettify(ua.queue_labels), reply_markup=await get_message_join_q_buttons()))
            try:
                await DB.queue.get_update_msg()[-1].pin(True)
            except AIO_Exceptions.BadRequest:
                await bot.send_message(chat_id, "SORRY I CANT PIN MESSAGES")
        except AIO_Exceptions.BadRequest: pass

    for user_id in DB.known_users:
        if DB.known_users[user_id].access_lvl in (conf.ACCESS_LEVELS.GROUP_STUDENT, conf.ACCESS_LEVELS.ADMIN):
            await bot.send_message(user_id, ua.queue_collection_start, reply_markup=await get_message_join_q_buttons())

async def Queue_Pair_Start(*args, **kwargs):
    DB.queue.start()

    for user in DB.queue:
        await bot.send_message(user.user_id, DB.queue.prettify(ua.queue_labels), reply_markup=await get_message_join_q_buttons())

    im_done_buts = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(ua.queue_im_done_but, callback_data="/queue_next")]
        ]
    )

    if DB.queue.current() is not None:
        await bot.send_message(DB.queue.current().user_id, ua.queue_you_are_now, reply_markup=im_done_buts)

    await Notify_Queue_Change(0)

    return True

async def Queue_End(*args, **kwargs):
    DB.queue.clear()

async def queue_show(message: types.Message, user_data: user_classes.TELEG_USER):
    buttons = types.InlineKeyboardMarkup(row_width=1,
        inline_keyboard=[
            [queue_but_gen(user_data)],
            [types.InlineKeyboardButton(ua.queue_show_but, callback_data="/show_queue")],
            [types.InlineKeyboardButton(ua.queue_invite_but, switch_inline_query=ua.queue_invite.format("https://t.me/{bot_name}?start=join_queue".format(bot_name=(await bot.get_me()).username)))],
        ]
    )

    return await bot.send_message(message.from_user.id, DB.queue.prettify(ua.queue_labels), reply_markup=buttons)

async def react_if_in_queue(user_id):
    if user_id in DB.queue and conf.queue_one_pos:
        await bot.send_message(user_id, ua.queue_already_joined, reply_markup=view_q_but(DB.known_users[user_id]))
        return True

    return False

async def queue_join_decider_IP24(message: types.Message, user_data: user_classes.TELEG_USER):

    try:
        return await queue_join(message, user_data, int(message.get_args()))
    except ValueError:
        pass
    except TypeError:
        pass

    queue_type_but = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(ua.queue_type_fast_but, callback_data="/join_queue 0")],
            [types.InlineKeyboardButton(ua.queue_type_slow_but, callback_data="/join_queue 1")],
        ]
    )

    return await bot.send_message(message.from_user.id, ua.queue_choose_type, reply_markup=queue_type_but)

async def queue_join_decider_ALTG(message: types.Message, user_data: user_classes.TELEG_USER):

    await queue_join(message, user_data, conf.queue_order.get(user_data.access_lvl, conf.queue_order[conf.ACCESS_LEVELS.OTHER_STUDENT]))

    return

async def queue_join(message: types.Message, user_data: user_classes.TELEG_USER, priority = None):

    if await react_if_in_queue(user_data.user_id): return False

    if priority is None:
        try:
            priority = int(message.get_args())
        except ValueError:
            priority = conf.queue_order.get(user_data.access_lvl, conf.queue_order[conf.ACCESS_LEVELS.OTHER_STUDENT])
        except TypeError:
            priority = conf.queue_order.get(user_data.access_lvl, conf.queue_order[conf.ACCESS_LEVELS.OTHER_STUDENT])

    pos = DB.queue.add(priority, user_data)

    await Notify_Queue_Change(pos)

    await bot.send_message(message.from_user.id, ua.queue_joined, reply_markup=view_q_but(user_data))

    if DB.queue.current() is None and DB.queue:
        await queue_next(message, user_data)

    return

async def queue_leave(message: types.Message, user_data: user_classes.TELEG_USER):
    if user_data.user_id not in DB.queue: return await bot.send_message(message.from_user.id, ua.queue_didnt_joined, reply_markup=view_q_but(user_data))

    res_leave = DB.queue.remove(user_data)

    if res_leave is not None:
        await bot.send_message(message.from_user.id, ua.queue_left, reply_markup=view_q_but(user_data))
        await Notify_Queue_Change(res_leave + 1)
    else:
        await bot.send_message(message.from_user.id, ua.queue_didnt_left, reply_markup=view_q_but(user_data))
    return

async def queue_next(message: types.Message, user_data: user_classes.TELEG_USER):

    if not DB.queue:
        return await bot.send_message(message.from_user.id, ua.queue_not_started)

    if not (user_data == DB.queue.current() or (len(DB.queue) > 0 and user_data == DB.queue[0])):
        return await bot.send_message(message.from_user.id, ua.you_cant)

    await force_next_queue(message, user_data)

    return

async def force_next_queue(message: types.Message, user_data: user_classes.TELEG_USER):

    if DB.queue.current() is not None:
        buttons = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(ua.queue_join_but + " " + emoji.join_queue, callback_data="/join_queue")]
            ]
        )

        await bot.send_message(DB.queue.current().user_id, ua.queue_place_end, reply_markup=buttons)

    current_u: user_classes.TELEG_USER = DB.queue.next()

    if current_u is not None:

        im_done_buts = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(ua.queue_im_done_but, callback_data="/queue_next")]
            ]
        )

        await bot.send_message(DB.queue.current().user_id, ua.queue_you_are_now, reply_markup=im_done_buts)

    await Notify_Queue_Change(0)

    return

#end queues

#rozklad
async def send_pair_info(chat_id: int, pair: schedules.study_hour | schedules.dodka_hour):
    buttons = types.InlineKeyboardMarkup()
    if pair.link != "":
        buttons.add(
            types.InlineKeyboardButton("ТИЦЬ!", url=pair.link)
        )
    await bot.send_message(chat_id, ua.pair_info.format(f=pair.time_start.strftime("%H:%M"),t=pair.time_end.strftime("%H:%M"), name=pair.subject, teacher=pair.teacher), reply_markup=buttons)

async def show_full_schedule(message: types.Message, user_data: user_classes.TELEG_USER):

    def generate_message_for_week(week_i, week_dict):
        res = ua.show_full_week_head.format(week_i+1)

        for d in week_dict:

            if len(week_dict[d]) == 0: continue

            res += ua.show_full_day_head.format(ua.week_days[d].upper())

            for h in week_dict[d]:
                res+= ua.pair_info_super_shorted.format(**week_dict[d][h])

        return res

    s_dict = DB.schedule.dict()

    await bot.send_message(message.from_user.id, ua.full_schedule.format(int(DB.schedule.now_active().week_index) + 1))

    for w in s_dict:
        await bot.send_message(message.from_user.id, generate_message_for_week(w, s_dict[w]))

def str_day_schedule(day: schedules.study_day):
    res = ""
    for pair in day:
        res += "\n\n" + ua.pair_info_shorted.format(link = pair.link, name = pair.subject, teacher = pair.teacher, f = pair.time_start.strftime("%H:%M"), t = pair.time_end.strftime("%H:%M"), queue = (emoji.pair_has_q if pair.queue else emoji.pair_has_no_q))

    return res

async def show_full_schedule_for_today(message: types.Message, user_data: user_classes.TELEG_USER):
    text = ua.this_day_schedule

    today = DB.schedule.now_active().now_active()

    if not today:
        text += "\n\n" + ua.no_pairs
    else:
        text += str_day_schedule(today)

    await bot.send_message(message.from_user.id, text)

async def show_full_schedule_for_tomorrow(message: types.Message, user_data: user_classes.TELEG_USER):
    next_day = DB.schedule.now_active().next_active()

    if next_day is None:
        next_day = DB.schedule.next_active().days[0]

    text = ua.next_day_schedule

    if not next_day:
        text += "\n\n" + ua.no_pairs
    else:
        text += str_day_schedule(next_day)

    await bot.send_message(message.from_user.id, text)

async def show_what_pair_now(message: types.Message, user_data: user_classes.TELEG_USER):
    pair = DB.schedule.now_active().now_active().now_active()
    if pair is None:
        return await bot.send_message(message.from_user.id, ua.no_pair_now)
    else:
        return await send_pair_info(message.from_user.id, pair)

async def show_what_pair_next(message: types.Message, user_data: user_classes.TELEG_USER):
    pair = DB.schedule.now_active().now_active().next_active()
    if pair is None:
        return await bot.send_message(message.from_user.id, ua.no_pair_next)
    else:
        return await send_pair_info(message.from_user.id, pair)

async def special_schedule_for_today(message: types.Message, user_data: user_classes.TELEG_USER):
    await show_full_schedule_for_today(message, user_data)
    await show_what_pair_now(message, user_data)

#adding extra pair

async def dod_show(chat_id, dodka: schedules.dodka_hour):

    hour_num = DB.schedule.schedule[dodka.week_index].days[dodka.day_index].find(dodka)

    change_buts = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(ua.but_delete, callback_data=f"/delete_dod {dodka.week_index} {dodka.day_index} {hour_num}")],
            [types.InlineKeyboardButton(ua.but_notif_all, callback_data=f"/notif_dod {dodka.week_index} {dodka.day_index} {hour_num}")],
        ]
    )

    return await bot.send_message(chat_id, ua.dodka_info.format(**dodka.dict()), reply_markup=change_buts)

async def delete_dod(message: types.Message, user_data: user_classes.TELEG_USER):
    week_i, day_i, hour_i = map(int, message.get_args().split(" "))

    try:
        DB.schedule.del_dodka(week_i, day_i, hour_i)
    except IndexError:
        return await bot.send_message(message.from_user.id, ua.this_hour_is_not_dodka)
    except schedules.HourNotDodka:
        return await bot.send_message(message.from_user.id, ua.this_hour_is_not_dodka)
    except schedules.CantDeleteActive:
        return await bot.send_message(message.from_user.id, ua.cant_delete_active)

    return await bot.send_message(message.from_user.id, ua.dodka_deleted)

async def notif_dod_all(message: types.Message, user_data: user_classes.TELEG_USER):
    week_i, day_i, hour_i = map(int, message.get_args().split(" "))

    dodka = DB.schedule.get_pair(week_i, day_i, hour_i)

    text = ua.dod_added + "\n\n" + ua.dodka_info_pretty.format(link = dodka.link, subject = dodka.subject, teacher = dodka.teacher, f = dodka.time_start.strftime("%H:%M"), t = dodka.time_end.strftime("%H:%M"), queue = (emoji.pair_has_q if dodka.queue else emoji.pair_has_no_q), week_num =dodka.week_index + 1, day = ua.week_days[dodka.day_index])

    async def func(_user_id):
        await bot.send_message(_user_id, text)

    for user_id in DB.known_users:
        if DB.known_users[user_id].access_lvl in (conf.ACCESS_LEVELS.GROUP_STUDENT, conf.ACCESS_LEVELS.ADMIN) \
                and DB.known_users[user_id].notif_settings.notif_pairs:
            asyncio.create_task(func(user_id))

    for chat_id in conf.queue_notify_chats:
        await bot.send_message(chat_id, text)

async def dod_create(message: types.Message, user_data: user_classes.TELEG_USER):
    await bot.send_message(message.from_user.id, ua.add_dodka_inst, reply_markup=cancel_but())

    user_data.answer_function = user_classes.answer_function(dod_menu)

async def show_all_dods(message: types.Message, user_data: user_classes.TELEG_USER):
    for w_i, w in enumerate(DB.schedule.schedule):
        for d_i, d in enumerate(w.days):
            for h_i, h in enumerate(d.hours):
                if isinstance(h, schedules.dodka_hour):
                    await dod_show(message.from_user.id, h)

async def dod_menu(message: types.Message, user_data: user_classes.TELEG_USER):

    data = message.text.split("\n")

    try:
        dodka_dict= {
            "subject" : data[0],
            "time_start" : datetime.strptime(data[1], "%H:%M"),
            "time_end" : datetime.strptime(data[2], "%H:%M"),
            "teacher" : data[3],
            "link" : data[4],
            "queue" : data[5] == "True",
            "week_num" : int(data[6]) - 1,
            "day_num" : int(data[7]) - 1
        }
    except ValueError:
        await dod_create(message, user_data)
        return
    except IndexError:
        await dod_create(message, user_data)
        return

    added = DB.schedule.add_dodka(**dodka_dict)

    await bot.send_message(message.from_user.id, ua.dodka_check_and_done, reply_markup=start_butts())

    await dod_show(message.from_user.id, added)
#end dods

async def Notify_All_About_Next_Pair(pair: schedules.study_hour, *args, **kwargs):

    async def func(_user_id):
        await bot.send_message(_user_id, ua.soon_next_pair.format(string_time_class.s_t(conf.notice_before_pair)))
        await send_pair_info(_user_id, pair)

    for user_id in DB.known_users:
        if DB.known_users[user_id].access_lvl in (conf.ACCESS_LEVELS.GROUP_STUDENT, conf.ACCESS_LEVELS.ADMIN) \
                and DB.known_users[user_id].notif_settings.notif_pairs:
            asyncio.create_task(func(user_id))

async def Notify_All_About_Current_Pair(pair: schedules.study_hour, *args, **kwargs):

    async def func(_user_id):
        await bot.send_message(_user_id, ua.now_next_pair)
        await send_pair_info(_user_id, pair)

    for user_id in DB.known_users:
        if DB.known_users[user_id].access_lvl in (conf.ACCESS_LEVELS.GROUP_STUDENT, conf.ACCESS_LEVELS.ADMIN) \
                and DB.known_users[user_id].notif_settings.notif_pairs:
            asyncio.create_task(func(user_id))


async def Notify_All_About_This_Pair_End(pair: schedules.study_hour, *args, **kwargs):
    text = ua.this_pair_end

    if pair is not None:
        text = text.format(ua.soon_next_pair.format(string_time_class.s_t(pair.till_start_end()[0])))
    else:
        text = text.format(ua.no_pair_next)

    async def func(_user_id):
        await bot.send_message(_user_id, text)
        if pair is not None:
            await send_pair_info(_user_id, pair)

    for user_id in DB.known_users:
        if DB.known_users[user_id].access_lvl in (conf.ACCESS_LEVELS.GROUP_STUDENT, conf.ACCESS_LEVELS.ADMIN) \
                and DB.known_users[user_id].notif_settings.notif_pairs:
            asyncio.create_task(func(user_id))

async def Morning_Notif_Schedule(day: schedules.study_day, *args, **kwargs):
    text = ua.this_day_schedule

    if not day:
        text += "\n\n" + ua.no_pairs
    else:
        text += str_day_schedule(day)

    async def func(_user_id):
        await bot.send_message(_user_id, text)

    for user_id in DB.known_users:
        if DB.known_users[user_id].access_lvl in (conf.ACCESS_LEVELS.GROUP_STUDENT, conf.ACCESS_LEVELS.ADMIN) \
                and DB.known_users[user_id].notif_settings.notif_morning:
            asyncio.create_task(func(user_id))

#end rozklad
# import requests as req
# async def check_moodle(message: types.Message, user_data: user_classes.TELEG_USER):
#
#     resp = req.get("https://stats.uptimerobot.com/api/getMonitorList/xwAP9TL0r2?page=1")
#
#     if resp.json()["statistics"]["counts"]["down"] == 0:
#         return await bot.send_message(message.from_user.id, ua.moodle_work)
#     else:
#         return await bot.send_message(message.from_user.id, ua.moodle_sleep)

async def place_holder(message: types.Message, user_data: user_classes.TELEG_USER):
    return await bot.send_message(message.from_user.id, f"PLACE HOLDER {user_data.user_id}")

#end command function

emoji_shortcut = {
    # emoji.moodle_status:"/moodle",
    emoji.join_queue:"/join_queue",
    emoji.leave_queue:"/leave_queue",
    emoji.show_full_roz_for_today_but:"/pairs_today",
    emoji.show_full_roz_for_tomorrow_but:"/pairs_tomorrow",
    emoji.show_full_roz_but:"/full_rozklad",
    emoji.settings:"/settings",
    emoji.cancel:"/cancel",
}

admin_comms = {
    "/help": admins_comms,
    "/add_dodka": dod_create,
    "/delete_dod": delete_dod,
    "/all_dods": show_all_dods,
    "/force_q": force_next_queue,
    "/q_c_t": Queue_Collecting_Start,
    "/q_s_t": Queue_Pair_Start,
}

starter_comms = {
    "/start":auth_start,
    "/auth_main":auth_main,
    "/auth_alt":auth_alt_PIB,
}

gen_comms = {
    "/me":me,
    "/start":starter,
    # "/moodle":check_moodle,
    "/leave_queue": queue_leave,
    "/queue_next": queue_next,
    "/show_queue": queue_show,
    "/cancel": cancel,
}

IP24_comms = {
    "/join_queue": queue_join_decider_IP24,
    "/pairs_today": special_schedule_for_today,
    "/pairs_tomorrow": show_full_schedule_for_tomorrow,
    "/full_rozklad": show_full_schedule,
    "/settings":notifications_menu,
    "/set_setting":set_setting,
    "/notif_dod":notif_dod_all,
}

altg_comms = {
    "/join_queue": queue_join_decider_ALTG,
}



COMMANDS = {
    conf.ACCESS_LEVELS.DEFAULT: (starter_comms),
    conf.ACCESS_LEVELS.OTHER_STUDENT: (gen_comms | altg_comms),
    conf.ACCESS_LEVELS.GROUP_STUDENT: (gen_comms | IP24_comms),
    conf.ACCESS_LEVELS.ADMIN: (gen_comms | IP24_comms | admin_comms),
}

async def perform_for_commands(command: str, message: types.Message, user_data: user_classes.TELEG_USER):
    available_commands = COMMANDS.get(user_data.access_lvl, COMMANDS.get(conf.ACCESS_LEVELS.DEFAULT, {}))  # if unknown access level than give default level commands, if none present give empty

    to_command = available_commands.get(command, None)

    if to_command is not None:
        return await to_command(message, user_data)
    else:
        return



#catchers

@dp.message_handler(content_types="video")
async def media_catcher(message: types.Message):
    logger_.info(u'%(author)13s:%(id)-13s | vid-> %(message)s' % {"author": message.from_user.first_name, "message": message.video.file_id, "id": message.from_user.id})
    author_profile = funcs.get_user_profile_from_message(message, DB)

    if author_profile.answer_function is not None:
        return await author_profile.answer(message=message, user_data=author_profile)

@dp.message_handler(content_types="photo")
async def media_catcher(message: types.Message):
    logger_.info(u'%(author)13s:%(id)-13s | pho-> %(message)s' % {"author": message.from_user.first_name, "message": message.photo[0].file_id, "id": message.from_user.id})
    author_profile = funcs.get_user_profile_from_message(message, DB)

    if author_profile.answer_function is not None:
        return await author_profile.answer(message=message, user_data=author_profile)

@dp.message_handler(content_types="text")
async def message_processor(message: types.Message):
    try:
        await dp.throttle('message', rate=0.4)
    except AIO_Exceptions.Throttled:
        return

    author_profile = funcs.get_user_profile_from_message(message, DB)

    logger_.info(u'%(author)13s:%(id)-13s:%(lvl)s:%(id_c)-13s | msg-> %(message)s' % {"author": message.from_user.first_name, "message": message.text, "id": message.from_user.id, "id_c": message.chat.id, "lvl": author_profile.access_lvl})

    command = message.get_command()

    if command is None:
        if message.text[-1] in emoji_shortcut:
            command = emoji_shortcut[message.text[-1]]
        else:
            if author_profile.answer_function is not None:
                await author_profile.answer(message = message, user_data = author_profile)
            return

    await perform_for_commands(command, message, author_profile)

@dp.callback_query_handler(lambda message: True)
async def query_processor(query: types.CallbackQuery):

    logger_.info(u'%(author)13s:%(id)-13s | q-> %(message)s' % {"author": query.from_user.first_name, "message": query.data, "id": query.from_user.id})

    if query.from_user.id not in DB.known_users:
        return

    author_profile = DB.known_users[query.from_user.id]

    author_profile.answer_function = None

    message = query.message
    message.text = query.data
    message.from_user = query.from_user

    if author_profile.access_lvl <= conf.ACCESS_LEVELS.BANNED:  # unauthorized
        return

    extracted_command = message.text.split(" ")[0]

    await perform_for_commands(extracted_command, message, author_profile)

#end catchers



async def custom_shutdown(*args, **kwargs):
    DB.save()
    print("SHUTTING DOWN")

async def Schedule_manager():
    await DB.schedule.manage(
        logger_,

        Notify_All_About_Next_Pair,
        Notify_All_About_Current_Pair,
        Notify_All_About_This_Pair_End,

        Queue_Collecting_Start,
        Queue_Pair_Start,

        clear_dynamic_messages,

        conf.notice_before_pair,
    )

async def custom_startup(*args, **kwargs):

    asyncio.create_task(Schedule_manager())

    print("BOT HAS BEEN STARTED")

if __name__ == "__main__":

    def load_no_file():
        print("FAILED TO FIND OR LOAD SAFE FILE")

        if input("Use load without save file? (Using only json *some data might be lost*) y/n --> ") in ["Y", "y"]:
            DB.load({"known_users": {}})

    if input("Use saved data? y/n --> ") in ["Y", "y"]:
        try:
            with open("savedata/save-file", "rb") as f:
                load_file: dict = pickle.load(f)

            DB.load(load_file)
        except FileNotFoundError:
            load_no_file()
        except AttributeError:
            load_no_file()


    executor.start_polling(dp, skip_updates=True, on_shutdown=custom_shutdown,on_startup=custom_startup)