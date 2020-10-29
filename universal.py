import telebot
import config
import sqlite3

bot = telebot.TeleBot(config.token)


def error_call(call):
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    curs.execute('SELECT language FROM chats WHERE chat_id = ?', (call.message.chat.id,))
    rows = curs.fetchall()
    conn.close()

    text = ''
    if rows[0][0] == 'eng':
        text = 'Oops... Something went wrong'
    elif rows[0][0] == 'rus':
        text = 'Упс... Что-то пошло не так'

    bot.answer_callback_query(callback_query_id=call.id,
                              text=text)


def error_msg(message):
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    curs.execute('SELECT language FROM chats WHERE chat_id = ?', (message.chat.id,))
    rows = curs.fetchall()
    conn.close()

    text = ''
    if rows[0][0] == 'eng':
        text = 'Oops... Something went wrong'
    elif rows[0][0] == 'rus':
        text = 'Упс... Что-то пошло не так'

    bot.reply_to(message, text)
