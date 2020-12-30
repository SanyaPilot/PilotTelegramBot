from aiogram.types import Message
from init import bot, dp, tw
from loguru import logger


@dp.message_handler(commands='restrict')
async def restrict(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if message.reply_to_message:
            member = await bot.get_chat_member(chat_id=message.chat.id,
                                               user_id=message.from_user.id)
            if member.status == 'creator' or member.status == 'administrator':
                me = await bot.get_me()
                if not message.reply_to_message.from_user.id == me.id:
                    member2 = await bot.get_chat_member(chat_id=message.chat.id,
                                                        user_id=message.reply_to_message.from_user.id)
                    if not message.from_user.id == message.reply_to_message.from_user.id:
                        if not (member2.status == 'creator' or member2.status == 'administrator'):
                            await bot.restrict_chat_member(chat_id=message.chat.id,
                                                           user_id=message.reply_to_message.from_user.id,
                                                           until_date=0)

                            await bot.send_message(chat_id=message.chat.id,
                                                   text=trans['perms']['restrict'].format(
                                                       username=str(message.reply_to_message.from_user.username)))
                            logger.info(f"{message.chat.full_name}: restrict {message.reply_to_message.from_user.full_name}")
                        else:
                            await message.reply(trans['perms']['admin_err'][0])
                            logger.warning(
                                f"{message.chat.full_name}: {message.from_user.full_name} Why are you trying to restrict admin?")
                    else:
                        await message.reply(trans['perms']['same_usr_err'][0])
                        logger.warning(
                            f"{message.chat.full_name}: User {message.from_user.full_name} wanted to restrict myself")
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
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


@dp.message_handler(commands='permit')
async def permit(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if message.reply_to_message:
            member = await bot.get_chat_member(chat_id=message.chat.id,
                                               user_id=message.from_user.id)
            if member.status == 'creator' or member.status == 'administrator':
                me = await bot.get_me()
                if not message.reply_to_message.from_user.id == me.id:
                    member2 = await bot.get_chat_member(chat_id=message.chat.id,
                                                        user_id=message.reply_to_message.from_user.id)
                    if not message.from_user.id == message.reply_to_message.from_user.id:
                        if not (member2.status == 'creator' or member2.status == 'administrator'):
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
                            logger.info(
                                f"{message.chat.full_name}: permit {message.reply_to_message.from_user.full_name}")
                        else:
                            await message.reply(trans['perms']['admin_err'][1])
                            logger.warning(
                                f"{message.chat.full_name}: {message.from_user.full_name} Why are you trying to give base permissions to admin?")
                    else:
                        await message.reply(trans['perms']['same_usr_err'][1])
                        logger.warning(
                            f"{message.chat.full_name}: User {message.from_user.full_name} wanted to permit myself")
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
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


@dp.message_handler(commands='dpermit')
async def permit_default(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if message.reply_to_message:
            member = await bot.get_chat_member(chat_id=message.chat.id,
                                               user_id=message.from_user.id)
            if member.status == 'creator' or member.status == 'administrator':
                me = await bot.get_me()
                if not message.reply_to_message.from_user.id == me.id:
                    member2 = await bot.get_chat_member(chat_id=message.chat.id,
                                                        user_id=message.reply_to_message.from_user.id)
                    if not message.from_user.id == message.reply_to_message.from_user.id:
                        if not (member2.status == 'creator' or member2.status == 'administrator'):
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
                            logger.info(
                                f"{message.chat.full_name}: dpermit {message.reply_to_message.from_user.full_name}")
                        else:
                            await message.reply(trans['perms']['admin_err'][1])
                            logger.warning(
                                f"{message.chat.full_name}: {message.from_user.full_name} Why are you trying to give base permissions to admin?")
                    else:
                        await message.reply(trans['perms']['same_usr_err'][1])
                        logger.warning(
                            f"{message.chat.full_name}: User {message.from_user.full_name} wanted to dpermit myself")
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
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


@dp.message_handler(commands='demote')
async def demote(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
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
                                await bot.send_message(chat_id=message.chat.id,
                                                       text=trans['perms']['demote'].format(username=str(
                                                           message.reply_to_message.from_user.username)))
                                logger.info(
                                    f"{message.chat.full_name}: demote {message.reply_to_message.from_user.full_name}")
                            else:
                                await message.reply(trans['perms']['unable_to_edit'])
                                logger.warning(f"{message.chat.full_name}: {message.from_user.full_name} Unable to remove admin permissions")
                        else:
                            await message.reply(trans['perms']['admin_err'][2])
                            logger.warning(
                                f"{message.chat.full_name}: {message.from_user.full_name} Why are you trying to restrict admin?")
                    else:
                        await message.reply(trans['perms']['same_usr_err'][0])
                        logger.warning(
                            f"{message.chat.full_name}: User {message.from_user.full_name} wanted to demote myself")
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
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


@dp.message_handler(commands='promote')
async def promote(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if message.reply_to_message:
            member = await bot.get_chat_member(chat_id=message.chat.id,
                                               user_id=message.from_user.id)
            if member.status == 'creator' or member.status == 'administrator':
                me = await bot.get_me()
                if not message.reply_to_message.from_user.id == me.id:
                    member2 = await bot.get_chat_member(chat_id=message.chat.id,
                                                        user_id=message.reply_to_message.from_user.id)
                    if not message.from_user.id == message.reply_to_message.from_user.id:
                        if not (member2.status == 'creator' or member2.status == 'administrator'):
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
                            logger.info(f"{message.chat.full_name}: new Admin {message.reply_to_message.from_user.full_name}")
                        else:
                            await message.reply(trans['perms']['admin_err'][3])
                            logger.warning(f"{message.chat.full_name}: {message.from_user.full_name} Why are you trying to restrict admin?")
                    else:
                        await message.reply(trans['perms']['same_usr_err'][1])
                        logger.warning(
                            f"{message.chat.full_name}: User {message.from_user.full_name} wanted to promote myself")
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
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")
