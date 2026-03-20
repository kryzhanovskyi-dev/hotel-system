from datetime import date
from pydantic import BaseModel, ConfigDict


class BookingAddRequestSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAddSchema(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class BookingSchema(BookingAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
