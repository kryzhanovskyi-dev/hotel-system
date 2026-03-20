# ruff: noqa: E402
import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from httpx import AsyncClient, ASGITransport
import pytest

from backend.api.dependencies import get_db
from backend.config import settings
from backend.database import Base, engine_null_pool, async_session_maker_null_pool
from backend.models import *  # noqa
from backend.main import app
from backend.schemas.hotels import HotelAddSchema
from backend.schemas.rooms import RoomAddSchema
from backend.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mod():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture()
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mod):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def add_mock_hotels(setup_database):
    with open("tests/mock_hotels.json", "r", encoding="utf-8") as f:
        hotels = json.load(f)

    hotels_ = [HotelAddSchema.model_validate(hotel) for hotel in hotels]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels_)
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def add_mock_rooms(setup_database):
    with open("tests/mock_rooms.json", "r", encoding="utf-8") as f:
        rooms = json.load(f)

    rooms_ = [RoomAddSchema.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.rooms.add_bulk(rooms_)
        await db.commit()


# @pytest.fixture(scope="session", autouse=True)
# async def add_mock_rooms(setup_database):
#     async with engine_null_pool.begin() as conn:
#         with open("tests/mock_rooms.json", "r", encoding="utf-8") as f:
#             rooms_stmt = insert(RoomsOrm).values(json.load(f))
#             await conn.execute(rooms_stmt)


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "test@gmail.com",
            "password": "12345",
        },
    )


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac) -> AsyncClient:
    response = await ac.post(
        "/auth/login",
        json={
            "email": "test@gmail.com",
            "password": "12345",
        },
    )
    assert ac.cookies.get("access_token") == response.cookies.get("access_token")
    yield ac
