from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.users import get_user_by_token


async def get_current_user(db:AsyncSession = Depends(get_db),authorization:str = Header(..., alias="Authorization")):
    token = authorization.replace("Bearer ", "")
    user = await get_user_by_token(db,token)
    if not user:
        raise HTTPException(status_code=401,detail="用户验证失败")
    return user



