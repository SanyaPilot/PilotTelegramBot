import telebot
bot = telebot.TeleBot('1073948237:AAGKs3HzRBZwBZGkoQ5moJIakWQn39nQtX4')


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
