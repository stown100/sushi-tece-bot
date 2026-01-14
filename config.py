# -*- coding: utf-8 -*-
"""
Конфигурация бота
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота (получить у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# ID администратора (получать заказы)
ADMIN_ID_STR = os.getenv("ADMIN_ID", "0").strip()
try:
    ADMIN_ID = int(ADMIN_ID_STR) if ADMIN_ID_STR else 0
except ValueError:
    ADMIN_ID = 0

# Цены товаров теперь хранятся в data.py для каждого товара индивидуально
