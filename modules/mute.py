import time
import datetime
from utils.timedelta import parse_timedelta_from_message
from aiogram.types import Message
from init import dp, tw, bot
from babel.dates import format_timedelta


# Мут навсегда
@dp.message_handler(commands='mute')
async def mute(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return

    duration = await parse_timedelta_from_message(message)
    if not duration:
        return
    try:
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
                                await message.reply(trans['mute']['admin_err'])
                                return
                        else:
                            await message.reply(trans['mute']['no_force_err'])
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
                else:
                    await message.reply(trans['ban']['same_usr_err'][0])
            else:
                await message.reply(trans['global']['errors']['affect_on_bot'])
        else:
            await message.reply(trans['global']['errors']['admin'])

    except Exception:
        await message.reply(trans['global']['errors']['default'])


# Размут
@dp.message_handler(commands='unmute')
async def unmute(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
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
                    else:
                        await message.reply(trans['mute']['user_not_muted'])
                else:
                    await message.reply(trans['global']['errors']['affect_on_bot'])
            else:
                await message.reply(trans['global']['errors']['affect_on_bot'])
        else:
            await message.reply(trans['global']['errors']['admin'])

    except Exception:
        await message.reply(trans['global']['errors']['default'])
