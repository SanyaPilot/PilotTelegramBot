import telebot
from telebot import types
import config
import universal
import sqlite3

bot = telebot.TeleBot(config.token)


def start(message):
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    curs.execute('INSERT INTO chats(chat_id, setup_is_finished) VALUES(?,?)', (message.chat.id, 0))
    conn.commit()

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    key_rus = types.InlineKeyboardButton(text='Русский \ud83c\uddf7\ud83c\uddfa', callback_data='lang_rus')
    key_eng = types.InlineKeyboardButton(text='English \ud83c\uddec\ud83c\udde7', callback_data='lang_eng')
    keyboard.add(key_rus, key_eng)
    # key_close = types.InlineKeyboardButton(text='Next >>', callback_data='setup_next')
    # keyboard.add(key_close)
    curs.execute("""UPDATE chats
                    SET language = ?,
                        setup_is_finished = ?
                    WHERE chat_id = ?""", ('eng', 1, message.chat.id))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Hello! I'm chat admin bot.\nFrom this moment I'll help in this chat\n"
                                      "For correct work you should give administrative privileges to me\n"
                                      "Please choose language. This will affect all messages from the bot",
                     reply_markup=keyboard)


def help(message):
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    curs.execute("""SELECT language FROM chats
                    WHERE chat_id = ?
                          AND setup_is_finished = ?""", (message.chat.id, 1))
    rows = curs.fetchall()
    conn.close()
    text = None
    try:
        if rows[0][0] == 'eng':
            text = 'Command list:\n' \
                   "/tr - Translate message. /tr <language code>" \
                   '/notes - Show notes list\n' \
                   '/note - Show note\n' \
                   '/addnote - Add note\n' \
                   '/delnote - Delete note\n' \
                   '/mute - Mute a user forever (until unmute)\n' \
                   '/tmute - Mute a user for a while. Time format: <quantity><s/m/h/d>\n' \
                   '/unmute - Remove mute from a user\n' \
                   '/ban - Ban a user forever (until unban)\n' \
                   '/banme - Ban a user, who wrote the command\n' \
                   '/tban - Ban a user for a while. Time format: <quantity><s/m/h/d>\n' \
                   '/unban - Remove ban from a user\n' \
                   '/kick - Kick a user\n' \
                   '/kickme - Kick a user, who wrote the command\n' \
                   '/restrict - Restrict all permissions of a user\n' \
                   '/permit - Permit all permissions of a user\n' \
                   '/dpermit - Permit default chat permissions of a user\n' \
                   '/demote - Remove administrative privileges from a user\n' \
                   '/promote - Give administrative privileges to a user\n' \
                   '/weather - Show current weather. /weather <city name>\n' \
                   '/forecast - Show weather forecast for a week. /forecast <city name>\n' \
                   '/setgreeting - Set greeting for new users.\n' \
                   "/rmgreeting - Remove greeting for new users. ATTENTION! If a chat doesn't have greeting, " \
                   "check for real user will be disabled!\n" \
                   'To use all of these commands you should reply command to message from user who you want to kick, ' \
                   'ban etc '

        elif rows[0][0] == 'rus':
            text = 'Список команд:\n' \
                   '/tr - Перевести сообщение. /tr <код языка, на который надо перевести>' \
                   '/notes - Показать список заметок\n' \
                   '/note - Просмотр заметки\n' \
                   '/addnote - Добавить заметку\n' \
                   '/delnote - Удалить заметку\n' \
                   '/mute - Мут навсегда (до размута)\n' \
                   '/tmute - Мут на время. Время прописывается в формате <кол-во><s/m/h/d>\n' \
                   '/unmute - Размут\n' \
                   '/ban - Забанить пользователя навсегда (до разбана)\n' \
                   '/banme - Забанить пользователя, написавшего команду\n' \
                   '/tban - Забанить пользователя на время. Формат такой же как в /tmute\n' \
                   '/unban - Разбан\n' \
                   '/kick - Кикнуть пользователя\n' \
                   '/kickme - Кикнуть пользователя, написавшего команду\n' \
                   '/restrict - Лишение пользователя всех прав\n' \
                   '/permit - Выдача пользователю всех прав\n' \
                   '/dpermit - Выдача пользователю дефолтных прав чата\n' \
                   '/demote - Лишение пользователя всех административных прав\n' \
                   '/promote - Выдача пользователю всех административных прав\n' \
                   '/weather - Показать текущую погоду. /weather <название города>\n' \
                   '/forecast - Показать прогноз погоды на неделю. /forecast <название города>\n' \
                   '/setgreeting - Установить приветствие для новых пользователей.\n' \
                   "/rmgreeting - Удалить приветствие для новых пользоватеоей. ВНИМАНИЕ! Если у чата нет приветствия, " \
                   "то проверка на реального пользователя также будет отключена!\n" \
                   'Чтобы применить все эти команды, необходимо ответить командой на сообщение пользователя, ' \
                   'которого вы хотите кикнуть, забанить и т. д.'
    except IndexError:
        text = 'Setup is not completed!'

    bot.send_message(chat_id=message.chat.id,
                     text=text)


def call_handler(call):
    try:
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        member = bot.get_chat_member(chat_id=call.message.chat.id,
                                     user_id=call.message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            if call.data == 'lang_rus':
                curs.execute("""UPDATE chats
                                SET language = ?,
                                    setup_is_finished = ?
                                WHERE chat_id = ?""", ('rus', 1, call.message.chat.id))
                conn.commit()
                conn.close()
                bot.answer_callback_query(callback_query_id=call.id,
                                        text='Хорошо! Язык установлен на русский!')

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                key_rus = types.InlineKeyboardButton(text='Русский \ud83c\uddf7\ud83c\uddfa', callback_data='lang_rus')
                key_eng = types.InlineKeyboardButton(text='English \ud83c\uddec\ud83c\udde7', callback_data='lang_eng')
                keyboard.add(key_rus, key_eng)
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="Привет! Я административный бот для чата.\nС этого момента я буду помогать в"
                                           " этом чате.\nДля корректной работы вам следует дать мне административные "
                                           "привилегии.\nПожалуйста, выберите язык. "
                                           "Это повлияет на все сообщения бота.",
                                      reply_markup=keyboard)
            elif call.data == 'lang_eng':
                curs.execute("""UPDATE chats
                                SET language = ?,
                                    setup_is_finished = ?
                                WHERE chat_id = ?""", ('eng', 1, call.message.chat.id))
                conn.commit()
                conn.close()
                bot.answer_callback_query(callback_query_id=call.id,
                                          text='Okay! Language is set to english!')

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                key_rus = types.InlineKeyboardButton(text='Русский \ud83c\uddf7\ud83c\uddfa', callback_data='lang_rus')
                key_eng = types.InlineKeyboardButton(text='English \ud83c\uddec\ud83c\udde7', callback_data='lang_eng')
                keyboard.add(key_rus, key_eng)
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="Hello! I'm chat admin bot.\nFrom this moment I'll help in this chat\n"
                                           "For correct work you should give administrative privileges to me\n"
                                           "Please choose language. This will affect all messages from the bot",
                                      reply_markup=keyboard)

        else:
            bot.answer_callback_query(callback_query_id=call.id,
                                      text='You need administrative privileges to do this')
    except Exception:
        universal.error_call(call)
