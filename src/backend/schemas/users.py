from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAddSchema(BaseModel):
    email: EmailStr
    password: str


class UserAddSchema(BaseModel):
    email: EmailStr
    hashed_password: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPasswordSchema(UserSchema):
    hashed_password: str
