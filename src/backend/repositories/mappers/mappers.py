from backend.models.bookings import BookingsOrm
from backend.models.facilities import FacilitiesOrm
from backend.models.hotels import HotelsOrm
from backend.models.rooms import RoomsOrm
from backend.models.users import UsersOrm
from backend.repositories.mappers.base import DataMapper
from backend.schemas.bookings import BookingSchema
from backend.schemas.facilities import FacilitySchema
from backend.schemas.hotels import HotelSchema
from backend.schemas.rooms import RoomSchema, RoomWithRelsSchema
from backend.schemas.users import UserSchema


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = HotelSchema

class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomSchema

class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRelsSchema

class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserSchema

class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = BookingSchema

class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = FacilitySchema
    