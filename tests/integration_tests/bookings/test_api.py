import pytest

from tests.conftest import get_db_null_pool


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.session.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2026-03-25", "2026-05-01", 200),
        (1, "2026-03-25", "2026-05-01", 200),
        (1, "2026-03-25", "2026-05-01", 200),
        (1, "2026-03-25", "2026-05-01", 200),
        (1, "2026-03-25", "2026-05-01", 200),
        (1, "2026-03-25", "2026-05-01", 500),
    ],
)
async def test_post_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    authenticated_ac,
):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    res_json = response.json()

    assert response.status_code == status_code
    if status_code == 200:
        assert res_json["status"] == "ok"
        assert isinstance(res_json, dict)
        assert "data" in res_json


@pytest.mark.parametrize(
    "room_id, date_from, date_to, bookings_count",
    [
        (1, "2026-03-25", "2026-05-01", 1),
        (1, "2026-03-25", "2026-05-01", 2),
        (1, "2026-03-25", "2026-05-01", 3),
        (1, "2026-03-25", "2026-05-01", 4),
        (1, "2026-03-25", "2026-05-01", 5),
    ],
)
async def test_post_and_get_my_bookings(
    room_id,
    date_from,
    date_to,
    bookings_count,
    authenticated_ac,
    delete_all_bookings,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200

    response_my_bookings = await authenticated_ac.get("/bookings/me")

    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == bookings_count
