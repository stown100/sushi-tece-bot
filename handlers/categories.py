# -*- coding: utf-8 -*-
"""
Обработчики выбора категорий и товаров
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import (
    get_main_menu_keyboard,
    get_products_keyboard,
    get_after_add_product_keyboard,
)
from services.cart import cart_service
from states import OrderStates
from data import get_product_price

router = Router()


@router.callback_query(F.data == "back_to_menu", OrderStates.choosing_category)
@router.callback_query(F.data == "back_to_menu", OrderStates.choosing_product)
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    text = "🍽️ Выберите категорию:"
    await callback.message.edit_text(
        text=text,
        reply_markup=get_main_menu_keyboard()
    )
    await state.set_state(OrderStates.choosing_category)
    await callback.answer()


@router.callback_query(F.data.startswith("category_"), OrderStates.choosing_category)
async def choose_category(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора категории"""
    # Извлекаем название категории из callback_data
    category = callback.data.replace("category_", "")
    
    # Сохраняем выбранную категорию в состояние
    await state.update_data(category=category)
    
    # Показываем товары категории
    text = f"📋 {category}:\n\nВыберите товар:"
    await callback.message.edit_text(
        text=text,
        reply_markup=get_products_keyboard(category)
    )
    
    await state.set_state(OrderStates.choosing_product)
    await callback.answer()


@router.callback_query(F.data.startswith("product_"), OrderStates.choosing_product)
async def choose_product(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора товара"""
    # Извлекаем категорию и название товара
    # Формат: product_Категория_Название товара
    parts = callback.data.replace("product_", "").split("_", 1)
    if len(parts) != 2:
        await callback.answer("Ошибка при выборе товара", show_alert=True)
        return
    
    category = parts[0]
    product_name = parts[1]
    
    # Добавляем товар в корзину
    user_id = callback.from_user.id
    cart_service.add_product(user_id, product_name)
    
    # Получаем цену товара
    price = get_product_price(product_name)
    
    # Показываем сообщение об успешном добавлении
    text = (
        f"✅ Товар добавлен в корзину!\n\n"
        f"📦 {product_name}\n"
        f"💰 Цена: {price}₽"
    )
    
    await callback.message.edit_text(
        text=text,
        reply_markup=get_after_add_product_keyboard()
    )
    
    await callback.answer(f"{product_name} добавлен в корзину!")


@router.callback_query(F.data == "add_more")
async def add_more(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Добавить ещё'"""
    # Возвращаемся в главное меню
    text = "🍽️ Выберите категорию:"
    await callback.message.edit_text(
        text=text,
        reply_markup=get_main_menu_keyboard()
    )
    await state.set_state(OrderStates.choosing_category)
    await callback.answer()
