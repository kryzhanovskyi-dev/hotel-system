from datetime import date

from sqlalchemy import select

from backend.models.hotels import HotelsOrm
from backend.models.rooms import RoomsOrm
from backend.repositories.base import BaseRepository
from backend.repositories.mappers.mappers import HotelDataMapper
from backend.repositories.utils import rooms_ids_for_booking
from backend.schemas.hotels import HotelSchema


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper
    
    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location,
            title,
            limit,
            offset,
    ) -> list[HotelSchema]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))
        if title:
            query = query.filter(HotelsOrm.title.icontains(title))
        if location:
            query = query.filter(HotelsOrm.location.icontains(location))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
    