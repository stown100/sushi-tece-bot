# -*- coding: utf-8 -*-
"""
Сервис для управления корзиной пользователя
Корзина хранится в памяти (словарь)
"""
from typing import Dict, List, Tuple
from data import get_product_price


class CartService:
    """Сервис для работы с корзиной"""
    
    def __init__(self):
        # Структура: {user_id: {product_name: quantity}}
        self._carts: Dict[int, Dict[str, int]] = {}
    
    def add_product(self, user_id: int, product_name: str) -> None:
        """Добавить товар в корзину"""
        if user_id not in self._carts:
            self._carts[user_id] = {}
        
        if product_name in self._carts[user_id]:
            self._carts[user_id][product_name] += 1
        else:
            self._carts[user_id][product_name] = 1
    
    def get_cart(self, user_id: int) -> Dict[str, int]:
        """Получить корзину пользователя"""
        return self._carts.get(user_id, {})
    
    def get_cart_items(self, user_id: int) -> List[Tuple[str, int, int]]:
        """
        Получить список товаров корзины с ценами
        Возвращает: [(product_name, quantity, total_price), ...]
        """
        cart = self.get_cart(user_id)
        items = []
        for product_name, quantity in cart.items():
            price = get_product_price(product_name)
            total_price = price * quantity
            items.append((product_name, quantity, total_price))
        return items
    
    def get_total_sum(self, user_id: int) -> int:
        """Получить итоговую сумму корзины"""
        items = self.get_cart_items(user_id)
        return sum(total_price for _, _, total_price in items)
    
    def clear_cart(self, user_id: int) -> None:
        """Очистить корзину пользователя"""
        if user_id in self._carts:
            del self._carts[user_id]
    
    def is_empty(self, user_id: int) -> bool:
        """Проверить, пуста ли корзина"""
        cart = self.get_cart(user_id)
        return len(cart) == 0
    
    def format_cart_message(self, user_id: int) -> str:
        """Форматировать корзину для отображения"""
        items = self.get_cart_items(user_id)
        if not items:
            return "Корзина пуста"
        
        lines = ["📦 Ваш заказ:\n"]
        for product_name, quantity, total_price in items:
            lines.append(
                f"• {product_name} x{quantity} = {total_price}₽"
            )
        
        total_sum = self.get_total_sum(user_id)
        lines.append(f"\n💰 Итого: {total_sum}₽")
        
        return "\n".join(lines)


# Глобальный экземпляр сервиса корзины
cart_service = CartService()
