import logging
from aiogram import types, Dispatcher
from aiogram.utils import executor
from config import dp, admin, bot
import fsm_staff
import order
import products
from db import db_main
async def on_startup(_):
    for i in admin:
        await bot.send_message(chat_id=i, text="Бот включен!")
        await db_main.sql_create()

async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Здравствуйте {message.from_user.first_name}!')

def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])

register_start(dp)

async def info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Этот бот помогает управлять товарами и принимать заказы.")

def register_info(dp: Dispatcher):
    dp.register_message_handler(info, commands=['info'])

register_info(dp)
fsm_staff.register_store(dp)
products.register_send_products_handler(dp)
order.register_order(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
