import telebot
import config
import universal
import time
bot = telebot.TeleBot(config.token)


# Мут навсегда
def mute(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            bot.restrict_chat_member(chat_id=message.chat.id,
                                     user_id=message.reply_to_message.from_user.id,
                                     can_send_messages=False,
                                     until_date=0)

            bot.send_message(chat_id=message.chat.id,
                             text='Мут был дан пользователю @' +
                                  str(message.reply_to_message.from_user.username) + ' навсегда')

        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        universal.error_msg(message)


# Мут на время
def tmute(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            words = message.text.split()
            timeout = words[1]
            timeout_units = timeout[-1:]
            timeout_numbers = timeout[:-1]
            final_timeout = None
            timeout_text = None
            if timeout_units == 's':
                final_timeout = int(timeout_numbers)
                if int(timeout_numbers[-1:]) == 1:
                    text = ' секунду'
                elif 2 <= int(timeout_numbers) <= 4:
                    text = ' секунды'
                else:
                    text = ' секунд'
                timeout_text = timeout_numbers + text
            elif timeout_units == 'm':
                final_timeout = int(timeout_numbers) * 60
                if int(timeout_numbers[-1:]) == 1:
                    text = ' минуту'
                elif 2 <= int(timeout_numbers) <= 4:
                    text = ' минуты'
                else:
                    text = ' минут'
                timeout_text = timeout_numbers + text
            elif timeout_units == 'h':
                final_timeout = int(timeout_numbers) * 3600
                if int(timeout_numbers) == 1:
                    text = ' час'
                elif 2 <= int(timeout_numbers) <= 4:
                    text = ' часа'
                else:
                    text = ' часов'
                timeout_text = timeout_numbers + text
            elif timeout_units == 'd':
                final_timeout = int(timeout_numbers) * 86400
                if int(timeout_numbers) == 1:
                    text = ' день'
                elif 2 <= int(timeout_numbers[-1:]) <= 4:
                    text = ' дня'
                else:
                    text = ' дней'
                timeout_text = timeout_numbers + text

            bot.restrict_chat_member(chat_id=message.chat.id,
                                     user_id=message.reply_to_message.from_user.id,
                                     can_send_messages=False,
                                     until_date=int(time.time()) + final_timeout)

            bot.send_message(chat_id=message.chat.id,
                             text='Мут был дан пользователю @' + str(
                                 message.reply_to_message.from_user.username) + ' на ' + timeout_text)

        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        universal.error_msg(message)


# Размут
def unmute(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            chat = bot.get_chat(chat_id=message.chat.id)
            perms = chat.permissions
            bot.restrict_chat_member(chat_id=message.chat.id,
                                     user_id=message.reply_to_message.from_user.id,
                                     can_send_messages=True,
                                     can_send_media_messages=perms.can_send_media_messages,
                                     can_send_polls=perms.can_send_polls,
                                     can_send_other_messages=perms.can_send_other_messages,
                                     can_add_web_page_previews=perms.can_add_web_page_previews,
                                     until_date=0)
            bot.send_message(chat_id=message.chat.id,
                             text='Мут был снят с пользователя @' + str(
                                 message.reply_to_message.from_user.username))
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        universal.error_msg(message)
