# -*- coding: utf-8 -*-
"""
Данные о товарах
Легко расширяемая структура для добавления новых категорий и товаров
Каждый товар имеет свое название и индивидуальную цену
Поддерживает категории с подкатегориями
"""

# Структура товаров: 
# - Если категория имеет подкатегории: {category: {subcategory: [{name, price}, ...]}}
# - Если категория без подкатегорий: {category: [{name, price}, ...]}
PRODUCTS = {
    "📦 Сеты": [
        {"name": "Мега сет", "price": 3000},
        {"name": "Гурман сет", "price": 2500},
        {"name": "Color Boom Set", "price": 1000},
        {"name": "Арт сет", "price": 1500},
        {"name": "Тёплый микс сет", "price": 1350},
        {"name": "Top Hit Set", "price": 1200},
        {"name": "Микс вкусов сет", "price": 1800},
        {"name": "Бум сет", "price": 3500},
    ],
    "🍣 Суши и роллы": {
        "🍔 Суши бургер": [
            {"name": "Рыбный микс", "price": 270},
            {"name": "Креветка", "price": 270},
        ],
        "🧀 Филадельфия": [
            {"name": "Фила манго", "price": 360},
            {"name": "Фила со свежим лососем", "price": 360},
            {"name": "Фила в икре", "price": 360},
            {"name": "Фила с тунцом", "price": 360},
            {"name": "Фила креветка темпура", "price": 360},
        ],
        "🥑 Калифорния": [
            {"name": "Калифорния лосось", "price": 320},
            {"name": "Калифорния креветка варёная", "price": 320},
        ],
        "🍙 Маки": [
            {"name": "Мак с лососем", "price": 150},
            {"name": "Мак с креветкой", "price": 150},
        ],
        "🍣 Футо маки": [
            {"name": "Футо мак с крабом", "price": 250},
            {"name": "Футо мак с креветкой", "price": 250},
        ],
        "🍥 Нигири": [
            {"name": "Нигири тунец", "price": 90},
            {"name": "Нигири лосось", "price": 90},
        ],
        "🔥 Запечённые роллы": [
            {"name": "С лососем", "price": 300},
            {"name": "Со свежим лососем", "price": 300},
            {"name": "С креветкой", "price": 300},
        ],
    },
    "🍤 Темпура": [
        {"name": "Краб", "price": 390},
        {"name": "Лосось", "price": 390},
        {"name": "Том Ям", "price": 300},
    ],
    "🍜 Рамен": [
        {"name": "С говядиной", "price": 500},
        {"name": "С креветкой", "price": 500},
        {"name": "С курицей", "price": 500},
    ],
    "🥢 WOK": [
        {"name": "С курицей и овощами", "price": 420},
        {"name": "С креветкой и овощами", "price": 420},
        {"name": "С говядиной и овощами", "price": 420},
    ],
    "🍔 Бургеры": [
        {"name": "Бургер YM", "price": 350},
        {"name": "Бургер Cheese YM", "price": 350},
    ],
    "🍡 Моти": [
        {"name": "Фисташка–малина", "price": 150},
        {"name": "Манго–маракуйя", "price": 150},
        {"name": "Клубника", "price": 150},
        {"name": "Лесной орех", "price": 150},
    ],
    "🍝 Паста и ризотто": [
        {"name": "Фетучини с лососем", "price": 480},
        {"name": "Фетучини с курицей и грибами", "price": 450},
        {"name": "Паста с морепродуктами", "price": 480},
        {"name": "Ризотто с морепродуктами", "price": 480},
    ],
    "🍗 Горячие блюда": [
        {"name": "Кальмары в панировке", "price": 450},
        {"name": "Курица в соусе терияки", "price": 450},
    ],
}

# Словарь для быстрого доступа к цене по названию товара
# {product_name: price}
PRODUCT_PRICES = {}

# Маппинг индексов категорий на названия
CATEGORY_INDEXES = {}
# Обратный маппинг: название -> индекс
CATEGORY_NAMES_TO_INDEX = {}

