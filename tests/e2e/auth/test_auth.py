import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("k1@gmail.com", "k1", 200),
        ("k1@gmail.com", "k1", 400),
        ("k2@gmail.com", "k2", 200),
        ("wggegegew", "k2", 422),
    ],
)
async def test_auth_flow(
    email: str,
    password: str,
    status_code: int,
    ac,
):
    # /register
    reg_res = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert reg_res.status_code == status_code
    if reg_res.status_code != 200:
        return

    # /login
    log_res = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert log_res.status_code == 200
    assert ac.cookies["access_token"]
    assert "access_token" in log_res.json()

    # /me
    authme_res = await ac.get("/auth/me")
    user = authme_res.json()
    assert log_res.status_code == 200
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    logout_res = await ac.post("/auth/logout")
    assert log_res.status_code == 200
    assert "access_token" not in logout_res.cookies

    # /me
    authme_res = await ac.get("/auth/me")
    assert log_res.status_code == 200
    assert authme_res.json()["detail"] == "No token"
