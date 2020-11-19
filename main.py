import telebot
import sqlite3

import config
import greeting as Greeting
import kick as Kick
import ban as Ban
import note as Note
import perms as Perms
import mute as Mute
import translate
import introduction
import weather as Weather
import messages as Messages
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


@bot.message_handler(commands=['setgreeting'])
def set_greeting(message):
    Greeting.set_greeting(message)


@bot.message_handler(commands=['rmgreeting'])
def rm_greeting(message):
    Greeting.rm_greeting(message)


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


@bot.message_handler(commands=['purge'])
def purge_wrapper(message):
    Messages.purge(message)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    try:
        if message.text[0] == '#':
            Note.text_handler(message)

    except Exception:
        pass


# Триггер на нового юзера в чате
@bot.message_handler(content_types=['new_chat_members'])
def greeting_wrapper(message):
    Greeting.greeting(message)


# Триггер на уход юзера из чата
@bot.message_handler(content_types=['left_chat_member'])
def greeting(message):
    bot.reply_to(message, text='Ну ладно, пока( *хнык*')


@bot.callback_query_handler(func=lambda call: True)
def button_callback_handler(call):
    trans = tw.get_translation(call)
    try:
        if call.data == 'captcha_ok':
            Greeting.call_handler(call)

        if 'forecast' in call.data or 'weather' in call.data:
            Weather.call_handler(call)

        if 'lang' in call.data:
            introduction.call_handler(call)

    except Exception:
        bot.answer_callback_query(callback_query_id=call.id, text=trans['global']['errors']['default'])


bot.polling()
