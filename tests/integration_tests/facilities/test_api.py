


async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_post_facility(ac):
    title = "TEST"
    response = await ac.post(
        "/facilities",
        json={
            "title": title, 
        }
    )
    res_json = response.json()

    assert response.status_code == 200
    assert res_json["status"] == "ok"
    assert isinstance(res_json, dict)
    assert "data" in res_json
    assert res_json["data"]["title"] == title
