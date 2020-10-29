import telebot
import config
import universal
bot = telebot.TeleBot(config.token)


def kick(message):
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
                             text='Пользователь @' + str(message.reply_to_message.from_user.username) +
                                  ' был кикнут\nОн сможет вернуться в чат в будущем')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        universal.error_msg(message)


def kickme(message):
    try:
        bot.kick_chat_member(chat_id=message.chat.id,
                             user_id=message.from_user.id,
                             until_date=0)
        bot.unban_chat_member(chat_id=message.chat.id,
                              user_id=message.from_user.id)

        bot.send_message(chat_id=message.chat.id,
                         text='Пользователь @' + str(message.from_user.username) +
                              ' был кикнут\nОн сможет вернуться в чат в будущем')

    except Exception:
        universal.error_msg(message)
