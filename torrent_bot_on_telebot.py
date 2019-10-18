# -*- coding: utf-8 -*-

import pdb
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import requests
import urllib3
import sqlite3
import json
import utils
import config
from pprint import pprint
import queue
import threading


bot = telebot.TeleBot(config.token)


cat_dict = 'categories_dict.json'

CATEGORY = None
SUBCATEGORY = None
QUERY = None
isRunning = False


def get_ctgs():
    with open(cat_dict, 'r', encoding='utf-8') as dictionary:
        d = json.load(dictionary)
    ctgs = [x for i, x in enumerate(d)]
    return d, ctgs

def search():
    db = 'rutracker.sqlite'
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    answer = ''

    if (CATEGORY is not None) and (SUBCATEGORY is not None):
        try:
            cursor.execute("SELECT * FROM torrents WHERE Category=? AND Subcategory=?", (CATEGORY, SUBCATEGORY))
            result = cursor.fetchall()
            for i in result:
                name = list(i)[2]
                link = list(i)[3]
                if QUERY in name.lower():
                    answer += name + '\n' + link + '\n\n'
            conn.commit()
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
        finally:
            conn.close()
    elif QUERY is not None:
        try:
            cursor.execute("SELECT Magnet_link FROM torrents WHERE Torrent=?", (QUERY.capitalize()))
            result = cursor.fetchall()
            if len(result) == 0:
                answer = 'Поиск не дал результатов, убедитесь, что запрос введен верно'
            else:
                for i in result:
                    name = list(i)[2]
                    link = list(i)[3]
                    if QUERY in name.lower():
                        answer += name + '\n' + link + '\n\n'
            conn.commit()
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
        finally:
            conn.close()
    return answer

@bot.callback_query_handler(func=lambda call: True)
def category_query(call):
    """
    Function - handler of choosing caterory.
    :param call:
    :return:
    """
    global CATEGORY
    global SUBCATEGORY

    chat_id = call.from_user.id
    data = call.data

    _, ctgs = get_ctgs()

    category_choose_text = """Перенаправляю вас на выбор категории. Обратите внимание, что всего 117 категорий, \
    но за 1 раз вам будет выведено только 58. На остальные категории вы сможете переключиться внутри меню выбора. \
    Если оно не выводится, вы можете вызвать его с помощью команд /categories58 и /categories117"""

    if data == 'Выбор категории 1-58' or data == 'e2':
        send = bot.send_message(chat_id, category_choose_text)
        bot.register_next_step_handler(send, first_categories(call))
    elif data == 'Выбор категории 59-117' or data == 'e1':
        send = bot.send_message(chat_id, category_choose_text)
        bot.register_next_step_handler(send, second_categories(call))
    elif data == 'm':
        send = bot.send_message(chat_id, 'Возврат в стартовое меню')
        bot.register_next_step_handler(send, start(call))
    elif data.find('-', 1, 4) == -1:
        CATEGORY = ctgs[int(data)]
        send = bot.send_message(chat_id, 'Выбрана категория: {}'.format(CATEGORY))
        bot.register_next_step_handler(send, subcategories(call))
    elif data == 'back':
        send = bot.send_message(chat_id, 'Возвращаемся в выбор категорий')
        bot.register_next_step_handler(send, first_categories(call))
    elif len(data.split('-')) == 2:
        ctgs_dict, ctgs = get_ctgs()

        subcats = ctgs_dict[CATEGORY]

        sbct_clbk = {}

        for sbct in subcats:
            clean_sbct = sbct.replace("'", "\'")
            clbk = '{}-{}'.format(ctgs.index(CATEGORY), subcats.index(sbct))
            sbct_clbk[clbk] = clean_sbct

        if data in sbct_clbk:
            SUBCATEGORY = sbct_clbk[call.data]
            send = bot.send_message(chat_id, 'Выбрана подкатегория: {}'.format(SUBCATEGORY))
            bot.register_next_step_handler(send, targetsearch(call))


