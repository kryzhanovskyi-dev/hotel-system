from datetime import date

from fastapi import Query, APIRouter, Body

from fastapi_cache.decorator import cache

from backend.schemas.hotels import HotelAddSchema, HotelPATCHSchema
from backend.api.dependencies import PaginationDep, DBDep


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Hotel's name"),
    location: str | None = Query(None, description="Hotel's location"),
    date_from: date = Query(example="2026-01-01"),
    date_to: date = Query(example="2026-01-05"),
):
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )

@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(db: DBDep, data: HotelAddSchema = Body(openapi_examples={
    "1": {"summary": "Odesa's example", "value": {
    "title": "Odesa",
    "location": "odesa",}},
    "2": {"summary": "Kyiv's example", "value": {
    "title": "Kyiv",
    "location": "kyiv",}},
})):
    hotel = await db.hotels.add(data)
    await db.commit()
    return {"status": "ok", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(db: DBDep, hotel_id: int, data: HotelAddSchema):
    await db.hotels.edit(data, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.patch(
    "/{hotel_id}",
    summary="Partially hotels' editing",
    description="<h1>Partially hotels' editing - description</h1>",
)
async def patch_hotel(db: DBDep, hotel_id: int, data: HotelPATCHSchema):
    await db.hotels.edit(data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    return {"status": "ok"}