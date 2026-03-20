from pydantic import BaseModel, ConfigDict


class FacilityAddSchema(BaseModel):
    title: str

class FacilitySchema(FacilityAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomFacilityAddSchema(BaseModel):
    room_id: int
    facility_id: int

class RoomFacilitySchema(RoomFacilityAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
