import time
import datetime
from utils.timedelta import parse_timedelta_from_message
from aiogram.types import Message
from init import dp, tw, bot
from babel.dates import format_timedelta
from loguru import logger


@dp.message_handler(commands='mute')
async def mute(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return

    duration = await parse_timedelta_from_message(message)
    if not duration:
        return
    try:
        bot_obj = await bot.get_me()
        bot_id = bot_obj.id
        me = await bot.get_chat_member(chat_id=message.chat.id, user_id=bot_id)
        if me.can_restrict_members:
            if message.reply_to_message:
                member = await bot.get_chat_member(chat_id=message.chat.id,
                                                   user_id=message.from_user.id)
                if member.status == 'creator' or member.status == 'administrator':
                    me = await bot.get_me()
                    if not message.reply_to_message.from_user.id == me.id:
                        member2 = await bot.get_chat_member(chat_id=message.chat.id,
                                                            user_id=message.reply_to_message.from_user.id)
                        if not message.from_user.id == message.reply_to_message.from_user.id:
                            if member2.status == 'creator' or member2.status == 'administrator':
                                if '--force' in message.get_args():
                                    if member2.can_be_edited:
                                        await bot.promote_chat_member(chat_id=message.chat.id,
                                                                      user_id=message.reply_to_message.from_user.id,
                                                                      can_pin_messages=False,
                                                                      can_change_info=False,
                                                                      can_invite_users=False,
                                                                      can_delete_messages=False,
                                                                      can_promote_members=False,
                                                                      can_restrict_members=False
                                                                      )
                                    else:
                                        await message.reply(trans['ban']['admin_err'])
                                        logger.warning(
                                            f"{message.chat.full_name}: User {message.reply_to_message.from_user.full_name} I can't ban this admin because admin privileges were given not by me")
                                        return
                                else:
                                    await message.reply(trans['ban']['no_force_err'])
                                    logger.warning(
                                        f"{message.chat.full_name}: User {message.reply_to_message.from_user.full_name} not --force flag")
                                    return

                            if duration != datetime.timedelta(hours=999999):
                                if not duration < datetime.timedelta(seconds=30):
                                    await bot.restrict_chat_member(chat_id=message.chat.id,
                                                                   user_id=message.reply_to_message.from_user.id,
                                                                   can_send_messages=False,
                                                                   until_date=duration)

                                    await bot.send_message(chat_id=message.chat.id,
                                                           text=trans['mute']['tmute'].format(
                                                               username=str(message.reply_to_message.from_user.username),
                                                               time=format_timedelta(
                                                                   duration, locale=trans['id'], granularity="seconds",
                                                                   format="long"
                                                               )))
                                else:
                                    await message.reply(trans['mute']['tmute_too_few'])
                            else:
                                await bot.restrict_chat_member(chat_id=message.chat.id,
                                                               user_id=message.reply_to_message.from_user.id,
                                                               can_send_messages=False,
                                                               until_date=0)

                                await bot.send_message(chat_id=message.chat.id,
                                                       text=trans['mute']['mute'].format(
                                                           username=str(message.reply_to_message.from_user.username)))
                                logger.info(f"{message.chat.full_name}: {message.reply_to_message.from_user.full_name} muted")
                        else:
                            await message.reply(trans['ban']['same_usr_err'][0])
                            logger.warning(
                                f"{message.chat.full_name}: User {message.from_user.full_name} wanted to ban myself")
                    else:
                        await message.reply(trans['global']['errors']['affect_on_bot'])
                        logger.warning(
                            f"{message.chat.full_name}: User {message.from_user.full_name} Why are you trying to do this?")
                else:
                    await message.reply(trans['global']['errors']['admin'])
                    logger.warning(
                        f"{message.chat.full_name}: User {message.from_user.full_name} need administrative privileges to do this")
            else:
                await message.reply(trans['global']['errors']['no_reply'])
                logger.warning(f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without reply')
        else:
            perm = 'can_restrict_members'
            await message.reply(trans['global']['errors']['no_needed_perm'].format(perm=perm),
                                parse_mode='HTML')
            logger.warning(f"{message.chat.full_name}: Bot doesn't have perm {perm}")
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


# Размут
@dp.message_handler(commands='unmute')
async def unmute(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        bot_obj = await bot.get_me()
        bot_id = bot_obj.id
        me = await bot.get_chat_member(chat_id=message.chat.id, user_id=bot_id)
        if me.can_restrict_members:
            if message.reply_to_message:
                member = await bot.get_chat_member(chat_id=message.chat.id,
                                                   user_id=message.from_user.id)
                if member.status == 'creator' or member.status == 'administrator':
                    me = await bot.get_me()
                    if not message.reply_to_message.from_user.id == me.id:
                        if not message.from_user.id == message.reply_to_message.from_user.id:
                            member2 = await bot.get_chat_member(chat_id=message.chat.id,
                                                                user_id=message.reply_to_message.from_user.id)
                            if member2.status == 'restricted':
                                chat = await bot.get_chat(chat_id=message.chat.id)
                                perms = chat.permissions
                                await bot.restrict_chat_member(chat_id=message.chat.id,
                                                               user_id=message.reply_to_message.from_user.id,
                                                               can_send_messages=True,
                                                               can_send_media_messages=perms.can_send_media_messages,
                                                               can_send_other_messages=perms.can_send_other_messages,
                                                               can_add_web_page_previews=perms.can_add_web_page_previews,
                                                               until_date=0)

                                await bot.send_message(chat_id=message.chat.id,
                                                       text=trans['mute']['unmute'].format(
                                                           username=str(message.reply_to_message.from_user.username)))
                                logger.info(f"{message.chat.full_name}: {message.reply_to_message.from_user.full_name} unmuted")
                            else:
                                await message.reply(trans['mute']['user_not_muted'])
                                logger.warning(f"{message.chat.full_name}: {message.reply_to_message.from_user.full_name} not muted")
                        else:
                            await message.reply(trans['global']['errors']['affect_on_bot'])
                            logger.warning(
                                f"{message.chat.full_name}: User {message.from_user.full_name} Why are you trying to do this?")
                    else:
                        await message.reply(trans['global']['errors']['affect_on_bot'])
                        logger.warning(
                            f"{message.chat.full_name}: User {message.from_user.full_name} Why are you trying to do this?")
                else:
                    await message.reply(trans['global']['errors']['admin'])
                    logger.warning(
                            f"{message.chat.full_name}: User {message.from_user.full_name} need administrative privileges to do this")
            else:
                await message.reply(trans['global']['errors']['no_reply'])
                logger.warning(f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without reply')
        else:
            perm = 'can_restrict_members'
            await message.reply(trans['global']['errors']['no_needed_perm'].format(perm=perm),
                                parse_mode='HTML')
            logger.warning(f"{message.chat.full_name}: Bot doesn't have perm {perm}")
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")