@bot.message_handler(func=lambda message: True)
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.from_user.id
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(InlineKeyboardButton('Инструкция', callback_data='Инструкция'),
                 InlineKeyboardButton('Выбор категории 1-58', callback_data='Выбор категории 1-58'),
                 InlineKeyboardButton('Выбор категории 59-117', callback_data='Выбор категории 59-117'),
                 InlineKeyboardButton('Поиск по категориям', callback_data='Поиск по категориям'),
                 InlineKeyboardButton('Глобальный поиск', callback_data='Глобальный поиск')
                 )
    introduction = """
    Добро пожаловать!\n\
    Данный бот осуществляет поиск magnet-ссылки на раздачу с сайта rutracker.org.\n\
    Чтобы понять, как работать с ботом рекомендуется прочитать инструкцию. Сделать это можно с помощью выбора \
    соответствующего пункта в меню, либо с помощью команды /instruction.
    """
    bot.send_message(chat_id, introduction, reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
@bot.message_handler(commands=['instruction'])
def instruction(message):
    chat_id = message.from_user.id
    instruction = """
    Мы все привыкли пользоваться сайтом rutracker.org и скачивать оттуда много полезного и приятного. \
    К сожалению, в последние годы доступ к нему хоть и не запрещен, но ограничен. \
    Данный бот предоставляет доступ к некоторым загрузкам, основываясь на архивах 2014 года. \
    В качестве результата своей работы он возвращает пользователю magnet-ссылку, с помощью которой можно так же запустить загрузку нужного файла. \
    О том как это сделать лучше читать в интернете.\n
    Все раздачи в рутрекере делятся по категориям, которые в свою очередь делятся на подкатегории, за редким исключением. \
    Это облегчает поиск, т.к. вычеркивает из поиска те категории, в которых явно не содержится нужная информация. \
    Категорий много, поэтому они разбиты на две группы. Ознакомиться с ними можно из меню, или с помощью команд /categories58 \
    и /categories117.\n
    Уже после выбора категории результаты поиска заметно улучшатся. Но чтобы выдача идеально подходила вашим запросам \
    так же рекомендуется выбрать подкатегорию. Сделать это так же можно из меню или по команде /subcategories. Главное, чтобы \
    перед выбором подкатегории была выбрана категория. Иначе не для чего будет выводить подкатегорию.\n
    После выбора категории и подкатегории можно осуществлять поиск по ним. Из меню или по команде /targetsearch. \
    Как и на сайте rutracker.org поиск можно осуществлять адресный или глобальный поиск. Для этого есть раздел в меню и команда /globalsearch.\n
    Желаем найти все!
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(InlineKeyboardButton('Выбор категории 1-58', callback_data='Выбор категории 1-58'),
                 InlineKeyboardButton('Выбор категории 59-117', callback_data='Выбор категории 59-117'),
                 InlineKeyboardButton('Поиск по категориям', callback_data='Поиск по категориям'),
                 InlineKeyboardButton('Глобальный поиск', callback_data='Глобальный поиск'),
                 InlineKeyboardButton('Меню', callback_data='Меню'),
                 )

    bot.send_message(chat_id, instruction, reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
@bot.message_handler(commands=['categories58'])
def first_categories(message):
    chat_id = message.from_user.id

    keyboard = InlineKeyboardMarkup()

    keyboard.row_width = 1

    _, ctgs = get_ctgs()

    for ctg in ctgs:
        if ctgs.index(ctg) < 59:
            keyboard.add(InlineKeyboardButton(ctg.replace("'", "\'"), callback_data=str(ctgs.index(ctg))))

    keyboard.add(InlineKeyboardButton('Еще категории', callback_data='e1'),
                 InlineKeyboardButton('Меню', callback_data='m'))
    bot.send_message(chat_id, 'Выберите категорию из списка', reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
@bot.message_handler(commands=['categories117'])
def second_categories(message):
    chat_id = message.from_user.id

    keyboard = InlineKeyboardMarkup()

    keyboard.row_width = 1

    _, ctgs = get_ctgs()

    for ctg in ctgs:
        if ctgs.index(ctg) > 58:
            keyboard.add(InlineKeyboardButton(ctg.replace("'", "\'"), callback_data=str(ctgs.index(ctg))))

    keyboard.add(InlineKeyboardButton('Еще категории', callback_data='e2'),
                 InlineKeyboardButton('Меню', callback_data='m'))
    bot.send_message(chat_id, 'Выберите категорию из списка', reply_markup=keyboard)
    return


@bot.message_handler(func=lambda message: True)
@bot.message_handler(commands=['subcategories'])
def subcategories(message):
    global SUBCATEGORY

    chat_id = message.from_user.id

    no_subcategory_text = """Сперва необходимо выбрать категорию. Сделать это можно из меню по команде /start или с помощью \
    команд /categories58 и /categories117"""

    subcategory_choose_text = """Перенаправляю вас на выбор подкатегории. Обратите внимание, что в каждой категории \
    свое количество подкатегорий. В некоторых категориях подкатегорий нет."""

    if CATEGORY == None:
        send = bot.send_message(message.from_user.id, no_subcategory_text)
        bot.register_next_step_handler(send, first_categories)

    with open(cat_dict, 'r', encoding='utf-8') as dictionary:
        d = json.load(dictionary)
        ctgs = [x for i, x in enumerate(d)]
        subcats = d[CATEGORY]
        if len(subcats) == 0:
            SUBCATEGORY = None
            text = """У категории ({}) нет подкатегорий. Перенаправляю вас на адресный поиск."""
            send = bot.send_message(chat_id, text.format(CATEGORY))
            bot.register_next_step_handler(send, targetsearch(message))
            return

    keyboard = InlineKeyboardMarkup()

    keyboard.row_width = 1

    for sbct in subcats:
        clean_sbct = sbct.replace("'", "\'")
        clbk = '{}-{}'.format(ctgs.index(CATEGORY), subcats.index(sbct))
        keyboard.add(InlineKeyboardButton(clean_sbct, callback_data=clbk))
    keyboard.add(InlineKeyboardButton('Назад', callback_data='back'))
    bot.send_message(chat_id, subcategory_choose_text, reply_markup=keyboard)
    return


@bot.message_handler(func=lambda message: True)
@bot.message_handler(commands=['globalsearch'])
def globalsearch(message):
    send = bot.send_message(message.from_user.id, 'Отправьте ваш запрос ответным сообщением')
    bot.register_next_step_handler(send, text_handler)


@bot.message_handler(func=lambda message: True)
@bot.message_handler(commands=['targetsearch'])
def targetsearch(message):
    if (CATEGORY is None) and (SUBCATEGORY is None):
        bot.send_message(message.from_user.id, 'Сперва необходимо выбрать категорию')
    send = bot.send_message(message.from_user.id, 'Отправьте ваш запрос ответным сообщением')
    bot.register_next_step_handler(send, text_handler)


# @bot.message_handler(content_types=['text'])
@ bot.message_handler(func=lambda message: True)
def text_handler(message):
    global QUERY
    QUERY = message.text.lower()
    send = bot.send_message(message.from_user.id, 'Ваш запрос обрабатывается')
    bot.register_next_step_handler(send, search())


if __name__ == '__main__':
    # bot.polling(none_stop=True, interval=0, timeout=20)
    pdb.run(bot.polling(none_stop=True))
    # bot.infinity_polling()
