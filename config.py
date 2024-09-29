from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


token = config('TOKEN')
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

admin = [531005109, ]
staff = [531005109, 906787989, 679043754, 812406795]