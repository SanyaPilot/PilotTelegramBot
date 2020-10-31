import telebot
import config
import universal
import sqlite3

bot = telebot.TeleBot(config.token)


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
        universal.error_msg(message)


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
        universal.error_msg(message)


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
            universal.admin_error_msg(message)

    except Exception:
        universal.error_msg(message)


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
            universal.admin_error_msg(message)

    except Exception:
        universal.error_msg(message)


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
