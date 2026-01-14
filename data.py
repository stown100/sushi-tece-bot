# -*- coding: utf-8 -*-
"""
Данные о товарах
Легко расширяемая структура для добавления новых категорий и товаров
Каждый товар имеет свое название и индивидуальную цену
"""

# Структура товаров: категория -> список словарей {name: str, price: int}
PRODUCTS = {
    "Наборы": [
        {"name": "Набор 1", "price": 500},
        {"name": "Набор 2", "price": 550},
        {"name": "Набор 3", "price": 600},
        {"name": "Набор 4", "price": 450},
        {"name": "Набор 5", "price": 650},
        {"name": "Набор 6", "price": 700},
        {"name": "Набор 7", "price": 580},
        {"name": "Набор 8", "price": 520},
    ],
    "Роллы": [
        {"name": "Ролл 1", "price": 350},
        {"name": "Ролл 2", "price": 380},
        {"name": "Ролл 3", "price": 320},
        {"name": "Ролл 4", "price": 400},
        {"name": "Ролл 5", "price": 360},
        {"name": "Ролл 6", "price": 340},
        {"name": "Ролл 7", "price": 370},
        {"name": "Ролл 8", "price": 390},
    ],
    "Бургеры": [
        {"name": "Бургер 1", "price": 400},
        {"name": "Бургер 2", "price": 450},
        {"name": "Бургер 3", "price": 420},
        {"name": "Бургер 4", "price": 480},
        {"name": "Бургер 5", "price": 380},
        {"name": "Бургер 6", "price": 460},
        {"name": "Бургер 7", "price": 440},
        {"name": "Бургер 8", "price": 410},
    ],
    "Напитки": [
        {"name": "Напиток 1", "price": 150},
        {"name": "Напиток 2", "price": 120},
        {"name": "Напиток 3", "price": 120},  # Одинаковая цена с напитком 2
        {"name": "Напиток 4", "price": 180},
        {"name": "Напиток 5", "price": 200},
        {"name": "Напиток 6", "price": 130},
        {"name": "Напиток 7", "price": 160},
        {"name": "Напиток 8", "price": 140},
    ],
}

# Словарь для быстрого доступа к цене по названию товара
# {product_name: price}
PRODUCT_PRICES = {}
for category_products in PRODUCTS.values():
    for product in category_products:
        PRODUCT_PRICES[product["name"]] = product["price"]


# Получить все категории
def get_categories():
    """Возвращает список всех категорий"""
    return list(PRODUCTS.keys())


# Получить товары категории
def get_products_by_category(category: str):
    """Возвращает список товаров для указанной категории"""
    return PRODUCTS.get(category, [])


# Получить цену товара по его названию
def get_product_price(product_name: str) -> int:
    """
    Возвращает цену товара по его названию
    """
    return PRODUCT_PRICES.get(product_name, 0)


# Получить название товара
def get_product_name(product: dict) -> str:
    """Получить название товара из словаря"""
    return product.get("name", "")
