import telebot
import config
from translation import tw
bot = telebot.TeleBot(config.token)


def kick(message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            bot.kick_chat_member(chat_id=message.chat.id,
                                 user_id=message.reply_to_message.from_user.id,
                                 until_date=0)
            bot.unban_chat_member(chat_id=message.chat.id,
                                  user_id=message.reply_to_message.from_user.id)

            bot.send_message(chat_id=message.chat.id,
                             text=trans['kick']['kick'].format(username=str(message.reply_to_message.from_user.username)))
        else:
            bot.reply_to(message, trans['global']['errors']['admin'])

    except Exception:
        bot.reply_to(message, trans['global']['errors']['default'])


def kickme(message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        bot.kick_chat_member(chat_id=message.chat.id,
                             user_id=message.from_user.id,
                             until_date=0)
        bot.unban_chat_member(chat_id=message.chat.id,
                              user_id=message.from_user.id)

        bot.send_message(chat_id=message.chat.id,
                         text=trans['kick']['kick'].format(username=str(message.reply_to_message.from_user.username)))

    except Exception:
        bot.reply_to(message, trans['global']['errors']['default'])
