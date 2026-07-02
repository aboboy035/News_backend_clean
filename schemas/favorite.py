from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.news import NewsItemBase


class FavoriteCheckResponse(BaseModel):
     is_favorites: bool = Field(...,alias="isFavorite",description="是否收藏")


class FavoriteAddRequest(BaseModel):
     news_id: int = Field(...,alias="newsId",description="新闻ID")


class FavoriteNewsResponse(NewsItemBase):
     favorite_id: int = Field(...,alias="favoriteId",description="收藏ID")
     favorite_time:datetime = Field(...,alias="favoriteTime",description="收藏时间")
     model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FavoriteListResponse(BaseModel):
     list:list[FavoriteNewsResponse]
     total: int
     has_more: bool = Field(...,alias="hasMore",description="是否有更多")
     model_config = ConfigDict(from_attributes=True,populate_by_name= True)