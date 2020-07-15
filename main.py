import telebot
import sqlite3
import time

bot = telebot.TeleBot('1073948237:AAGKs3HzRBZwBZGkoQ5moJIakWQn39nQtX4')

table = """ CREATE TABLE IF NOT EXISTS notes (
                id integer PRIMARY KEY,
                name text NOT NULL,
                message_id integer NOT NULL
            ); """

conn = sqlite3.connect('data.db')
curs = conn.cursor()
curs.execute(table)
conn.close()


@bot.message_handler(commands=['start'])
def command_handler(message):
    bot.send_message(message.chat.id, 'Приветствую) Я бот для чата. Идеи соберем всем лейковским комьюнити)\nСправку по'
                                      ' командам можно получить по команде /help@sanya_pilot_bot\nЕсли что-то не '
                                      'работает, пните @alexander_baransky496\n')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Список команд:\n/mute - Мут навсегда (до размута)\n'
                          '/tmute - Мут на время. Время прописывается в формате <кол-во><s/m/h/d>\n'
                          '/unmute - Размут\n/ban - Забанить пользователя навсегда (до разбана)\n'
                          '/tban - Забанить пользователя на время. Формат такой же как в /tmute\n'
                          '/unban - Разбан\n/kick - Кикнуть пользователя\n'
                          '/restrict - Лишение пользователя всех прав\n'
                          '/permit - Выдача пользователю всех прав\n'
                          '/dpermit - Выдача пользователю дефолтных прав чата\n'
                          '/demote - Лишение пользователя всех административных прав (пока не работает)\n'
                          '/promote - Выдача пользователю всех административных прав (пока не работает)\n'
                          'Что применить все эти команды, необходимо ответить командой на сообщение пользователя, '
                          'которого вы хотите кикнуть, забанить и т. д.')


# Мут навсегда
@bot.message_handler(commands=['mute'])
def mute(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            chat = bot.get_chat(chat_id=message.chat.id)
            perms = chat.permissions
            bot.restrict_chat_member(chat_id=message.chat.id,
                                     user_id=message.reply_to_message.from_user.id,
                                     can_send_messages=False,
                                     can_change_info=perms.can_change_info,
                                     can_invite_users=perms.can_invite_users,
                                     can_pin_messages=perms.can_pin_messages,
                                     until_date=0)

            bot.send_message(chat_id=message.chat.id,
                             text='Мут был дан пользователю @' +
                                  str(message.reply_to_message.from_user.username) + ' навсегда')

        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


# Мут на время
@bot.message_handler(commands=['tmute'])
def tmute(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            timeout = message.text[7:]
            timeout_units = timeout[-1:]
            timeout_numbers = timeout[:1]
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

            chat = bot.get_chat(chat_id=message.chat.id)
            perms = chat.permissions
            bot.restrict_chat_member(chat_id=message.chat.id,
                                     user_id=message.reply_to_message.from_user.id,
                                     can_send_messages=False,
                                     can_change_info=perms.can_change_info,
                                     can_invite_users=perms.can_invite_users,
                                     can_pin_messages=perms.can_pin_messages,
                                     until_date=int(time.time()) + final_timeout)

            bot.send_message(chat_id=message.chat.id,
                             text='Мут был дан пользователю @' + str(
                                 message.reply_to_message.from_user.username) + ' на ' + timeout_text)

        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


# Размут
@bot.message_handler(commands=['unmute'])
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
                                     can_send_media_messages=True,
                                     can_send_polls=True,
                                     can_send_other_messages=True,
                                     can_add_web_page_previews=True,
                                     can_change_info=perms.can_change_info,
                                     can_invite_users=perms.can_invite_users,
                                     can_pin_messages=perms.can_pin_messages,
                                     until_date=0)
            bot.send_message(chat_id=message.chat.id,
                             text='Мут был снят с пользователя @' + str(
                                 message.reply_to_message.from_user.username))
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['restrict'])
def restrict(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            bot.restrict_chat_member(chat_id=message.chat.id,
                                     user_id=message.reply_to_message.from_user.id,
                                     until_date=0)

            bot.send_message(chat_id=message.chat.id,
                            text='Пользователь @' + str(message.reply_to_message.from_user.username) +
                                 ' был лишен прав')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['permit'])
def permit(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            bot.restrict_chat_member(chat_id=message.chat.id,
                                     user_id=message.reply_to_message.from_user.id,
                                     can_send_messages=True,
                                     can_send_media_messages=True,
                                     can_send_polls=True,
                                     can_send_other_messages=True,
                                     can_add_web_page_previews=True,
                                     can_change_info=True,
                                     can_invite_users=True,
                                     can_pin_messages=True,
                                     until_date=0)

            bot.send_message(chat_id=message.chat.id,
                             text='Пользователю @' + str(message.reply_to_message.from_user.username) +
                                  ' были выданы полные пользовательские права (не путать с админкой)')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['dpermit'])
