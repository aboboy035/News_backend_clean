
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News


async def is_favorite(news_id:int,user_id,db:AsyncSession):
    query = select(Favorite).where(Favorite.user_id == user_id,Favorite.news_id == news_id)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


async def add_favorite(news_id:int,user_id,db:AsyncSession):
    favorite = Favorite(user_id=user_id,news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


async def remove_favorite(news_id:int,user_id,db:AsyncSession):
    query = delete(Favorite).where(Favorite.user_id == user_id,Favorite.news_id == news_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0

async def get_favorites(db:AsyncSession,user_id,page:int,page_size:int):
    query = select(func.count()).where(Favorite.user_id == user_id)
    result = await db.execute(query)
    total = result.scalars().one()

    offset = (page - 1)*page_size
    query = (select(News,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id"))
             .join(Favorite,Favorite.news_id == News.id)
             .where(Favorite.user_id == user_id)
             .order_by(Favorite.created_at.desc())
             .offset(offset)
             .limit(page_size))

    result = await db.execute(query)
    news_list = result.all()
    return news_list,total

async def clear_favorites(db:AsyncSession,user_id):
    query = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount or 0