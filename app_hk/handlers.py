from aiogram import Bot, Dispatcher, Router, F

from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
import app_hk.keyboards as kb
from dotenv import find_dotenv, load_dotenv # а не, все ок
import os
import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app_hk.keyboards import pizza_f_cust, users_order_busket
from aiogram.types import InputMediaPhoto # че это
from aiogram.filters.callback_data import CallbackData


# переписать часть с выдачей пицц, так как он ловит когда я нажимаю в админке на добавление
# пицц, а он ебащит мне выбор как при заказе

class ProductNav(CallbackData, prefix = 'nav'):
    category: str
    index: int

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
    await message.answer(f'Команды: /start, /help, /test_busket')

@router.message(Command('test_busket'))
async def test_buscket_tip(message: Message):
    await message.answer(f'TEST BUSCKET BY USER', kb.order_kb)

# команда /help с доступом к панели администратора
# для простых пользователей описание бота и с открытием возможности отправить жалобу и т.д.
@router.message(Command('help'))
async def help(message: Message):
    if message.from_user.id == int(os.getenv('ADMINID')):
        await message.answer('Открыт доступ к панели администратора.', reply_markup=kb.adminpaneledit)
        await message.answer('Вы можете зарегистироваться как администратор!')
    else:
        await message.answer('Это магазин пицц бла бла бла')

# подключение к бд
def pizzas_bd_connect():
    connection = sqlite3.connect('fastfood_database.db')
    cursor = connection.cursor() # МОГУ ПОТОМ ПЕРЕПИСАТЬ БОЛЕЕ УНИВЕРСАЛЬНО ЧЕРЕЗ IF - ELSE ПОД РАЗНЫЕ БД
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


# переписываю эту часть чтобы сделать более универсальной для всех продуктов
async def show_products(callback: CallbackQuery, index: int, category: str):
    products = pizzas_bd_connect()
    products = [p for p in products if p[-1] == category] # из 4 на -1
    if not products:
        await callback.message.answer('Пицц нет, приходите позже!')
        return
    # ограничение 0
    if index < 0:
        index = 0
    if index >=len(products):
        index = len(products)-1 # хзе
    product = products[index]

    # создаём актуальную клавиатуру
    kb = pizza_f_cust(index, len(products), products, category)

    await callback.message.edit_media(
        media= InputMediaPhoto(
            media=product[4],
            caption=f"Название: {product[1]}\nОписание: {product[2]}\nЦена: {product[3]}",
            parse_mode='Markdown'), reply_markup=kb
        )
    

    await callback.answer()

# вход в меню
@router.callback_query(F.data.startswith('menu_'))
async def category_start(callback: CallbackQuery):
    category = callback.data.split("_")[1]
    await show_products(callback, 0, category)

# листание
@router.callback_query(F.data.startswith("nav:"))
async def navifation(callback: CallbackQuery):
    _, category, index = callback.data.split(":")
    await show_products(callback, int(index), category)

# кнопка добавления в корзину пользователя
# ОСНОВНОЕ НАД ЧЕМ НАДО ПОРАБОТАТЬ
@router.callback_query(F.data.startswith("add:"))
async def user_basket_add(callback: CallbackQuery):
    _, category, product_id = callback.data.split(":") # мне не индекс бл нужен
    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor()
    user_order = (
        callback.from_user.id,
        callback.from_user.username,
        2,
        1,
        int(product_id), # тут в итоге ошибка
        category
    )
#    user_order = [callback.from_user.id, callback.from_user.username, 2, 2, index, category] # естественно не работает, там текст должен быть дебик
    cursor.execute(f'INSERT INTO orders VALUES (NULL, ?, ?, ?, ?, ?, ?)', (user_order))
#    cursor.execute(f'INSERT INTO orders (userid, user, price, count, name_product, product) VALUES ({callback.from_user.id}, name, 2, 2, {category[index]}, {category})')
    connection.commit()
    cursor.close()
    connection.close()


    callback.message.answer('Товар добавлен в корзину!')

# ПЕРЕПИСАТЬ ЧАСТЬ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ БД

# прописать клавиатуру для корзины пользователя
# копирую свою листалку 
# айди должен идти от пользователя
# тотал для всего списка заказов который сделал пользователь
# категория для сортировки какой продукт к какому идет
# также должен быть доп айди для продукта который будет подтягиваться из основной бд
# переписать так чтобы все заказы лежали в одной бд(пиццы, десерты, напитки)
# def users_order_busket(id_user: int, total: int, products, category: str, id_bd: int): # не уверен нужны ли категории

@router.callback_query(F.data.startswith('menu_'))
async def category_start(callback: CallbackQuery):
    category = callback.data.split("_")[1]
    await show_products(callback, 0, category)

