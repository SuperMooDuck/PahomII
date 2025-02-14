import asyncio
import pickle
import os

STORAGE_FILENAME = "config.pickle"

class Storage:

    def __init__(self):
        self.bot_key = ""
        self.alarms = []
        self.text_reactions = []
        self.home_chat_id = None

    def load_data(self):
        if os.path.exists(STORAGE_FILENAME):
            with open(STORAGE_FILENAME, 'rb') as f:
                try:
                    self.__dict__ = pickle.load(f)
                except :
                    print("Config file error")

    def save_data(self):
            with open(STORAGE_FILENAME, 'wb') as f:
                pickle.dump(self.__dict__, f)

storage = Storage()
storage.load_data()