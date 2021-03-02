from aiogram.types import Message
from init import bot, dp, tw, Chats, session
from modules.telethon.get_info import get_user_from_username as get_user
from loguru import logger


@dp.message_handler(commands='kick')
async def kick(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        bot_obj = await bot.get_me()
        bot_id = bot_obj.id
        me = await bot.get_chat_member(chat_id=message.chat.id, user_id=bot_id)
        if me.can_restrict_members:
            user = None
            username = None
            text_mention = False
            for entity in message.entities:
                if entity.type == 'mention':
                    if not '--force' in message.text:
                        user = message.text[entity.offset:]
                    elif '--force' in message.text:
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
                logger.warning(f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without args/reply')
                return

            member = await bot.get_chat_member(chat_id=message.chat.id,
                                               user_id=message.from_user.id)
            if member.status == 'creator' or member.status == 'administrator':
                me = await bot.get_me()
                if not user.id == me.id:
                    member2 = await bot.get_chat_member(chat_id=message.chat.id,
                                                        user_id=user.id)
                    if not message.from_user.id == user.id:
                        if member2.status == 'creator' or member2.status == 'administrator':
                            if '--force' in message.get_args():
                                if member2.can_be_edited:
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
                                    await message.reply(trans['kick']['admin_err'])
                                    logger.warning(
                                        f"{message.chat.full_name}: User {username} I can't ban this admin because admin privileges were given not by me")
                                    return
                            else:
                                await message.reply(trans['kick']['no_force_err'])
                                logger.warning(
                                    f"{message.chat.full_name}: User {message.from_user.full_name} no --force flag")
                                return

                        await bot.kick_chat_member(chat_id=message.chat.id,
                                                   user_id=user.id,
                                                   until_date=0)
                        await bot.unban_chat_member(chat_id=message.chat.id,
                                                    user_id=user.id)

                        if user.username:
                            name = '@' + user.username
                        else:
                            name = username

                        await bot.send_message(chat_id=message.chat.id,
                                               text=trans['kick']['kick'].format(
                                                   username=str(name)))
                        logger.info(f"{message.chat.full_name}: User {name} kicked")
                    else:
                        await message.reply(trans['kick']['same_usr_err'])
                        logger.warning(
                            f"{message.chat.full_name}: User {message.from_user.full_name} wanted to kick himself")
                else:
                    await message.reply(trans['global']['errors']['affect_on_bot'])
                    logger.warning(
                        f"{message.chat.full_name}: User {message.from_user.full_name} wanted to kick bot")
            else:
                await message.reply(trans['global']['errors']['admin'])
                logger.warning(
                    f"{message.chat.full_name}: User {message.from_user.full_name} need administrative privileges to do this")
        else:
            perm = 'can_restrict_members'
            await message.reply(trans['global']['errors']['no_needed_perm'].format(perm=perm),
                                parse_mode='HTML')
            logger.warning(f"{message.chat.full_name}: Bot doesn't have perm {perm}")
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


@dp.message_handler(commands='kickme')
async def kickme(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        bot_obj = await bot.get_me()
        bot_id = bot_obj.id
        me = await bot.get_chat_member(chat_id=message.chat.id, user_id=bot_id)
        if me.can_restrict_members:
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
                        await message.reply(trans['kick']['admin_err'])
                        logger.warning(
                            f"{message.chat.full_name}: User {message.from_user.full_name} I can't ban this admin because admin privileges were given not by me")
                        return
                else:
                    await message.reply(trans['kick']['no_force_err'])
                    logger.warning(
                        f"{message.chat.full_name}: User {message.from_user.full_name} not --force flag")
                    return

            await bot.kick_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id,
                                       until_date=0)
            await bot.unban_chat_member(chat_id=message.chat.id,
                                        user_id=message.from_user.id)

            await bot.send_message(chat_id=message.chat.id,
                                   text=trans['kick']['kick'].format(
                                       username=str(message.from_user.username)))
            logger.info(f"{message.chat.full_name}: User {message.from_user.full_name} kicked")
        else:
            perm = 'can_restrict_members'
            await message.reply(trans['global']['errors']['no_needed_perm'].format(perm=perm),
                                parse_mode='HTML')
            logger.warning(f"{message.chat.full_name}: Bot doesn't have perm {perm}")
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")
