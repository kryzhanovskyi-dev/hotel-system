from backend.schemas.hotels import HotelAddSchema


async def test_add_hotel(db):
    hotel_data = HotelAddSchema(title="Hotel Arc", location="Odesa")
    await db.hotels.add(hotel_data)
    await db.commit()
