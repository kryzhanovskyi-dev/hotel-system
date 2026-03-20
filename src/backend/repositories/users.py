from pydantic import EmailStr
from sqlalchemy import select

from backend.models.users import UsersOrm
from backend.repositories.base import BaseRepository
from backend.repositories.mappers.mappers import UserDataMapper
from backend.schemas.users import UserWithHashedPasswordSchema


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        model = (await self.session.execute(query)).scalars().one()
        return UserWithHashedPasswordSchema.model_validate(model)
