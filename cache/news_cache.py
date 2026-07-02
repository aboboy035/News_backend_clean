from typing import Dict, Any, List, Optional

from config.redis_conf import set_cache
from config.redis_conf import get_json_cache
CATEGORIES_KEY = "news:categories"
NEWS_LIST_KEY_PREX = "news:list:"

async def get_cached_categories():
    print("开始缓存新闻分类数据")
    return await get_json_cache(CATEGORIES_KEY)



async def set_cached_categories(data:List[Dict[str,Any]],expire:int = 7200):
    return await set_cache(CATEGORIES_KEY, data,expire)

async def get_cached_list(category_id: Optional[int], page: int, page_size: int):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_KEY_PREX}{category_part}:{page}:{page_size}"
    return await get_json_cache(key)




async def set_cached_list(category_id: Optional[int], page: int, page_size: int,data:List[Dict[str,Any]],expire:int = 1800):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_KEY_PREX}{category_part}:{page}:{page_size}"
    return await set_cache(key, data,expire)
