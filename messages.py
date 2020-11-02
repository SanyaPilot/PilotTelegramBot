import telebot
from time import sleep
import config
from translation import tw

bot = telebot.TeleBot(config.token)


def del_msgs(msgs, chat_id):
    for i in msgs:
        try:
            bot.delete_message(chat_id=chat_id, message_id=i)
        except Exception:
            pass


def purge(message):
    trans = tw.get_translation(message)
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            start = message.reply_to_message.message_id
            end = message.message_id + 1
            chat_id = message.chat.id

            msgs = []
            for i in range(start, end):
                msgs.append(i)
                if len(msgs) == 100:
                    del_msgs(msgs, chat_id)
                    msgs = []

            del_msgs(msgs, chat_id)
            sent_msg = bot.send_message(chat_id=chat_id, text=trans['messages']['purge'])
            sleep(5)
            bot.delete_message(chat_id=chat_id, message_id=sent_msg.message_id)
    except Exception:
        bot.reply_to(message, trans['global']['errors']['default'])
