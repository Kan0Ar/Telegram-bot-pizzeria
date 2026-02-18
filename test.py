@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет!', reply_markup=kb.shop_1)
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
    cursor.execute('SELECT name, description, price, photo, product FROM pizzas')
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

async def show_pizza(callback: CallbackQuery, index: int):
    pizzas = pizzas_bd_connect()
    pizzas = [p for p in pizzas if p[-1] == 'pizza']

    if not pizzas:
        await callback.message.answer("Пицц нет")
        return

    # защита от выхода за границы
    if index < 0:
        index = 0
    if index >= len(pizzas):
        index = len(pizzas) - 1

    pizza = pizzas[index]
    kb = pizza_f_cust(index, len(pizzas), pizzas)

    await callback.message.edit_text(
        f"Название: {pizza[1]}\nОписание: {pizza[2]}\nЦена: {pizza[3]}",
        reply_markup=kb
    )

    await callback.answer()

# вход в меню
@router.callback_query(F.data == 'menu_pizza')
async def pizza_start(callback: CallbackQuery):
    await show_pizza(callback, index=0)

# листать
@router.callback_query(F.data.startwith("pizza_"))
async def pizza_navigation(callback: CallbackQuery):
    index = int(callback.data.split("_")[1])
    await show_pizza(callback, index)


и вот клава

# кнопки для выбора пицц и десертов для заказа(работают)
shop = ReplyKeyboardMarkup(keyboard=
                           [[KeyboardButton(text='Пиццы')], [KeyboardButton(text='Десерты')]], 
                           resize_keyboard=True, input_field_placeholder='А че писать')
# замена верхней клавы # ТУТ ТОЖЕ ПОМЕНЯЛ С PIZZA НА MENU_PIZZA
shop_1 = InlineKeyboardMarkup(inline_keyboard=
                              [[InlineKeyboardButton(text='Pizzas', callback_data='menu_pizza')], [InlineKeyboardButton(text='Deserts', callback_data='desert')]])


# это кнопки чтобы решить что добавить в меню админу
choose_add_shop = InlineKeyboardMarkup(inline_keyboard=
                           [[InlineKeyboardButton(text='Пиццы', callback_data='pizza')], [InlineKeyboardButton(text='Десерты', callback_data='desert')]])
# это кнопки для вызова админ панели
adminpaneledit = ReplyKeyboardMarkup(keyboard=
                                    [[KeyboardButton(text='Admin Panel')], [KeyboardButton(text='Shop')]], 
                                    resize_keyboard=True, input_field_placeholder='А че писать')
# это кнопки прав админа
admin_rules = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text='Удалить товар', callback_data='delete'), InlineKeyboardButton(text='Добавить товар', callback_data='add')], 
                                    [InlineKeyboardButton(text='Выйти из Панели Администратора', callback_data='exitadminpanel')]])
# это не рабочая хуйня
adding_new = ReplyKeyboardMarkup(keyboard=
                                    [[KeyboardButton(text='Новая пицца')], [KeyboardButton(text='Новый Десерт')], 
                                    [KeyboardButton(text='Новый напиток')]], resize_keyboard=True, input_field_placeholder='Нажми ты че')


def pizza_f_cust(index: int, total: int, pizzas):
    buttons = []

    if index > 0:
        buttons.append(
            InlineKeyboardButton(
                text='<--',
                callback_data=f'pizza_{index - 1}'
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=pizzas[index][1],  # имя
            callback_data='none'
        )
    )

    if index < total - 1:
        buttons.append(
            InlineKeyboardButton(
                text='-->',
                callback_data=f'pizza_{index + 1}'
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text='Добавить в корзину',
            callback_data=f'add_{pizzas[index][0]}'  # id из БД
        )
    )

    return InlineKeyboardMarkup(inline_keyboard=[buttons])