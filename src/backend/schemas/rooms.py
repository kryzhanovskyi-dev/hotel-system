from pydantic import BaseModel, ConfigDict

from backend.schemas.facilities import FacilitySchema


class RoomAddRequestSchema(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomAddSchema(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomSchema(RoomAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRelsSchema(RoomSchema):
    facilities: list[FacilitySchema]


class RoomPatchRequestSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class RoomPatchSchema(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
