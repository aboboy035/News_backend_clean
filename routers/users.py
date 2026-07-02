from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.users import get_user_by_username, create_user, create_token, verify_user, update_user_info, change_password
from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdate, UpdatePasswordRequest
from utils.get_current_user import get_current_user
from utils.responses import success_response

router = APIRouter(prefix="/api/user",tags=["users"])


@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession = Depends(get_db),):
    existing_user = await get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=400,detail="用户已存在")
    user = await create_user(db,user_data)
    token = await create_token(db,user.id)
    response_data = UserAuthResponse(token = token,userinfo= UserInfoResponse.model_validate( user))
    return success_response(message="注册成功",data=response_data)


@router.post("/login")
async def login(user_data:UserRequest,db:AsyncSession = Depends(get_db)):
    user = await verify_user(db,user_data)
    if not user:
        raise HTTPException(status_code=401,detail="用户名或密码错误")
    token = await create_token(db,user.id)
    response_data = UserAuthResponse(token = token,userinfo= UserInfoResponse.model_validate( user))
    return success_response(message="登录成功",data=response_data)

@router.get("/info")
async def get_user_info(user:User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))



@router.put("/update")
async def update_user(user_info:UserUpdate,user:User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    user = await update_user_info(db,user.username,user_info)
    return success_response(message="更新用户信息成功",data=UserInfoResponse.model_validate(user))


@router.put("/password")
async def update_password(user_password:UpdatePasswordRequest,user:User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    result = await change_password(db,user,user_password.old_password,user_password.new_password)
    if not result:
        raise HTTPException(status_code=400,detail="旧密码错误")
    return success_response(message="更新密码成功")