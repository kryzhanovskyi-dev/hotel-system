async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2026-03-25",
            "date_to": "2026-05-01",
        },
    )

    assert response.status_code == 200
