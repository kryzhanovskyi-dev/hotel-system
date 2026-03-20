from fastapi import APIRouter

from fastapi_cache.decorator import cache

from backend.api.dependencies import DBDep
from backend.schemas.facilities import FacilityAddSchema
from backend.tasks.tasks import task_task

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def create_facility(
    db: DBDep,
    facility_data: FacilityAddSchema
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    task_task.delay()

    return {"status": "ok", "data": facility}
