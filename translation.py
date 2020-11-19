import telebot
import config
import sqlite3
import json
import os

bot = telebot.TeleBot(config.token)


class TranslationWorker:
    def __init__(self):
        self.available = os.listdir('translations')
        text = 'Available translations:'
        for i in self.available:
            text += ' ' + i.split('.')[0]
        
        print(text)
        self.translations = {}
        if self.available:
            for i in self.available:
                with open(f'translations/{i}', 'r') as file:
                    self.translations[i.split('.')[0]] = json.load(file)

        print('Translations loaded')

    def get_translation(self, data):
        try:
            return self.translations[self.get_lang(data)]
        except IndexError:
            return 1

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
