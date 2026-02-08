# -*- coding: utf-8 -*-
"""
Клавиатуры для бота
Все кнопки через InlineKeyboard
Поддерживает категории с подкатегориями
Использует индексы в callback_data для экономии места
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import (
    get_categories,
    get_products_by_category,
    get_subcategories,
    get_products_by_subcategory,
    get_product_name,
    has_subcategories,
    get_category_index,
    get_subcategory_index,
    get_subcategory_display_name,
    get_category_display_name,
)


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню с категориями"""
    categories = get_categories()
    buttons = []
    
    # Создаем кнопки для каждой категории
    for category in categories:
        cat_idx = get_category_index(category)
        display_name = get_category_display_name(category)
        buttons.append([InlineKeyboardButton(
            text=display_name,
            callback_data=f"cat_{cat_idx}"
        )])
    
    # Кнопка корзины (если есть товары)
    buttons.append([InlineKeyboardButton(
        text="🛒 Корзина",
        callback_data="view_cart"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_subcategories_keyboard(category: str) -> InlineKeyboardMarkup:
    """Клавиатура с подкатегориями категории"""
    subcategories = get_subcategories(category)
    buttons = []
    
    cat_idx = get_category_index(category)
    
    # Создаем кнопки для каждой подкатегории
    for subcategory in subcategories:
        sub_idx = get_subcategory_index(cat_idx, subcategory)
        display_name = get_subcategory_display_name(category, subcategory)
        buttons.append([InlineKeyboardButton(
            text=display_name,
            callback_data=f"sub_{cat_idx}_{sub_idx}"
        )])
    
    # Кнопка "Назад"
    buttons.append([InlineKeyboardButton(
        text="◀️ Назад",
        callback_data="back_to_menu"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_products_keyboard(category: str, subcategory: str = None) -> InlineKeyboardMarkup:
    """Клавиатура с товарами категории или подкатегории"""
    if subcategory:
        # Товары подкатегории
        products = get_products_by_subcategory(category, subcategory)
    else:
        # Товары категории (без подкатегорий)
        products = get_products_by_category(category)
    
    buttons = []
    
    cat_idx = get_category_index(category)
    
    # Создаем кнопки для каждого товара с отображением цены
    for idx, product in enumerate(products):
        product_name = get_product_name(product)
        product_price = product.get("price", 0)
        # Форматируем текст кнопки: "Название - Цена TL"
        button_text = f"{product_name} - {product_price} TL"
        
        # Формируем callback_data в зависимости от наличия подкатегории
        if subcategory:
            sub_idx = get_subcategory_index(cat_idx, subcategory)
            callback_data = f"prod_{cat_idx}_{sub_idx}_{idx}"
        else:
            callback_data = f"prod_{cat_idx}_{idx}"
        
        buttons.append([InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        )])
    
    # Кнопка "Назад"
    if subcategory:
        # Если есть подкатегория, возвращаемся к списку подкатегорий
        buttons.append([InlineKeyboardButton(
            text="◀️ Назад",
            callback_data=f"cat_{cat_idx}"
        )])
    else:
        # Если нет подкатегории, возвращаемся в главное меню
        buttons.append([InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="back_to_menu"
        )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_after_add_product_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура после добавления товара в корзину"""
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ Добавить ещё",
                callback_data="add_more"
            ),
            InlineKeyboardButton(
                text="🛒 Заказать",
                callback_data="checkout"
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️ Назад",
                callback_data="back_to_menu"
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_cart_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для корзины"""
    buttons = [
        [
            InlineKeyboardButton(
                text="✅ Заказать",
                callback_data="checkout"
            ),
            InlineKeyboardButton(
                text="🗑️ Очистить корзину",
                callback_data="clear_cart"
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️ Назад",
                callback_data="back_to_menu"
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_confirm_order_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для подтверждения заказа"""
    buttons = [
        [
            InlineKeyboardButton(
                text="✅ Подтвердить заказ",
                callback_data="confirm_order"
            ),
            InlineKeyboardButton(
                text="❌ Отменить",
                callback_data="cancel_order"
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_contact_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для запроса контакта"""
    buttons = [
        [
            InlineKeyboardButton(
                text="📱 Отправить контакт",
                callback_data="send_contact"
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ Отменить заказ",
                callback_data="cancel_order"
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
