import sqlite3 
from app_hk.keyboards import pizza_f_cust

connection = sqlite3.connect('fastfood_database.db')

cursor = connection.cursor()

# добавить пункт с картинками
def mainer():
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS pizzas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                price INTEGER,
                photo BLOB,
                product TEXT
                )
            """)
    connection.close()

def main():
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER,
                product 
                )
            """) # прописать какие боты и прочая херня должны быть в портфолио, сделать бота с парсингом + регистрацией на сайте

#if __name__ == '__main__':
#    main()








# добавить в бд картинки и тип товара(десерт, пицца, напиток)
# тип товара добавляется через inline клавиатуру для администратора
# по типу товара фильтруются данные и выводят при нажатии определенной кнопки
# поменять название вкладки для товаров


# чуть позже добавить номер телефона, и возможность показывать локации для доставки








"""def pizzas_bd_connect():
    connection = sqlite3.connect('fastfood_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name, description, price, photo, product FROM pizzas')
    pizzas = cursor.fetchall()
    connection.close()
    return pizzas

def pizzas_test_con_bd_and_keyboard():
    pizza = pizzas_bd_connect()
    first_al = pizza[0]
    last_al = pizza[-1]
    menu_keyboard = pizza_f_cust(pizza.index(first_al), pizza.index(last_al), pizza_name=pizza)
#    print(menu_keyboard)
    return menu_keyboard

def tesst(): # тут вызов команды пицц
    pizzas = pizzas_bd_connect()
    for p in pizzas:
        for product in p:
            if p == 'pizza':
                if not pizzas:
                    print('Нихуя нету(((')
                    return
                print('Вы нажали на кнопку пицц.')
            #    await message.answer('Выбирайте', reply_markup=pizzas_test_con_bd_and_keyboard())
                pizza = pizzas[0]
                kb = pizza_f_cust(0, len(pizzas), pizzas)
                print(kb)
                print(f'\n\n\n{pizza}')
                print(f'\n\n\n{pizzas}')
tesst()"""










"""def pizzas_bd_connect():
    connection = sqlite3.connect('fastfood_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name, description, price, photo, product FROM pizzas')
    pizzas = cursor.fetchall()
    connection.close()
    return pizzas

def pizzas_test_con_bd_and_keyboard():
    pizza = pizzas_bd_connect()
    for p in pizza:
        if p[4] == 'pizza':
            first_al = pizza[0]
            last_al = pizza[-1]
    print(f'{pizza}\n\n{first_al}\n{last_al}\n\n\n')
    menu_keyboard = pizza_f_cust(pizza.index(first_al), pizza.index(last_al), pizza_name=pizza)
    print(menu_keyboard)
    return menu_keyboard"""

#pizzas_test_con_bd_and_keyboard()





"""def pizzas_bd_connect():
    connection = sqlite3.connect('fastfood_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name, description, price FROM pizzas')
    pizzas = cursor.fetchall()
    connection.close()
    first_el = pizzas[0]
    print(pizzas.index(first_el))
    return pizzas

pizzas_bd_connect()"""


"""cursor.execute("SELECT id, name, description, price FROM pizzas")
pizzas = cursor.fetchall()
print(pizzas[index])
connection.close()"""
