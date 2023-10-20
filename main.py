import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6533784661:AAFX9_uK2ccrJvOnj01Dof8u1UKK9aAFgTk",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Анкета"  # Можно менять текст
text_button_1 = "Мультфильмы\сериалы на вечер"
text_button_2 = "Анекдоты"
text_button_3 = "Гороскоп"


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Здравствуйте! Здесь вы сможете отдохнуть от работы или учёбы в любое время! Выберете, что будем делать сначала)',  # Можно менять текст
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Ваше _любимое_ хобби?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Отличное хобби! От чего вы хотите сегодня отдохнуть?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Понимаю вас, спасибо за ответы, отдохните хорошенько ;)', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "*1)Мультфильмы:* Тачки(все части), Вверх, Вперёд, Кот в Сапогах 2, Плохие Парни, Я краснею, Ледниковый период (все части), Зверопой 1,2, Зверополис, Райя и Последний дракон, Лука, Тролли 1,2, Леди Баг и Супер Кот: Пробуждение, Как приручить Дракона (все 3 части и сериал).    *2) МультСериалы:* Рик и Морти, С приветом по планетам, Кик Бутовски, Гравити Фолз, Дом Совы, Время приключений, Черепашки-Ниндзя, Ну погоди, Леопольд, Дружба - это чудо, Кит и Кэт, Чип и Дейл, Смешарики, Братз, Монстр Хай, Скуби Ду.     *3) Фильмы:* Форсаж, Чарли и шоколадная фабрика, Джуманджи, Перевозчик, Красное Уведомление, Аватар 1,2, Чебурашка, Марсупелами, Железный человек, Мстители, Риддик, Иллюзия обмана 1,2, Трансформеры, Ёлки, Один дома(все части), Зачётный препод, Т-34"
, reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "*1.)* Ты знаешь, Юрка попал в больницу.  – Удивительно! Ведь только вчера вечером я видел его с очаровательной блондинкой! – Его жена тоже видела. * 2)* Папа, Мама попросила, чтобы ты походил по комнате без тапочек. — Зачем? Она потеpяла иголку и хочет ее найти. *3)* Учитель пишет на доске разноцветными мелками. Раздается голос из класса. — А голубым не видно. Учитель:— Пусть пересядут на первую парту. *4)* Жил был Спирт. О своем семейном положении отвечал просто. — Разведен.  *5)* Жена ссорится с мужем. – Уж лучше бы я вышла замуж за черта, чем за тебя! Это исключено, немедленно парирует муж. – Браки между ближайшими родственниками запрещены.   *6)* Дарить воздушные шарики — странная традиция: — С Днем рождения! Вот — держи резиновый мешочек, в который я предварительно надышал. *7)* Интересная рыцарская традиция — бросить перчатку в лицо врагу, чтобы вызвать его на поединок. Учитывая, что весила рыцарская перчатка 15 кг, при удачном броске, можно было обойтись и без поединка. *8)* — Ты чего такая грустная? — Да муж на восьмое марта духи подарил. А вечером, хоть я его и просила, все равно выпил. — Но в праздник-то можно и выпить. — Он духи выпил.  *9)* — Чай или кофе? — Кофе. — Слабый или крепкий? — Слабый, но с коньяком. *10)*  Вовочка, Ты кого больше слушаешь маму или папу? – Маму. Почему? – Она говорит больше.", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "_Гороскоп на 17 октября:_  *ОВЕН* - Не будь терпилой, отстаивай себя, ведь кто, если не ты? *ТЕЛЕЦ* - Хорошее настроение обеспечено: ты, как солнышко — сияешь чистотой и жизнелюбием. *БЛИЗНЕЦЫ* - Ты сегодня сорвешь какой-то джекпот. *РАК* - Твоя мудрость вытащит тебя сегодня откуда угодно.  *ЛЕВ* - Любовь тебя ранит сегодня, но помни: безразличие — не преимущество. *ДЕВА* - Сыграй сегодня в прятки с тем, кто волнует твое сердце — пускай понервничает.       *ВЕСЫ* - Не обманывай себя, ты от этого никуда не убежишь. *СКОРПИОН* - Хороший день, чтобы приобрести себе то, что давно хотелось. *СТРЕЛЕЦ* - Не обижай близких, они этого не заслуживают. *КОЗЕРОГ* - Твое умение вить из людей веревочки сегодня выйдет на новый уровень. *ВОДОЛЕЙ* - Ты такая милашка, что всё хорошее сегодня будет исполнено, как только ты попросишь. *РЫБЫ* - Твоя красота сегодня способна сшибать с ног, вау.")


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()