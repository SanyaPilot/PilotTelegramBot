from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ChatType
from init import bot, dp, tw, Chats, session
from loguru import logger
from modules.telethon.init import me as telethon_me
from modules.telethon.common import join_chat
from time import sleep


@dp.message_handler(commands='start')
async def start(message: Message):
    try:
        if message.chat.type == ChatType.SUPERGROUP or message.chat.type == ChatType.GROUP:
            if not session.query(Chats.chat_id).filter_by(chat_id=message.chat.id).first() == (message.chat.id,):
                new_chat = Chats(chat_id=message.chat.id, setup_is_finished=False, helper_in_chat=False)
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
                try:
                    result = await bot.get_chat_member(chat_id=message.chat.id, user_id=telethon_me.id)
                    if not result.status == 'left' and not result.status == 'kicked':
                        new_chat.helper_in_chat = True
                        session.commit()
                        keyboard.add(
                            InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_finish'))
                    else:
                        keyboard.add(
                            InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_helper'))
                except Exception:
                    keyboard.add(InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_helper'))

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


async def finish(call: CallbackQuery):
    trans = tw.get_translation(call)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=trans['introduction']['setup_finished'], parse_mode='HTML')

    sleep(5)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(lambda c: 'lang' in c.data)
async def call_handler(call: CallbackQuery):
    trans = tw.get_translation(call)
    try:
        member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                           user_id=call.message.from_user.id)
        print(member.status)
        if member.status == 'creator' or member.status == 'administrator':
            chat = session.query(Chats).filter_by(chat_id=call.message.chat.id).first()
            chat.language = call.data[5:]
            session.commit()
            trans = tw.get_translation(call)
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['lang_set'])

            keyboard = InlineKeyboardMarkup(row_width=2)
            for i in tw.available:
                name = i.split('.')[0]
                keyboard.add(
                    InlineKeyboardButton(text=tw.get_labels()[name], callback_data=f'lang_{name}'))

            try:
                result = await bot.get_chat_member(chat_id=call.message.chat.id, user_id=telethon_me.id)
                if not result.status == 'left' and not result.status == 'kicked':
                    keyboard.add(InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_finish'))
                else:
                    keyboard.add(InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_helper'))
            except Exception:
                keyboard.add(InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_helper'))

            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text=trans['introduction']['start'],
                                        reply_markup=keyboard)

        else:
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['global']['errors']['admin'])

    except Exception as err:
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text=trans['global']['errors']['default'])
        logger.error(f"{call.message.chat.full_name}: {err}")


@dp.callback_query_handler(lambda c: c.data == 'start_helper')
async def call_handler(call: CallbackQuery):
    trans = tw.get_translation(call)
    try:
        member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                           user_id=call.message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=trans['global']['yes'], callback_data='start_helper_join'),
                         InlineKeyboardButton(text=trans['global']['no'], callback_data='start_finish'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=trans['introduction']['add_helper'], reply_markup=keyboard)

    except Exception as err:
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text=trans['global']['errors']['default'])
        logger.error(f"{call.message.chat.full_name}: {err}")


async def helper_join_err(call: CallbackQuery):
    trans = tw.get_translation(call)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=trans['introduction']['try_again'], callback_data='start_helper_join'),
                 InlineKeyboardButton(text=trans['introduction']['skip'], callback_data='start_finish'))
    try:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=trans['introduction']['helper_join_failed'], parse_mode='HTML',
                                    reply_markup=keyboard)
    except Exception:
        pass


@dp.callback_query_handler(lambda c: c.data == 'start_helper_join')
async def callback_handler(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    try:
        await bot.export_chat_invite_link(chat_id=call.message.chat.id)
    except Exception:
        await helper_join_err(call)
        return

    chat = await bot.get_chat(chat_id=call.message.chat.id)
    invite_link = chat.invite_link
    result = await join_chat(call.message.chat.id)
    if not result:
        result = await join_chat(invite_link.split('https://t.me/joinchat/', 1)[1])
        if not result:
            await helper_join_err(call)
            return

    chat = session.query(Chats).filter_by(chat_id=call.message.chat.id).first()
    chat.helper_in_chat = True
    session.commit()
    await finish(call)


@dp.callback_query_handler(lambda c: c.data == 'start_finish')
async def callback_handler(call: CallbackQuery):
    await finish(call)
