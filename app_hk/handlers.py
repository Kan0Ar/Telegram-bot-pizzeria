from aiogram import Bot, Dispatcher, Router, F

from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
import app_hk.keyboards as kb
from dotenv import find_dotenv, load_dotenv # а не, все ок
import os
import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app_hk.keyboards import pizza_f_cust
from aiogram.types import InputMediaPhoto # че это


# переписать часть с выдачей пицц, так как он ловит когда я нажимаю в админке на добавление
# пицц, а он ебащит мне выбор как при заказе



load_dotenv(find_dotenv())
router = Router()

class AddNewProducts(StatesGroup):
    product = State()
    name = State()
    description = State()
    price = State()
    photo = State()


# Базовая команда старт, с выводом айди юзера и с командами которые есть в боте
@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет!', reply_markup=kb.shop_1) # ??????????????????????????????????????????????????????
    await message.answer(f'Yours id: {message.from_user.id}')
    await message.answer(f'Команды: /start, /help')

# команда /help с доступом к панели администратора
# для простых пользователей описание бота и с открытием возможности отправить жалобу и т.д.
@router.message(Command('help'))
async def start(message: Message):
    if message.from_user.id == int(os.getenv('ADMINID')):
        await message.answer('Открыт доступ к панели администратора.', reply_markup=kb.adminpaneledit)
        await message.answer('Вы можете зарегистироваться как администратор!')
    else:
        await message.answer('Это магазин пицц бла бла бла')

# подключение к бд
def pizzas_bd_connect():
    connection = sqlite3.connect('fastfood_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, name, description, price, photo, product FROM pizzas') # убрал id
    pizzas = cursor.fetchall() # возвращает кортеж
    connection.close()
    return pizzas

# настройка индексов пицц и десертов 
# добавить также напитки
def pizzas_test_con_bd_and_keyboard(): # добавил в фукции без роутера асинхронность
    pizza = pizzas_bd_connect()
    first_al = pizza[0]
    last_al = pizza[-1]
    menu_keyboard = pizza_f_cust(pizza.index(first_al), pizza.total(last_al), pizza_name=pizza) # не помню правильно тут или нет( с ласт индексом) # поменял с index на total
    return menu_keyboard

# тут вывод позиций пицц
#@router.callback_query(lambda c: c.data and c.data.startswith("pizza_"))

async def show_pizza(callback: CallbackQuery, index: int):
    pizzas = pizzas_bd_connect()
    pizzas = [p for p in pizzas if p[-1] == 'pizza'] # из 4 на -1
    if not pizzas:
        await callback.message.answer('Пицц нет, приходите позже!')
        return
    # ограничение 0
    if index < 0:
        index = 0
    if index >=len(pizzas):
        index = len(pizzas)-1 # хзе
    pizza = pizzas[index]
    #photo_file = f'temp_{pizza[3]}' # это пока не трогаю, позже посмотрю что можно сделать
    #with open(photo_file, 'wb') as f:
        #f.write(photo_file)

    # создаём актуальную клавиатуру
    kb = pizza_f_cust(index, len(pizzas), pizzas)

    # обновляем сообщение
    await callback.message.edit_text( # потом вернуть с картинка + проверить работает ли если больше 1 позиции + сделать нейтрал функцию для шаблона под остальное
        f"Название: {pizza[1]}\nОписание: {pizza[2]}\nЦена: {pizza[3]}",
        reply_markup=kb
    )
#     await callback.message.edit_media(
#         media= InputMediaPhoto(
# #            media=pizza[3],
#             caption=f"Название: {pizza[0]}\nОписание: {pizza[1]}\nЦена:{pizza[2]}",
#             parse_mode='Markdown'),
#             reply_markup=kb
#         )
    

    await callback.answer()

# вход в меню
@router.callback_query(F.data == 'menu_pizza')
async def pizza_start(callback: CallbackQuery):
    await show_pizza(callback, index=0)

# листать
@router.callback_query(F.data.startswith("pizza_"))
async def pizza_navigation(callback: CallbackQuery):
    index = int(callback.data.split("_")[1])
    await show_pizza(callback, index)


# попробовать прописать функцию чтобы не писать дважды один и тот же код
# объединив данные


