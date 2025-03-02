import asyncio
import pickle
import os

STORAGE_FILENAME = "config.pickle"

class Storage:

    def __init__(self):
        self.bot_key : str = ""
        self.alarms : list[str, str, list[str]] = []
        self.text_reactions : list[(str, str)] = []
        self.home_chat_id : int = None
        self.joy_old_post_ids : list[id] = []

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