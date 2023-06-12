import sqlalchemy.orm as _orm
from . import schemas as _schemas
from . import models as _models
from main import get_db
from Users import services as _user_services
from Events import services as _event_services


async def create_venue(db: _orm.Session, venue: _schemas.VenueCreate, owner_id: int):
    venue_obj = _models.Venue(**venue.dict(), owner_id=owner_id)
    db.add(venue_obj)
    db.commit()
    db.refresh(venue_obj)
    return _schemas.Venue.from_orm(venue_obj)


async def create_event_venue(db: _orm.Session, event, venue_id: int):
    event.venue_id = venue_id
    db.add(event)
    db.commit()
    db.refresh(event)


async def get_venue_by_id(db: _orm.Session, venue_id: int):
    venue = db.get(_models.Venue, venue_id)
    return venue


async def get_all_venues(db: _orm.Session, offset: int = 0, limit: int = 100):
    venues = db.query(_models.Venue).all()
    return venues


async def get_user_venues(db: _orm.Session, owner_id: int, offset: int = 0, limit: int = 100):
    venues = db.query(_models.Venue).filter(_models.Venue.owner_id == owner_id).offset(offset).limit(limit).all()
    return venues
