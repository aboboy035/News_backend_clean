

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.favorite import is_favorite, add_favorite, remove_favorite, get_favorites, clear_favorites
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteListResponse
from utils.get_current_user import get_current_user
from utils.responses import success_response

router = APIRouter(prefix="/api/favorite",tags=["favorite"])





@router.get("/check")
async def check_favorite(
        news_id:int = Query(...,alias="newsId"),
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)):
    is_favorites = await is_favorite(news_id,user.id,db)
    return success_response(message="获取收藏状态成功",data=FavoriteCheckResponse(isFavorite=is_favorites))


@router.post("/add")
async def add_favorites(
        data: FavoriteAddRequest,
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)):
    is_favorites = await is_favorite(data.news_id,user.id,db)
    if is_favorites:
        raise HTTPException(status_code=400,detail="已收藏")
    result = await add_favorite(data.news_id,user.id,db)
    return success_response(message="收藏成功",data = result)


@router.delete("/remove")
async def remove_favorites(
        news_id:int = Query(...,alias="newsId"),
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)):
    result = await remove_favorite(news_id,user.id,db)
    if not result:
        raise HTTPException(status_code=400,detail="未收藏")
    return success_response(message="取消收藏成功",data = result)


@router.get("/list")
async def get_favorite(
        page:int,
        page_size:int = Query(...,alias="pageSize"),
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)):
    news_list,total = await get_favorites(db,user.id,page,page_size)
    favorite_list = [
        {
            **news.__dict__,
            "favorite_time":favorite_time,
            "favorite_id":favorite_id
        } for news,favorite_time,favorite_id in news_list
    ]
    has_more = total > page * page_size
    return success_response(message="获取收藏列表成功",data=FavoriteListResponse(list=favorite_list,total=total,hasMore=has_more))

@router.delete("/clear")
async def clear_favorite(
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)):
    total = await clear_favorites(db,user.id)

    return success_response(message=f"成功清空{total}收藏")