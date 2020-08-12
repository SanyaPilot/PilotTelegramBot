import telebot
from telebot import types
import sqlite3
from threading import Timer

import kick as Kick
import ban as Ban
import note as Note
import perms as Perms
import mute as Mute
import translate
import introduction
import weather as Weather

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

timers = {}


@bot.message_handler(commands=['start'])
def start_wrapper(message):
    introduction.start(message)


@bot.message_handler(commands=['help'])
def help_wrapper(message):
    introduction.help(message)


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
def tr_wrapper(message):
    translate.tr(message)


@bot.message_handler(commands=['weather'])
def weather_wrapper(message):
    Weather.weather(message)


@bot.message_handler(commands=['forecast'])
def forecast_wrapper(message):
    Weather.forecast(message)


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

        if 'forecast' in call.data:
            Weather.call_handler(call)
    
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
