from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict

from schemas.news import NewsItemBase


class HistoryAddRequest(BaseModel):
    news_id: int = Field(...,alias="newsId",description="新闻ID")


class HistoryNewsResponse(NewsItemBase):
    history_id: int = Field(...,alias="historyId",description="浏览历史ID")
    view_time : datetime = Field(...,alias="viewTime")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class HistoryListResponse(BaseModel):
    list:list[HistoryNewsResponse]
    total: int
    has_more: bool = Field(...,alias="hasMore",description="是否有更多")
    model_config = ConfigDict(from_attributes=True,populate_by_name= True)