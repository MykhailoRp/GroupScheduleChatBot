import configurator as _conf

class ua:
    starter = f"Привіт!\nЯ <b>{_conf.bot_name} {_conf.this_group}</b>, твій єдиний інфобот"
    canceled = "Відмінено ❌"
    but_cancel = "Відмінити"
    but_done = "Готово"
    but_change = "Змінити"
    but_delete = "Видалити"

    authorize_start = "Перед початком роботи мені треба від вас ваше <b>ПІБ</b> та <b>група</b>"
    authorize_IP24 = f"Надайте ваше <b>ПІБ</b>, за прикладом \"Зубенко Михайло Петрович\", для авторизації як член групи\nЯкщо ви не з <b>{_conf.this_group}</b> тисніть кнопку знизу 👇"
    IP24_auth_ready = "Вітаю, <b>{}</b>, тепер ви член групи"
    IP24_auth_failed = "Нажаль на ваше ім'я, <b>{}</b>, вже зареєстровано користувача, або воно відсутнє у списку групи"
    alt_auth_group = f"Надайте свою <b>групу</b>, за прикладом \"<b>{_conf.this_group}</b>\""
    alt_auth_PIB = f"Надайте ваше <b>ПІБ</b>, за прикладом \"<b>Зубенко Михайло Петрович</b>\", для подальшого розпізнавання викладачами\nЯкщо ви з <b>{_conf.this_group}</b> тисніть кнопку знизу 👇"
    alt_auth_no_IB = "Схоже що ви не надали ваше ім'я та по-батькові, або вказали їх разом з прізвищем, спробуйте знову."
    alt_auth_no_B = "Схоже що ви не надали ваше по-батькові, або вказали його разом з ім'ям, спробуйте знову."
    alt_auth_ready = "Ви тепер зареєстровані як член іншої групи, в черзі ви будете відображені як <b>{}</b>"
    IP24_group_but = f"Я член {_conf.this_group}"
    alt_group_but = "Я з іншої групи"

    full_schedule = "<b>Повний розклад на обидва тижні</b>\n\n<i>Зараз тиждень: {}</i>"
    this_day_schedule = "<b>Розклад на сьогодні:</b>"
    next_day_schedule = "<b>Розклад на завтра:</b>"
    no_pairs = "Нема пар"
    no_pair_now = "Зараз пари нема"
    no_pair_next = "Далі пари на сьогодні нема"
    soon_next_pair = "За {} розпочнеться наступна пара"
    this_pair_end = "Ця пара завершена\n{}"
    now_next_pair = "Зараз розпочинається наступна пара"
    pair_info = '{f} - {t}\n<b>{name}</b>\n<i>{teacher}</i>'
    pair_info_shorted = '{f} - {t} {queue}\n<a href="{link}"><b>{name}</b></a>\n<i>{teacher}</i>'
    pair_info_super_shorted = '   <i>{time_start}-{time_end} <a href="{link}"><b>{subject}</b></a></i>\n'
    show_full_week_head = 'Розклад для тижня {}:\n'
    show_full_day_head = '- <b>{}</b>:\n'
    show_what_now_but = "Яка пара зараз?"
    show_what_next_but = "Яка пара наступна?"
    show_full_roz_for_today_but = "Розклад на сьогодні"
    show_full_roz_for_tomorrow_but = "Розклад на завтра"
    show_full_roz_but = "Повний розклад"
    week_days = [
        "понеділок",
        "вівторок",
        "середа",
        "четвер",
        "п'ятниця",
        "субота",
        "неділя",
    ]

    add_dodka_inst = "Додайте додку за таким форматом:\n\n<b>Назва\nЧас початку <i>(години:хвилини)</i>\nЧас кінця <i>(години:хвилини)</i>\nПрепод\nПосилання <i>(якщо відсунє то пустим)</i>\nЧи треба чергу <i>(True/False)</i>\nНомер тижня <i>(1-2)</i>\nНомер дня тижня <i>(1-7)</i></b>"
    dodka_check_and_done = "Перевірте дані, якщо щось не так, то перевведіть"
    this_hour_is_not_dodka = "Ця кнопка втратила актуальність"
    cant_delete_active = "Ви не можете видаляти наступні або активні додки"
    dodka_deleted = "Додку видалено"
    dod_added = "Додано додаткову пару"
    dodka_info = "<b>{subject}</b>\n{time_start} - {time_end}\n{teacher}\n{link}\nЧерга: {queue}\nНомер тижня: {week_num}\nНомер дня: {day_num}"
    dodka_info_pretty = '<a href="{link}"><b>{subject}</b></a>  {queue}\n<b>{f} - {t}</b>\n<i>{teacher}</i>\n\nНомер тижня: <b>{week_num}</b>\nДень: <b>{day}</b>'
    but_notif_all = "Повідомити студентів"

    queue_collection_start = "Незабаром розпочнеться пара для якої треба сформувати <b>чергу</b>\n\nТисни\n - Першу кнопку знизу щоб приєднатись до швидкої черги\n - Другу щоб щоб приєднатись до пізнішої черги\n - Третю щоб запросити інші групи"
    queue_joined = "Ви приєднались до черги, щоб її переглянути натисніть нижче 👇"
    queue_already_joined = "Ви <b>ВЖЕ</b> перебуваєте в черзі, щоб її переглянути натисніть нижче 👇"
    queue_not_started = "Чергу ще не розпочато"
    queue_didnt_joined = "Ви не стоїте в черзі"
    queue_left = "Ви облишили чергу"
    queue_didnt_left = "Ви не змогли облишити чергу"
    queue_you_are_now = "Ви зараз маєте відповідати,\nпо завершенню вашої відповіді натисніть кнопку нижче 👇"
    queue_you_are_next_skip = "Ви наступний хто має відповідати\n<i>Якщо студент перед вами завершив доповіть але не передав чергу, натисніть кнопку нижче 👇</i>"
    queue_you_are_next_no_skip = "Ви наступний хто має відповідати"
    queue_you_are_now_num = "Черга здвинулась, ваше місце тепер: {}"
    queue_place_end = "Ви завершили свою доповідь 🥳\nЯкщо ви бажаєте перездати або доздати ще щось на цій парі, натисніть нижче 👇"
    queue_invite = f"\nВи можете приєднатись до черги наступної пари {_conf.this_group} за посиланням:\n{{}}"
    queue_choose_type = "Як швидко ви готові здавати вашу роботу?"
    queue_im_done_but = "Я завершив доповідь"
    queue_person_before_done_but = "Студент попереду завершив"
    queue_join_but = "Увійти до черги"
    queue_leave_but = "Облишити чергу"
    queue_invite_but = "Запросити інші групи"
    queue_show_but = "Переглянути чергу"
    queue_type_fast_but = "Якнайшвидше 🏃💨‍"
    queue_type_slow_but = "Почекаю ⏳"
    queue_fast_but = "Швидка черга 🏃💨‍"
    queue_slow_but = "Звичайна черга ⏳"
    queue_type_last_but = "Підкінець ⌛️"
    queue_labels = [
        "Швидка черга для студентів групи",
        "Звичайна черга для студентів групи",
        "Черга для студентів інших груп",
    ]

    you_cant = "Ви не можете цього зробити"

    # moodle_sleep = "<i>Спить</i>  🥱💤💤💤💤"
    # moodle_work = "<b>Працює</b> 🥵💨💨💨💨"
    # moodle_but = "Що там Мудл?"

    notif_options = {
        "notif_pairs": "Нагадування про пари",
        "notif_morning": "Надсилати розклад зранку",
        "queue_movement": "Повідомляти про просування черги",
    }
    options_menu = "Список опцій які можна налаштувати:"
    settings_but = "Налаштування"

class emoji:
    cancel = "❌"

    # moodle_status = "🔮"

    leave_queue = "🚪"
    join_queue = "🙋"

    pair_has_q = "✅👥"
    pair_has_no_q = "⛔👥"

    show_full_roz_for_today_but = "🤔"
    show_full_roz_for_tomorrow_but = "⏰"
    show_full_roz_but = "📋"

    option_on = "➖✅"
    option_off = "🛑➖"
    settings = "⚙"