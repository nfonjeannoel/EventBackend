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
    #     update the event with the venue_id
    event.venue_id = venue_id
    db.add(event)
    db.commit()
    db.refresh(event)
    # return _schemas.Event.from_orm(event)
