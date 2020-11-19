import telebot
import config
from translation import tw
bot = telebot.TeleBot(config.token)


def restrict(message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            bot.restrict_chat_member(chat_id=message.chat.id,
                                     user_id=message.reply_to_message.from_user.id,
                                     until_date=0)

            bot.send_message(chat_id=message.chat.id,
                             text=trans['perms']['restrict'].format(username=str(message.reply_to_message.from_user.username)))
        else:
            bot.reply_to(message, trans['global']['errors']['admin'])

    except Exception:
        bot.reply_to(message, trans['global']['errors']['default'])


def permit(message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
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
                             text=trans['perms']['permit'].format(username=str(message.reply_to_message.from_user.username)))
        else:
            bot.reply_to(message, trans['global']['errors']['admin'])

    except Exception:
        bot.reply_to(message, trans['global']['errors']['default'])


def permit_default(message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
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
                             text=trans['perms']['permit_default'].format(username=str(
                                                                        message.reply_to_message.from_user.username)))
        else:
            bot.reply_to(message, trans['global']['errors']['admin'])

    except Exception:
        bot.reply_to(message, trans['global']['errors']['default'])


# Убрать все права
def demote(message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            bot.promote_chat_member(chat_id=message.chat.id,
                                    user_id=message.reply_to_message.from_user.id,
                                    can_pin_messages=False,
                                    can_change_info=False,
                                    can_invite_users=False,
                                    can_delete_messages=False,
                                    can_promote_members=False,
                                    can_restrict_members=False
                                    )
            bot.send_message(chat_id=message.chat.id,
                             text=trans['perms']['demote'].format(username=str(
                                                                        message.reply_to_message.from_user.username)))
        else:
            bot.reply_to(message, trans['global']['errors']['admin'])

    except Exception:
        bot.reply_to(message, trans['global']['errors']['default'])


# Дать все права
def promote(message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = bot.get_chat_member(chat_id=message.chat.id,
                                     user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            bot.promote_chat_member(chat_id=message.chat.id,
                                    user_id=message.reply_to_message.from_user.id,
                                    can_pin_messages=True,
                                    can_change_info=True,
                                    can_invite_users=True,
                                    can_delete_messages=True,
                                    can_promote_members=True,
                                    can_restrict_members=True
                                    )
            bot.send_message(chat_id=message.chat.id,
                             text=trans['perms']['promote'].format(username=str(
                                                                        message.reply_to_message.from_user.username)))
        else:
            bot.reply_to(message, trans['global']['errors']['admin'])

    except Exception:
        bot.reply_to(message, trans['global']['errors']['default'])
