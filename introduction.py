import telebot
from telebot import types
import config
import sqlite3

bot = telebot.TeleBot(config.token)


def start(message):
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    curs.execute('INSERT INTO chats(chat_id, setup_is_finished) VALUES(?,?)', (message.chat.id, 0))
    conn.commit()
    conn.close()
    #bot.send_message(message.chat.id, 'Приветствую) Я бот-админ для чата.\nС этого момента я буду помогать в этом '
    #                                  'чате\nДля корректной работы необходимо выдать административные привилегии боту')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    key_rus = types.InlineKeyboardButton(text='Русский \ud83c\uddf7\ud83c\uddfa', callback_data='lang_rus')
    key_eng = types.InlineKeyboardButton(text='English \ud83c\uddec\ud83c\udde7', callback_data='lang_eng')
    keyboard.add(key_rus, key_eng)
    #key_close = types.InlineKeyboardButton(text='Next >>', callback_data='setup_next')
    #keyboard.add(key_close)

    bot.send_message(message.chat.id, "Hello! I'm chat admin bot.\nFrom this moment I'll help in this chat\n"
                                      "For correct work you should give administrative permissions to me\n"
                                      "Please choose language. This will affect all messages from the bot",
                     reply_markup=keyboard)


def help(message):
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


def call_handler(call):
    try:
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        if call.data == 'lang_rus':
            curs.execute("""UPDATE chats
                            SET language = ?,
                                setup_is_finished = ?
                            WHERE chat_id = ?""", ('rus', 1, call.message.chat.id))
            conn.commit()
            conn.close()
            bot.answer_callback_query(callback_query_id=call.id,
                                      text='Хорошо! Язык установлен на русский!')
        elif call.data == 'lang_eng':
            curs.execute("""UPDATE chats
                            SET language = ?,
                                setup_is_finished = ?
                            WHERE chat_id = ?""", ('eng', 1, call.message.chat.id))
            conn.commit()
            conn.close()
            bot.answer_callback_query(callback_query_id=call.id,
                                      text='Okay! Language is set to english!')
    except Exception:
        bot.answer_callback_query(callback_query_id=call.id,
                                  text='Упс... Что-то пошло не так')
