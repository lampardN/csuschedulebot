from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# import os

# bot = Bot(token=os.getenv('TOKEN'))

storage = MemoryStorage()
bot = Bot(token='5341603217:AAGuno377Pa6gZMiHD8YQVz_NfQ7MN3QAAA')
dp = Dispatcher(bot, storage=storage)
