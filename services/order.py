# -*- coding: utf-8 -*-
"""
Сервис для работы с заказами
"""
from typing import Dict, Optional, List
from datetime import datetime
from services.cart import cart_service


class OrderService:
    """Сервис для работы с заказами"""
    
    def __init__(self):
        # Хранилище заказов: {order_id: order_data}
        # order_data = {
        #     'order_id': int,
        #     'user_id': int,
        #     'username': str,
        #     'first_name': str,
        #     'phone': str,
        #     'items': [(product_name, quantity, total_price), ...],
        #     'total_sum': int,
        #     'timestamp': datetime,
        #     'status': str  # 'new', 'processing', 'completed', 'cancelled'
        # }
        self._orders: Dict[int, dict] = {}
        self._next_order_id = 1
    
    def create_order(
        self,
        user_id: int,
        username: Optional[str],
        first_name: Optional[str],
        phone: Optional[str],
    ) -> int:
        """
        Создает новый заказ и возвращает его ID
        """
        # Получаем данные корзины
        items = cart_service.get_cart_items(user_id)
        total_sum = cart_service.get_total_sum(user_id)
        
        order_id = self._next_order_id
        self._next_order_id += 1
        
        order_data = {
            'order_id': order_id,
            'user_id': user_id,
            'username': username or "не указан",
            'first_name': first_name or "не указано",
            'phone': phone or "не указан",
            'items': items,
            'total_sum': total_sum,
            'timestamp': datetime.now(),
            'status': 'new',
        }
        
        self._orders[order_id] = order_data
        return order_id
    
    def get_order(self, order_id: int) -> Optional[dict]:
        """Получить заказ по ID"""
        return self._orders.get(order_id)
    
    def get_all_orders(self) -> List[dict]:
        """Получить все заказы, отсортированные по времени (новые первыми)"""
        return sorted(
            self._orders.values(),
            key=lambda x: x['timestamp'],
            reverse=True
        )
    
    def update_order_status(self, order_id: int, status: str) -> bool:
        """Обновить статус заказа"""
        if order_id in self._orders:
            self._orders[order_id]['status'] = status
            return True
        return False
    
    def format_order_for_admin(
        self,
        user_id: int,
        username: Optional[str],
        first_name: Optional[str],
        phone: Optional[str],
    ) -> str:
        """
        Форматирует заказ для отправки администратору
        """
        # Получаем данные корзины
        items = cart_service.get_cart_items(user_id)
        total_sum = cart_service.get_total_sum(user_id)
        
        # Формируем сообщение
        lines = ["🆕 Новый заказ!\n"]
        lines.append("👤 Клиент:")
        lines.append(f"   ID: {user_id}")
        if first_name:
            lines.append(f"   Имя: {first_name}")
        if username:
            lines.append(f"   Username: @{username}")
        if phone:
            lines.append(f"   Телефон: {phone}")
        
        lines.append("\n📦 Заказ:")
        for product_name, quantity, total_price in items:
            lines.append(f"   • {product_name} x{quantity} = {total_price}₽")
        
        lines.append(f"\n💰 Итого: {total_sum}₽")
        
        return "\n".join(lines)
    
    def format_order_details(self, order: dict) -> str:
        """Форматирует детали заказа для отображения"""
        lines = []
        lines.append(f"📋 Заказ #{order['order_id']}")
        lines.append(f"🕐 {order['timestamp'].strftime('%d.%m.%Y %H:%M')}")
        lines.append(f"📊 Статус: {self.get_status_emoji(order['status'])} {order['status']}\n")
        
        lines.append("👤 Клиент:")
        lines.append(f"   ID: {order['user_id']}")
        lines.append(f"   Имя: {order['first_name']}")
        lines.append(f"   Username: @{order['username']}")
        lines.append(f"   Телефон: {order['phone']}\n")
        
        lines.append("📦 Заказ:")
        for product_name, quantity, total_price in order['items']:
            lines.append(f"   • {product_name} x{quantity} = {total_price}₽")
        
        lines.append(f"\n💰 Итого: {order['total_sum']}₽")
        
        return "\n".join(lines)
    
    def format_orders_list(self, orders: List[dict]) -> str:
        """Форматирует список заказов"""
        if not orders:
            return "📭 Заказов пока нет"
        
        lines = [f"📋 Всего заказов: {len(orders)}\n"]
        
        for order in orders:
            status_emoji = self.get_status_emoji(order['status'])
            timestamp = order['timestamp'].strftime('%d.%m.%Y %H:%M')
            lines.append(
                f"{status_emoji} Заказ #{order['order_id']} | "
                f"{order['total_sum']}₽ | {timestamp} | "
                f"@{order['username']}"
            )
        
        return "\n".join(lines)
    
    def get_status_emoji(self, status: str) -> str:
        """Получить эмодзи для статуса"""
        status_emojis = {
            'new': '🆕',
            'processing': '⏳',
            'completed': '✅',
            'cancelled': '❌',
        }
        return status_emojis.get(status, '📋')


# Глобальный экземпляр сервиса заказов
order_service = OrderService()
