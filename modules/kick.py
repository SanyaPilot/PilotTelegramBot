from aiogram.types import Message
from init import bot, dp, tw


@dp.message_handler(commands='kick')
async def kick(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            await bot.kick_chat_member(chat_id=message.chat.id,
                                       user_id=message.reply_to_message.from_user.id,
                                       until_date=0)
            await bot.unban_chat_member(chat_id=message.chat.id,
                                        user_id=message.reply_to_message.from_user.id)

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['kick']['kick'].format(
                                       username=str(message.reply_to_message.from_user.username)))
        else:
            await message.reply(trans['global']['errors']['admin'])

    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(commands='kickme')
async def kickme(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        await bot.kick_chat_member(chat_id=message.chat.id,
                                   user_id=message.from_user.id,
                                   until_date=0)
        await bot.unban_chat_member(chat_id=message.chat.id,
                                    user_id=message.from_user.id)

        await bot.send_message(chat_id=message.chat.id,
                               text=trans['kick']['kick'].format(
                                   username=str(message.from_user.username)))

    except Exception:
        await message.reply(trans['global']['errors']['default'])
