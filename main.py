import telebot
import sqlite3

import config
from modules import introduction, translate, ban, greeting, kick, messages, mute, note, perms, weather, admin
from translation import tw

bot = telebot.TeleBot(config.token)

conn = sqlite3.connect('data.db')
curs = conn.cursor()

table = """ CREATE TABLE IF NOT EXISTS notes (
                id integer PRIMARY KEY,
                name text NOT NULL,
                message_id integer NOT NULL,
                chat_id integer NOT NULL
            ); """
curs.execute(table)

table = """ CREATE TABLE IF NOT EXISTS chats (
                id integer PRIMARY KEY,
                chat_id integer NOT NULL,
                setup_is_finished integer NOT NULL,
                greeting text,
                leave_msg text,
                language text
            ); """
curs.execute(table)
conn.commit()
conn.close()


@bot.message_handler(commands=['start'])
def start_wrapper(message):
    introduction.start(message)


@bot.message_handler(commands=['help'])
def help_wrapper(message):
    introduction.help(message)


# Мут навсегда
@bot.message_handler(commands=['mute'])
def mute_wrapper(message):
    mute.mute(message)


# Размут
@bot.message_handler(commands=['unmute'])
def unmute_wrapper(message):
    mute.unmute(message)


@bot.message_handler(commands=['restrict'])
def restrict_wrapper(message):
    perms.restrict(message)


@bot.message_handler(commands=['permit'])
def permit_wrapper(message):
    perms.permit(message)


@bot.message_handler(commands=['dpermit'])
def permit_default_wrapper(message):
    perms.permit_default(message)


# Убрать все права
@bot.message_handler(commands=['demote'])
def demote_wrapper(message):
    perms.demote(message)


# Дать все права
@bot.message_handler(commands=['promote'])
def promote_wrapper(message):
    perms.promote(message)


@bot.message_handler(commands=['kick'])
def kick_wrapper(message):
    kick.kick(message)


@bot.message_handler(commands=['kickme'])
def kickme_wrapper(message):
    kick.kickme(message)


@bot.message_handler(commands=['ban'])
def ban_wrapper(message):
    ban.ban(message)


@bot.message_handler(commands=['banme'])
def banme_wrapper(message):
    ban.banme(message)


@bot.message_handler(commands=['tban'])
def tban_wrapper(message):
    ban.tban(message)


@bot.message_handler(commands=['unban'])
def unban_wrapper(message):
    ban.unban(message)


@bot.message_handler(commands=['notes'])
def notes_wrapper(message):
    note.notes(message)


@bot.message_handler(commands=['note'])
def note_wrapper(message):
    note.note(message)


@bot.message_handler(commands=['addnote'])
def addnote_wrapper(message):
    note.addnote(message)


@bot.message_handler(commands=['delnote'])
def delnote_wrapper(message):
    note.delnote(message)


@bot.message_handler(commands=['tr'])
def tr_wrapper(message):
    translate.tr(message)


@bot.message_handler(commands=['weather'])
def weather_wrapper(message):
    weather.weather(message)


@bot.message_handler(commands=['forecast'])
def forecast_wrapper(message):
    weather.forecast(message)


@bot.message_handler(commands=['purge'])
def purge_wrapper(message):
    messages.purge(message)


@bot.message_handler(commands=['setgreeting'])
def set_greeting(message):
    greeting.set_greeting(message)


@bot.message_handler(commands=['rmgreeting'])
def rm_greeting(message):
    greeting.rm_greeting(message)


@bot.message_handler(commands=['setleavemsg'])
def rm_user_leave_msg(message):
    greeting.set_user_leave_msg(message)


@bot.message_handler(commands=['rmleavemsg'])
def rm_greeting(message):
    greeting.rm_user_leave_msg(message)


@bot.message_handler(commands=['broadcast'])
def broadcast_wrapper(message):
    admin.broadcast(message)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    try:
        if message.text[0] == '#':
            note.text_handler(message)

    except Exception:
        pass


# Триггер на нового юзера в чате
@bot.message_handler(content_types=['new_chat_members'])
def greeting_wrapper(message):
    greeting.greeting(message)


# Триггер на уход юзера из чата
@bot.message_handler(content_types=['left_chat_member'])
def user_leave_msg_wrapper(message):
    greeting.user_leave_msg(message)


@bot.callback_query_handler(func=lambda call: True)
def button_callback_handler(call):
    trans = tw.get_translation(call)
    try:
        if call.data == 'captcha_ok':
            greeting.call_handler(call)

        if 'forecast' in call.data or 'weather' in call.data:
            weather.call_handler(call)

        if 'lang' in call.data:
            introduction.call_handler(call)

    except Exception:
        bot.answer_callback_query(callback_query_id=call.id, text=trans['global']['errors']['default'])


bot.polling()
