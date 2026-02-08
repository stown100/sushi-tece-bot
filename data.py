# -*- coding: utf-8 -*-
"""
Данные о товарах
Загружает products из Sanity CMS
Структура: категории с подкатегориями, товары с slug, name, price
Язык меню: ru
"""
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Union

from services.sanity import fetch_products

# Язык для меню
LANG = "ru"

# Маппинг slug (category/subcategory из Sanity) -> отображаемое название с иконками
# Ключи в нижнем регистре для поиска
MENU_LABELS: Dict[str, str] = {
    # Категории
    "sets": "📦 Сеты",
    "rolls": "🍣 Роллы",
    "sushi": "🍣 Суши",
    "tempura": "🍤 Темпура",
    "ramen": "🍜 Рамен",
    "wok": "🥢 WOK",
    "burgers": "🍔 Бургеры",
    "mochi": "🍡 Моти",
    "pasta-risotto": "🍝 Паста и ризотто",
    "hot-dishes": "🍗 Горячие блюда",
    "pizza": "🍕 Пиццы",
    "utensils": "🍴 Приборы",
    # Подкатегории
    "sushi-burger": "🍔 Суши бургер",
    "philadelphia": "🧀 Филадельфия",
    "california": "🥑 Калифорния",
    "maki": "🍙 Маки",
    "futo-maki": "🍣 Футо маки",
    "nigiri": "🍥 Нигири",
    "baked-rolls": "🔥 Запечённые роллы",
}


def _menu_label(slug: str) -> str:
    """Возвращает отображаемое название по slug или исходный slug"""
    if not slug:
        return slug
    key = slug.strip().lower()
    return MENU_LABELS.get(key, slug)


# Структура: {category: [products]} или {category: {subcategory: [products]}}
# Каждый product: {slug, name, price, ...}
PRODUCTS: Dict[str, Union[List[Dict], Dict[str, List[Dict]]]] = {}

# slug -> цена
PRODUCT_PRICES: Dict[str, int] = {}

# slug -> display name (ru)
SLUG_TO_NAME: Dict[str, str] = {}

# Маппинг индексов категорий
CATEGORY_INDEXES: Dict[int, str] = {}
CATEGORY_NAMES_TO_INDEX: Dict[str, int] = {}

# Маппинг индексов подкатегорий
SUBCATEGORY_INDEXES: Dict[int, Dict[int, str]] = {}
SUBCATEGORY_NAMES_TO_INDEX: Dict[int, Dict[str, int]] = {}


def _get_display_name(name_obj: Any) -> str:
    """Извлекает имя на языке LANG из объекта name Sanity"""
    if not name_obj:
        return ""
    if isinstance(name_obj, str):
        return name_obj
    return name_obj.get(LANG) or name_obj.get("ru") or name_obj.get("en") or ""


def _build_products_from_sanity(raw_products: List[Dict]) -> None:
    """
    Строит PRODUCTS из сырых данных Sanity.
    Группирует по category, затем по subcategory (если есть).
    """
    global PRODUCTS, PRODUCT_PRICES, SLUG_TO_NAME

    # Используем OrderedDict для сохранения порядка категорий/подкатегорий
    hierarchy: Dict[str, Union[List, Dict]] = OrderedDict()

    for p in raw_products:
        slug = p.get("slug") or p.get("_id", "")
        if not slug:
            continue

        category = (p.get("category") or "").strip()
        subcategory = (p.get("subcategory") or "").strip()
        price = int(p.get("price") or 0)
        name_obj = p.get("name")
        display_name = _get_display_name(name_obj) or slug

        product = {
            "slug": slug,
            "name": display_name,
            "price": price,
        }
        PRODUCT_PRICES[slug] = price
        SLUG_TO_NAME[slug] = display_name

        if not category:
            continue

        if subcategory:
            if category not in hierarchy:
                hierarchy[category] = OrderedDict()
            subcats = hierarchy[category]
            if not isinstance(subcats, dict):
                # Была категория без подкатегорий — переделываем
                existing_list = subcats if isinstance(subcats, list) else []
                hierarchy[category] = OrderedDict()
                hierarchy[category][""] = existing_list
                subcats = hierarchy[category]
            if subcategory not in subcats:
                subcats[subcategory] = []
            subcats[subcategory].append(product)
        else:
            if category not in hierarchy:
                hierarchy[category] = []
            subcats = hierarchy[category]
            if isinstance(subcats, dict):
                if "" not in subcats:
                    subcats[""] = []
                subcats[""].append(product)
            else:
                subcats.append(product)

    # Нормализуем: категории только с одной пустой подкатегорией "" -> список (без подкатегорий)
    for cat in list(hierarchy.keys()):
        val = hierarchy[cat]
        if isinstance(val, dict) and len(val) == 1 and "" in val:
            hierarchy[cat] = val[""]

    PRODUCTS.clear()
    PRODUCTS.update(hierarchy)


