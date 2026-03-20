import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


from backend.api.dependencies import get_db
from backend.init import redis_connector

from backend.api.auth import router as auth_router
from backend.api.hotels import router as hotels_router
from backend.api.rooms import router as rooms_router
from backend.api.bookings import router as bookings_router
from backend.api.facilities import router as facilities_router
from backend.api.images import router as images_router


async def send_emails_bookings_today_checkin():
    async for db in get_db():
        await db.bookings.get_bookings_with_today_checkin()


async def run_send_emails_regularly():
    while True:
        await send_emails_bookings_today_checkin()
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(run_send_emails_regularly())
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    yield
    await redis_connector.close()


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(facilities_router)
app.include_router(bookings_router)
app.include_router(images_router)


"""
@app.get("/sync/{id}")
def sync(id: int):
    print(f"sync. Threads: {threading.active_count()}")
    print(f"sync. Started by {id}: {time.time():.2f}")
    time.sleep(3)
    print(f"sync. Finished by {id}: {time.time():.2f}")


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Threads: {threading.active_count()}")
    print(f"async. Started by {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async. Finished by {id}: {time.time():.2f}")
"""


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@2/bundles/redoc.standalone.js",
    )


@app.get("/")
def func():
    return "Hello World!"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
