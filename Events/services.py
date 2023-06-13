import sqlalchemy.orm as _orm
from . import schemas as _schemas
from . import models as _models
from database import get_db
from Users import services as _user_services

async def create_event(db: _orm.Session, event: _schemas.EventCreate, owner_id: int):
    event_obj = _models.Event(**event.dict(), owner_id=owner_id)
    db.add(event_obj)
    db.commit()
    db.refresh(event_obj)
    return _schemas.Event.from_orm(event_obj)


async def get_event_by_id(db: _orm.Session, event_id: int):
    return db.get(_models.Event, event_id)


async def get_all_events(db: _orm.Session):
    return db.query(_models.Event).all()


async def get_events_by_owner(db: _orm.Session, owner_id: int):
    return db.query(_models.Event).filter(_models.Event.owner_id == owner_id).all()


async def update_event(db: _orm.Session, event: _schemas.EventUpdate, db_event):
    for key, value in event.dict().items():
        setattr(db_event, key, value)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return _schemas.Event.from_orm(db_event)


async def get_event_by_date(db: _orm.Session, date: str):
    return db.query(_models.Event).filter(_models.Event.date == date).all()
