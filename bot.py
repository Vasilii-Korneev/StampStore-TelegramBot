import telebot
import logging
import psycopg2
from psycopg2 import extras
from telebot import types
from config import host, user, password, db_name, port, BOT_TOKEN


# Получение токена для доступа к API бота
bot = telebot.TeleBot(BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

# Подключение к базе данных
try:
    connection = psycopg2.connect(host = host, user = user, password = password, database = db_name, port = port)
except Exception as _ex:
    print("Ошибка подключения к базе данных", _ex)

# Заполнение списка клиентов (пользователей)
users = [] # Список пользователей
cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor) # Настройка курсора с помощью DictCursor factory
cursor.execute("SELECT * FROM client") # запрос на получение списка пользователей
rows = cursor.fetchall() # метод возвращает список кортежей из последней выполненной инструкции из таблицы
for row in rows: # вставка строк в список
   users.append(dict(row))

users = { # Словарь для хранения логинов и паролей пользователей
"i.i.ivanov": "ivanov_password",
"p.p.petrov": "petrov_password"
}

user_sessions = {} # Сессии пользователей

# Заполнение списка истории заказов
orders_history = [] # Список заказов
cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor) # Настройка курсора с помощью DictCursor factory
cursor.execute("SELECT * FROM orders") # запрос на получение списка заказов
rows = cursor.fetchall() # метод возвращает список строк из последней выполненной инструкции из таблицы
for row in rows: # вставка строк в список
   orders_history.append(dict(row))
print(orders_history) # вывод списка клиентов

# Заполнение списков товаров
products = [] # Cписок товаров для заказа
catalog = [] # Cписок товаров для заказа
cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor) # Настройка курсора с помощью DictCursor factory
cursor.execute("SELECT * FROM product") # запрос на получение списка пользователей
rows = cursor.fetchall() # метод возвращает список строк из последней выполненной инструкции из таблицы
for row in rows: # вставка строк в списки
   products.append(dict(row))
   catalog.append(dict(row))
# print(products_to_order) # вывод списка клиентов

products = { # Словарь для хранения списка товаров
"Игры будущего": { "title": "Игры будущего", "price": 680, "quantity": 8, "image": "https://rusmarka.ru/files/resize/Z0C/300_300_0__files_sitedata_401_1439_138bdb42-5653-412a-9234-4831f7e93090_jpg_AD1A256C.jpg"},
"Дворец зимнего спорта Айсберг": { "title": "Дворец зимнего спорта «Айсберг»", "price": 67, "quantity": 1, "image": "https://rusmarka.ru/files/resize/ZEB/300_300_0__files_sitedata_401_1439_9027aca0-3071-452e-945d-a04e9afa1a38_jpg_7997F242.jpg"},
"Стадион Фишт": { "title": "Стадион «Фишт»", "price": 67, "quantity": 1, "image": "https://rusmarka.ru/files/resize/ZE0/300_300_0__files_sitedata_401_1439_6349d42b-fb2f-456e-96ee-ce563ae819d7_jpg_E2F8FCB6.jpg"},
"Дворец спорта Большой": { "title": "Дворец спорта «Большой»", "price": 67, "quantity": 1, "image": "https://rusmarka.ru/files/resize/Z04/300_300_0__files_sitedata_401_1439_1c14178e-240c-4eff-9288-d02e211da682_jpg_2D11DD9E.jpg"},
"Авиапочта": { "title": "Авиапочта", "price": 45, "quantity": 3, "image": "https://coinsmart.ru/wa-data/public/shop/products/53/71/37153/images/69061/69061.750.jpg"},
"Международный год Солнца": { "title": "Международный год Солнца", "price": 120, "quantity": 8, "image": "https://coinsmart.ru/wa-data/public/shop/products/98/93/29398/images/69088/69088.750.jpg"},
"Российская авиация Вертолеты": { "title": "Российская авиация - Вертолеты", "price": 140, "quantity": 6, "image": "https://coinsmart.ru/wa-data/public/shop/products/00/40/34000/images/65302/65302.750.jpg"},
"Советская гражданская авиация": { "title": "Советская гражданская авиация", "price": 165, "quantity": 1, "image": "https://coinsmart.ru/wa-data/public/shop/products/78/71/37178/images/69086/69086.750.jpg"},
"Всемирный год коммуникаций": { "title": "Всемирный год коммуникаций", "price": 90, "quantity": 4, "image": "https://coinsmart.ru/wa-data/public/shop/products/57/61/36157/images/67920/67920.750.jpg"},
"Народная армия Болгарии": { "title": "Народная армия Болгарии", "price": 60, "quantity": 3, "image": "https://coinsmart.ru/wa-data/public/shop/products/37/61/36137/images/67896/67896.750.jpg"},
}