# ПОТОМ ЧУТКА ПОМЕНЯТЬ И СДЕЛАТЬ ПОЧИЩЕ 
def user_order_test_db(userid):
    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor() # МОГУ ПОТОМ ПЕРЕПИСАТЬ БОЛЕЕ УНИВЕРСАЛЬНО ЧЕРЕЗ IF - ELSE ПОД РАЗНЫЕ БД
    # прописать чтобы в бд от количества менялся прайс(или сделать это отдельно)
    cursor.execute('SELECT price, count, name_product, product FROM orders WHERE userid = ?', (userid,)) # поменял с id на userid,
    orders_ = cursor.fetchone() # возвращает кортеж
    connection.close()
    return orders_

def connect_menu_database(product_id):
    connection = sqlite3.connect('fastfood_database.db')
    cursor = connection.cursor() # МОГУ ПОТОМ ПЕРЕПИСАТЬ БОЛЕЕ УНИВЕРСАЛЬНО ЧЕРЕЗ IF - ELSE ПОД РАЗНЫЕ БД
    # прописать чтобы в бд от количества менялся прайс(или сделать это отдельно)
    cursor.execute('SELECT name, description, price, photo, product FROM pizzas WHERE id = ?', (product_id,)) # поменял с id на userid,
    orders_ = cursor.fetchone() # возвращает кортеж
    connection.close()
    return orders_


# def user_order_test_db_connection(id): # бля в этом случае не понимаю как передать данные 
#     ordder_test = user_order_test_db(username=id) # ??????????????????????????????????????????????????????????????
#     first_al = ordder_test[0]
#     last_al = ordder_test[-1] # id: int, total: int, products, category: str
#     menu_user_orders = users_order_busket(ordder_test.id(first_al), ordder_test.total(last_al), ) # не помню правильно тут или нет( с ласт индексом) # поменял с index на total
#     return menu_user_orders


@router.callback_query(F.data == "orders")
async def user_orders(callback: CallbackQuery):
    await show_user_orders(callback, 0)

@router.callback_query(F.data.startswith("orders_nav:"))
async def orders_navigation(callback: CallbackQuery):
    index = int(callback.data.split(':')[1])
    await show_user_orders(callback, index)


#@router.callback_query(F.data.startswith("orders:"))
async def show_user_orders(callback: CallbackQuery, index: int):
    user_busket_id = user_order_test_db(userid=callback.from_user.id)
    if not user_busket_id:
        await callback.message.answer('ниче не заказано так-то')
        return
    if index < 0:
        index = 0
    if index >= len(user_busket_id):
        index = len(user_busket_id) - 1

    order = user_busket_id[index]
    price, count, product_id, category = order
    product = connect_menu_database(product_id=product_id)

    name = product[0]
    description = product[1]
    kb = users_order_busket(index, len(user_busket_id), user_busket_id)

    await callback.message.edit_text(
        f"🧺 {name}\n\n"
        f"{description}\n\n"
        f"Количество: {count}\n"
        f"Цена: {price * count}",
        reply_markup=kb
    )

    await callback.answer()
    
    
    






    # user_order_buscket_onlain = user_order_test_db(username=callback.from_user.id)
    # _, category, product_id = callback.data.split(":")
    
    # if user_order_buscket_onlain:
    #     await callback.message.answer('Ваша корзина')
    #     await callback.message.edit_media(
    #     media= InputMediaPhoto(
    #         media=user_order_buscket_onlain[4],
    #         caption=f"Название: {user_order_buscket_onlain[1]}\nОписание: {user_order_buscket_onlain[2]}\nЦена: {user_order_buscket_onlain[3]}",
    #         parse_mode='Markdown'), reply_markup=kb
    #     )
    # else:
    #         await callback.message.answer('Корзина пуста.')


    # products = [p for p in products if p[-1] == category] # из 4 на -1
    # if not products:
    #     await callback.message.answer('Пицц нет, приходите позже!')
    #     return
    # # ограничение 0
    # if index < 0:
    #     index = 0
    # if index >=len(products):
    #     index = len(products)-1 # хзе
    # product = products[index]

    # # создаём актуальную клавиатуру
    # kb = pizza_f_cust(index, len(products), products, category)

    # await callback.message.edit_media(
    #     media= InputMediaPhoto(
    #         media=product[4],
    #         caption=f"Название: {product[1]}\nОписание: {product[2]}\nЦена: {product[3]}",
    #         parse_mode='Markdown'), reply_markup=kb
    #     )
    

    # await callback.answer()
    # ПЕРЕПИСАТЬ ЭТУ ЧАСТЬ НА ТО ЧТО ВМЕСТО ID Я БУДУ БРАТЬ НАЗВАНИЕ ПРОДУКТА






#    await show_products(callback, int(index), category)

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
@router.callback_query(F.data == 'adding') # CHANGED ADDING FROM ADD
async def add_p(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы нажали кнопку добавления товара!')
    await state.set_state(AddNewProducts.product)
    await callback.message.answer('Выберите категорию:', reply_markup=kb.choose_add_shop) 
    # все ок, работает и для десертов


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

#@router.callback_query()