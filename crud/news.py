from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News


async def get_categories(db:AsyncSession,skip:int = 0,limit:int = 100,):
    results = await db.execute(select(Category).offset(skip).limit( limit))
    return results.scalars().all()


async def get_news_list(db:AsyncSession, category_id,page, page_size):
    results = await db.execute(select(News).where(News.category_id == category_id).offset(page_size * (page - 1)).limit(page_size))
    return results.scalars().all()


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
