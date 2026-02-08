# -*- coding: utf-8 -*-
"""
Сервис для загрузки products из Sanity CMS
"""
import logging
from typing import List, Dict, Any, Optional
import requests

from config import SANITY_PROJECT_ID, SANITY_DATASET, SANITY_API_VERSION

logger = logging.getLogger(__name__)

GROQ_QUERY = '''*[_type == "product"] | order(category asc, slug asc) {
  _id,
  slug,
  name,
  description,
  category,
  subcategory,
  price,
  weight,
  image,
  badge,
  utensils,
  "recommendations": recommendations[]->slug
}'''


def fetch_products() -> List[Dict[str, Any]]:
    """
    Загружает products из Sanity CMS через GROQ API.
    Возвращает список сырых продуктов из Sanity.
    """
    url = (
        f"https://{SANITY_PROJECT_ID}.api.sanity.io"
        f"/v{SANITY_API_VERSION}/data/query/{SANITY_DATASET}"
    )
    params = {"query": GROQ_QUERY}

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        result = data.get("result", [])
        return result if isinstance(result, list) else []
    except requests.RequestException as e:
        logger.error("Ошибка загрузки products из Sanity: %s", e)
        return []
    except (ValueError, KeyError) as e:
        logger.error("Ошибка парсинга ответа Sanity: %s", e)
        return []
