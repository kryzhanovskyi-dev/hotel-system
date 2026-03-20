from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from backend.models.rooms import RoomsOrm
from backend.repositories.base import BaseRepository
from backend.repositories.mappers.mappers import (
    RoomDataMapper,
    RoomWithRelsDataMapper,
)
from backend.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"Literal_bind": True}))

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        res = await self.session.execute(query)
        return [
            RoomWithRelsDataMapper.map_to_domain_entity(model)
            for model in res.unique().scalars().all()
        ]

    async def get_one_or_none_with_rels(self, **filter_by):
        query = (
            select(self.model).filter_by(**filter_by).options(selectinload(self.model.facilities))
        )
        model = (await self.session.execute(query)).scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRelsDataMapper.map_to_domain_entity(model)
