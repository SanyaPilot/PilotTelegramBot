from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ChatType
from init import bot, dp, tw, Chats, session
from loguru import logger


@dp.message_handler(commands='start')
async def start(message: Message):
    try:
        if message.chat.type == ChatType.SUPERGROUP or message.chat.type == ChatType.GROUP:
            if not session.query(Chats.chat_id).filter_by(chat_id=message.chat.id).first() == (message.chat.id,):
                new_chat = Chats(chat_id=message.chat.id, setup_is_finished=False)
                session.add(new_chat)
                logger.info(f"New chat {message.chat.full_name}")

                keyboard = InlineKeyboardMarkup(row_width=2)
                for i in tw.available:
                    name = i.split('.')[0]
                    keyboard.add(InlineKeyboardButton(text=tw.get_labels()[name], callback_data=f'lang_{name}'))

                if 'eng.json' in tw.available:
                    new_chat.language = 'eng'
                    new_chat.setup_is_finished = True
                else:
                    new_chat.language = tw.available[0].split('.')[0]
                    new_chat.setup_is_finished = True

                session.commit()

                trans = tw.get_translation(message)
                await bot.send_message(message.chat.id, trans['introduction']['start'],
                                       reply_markup=keyboard)
            else:
                logger.warning(f"Non-new chat {message.chat.full_name}")
    except Exception as err:
        logger.error(f"{message.chat.full_name}: {err}")


@dp.message_handler(commands='help')
async def help(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return

    lang = session.query(Chats.setup_is_finished).filter_by(chat_id=message.chat.id)
    if not lang:
        text = trans['global']['errors']['setup']
    else:
        text = trans['introduction']['help']

    await bot.send_message(chat_id=message.chat.id,
                           text=text)
    logger.info(f"{message.chat.full_name}: {message.from_user.full_name} - {message.text}")


@dp.callback_query_handler(lambda c: 'lang' in c.data)
async def call_handler(call: CallbackQuery):
    trans = tw.get_translation(call)
    try:
        member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                           user_id=call.message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            chat = session.query(Chats).filter_by(chat_id=call.message.chat.id).first()
            chat.language = call.data[5:]
            chat.setup_is_finished = True
            session.commit()
            trans = tw.get_translation(call)
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['lang_set'])

            keyboard = InlineKeyboardMarkup(row_width=2)
            for i in tw.available:
                name = i.split('.')[0]
                keyboard.add(
                    InlineKeyboardButton(text=tw.get_labels()[name], callback_data=f'lang_{name}'))
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text=trans['introduction']['start'],
                                        reply_markup=keyboard)

        else:
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['global']['errors']['admin'])
            logger.warning(
                f"{message.chat.full_name}: User {message.reply_to_message.from_user.full_name} need administrative privileges to do this")
    except Exception as err:
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text=trans['global']['errors']['default'])
        logger.error(f"{call.message.chat.full_name}: {err}")
