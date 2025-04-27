from news.repository import NewsMySQLRepository
from news.service import NewsService


async def news_service():
    return NewsService(NewsMySQLRepository)
