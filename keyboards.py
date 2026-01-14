# -*- coding: utf-8 -*-
"""
Клавиатуры для бота
Все кнопки через InlineKeyboard
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import get_categories, get_products_by_category, get_product_name


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню с категориями"""
    categories = get_categories()
    buttons = []
    
    # Создаем кнопки для каждой категории
    for category in categories:
        buttons.append([InlineKeyboardButton(
            text=category,
            callback_data=f"category_{category}"
        )])
    
    # Кнопка корзины (если есть товары)
    buttons.append([InlineKeyboardButton(
        text="🛒 Корзина",
        callback_data="view_cart"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_products_keyboard(category: str) -> InlineKeyboardMarkup:
    """Клавиатура с товарами категории"""
    products = get_products_by_category(category)
    buttons = []
    
    # Создаем кнопки для каждого товара с отображением цены
    for product in products:
        product_name = get_product_name(product)
        product_price = product.get("price", 0)
        # Форматируем текст кнопки: "Название - Цена₽"
        button_text = f"{product_name} - {product_price}₽"
        buttons.append([InlineKeyboardButton(
            text=button_text,
            callback_data=f"product_{category}_{product_name}"
        )])
    
    # Кнопка "Назад"
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