def permit_default(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            chat = bot.get_chat(chat_id=message.chat.id)
            perms = chat.permissions
            bot.restrict_chat_member(chat_id=message.chat.id,
                                     user_id=message.reply_to_message.from_user.id,
                                     can_send_messages=perms.can_send_messages,
                                     can_send_media_messages=perms.can_send_media_messages,
                                     can_send_polls=perms.can_send_polls,
                                     can_send_other_messages=perms.can_send_other_messages,
                                     can_add_web_page_previews=perms.can_add_web_page_previews,
                                     can_change_info=perms.can_change_info,
                                     can_invite_users=perms.can_invite_users,
                                     can_pin_messages=perms.can_pin_messages,
                                     until_date=0)

            bot.send_message(chat_id=message.chat.id,
                             text='Пользователю @' + str(message.reply_to_message.from_user.username) +
                                  ' были выданы дефолтные права')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


# Убрать все права
@bot.message_handler(commands=['demote'])
def demote(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            bot.promote_chat_member(chat_id=message.chat.id,
                                    user_id=message.reply_to_message.from_user.id,
                                    can_pin_messages=0,
                                    can_change_info=0,
                                    can_edit_messages=0,
                                    can_invite_users=0,
                                    can_post_messages=0,
                                    can_delete_messages=0,
                                    can_promote_members=0,
                                    can_restrict_members=0
                                    )
            bot.send_message(chat_id=message.chat.id,
                             text='Пользователь @' + str(message.reply_to_message.from_user.username) +
                                  ' был лишен всех админских прав')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


# Дать все права
@bot.message_handler(commands=['promote'])
def promote(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                    user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            bot.promote_chat_member(chat_id=message.chat.id,
                                    user_id=message.reply_to_message.from_user.id,
                                    can_pin_messages=1,
                                    can_change_info=1,
                                    can_edit_messages=1,
                                    can_invite_users=1,
                                    can_post_messages=1,
                                    can_delete_messages=1,
                                    can_promote_members=1,
                                    can_restrict_members=1
                                    )
            bot.send_message(chat_id=message.chat.id,
                             text='Пользователю @' + str(message.reply_to_message.from_user.username) +
                                  ' были выданы полные админские права')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['kick'])
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
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['kickme'])
def kick(message):
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
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['ban'])
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


@bot.message_handler(commands=['banme'])
def kick(message):
    try:
        bot.kick_chat_member(chat_id=message.chat.id,
                             user_id=message.from_user.id,
                             until_date=0)

        bot.send_message(chat_id=message.chat.id,
                         text='Пользователь @' + str(message.from_user.username) +
                              ' был забанен\nОн больше НЕ сможет вернуться в чат в будущем')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['tban'])
def tban(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            timeout = message.text[6:]
            timeout_units = timeout[-1:]
            timeout_numbers = timeout[:1]
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


@bot.message_handler(commands=['unban'])
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


# Триггер на нового юзера в чате
@bot.message_handler(content_types=['new_chat_members'])
def greeting(message):
    bot.reply_to(message,
                 text='Привет, как дела?\nЗдесь мы осуждаем телефон LeEco Le 2 (ну или не совсем)\nВообщем не '
                      'разжигай холивары и все будет ок)')


# Триггер на уход юзера из чата
@bot.message_handler(content_types=['left_chat_member'])
def greeting(message):
    bot.reply_to(message, text='Ну ладно, пока( *хнык*')


@bot.message_handler(commands=['notes'])
def notes(message):
    try:
        cmd = """ SELECT name FROM notes """

        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        curs.execute(cmd)
        rows = curs.fetchall()
        conn.close()
        text = 'Список заметок:\n'
        for row in rows:
            text += '- '
            text += row[0]
            text += '\n'

        text += 'Вы можете просмотреть заметку командой /note <имя-заметки> либо при помощи #<имя-заметки>'
        bot.reply_to(message, text)

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['note'])
def note(message):
    try:
        name = message.text[6:]
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        cmd = """ SELECT message_id FROM notes
                  WHERE name = ? """
        curs.execute(cmd, (name,))

        rows = curs.fetchall()

        conn.close()

        row = rows[0]
        bot.forward_message(message.chat.id, message.chat.id, row[0])

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['addnote'])
def addnote(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            name = message.text[9:]
            conn = sqlite3.connect('data.db')
            curs = conn.cursor()
            cmd = """ INSERT INTO notes(name, message_id)
                      VALUES(?,?) """
            params = (name, message.reply_to_message.message_id)
            curs.execute(cmd, params)
            conn.commit()
            conn.close()

            bot.reply_to(message, 'Заметка была добавлена')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(commands=['delnote'])
def delnote(message):
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            name = message.text[9:]
            conn = sqlite3.connect('data.db')
            curs = conn.cursor()
            cmd = """ DELETE FROM notes WHERE name = ? """
            curs.execute(cmd, (name,))
            conn.commit()
            conn.close()

            bot.reply_to(message, 'Заметка была удалена')
        else:
            bot.reply_to(message, 'Для этого нужны админские права')

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    try:
        if message.text[0] == '#':
            name = message.text[1:]
            conn = sqlite3.connect('data.db')
            curs = conn.cursor()
            cmd = """ SELECT message_id FROM notes
                      WHERE name = ? """
            curs.execute(cmd, (name,))

            rows = curs.fetchall()

            conn.close()

            row = rows[0]
            bot.forward_message(message.chat.id, message.chat.id, row[0])

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


bot.polling()
