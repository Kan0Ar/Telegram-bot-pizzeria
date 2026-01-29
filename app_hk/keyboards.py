from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
#from bd_test import bd_fastfood
import sqlite3



# кнопки для выбора пицц и десертов для заказа(работают)
shop = ReplyKeyboardMarkup(keyboard=
                           [[KeyboardButton(text='Пиццы')], [KeyboardButton(text='Десерты')]], 
                           resize_keyboard=True, input_field_placeholder='А че писать')


# это кнопки чтобы решить что добавить в меню
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


# этот пиздец для листания товаров <-- -->
def pizza_f_cust(index: int, total: int, pizza_name):
    buttons = []
    if index > 0:
        buttons.append(
            InlineKeyboardButton(text='<--', callback_data=f'pizza_{index - 1}')
        )
    buttons.append(
        InlineKeyboardButton(text=pizza_name[index][0], callback_data='none')
    )
    if index < total - 1:
        buttons.append(
            InlineKeyboardButton(text='-->', callback_data=f'pizza_{index + 1}')
        )
    buttons.append(
        InlineKeyboardButton(text ='Добавить в корзину', callback_data='add_into_backet')
    )
    menu = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return menu








"""def pizza_f_cust(index:int, total: int):
    buttons = []
    if index > 1:
        buttons.append(InlineKeyboardButton(text='<--', callback_data=f'pizza_{index - 1}'))
    buttons.append(InlineKeyboardButton(text=f'pizza_{index}', callback_data=f'pizza_{index}'))
    if index < total - 1:
        buttons.append(InlineKeyboardButton(text='-->', callback_data=f'pizza_{index + 1}'))
    menu = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return menu"""


"""async def pizzas_for_customers(index: int, total: int):
    buttons_for_pizzas = []
    index = 0
    if index > 0:
        buttons_for_pizzas.append(InlineKeyboardButton(text='  <--  ', callback_data=f'pizza{index-1}'))
    buttons_for_pizzas.append(InlineKeyboardButton(text=f'pizza{index+1}', callback_data='null'))
    if index < total -1:
        buttons_for_pizzas.append(InlineKeyboardButton(text='  -->  ', callback_data=f'pizza{index+1}'))
    return InlineKeyboardMarkup(inline_keyboard=[buttons_for_pizzas])"""
    




#pizzas_asker = InlineKeyboardMarkup(inline_keyboard=(
#                                    [[InlineKeyboardButton(text='Вперед', callback_data='')], [InlineKeyboardButton(text='Название?', callback_data='')], 
#                                    [InlineKeyboardButton(text='Назад', callback_data='')]], [InlineKeyboardButton(text='Добавить в корзину', callback_data='')]
#                                    ))