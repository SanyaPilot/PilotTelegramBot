import telebot
import sqlite3

bot = telebot.TeleBot('1073948237:AAGKs3HzRBZwBZGkoQ5moJIakWQn39nQtX4')


def notes(message):
    try:
        cmd = """ SELECT name FROM notes
                  WHERE chat_id = ?"""

        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        curs.execute(cmd, (message.chat.id,))
        rows = curs.fetchall()
        conn.close()
        text = '┏━━━━━━━━━━━━━━━━━━━━━━\n┣Список заметок:\n┃\n'
        for row in rows:
            text += '┣['
            text += row[0]
            text += '\n'

        text += '┗━━━━━━━━━━━━━━━━━━━━━━\n'
        text += 'Вы можете просмотреть заметку командой /note <имя-заметки> либо при помощи #<имя-заметки>'
        bot.reply_to(message, text)

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


def note(message):
    try:
        words = message.text.split()
        name = words[1]
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        cmd = """ SELECT message_id FROM notes
                  WHERE name = ?
                  AND chat_id = ?"""
        curs.execute(cmd, (name, message.chat.id))

        rows = curs.fetchall()

        conn.close()

        row = rows[0]
        bot.forward_message(message.chat.id, message.chat.id, row[0])

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


def addnote(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            words = message.text.split()
            name = words[1]
            conn = sqlite3.connect('data.db')
            curs = conn.cursor()
            cmd = """ INSERT INTO notes(name, message_id, chat_id)
                      VALUES(?,?,?) """
            params = (name, message.reply_to_message.message_id, message.chat.id)
            curs.execute(cmd, params)
            conn.commit()
            conn.close()

            bot.reply_to(message, 'Заметка была добавлена')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


def delnote(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            words = message.text.split()
            name = words[1]
            conn = sqlite3.connect('data.db')
            curs = conn.cursor()
            cmd = """ DELETE FROM notes
                      WHERE name = ?
                      AND chat_id = ?"""
            curs.execute(cmd, (name, message.chat.id))
            conn.commit()
            conn.close()

            bot.reply_to(message, 'Заметка была удалена')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


def text_handler(message):
    name = message.text[1:]
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    cmd = """ SELECT message_id FROM notes
                          WHERE name = ?
                          AND chat_id = ?"""
    curs.execute(cmd, (name, message.chat.id))
    rows = curs.fetchall()
    conn.close()

    row = rows[0]
    bot.forward_message(message.chat.id, message.chat.id, row[0])
