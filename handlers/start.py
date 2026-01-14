# -*- coding: utf-8 -*-
"""
Обработчик команды /start
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards import get_main_menu_keyboard
from states import OrderStates

router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    """
    Обработчик команды /start
    Показывает главное меню с категориями
    """
    # Сбрасываем состояние
    await state.clear()
    
    text = (
        "🍽️ Добро пожаловать в наш ресторан!\n\n"
        "Выберите категорию:"
    )
    
    await message.answer(
        text=text,
        reply_markup=get_main_menu_keyboard()
    )
    
    # Устанавливаем состояние выбора категории
    await state.set_state(OrderStates.choosing_category)


@router.message(F.text == "/myid")
async def cmd_myid(message: Message):
    """
    Показывает ID пользователя (для получения ADMIN_ID)
    """
    user_id = message.from_user.id
    username = message.from_user.username or "не указан"
    first_name = message.from_user.first_name or "не указано"
    
    text = (
        f"🆔 Ваш Telegram ID: `{user_id}`\n\n"
        f"👤 Имя: {first_name}\n"
        f"📱 Username: @{username}\n\n"
        f"💡 Скопируйте ID и добавьте в .env файл:\n"
        f"`ADMIN_ID={user_id}`"
    )
    
    await message.answer(text, parse_mode="Markdown")
