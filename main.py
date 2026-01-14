# -*- coding: utf-8 -*-
"""
Главный файл для запуска Telegram-бота
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN

# Импортируем роутеры
from handlers import start, categories, cart, order, admin

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Основная функция запуска бота"""
    
    # Проверяем наличие токена
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не установлен!")
        logger.error("📝 Создайте файл .env и добавьте в него:")
        logger.error("   BOT_TOKEN=your_bot_token_here")
        logger.error("💡 Получить токен можно у @BotFather в Telegram")
        return
    
    # Проверяем формат токена (должен содержать : и быть достаточно длинным)
    if ":" not in BOT_TOKEN or len(BOT_TOKEN) < 40:
        logger.error("❌ BOT_TOKEN имеет неверный формат!")
        logger.error("📝 Токен должен выглядеть примерно так: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
        logger.error("💡 Проверьте файл .env и убедитесь, что токен указан правильно")
        return
    
    # Инициализация бота и диспетчера
    try:
        bot = Bot(token=BOT_TOKEN)
    except Exception as e:
        logger.error(f"❌ Ошибка при создании бота: {e}")
        logger.error("💡 Проверьте правильность токена в файле .env")
        return
    storage = MemoryStorage()  # Хранилище состояний в памяти
    dp = Dispatcher(storage=storage)
    
    # Регистрируем роутеры
    dp.include_router(start.router)
    dp.include_router(categories.router)
    dp.include_router(cart.router)
    dp.include_router(order.router)
    dp.include_router(admin.router)  # Команды администратора
    
    logger.info("Бот запущен и готов к работе!")
    
    # Запускаем polling
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
