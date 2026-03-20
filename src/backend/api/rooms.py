from datetime import date

from fastapi import APIRouter, Body, Query

from backend.schemas.facilities import RoomFacilityAddSchema
from backend.schemas.rooms import RoomAddRequestSchema, RoomAddSchema, RoomPatchSchema, RoomPatchRequestSchema
from backend.api.dependencies import DBDep


router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Rooms"])


@router.get("")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2026-01-01"),
    date_to: date = Query(example="2026-01-05"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    
@router.get("/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)


@router.post("")
async def create_room(
    db: DBDep,
    hotel_id: int,
    data: RoomAddRequestSchema = Body(openapi_examples={})
):
    _data = RoomAddSchema(hotel_id=hotel_id, **data.model_dump())
    room = await db.rooms.add(_data)

    rooms_facilities_data = [RoomFacilityAddSchema(room_id=room.id, facility_id=f_id) for f_id in data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    
    return {"status": "ok", "data": room}


@router.put("/{room_id}")
async def put_room(db: DBDep, hotel_id: int, room_id: int, data: RoomAddRequestSchema):
    _data = RoomAddSchema(hotel_id=hotel_id, **data.model_dump())
    await db.rooms.edit(_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=data.facilities_ids)
    await db.commit()
    return {"status": "ok"}


@router.patch(
    "/{room_id}",
    summary="Partially hotels' editing",
    description="<h1>Partially hotels' editing - description</h1>",
)
async def patch_room(db: DBDep, hotel_id: int, room_id: int, data: RoomPatchRequestSchema):
    _room_data_dict = data.model_dump(exclude_unset=True)
    _data = RoomPatchSchema(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])
        
    await db.commit()
    return {"status": "ok"}


@router.delete("/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    return {"status": "ok"}
