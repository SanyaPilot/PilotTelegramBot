import telebot
from telebot import types
import config
from translation import tw
import sqlite3

bot = telebot.TeleBot(config.token)


def start(message):
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    curs.execute('INSERT INTO chats(chat_id, setup_is_finished) VALUES(?,?)', (message.chat.id, 0))
    conn.commit()

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for i in tw.available:
        name = i.split('.')[0]
        keyboard.add(types.InlineKeyboardButton(text=tw.get_labels()[name], callback_data=f'lang_{name}'))

    # key_close = types.InlineKeyboardButton(text='Next >>', callback_data='setup_next')
    # keyboard.add(key_close)
    if 'eng.json' in tw.available:
        curs.execute("""UPDATE chats
                        SET language = ?,
                            setup_is_finished = ?
                        WHERE chat_id = ?""", ('eng', 1, message.chat.id))
    else:
        curs.execute("""UPDATE chats
                                SET language = ?,
                                    setup_is_finished = ?
                                WHERE chat_id = ?""", (tw.available[0].split('.')[0], 1, message.chat.id))
    conn.commit()
    conn.close()
    print(message)
    trans = tw.get_translation(message)
    bot.send_message(message.chat.id, trans['introduction']['start'],
                     reply_markup=keyboard)


def help(message):
    trans = tw.get_translation(message)

    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    curs.execute("""SELECT language FROM chats
                    WHERE chat_id = ?
                          AND setup_is_finished = ?""", (message.chat.id, 1))
    rows = curs.fetchall()
    conn.close()
    if not rows:
        text = trans['global']['errors']['setup']
    else:
        text = trans['introduction']['help']

    bot.send_message(chat_id=message.chat.id,
                     text=text)


def call_handler(call):
    trans = tw.get_translation(call)
    try:
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        member = bot.get_chat_member(chat_id=call.message.chat.id,
                                     user_id=call.message.from_user.id)

        if member.status == 'creator' or member.status == 'administrator':
            print(call.data[5:])
            curs.execute("""UPDATE chats
                            SET language = ?,
                                setup_is_finished = ?
                            WHERE chat_id = ?""", (call.data[5:], 1, call.message.chat.id))
            conn.commit()
            conn.close()
            trans = tw.get_translation(call)
            bot.answer_callback_query(callback_query_id=call.id,
                                      text=trans['lang_set'])

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            for i in tw.available:
                name = i.split('.')[0]
                keyboard.add(
                    types.InlineKeyboardButton(text=tw.get_labels()[name], callback_data=f'lang_{name}'))
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=trans['introduction']['start'],
                                  reply_markup=keyboard)

        else:
            bot.answer_callback_query(callback_query_id=call.id,
                                      text=trans['global']['errors']['admin'])
    except Exception:
        bot.answer_callback_query(callback_query_id=call.id,
                                  text=trans['global']['errors']['default'])
