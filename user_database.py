import sqlite3


connection = sqlite3.connect('user_database.db')

cursor = connection.cursor()

def main():
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS orders(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    userid INTEGER,
                    user TEXT,
                    price INTEGER,
                    count INTEGER,
                    name_product TEXT,
                    product TEXT
                   )
            """) # потом добавить геопозицию или тип того
    # сделать отдельное бд для заказов чтобы можно было добавить данные оплаты
    # карта, анал
    connection.close()


if __name__ == '__main__':
    main()