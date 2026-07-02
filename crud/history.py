from datetime import datetime
from os.path import join

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def add_histories(news_id:int,user_id,db:AsyncSession):
    query = select(History).where(History.user_id == user_id,History.news_id == news_id)
    result = await db.execute(query)
    history = result.scalar_one_or_none()
    if history:
        history.view_time = datetime.now()
        await db.commit()
        await db.refresh(history)
        return history
    history = History(user_id=user_id,news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return  history


async def get_all_histories(db:AsyncSession,user_id,page:int,page_size:int):
    query = select(func.count()).where(History.user_id == user_id)
    result = await db.execute(query)
    total = result.scalars().one()

    offset = (page - 1)*page_size
    query = (select(News,History.view_time.label("view_time"),History.id.label("history_id"))
             .join(History,History.news_id == News.id)
             .where(History.user_id == user_id)
             .offset(offset)
             .limit(page_size))
    result = await db.execute(query)
    news_list = result.all()
    return news_list,total

async def delete_histories(history_id,user_id,db:AsyncSession):
    query = delete(History).where(History.user_id == user_id,History.id == history_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0

async def clear_histories(db:AsyncSession,user_id):
    query = delete(History).where(History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount or 0
