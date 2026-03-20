from fastapi import APIRouter

from backend.schemas.bookings import BookingAddRequestSchema, BookingAddSchema
from backend.api.dependencies import DBDep, UserIdDep


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return bookings


@router.get("/me")
async def get_my_bookings(
    user_id: UserIdDep,
    db: DBDep,
):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return bookings


@router.post("")
async def create_booking(user_id: UserIdDep, db: DBDep, data: BookingAddRequestSchema):
    room = await db.rooms.get_one_or_none(id=data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    room_price: int = room.price
    _data = BookingAddSchema(user_id=user_id, price=room_price, **data.model_dump())
    booking = await db.bookings.add_booking(data=_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "ok", "data": booking}
