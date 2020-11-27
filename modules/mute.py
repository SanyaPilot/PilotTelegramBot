import time

from aiogram.types import Message
from init import dp, tw, bot


# Мут навсегда
@dp.message_handler(commands='mute')
async def mute(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            if len(message.text.split()) > 1:
                words = message.text.split()
                timeout = words[1]
                timeout_units = timeout[-1:]
                timeout_numbers = timeout[:-1]
                if timeout_units == 's' and int(timeout_numbers) < 30:
                    await bot.send_message(chat_id=message.chat.id,
                                           text=trans['mute']['tmute_too_few'])
                    return
                final_timeout = None
                timeout_text = None
                if str(type(tw.get_translation(message)['global']['time']['seconds'])) == "<class 'list'>":
                    if timeout_units == 's':
                        final_timeout = int(timeout_numbers)
                        if int(timeout_numbers[-1:]) == 1:
                            text = trans['global']['time']['seconds'][0]
                        elif 2 <= int(timeout_numbers) <= 4:
                            text = trans['global']['time']['seconds'][1]
                        else:
                            text = trans['global']['time']['seconds'][2]
                        timeout_text = timeout_numbers + ' ' + text
                    elif timeout_units == 'm':
                        final_timeout = int(timeout_numbers) * 60
                        if int(timeout_numbers[-1:]) == 1:
                            text = trans['global']['time']['minutes'][0]
                        elif 2 <= int(timeout_numbers) <= 4:
                            text = trans['global']['time']['minutes'][1]
                        else:
                            text = trans['global']['time']['minutes'][2]
                        timeout_text = timeout_numbers + ' ' + text
                    elif timeout_units == 'h':
                        final_timeout = int(timeout_numbers) * 3600
                        if int(timeout_numbers) == 1:
                            text = trans['global']['time']['hours'][0]
                        elif 2 <= int(timeout_numbers) <= 4:
                            text = trans['global']['time']['hours'][1]
                        else:
                            text = trans['global']['time']['hours'][2]
                        timeout_text = timeout_numbers + ' ' + text
                    elif timeout_units == 'd':
                        final_timeout = int(timeout_numbers) * 86400
                        if int(timeout_numbers) == 1:
                            text = trans['global']['time']['days'][0]
                        elif 2 <= int(timeout_numbers[-1:]) <= 4:
                            text = trans['global']['time']['days'][1]
                        else:
                            text = trans['global']['time']['days'][2]
                        timeout_text = timeout_numbers + ' ' + text

                else:
                    if timeout_units == 's':
                        final_timeout = int(timeout_numbers)
                        text = trans['global']['time']['seconds']
                        timeout_text = timeout_numbers + ' ' + text
                    elif timeout_units == 'm':
                        final_timeout = int(timeout_numbers) * 60
                        text = trans['global']['time']['minutes']
                        timeout_text = timeout_numbers + ' ' + text
                    elif timeout_units == 'h':
                        final_timeout = int(timeout_numbers) * 3600
                        text = trans['global']['time']['hours']
                        timeout_text = timeout_numbers + ' ' + text
                    elif timeout_units == 'd':
                        final_timeout = int(timeout_numbers) * 86400
                        text = trans['global']['time']['days']
                        timeout_text = timeout_numbers + ' ' + text

                await bot.restrict_chat_member(chat_id=message.chat.id,
                                               user_id=message.reply_to_message.from_user.id,
                                               can_send_messages=False,
                                               until_date=int(time.time()) + final_timeout)

                await bot.send_message(chat_id=message.chat.id,
                                       text=trans['mute']['tmute'].format(
                                           username=str(message.reply_to_message.from_user.username),
                                           time=timeout_text))
            else:
                await bot.restrict_chat_member(chat_id=message.chat.id,
                                               user_id=message.reply_to_message.from_user.id,
                                               can_send_messages=False,
                                               until_date=0)

                await bot.send_message(chat_id=message.chat.id,
                                       text=trans['mute']['mute'].format(
                                           username=str(message.reply_to_message.from_user.username)))

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
            await message.reply(trans['global']['errors']['admin'])

    except Exception as e:
        await message.reply(trans['global']['errors']['default'])
        print(e)
