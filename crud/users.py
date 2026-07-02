import uuid
from datetime import datetime, timedelta
from http.client import HTTPException

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User,UserToken
from schemas.users import UserUpdate
from utils import security
from utils.security import get_hash_password


async def get_user_by_username(db:AsyncSession,username):
    results = await db.execute(select(User).where(User.username == username))
    return results.scalar_one_or_none()


async def create_user(db:AsyncSession,userdata):
    hashed_password = get_hash_password(userdata.password)
    user = User(username=userdata.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_token(db:AsyncSession,user_id):
    token = str(uuid.uuid4())
    expire_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expire_at
        await db.commit()
    else:
        user_token = UserToken(user_id=user_id,token=token,expires_at=expire_at)
        db.add(user_token)
        await db.commit()
    return token

async def verify_user(db:AsyncSession,user_data):
    user = await get_user_by_username(db,user_data.username)
    if not user:
        return None
    if not security.verify_password(user_data.password,user.password):
        return None
    return user


async def get_user_by_token(db:AsyncSession,token):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if not user_token:
        return None
    if user_token.expires_at < datetime.now():
        return None
    query = select(User).where(User.id == user_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()



async def update_user_info(db:AsyncSession,username,user_data:UserUpdate):
    query = update(User).where(User.username == username).values(user_data.model_dump(exclude_none=True,exclude_unset=True))
    result = await db.execute(query)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404,detail="用户不存在")
    updated_user = await get_user_by_username(db,username)
    return updated_user


async def change_password(db:AsyncSession,user,old_password,new_password):
    if not security.verify_password(old_password,user.password):
        raise False
    hashed_password = get_hash_password(new_password)
    user.password = hashed_password
    await db.commit()
    await db.refresh(user)
    return True
