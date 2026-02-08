# -*- coding: utf-8 -*-
"""
Конфигурация бота
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота (получить у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# ID администраторов (получать заказы)
# Формат: ADMIN_IDS=[916788192,8160753336] или ADMIN_ID=123456789 (для одного)
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "").strip()
ADMIN_ID_STR = os.getenv("ADMIN_ID", "0").strip()  # Для обратной совместимости

ADMIN_IDS = []

# Парсим ADMIN_IDS (формат: [id1,id2] или [id1, id2])
if ADMIN_IDS_STR:
    try:
        # Убираем квадратные скобки и пробелы, разделяем по запятым
        admin_ids_cleaned = ADMIN_IDS_STR.strip("[]")
        if admin_ids_cleaned:
            admin_ids_list = [
                int(id_str.strip()) 
                for id_str in admin_ids_cleaned.split(",") 
                if id_str.strip()
            ]
            ADMIN_IDS = admin_ids_list
    except (ValueError, AttributeError):
        ADMIN_IDS = []

# Если ADMIN_IDS не указан, проверяем ADMIN_ID (для обратной совместимости)
if not ADMIN_IDS and ADMIN_ID_STR:
    try:
        admin_id = int(ADMIN_ID_STR.strip())
        if admin_id:
            ADMIN_IDS = [admin_id]
    except ValueError:
        ADMIN_IDS = []

# Для обратной совместимости: первый ID (если есть)
ADMIN_ID = ADMIN_IDS[0] if ADMIN_IDS else 0

# Sanity CMS
SANITY_PROJECT_ID = os.getenv("SANITY_PROJECT_ID", "").strip()
SANITY_DATASET = os.getenv("SANITY_DATASET", "").strip()
SANITY_API_VERSION = os.getenv("SANITY_API_VERSION", "").strip()
