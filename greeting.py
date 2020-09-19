import telebot
import config
from telebot import types
from threading import Timer
bot = telebot.TeleBot(config.token)

timers = {}


def greeting(message):
    if not message.from_user.is_bot:
        text = 'Привет, как дела?\nЗдесь мы осуждаем телефон LeEco Le 2 (ну или не совсем)\nВ общем не '
        text += 'разжигай холивары и все будет ок)\n\nНо перед тем как ты вступишь в чат, нам нужно проверить,'
        text += ' действительно ли ты не бот. Для этого нужно нажать на кнопку, я думаю ты справишся\n\n'
        text += '<i><b>Ограничение по времени: 5 минут.\n'
        text += 'Если по истечении времени не была нажата кнопка, ты получаешь кик</b></i>'

        keyboard = types.InlineKeyboardMarkup()
        key = types.InlineKeyboardButton(text='Я хочу общатся!', callback_data='captcha_ok')
        keyboard.add(key)

        bot.send_message(chat_id=message.chat.id,
                         reply_to_message_id=message.message_id,
                         parse_mode='HTML',
                         text=text,
                         reply_markup=keyboard)

        global timers
        timers[message.from_user.id] = Timer(300.0, kick_bot, [message.chat.id, message.from_user.id])
        timers[message.from_user.id].start()


def kick_bot(chat_id, user_id):
    try:
        bot.kick_chat_member(chat_id=chat_id,
                             user_id=user_id,
                             until_date=0)

        bot.unban_chat_member(chat_id=chat_id,
                              user_id=user_id)

        chat_member = bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        user = chat_member.user
        bot.send_message(chat_id=chat_id,
                         text='Пользователь @' + str(user.username) +
                              ' не прошел проверку на бота\nОн был кикнут')
        global timers
        timers.pop(user_id)

    except Exception:
        bot.send_message(chat_id=chat_id, text='Упс... Что-то пошло не так')


def call_handler(call):
    try:
        timers[call.from_user.id].cancel()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Вы успешно прошли проверку!')
        timers.pop(call.from_user.id)
    except KeyError:
        bot.answer_callback_query(callback_query_id=call.id,
                                  text='Нельзя проходить проверку за другого пользователя')
