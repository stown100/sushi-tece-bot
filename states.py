# -*- coding: utf-8 -*-
"""
FSM состояния для управления диалогом с пользователем
"""
from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    """Состояния процесса заказа"""
    # Выбор категории, подкатегории и товаров
    choosing_category = State()
    choosing_subcategory = State()
    choosing_product = State()
    
    # Оформление заказа
    confirming_order = State()
    waiting_for_contact = State()
