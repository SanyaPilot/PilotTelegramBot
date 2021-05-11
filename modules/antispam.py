from aiogram.types import Message, ContentType
from init import bot, dp, tw, Chats, session
from modules.warn import warn
from time import time
from babel.dates import format_timedelta
from loguru import logger

chats = {}


def check(text):
    try:
        if text[0] != '/':
            return 0
        else:
            return 1
    except TypeError:
        return 1


@dp.message_handler(lambda msg: check(msg.text) == 0, content_types=ContentType.ANY)
async def antispam(message: Message):
    punishment = session.query(Chats.antispam_punishment).filter_by(chat_id=message.chat.id).first()
    if punishment is None:
        return
    if punishment[0] is None:
        return

    chat = chats.get(message.chat.id)
    if chat is None:
        chats[message.chat.id] = [message.from_user.id, 0]

    if chats[message.chat.id][0] == message.from_user.id:
        chats[message.chat.id][1] += 1
    else:
        chats[message.chat.id][0] = message.from_user.id
        chats[message.chat.id][1] = 1
    max_msgs = session.query(Chats.antispam_max).filter_by(chat_id=message.chat.id).first()
    if chats[message.chat.id][1] >= max_msgs[0]:
        await apply_punishment(message, punishment)


async def apply_punishment(message: Message, punishment):
    trans = tw.get_translation(message)
    duration = session.query(Chats.warns_punishment_time).filter_by(chat_id=message.chat.id).first()
    can_punish_admins = session.query(Chats.antispam_can_punish_admins).filter_by(chat_id=message.chat.id).first()
    member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        if member.can_be_edited and can_punish_admins[0]:
            await bot.promote_chat_member(chat_id=message.chat.id,
                                          user_id=message.from_user.id,
                                          can_pin_messages=False,
                                          can_change_info=False,
                                          can_invite_users=False,
                                          can_delete_messages=False,
                                          can_promote_members=False,
                                          can_restrict_members=False
                                          )
        else:
            return

    if punishment[0] == 'mute':
        if duration[0] is None:
            await bot.restrict_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id,
                                           can_send_messages=False)

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['mute']['mute'].format(
                                       username=message.from_user.full_name))
        else:
            await bot.restrict_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id,
                                           can_send_messages=False,
                                           until_date=time() + duration[0])

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['mute']['tmute'].format(
                                       username=message.from_user.full_name,
                                       time=format_timedelta(
                                           duration[0], locale=trans['id'], granularity="seconds",
                                           format="long"
                                       )))
        logger.info(f"{message.chat.full_name}: User {message.from_user.full_name} was muted")

    elif punishment[0] == 'ban':
        if duration[0] is None:
            await bot.kick_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id,
                                       until_date=0)

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['ban']['ban'].format(
                                       username=message.from_user.full_name))

        else:
            await bot.kick_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id,
                                       until_date=time() + duration[0])

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['ban']['tban'].format(
                                       username=message.from_user.full_name,
                                       time=format_timedelta(
                                           duration[0], locale=trans['id'], granularity="seconds",
                                           format="long"
                                       )))

        logger.info(f'{message.chat.full_name}: Banned {message.from_user.full_name}')

    elif punishment[0] == 'kick':
        await bot.kick_chat_member(chat_id=message.chat.id,
                                   user_id=message.from_user.id,
                                   until_date=0)
        await bot.unban_chat_member(chat_id=message.chat.id,
                                    user_id=message.from_user.id)

        await bot.send_message(chat_id=message.chat.id,
                               text=trans['kick']['kick'].format(
                                   username=message.from_user.full_name))

    elif punishment[0] == 'warn':
        await warn(message, message.from_user)

    chats[message.chat.id] = None
