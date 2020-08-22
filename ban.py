import telebot
import time
bot = telebot.TeleBot('1073948237:AAGKs3HzRBZwBZGkoQ5moJIakWQn39nQtX4')


def ban(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            bot.kick_chat_member(chat_id=message.chat.id,
                                 user_id=message.reply_to_message.from_user.id,
                                 until_date=0)

            bot.send_message(chat_id=message.chat.id,
                             text='Пользователь @' + str(message.reply_to_message.from_user.username) +
                                  ' был забанен\nОн больше НЕ сможет вернуться в чат в будущем')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


def banme(message):
    try:
        bot.kick_chat_member(chat_id=message.chat.id,
                             user_id=message.from_user.id,
                             until_date=0)

        bot.send_message(chat_id=message.chat.id,
                         text='Пользователь @' + str(message.from_user.username) +
                              ' был забанен\nОн больше НЕ сможет вернуться в чат в будущем')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


def tban(message):
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
                    text = ' секунда'
                elif 2 <= int(timeout_numbers) <= 4:
                    text = ' секунды'
                else:
                    text = ' секунд'
                timeout_text = timeout_numbers + text
            elif timeout_units == 'm':
                final_timeout = int(timeout_numbers) * 60
                if int(timeout_numbers[-1:]) == 1:
                    text = ' минута'
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

            bot.kick_chat_member(chat_id=message.chat.id,
                                 user_id=message.reply_to_message.from_user.id,
                                 until_date=int(time.time()) + final_timeout)

            bot.send_message(chat_id=message.chat.id,
                             text='Пользователь @' + str(message.reply_to_message.from_user.username) +
                                  ' был забанен на ' + timeout_text +
                                  '\nОн сможет вернуться в чат после истечения времени')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


def unban(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            bot.unban_chat_member(chat_id=message.chat.id,
                                  user_id=message.reply_to_message.from_user.id)

            bot.send_message(chat_id=message.chat.id,
                             text='Пользователь @' + str(message.reply_to_message.from_user.username) +
                                  ' был разбанен\nТеперь он может вернуться в чат')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')
