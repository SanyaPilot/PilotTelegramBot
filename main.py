import telebot
from telebot import types
import requests
import json
import sqlite3
import time
from threading import Timer
import googletrans
from googletrans import Translator
from geopy.geocoders import Nominatim

import kick as Kick
import ban as Ban
import note as Note
import perms as Perms
import mute as Mute

bot = telebot.TeleBot('1073948237:AAGKs3HzRBZwBZGkoQ5moJIakWQn39nQtX4')

conn = sqlite3.connect('data.db')
curs = conn.cursor()

table = """ CREATE TABLE IF NOT EXISTS notes (
                id integer PRIMARY KEY,
                name text NOT NULL,
                message_id integer NOT NULL,
                chat_id integer NOT NULL
            ); """
curs.execute(table)
conn.commit()
conn.close()

translator = Translator()

geolocator = Nominatim(user_agent="sanya_pilot_telegram_bot")

timers = {}
forecasts = {}


@bot.message_handler(commands=['start'])
def command_handler(message):
    bot.send_message(message.chat.id, 'Приветствую) Я бот-админ для чата.\nСправку по'
                                      ' командам можно получить по команде /help@sanya_pilot_bot\nЕсли что-то не '
                                      'работает, пните @alexander_baransky496\n')


@bot.message_handler(commands=['help'])
def show_help(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Список команд:\n'
                          '/tr - Перевести сообщение. /tr <код языка, на который надо перевести>'
                          '/notes - Показать список заметок\n'
                          '/note - Просмотр заметки\n'
                          '/addnote - Добавить заметку\n'
                          '/delnote - Удалить заметку\n'
                          '/mute - Мут навсегда (до размута)\n'
                          '/tmute - Мут на время. Время прописывается в формате <кол-во><s/m/h/d>\n'
                          '/unmute - Размут\n'
                          '/ban - Забанить пользователя навсегда (до разбана)\n'
                          '/banme - Забанить пользователя, написавшего команду\n'
                          '/tban - Забанить пользователя на время. Формат такой же как в /tmute\n'
                          '/unban - Разбан\n'
                          '/kick - Кикнуть пользователя\n'
                          '/kickme - Кикнуть пользователя, написавшего команду\n'
                          '/restrict - Лишение пользователя всех прав\n'
                          '/permit - Выдача пользователю всех прав\n'
                          '/dpermit - Выдача пользователю дефолтных прав чата\n'
                          '/demote - Лишение пользователя всех административных прав (пока не работает)\n'
                          '/promote - Выдача пользователю всех административных прав (пока не работает)\n'
                          '/weather - Показать текущую погоду. /weather <название города>'
                          'Чтобы применить все эти команды, необходимо ответить командой на сообщение пользователя, '
                          'которого вы хотите кикнуть, забанить и т. д.')


# Мут навсегда
@bot.message_handler(commands=['mute'])
def mute_wrapper(message):
    Mute.mute(message)


# Мут на время
@bot.message_handler(commands=['tmute'])
def tmute_wrapper(message):
    Mute.tmute(message)


# Размут
@bot.message_handler(commands=['unmute'])
def unmute_wrapper(message):
    Mute.unmute(message)


@bot.message_handler(commands=['restrict'])
def restrict_wrapper(message):
    Perms.restrict(message)


@bot.message_handler(commands=['permit'])
def permit_wrapper(message):
    Perms.permit(message)


@bot.message_handler(commands=['dpermit'])
def permit_default_wrapper(message):
    Perms.permit_default(message)


# Убрать все права
@bot.message_handler(commands=['demote'])
def demote_wrapper(message):
    Perms.demote(message)


# Дать все права
@bot.message_handler(commands=['promote'])
def promote_wrapper(message):
    Perms.promote(message)


@bot.message_handler(commands=['kick'])
def kick_wrapper(message):
    Kick.kick(message)


@bot.message_handler(commands=['kickme'])
def kickme_wrapper(message):
    Kick.kickme(message)


