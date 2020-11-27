from aiogram.types import Message
from init import bot, dp, tw


@dp.message_handler(commands='restrict')
async def restrict(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            await bot.restrict_chat_member(chat_id=message.chat.id,
                                           user_id=message.reply_to_message.from_user.id,
                                           until_date=0)

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['perms']['restrict'].format(
                                       username=str(message.reply_to_message.from_user.username)))
        else:
            await message.reply(trans['global']['errors']['admin'])

    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(commands='permit')
async def permit(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            await bot.restrict_chat_member(chat_id=message.chat.id,
                                           user_id=message.reply_to_message.from_user.id,
                                           can_send_messages=True,
                                           can_send_media_messages=True,
                                           can_send_other_messages=True,
                                           can_add_web_page_previews=True,
                                           until_date=0)

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['perms']['permit'].format(
                                       username=str(message.reply_to_message.from_user.username)))
        else:
            await message.reply(trans['global']['errors']['admin'])

    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(commands='dpermit')
async def permit_default(message: Message):
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
                                           can_send_messages=perms.can_send_messages,
                                           can_send_media_messages=perms.can_send_media_messages,
                                           can_send_other_messages=perms.can_send_other_messages,
                                           can_add_web_page_previews=perms.can_add_web_page_previews,
                                           until_date=0)

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['perms']['permit_default'].format(username=str(
                                       message.reply_to_message.from_user.username)))
        else:
            await message.reply(trans['global']['errors']['admin'])

    except Exception:
        await message.reply(trans['global']['errors']['default'])


# Убрать все права
@dp.message_handler(commands='demote')
async def demote(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            await bot.promote_chat_member(chat_id=message.chat.id,
                                          user_id=message.reply_to_message.from_user.id,
                                          can_pin_messages=False,
                                          can_change_info=False,
                                          can_invite_users=False,
                                          can_delete_messages=False,
                                          can_promote_members=False,
                                          can_restrict_members=False
                                          )
            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['perms']['demote'].format(username=str(
                                       message.reply_to_message.from_user.username)))
        else:
            await message.reply(trans['global']['errors']['admin'])

    except Exception:
        await message.reply(trans['global']['errors']['default'])


# Дать все права
@dp.message_handler(commands='promote')
async def promote(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            await bot.promote_chat_member(chat_id=message.chat.id,
                                          user_id=message.reply_to_message.from_user.id,
                                          can_pin_messages=True,
                                          can_change_info=True,
                                          can_invite_users=True,
                                          can_delete_messages=True,
                                          can_promote_members=True,
                                          can_restrict_members=True
                                          )
            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['perms']['promote'].format(username=str(
                                       message.reply_to_message.from_user.username)))
        else:
            await message.reply(trans['global']['errors']['admin'])

    except Exception:
        await message.reply(trans['global']['errors']['default'])