catalog = { # Словарь для хранения каталога товаров
"Игры будущего": 680,
"Дворец зимнего спорта 'Айсберг'": 67,
"Стадион 'Фишт'": 67,
"Дворец спорта 'Большой'": 67,
"Авиапочта": 45,
"Международный год Солнца": 120,
"Российская авиация - Вертолеты": 140,
"Советская гражданская авиация": 165,
"Всемирный год коммуникаций": 90,
"Народная армия Болгарии": 60
}

# Словарь для хранения корзины пользователя (товар: количество)
user_basket = {}



# Обработчик команды /start
@bot.message_handler(commands=['start'])

def start(message): # Считывание логина пользователя
    user_id = message.chat.id
    user_sessions[user_id] = {"authenticated": False} # добавление сессии пользователя
    bot.send_message(user_id, "Добро пожаловать в интернет-магазин Маро4ка!\nДля начала давайте войдем в личный кабинет.\nВведите логин от Вашего личного кабинета:")
    bot.register_next_step_handler(message, check_login) # считывание логина

def check_login(message): # Считывание пароля польователя
    user_id = message.chat.id
    login = message.text
    if login in users:
        user_sessions[user_id]["login"] = login
        bot.send_message(user_id, "Отлично! Теперь введите пароль:")
        bot.register_next_step_handler(message, check_password)
    else:
        bot.send_message(user_id, "К сожалению, личный кабинет с таким логином не найден( \nПопробуйте снова.")
        start(message)

def check_password(message):
    user_id = message.chat.id
    password = message.text
    login = user_sessions[user_id]["login"]
    if users[login] == password:
        user_sessions[user_id]["authenticated"] = True
        bot.send_message(user_id, "Вы успешно вошли в личный кабинет! \nТеперь можно собрать новый заказ: /basket\nА для для поиска товаров к каталоге используйте /search")
    else:
        bot.send_message(user_id, "К сожалению, это неверный пароль( \nПопробуйте снова.")
        start(message)

@bot.message_handler(commands=['basket'])
def basket(message):
    user_id = message.chat.id
    user_basket[user_id] = {} # Создаем корзину для пользователя

    keyboard = types.InlineKeyboardMarkup()
    for item_id, price in catalog.items():
        key = types.InlineKeyboardButton(text=f"{item_id} - {price} руб", callback_data=item_id)
        keyboard.add(key)

    bot.send_message(user_id, "Выберите товар для добавления в корзину:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def add_to_basket(call):
    user_id = call.message.chat.id
    product_name = call.data

    if product_name in catalog:
        if product_name in user_basket[user_id]:
            user_basket[user_id][product_name] += 1
        else:
            user_basket[user_id][product_name] = 1

    bot.send_message(user_id, f"{product_name} добавлен в корзину.\nДля оформления заказа: /order")

@bot.message_handler(commands=['order'])
def show_order(message):
    user_id = message.chat.id
    if user_basket[user_id]:
        total_price = 0
        cart_items = ""
        for item, quantity in user_basket[user_id].items():
            price = catalog[item] * quantity
            cart_items += f"{item} - {quantity} шт. - {price} руб\n"
            total_price += price

        bot.send_message(user_id, f"История заказов:\n{cart_items}\nИтого: {total_price} руб")
    else:
        bot.send_message(user_id, "Корзина пуста.")

# Обработчик команды поиска - /search
@bot.message_handler(commands=['search'])
def search_items(message):
    bot.send_message(message.chat.id, "Введите наименование товара:")
    bot.register_next_step_handler(message, process_search)

def process_search(message):
    item_id = message.text
    if item_id in products:
        item = products[item_id]
        response = f"Найден товар: '{item['title']}'\nЦена: {item['price']} руб.\nКоличетсво марок (в блоке): {item['quantity']}"
        bot.send_message(message.chat.id, response)
        bot.send_photo(message.chat.id, item['image'])
    else:
        response = "Такого товара не нашлось в каталоге(\nДля повторного поиска /search"
        bot.send_message(message.chat.id, response)

bot.polling() # бесконечно выполняющийся цикл запросов к серверам Telegram