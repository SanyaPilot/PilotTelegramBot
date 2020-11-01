import telebot
import config
import sqlite3
import json
import os

bot = telebot.TeleBot(config.token)


class TranslationWorker:
    def __init__(self):
        self.available = os.listdir('translations')
        print('Available translations: ' + self.available[0].split('.')[0])
        self.translations = {}
        if self.available:
            for i in self.available:
                with open(f'translations/{i}', 'r') as file:
                    self.translations[i.split('.')[0]] = json.load(file)

        print('Translations loaded')

    def get_translation(self, data):
        return self.translations[self.get_lang(data)]

    def get_labels(self):
        labels = {}
        for key, value in self.translations.items():
            labels[key] = value['label']

        return labels

    @staticmethod
    def get_lang(data):
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        try:
            chat_id = data.chat.id
        except AttributeError:
            chat_id = data.message.chat.id

        curs.execute('SELECT language FROM chats WHERE chat_id = ?', (chat_id,))
        rows = curs.fetchall()
        conn.close()
        return rows[0][0]


tw = TranslationWorker()


def get_lang(data):
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    try:
        chat_id = data.chat.id
    except AttributeError:
        chat_id = data.message.chat.id

    curs.execute('SELECT language FROM chats WHERE chat_id = ?', (chat_id,))
    rows = curs.fetchall()
    conn.close()
    return rows[0][0]


def error_call(call):
    lang = get_lang(call)
    text = ''
    if lang == 'eng':
        text = 'Oops... Something went wrong'
    elif lang == 'rus':
        text = 'Упс... Что-то пошло не так'

    bot.answer_callback_query(callback_query_id=call.id,
                              text=text)


def error_msg(message):
    lang = get_lang(message)
    text = ''
    if lang == 'eng':
        text = 'Oops... Something went wrong'
    elif lang == 'rus':
        text = 'Упс... Что-то пошло не так'

    bot.reply_to(message, text)


def admin_error_msg(message):
    lang = get_lang(message)
    text = ''
    if lang == 'eng':
        text = 'You need administrative privileges to do this'
    elif lang == 'rus':
        text = 'Для этого нужны административные права'

    bot.reply_to(message, text)


def admin_error_call(call):
    lang = get_lang(call)
    text = ''
    if lang == 'eng':
        text = 'You need administrative privileges to do this'
    elif lang == 'rus':
        text = 'Для этого нужны административные права'

    bot.answer_callback_query(callback_query_id=call.id,
                              text=text)