# Маппинг индексов подкатегорий на названия (для каждой категории)
SUBCATEGORY_INDEXES = {}
# Обратный маппинг: (category_index, subcategory_index) -> название
SUBCATEGORY_NAMES_TO_INDEX = {}


def _build_indexes():
    """Построить маппинги индексов для категорий и подкатегорий"""
    global CATEGORY_INDEXES, CATEGORY_NAMES_TO_INDEX, SUBCATEGORY_INDEXES, SUBCATEGORY_NAMES_TO_INDEX
    
    cat_idx = 0
    for category_name, category_data in PRODUCTS.items():
        CATEGORY_INDEXES[cat_idx] = category_name
        CATEGORY_NAMES_TO_INDEX[category_name] = cat_idx
        
        if isinstance(category_data, dict):
            # Категория с подкатегориями
            if cat_idx not in SUBCATEGORY_INDEXES:
                SUBCATEGORY_INDEXES[cat_idx] = {}
            if cat_idx not in SUBCATEGORY_NAMES_TO_INDEX:
                SUBCATEGORY_NAMES_TO_INDEX[cat_idx] = {}
            
            sub_idx = 0
            for subcategory_name, products in category_data.items():
                SUBCATEGORY_INDEXES[cat_idx][sub_idx] = subcategory_name
                SUBCATEGORY_NAMES_TO_INDEX[cat_idx][subcategory_name] = sub_idx
                sub_idx += 1
        
        cat_idx += 1


def _build_product_prices():
    """Построить словарь цен товаров"""
    for category_data in PRODUCTS.values():
        if isinstance(category_data, list):
            # Категория без подкатегорий
            for product in category_data:
                PRODUCT_PRICES[product["name"]] = product["price"]
        elif isinstance(category_data, dict):
            # Категория с подкатегориями
            for subcategory_products in category_data.values():
                for product in subcategory_products:
                    PRODUCT_PRICES[product["name"]] = product["price"]


_build_indexes()
_build_product_prices()


# Получить все категории
def get_categories():
    """Возвращает список всех категорий"""
    return list(PRODUCTS.keys())


# Получить индекс категории по названию
def get_category_index(category_name: str) -> int:
    """Возвращает индекс категории"""
    return CATEGORY_NAMES_TO_INDEX.get(category_name, -1)


# Получить название категории по индексу
def get_category_name(category_index: int) -> str:
    """Возвращает название категории по индексу"""
    return CATEGORY_INDEXES.get(category_index, "")


# Проверить, имеет ли категория подкатегории
def has_subcategories(category: str) -> bool:
    """Проверяет, имеет ли категория подкатегории"""
    category_data = PRODUCTS.get(category)
    return isinstance(category_data, dict)


# Получить подкатегории категории
def get_subcategories(category: str):
    """Возвращает список подкатегорий для указанной категории"""
    category_data = PRODUCTS.get(category)
    if isinstance(category_data, dict):
        return list(category_data.keys())
    return []


# Получить индекс подкатегории
def get_subcategory_index(category_index: int, subcategory_name: str) -> int:
    """Возвращает индекс подкатегории"""
    return SUBCATEGORY_NAMES_TO_INDEX.get(category_index, {}).get(subcategory_name, -1)


# Получить название подкатегории по индексу
def get_subcategory_name(category_index: int, subcategory_index: int) -> str:
    """Возвращает название подкатегории по индексу"""
    return SUBCATEGORY_INDEXES.get(category_index, {}).get(subcategory_index, "")


# Получить товары категории (если нет подкатегорий)
def get_products_by_category(category: str):
    """Возвращает список товаров для указанной категории (без подкатегорий)"""
    category_data = PRODUCTS.get(category)
    if isinstance(category_data, list):
        return category_data
    return []


# Получить товары подкатегории
def get_products_by_subcategory(category: str, subcategory: str):
    """Возвращает список товаров для указанной подкатегории"""
    category_data = PRODUCTS.get(category)
    if isinstance(category_data, dict):
        return category_data.get(subcategory, [])
    return []


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
