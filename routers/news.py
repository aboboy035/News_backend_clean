
from fastapi import APIRouter, Depends,Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import news, news_cached

router = APIRouter(prefix="/api/news",tags=["news"])


@router.get("/categories")
async def get_categories(db:AsyncSession = Depends(get_db),skip:int = 0,limit:int = 100):
    categories = await news_cached.get_categories(db,skip,limit)
    return {
        "code" : 200,
        "message":"success",
        "data":categories
    }

@router.get("/list")
async def get_news_list(
        db:AsyncSession = Depends(get_db),
        category_id:int = Query(...,alias="categoryId"),
        page:int = 1,
        page_size:int = Query(10,le=100,alias="pageSize")):
    news_list = await news_cached.get_news_list(db,category_id,page,page_size)
    total = await news.get_news_count(db,category_id)
    has_more = ((page -1)*page_size+len(news_list))< total
    return {
        "code" : 200,
        "message":"success",
        "data": {
            "list":news_list,
            "total": total,
            "hasMore": has_more

        }
    }


@router.get("/detail")
async def get_news_detail(
        db:AsyncSession = Depends(get_db),
        news_id:int = Query(...,alias="id")):
    news_detail = await news.get_news_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")

    views_res = await news.increase_views(db,news_id)
    if not views_res:
        raise HTTPException(status_code=404,detail="新闻不存在")
    related_news = await news.get_related_news(db,news_id,news_detail.category_id)
    return {
        "code" : 200,
        "message":"success",
        "data":{
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
            "categoryId":news_detail.category_id,
            "views":news_detail.views ,
            "relatedNews":related_news
        }
    }