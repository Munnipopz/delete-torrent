# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import sqlite3
import json
# import utils
import config
from pprint import pprint


bot = telebot.TeleBot(config.token)


dict = 'categories_dict.json'

CATEGORY = None
SUBCATEGORY = None
QUERY = None
isRunning = False


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Function - handler of choosing caterory.
    :param call:
    :return:
    """
    global CATEGORY
    category_choose_text = """Перенаправляю вас на выбор категории. Обратите внимание, что всего 117 категорий, \
    но за 1 раз вам будет вывеено только 58. На остальные категории вы сможете переключиться внутри меню выбора. \
    Если оно не выводится, вы можете вызвать его с помощью команд /categories58 и /categories117"""
    if call.data == 'Выбор категории 1-58':
        send = bot.send_message(call.from_user.id, category_choose_text)
        bot.register_next_step_handler(send, first_categories)
    elif call.data == 'Выбор категории 59-117':
        send = bot.send_message(call.from_user.id, category_choose_text)
        bot.register_next_step_handler(send, second_categories)
    elif call.data == '1':
        CATEGORY = 'Rutracker Awards (мероприятия и конкурсы)'
        send = bot.send_message(call.from_user.id, 'Выбрана категория: "{}"'.format(CATEGORY))
        bot.register_next_step_handler(send, subcategories)
    elif call.data == '2':
        bot.answer_callback_query(call.id, 'Выбрана категория Зарубежное кино')
        CATEGORY = 'Зарубежное кино'
    elif call.data == '3':
        bot.answer_callback_query(call.id, 'Выбрана категория Наше кино')
        CATEGORY = 'Наше кино'
    elif call.data == '4':
        bot.answer_callback_query(call.id, 'Выбрана категория Арт-хаус и авторское кино')
        CATEGORY = 'Арт-хаус и авторское кино'
    elif call.data == '5':
        bot.answer_callback_query(call.id, 'Выбрана категория Театр')
        CATEGORY = 'Театр'
    elif call.data == '6':
        bot.answer_callback_query(call.id, 'Выбрана категория DVD Video')
        CATEGORY = 'DVD Video'
    elif call.data == '7':
        bot.answer_callback_query(call.id, 'Выбрана категория HD Video')
        CATEGORY = 'HD Video'
    elif call.data == '8':
        bot.answer_callback_query(call.id, 'Выбрана категория 3D/Стерео Кино, Видео, TV и Спорт')
        CATEGORY = '3D/Стерео Кино, Видео, TV и Спорт'
    elif call.data == '9':
        bot.answer_callback_query(call.id, 'Выбрана категория Мультфильмы')
        CATEGORY = 'Мультфильмы'
    elif call.data == '10':
        bot.answer_callback_query(call.id, 'Выбрана категория Мультсериалы')
        CATEGORY = 'Мультсериалы'
    elif call.data == '11':
        bot.answer_callback_query(call.id, 'Выбрана категория Аниме')
        CATEGORY = 'Аниме'
    elif call.data == '12':
        bot.answer_callback_query(call.id, 'Выбрана категория Русские сериалы')
        CATEGORY = 'Русские сериалы'
    elif call.data == '13':
        bot.answer_callback_query(call.id, 'Выбрана категория Зарубежные сериалы')
        CATEGORY = 'Зарубежные сериалы'
    elif call.data == '14':
        bot.answer_callback_query(call.id, 'Выбрана категория Зарубежные сериалы (HD Video)')
        CATEGORY = 'Зарубежные сериалы (HD Video)'
    elif call.data == '15':
        bot.answer_callback_query(call.id, 'Выбрана категория Сериалы Латинской Америки, Турции и Индии')
        CATEGORY = 'Сериалы Латинской Америки, Турции и Индии'
    elif call.data == '16':
        bot.answer_callback_query(call.id, 'Выбрана категория Азиатские сериалы')
        CATEGORY = 'Азиатские сериалы'
    elif call.data == '17':
        bot.answer_callback_query(call.id, 'Выбрана категория Вера и религия')
        CATEGORY = 'Вера и религия'
    elif call.data == '18':
        bot.answer_callback_query(call.id, 'Выбрана категория Документальные фильмы и телепередачи')
        CATEGORY = 'Документальные фильмы и телепередачи'
    elif call.data == '19':
        bot.answer_callback_query(call.id, 'Выбрана категория Документальные (HD Video)')
        CATEGORY = 'Документальные (HD Video)'
    elif call.data == '20':
        bot.answer_callback_query(call.id, 'Выбрана категория Развлекательные телепередачи и шоу, приколы и юмор')
        CATEGORY = 'Развлекательные телепередачи и шоу, приколы и юмор'
    elif call.data == '21':
        bot.answer_callback_query(call.id, 'Выбрана категория Зимние Олимпийские игры 2018')
        CATEGORY = 'Зимние Олимпийские игры 2018'
    elif call.data == '22':
        bot.answer_callback_query(call.id, 'Выбрана категория Спортивные турниры, фильмы и передачи')
        CATEGORY = 'Спортивные турниры, фильмы и передачи'
    elif call.data == '23':
        bot.answer_callback_query(call.id, 'Выбрана категория ⚽ Футбол')
        CATEGORY = '⚽ Футбол'
    elif call.data == '24':
        bot.answer_callback_query(call.id, 'Выбрана категория 🏀 Баскетбол')
        CATEGORY = '🏀 Баскетбол'
    elif call.data == '25':
        bot.answer_callback_query(call.id, 'Выбрана категория 🏒 Хоккей')
        CATEGORY = '🏒 Хоккей'
    elif call.data == '26':
        bot.answer_callback_query(call.id, 'Выбрана категория Рестлинг')
        CATEGORY = 'Рестлинг'
    elif call.data == '27':
        bot.answer_callback_query(call.id, 'Выбрана категория Сканирование, обработка сканов')
        CATEGORY = 'Сканирование, обработка сканов'
    elif call.data == '28':
        bot.answer_callback_query(call.id, 'Выбрана категория Книги и журналы (общий раздел)')
        CATEGORY = 'Книги и журналы (общий раздел)'
    elif call.data == '29':
        bot.answer_callback_query(call.id, 'Выбрана категория Для детей, родителей и учителей')
        CATEGORY = 'Для детей, родителей и учителей'
    elif call.data == '30':
        bot.answer_callback_query(call.id, 'Выбрана категория Спорт, физическая культура, боевые искусства')
        CATEGORY = 'Спорт, физическая культура, боевые искусства'
    elif call.data == '31':
        bot.answer_callback_query(call.id, 'Выбрана категория Гуманитарные науки')
        CATEGORY = 'Гуманитарные науки'
    elif call.data == '32':
        bot.answer_callback_query(call.id, 'Выбрана категория Исторические науки')
        CATEGORY = 'Исторические науки'
    elif call.data == '33':
        bot.answer_callback_query(call.id, 'Выбрана категория Точные, естественные и инженерные науки')
        CATEGORY = 'Точные, естественные и инженерные науки'
    elif call.data == '34':
        bot.answer_callback_query(call.id, 'Выбрана категория Ноты и Музыкальная литература')
        CATEGORY = 'Ноты и Музыкальная литература'
    elif call.data == '35':
        bot.answer_callback_query(call.id, 'Выбрана категория Военное дело')
        CATEGORY = 'Военное дело'
    elif call.data == '36':
        bot.answer_callback_query(call.id, 'Выбрана категория Психология')
        CATEGORY = 'Психология'
    elif call.data == '37':
        bot.answer_callback_query(call.id, 'Выбрана категория Коллекционирование, увлечения и хобби')
        CATEGORY = 'Коллекционирование, увлечения и хобби'
    elif call.data == '38':
        bot.answer_callback_query(call.id, 'Выбрана категория Художественная литература')
        CATEGORY = 'Художественная литература'
    elif call.data == '39':
        bot.answer_callback_query(call.id, 'Выбрана категория Компьютерная литература')
        CATEGORY = 'Компьютерная литература'
    elif call.data == '40':
        bot.answer_callback_query(call.id, 'Выбрана категория Комиксы, манга, ранобэ')
        CATEGORY = 'Комиксы, манга, ранобэ'
    elif call.data == '41':
        bot.answer_callback_query(call.id, 'Выбрана категория Коллекции книг и библиотеки')
        CATEGORY = 'Коллекции книг и библиотеки'
    elif call.data == '42':
        bot.answer_callback_query(call.id, 'Выбрана категория Мультимедийные и интерактивные издания')
        CATEGORY = 'Мультимедийные и интерактивные издания'
    elif call.data == '43':
        bot.answer_callback_query(call.id, 'Выбрана категория Медицина и здоровье')
        CATEGORY = 'Медицина и здоровье'
    elif call.data == '44':
        bot.answer_callback_query(call.id, 'Выбрана категория Иностранные языки для взрослых')
        CATEGORY = 'Иностранные языки для взрослых'
    elif call.data == '45':
        bot.answer_callback_query(call.id, 'Выбрана категория Иностранные языки для детей')
        CATEGORY = 'Иностранные языки для детей'
    elif call.data == '46':
        bot.answer_callback_query(call.id, 'Выбрана категория Художественная литература (ин.языки)')
        CATEGORY = 'Художественная литература (ин.языки)'
    elif call.data == '47':
        bot.answer_callback_query(call.id, 'Выбрана категория Аудиокниги на иностранных языках')
        CATEGORY = 'Аудиокниги на иностранных языках'
    elif call.data == '48':
        bot.answer_callback_query(call.id, 'Выбрана категория Видеоуроки и обучающие интерактивные DVD')
        CATEGORY = 'Видеоуроки и обучающие интерактивные DVD'
    elif call.data == '49':
        bot.answer_callback_query(call.id, 'Выбрана категория Боевые искусства (Видеоуроки)')
        CATEGORY = 'Боевые искусства (Видеоуроки)'
    elif call.data == '50':
        bot.answer_callback_query(call.id, 'Выбрана категория Компьютерные видеоуроки и обучающие интерактивные DVD')
        CATEGORY = 'Компьютерные видеоуроки и обучающие интерактивные DVD'
    elif call.data == '51':
        bot.answer_callback_query(call.id, 'Выбрана категория Радиоспектакли, история, мемуары')
        CATEGORY = 'Радиоспектакли, история, мемуары'
    elif call.data == '52':
        bot.answer_callback_query(call.id, 'Выбрана категория Фантастика, фэнтези, мистика, ужасы, фанфики')
        CATEGORY = 'Фантастика, фэнтези, мистика, ужасы, фанфики'
    elif call.data == '53':
        bot.answer_callback_query(call.id, 'Выбрана категория Религии')
        CATEGORY = 'Религии'
    elif call.data == '54':
        bot.answer_callback_query(call.id, 'Выбрана категория Прочая литература')
        CATEGORY = 'Прочая литература'
    elif call.data == '55':
        bot.answer_callback_query(call.id, 'Выбрана категория Ремонт и эксплуатация транспортных средств')
        CATEGORY = 'Ремонт и эксплуатация транспортных средств'
    elif call.data == '56':
        bot.answer_callback_query(call.id, 'Выбрана категория Фильмы и передачи по авто/мото')
        CATEGORY = 'Фильмы и передачи по авто/мото'
    elif call.data == '57':
        bot.answer_callback_query(call.id, 'Выбрана категория Классическая и современная академическая музыка')
        CATEGORY = 'Классическая и современная академическая музыка'
    elif call.data == '58':
        bot.answer_callback_query(call.id, 'Выбрана категория Фольклор, Народная и Этническая музыка')
        CATEGORY = 'Фольклор, Народная и Этническая музыка'
    elif call.data == '59':
        bot.answer_callback_query(call.id, 'Выбрана категория New Age, Relax, Meditative & Flamenco')
        CATEGORY = 'New Age, Relax, Meditative & Flamenco'
    elif call.data == '60':
        bot.answer_callback_query(call.id, 'Выбрана категория Рэп, Хип-Хоп, R\'n\'B')
        CATEGORY = 'Рэп, Хип-Хоп, R\'n\'B'
    elif call.data == '61':
        bot.answer_callback_query(call.id, 'Выбрана категория Reggae, Ska, Dub')
        CATEGORY = 'Reggae, Ska, Dub'
    elif call.data == '62':
        bot.answer_callback_query(call.id, 'Выбрана категория Саундтреки, караоке и мюзиклы')
        CATEGORY = 'Саундтреки, караоке и мюзиклы'
    elif call.data == '63':
        bot.answer_callback_query(call.id, 'Выбрана категория Шансон, Авторская и Военная песня')
        CATEGORY = 'Шансон, Авторская и Военная песня'
    elif call.data == '64':
        bot.answer_callback_query(call.id, 'Выбрана категория Музыка других жанров')
        CATEGORY = 'Музыка других жанров'
    elif call.data == '65':
        bot.answer_callback_query(call.id, 'Выбрана категория Отечественная поп-музыка')
        CATEGORY = 'Отечественная поп-музыка'
    elif call.data == '66':
        bot.answer_callback_query(call.id, 'Выбрана категория Зарубежная поп-музыка')
        CATEGORY = 'Зарубежная поп-музыка'
    elif call.data == '67':
        bot.answer_callback_query(call.id, 'Выбрана категория Eurodance, Disco, Hi-NRG')
        CATEGORY = 'Eurodance, Disco, Hi-NRG'
    elif call.data == '68':
        bot.answer_callback_query(call.id, 'Выбрана категория Видео, DVD Video, HD Video (поп-музыка)')
        CATEGORY = 'Видео, DVD Video, HD Video (поп-музыка)'
    elif call.data == '69':
        bot.answer_callback_query(call.id, 'Выбрана категория Зарубежный джаз')
        CATEGORY = 'Зарубежный джаз'
    elif call.data == '70':
        bot.answer_callback_query(call.id, 'Выбрана категория Зарубежный блюз')
        CATEGORY = 'Зарубежный блюз'
    elif call.data == '71':
        bot.answer_callback_query(call.id, 'Выбрана категория Отечественный джаз и блюз')
        CATEGORY = 'Отечественный джаз и блюз'
    elif call.data == '72':
        bot.answer_callback_query(call.id, 'Выбрана категория Видео, DVD Video, HD Video (Джаз и блюз)')
        CATEGORY = 'Видео, DVD Video, HD Video (Джаз и блюз)'
    elif call.data == '73':
        bot.answer_callback_query(call.id, 'Выбрана категория Зарубежный Rock')
        CATEGORY = 'Зарубежный Rock'
    elif call.data == '74':
        bot.answer_callback_query(call.id, 'Выбрана категория Зарубежный Metal')
        CATEGORY = 'Зарубежный Metal'
    elif call.data == '75':
        bot.answer_callback_query(call.id, 'Выбрана категория Зарубежные Alternative, Punk, Independent')
        CATEGORY = 'Зарубежные Alternative, Punk, Independent'
    elif call.data == '76':
        bot.answer_callback_query(call.id, 'Выбрана категория Отечественный Rock, Metal')
        CATEGORY = 'Отечественный Rock, Metal'
    elif call.data == '77':
        bot.answer_callback_query(call.id, 'Выбрана категория Видео, DVD Video, HD Video (Рок-музыка)')
        CATEGORY = 'Видео, DVD Video, HD Video (Рок-музыка)'
    elif call.data == '78':
        bot.answer_callback_query(call.id, 'Выбрана категория Trance, Goa Trance, Psy-Trance, PsyChill, Ambient, Dub')
        CATEGORY = 'Trance, Goa Trance, Psy-Trance, PsyChill, Ambient, Dub'
    elif call.data == '79':
        bot.answer_callback_query(call.id, 'Выбрана категория House, Techno, Hardcore, Hardstyle, Jumpstyle')
        CATEGORY = 'House, Techno, Hardcore, Hardstyle, Jumpstyle'
    elif call.data == '80':
        bot.answer_callback_query(call.id, 'Выбрана категория Drum & Bass, Jungle, Breakbeat, Dubstep, IDM, Electro')
        CATEGORY = 'Drum & Bass, Jungle, Breakbeat, Dubstep, IDM, Electro'
    elif call.data == '81':
        bot.answer_callback_query(call.id, 'Выбрана категория Chillout, Lounge, Downtempo, Trip-Hop')
        CATEGORY = 'Chillout, Lounge, Downtempo, Trip-Hop'
    elif call.data == '82':
        bot.answer_callback_query(call.id,
                                  'Выбрана категория Traditional Electronic, Ambient, Modern Classical, Electroacoustic, Ex..')
        CATEGORY = 'Traditional Electronic, Ambient, Modern Classical, Electroacoustic, Ex..'
    elif call.data == '83':
        bot.answer_callback_query(call.id,
                                  'Выбрана категория Industrial, Noise, EBM, Dark Electro, Aggrotech, Synthpop, New Wave')
        CATEGORY = 'Industrial, Noise, EBM, Dark Electro, Aggrotech, Synthpop, New Wave'
    elif call.data == '84':
        bot.answer_callback_query(call.id, 'Выбрана категория Label Packs (lossless)')
        CATEGORY = 'Label Packs (lossless)'
    elif call.data == '85':
        bot.answer_callback_query(call.id, 'Выбрана категория Label packs, Scene packs (lossy)')
        CATEGORY = 'Label packs, Scene packs (lossy)'
    elif call.data == '86':
        bot.answer_callback_query(call.id, 'Выбрана категория Электронная музыка (Видео, DVD Video, HD Video)')
        CATEGORY = 'Электронная музыка (Видео, DVD Video, HD Video)'
    elif call.data == '87':
        bot.answer_callback_query(call.id, 'Выбрана категория Hi-Res stereo и многоканальная музыка')
        CATEGORY = 'Hi-Res stereo и многоканальная музыка'
    elif call.data == '88':
        bot.answer_callback_query(call.id, 'Выбрана категория Оцифровки с аналоговых носителей')
        CATEGORY = 'Оцифровки с аналоговых носителей'
    elif call.data == '89':
        bot.answer_callback_query(call.id, 'Выбрана категория Неофициальные конверсии цифровых форматов')
        CATEGORY = 'Неофициальные конверсии цифровых форматов'
    elif call.data == '90':
        bot.answer_callback_query(call.id, 'Выбрана категория Игры для Windows')
        CATEGORY = 'Игры для Windows'
    elif call.data == '91':
        bot.answer_callback_query(call.id, 'Выбрана категория Прочее для Windows-игр')
        CATEGORY = 'Прочее для Windows-игр'
    elif call.data == '92':
        bot.answer_callback_query(call.id, 'Выбрана категория Прочее для Microsoft Flight Simulator, Prepar3D, X-Plane')
        CATEGORY = 'Прочее для Microsoft Flight Simulator, Prepar3D, X-Plane'
    elif call.data == '93':
        bot.answer_callback_query(call.id, 'Выбрана категория Игры для Macintosh')
        CATEGORY = 'Игры для Macintosh'
    elif call.data == '94':
        bot.answer_callback_query(call.id, 'Выбрана категория Игры для Linux')
        CATEGORY = 'Игры для Linux'
    elif call.data == '95':
        bot.answer_callback_query(call.id, 'Выбрана категория Игры для консолей')
        CATEGORY = 'Игры для консолей'
    elif call.data == '96':
        bot.answer_callback_query(call.id, 'Выбрана категория Видео для консолей')
        CATEGORY = 'Видео для консолей'
    elif call.data == '97':
        bot.answer_callback_query(call.id, 'Выбрана категория Игры для мобильных устройств')
        CATEGORY = 'Игры для мобильных устройств'
    elif call.data == '98':
        bot.answer_callback_query(call.id, 'Выбрана категория Игровое видео')
        CATEGORY = 'Игровое видео'
    elif call.data == '99':
        bot.answer_callback_query(call.id, 'Выбрана категория Операционные системы от Microsoft')
        CATEGORY = 'Операционные системы от Microsoft'
    elif call.data == '100':
        bot.answer_callback_query(call.id, 'Выбрана категория Linux, Unix и другие ОС')
        CATEGORY = 'Linux, Unix и другие ОС'
    elif call.data == '101':
        bot.answer_callback_query(call.id, 'Выбрана категория Тестовые диски для настройки аудио/видео аппаратуры')
        CATEGORY = 'Тестовые диски для настройки аудио/видео аппаратуры'
    elif call.data == '102':
        bot.answer_callback_query(call.id, 'Выбрана категория Системные программы')
        CATEGORY = 'Системные программы'
    elif call.data == '103':
        bot.answer_callback_query(call.id, 'Выбрана категория Системы для бизнеса, офиса, научной и проектной работы')
        CATEGORY = 'Системы для бизнеса, офиса, научной и проектной работы'
    elif call.data == '104':
        bot.answer_callback_query(call.id, 'Выбрана категория Веб-разработка и Программирование')
        CATEGORY = 'Веб-разработка и Программирование'
    elif call.data == '105':
        bot.answer_callback_query(call.id, 'Выбрана категория Программы для работы с мультимедиа и 3D')
        CATEGORY = 'Программы для работы с мультимедиа и 3D'
    elif call.data == '106':
        bot.answer_callback_query(call.id, 'Выбрана категория Материалы для мультимедиа и дизайна')
        CATEGORY = 'Материалы для мультимедиа и дизайна'
    elif call.data == '107':
        bot.answer_callback_query(call.id, 'Выбрана категория ГИС, системы навигации и карты')
        CATEGORY = 'ГИС, системы навигации и карты'
    elif call.data == '108':
        bot.answer_callback_query(call.id, 'Выбрана категория Приложения для мобильных устройств')
        CATEGORY = 'Приложения для мобильных устройств'
    elif call.data == '109':
        bot.answer_callback_query(call.id, 'Выбрана категория Видео для мобильных устройств')
        CATEGORY = 'Видео для мобильных устройств'
    elif call.data == '110':
        bot.answer_callback_query(call.id, 'Выбрана категория Apple Macintosh')
        CATEGORY = 'Apple Macintosh'
    elif call.data == '111':
        bot.answer_callback_query(call.id, 'Выбрана категория iOS')
        CATEGORY = 'iOS'
    elif call.data == '112':
        bot.answer_callback_query(call.id, 'Выбрана категория Видео')
        CATEGORY = 'Видео'
    elif call.data == '113':
        bot.answer_callback_query(call.id, 'Выбрана категория Видео HD')
        CATEGORY = 'Видео HD'
    elif call.data == '114':
        bot.answer_callback_query(call.id, 'Выбрана категория Аудио')
        CATEGORY = 'Аудио'
    elif call.data == '115':
        bot.answer_callback_query(call.id, 'Выбрана категория Разное (раздачи)')
        CATEGORY = 'Разное (раздачи)'
    elif call.data == '116':
        bot.answer_callback_query(call.id, 'Выбрана категория Тестовый форум')
        CATEGORY = 'Тестовый форум'
    elif call.data == '117':
        bot.answer_callback_query(call.id, 'Выбрана категория Отчеты о встречах')
        CATEGORY = 'Отчеты о встречах'




@bot.message_handler(commands=['start'])
def start(message):
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
    send = bot.send_message(message.from_user.id, introduction, reply_markup=keyboard)
    # bot.register_next_step_handler(send, second)

@bot.message_handler(commands=['instruction'])
def instruction(message):
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

    send = bot.send_message(message.from_user.id, instruction, reply_markup=keyboard)
    # bot.register_next_step_handler(send, second)


@bot.message_handler(commands=['categories58'])
def first_categories(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.row_width = 1

    keyboard.add(InlineKeyboardButton('Rutracker Awards (мероприятия и конкурсы)', callback_data='0'),
                 InlineKeyboardButton('Зарубежное кино', callback_data='1'),
                 InlineKeyboardButton('Наше кино', callback_data='2'),
                 InlineKeyboardButton('Арт-хаус и авторское кино', callback_data='3'),
                 InlineKeyboardButton('Театр', callback_data='4'),
                 InlineKeyboardButton('DVD Video', callback_data='5'),
                 InlineKeyboardButton('HD Video', callback_data='6'),
                 InlineKeyboardButton('3D/Стерео Кино, Видео, TV и Спорт', callback_data='7'),
                 InlineKeyboardButton('Мультфильмы', callback_data='8'),
                 InlineKeyboardButton('Мультсериалы', callback_data='9'),
                 InlineKeyboardButton('Аниме', callback_data='10'),
                 InlineKeyboardButton('Русские сериалы', callback_data='11'),
                 InlineKeyboardButton('Зарубежные сериалы', callback_data='12'),
                 InlineKeyboardButton('Зарубежные сериалы (HD Video)', callback_data='13'),
                 InlineKeyboardButton('Сериалы Латинской Америки, Турции и Индии', callback_data='14'),
                 InlineKeyboardButton('Азиатские сериалы', callback_data='15'),
                 InlineKeyboardButton('Вера и религия', callback_data='16'),
                 InlineKeyboardButton('Документальные фильмы и телепередачи', callback_data='17'),
                 InlineKeyboardButton('Документальные (HD Video)', callback_data='18'),
                 InlineKeyboardButton('Развлекательные телепередачи и шоу, приколы и юмор', callback_data='19'),
                 InlineKeyboardButton('Зимние Олимпийские игры 2018', callback_data='20'),
                 InlineKeyboardButton('Спортивные турниры, фильмы и передачи', callback_data='21'),
                 InlineKeyboardButton('⚽ Футбол', callback_data='22'),
                 InlineKeyboardButton('🏀 Баскетбол', callback_data='23'),
                 InlineKeyboardButton('🏒 Хоккей', callback_data='24'),
                 InlineKeyboardButton('Рестлинг', callback_data='25'),
                 InlineKeyboardButton('Сканирование, обработка сканов', callback_data='26'),
                 InlineKeyboardButton('Книги и журналы (общий раздел)', callback_data='27'),
                 InlineKeyboardButton('Для детей, родителей и учителей', callback_data='28'),
                 InlineKeyboardButton('Спорт, физическая культура, боевые искусства', callback_data='29'),
                 InlineKeyboardButton('Гуманитарные науки', callback_data='30'),
                 InlineKeyboardButton('Исторические науки', callback_data='31'),
                 InlineKeyboardButton('Точные, естественные и инженерные науки', callback_data='32'),
                 InlineKeyboardButton('Ноты и Музыкальная литература', callback_data='33'),
                 InlineKeyboardButton('Военное дело', callback_data='34'),
                 InlineKeyboardButton('Психология', callback_data='35'),
                 InlineKeyboardButton('Коллекционирование, увлечения и хобби', callback_data='36'),
                 InlineKeyboardButton('Художественная литература', callback_data='37'),
                 InlineKeyboardButton('Компьютерная литература', callback_data='38'),
                 InlineKeyboardButton('Комиксы, манга, ранобэ', callback_data='39'),
                 InlineKeyboardButton('Коллекции книг и библиотеки', callback_data='40'),
                 InlineKeyboardButton('Мультимедийные и интерактивные издания', callback_data='41'),
                 InlineKeyboardButton('Медицина и здоровье', callback_data='42'),
                 InlineKeyboardButton('Иностранные языки для взрослых', callback_data='43'),
                 InlineKeyboardButton('Иностранные языки для детей', callback_data='44'),
                 InlineKeyboardButton('Художественная литература (ин.языки)', callback_data='45'),
                 InlineKeyboardButton('Аудиокниги на иностранных языках', callback_data='46'),
                 InlineKeyboardButton('Видеоуроки и обучающие интерактивные DVD', callback_data='47'),
                 InlineKeyboardButton('Боевые искусства (Видеоуроки)', callback_data='48'),
                 InlineKeyboardButton('Компьютерные видеоуроки и обучающие интерактивные DVD', callback_data='49'),
                 InlineKeyboardButton('Радиоспектакли, история, мемуары', callback_data='50'),
                 InlineKeyboardButton('Фантастика, фэнтези, мистика, ужасы, фанфики', callback_data='51'),
                 InlineKeyboardButton('Религии', callback_data='52'),
                 InlineKeyboardButton('Прочая литература', callback_data='53'),
                 InlineKeyboardButton('Ремонт и эксплуатация транспортных средств', callback_data='54'),
                 InlineKeyboardButton('Фильмы и передачи по авто/мото', callback_data='55'),
                 InlineKeyboardButton('Классическая и современная академическая музыка', callback_data='56'),
                 InlineKeyboardButton('Фольклор, Народная и Этническая музыка', callback_data='57'),
                 InlineKeyboardButton('New Age, Relax, Meditative & Flamenco', callback_data='58'),
                 InlineKeyboardButton('Еще категории', callback_data='e1'),
                 InlineKeyboardButton('Меню', callback_data='m')
                 )
    send = bot.send_message(message.from_user.id, 'Выберите категорию из списка', reply_markup=keyboard)
    # bot.register_next_step_handler(send, second)

@bot.message_handler(commands=['categories117'])
def second_categories(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.row_width = 1

    keyboard.add(InlineKeyboardButton('Рэп, Хип-Хоп, R\'n\'B', callback_data='59'),
                 InlineKeyboardButton('Reggae, Ska, Dub', callback_data='60'),
                 InlineKeyboardButton('Саундтреки, караоке и мюзиклы', callback_data='61'),
                 InlineKeyboardButton('Шансон, Авторская и Военная песня', callback_data='62'),
                 InlineKeyboardButton('Музыка других жанров', callback_data='63'),
                 InlineKeyboardButton('Отечественная поп-музыка', callback_data='64'),
                 InlineKeyboardButton('Зарубежная поп-музыка', callback_data='65'),
                 InlineKeyboardButton('Eurodance, Disco, Hi-NRG', callback_data='66'),
                 InlineKeyboardButton('Видео, DVD Video, HD Video (поп-музыка)', callback_data='67'),
                 InlineKeyboardButton('Зарубежный джаз', callback_data='68'),
                 InlineKeyboardButton('Зарубежный блюз', callback_data='69'),
                 InlineKeyboardButton('Отечественный джаз и блюз', callback_data='70'),
                 InlineKeyboardButton('Видео, DVD Video, HD Video (Джаз и блюз)', callback_data='71'),
                 InlineKeyboardButton('Зарубежный Rock', callback_data='72'),
                 InlineKeyboardButton('Зарубежный Metal', callback_data='73'),
                 InlineKeyboardButton('Зарубежные Alternative, Punk, Independent', callback_data='74'),
                 InlineKeyboardButton('Отечественный Rock, Metal', callback_data='75'),
                 InlineKeyboardButton('Видео, DVD Video, HD Video (Рок-музыка)', callback_data='76'),
                 InlineKeyboardButton('Trance, Goa Trance, Psy-Trance, PsyChill, Ambient, Dub', callback_data='77'),
                 InlineKeyboardButton('House, Techno, Hardcore, Hardstyle, Jumpstyle', callback_data='78'),
                 InlineKeyboardButton('Drum & Bass, Jungle, Breakbeat, Dubstep, IDM, Electro', callback_data='79'),
                 InlineKeyboardButton('Chillout, Lounge, Downtempo, Trip-Hop', callback_data='80'),
                 InlineKeyboardButton('Traditional Electronic, Ambient, Modern Classical, Electroacoustic, Ex..', callback_data='81'),
                 InlineKeyboardButton('Industrial, Noise, EBM, Dark Electro, Aggrotech, Synthpop, New Wave', callback_data='82'),
                 InlineKeyboardButton('Label Packs (lossless)', callback_data='83'),
                 InlineKeyboardButton('Label packs, Scene packs (lossy)', callback_data='84'),
                 InlineKeyboardButton('Электронная музыка (Видео, DVD Video, HD Video)', callback_data='85'),
                 InlineKeyboardButton('Hi-Res stereo и многоканальная музыка', callback_data='86'),
                 InlineKeyboardButton('Оцифровки с аналоговых носителей', callback_data='87'),
                 InlineKeyboardButton('Неофициальные конверсии цифровых форматов', callback_data='88'),
                 InlineKeyboardButton('Игры для Windows', callback_data='89'),
                 InlineKeyboardButton('Прочее для Windows-игр', callback_data='90'),
                 InlineKeyboardButton('Прочее для Microsoft Flight Simulator, Prepar3D, X-Plane', callback_data='91'),
                 InlineKeyboardButton('Игры для Macintosh', callback_data='92'),
                 InlineKeyboardButton('Игры для Linux', callback_data='93'),
                 InlineKeyboardButton('Игры для консолей', callback_data='94'),
                 InlineKeyboardButton('Видео для консолей', callback_data='95'),
                 InlineKeyboardButton('Игры для мобильных устройств', callback_data='96'),
                 InlineKeyboardButton('Игровое видео', callback_data='97'),
                 InlineKeyboardButton('Операционные системы от Microsoft', callback_data='98'),
                 InlineKeyboardButton('Linux, Unix и другие ОС', callback_data='99'),
                 InlineKeyboardButton('Тестовые диски для настройки аудио/видео аппаратуры', callback_data='100'),
                 InlineKeyboardButton('Системные программы', callback_data='101'),
                 InlineKeyboardButton('Системы для бизнеса, офиса, научной и проектной работы', callback_data='102'),
                 InlineKeyboardButton('Веб-разработка и Программирование', callback_data='103'),
                 InlineKeyboardButton('Программы для работы с мультимедиа и 3D', callback_data='104'),
                 InlineKeyboardButton('Материалы для мультимедиа и дизайна', callback_data='105'),
                 InlineKeyboardButton('ГИС, системы навигации и карты', callback_data='106'),
                 InlineKeyboardButton('Приложения для мобильных устройств', callback_data='107'),
                 InlineKeyboardButton('Видео для мобильных устройств', callback_data='108'),
                 InlineKeyboardButton('Apple Macintosh', callback_data='109'),
                 InlineKeyboardButton('iOS', callback_data='110'),
                 InlineKeyboardButton('Видео', callback_data='111'),
                 InlineKeyboardButton('Видео HD', callback_data='112'),
                 InlineKeyboardButton('Аудио', callback_data='113'),
                 InlineKeyboardButton('Разное (раздачи)', callback_data='114'),
                 InlineKeyboardButton('Тестовый форум', callback_data='115'),
                 InlineKeyboardButton('Еще категории', callback_data='e2'),
                 InlineKeyboardButton('Меню', callback_data='m')
                 )
    send = bot.send_message(message.from_user.id, 'Выберите категорию из списка', reply_markup=keyboard)
    # bot.register_next_step_handler(send, second)

@bot.message_handler(commands=['subcategories'])
def subcategories(message):
    global SUBCATEGORY
    if CATEGORY == None:
        text = """Сперва необходимо выбрать категорию. Сделать это можно из меню по команде /start или с помощью \
        команд /categories58 и /categories117"""
        send = bot.send_message(message.from_user.id, text)
        bot.register_next_step_handler(send, first_categories)
    send = bot.send_message(message.from_user.id, 'Здесь будет раелизован выбор подкатегории'.format(CATEGORY))
    bot.register_next_step_handler(send, targetsearch)


@bot.message_handler(commands=['globalsearch'])
def globalsearch(message):
    send = bot.send_message(message.from_user.id, 'Здесь будет реализован глобальный поиск')


@bot.message_handler(commands=['targetsearch'])
def targetsearch(message):
    send = bot.send_message(message.from_user.id, 'Здесь будет реализован поиск по категориям')



if __name__ == '__main__':
    bot.polling(none_stop=True)
