import telebot
from telebot import types
import datetime
import psycopg2
from copy import copy

token = "5654099089:AAHOrE1LZAUIhJzQ5ROiiWgbP1FEv0Acj3Q"

conn = psycopg2.connect(database="telegram_bot",
                        user="aleksejkessler",
                        password="8205",
                        host="localhost",
                        port="5433")

cursor = conn.cursor()

bot = telebot.TeleBot(token)

mon = types.KeyboardButton('Понедельник')
tue = types.KeyboardButton('Вторник')
wed = types.KeyboardButton('Среда')
thur = types.KeyboardButton('Четверг')
fri = types.KeyboardButton('Пятница')
cur_week = types.KeyboardButton('Расписание на текущую неделю')
next_week = types.KeyboardButton('Расписание на следующую неделю')

keyboard = types.ReplyKeyboardMarkup()
keyboard.add(mon)
keyboard.add(tue)
keyboard.add(wed)
keyboard.add(thur)
keyboard.add(fri)
keyboard.add(cur_week)
keyboard.add(next_week)


def week1():
    week_number = datetime.datetime.today().isocalendar()[1]
    return week_number - 4


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    help_message = '''Здравствуйте! Я бот, созданный Кесслером Алексеем из группы БВТ2202.
Я умею выводить ваше расписание, а также информацию о вашем ВУЗе.
Это немного, но это честная работа. 🤗
Основные команды:
/start - начало работы
/help - краткая информация обо мне
/week - какая сейчас неделя, четная или нечетная
/mtuci - сайт вашего ВУЗа
'''
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['mtuci'])
def help(message):
    mtuci_site = "https://mtuci.ru/"
    bot.send_message(message.chat.id, mtuci_site, reply_markup=keyboard)


@bot.message_handler(commands=['week'])
def week(message):
    week_number = datetime.datetime.today().isocalendar()[1]
    s = "Сейчас идет четная неделя, номер "
    if week_number % 2 == 1:
        s = "Сейчас идет нечетная неделя, номер "
    bot.send_message(message.chat.id, s + str(week_number - 4), reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def answer(message):

    def search(s):
        cursor.execute("select subject, room_numb, start_time from timetable where day = '{}'".format(s))
        records = list(cursor.fetchall())

        cnt = 1
        for d in records:
            s += "\n"
            s = s + str(cnt) + "-----------\n"
            s = s + "Предмет: {}\n".format(d[0])
            s = s + "Аудитория: {}\n".format(d[1])
            s = s + "Начало занятия: {}\n".format(d[2])
            cnt += 1
        return s

    r_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']

    s = message.text
    if week1() % 2 == 1:
        s = s + "_нечет"
    else:
        s = s + "_чет"

    if message.text in r_week:
        bot.send_message(message.chat.id, search(s), reply_markup=keyboard)

    elif message.text == "Расписание на текущую неделю":
        for r in r_week:
            s = copy(r)
            if week1() % 2 == 1:
                s = s + "_нечет"
            else:
                s = s + "_чет"
            bot.send_message(message.chat.id, search(s), reply_markup=keyboard)

    elif message.text == "Расписание на следующую неделю":
        for r in r_week:
            s = copy(r)
            if week1() % 2 == 0:
                s = s + "_нечет"
            else:
                s = s + "_чет"
            bot.send_message(message.chat.id, search(s), reply_markup=keyboard)

    else:
        bot.send_message(message.chat.id, 'Извините, я вас не понимаю(((', reply_markup=keyboard)


bot.infinity_polling()