@bot.message_handler(commands=['ban'])
def ban_wrapper(message):
    Ban.ban(message)


@bot.message_handler(commands=['banme'])
def banme_wrapper(message):
    Ban.banme(message)


@bot.message_handler(commands=['tban'])
def tban_wrapper(message):
    Ban.tban(message)


@bot.message_handler(commands=['unban'])
def unban_wrapper(message):
    Ban.unban(message)


@bot.message_handler(commands=['notes'])
def notes_wrapper(message):
    Note.notes(message)


@bot.message_handler(commands=['note'])
def note_wrapper(message):
    Note.note(message)


@bot.message_handler(commands=['addnote'])
def addnote_wrapper(message):
    Note.addnote(message)


@bot.message_handler(commands=['delnote'])
def delnote_wrapper(message):
    Note.delnote(message)


@bot.message_handler(commands=['tr'])
def tr(message):
    try:
        lang_code = message.text[4:]
        result = translator.translate(message.reply_to_message.text, dest=lang_code)

        langs = googletrans.LANGUAGES
        text = '<i>Перевод с <b>' + langs[result.src] + '</b> на <b>' + langs[lang_code] + '</b>\n'
        text += 'Translate from <b>' + langs[result.src] + '</b> to <b>' + langs[
            lang_code] + '</b></i>\n\n' + result.text
        bot.send_message(chat_id=message.chat.id,
                         reply_to_message_id=message.message_id,
                         parse_mode='HTML',
                         text=text)
    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['weather'])
def weather(message):
    try:
        city_name = message.text[9:]
        loc = geolocator.geocode(city_name)
        if loc is None:
            bot.reply_to(message, 'Такой город не найден')
        else:
            response = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + str(loc.latitude) +
                                    '&lon=' + str(loc.longitude) + '&appid=c1c0032b6ff3be83e44ab641e780fc3d&lang=RU' +
                                    '&units=metric')

            data = json.loads(response.content)
            destination = loc.address.split(',')

            text = '<b><i>Погода в '
            for i in destination:
                if i == destination[0]:
                    text += i
                else:
                    text += ',' + i

            text += '</i></b>\n'
            text += '━━━━━━━━━━━━━━━━━━━━━━━\n'
            text += '<b>Текущая погода</b>\n'
            text += '━━━━━━━━━━━━━━━━━━━━━━━\n'
            text += '<b>' + str(data['current']['temp']) + ' °C <i>' + data['current']['weather'][0]['description'].capitalize() + '</i></b>\n'
            text += '<i>Чувствуется как:</i> <b>' + str(data['current']['feels_like']) + ' °C</b>\n'
            text += '<i>Влажность:</i> <b>' + str(data['current']['humidity']) + '%</b>\n'
            text += '<i>Давление:</i> <b>' + str(data['current']['pressure']) + ' гПа</b>\n'
            text += '<i>Скорость ветра:</i> <b>' + str(data['current']['wind_speed']) + ' м/с</b>\n'
            text += '<i>Облачность:</i> <b>' + str(data['current']['clouds']) + '%</b>\n'
            text += '<i>UV индекс:</i> <b>' + str(data['current']['uvi']) + '</b>\n'

            bot.send_message(chat_id=message.chat.id,
                             text=text,
                             reply_to_message_id=message.message_id,
                             parse_mode='HTML')
    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['forecast'])
