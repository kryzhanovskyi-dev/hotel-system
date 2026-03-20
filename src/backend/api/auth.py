from fastapi import APIRouter, HTTPException, Response

from backend.api.dependencies import UserIdDep, DBDep
from backend.services.auth import AuthService
from backend.schemas.users import UserAddSchema, UserRequestAddSchema


router = APIRouter(prefix="/auth", tags=["Authentification and autorization"])  # dependencies=[]


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAddSchema):
    try:
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAddSchema(email=data.email, hashed_password=hashed_password)
        await db.users.add(new_user_data)
        await db.commit()
    except:  # noqa: E722
        raise HTTPException(status_code=400)

    return {"status": "ok"}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserRequestAddSchema,
    response: Response,
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Password incorrect")

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "ok"}


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user
