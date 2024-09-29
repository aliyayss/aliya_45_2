from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from db import db_main

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отмена'))

submit_button = ReplyKeyboardMarkup(resize_keyboard=True,
                                    row_width=2).add(KeyboardButton('Да'), KeyboardButton('Нет'))


class fsm(StatesGroup):
    name_products = State()
    category = State()
    size = State()
    price = State()
    product_id = State()
    info_product = State()
    photo_products = State()
    submit = State()


async def start_fsm(message: types.Message):
    await message.answer('Укажите название или бренд товара: ', reply_markup=cancel_button)
    await fsm.name_products.set()


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_products'] = message.text

    await message.answer('Введите размер товара: ')
    await fsm.next()


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await message.answer('Введите категорию товара: ')
    await fsm.next()


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await message.answer('Введите цену товара: ')
    await fsm.next()


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await message.answer('Введите артикул (он должен быть уникальным): ')
    await fsm.next()


async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await message.answer('Напишите описание товара: ')
    await fsm.next()


async def load_info_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info_product'] = message.text
    await message.answer('Отправьте фото:')
    await fsm.next()


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await message.answer('Верные ли данные ?')
    await message.answer_photo(
        photo=data['photo'],
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
            await db_main.sql_insert_products(data['name_products'],
                                              data['category'],
                                              data['size'],
                                              data['price'],
                                              data['product_id'],
                                              photo=data['photo'])

            await state.finish()

    elif message.text == 'Нет':
        await message.answer('Хорошо, заполнение данных завершено!', reply_markup=kb)
        await state.finish()

    else:
        await message.answer('Выберите "Да" или "Нет"')


    def register_store(dp: Dispatcher):
        dp.register_message_handler(start_fsm, commands=['store'])
        dp.register_message_handler(load_name, state=fsm.name_products)
        dp.register_message_handler(load_size, state=fsm.size)
        dp.register_message_handler(load_category, state=fsm.category)
        dp.register_message_handler(load_price, state=fsm.price)
        dp.register_message_handler(load_product_id, state=fsm.product_id)
        dp.register_message_handler(load_info_product, state=fsm.info_product)
        dp.register_message_handler(load_photo, state=fsm.photo_products, content_types=['photo'])
        dp.register_message_handler(submit, state=fsm.submit)