def forecast(message):
    try:
        city_name = message.text[9:]
        loc = geolocator.geocode(city_name)
        if loc is None:
            bot.reply_to(message, 'Такой город не найден')
        else:
            forecast_message = bot.send_message(chat_id=message.chat.id,
                                                text='Готовлю прогноз погоды для Вас)',
                                                reply_to_message_id=message.message_id)

            global forecasts
            forecasts[forecast_message.message_id] = []

            response = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + str(loc.latitude) +
                                    '&lon=' + str(loc.longitude) + '&appid=c1c0032b6ff3be83e44ab641e780fc3d&lang=RU' +
                                    '&units=metric')

            data = json.loads(response.content)
            destination = loc.address.split(',')

            for i in range(8):
                text = '<b><i>Погода в '
                for j in destination:
                    if j == destination[0]:
                        text += j
                    else:
                        text += ',' + j

                text += '</i></b>\n'
                text += '━━━━━━━━━━━━━━━━━━━━━━━\n'
                text += '<b>Прогноз на ' + time.strftime("%d/%m", time.gmtime(data['daily'][i]['dt'])) + '</b>\n'
                text += '━━━━━━━━━━━━━━━━━━━━━━━\n'
                text += '<b>' + str(data['daily'][i]['temp']['day']) + ' °C <i>' + data['daily'][i]['weather'][0]['description'].capitalize() + '</i></b>\n'
                text += '<i>Мин. температура:</i> <b>' + str(data['daily'][i]['temp']['min']) + ' °C</b>\n'
                text += '<i>Макс. температура:</i> <b>' + str(data['daily'][i]['temp']['max']) + ' °C</b>\n'
                text += '<i>Температура утром:</i> <b>' + str(data['daily'][i]['temp']['morn']) + ' °C</b>\n'
                text += '<i>Температура вечером:</i> <b>' + str(data['daily'][i]['temp']['eve']) + ' °C</b>\n'
                text += '<i>Температура ночью:</i> <b>' + str(data['daily'][i]['temp']['night']) + ' °C</b>\n'
                text += '<i>Влажность:</i> <b>' + str(data['daily'][i]['humidity']) + '%</b>\n'
                text += '<i>Давление:</i> <b>' + str(data['daily'][i]['pressure']) + ' гПа</b>\n'
                text += '<i>Скорость ветра:</i> <b>' + str(data['daily'][i]['wind_speed']) + ' м/с</b>\n'
                text += '<i>Облачность:</i> <b>' + str(data['daily'][i]['clouds']) + '%</b>\n'
                text += '<i>UV индекс:</i> <b>' + str(data['daily'][i]['uvi']) + '</b>'

                forecasts[forecast_message.message_id].append(text)

            forecasts[forecast_message.message_id].append(0)
            forecasts[forecast_message.message_id].append(message.from_user.id)

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            key_prev = types.InlineKeyboardButton(text='<<', callback_data='forecast_prev')
            key_next = types.InlineKeyboardButton(text='>>', callback_data='forecast_next')
            keyboard.add(key_prev, key_next)
            key_close = types.InlineKeyboardButton(text='Я прочитал', callback_data='forecast_close')
            keyboard.add(key_close)

            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=forecast_message.message_id,
                                  text=forecasts[forecast_message.message_id][0],
                                  parse_mode='HTML',
                                  reply_markup=keyboard)

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    try:
        if message.text[0] == '#':
            name = message.text[1:]
            conn = sqlite3.connect('data.db')
            curs = conn.cursor()
            cmd = """ SELECT message_id FROM notes
                      WHERE name = ?
                      AND chat_id = ?"""
            curs.execute(cmd, (name,message.chat.id))
            rows = curs.fetchall()
            conn.close()

            row = rows[0]
            bot.forward_message(message.chat.id, message.chat.id, row[0])

    except Exception:
        pass