def _build_indexes() -> None:
    """Построить маппинги индексов"""
    global CATEGORY_INDEXES, CATEGORY_NAMES_TO_INDEX
    global SUBCATEGORY_INDEXES, SUBCATEGORY_NAMES_TO_INDEX

    CATEGORY_INDEXES.clear()
    CATEGORY_NAMES_TO_INDEX.clear()
    SUBCATEGORY_INDEXES.clear()
    SUBCATEGORY_NAMES_TO_INDEX.clear()

    for cat_idx, (category_name, category_data) in enumerate(PRODUCTS.items()):
        CATEGORY_INDEXES[cat_idx] = category_name
        CATEGORY_NAMES_TO_INDEX[category_name] = cat_idx

        if isinstance(category_data, dict):
            SUBCATEGORY_INDEXES[cat_idx] = {}
            SUBCATEGORY_NAMES_TO_INDEX[cat_idx] = {}
            for sub_idx, subcategory_name in enumerate(category_data.keys()):
                SUBCATEGORY_INDEXES[cat_idx][sub_idx] = subcategory_name
                SUBCATEGORY_NAMES_TO_INDEX[cat_idx][subcategory_name] = sub_idx


def _load_from_sanity() -> None:
    """Загружает данные из Sanity и строит индексы"""
    raw = fetch_products()
    _build_products_from_sanity(raw)
    _build_indexes()


# Инициализация при импорте
_load_from_sanity()


def get_categories() -> List[str]:
    """Возвращает список всех категорий"""
    return list(PRODUCTS.keys())


def get_category_index(category_name: str) -> int:
    """Возвращает индекс категории"""
    return CATEGORY_NAMES_TO_INDEX.get(category_name, -1)


def get_category_name(category_index: int) -> str:
    """Возвращает название категории по индексу"""
    return CATEGORY_INDEXES.get(category_index, "")


def has_subcategories(category: str) -> bool:
    """Проверяет, имеет ли категория подкатегории"""
    category_data = PRODUCTS.get(category)
    return isinstance(category_data, dict)


def get_subcategories(category: str) -> List[str]:
    """Возвращает список подкатегорий (включая пустую '' для товаров без подкатегории)"""
    category_data = PRODUCTS.get(category)
    if isinstance(category_data, dict):
        return list(category_data.keys())
    return []


def get_subcategory_index(category_index: int, subcategory_name: str) -> int:
    """Возвращает индекс подкатегории"""
    return SUBCATEGORY_NAMES_TO_INDEX.get(category_index, {}).get(subcategory_name, -1)


def get_subcategory_name(category_index: int, subcategory_index: int) -> str:
    """Возвращает название подкатегории"""
    return SUBCATEGORY_INDEXES.get(category_index, {}).get(subcategory_index, "")


def get_category_display_name(category_slug: str) -> str:
    """Отображаемое название категории с иконкой (например: sets -> 📦 Сеты)"""
    return _menu_label(category_slug)


def get_subcategory_display_name(category: str, subcategory: str) -> str:
    """Отображаемое название подкатегории с иконкой (пустая -> 'Прочее')"""
    if not subcategory:
        return "Прочее"
    return _menu_label(subcategory)


def get_products_by_category(category: str) -> List[Dict]:
    """Товары категории без подкатегорий"""
    category_data = PRODUCTS.get(category)
    if isinstance(category_data, list):
        return category_data
    return []


def get_products_by_subcategory(category: str, subcategory: str) -> List[Dict]:
    """Товары подкатегории"""
    category_data = PRODUCTS.get(category)
    if isinstance(category_data, dict):
        return category_data.get(subcategory, [])
    return []


def get_product_price(product_slug: str) -> int:
    """Цена товара по slug"""
    return PRODUCT_PRICES.get(product_slug, 0)


def get_product_name(product: Dict) -> str:
    """Display name товара из словаря"""
    return product.get("name", "")


def get_product_name_by_slug(slug: str) -> str:
    """Display name по slug (для корзины/заказов)"""
    return SLUG_TO_NAME.get(slug, slug)


def get_product_slug(product: Dict) -> str:
    """Slug товара из словаря"""
    return product.get("slug", "")
