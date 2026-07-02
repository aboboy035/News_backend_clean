from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRequest(BaseModel):
    username: str
    password: str



class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50,description="昵称")
    avatar: Optional[str] = Field(None, max_length=255,description="头像URL")
    gender: Optional[str] = Field(None, max_length=10,description="性别")
    bio: Optional[str] = Field(None, max_length=500,description="个人简介")
    model_config = ConfigDict(from_attributes=True)



class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserAuthResponse(BaseModel):
    token: str
    userinfo: UserInfoResponse
    model_config = ConfigDict(from_attributes=True,populate_by_name= True)


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None


class UpdatePasswordRequest(BaseModel):
    old_password: str = Field(...,max_length=255,alias="oldPassword",description="旧密码")
    new_password: str = Field(...,max_length=255,alias="newPassword",description="新密码")