# Триггер на нового юзера в чате
@bot.message_handler(content_types=['new_chat_members'])
def greeting(message):
    if not message.from_user.is_bot:
        text = 'Привет, как дела?\nЗдесь мы осуждаем телефон LeEco Le 2 (ну или не совсем)\nВ общем не '
        text += 'разжигай холивары и все будет ок)\n\nНо перед тем как ты вступишь в чат, нам нужно проверить,'
        text += ' действительно ли ты не бот. Для этого нужно нажать на кнопку, я думаю ты справишся\n\n'
        text += '<i><b>Ограничение по времени: 5 минут.\n'
        text += 'Если по истечении времени не была нажата кнопка, ты получаешь кик</b></i>'

        keyboard = types.InlineKeyboardMarkup()
        key = types.InlineKeyboardButton(text='Я хочу общатся!', callback_data='captcha_ok')
        keyboard.add(key)

        bot.send_message(chat_id=message.chat.id,
                         reply_to_message_id=message.message_id,
                         parse_mode='HTML',
                         text=text,
                         reply_markup=keyboard)

        global timers
        timers[message.from_user.id] = Timer(300.0, kick_bot, [message.chat.id, message.from_user.id])
        timers[message.from_user.id].start()


# Триггер на уход юзера из чата
@bot.message_handler(content_types=['left_chat_member'])
def greeting(message):
    bot.reply_to(message, text='Ну ладно, пока( *хнык*')


@bot.callback_query_handler(func=lambda call: True)
def button_callback_handler(call):
    global forecasts
    try:
        if call.data == 'captcha_ok':
            global timers
            try:
                timers[call.from_user.id].cancel()
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text='Вы успешно прошли проверку!')
                timers.pop(call.from_user.id)
            except KeyError:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text='Нельзя проходить проверку за другого пользователя')

        elif call.data == 'forecast_prev':
            if call.from_user.id == forecasts[call.message.message_id][9]:
                if not forecasts[call.message.message_id][8] <= 0:
                    forecasts[call.message.message_id][8] -= 1
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    key_prev = types.InlineKeyboardButton(text='<<', callback_data='forecast_prev')
                    key_next = types.InlineKeyboardButton(text='>>', callback_data='forecast_next')
                    keyboard.add(key_prev, key_next)
                    key_close = types.InlineKeyboardButton(text='Я прочитал', callback_data='forecast_close')
                    keyboard.add(key_close)

                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          text=forecasts[call.message.message_id][forecasts[call.message.message_id][8]],
                                          parse_mode='HTML',
                                          reply_markup=keyboard)
                else:
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Это начало списка')
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text='Нельзя управлять меню прогноза погоды другого пользователя')

        elif call.data == 'forecast_next':
            if call.from_user.id == forecasts[call.message.message_id][9]:
                if not forecasts[call.message.message_id][8] >= 7:
                    forecasts[call.message.message_id][8] += 1
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    key_prev = types.InlineKeyboardButton(text='<<', callback_data='forecast_prev')
                    key_next = types.InlineKeyboardButton(text='>>', callback_data='forecast_next')
                    keyboard.add(key_prev, key_next)
                    key_close = types.InlineKeyboardButton(text='Я прочитал', callback_data='forecast_close')
                    keyboard.add(key_close)

                    bot.edit_message_text(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          text=forecasts[call.message.message_id][
                                              forecasts[call.message.message_id][8]],
                                          parse_mode='HTML',
                                          reply_markup=keyboard)
                else:
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text='Это конец списка')
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text='Нельзя управлять меню прогноза погоды другого пользователя')

        elif call.data == 'forecast_close':
            if call.from_user.id == forecasts[call.message.message_id][9]:
                forecasts.pop(call.message.message_id)
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text='Нельзя управлять меню прогноза погоды другого пользователя')
    except Exception:
        bot.reply_to(call.message, 'Упс... Что-то пошло не так')


def kick_bot(chat_id, user_id):
    try:
        bot.kick_chat_member(chat_id=chat_id,
                             user_id=user_id,
                             until_date=0)

        bot.unban_chat_member(chat_id=chat_id,
                              user_id=user_id)

        chat_member = bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        user = chat_member.user
        bot.send_message(chat_id=chat_id,
                         text='Пользователь @' + str(user.username) +
                              ' не прошел проверку на бота\nОн был кикнут')
        global timers
        timers.pop(user_id)

    except Exception:
        bot.send_message(chat_id=chat_id, text='Упс... Что-то пошло не так')


bot.polling()
