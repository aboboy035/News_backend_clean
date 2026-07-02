from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import news, users, favorite, history
from utils.exception_handlers import register_exception_handlers

app = FastAPI(redirect_slashes=False)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)