from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from db import db_main
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отмена'))

submit_button = ReplyKeyboardMarkup(resize_keyboard=True,
                                    row_width=2).add(KeyboardButton('Да'), KeyboardButton('Нет'))
class fsm(StatesGroup):
    product_id = State()
    size = State()
    quantity = State()
    phone_number = State()
    submit = State()


async def start_fsm(message: types.Message):
    await message.answer('Укажите название или бренд товара: ', reply_markup=cancel_button)
    await fsm.product_id.set()


async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await message.answer('Введите размер товара: ')
    await fsm.next()

async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await message.answer('Введите количество товара: ')
    await fsm.next()


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await message.answer('Введите контактные данные: ')
    await fsm.next()

async def load_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    await message.answer(
        caption=f'Название/Бренд товара: {data["name_products"]}\n'
                f'Размер товара: {data["size"]}\n'
                f'Категория товара: {data["category"]}\n'
                f'Стоимость: {data["price"]}\n'
                f'Артикул: {data["product_id"]}\n'
                f'Описание товара: {data["info_product"]}\n',
        reply_markup=submit_button)

    await fsm.next()

async def submit(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()

    if message.text == 'Да':
        async with state.proxy() as data:
            await message.answer('Отлично, Данные в базе!', reply_markup=kb)
            await db_main.sql_insert_products(data['product_id'],
                                              data['size'],
                                              data['category'],
                                              data['phone_number'])

            await state.finish()

    elif message.text == 'Нет':
        await message.answer('Хорошо, заполнение данных завершено!', reply_markup=kb)
        await state.finish()

    else:
        await message.answer('Выберите "Да" или "Нет"')


    def register_order(dp: Dispatcher):
        dp.register_message_handler(start_fsm, commands=['store'])
        dp.register_message_handler(load_product_id, state=fsm.product_id)
        dp.register_message_handler(load_size, state=fsm.size)
        dp.register_message_handler(load_quantity, state=fsm.quantity)
        dp.register_message_handler(load_phone_number, state=fsm.phone_number)
        dp.register_message_handler(submit, state=fsm.submit)