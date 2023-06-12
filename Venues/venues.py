import fastapi as _fastapi

import sqlalchemy.orm as _orm

from . import services as _services
from . import schemas as _schemas
from main import app
from .services import _user_services, _event_services
from Users import schemas as _user_schemas


@app.post("/api/create_venue", response_model=_schemas.Venue)
async def create_venue(venue: _schemas.VenueCreate, db: _orm.Session = _fastapi.Depends(_services.get_db),
                       current_user: _user_schemas.User = _fastapi.Depends(_user_services.get_current_user)
                       ):
    return await _services.create_venue(db=db, venue=venue, owner_id=current_user.id)


@app.post("/api/create_event_venue/{event_id}", response_model=_schemas.Venue)
async def create_venue(
        event_id: int,
        venue: _schemas.VenueCreate, db: _orm.Session = _fastapi.Depends(_services.get_db),
        current_user: _user_schemas.User = _fastapi.Depends(_user_services.get_current_user),
):
    venue = await _services.create_venue(db=db, venue=venue, owner_id=current_user.id)
    # get event by id and check if it exists
    event = await _event_services.get_event_by_id(db=db, event_id=event_id)
    if not event:
        raise _fastapi.HTTPException(status_code=404, detail="Event not found")
    # check if the event already has a venue
    if event.venue:
        raise _fastapi.HTTPException(status_code=400, detail="Event already has a venue. update instead")
    # check if the user is the owner of the event
    if event.owner_id != current_user.id:
        raise _fastapi.HTTPException(status_code=401, detail="Unauthorized")

    await _services.create_event_venue(db=db, event=event, venue_id=venue.id)
    return venue
