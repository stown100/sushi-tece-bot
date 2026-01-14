# -*- coding: utf-8 -*-
"""
Обработчики корзины
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import (
    get_main_menu_keyboard,
    get_cart_keyboard,
    get_confirm_order_keyboard,
)
from services.cart import cart_service
from states import OrderStates

router = Router()


@router.callback_query(F.data == "view_cart")
async def view_cart(callback: CallbackQuery, state: FSMContext):
    """Просмотр корзины"""
    user_id = callback.from_user.id
    
    if cart_service.is_empty(user_id):
        text = "🛒 Ваша корзина пуста"
        await callback.message.edit_text(
            text=text,
            reply_markup=get_main_menu_keyboard()
        )
        await callback.answer("Корзина пуста")
        return
    
    # Форматируем корзину
    text = cart_service.format_cart_message(user_id)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=get_cart_keyboard()
    )
    
    await state.set_state(OrderStates.confirming_order)
    await callback.answer()


@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):
    """Оформление заказа"""
    user_id = callback.from_user.id
    
    if cart_service.is_empty(user_id):
        await callback.answer("Корзина пуста", show_alert=True)
        return
    
    # Показываем итоговый заказ
    text = cart_service.format_cart_message(user_id)
    text += "\n\n✅ Подтвердите заказ:"
    
    await callback.message.edit_text(
        text=text,
        reply_markup=get_confirm_order_keyboard()
    )
    
    await state.set_state(OrderStates.confirming_order)
    await callback.answer()


@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery, state: FSMContext):
    """Очистка корзины"""
    user_id = callback.from_user.id
    cart_service.clear_cart(user_id)
    
    text = "🗑️ Корзина очищена\n\n🍽️ Выберите категорию:"
    await callback.message.edit_text(
        text=text,
        reply_markup=get_main_menu_keyboard()
    )
    
    await state.set_state(OrderStates.choosing_category)
    await callback.answer("Корзина очищена")
