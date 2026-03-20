from backend.config import settings
from backend.connectors.redis_connector import RedisConnector


redis_connector = RedisConnector(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)