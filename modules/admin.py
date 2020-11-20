import telebot
import config
from translation import tw
import sqlite3

bot = telebot.TeleBot(config.token)


def broadcast(message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    if message.from_user.username == config.owner_username:
        try:
            conn = sqlite3.connect('data.db')
            curs = conn.cursor()
            curs.execute('SELECT chat_id FROM chats')
            rows = curs.fetchall()
            conn.close()

            msg = bot.send_message(chat_id=message.chat.id, text=trans['admin']['broadcast']['start'])

            i = 0
            for row in rows:
                if not row[0] > 0:
                    bot.send_message(chat_id=row[0], text=message.text.split(' ', 1)[1])
                    i += 1
                    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                                          text=trans['admin']['broadcast']['process'].format(count=str(i)))

            bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                                  text=trans['admin']['broadcast']['end'].format(count=str(i)))
        except Exception as e:
            print(e)
