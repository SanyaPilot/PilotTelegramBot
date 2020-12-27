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
                                return
                        else:
                            await message.reply(trans['ban']['no_force_err'])
                            return

                    await bot.kick_chat_member(chat_id=message.chat.id,
                                               user_id=message.reply_to_message.from_user.id,
                                               until_date=0)
                    await bot.unban_chat_member(chat_id=message.chat.id,
                                                user_id=message.reply_to_message.from_user.id)

                    await bot.send_message(chat_id=message.chat.id,
                                           text=trans['kick']['kick'].format(
                                               username=str(message.reply_to_message.from_user.username)))
                else:
                    await message.reply(trans['ban']['same_usr_err'])
            else:
                await message.reply(trans['global']['errors']['affect_on_bot'])
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
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            if '--force' in message.get_args():
                if member.can_be_edited:
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
                    return
            else:
                await message.reply(trans['ban']['no_force_err'])
                return

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
