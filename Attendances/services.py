import sqlalchemy.orm as _orm
from . import schemas as _schemas
from . import models as _models
from main import get_db
from Users import services as _user_services


async def create_rsvp(db: _orm.Session, rsvp: _schemas.RsvpCreate, user_id: int):
    rsvp_obj = _models.Attendance(**rsvp.dict(), user_id=user_id)
    db.add(rsvp_obj)
    db.commit()
    db.refresh(rsvp_obj)
    return _schemas.Rsvp.from_orm(rsvp_obj)


async def get_rsvp_by_user_and_event(db: _orm.Session, user_id: int, event_id: int):
    return db.query(_models.Attendance).filter(_models.Attendance.user_id == user_id,
                                               _models.Attendance.event_id == event_id).first()


async def get_rsvps_by_user(db: _orm.Session, user_id: int):
    return db.query(_models.Attendance).filter(_models.Attendance.user_id == user_id).all()
