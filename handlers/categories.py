# -*- coding: utf-8 -*-
"""
Обработчики выбора категорий и товаров
Поддерживает категории с подкатегориями
Использует индексы в callback_data
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import (
    get_main_menu_keyboard,
    get_subcategories_keyboard,
    get_products_keyboard,
    get_after_add_product_keyboard,
)
from services.cart import cart_service
from states import OrderStates
from data import (
    get_product_price,
    has_subcategories,
    get_subcategories,
    get_category_name,
    get_subcategory_name,
    get_products_by_category,
    get_products_by_subcategory,
    get_product_name,
)


router = Router()


@router.callback_query(F.data == "back_to_menu", OrderStates.choosing_category)
@router.callback_query(F.data == "back_to_menu", OrderStates.choosing_subcategory)
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


@router.callback_query(F.data.startswith("cat_"), OrderStates.choosing_category)
@router.callback_query(F.data.startswith("cat_"), OrderStates.choosing_product)
async def choose_category(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора категории"""
    try:
        # Извлекаем индекс категории из callback_data
        # Формат: cat_0, cat_1, etc.
        cat_idx_str = callback.data.replace("cat_", "")
        try:
            cat_idx = int(cat_idx_str)
        except ValueError:
            await callback.answer("Ошибка: неверный формат категории", show_alert=True)
            return
        
        category = get_category_name(cat_idx)
        if not category:
            await callback.answer("Ошибка: категория не найдена", show_alert=True)
            return
        
        # Сохраняем выбранную категорию в состояние
        # Очищаем subcategory, если она была установлена ранее
        await state.update_data(
            category=category,
            category_index=cat_idx,
            subcategory=None,
            subcategory_index=None
        )
        
        # Проверяем, есть ли у категории подкатегории
        if has_subcategories(category):
            # Показываем подкатегории
            subcategories = get_subcategories(category)
            if not subcategories:
                await callback.answer("Ошибка: подкатегории не найдены", show_alert=True)
                return
            
            text = f"📋 {category}:\n\nВыберите подкатегорию:"
            keyboard = get_subcategories_keyboard(category)
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard
            )
            await state.set_state(OrderStates.choosing_subcategory)
        else:
            # Показываем товары категории напрямую
            text = f"📋 {category}:\n\nВыберите товар:"
            keyboard = get_products_keyboard(category)
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard
            )
            await state.set_state(OrderStates.choosing_product)
        
        await callback.answer()
    except Exception as e:
        import logging
        logging.error(f"Ошибка в choose_category: {e}", exc_info=True)
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)


@router.callback_query(F.data.startswith("sub_"), OrderStates.choosing_subcategory)
async def choose_subcategory(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора подкатегории"""
    try:
        # Извлекаем индексы категории и подкатегории из callback_data
        # Формат: sub_0_1 (cat_idx_sub_idx)
        parts = callback.data.replace("sub_", "").split("_")
        if len(parts) != 2:
            await callback.answer("Ошибка при выборе подкатегории", show_alert=True)
            return
        
        try:
            cat_idx = int(parts[0])
            sub_idx = int(parts[1])
        except ValueError:
            await callback.answer("Ошибка: неверный формат подкатегории", show_alert=True)
            return
        
        category = get_category_name(cat_idx)
        subcategory = get_subcategory_name(cat_idx, sub_idx)
        
        if not category or not subcategory:
            await callback.answer("Ошибка: подкатегория не найдена", show_alert=True)
            return
        
        # Сохраняем выбранную подкатегорию в состояние
        await state.update_data(
            category=category,
            category_index=cat_idx,
            subcategory=subcategory,
            subcategory_index=sub_idx
        )
        
        # Показываем товары подкатегории
        text = f"📋 {category} - {subcategory}:\n\nВыберите товар:"
        await callback.message.edit_text(
            text=text,
            reply_markup=get_products_keyboard(category, subcategory)
        )
        
        await state.set_state(OrderStates.choosing_product)
        await callback.answer()
    except Exception as e:
        import logging
        logging.error(f"Ошибка в choose_subcategory: {e}", exc_info=True)
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)


@router.callback_query(F.data.startswith("prod_"), OrderStates.choosing_product)
async def choose_product(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора товара"""
    try:
        # Получаем данные из состояния
        state_data = await state.get_data()
        category = state_data.get("category")
        subcategory = state_data.get("subcategory")
        cat_idx = state_data.get("category_index")
        
        if not category or cat_idx is None:
            await callback.answer("Ошибка: категория не выбрана", show_alert=True)
            return
        
        # Извлекаем информацию о товаре из callback_data
        # Формат с подкатегорией: prod_0_1_2 (cat_idx_sub_idx_prod_idx)
        # Формат без подкатегории: prod_0_2 (cat_idx_prod_idx)
        parts = callback.data.replace("prod_", "").split("_")
        
        if len(parts) < 2:
            await callback.answer("Ошибка при выборе товара", show_alert=True)
            return
        
        try:
            # Определяем наличие подкатегории по количеству частей в callback_data
            # Если 3 части - есть подкатегория, если 2 - нет подкатегории
            if len(parts) == 3:
                # Есть подкатегория: prod_cat_idx_sub_idx_prod_idx
                cat_idx_from_callback = int(parts[0])
                sub_idx = int(parts[1])
                prod_idx = int(parts[2])
                
                # Проверяем, что индекс категории совпадает
                if cat_idx_from_callback != cat_idx:
                    await callback.answer("Ошибка: несоответствие категории", show_alert=True)
                    return
                
                # Получаем название подкатегории по индексу
                subcategory_name = get_subcategory_name(cat_idx, sub_idx)
                if not subcategory_name:
                    await callback.answer("Ошибка: подкатегория не найдена", show_alert=True)
                    return
                
                products = get_products_by_subcategory(category, subcategory_name)
            elif len(parts) == 2:
                # Нет подкатегории: prod_cat_idx_prod_idx
                cat_idx_from_callback = int(parts[0])
                prod_idx = int(parts[1])
                
                # Проверяем, что индекс категории совпадает
                if cat_idx_from_callback != cat_idx:
                    await callback.answer("Ошибка: несоответствие категории", show_alert=True)
                    return
                
                products = get_products_by_category(category)
            else:
                await callback.answer("Ошибка: неверный формат товара", show_alert=True)
                return
        except ValueError as e:
            await callback.answer(f"Ошибка: неверный формат товара ({str(e)})", show_alert=True)
            return
        
        if prod_idx < 0 or prod_idx >= len(products):
            await callback.answer("Ошибка: товар не найден", show_alert=True)
            return
        
        product = products[prod_idx]
        product_name = get_product_name(product)
        
        # Добавляем товар в корзину
        user_id = callback.from_user.id
        cart_service.add_product(user_id, product_name)
        
        # Получаем цену товара
        price = get_product_price(product_name)
        
        # Показываем сообщение об успешном добавлении
        text = (
            f"✅ Товар добавлен в корзину!\n\n"
            f"📦 {product_name}\n"
            f"💰 Цена: {price} TL"
        )
        
        await callback.message.edit_text(
            text=text,
            reply_markup=get_after_add_product_keyboard()
        )
        
        await callback.answer(f"{product_name} добавлен в корзину!")
    except Exception as e:
        import logging
        logging.error(f"Ошибка в choose_product: {e}", exc_info=True)
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)


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
