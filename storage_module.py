import asyncio
import pickle
import os
import logging

STORAGE_FILENAME = "config.pickle"

class Storage:

    bot_key : str
    alarms : list[str, str, list[str]]
    text_reactions : list[(str, str)]
    home_chat_id : int
    joy_old_post_ids : list[int]

    def load_data(self):
        if os.path.exists(STORAGE_FILENAME):
            with open(STORAGE_FILENAME, 'rb') as f:
                self.__dict__ = pickle.load(f)
        else:
            logging.warning("Config file not found. Initializing fresh storage.")
            self.alarms = []
            self.text_reactions = []
            self.joy_old_post_ids = []

    def save_data(self):
            with open(STORAGE_FILENAME, 'wb') as f:
                pickle.dump(self.__dict__, f)

storage = Storage()
