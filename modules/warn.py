from aiogram.types import Message
from init import bot, dp, tw, Chats, Warns, session
from modules.telethon.get_info import get_user_from_username as get_user
from babel.dates import format_timedelta
from time import time
from loguru import logger


@dp.message_handler(commands='warn')
async def warn(message: Message, user_obj=None):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        punishment = session.query(Chats.warns_punishment).filter_by(chat_id=message.chat.id).first()
        if punishment[0] is None:
            return
        check_perms = True
        if user_obj:
            user = user_obj
            username = user.full_name
            check_perms = False
        else:
            user = None
            username = None
            text_mention = False
            for entity in message.entities:
                if entity.type == 'mention':
                    if not '--force' in message.text:
                        user = message.text[entity.offset:]
                    else:
                        user = message.text[entity.offset:-7]

                elif entity.type == 'text_mention':
                    user = entity.user
                    text_mention = True

            if user and not text_mention:
                try:
                    user = await get_user(user)
                except ValueError:
                    await message.reply(text=trans['global']['errors']['user_not_found'])
                    return

                if not user.last_name:
                    username = user.first_name
                else:
                    username = user.first_name + user.last_name

            elif not user and message.reply_to_message:
                user = message.reply_to_message.from_user
                username = user.full_name
            elif text_mention:
                username = user.full_name
            else:
                await message.reply(trans['global']['errors']['no_args/reply'])
                logger.warning(
                    f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without args/reply')
                return

        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if check_perms and not (member.status == 'creator' or member.status == 'administrator'):
            await message.reply(trans['global']['errors']['admin'])
            logger.warning(
                f"{message.chat.full_name}: User {message.from_user.full_name} need administrative privileges to do this")
            return

        if check_perms and message.from_user.id == user.id:
            await message.reply(trans['warn']['same_usr_err'])
            logger.warning(f"{message.chat.full_name}: User {username} wanted to warn himself")
            return

        me = await bot.get_me()
        if not user.id == me.id:
            member2 = await bot.get_chat_member(chat_id=message.chat.id,
                                                user_id=user.id)

            if (member2.status == 'creator' or member2.status == 'administrator') and not '--force' in message.get_args():
                await message.reply(trans['warn']['no_force_err'])
                logger.warning(
                    f"{message.chat.full_name}: User {message.from_user.full_name} not --force flag")
                return

            data = session.query(Warns).filter_by(chat_id=message.chat.id, user_id=user.id).first()
            max_warns = session.query(Chats.max_warns).filter_by(chat_id=message.chat.id).first()
            warns = None
            name = None
            if user.username:
                name = '@' + user.username
            else:
                name = username
            if data:
                data.warns += 1
                session.commit()
                warns = data.warns
                if data.warns == max_warns[0]:
                    res = await apply_punishment(message, user, trans, name, member2)
                    if res == 1:
                        return

                    session.query(Warns).filter_by(user_id=user.id, chat_id=message.chat.id).delete()
                    session.commit()
                    return

            else:
                session.add(Warns(user_id=user.id, chat_id=message.chat.id, warns=1))
                warns = 1

            await message.reply(text=trans['warn']['warn'].format(
                username=name, current_warns=str(warns), max_warns=str(max_warns[0])), parse_mode='HTML')
        else:
            await message.reply(trans['global']['errors']['affect_on_bot'])
            logger.warning(f"{message.chat.full_name}: User {message.from_user.full_name} wanted to warn bot")

    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


async def apply_punishment(message: Message, user, trans, name, member):
    punishment = session.query(Chats.warns_punishment).filter_by(chat_id=message.chat.id).first()
    duration = session.query(Chats.warns_punishment_time).filter_by(chat_id=message.chat.id).first()
    warns = session.query(Warns).filter_by(chat_id=message.chat.id, user_id=user.id).first()
    if member.status == 'creator' or member.status == 'administrator':
        if member.can_be_edited:
            await bot.promote_chat_member(chat_id=message.chat.id,
                                          user_id=user.id,
                                          can_pin_messages=False,
                                          can_change_info=False,
                                          can_invite_users=False,
                                          can_delete_messages=False,
                                          can_promote_members=False,
                                          can_restrict_members=False
                                          )
        else:
            await message.reply(trans[punishment[0]]['admin_err'])
            warns.warns -= 1
            session.commit()
            return 1

    if punishment[0] == 'mute':
        if duration[0] is None:
            await bot.restrict_chat_member(chat_id=message.chat.id,
                                           user_id=user.id,
                                           can_send_messages=False)

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['mute']['mute'].format(
                                        username=str(name)))
        else:
            await bot.restrict_chat_member(chat_id=message.chat.id,
                                           user_id=user.id,
                                           can_send_messages=False,
                                           until_date=time() + duration[0])

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['mute']['tmute'].format(
                                       username=str(name),
                                       time=format_timedelta(
                                           duration[0], locale=trans['id'], granularity="seconds",
                                           format="long"
                                       )))
        logger.info(f"{message.chat.full_name}: User {name} was muted")

    elif punishment[0] == 'ban':
        if duration[0] is None:
            await bot.kick_chat_member(chat_id=message.chat.id,
                                       user_id=user.id,
                                       until_date=0)

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['ban']['ban'].format(
                                        username=str(name)))

        else:
            await bot.kick_chat_member(chat_id=message.chat.id,
                                       user_id=user.id,
                                       until_date=time() + duration[0])

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['ban']['tban'].format(
                                       username=str(name),
                                       time=format_timedelta(
                                           duration[0], locale=trans['id'], granularity="seconds",
                                           format="long"
                                       )))

        logger.info(f'{message.chat.full_name}: Banned {name}')

    elif punishment[0] == 'kick':
        await bot.kick_chat_member(chat_id=message.chat.id,
                                   user_id=user.id,
                                   until_date=0)
        await bot.unban_chat_member(chat_id=message.chat.id,
                                    user_id=user.id)

        await bot.send_message(chat_id=message.chat.id,
                               text=trans['kick']['kick'].format(
                                    username=str(name)))
