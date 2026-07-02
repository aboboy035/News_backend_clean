from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.history import add_histories, get_all_histories, delete_histories, clear_histories
from models.users import User
from schemas.history import HistoryAddRequest, HistoryListResponse
from utils.get_current_user import get_current_user
from utils.responses import success_response

router = APIRouter(prefix="/api/history",tags=["history"])


@router.post("/add")
async def add_history(
        news_id:HistoryAddRequest,
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)):
    history = await add_histories(news_id.news_id,user.id,db)
    return success_response(message="收藏成功",data = history)



@router.get("/list")
async def get_history(
        page:int = Query(1,ge=1),
        page_size:int = Query(10, ge=1, le=100,alias="pageSize"),
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)):
    news_list,total = await get_all_histories(db,user.id,page,page_size)
    history_list = [
        {
            **news.__dict__,
            "view_time":view_time,
            "history_id":history_id
        } for news,view_time,history_id in news_list
    ]
    has_more = total > page * page_size
    return success_response(message="获取浏览历史成功",data=HistoryListResponse(list=history_list,total=total,hasMore=has_more))

@router.delete("/delete/{history_id}")
async def delete_history(
        history_id:int,
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)):
    result = await delete_histories(history_id,user.id,db)
    if not result:
        raise HTTPException(status_code=400,detail="未收藏")
    return success_response(message="删除成功")

@router.delete("/clear")
async def clear_history(
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)):
    total = await clear_histories(db,user.id)
    return success_response(message=f"成功清空{total}条浏览历史")

