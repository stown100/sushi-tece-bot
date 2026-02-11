# -*- coding: utf-8 -*-
"""
Сервис для загрузки категорий и товаров из Sanity CMS
"""
import logging
from typing import List, Dict, Any
import requests

from config import SANITY_PROJECT_ID, SANITY_DATASET, SANITY_API_VERSION

logger = logging.getLogger(__name__)

CATEGORIES_QUERY = '''*[_type == "category"] | order(order asc, slug asc) {
  _id,
  slug,
  name,
  order
}'''

PRODUCTS_QUERY = '''*[_type == "product"] | order(category->order asc, category->slug asc, slug asc) {
  _id,
  slug,
  name,
  description,
  "category": category->slug,
  subcategory,
  price,
  weight,
  image,
  badge,
  "recommendations": recommendations[]->slug
}'''


def _run_query(query: str) -> List[Dict[str, Any]]:
    """Выполнить GROQ-запрос к Sanity"""
    url = (
        f"https://{SANITY_PROJECT_ID}.api.sanity.io"
        f"/v{SANITY_API_VERSION}/data/query/{SANITY_DATASET}"
    )
    try:
        response = requests.get(url, params={"query": query}, timeout=30)
        response.raise_for_status()
        data = response.json()
        result = data.get("result", [])
        return result if isinstance(result, list) else []
    except requests.RequestException as e:
        logger.error("Ошибка запроса к Sanity: %s", e)
        return []
    except (ValueError, KeyError) as e:
        logger.error("Ошибка парсинга ответа Sanity: %s", e)
        return []


def fetch_categories() -> List[Dict[str, Any]]:
    """Загружает категории из Sanity (*[_type == "category"])"""
    return _run_query(CATEGORIES_QUERY)


def fetch_products() -> List[Dict[str, Any]]:
    """Загружает products из Sanity CMS"""
    return _run_query(PRODUCTS_QUERY)
