import telebot
import config
import sqlite3

bot = telebot.TeleBot(config.token)


def get_lang(data):
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    try:
        chat_id = data.chat.id
    except AttributeError:
        chat_id = data.message.chat.id

    curs.execute('SELECT language FROM chats WHERE chat_id = ?', (chat_id,))
    rows = curs.fetchall()
    conn.close()
    return rows[0][0]


def error_call(call):
    lang = get_lang(call)
    text = ''
    if lang == 'eng':
        text = 'Oops... Something went wrong'
    elif lang == 'rus':
        text = 'Упс... Что-то пошло не так'

    bot.answer_callback_query(callback_query_id=call.id,
                              text=text)


def error_msg(message):
    lang = get_lang(message)
    text = ''
    if lang == 'eng':
        text = 'Oops... Something went wrong'
    elif lang == 'rus':
        text = 'Упс... Что-то пошло не так'

    bot.reply_to(message, text)


def admin_error_msg(message):
    lang = get_lang(message)
    text = ''
    if lang == 'eng':
        text = 'You need administrative privileges to do this'
    elif lang == 'rus':
        text = 'Для этого нужны административные права'

    bot.reply_to(message, text)


def admin_error_call(call):
    lang = get_lang(call)
    text = ''
    if lang == 'eng':
        text = 'You need administrative privileges to do this'
    elif lang == 'rus':
        text = 'Для этого нужны административные права'

    bot.answer_callback_query(callback_query_id=call.id,
                              text=text)
