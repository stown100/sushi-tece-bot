# -*- coding: utf-8 -*-
"""
Обработчики команд администратора
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_IDS
from services.order import order_service

router = Router()


def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    return user_id in ADMIN_IDS


def _create_orders_keyboard(orders: list) -> InlineKeyboardMarkup:
    """Создать клавиатуру со списком заказов"""
    keyboard_buttons = []
    for order in orders[:10]:  # Показываем первые 10 заказов
        status_emoji = order_service.get_status_emoji(order['status'])
        keyboard_buttons.append([InlineKeyboardButton(
            text=f"{status_emoji} Заказ #{order['order_id']} - {order['total_sum']}₽",
            callback_data=f"order_detail_{order['order_id']}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def _create_order_status_keyboard(order_id: int, status: str) -> InlineKeyboardMarkup:
    """Создать клавиатуру для управления статусом заказа"""
    keyboard_buttons = []
    
    if status == 'new':
        keyboard_buttons.append([InlineKeyboardButton(
            text="⏳ В обработку",
            callback_data=f"order_status_{order_id}_processing"
        )])
    
    if status in ['new', 'processing']:
        keyboard_buttons.append([InlineKeyboardButton(
            text="✅ Завершить",
            callback_data=f"order_status_{order_id}_completed"
        )])
        keyboard_buttons.append([InlineKeyboardButton(
            text="❌ Отменить",
            callback_data=f"order_status_{order_id}_cancelled"
        )])
    
    keyboard_buttons.append([InlineKeyboardButton(
        text="◀️ Назад к списку",
        callback_data="back_to_orders"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


@router.message(F.text == "/orders")
async def cmd_orders(message: Message):
    """Показать все заказы (только для администратора)"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к этой команде")
        return
    
    # Получаем все заказы
    orders = order_service.get_all_orders()
    
    if not orders:
        await message.answer("📭 Заказов пока нет")
        return
    
    # Форматируем список заказов
    text = order_service.format_orders_list(orders)
    keyboard = _create_orders_keyboard(orders)
    
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("order_detail_"))
async def show_order_detail(callback: CallbackQuery):
    """Показать детали конкретного заказа"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ У вас нет доступа", show_alert=True)
        return
    
    # Извлекаем ID заказа
    order_id = int(callback.data.replace("order_detail_", ""))
    order = order_service.get_order(order_id)
    
    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return
    
    # Форматируем детали заказа
    text = order_service.format_order_details(order)
    keyboard = _create_order_status_keyboard(order['order_id'], order['status'])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("order_status_"))
async def update_order_status(callback: CallbackQuery):
    """Обновить статус заказа"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ У вас нет доступа", show_alert=True)
        return
    
    # Извлекаем ID заказа и новый статус
    parts = callback.data.replace("order_status_", "").split("_")
    if len(parts) != 2:
        await callback.answer("Ошибка", show_alert=True)
        return
    
    order_id = int(parts[0])
    new_status = parts[1]
    
    # Обновляем статус
    if order_service.update_order_status(order_id, new_status):
        order = order_service.get_order(order_id)
        if order:
            text = order_service.format_order_details(order)
            text += f"\n\n✅ Статус обновлен на: {new_status}"
            keyboard = _create_order_status_keyboard(order_id, order['status'])
            
            await callback.message.edit_text(text, reply_markup=keyboard)
            await callback.answer("Статус обновлен")
        else:
            await callback.answer("Заказ не найден", show_alert=True)
    else:
        await callback.answer("Ошибка обновления статуса", show_alert=True)


@router.callback_query(F.data == "back_to_orders")
async def back_to_orders(callback: CallbackQuery):
    """Вернуться к списку заказов"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ У вас нет доступа", show_alert=True)
        return
    
    # Получаем все заказы
    orders = order_service.get_all_orders()
    
    if not orders:
        await callback.message.edit_text("📭 Заказов пока нет")
        await callback.answer()
        return
    
    # Форматируем список заказов
    text = order_service.format_orders_list(orders)
    keyboard = _create_orders_keyboard(orders)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
