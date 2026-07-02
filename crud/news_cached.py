from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_categories, set_cached_categories, get_cached_list, set_cached_list
from models.news import Category, News
from schemas.news import NewsItemBase


async def get_categories(db:AsyncSession,skip:int = 0,limit:int = 100,):
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories
    results = await db.execute(select(Category).offset(skip).limit( limit))
    categories = results.scalars().all()
    if categories:
        categories = jsonable_encoder( categories)
        await set_cached_categories(categories)
        print("缓存新闻分类数据成功")
    return categories


async def get_news_list(db:AsyncSession, category_id,page, page_size):
    cached_news_list = await get_cached_list(category_id,page,page_size)
    if cached_news_list:
        print("从缓存中获取新闻列表数据成功")
        return [News(**item) for item in cached_news_list]
    results = await db.execute(select(News).where(News.category_id == category_id).offset(page_size * (page - 1)).limit(page_size))
    news_list =  results.scalars().all()

    if news_list:
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json",by_alias=False) for item in news_list]
        # news_data = jsonable_encoder(news_list)
        await set_cached_list(category_id,page,page_size,news_data)
        print("缓存新闻列表数据成功")
    return news_list




async def get_news_count(db:AsyncSession, category_id):
    stmt=select(func.count(News.id)).where(News.category_id == category_id)
    results = await db.execute(stmt)
    return results.scalar_one()


async def get_news_detail(db:AsyncSession, news_id):
    results = await db.execute(select(News).where(News.id == news_id))
    return results.scalar_one_or_none()

async def increase_views(db:AsyncSession, news_id):
    stmt = update( News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount

async def get_related_news(db:AsyncSession, news_id,news_category_id,limit:int = 5):
    stmt = select(News).where(News.id != news_id , News.category_id == news_category_id).order_by(News.views.desc(),News.publish_time.desc()).limit(limit)
    results = await db.execute(stmt)
    return results.scalars().all()
