from aiogram.types import Message
from init import bot, dp, tw
from time import sleep
from loguru import logger


async def del_msgs(msgs, chat_id):
    for i in msgs:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=i)
        except Exception:
            pass


@dp.message_handler(commands='purge')
async def purge(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if message.reply_to_message:
            member = await bot.get_chat_member(chat_id=message.chat.id,
                                               user_id=message.from_user.id)
            if member.status == 'creator' or member.status == 'administrator':
                start = message.reply_to_message.message_id
                end = message.message_id + 1
                chat_id = message.chat.id

                msgs = []
                for i in range(start, end):
                    msgs.append(i)
                    if len(msgs) == 100:
                        await del_msgs(msgs, chat_id)
                        msgs = []

                await del_msgs(msgs, chat_id)
                sent_msg = await bot.send_message(chat_id=chat_id, text=trans['messages']['purge'])
                logger.info(f"{message.chat.full_name}: Purge completed")
                sleep(5)
                await bot.delete_message(chat_id=chat_id, message_id=sent_msg.message_id)
        else:
            await message.reply(trans['global']['errors']['no_reply'])
            logger.warning(f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without reply')
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")