"""@router.callback_query(lambda c: c.data and c.data.startswith("pizza_"))
async def desert_navigation(callback: CallbackQuery):
    pizzas = pizzas_bd_connect()
    pizzas = [p for p in pizzas if p[4] == 'desert']
    if not pizzas:
        await callback.answer('Них нету(((')
        return
    await callback.answer('Вы нажали на кнопку десертов.')
    index = int(callback.data.split("_")[1])
    pizza = pizzas[index]
#    photo_file = f'temp_{pizza[3]}'
#    with open(photo_file, 'wb') as file:
#        file.write(photo_blob)
    

    # создаём актуальную клавиатуру
    kb = pizza_f_cust(index, len(pizzas), pizzas)

    # обновляем сообщение
    await callback.message.edit_media(
        media= InputMediaPhoto(
            media=pizza[3],
            caption=f"Название: {pizza[0]}\nОписание: {pizza[1]}\nЦена:{pizza[2]}",
            parse_mode='Markdown'),
        reply_markup=kb
        )
#        f"Название: {pizza[0]}\nОписание: {pizza[1]}\nЦена:{pizza[2]},", #{pizza[3]}",
#        reply_markup=kb

    await callback.answer()"""




    #, reply_markup=pizzas)
# так, мне нужно при нажатии на кнопку пиццы меня перекидывало на inline клавиатуру
# которая может листаться влево, Показ названия пиццы, вправо
# при достижении минимума или максимцума кнопка(лево, право) должна переставать работать
# добавить текст, картинки и тд,
# ДОБАВИТЬ КНОПКУ КОТОРАЯ КИДАЕТ ТОВАРЫ В КОРЗИНУ (и сумирует плату)



@router.message(F.text == 'Kuddos')
async def kuddos(message: Message):
    await message.answer('Вы нажали на кнопку лайков.')

@router.message(F.text == 'Admin Panel')
async def start(message: Message):
    await message.answer('Вы вошли в Панель Админа.', reply_markup=kb.admin_rules)


# Старт добавления
@router.callback_query(F.data == 'add')
async def add_p(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы нажали кнопку добавления товара!')
    await state.set_state(AddNewProducts.product)
    await callback.message.answer('Выберите категорию:', reply_markup=kb.choose_add_shop)


# Получаем, какую категорию выбрали
# тут хуйня, сделать универсальный ответ на добавление любого вида товара
@router.callback_query(AddNewProducts.product)
async def step_choose_product(callback: CallbackQuery, state: FSMContext):
    await state.update_data(product=callback.data)  # берем данные из callback.data!
    await state.set_state(AddNewProducts.name)
    await callback.message.answer('Введите название новой пиццы:')


# Название вводится текстом
@router.message(AddNewProducts.name)
async def step_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddNewProducts.description)
    await message.answer('Введите описание новой пиццы:')


@router.message(AddNewProducts.description)
async def step_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddNewProducts.price)
    await message.answer('Введите цену:')


@router.message(AddNewProducts.price)
async def step_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(AddNewProducts.photo)
    await message.answer('Отправьте фото пиццы:')


@router.message(AddNewProducts.photo)
async def step_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    all_prod = await state.get_data()

    # Отладочный вывод
    await message.answer(
        f"✅ Ваши данные:\n"
        f"Категория: {all_prod['product']}\n"
        f"Название: {all_prod['name']}\n"
        f"Описание: {all_prod['description']}\n"
        f"Цена: {all_prod['price']}"
    )
    # Запись в БД
    connection = sqlite3.connect('fastfood_database.db')
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pizzas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL,
            photo TEXT,
            product TEXT
        )
    """)
    cursor.execute(
        "INSERT INTO pizzas (product, name, description, price, photo) VALUES (?, ?, ?, ?, ?)",
        (all_prod['product'], all_prod['name'], all_prod['description'], all_prod['price'], all_prod['photo'])
    )
    connection.commit()
    connection.close()

    await state.clear()
    await message.answer('✅ Данные успешно добавлены в базу!')


# прописать добавление товаров, добавить кнопку add

@router.callback_query(F.data == 'add_into_backet')
async def user_card(callback: CallbackQuery):
    # сделать вызов бд для сохранения данных который пользователь добавил
    order = pizzas_bd_connect()
    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS orders(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   userid
                   user TEXT,
                   number INTEGER,
                   pizza TEXT,
                   desert TEXT
                   )
            """)
    cursor.execute("INSERT INTO orders (userrid, pizza) VALUES (?, ?)",
                   ()
                   )
    await callback.answer('Товар добавлен в корзину!')



# добавить кнопки для добавления, удаления товара(с добавлением fsmcontext(для цены картинки описания и т.д)), проверки количества товаров
# просмотр всех товаров с кнопками влево вправо, на главную
# дописать херню с админкой