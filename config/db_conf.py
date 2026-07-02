from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
ASYNCIO_DATABASE_URL = "mysql+aiomysql://root:*********@localhost:3306/news_app?charset=utf8mb4"
async_engine = create_async_engine(
    ASYNCIO_DATABASE_URL,
    echo = True,
    pool_size = 10,
    max_overflow = 20
)


AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,
    class_= AsyncSession,
    expire_on_commit= False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()




