from datetime import date

from backend.schemas.bookings import BookingAddSchema


async def test_boooking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    #create
    booking_data = BookingAddSchema(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=3, day=25),
        date_to=date(year=2026, month=5, day=1),
        price=100,
    )
    booking_added = await db.bookings.add(booking_data)

    #read
    booking_read = await db.bookings.get_one_or_none(id=booking_added.id)
    assert booking_read
    assert booking_read.id == booking_added.id
    assert booking_read.room_id == booking_added.room_id
    assert booking_read.user_id == booking_added.user_id

    #update
    updated_price = 250
    updated_booking_data = BookingAddSchema(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=3, day=25),
        date_to=date(year=2026, month=5, day=1),
        price=updated_price,
    )
    await db.bookings.edit(updated_booking_data, id=booking_added.id)
    updated_booking = await db.bookings.get_one_or_none(id=booking_added.id)
    assert updated_booking
    assert updated_booking.id == booking_added.id
    assert updated_booking.price == updated_price

    #delete
    await db.bookings.delete(id=booking_added.id)
    deleted_booking = await db.bookings.get_one_or_none(id=booking_added.id)
    assert not deleted_booking

    await db.rollback() 
