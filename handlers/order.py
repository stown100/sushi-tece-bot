# -*- coding: utf-8 -*-
"""
Обработчики оформления заказа
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards import get_contact_keyboard, get_main_menu_keyboard
from services.cart import cart_service
from services.order import order_service
from states import OrderStates
from config import ADMIN_ID

router = Router()


@router.callback_query(F.data == "confirm_order", OrderStates.confirming_order)
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    """Подтверждение заказа - запрос контакта"""
    user_id = callback.from_user.id
    
    if cart_service.is_empty(user_id):
        await callback.answer("Корзина пуста", show_alert=True)
        return
    
    # Показываем итоговый заказ и запрашиваем контакт
    text = cart_service.format_cart_message(user_id)
    text += "\n\n📱 Для оформления заказа отправьте ваш контакт:"
    
    await callback.message.edit_text(
        text=text,
        reply_markup=get_contact_keyboard()
    )
    
    await state.set_state(OrderStates.waiting_for_contact)
    await callback.answer()


@router.callback_query(F.data == "send_contact", OrderStates.waiting_for_contact)
async def request_contact(callback: CallbackQuery, state: FSMContext):
    """Запрос контакта через кнопку"""
    text = (
        "📱 Пожалуйста, отправьте ваш контакт, нажав на кнопку ниже:\n\n"
        "Или отправьте номер телефона текстом"
    )
    
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(
            text="📱 Отправить контакт",
            request_contact=True
        )]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await callback.message.answer(
        text=text,
        reply_markup=contact_keyboard
    )
    
    await callback.answer()


async def _process_order_completion(message: Message, state: FSMContext, phone: str):
    """Общая функция для завершения заказа"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Создаем заказ в системе
    order_id = order_service.create_order(
        user_id=user_id,
        username=username,
        first_name=first_name,
        phone=phone or "Не указан",
    )
    
    # Формируем заказ для администратора
    order_text = order_service.format_order_for_admin(
        user_id=user_id,
        username=username,
        first_name=first_name,
        phone=phone or "Не указан",
    )
    order_text += f"\n\n🆔 ID заказа: #{order_id}"
    
    # Отправляем заказ администратору
    if ADMIN_ID:
        try:
            await message.bot.send_message(chat_id=ADMIN_ID, text=order_text)
        except Exception as e:
            print(f"Ошибка отправки заказа администратору: {e}")
    
    # Очищаем корзину
    cart_service.clear_cart(user_id)
    
    # Убираем клавиатуру и показываем сообщение
    await message.answer(
        text="✅ Заказ принят! Мы свяжемся с вами в ближайшее время.",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Показываем главное меню
    await message.answer(
        text="🍽️ Выберите категорию:",
        reply_markup=get_main_menu_keyboard()
    )
    
    # Сбрасываем состояние
    await state.set_state(OrderStates.choosing_category)


@router.message(F.contact, OrderStates.waiting_for_contact)
async def process_contact(message: Message, state: FSMContext):
    """Обработка полученного контакта"""
    contact = message.contact
    phone = contact.phone_number if contact else None
    
    # Если контакт не пришел, пробуем получить из текста
    if not phone:
        phone = message.text
    
    await _process_order_completion(message, state, phone)


@router.message(F.text, OrderStates.waiting_for_contact)
async def process_phone_text(message: Message, state: FSMContext):
    """Обработка номера телефона, отправленного текстом"""
    phone = message.text
    await _process_order_completion(message, state, phone)


@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    """Отмена заказа"""
    user_id = callback.from_user.id
    
    # Очищаем корзину
    cart_service.clear_cart(user_id)
    
    text = "❌ Заказ отменен\n\n🍽️ Выберите категорию:"
    await callback.message.edit_text(
        text=text,
        reply_markup=get_main_menu_keyboard()
    )
    
    await state.set_state(OrderStates.choosing_category)
    await callback.answer("Заказ отменен")
